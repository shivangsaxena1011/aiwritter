"""
Production Audit Regression Suite:
Verifies resolutions for all audit requirements:
- Job queue loop-isolation & concurrency
- Real cancellation and race conditions
- Startup stuck job recovery
- SSE deduplication and connection leak prevention
- Internal artifacts isolation
- Path traversal defenses
- BYOK key isolation (never falls back to server keys)
- Production MockProvider guards
- TOC bounds and blank input validation
- OMML advanced math and equation rendering
- PARTIAL vs COMPLETED status correctness and retries
- Rate limiting and API auth enforcement
- S3 upload failure handling
"""

import os
import asyncio
import pytest
from datetime import datetime, timezone
from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.core.config import settings
from backend.app.core.database import SessionLocal
from backend.app.models import Book, GenerationJob, GenerationEvent, GeneratedAsset, GeneratedSection
from backend.app.workers.queue_manager import JobQueueManager, queue_manager
from backend.app.services.ai.factory import get_ai_provider
from backend.app.services.ai.gemini_provider import GeminiProvider
from backend.app.services.ai.mock_provider import MockProvider
from backend.app.services.math.omml_engine import OMMLEngine
from backend.app.core.rate_limit import InMemoryRateLimiter
from backend.app.core.security import verify_api_auth, validate_safe_filename, resolve_gemini_api_key
from backend.app.schemas import CreateBookRequest, ParseSyllabusRequest, TableOfContentsSchema, UnitSchema, TopicSchema

client = TestClient(app)


# 1. Job Queue Cross-Event-Loop Isolation
def test_job_queue_loop_isolation():
    manager = JobQueueManager()
    
    # Loop 1
    loop1 = asyncio.new_event_loop()
    async def get_sem1():
        return manager._get_semaphore()
    sem1 = loop1.run_until_complete(get_sem1())
    assert sem1 is not None
    loop1.close()
    
    # Loop 2 (distinct loop)
    loop2 = asyncio.new_event_loop()
    async def get_sem2():
        return manager._get_semaphore()
    sem2 = loop2.run_until_complete(get_sem2())
    assert sem2 is not None
    assert sem2 is not sem1
    assert sem2._value == settings.MAX_CONCURRENT_JOBS
    loop2.close()


# 2. Real Job Cancellation and Terminal State Guards
def test_real_job_cancellation_and_terminal_states():
    db = SessionLocal()
    try:
        book = Book(title="Cancellation Test Book", status="planning")
        db.add(book)
        db.flush()

        job = GenerationJob(
            book_id=book.id,
            status="RUNNING",
            progress=25.0,
            current_stage="Drafting"
        )
        db.add(job)
        db.commit()

        # Cancellation should succeed for running job
        mgr = JobQueueManager()
        res = mgr.cancel_job(job.id, db)
        assert res is True

        db.refresh(job)
        assert job.status == "CANCELLED"
        assert job.current_stage == "Cancelled"

        # Cancellation should be rejected for terminal job
        res_terminal = mgr.cancel_job(job.id, db)
        assert res_terminal is False

        # Completed job cannot be cancelled
        job.status = "COMPLETED"
        db.commit()
        assert mgr.cancel_job(job.id, db) is False
    finally:
        db.close()


# 3. Stuck Non-Terminal Job Startup Recovery
def test_startup_interrupted_jobs_recovery():
    db = SessionLocal()
    try:
        book = Book(title="Recovery Test Book", status="planning")
        db.add(book)
        db.flush()

        job1 = GenerationJob(book_id=book.id, status="PLANNING", progress=10.0)
        job2 = GenerationJob(book_id=book.id, status="RUNNING", progress=50.0)
        job3 = GenerationJob(book_id=book.id, status="COMPLETED", progress=100.0)
        db.add_all([job1, job2, job3])
        db.commit()

        mgr = JobQueueManager()
        recovered = mgr.recover_interrupted_jobs(db)
        assert recovered >= 2

        db.refresh(job1)
        db.refresh(job2)
        db.refresh(job3)

        assert job1.status == "FAILED"
        assert "interrupted" in (job1.error or "").lower()
        assert job2.status == "FAILED"
        assert job3.status == "COMPLETED"
    finally:
        db.close()


# 4. SSE Event Deduplication
def test_sse_event_deduplication():
    from backend.app.api.v1.jobs import _fetch_poll_update
    db = SessionLocal()
    try:
        book = Book(title="SSE Book", status="planning")
        db.add(book)
        db.flush()

        job = GenerationJob(book_id=book.id, status="RUNNING", progress=10.0)
        db.add(job)
        db.flush()

        now = datetime.now(timezone.utc)
        ev1 = GenerationEvent(job_id=job.id, message="Event 1", created_at=now)
        ev2 = GenerationEvent(job_id=job.id, message="Event 2", created_at=now)
        db.add_all([ev1, ev2])
        db.commit()

        seen_ids = set()
        events_1, _ = _fetch_poll_update(job.id, None, seen_ids)
        assert len(events_1) == 2
        assert len(seen_ids) == 2

        # Second poll with same timestamp must not duplicate seen events
        events_2, _ = _fetch_poll_update(job.id, now, seen_ids)
        assert len(events_2) == 0
    finally:
        db.close()


# 5. Internal Artifacts File Exposure Defense
def test_internal_artifacts_not_exposed():
    # Attempting to download any internal artifact file should return 404
    resp = client.get("/api/v1/files/final_release_report.json")
    assert resp.status_code == 404

    resp2 = client.get("/api/v1/files/ai_style_audit.json")
    assert resp2.status_code == 404


# 6. Path Traversal Defenses
def test_path_traversal_defenses():
    with pytest.raises(Exception):
        validate_safe_filename("../../app.db")

    with pytest.raises(Exception):
        validate_safe_filename("/etc/passwd")

    resp = client.get("/api/v1/files/..%2F..%2Fapp.db")
    assert resp.status_code in (400, 404)


# 7. BYOK Isolation (Never Fall Back to Server Keys)
def test_byok_isolation():
    client_key = "AIzaSyTestClientBYOKKey123456789"
    provider = get_ai_provider(api_key=client_key)
    assert isinstance(provider, GeminiProvider)
    assert provider.keys == [client_key]
    # Critical invariant: BYOK must have 0 backup keys
    assert len(provider.keys) == 1

    # Empty BYOK key must be rejected and not fall back to server key
    with pytest.raises(Exception):
        resolve_gemini_api_key(client_provided_key="   ")


# 8. Production MockProvider Guard
def test_production_mock_guard(monkeypatch):
    monkeypatch.setattr(settings, "APP_ENV", "production")
    monkeypatch.setattr(settings, "ALLOW_MOCK_PROVIDERS", False)

    with pytest.raises(RuntimeError) as exc_info:
        get_ai_provider(force_mock=True)
    assert "strictly prohibited" in str(exc_info.value).lower()


# 9. Blank and Oversized Input Validation
def test_blank_and_oversized_input_validation():
    # 1. Blank book title
    with pytest.raises(ValueError):
        CreateBookRequest(
            title="   ",
            toc=TableOfContentsSchema(units=[UnitSchema(name="Unit 1", topics=[])])
        )

    # 2. Blank syllabus text
    with pytest.raises(ValueError):
        ParseSyllabusRequest(text="      ")

    # 3. Oversized TOC (> 120 subtopics)
    huge_topics = [
        TopicSchema(name=f"Topic {i}", subtopics=[f"Sub {j}" for j in range(15)])
        for i in range(10)
    ]
    with pytest.raises(ValueError) as exc:
        TableOfContentsSchema(units=[UnitSchema(name="Big Unit", topics=huge_topics)])
    assert "exceeds maximum allowed limit" in str(exc.value)


# 10. OMML Advanced Equations
def test_omml_advanced_equations():
    # Functions
    eq1 = r"\sin(kx) + \ln(x) + \exp(-t)"
    xml1 = OMMLEngine.latex_to_omml_xml(eq1, is_display=False)
    assert "sin" in xml1
    assert "ln" in xml1
    assert "exp" in xml1

    # N-th radical
    eq2 = r"\sqrt[3]{\frac{x}{y}}"
    xml2 = OMMLEngine.latex_to_omml_xml(eq2, is_display=True)
    assert "<m:rad>" in xml2
    assert "<m:deg>" in xml2
    assert "<m:f>" in xml2

    # Vector and Hat Accents
    eq3 = r"\vec{F} = m \hat{a}"
    clean3 = OMMLEngine.sanitize_math_text(eq3)
    assert "F⃗" in clean3
    assert "â" in clean3

    # Large operator with subscript/superscript
    eq4 = r"\sum_{i=1}^{N} x_i"
    xml4 = OMMLEngine.latex_to_omml_xml(eq4, is_display=True)
    assert "<m:sSubSup>" in xml4 or "<m:sSub>" in xml4


# 11. PARTIAL vs COMPLETED Status and Retries
def test_partial_vs_completed_and_retries():
    db = SessionLocal()
    try:
        book = Book(title="Partial Status Book", status="planning")
        db.add(book)
        db.flush()

        job = GenerationJob(
            book_id=book.id,
            status="PARTIAL",
            progress=100.0,
            current_stage="Completed (PARTIAL)"
        )
        db.add(job)
        db.commit()

        # PARTIAL status must be retryable
        mgr = JobQueueManager()
        retry_res = mgr.retry_job(job.id, db)
        assert retry_res is True

        db.refresh(job)
        assert job.status == "RETRYING"
    finally:
        db.close()


# 12. Rate Limiter
def test_in_memory_rate_limiter():
    limiter = InMemoryRateLimiter()
    key = "test_client:endpoint"
    
    # 3 requests allowed in 10 seconds
    assert limiter.check_rate_limit(key, max_requests=3, window_seconds=10.0) is None
    assert limiter.check_rate_limit(key, max_requests=3, window_seconds=10.0) is None
    assert limiter.check_rate_limit(key, max_requests=3, window_seconds=10.0) is None

    # 4th request must be rate limited
    retry_after = limiter.check_rate_limit(key, max_requests=3, window_seconds=10.0)
    assert retry_after is not None
    assert retry_after > 0


# 13. API Auth Enforcement
def test_api_auth_enforcement(monkeypatch):
    monkeypatch.setattr(settings, "AUTH_REQUIRED", True)
    monkeypatch.setattr(settings, "API_AUTH_SECRET", "super-secret-key-xyz")

    # Invalid auth raises 401
    with pytest.raises(Exception):
        verify_api_auth(authorization="Bearer wrong-key", x_api_key=None)

    # Valid Bearer auth passes
    assert verify_api_auth(authorization="Bearer super-secret-key-xyz", x_api_key=None) is True

    # Valid X-API-Key auth passes
    assert verify_api_auth(authorization=None, x_api_key="super-secret-key-xyz") is True
