"""
End-to-End Acceptance Test for AIWritter Engine.
Executes complete autonomous pipeline for academic syllabus:
SyllabusAnalysis -> TopicDecomposition -> WebResearch -> Planning -> ContentWriting ->
Derivations -> DiagramGeneration -> QualityReview -> FactCheck -> Consistency -> DOCX -> Validation.
"""

import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.app.core.database import Base
from backend.app.models import (
    Book, BookUnit, BookTopic, BookSubtopic, GenerationJob, GeneratedAsset, DocumentExport
)
from backend.app.services.ai.mock_provider import MockProvider
from backend.app.workers.pipeline import BookGenerationOrchestrator
from backend.app.agents.document_validation_agent import DocumentValidationAgent

@pytest.mark.asyncio
async def test_complete_e2e_academic_book_pipeline(tmp_path):
    # 1. Setup isolated SQLite in-memory/temp database
    db_file = str(tmp_path / "test_e2e.db")
    engine = create_engine(f"sqlite:///{db_file}")
    Base.metadata.create_all(bind=engine)
    TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = TestingSession()

    try:
        # 2. Seed Academic Book (Engineering Physics - Quantum Mechanics syllabus)
        book = Book(
            title="Engineering Physics: Quantum Foundations",
            subtitle="An Academic Reference Monograph",
            author="Prof. Quantum",
            academic_level="Undergraduate",
            book_metadata={
                "subject": "Engineering Physics",
                "writing_depth": "Standard",
                "research_depth": "Standard",
                "citation_style": "IEEE",
                "generate_images": True,
                "include_diagrams": True,
                "include_numericals": True,
                "include_questions": True,
                "include_examples": True,
                "include_references": True
            }
        )
        db.add(book)
        db.flush()

        # Chapter 1: Quantum Mechanics
        unit1 = BookUnit(book_id=book.id, position=1, title="Quantum Mechanics")
        db.add(unit1)
        db.flush()

        t1 = BookTopic(unit_id=unit1.id, position=1, title="Wave Nature of Particles")
        db.add(t1)
        db.flush()

        s1_1 = BookSubtopic(topic_id=t1.id, position=1, title="de Broglie Hypothesis")
        s1_2 = BookSubtopic(topic_id=t1.id, position=2, title="Matter Waves & Dispersion")
        db.add_all([s1_1, s1_2])

        t2 = BookTopic(unit_id=unit1.id, position=2, title="Schrödinger Equation & Particle in a Box")
        db.add(t2)
        db.flush()

        s2_1 = BookSubtopic(topic_id=t2.id, position=1, title="Time-Independent Schrödinger Equation")
        s2_2 = BookSubtopic(topic_id=t2.id, position=2, title="Particle in an Infinite Potential Box")
        db.add_all([s2_1, s2_2])

        # Chapter 2: Solid State Physics
        unit2 = BookUnit(book_id=book.id, position=2, title="Solid State Physics")
        db.add(unit2)
        db.flush()

        t3 = BookTopic(unit_id=unit2.id, position=1, title="Band Theory of Solids")
        db.add(t3)
        db.flush()

        s3_1 = BookSubtopic(topic_id=t3.id, position=1, title="Kronig-Penney Model & Energy Bands")
        db.add(s3_1)

        # 3. Create Generation Job
        job = GenerationJob(
            book_id=book.id,
            status="CREATED",
            progress=0.0
        )
        db.add(job)
        db.commit()

        # 4. Execute Orchestrator Pipeline with MockProvider
        ai_provider = MockProvider()
        orchestrator = BookGenerationOrchestrator(job_id=job.id, db=db, ai_provider=ai_provider)
        await orchestrator.execute()

        # 5. Verify Job Outcomes in Database
        db.refresh(job)
        assert job.status in ("COMPLETED", "PARTIAL")
        assert job.progress == 100.0

        # Verify Generated DOCX Asset
        docx_asset = db.query(GeneratedAsset).filter(
            GeneratedAsset.job_id == job.id,
            GeneratedAsset.type == "docx"
        ).first()
        assert docx_asset is not None
        assert os.path.exists(os.path.join(orchestrator.storage.local_dir, docx_asset.storage_key))

        docx_path = os.path.join(orchestrator.storage.local_dir, docx_asset.storage_key)

        # 6. Programmatic Quality & Layout Validation
        validation = DocumentValidationAgent.validate_docx(
            docx_path=docx_path,
            expected_chapters=2,
            expected_topics=5,
            include_diagrams=True
        )

        assert validation["total_paragraphs"] > 10
        assert validation["total_equations"] >= 1
        assert validation["total_tables"] >= 1
        assert "Times New Roman" in validation["detected_fonts"]
        assert validation["overall_score"] >= 80.0

    finally:
        db.close()
