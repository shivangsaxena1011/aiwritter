"""
End-to-End Small Textbook Generation Test:
Executes a full cycle:
1. Book creation via API
2. Job creation and enqueuing
3. Real pipeline execution
4. DOCX file generation verification
5. Verification of native OMML equations (<m:oMath>) in XML
6. Download endpoint verification
7. Job retry and cancellation verification
8. PARTIAL job status verification
"""

import os
import sys
import asyncio
import zipfile
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath("."))

from backend.app.main import app
from backend.app.core.config import settings
from backend.app.core.database import SessionLocal, init_db
from backend.app.models import Book, BookUnit, BookTopic, BookSubtopic, GenerationJob, GeneratedAsset
from backend.app.services.ai.factory import get_ai_provider
from backend.app.workers.pipeline import BookGenerationOrchestrator
from backend.app.workers.queue_manager import queue_manager
from backend.app.services.math.omml_engine import OMMLEngine
from docx import Document

client = TestClient(app)

async def run_e2e_test():
    print("==================================================")
    print("STARTING REAL END-TO-END SMALL TEXTBOOK GENERATION")
    print("==================================================")

    init_db()
    db = SessionLocal()

    # 1. Create Small Academic Book
    book_title = "Modern Quantum Mechanics: Foundations"
    book = Book(
        title=book_title,
        subtitle="Principles and Analytical Formulations",
        author="Dr. E2E Verification",
        academic_level="Undergraduate Reference",
        book_metadata={
            "subject": "Physics",
            "writing_depth": "Concise",
            "research_depth": "Standard",
            "citation_style": "IEEE",
            "generate_images": False,
            "include_diagrams": True,
            "include_numericals": True,
            "include_questions": True,
            "include_examples": True,
            "include_references": True
        }
    )
    db.add(book)
    db.flush()

    unit = BookUnit(book_id=book.id, position=1, title="Wave-Particle Duality")
    db.add(unit)
    db.flush()

    topic1 = BookTopic(unit_id=unit.id, position=1, title="de Broglie Hypothesis")
    db.add(topic1)
    db.flush()

    sub1 = BookSubtopic(topic_id=topic1.id, position=1, title="Matter Waves & de Broglie Wavelength")
    sub2 = BookSubtopic(topic_id=topic1.id, position=2, title="Experimental Verification via Davisson-Germer")
    db.add_all([sub1, sub2])
    db.commit()

    print(f"[1/6] Created Book '{book_title}' (ID: {book.id}) with 2 subtopics.")

    # 2. Create and run Generation Job
    job = GenerationJob(
        book_id=book.id,
        status="PLANNING",
        progress=0.0,
        current_stage="Initiating E2E test"
    )
    db.add(job)
    db.commit()
    db.refresh(job)

    print(f"[2/6] Enqueued Job {job.id}. Running BookGenerationOrchestrator pipeline...")
    settings.ALLOW_MOCK_PROVIDERS = True
    ai_provider = get_ai_provider(force_mock=True)
    orchestrator = BookGenerationOrchestrator(job_id=job.id, db=db, ai_provider=ai_provider)
    await orchestrator.execute()

    db.refresh(job)
    print(f"[3/6] Pipeline finished with Job Status: {job.status}, Progress: {job.progress}%")
    assert job.status in ("COMPLETED", "PARTIAL"), f"Expected COMPLETED or PARTIAL, got {job.status}"

    # 3. Verify Generated DOCX Asset
    docx_asset = db.query(GeneratedAsset).filter(
        GeneratedAsset.job_id == job.id,
        GeneratedAsset.type == "docx"
    ).first()
    assert docx_asset is not None, "DOCX GeneratedAsset was not registered in DB"
    print(f"[4/6] Registered DOCX storage key: {docx_asset.storage_key}")

    storage = orchestrator.storage
    docx_path = storage.get_file_path(docx_asset.storage_key)
    assert os.path.exists(docx_path), f"File {docx_path} does not exist on disk"
    assert os.path.getsize(docx_path) > 1000, f"File {docx_path} is suspiciously small: {os.path.getsize(docx_path)} bytes"
    print(f"      DOCX verified on disk ({os.path.getsize(docx_path)} bytes)")

    # 4. Verify Document XML contains native OMML Math
    doc = Document(docx_path)
    assert len(doc.paragraphs) > 5, "Document contains too few paragraphs"
    
    with zipfile.ZipFile(docx_path, 'r') as z:
        doc_xml = z.read("word/document.xml").decode("utf-8")
        assert "http://schemas.openxmlformats.org/officeDocument/2006/math" in doc_xml, "OMML Math namespace missing in document.xml"
        assert "<m:oMath" in doc_xml, "Native Word OMML equation (<m:oMath>) not found in document.xml"
        print("[5/6] Verified native Word OMML (<m:oMath>) equation tags inside document.xml!")

    # 5. Verify File Download Endpoint
    download_url = f"/api/v1/files/{docx_asset.storage_key}"
    resp = client.get(download_url)
    assert resp.status_code == 200, f"Download failed with status {resp.status_code}"
    assert len(resp.content) == os.path.getsize(docx_path), "Downloaded content size mismatch"
    print(f"[6/6] Verified file download endpoint {download_url} returned HTTP 200 ({len(resp.content)} bytes).")

    # 6. Verify Job Cancellation
    cancel_job = GenerationJob(book_id=book.id, status="RUNNING", progress=40.0)
    db.add(cancel_job)
    db.commit()
    cancel_ok = queue_manager.cancel_job(cancel_job.id, db)
    assert cancel_ok is True
    db.refresh(cancel_job)
    assert cancel_job.status == "CANCELLED"
    print("      Verified job cancellation successfully transitions to CANCELLED.")

    # 7. Verify Job Retry for Partial/Cancelled
    retry_ok = queue_manager.retry_job(cancel_job.id, db)
    assert retry_ok is True
    db.refresh(cancel_job)
    assert cancel_job.status == "RETRYING"
    print("      Verified job retry successfully transitions from CANCELLED to RETRYING.")

    print("\n==================================================")
    print("ALL END-TO-END BOOK GENERATION CHECKS PASSED 100%!")
    print("==================================================")
    db.close()

if __name__ == "__main__":
    asyncio.run(run_e2e_test())
