import pytest
from datetime import datetime, timezone
from backend.app.core.database import SessionLocal, init_db
from backend.app.models import Book, GenerationJob, GenerationEvent
from backend.app.workers.queue_manager import queue_manager

@pytest.fixture(scope="module")
def db_session():
    init_db()
    session = SessionLocal()
    yield session
    session.close()

def test_job_lifecycle_and_cancellation(db_session):
    # 1. Create a dummy book
    book = Book(
        title="Test Architecture Book",
        academic_level="Undergraduate",
        status="DRAFT"
    )
    db_session.add(book)
    db_session.commit()
    db_session.refresh(book)

    # 2. Create job
    job = GenerationJob(
        book_id=book.id,
        status="QUEUED",
        progress=0.0,
        current_stage="Queued in test",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )
    db_session.add(job)
    db_session.commit()
    db_session.refresh(job)

    assert job.status == "QUEUED"
    assert job.progress == 0.0

    # 3. Simulate job transition to GENERATING
    job.status = "GENERATING"
    job.progress = 25.0
    job.current_stage = "Writing sections"
    db_session.commit()
    db_session.refresh(job)

    assert job.status == "GENERATING"
    assert job.progress == 25.0

    # 4. Cancel job via queue manager
    cancelled = queue_manager.cancel_job(job.id, db_session)
    assert cancelled is True
    db_session.refresh(job)
    assert job.status == "CANCELLED"

    # 5. Retry cancelled job
    retried = queue_manager.retry_job(job.id, db_session)
    assert retried is True
    db_session.refresh(job)
    assert job.status in ["RETRYING", "QUEUED"]
    assert job.error is None

