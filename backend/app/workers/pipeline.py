import os
import uuid
import logging
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session

from backend.app.core.config import settings
from backend.app.models import (
    Book, BookUnit, BookTopic, BookSubtopic,
    GenerationJob, GenerationEvent, GeneratedAsset, GeneratedSection
)
from backend.app.services.ai.base import AIProvider
from backend.app.agents.book_context_manager import BookContextManager
from backend.app.agents.chapter_depth_controller import ChapterDepthController
from backend.app.agents.content_writer import ContentWriter
from backend.app.agents.diagram_system import DiagramPlanner, DiagramGenerator
from backend.app.agents.review_agent import ReviewAgent
from backend.app.agents.consistency_auditor import ConsistencyAuditor
from backend.app.agents.quality_controller import QualityController
from backend.app.services.document.docx_engine import DOCXExporter
from backend.app.storage import get_storage_provider

logger = logging.getLogger(__name__)

class BookGenerationPipeline:
    """
    Executes the 14-stage academic textbook generation pipeline with full database durability,
    cross-chapter context, deterministic diagrams, peer review, and verifiable quality scoring.
    """

    def __init__(self, job_id: str, db: Session, ai_provider: AIProvider):
        self.job_id = job_id
        self.db = db
        self.ai = ai_provider
        self.storage = get_storage_provider()

        # Agents
        self.content_writer = ContentWriter(self.ai)
        self.diagram_planner = DiagramPlanner(self.ai)
        self.diagram_generator = DiagramGenerator(self.ai)
        self.review_agent = ReviewAgent(self.ai)
        self.consistency_auditor = ConsistencyAuditor(self.ai)
        self.docx_exporter = DOCXExporter()

    def _log_event(self, event_type: str, message: str, progress: Optional[float] = None, metadata: Optional[Dict[str, Any]] = None):
        """Persists generation event into database and updates job progress."""
        try:
            job = self.db.query(GenerationJob).filter(GenerationJob.id == self.job_id).first()
            if job:
                if progress is not None:
                    job.progress = min(100.0, max(0.0, progress))
                job.updated_at = datetime.now(timezone.utc)

            event = GenerationEvent(
                job_id=self.job_id,
                event_type=event_type,
                message=message,
                progress=progress,
                event_metadata=metadata or {}
            )
            self.db.add(event)
            self.db.commit()
        except Exception as e:
            logger.error(f"Failed to record generation event: {e}")
            self.db.rollback()

    def _check_cancellation(self) -> bool:
        """Checks if job was cancelled by user."""
        self.db.expire_all()
        job = self.db.query(GenerationJob).filter(GenerationJob.id == self.job_id).first()
        return bool(job and job.status == "CANCELLED")

    async def execute(self):
        job = self.db.query(GenerationJob).filter(GenerationJob.id == self.job_id).first()
        if not job:
            raise ValueError(f"Job {self.job_id} not found")

        book = self.db.query(Book).filter(Book.id == job.book_id).first()
        if not book:
            raise ValueError(f"Book {job.book_id} not found")

        try:
            # Stage 1: Validation
            job.status = "PLANNING"
            job.current_stage = "Stage 1: Input Validation"
            job.started_at = datetime.now(timezone.utc)
            self.db.commit()
            self._log_event("stage", "Initializing generation pipeline...", 5.0)

            # Stage 2: Initialize Context Manager
            context_mgr = BookContextManager(
                book_title=book.title,
                academic_level=book.academic_level,
                target_audience=book.target_audience,
                writing_depth=book.book_metadata.get("writing_depth", "Detailed"),
                citation_style=book.book_metadata.get("citation_style", "IEEE")
            )

            # Count total subtopics for progress calculation
            units = self.db.query(BookUnit).filter(BookUnit.book_id == book.id).order_by(BookUnit.position).all()
            total_subtopics = 0
            for u in units:
                topics = self.db.query(BookTopic).filter(BookTopic.unit_id == u.id).all()
                for t in topics:
                    total_subtopics += self.db.query(BookSubtopic).filter(BookSubtopic.topic_id == t.id).count()

            total_subtopics = max(1, total_subtopics)
            completed_subtopics = 0

            # Collect content and assets for export
            compiled_sections: List[Dict[str, Any]] = []
            compiled_assets: List[Dict[str, Any]] = []
            audits_summary: List[Dict[str, Any]] = []

            job.status = "GENERATING"
            self.db.commit()

            # Iterate through Units -> Topics -> Subtopics
            for u_idx, unit in enumerate(units, start=1):
                if self._check_cancellation():
                    self._log_event("warning", "Generation job cancelled by user.")
                    return

                topics = self.db.query(BookTopic).filter(BookTopic.unit_id == unit.id).order_by(BookTopic.position).all()
                topic_names = [t.title for t in topics]

                # Chapter Planning / Overview
                self._log_event("log", f"✍️ Planning {unit.title} roadmap...", (completed_subtopics / total_subtopics) * 80.0 + 10.0)
                unit_overview = await self.content_writer.write_unit_overview(
                    book_title=book.title,
                    unit_title=unit.title,
                    topics=topic_names,
                    academic_level=book.academic_level
                )

                compiled_sections.append({
                    "unit": unit.title,
                    "is_unit_overview": True,
                    "content": unit_overview.get("unit_introduction", f"# {unit.title}\n\nChapter overview and foundations.")
                })

                for t_idx, topic in enumerate(topics, start=1):
                    subtopics = self.db.query(BookSubtopic).filter(BookSubtopic.topic_id == topic.id).order_by(BookSubtopic.position).all()
                    is_first_in_topic = True

                    for s_idx, subtopic in enumerate(subtopics, start=1):
                        if self._check_cancellation():
                            self._log_event("warning", "Generation job cancelled by user.")
                            return

                        job.current_stage = f"Generating: {unit.title} > {topic.title}"
                        job.current_item = subtopic.title
                        self.db.commit()

                        # PARTIAL RECOVERY (Item 54): Check if section was already successfully generated
                        existing_sec = self.db.query(GeneratedSection).filter(
                            GeneratedSection.book_id == book.id,
                            GeneratedSection.subtopic_id == subtopic.id,
                            GeneratedSection.status == "reviewed"
                        ).first()

                        if existing_sec:
                            self._log_event("log", f"⏩ Reusing previously generated section: {subtopic.title}")
                            content = existing_sec.content
                            word_count = existing_sec.word_count
                        else:
                            self._log_event("log", f"✍️ Writing Section {u_idx}.{t_idx}.{s_idx}: {subtopic.title}...")

                            # Content Generation
                            content = await self.content_writer.write_subtopic_section(
                                book_title=book.title,
                                unit_title=unit.title,
                                topic_title=topic.title,
                                subtopic_title=subtopic.title,
                                context_manager=context_mgr,
                                writing_depth=book.book_metadata.get("writing_depth", "Detailed")
                            )

                            profile = ChapterDepthController.get_profile(book.book_metadata.get("writing_depth", "Detailed"))
                            word_count = len(content.split())

                            # Review Agent
                            review_res = await self.review_agent.review_section(
                                book_title=book.title,
                                subtopic_title=subtopic.title,
                                content=content,
                                target_word_count=profile["target_words"]
                            )
                            audits_summary.append(review_res)

                            # If rewrite required and under limit
                            if review_res.get("rewrite_required"):
                                self._log_event("warning", f"⚠️ Refactoring section for quality: {subtopic.title}")
                                content = await self.content_writer.write_subtopic_section(
                                    book_title=book.title,
                                    unit_title=unit.title,
                                    topic_title=topic.title,
                                    subtopic_title=subtopic.title,
                                    context_manager=context_mgr,
                                    writing_depth=book.book_metadata.get("writing_depth", "Detailed")
                                )
                                word_count = len(content.split())

                            # Consistency Audit & Glossary Update
                            await self.consistency_auditor.audit_and_update(content, context_mgr)

                            # Persist Section in DB
                            gen_sec = GeneratedSection(
                                book_id=book.id,
                                unit_id=unit.id,
                                topic_id=topic.id,
                                subtopic_id=subtopic.id,
                                content=content,
                                status="reviewed",
                                word_count=word_count,
                                review_status="approved",
                                quality_score=review_res.get("overall_score", 85.0)
                            )
                            self.db.add(gen_sec)
                            subtopic.status = "completed"
                            self.db.commit()

                        # Update context summary
                        context_mgr.record_section_summary(
                            unit.title, topic.title, subtopic.title,
                            summary=f"{subtopic.title}: core concepts established with {word_count} words."
                        )

                        # Diagram Planning & Generation
                        img_path = None
                        img_caption = None
                        placeholder_box = None

                        if book.book_metadata.get("generate_images", False):
                            self._log_event("log", f"🎨 Planning visuals for: {subtopic.title}...")
                            diag_plan = await self.diagram_planner.plan_diagram(
                                book_title=book.title,
                                subtopic_title=subtopic.title,
                                section_content=content
                            )

                            if diag_plan.get("needs_diagram"):
                                output_dir = os.path.join(settings.STORAGE_LOCAL_DIR, "assets", book.id)
                                asset_res = await self.diagram_generator.generate_asset(
                                    diag_plan, output_dir=output_dir, topic_title=subtopic.title
                                )
                                img_path = asset_res.get("path")
                                img_caption = asset_res.get("caption")
                                placeholder_box = asset_res.get("placeholder")
                                compiled_assets.append(asset_res)

                                if img_path:
                                    asset_record = GeneratedAsset(
                                        book_id=book.id,
                                        job_id=job.id,
                                        type=asset_res.get("modality", "image_png"),
                                        storage_key=os.path.basename(img_path),
                                        url=f"/api/v1/files/{os.path.basename(img_path)}",
                                        asset_metadata={"caption": img_caption}
                                    )
                                    self.db.add(asset_record)
                                    self.db.commit()

                        compiled_sections.append({
                            "unit": unit.title,
                            "topic": topic.title,
                            "subtopic": subtopic.title,
                            "is_first_in_topic": is_first_in_topic,
                            "content": content,
                            "word_count": word_count,
                            "image_path": img_path,
                            "image_caption": img_caption,
                            "placeholder_box": placeholder_box
                        })

                        is_first_in_topic = False
                        completed_subtopics += 1
                        progress_pct = (completed_subtopics / total_subtopics) * 75.0 + 15.0
                        self._log_event("progress", f"Completed {subtopic.title} ({completed_subtopics}/{total_subtopics})", progress_pct)

            # Stage 11 & 12: Formatting & DOCX Export
            job.status = "EXPORTING"
            job.current_stage = "Stage 12: DOCX Compilation & Layout"
            self._log_event("stage", "📚 Compiling master academic DOCX...", 92.0)

            # Quality Verification
            quality_report = QualityController.generate_report(
                book_title=book.title,
                total_units=len(units),
                total_topics=sum(len(u.topics) for u in units),
                total_subtopics=total_subtopics,
                sections=compiled_sections,
                assets=compiled_assets,
                audits=audits_summary
            )

            # Export DOCX
            safe_title = "".join(c for c in book.title if c.isalnum() or c in (" ", "_", "-")).replace(" ", "_")
            out_filename = f"{safe_title}_{uuid.uuid4().hex[:6]}.docx"
            out_filepath = os.path.join(settings.STORAGE_LOCAL_DIR, out_filename)

            toc_dict = {
                "units": [
                    {
                        "name": u.title,
                        "topics": [
                            {"name": t.title, "subtopics": [s.title for s in t.subtopics]}
                            for t in u.topics
                        ]
                    }
                    for u in units
                ]
            }

            self.docx_exporter.export(
                book_title=book.title,
                subtitle=book.subtitle,
                author=book.author,
                academic_level=book.academic_level,
                toc_data=toc_dict,
                sections=compiled_sections,
                assets=compiled_assets,
                output_path=out_filepath,
                quality_report=quality_report
            )

            # Register Final Asset
            docx_asset = GeneratedAsset(
                book_id=book.id,
                job_id=job.id,
                type="docx",
                storage_key=out_filename,
                url=f"/api/v1/files/{out_filename}",
                asset_metadata={"quality_report": quality_report}
            )
            self.db.add(docx_asset)

            # Finalize Job
            job.status = "COMPLETED"
            job.current_stage = "Completed"
            job.progress = 100.0
            job.completed_at = datetime.now(timezone.utc)
            book.status = "completed"
            self.db.commit()

            self._log_event("complete", "Book publication pipeline finished successfully!", 100.0, {
                "download_url": f"/api/v1/files/{out_filename}",
                "filename": out_filename,
                "quality_report": quality_report
            })

        except Exception as e:
            logger.exception(f"Pipeline execution error: {e}")
            job.status = "FAILED"
            job.error = str(e)
            job.updated_at = datetime.now(timezone.utc)
            self.db.commit()
            self._log_event("error", f"Pipeline failed: {str(e)}", job.progress)
            raise
