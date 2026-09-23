"""
BookGenerationOrchestrator — Complete 14-Stage Multi-Agent Publishing Pipeline.
Coordinates syllabus analysis, decomposition, web research, content drafting,
derivations, diagrams, peer review, consistency auditing, fact-checking,
DOCX export with Times New Roman 12pt / 1.5 spacing / OMML math, and programmatic validation.
"""

import os
import uuid
import logging
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session

from backend.app.core.config import settings
from backend.app.models import (
    Book, BookUnit, BookTopic, BookSubtopic,
    GenerationJob, GenerationEvent, GeneratedAsset, GeneratedSection,
    ResearchSource, ReviewResult, DocumentExport
)
from backend.app.services.ai.base import AIProvider
from backend.app.agents.base import AgentContext
from backend.app.agents.syllabus_analysis_agent import SyllabusAnalysisAgent
from backend.app.agents.topic_decomposition_agent import TopicDecompositionAgent
from backend.app.agents.research_agent import ResearchAgent
from backend.app.agents.content_planning_agent import ContentPlanningAgent
from backend.app.agents.content_writer_agent import ContentWriterAgent
from backend.app.agents.derivation_agent import DerivationAgent
from backend.app.agents.diagram_system import DiagramPlannerAgent, DiagramGeneratorAgent
from backend.app.agents.review_agent import ContentReviewAgent
from backend.app.agents.fact_check_agent import FactCheckAgent
from backend.app.agents.consistency_auditor import BookConsistencyAgent
from backend.app.agents.book_context_manager import BookContextManager
from backend.app.agents.chapter_depth_controller import ChapterDepthController
from backend.app.agents.document_structure_agent import DocumentStructureAgent
from backend.app.agents.document_validation_agent import DocumentValidationAgent
from backend.app.services.document.docx_engine import DOCXExporter
from backend.app.storage import get_storage_provider

logger = logging.getLogger(__name__)

class BookGenerationOrchestrator:
    """
    Executes the multi-agent academic textbook publishing workflow with full database durability,
    fault-tolerant retries, and comprehensive publication validation.
    """

    def __init__(self, job_id: str, db: Session, ai_provider: AIProvider):
        self.job_id = job_id
        self.db = db
        self.ai = ai_provider
        self.storage = get_storage_provider()

        # Instantiate specialized agents
        self.syllabus_agent = SyllabusAnalysisAgent(self.ai)
        self.decomposition_agent = TopicDecompositionAgent(self.ai)
        self.research_agent = ResearchAgent(self.ai)
        self.planning_agent = ContentPlanningAgent(self.ai)
        self.writer_agent = ContentWriterAgent(self.ai)
        self.derivation_agent = DerivationAgent(self.ai)
        self.diagram_planner = DiagramPlannerAgent(self.ai)
        self.diagram_generator = DiagramGeneratorAgent(self.ai)
        self.review_agent = ContentReviewAgent(self.ai)
        self.fact_check_agent = FactCheckAgent(self.ai)
        self.consistency_agent = BookConsistencyAgent(self.ai)
        self.docx_exporter = DOCXExporter()

    def _log_event(
        self,
        event_type: str,
        message: str,
        progress: Optional[float] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
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
            # Stage 1: Initialization and Context Setup
            job.status = "PLANNING"
            job.current_stage = "Stage 1: Syllabus Analysis & Architecture"
            job.started_at = datetime.now(timezone.utc)
            self.db.commit()
            self._log_event("stage", "Initializing publication publishing pipeline...", 5.0)

            # Metadata extraction
            meta = book.book_metadata or {}
            subject = meta.get("subject") or book.title
            writing_depth = meta.get("writing_depth", "Detailed")
            research_depth = meta.get("research_depth", "Standard")
            include_images = meta.get("generate_images", False)
            include_diagrams = meta.get("include_diagrams", True)
            include_numericals = meta.get("include_numericals", False)
            include_questions = meta.get("include_questions", False)
            include_examples = meta.get("include_examples", True)
            include_references = meta.get("include_references", True)

            agent_context = AgentContext(
                book_id=book.id,
                job_id=job.id,
                book_title=book.title,
                subject=subject,
                academic_level=book.academic_level,
                target_audience=book.target_audience,
                writing_depth=writing_depth,
                research_depth=research_depth,
                include_numericals=include_numericals,
                include_questions=include_questions,
                include_examples=include_examples,
                include_references=include_references,
                include_diagrams=include_diagrams,
                language=book.language
            )

            # Stage 2: Initialize Book Context Manager
            context_mgr = BookContextManager(
                book_title=book.title,
                academic_level=book.academic_level,
                target_audience=book.target_audience,
                writing_depth=writing_depth,
                citation_style=meta.get("citation_style", "IEEE")
            )

            # Stage 1: Load or Analyze Units & Topics
            units = self.db.query(BookUnit).filter(BookUnit.book_id == book.id).order_by(BookUnit.position).all()
            if not units and meta.get("raw_syllabus"):
                self._log_event("stage", "🔍 SyllabusAnalysisAgent: Parsing and decomposing syllabus hierarchy...", 6.0)
                try:
                    analysis = await self.syllabus_agent.analyze_syllabus(
                        syllabus_text=meta["raw_syllabus"],
                        subject=subject,
                        academic_level=book.academic_level,
                        include_numericals=include_numericals,
                        include_diagrams=include_diagrams
                    )
                    for ch_data in analysis.get("chapters", []):
                        ch_unit = BookUnit(book_id=book.id, position=ch_data.get("number", 1), title=ch_data.get("title", "Chapter"))
                        self.db.add(ch_unit)
                        self.db.flush()
                        for top_idx, top_data in enumerate(ch_data.get("topics", []), start=1):
                            b_top = BookTopic(unit_id=ch_unit.id, position=top_idx, title=top_data.get("title", "Topic"))
                            self.db.add(b_top)
                            self.db.flush()
                            for sub_idx, sub_name in enumerate(top_data.get("subtopics", []), start=1):
                                b_sub = BookSubtopic(topic_id=b_top.id, position=sub_idx, title=sub_name)
                                self.db.add(b_sub)
                    self.db.commit()
                    units = self.db.query(BookUnit).filter(BookUnit.book_id == book.id).order_by(BookUnit.position).all()
                except Exception as s_err:
                    logger.warning(f"Syllabus analysis fallback: {s_err}")

            # Count total units and subtopics
            total_subtopics = 0
            for u in units:
                topics = self.db.query(BookTopic).filter(BookTopic.unit_id == u.id).all()
                for t in topics:
                    total_subtopics += self.db.query(BookSubtopic).filter(BookSubtopic.topic_id == t.id).count()

            total_subtopics = max(1, total_subtopics)
            completed_subtopics = 0
            failed_subtopics = 0

            compiled_sections: List[Dict[str, Any]] = []
            compiled_assets: List[Dict[str, Any]] = []
            audits_summary: List[Dict[str, Any]] = []
            all_sources: List[Any] = []

            job.status = "GENERATING"
            self.db.commit()

            # Iterate through Chapters -> Topics -> Subtopics
            for u_idx, unit in enumerate(units, start=1):
                if self._check_cancellation():
                    self._log_event("warning", "Generation job cancelled by user.")
                    return

                topics = self.db.query(BookTopic).filter(BookTopic.unit_id == unit.id).order_by(BookTopic.position).all()
                topic_names = [t.title for t in topics]

                # Chapter Planning
                self._log_event("stage", f"📖 Planning Chapter {u_idx}: {unit.title} roadmap...", (completed_subtopics / total_subtopics) * 75.0 + 8.0)
                unit_plan = await self.planning_agent.plan_chapter(
                    book_title=book.title,
                    subject=subject,
                    unit_title=unit.title,
                    topics=topic_names,
                    academic_level=book.academic_level,
                    writing_depth=writing_depth,
                    include_numericals=include_numericals,
                    include_questions=include_questions,
                    include_examples=include_examples
                )

                compiled_sections.append({
                    "unit": unit.title,
                    "is_unit_overview": True,
                    "content": unit_plan.get("unit_introduction", f"# {unit.title}\n\nChapter overview and foundations.")
                })

                figure_counter = 1

                for t_idx, topic in enumerate(topics, start=1):
                    # Check topic derivation & numerical flags
                    requires_derivation = any(w in topic.title.lower() for w in ["schrodinger", "wave", "equation", "derivation", "formula", "hamiltonian", "box", "well", "maxwell", "operator", "quantum"])
                    requires_numericals = include_numericals and any(w in topic.title.lower() for w in ["problem", "calculation", "energy", "wavelength", "probability", "numerical", "box", "well"])

                    subtopics = self.db.query(BookSubtopic).filter(BookSubtopic.topic_id == topic.id).order_by(BookSubtopic.position).all()
                    if not subtopics:
                        self._log_event("log", f"🧩 TopicDecompositionAgent: Blueprinting sections for {topic.title}...")
                        try:
                            decomp = await self.decomposition_agent.decompose_topic(
                                topic_title=topic.title,
                                subject=subject,
                                academic_level=book.academic_level,
                                requires_derivation=requires_derivation,
                                requires_numericals=requires_numericals
                            )
                            for s_pos, s_item in enumerate(decomp.get("sections", []), start=1):
                                s_title = s_item.get("title", f"Section {s_pos}") if isinstance(s_item, dict) else str(s_item)
                                st_row = BookSubtopic(topic_id=topic.id, position=s_pos, title=s_title)
                                self.db.add(st_row)
                            self.db.commit()
                            subtopics = self.db.query(BookSubtopic).filter(BookSubtopic.topic_id == topic.id).order_by(BookSubtopic.position).all()
                        except Exception as dec_err:
                            logger.warning(f"Topic decomposition fallback: {dec_err}")

                    is_first_in_topic = True

                    # Stage 3: Educational Web Research per Topic
                    self._log_event("log", f"🔬 Grounding research for: {topic.title}...")
                    research_res = await self.research_agent.research_topic(
                        topic=topic.title,
                        subject=subject,
                        depth=research_depth
                    )
                    all_sources.extend(research_res.sources)

                    # Persist research sources in database
                    for s_data in research_res.sources:
                        rs_row = ResearchSource(
                            book_id=book.id,
                            topic_id=topic.id,
                            title=s_data.title,
                            url=s_data.url,
                            author=s_data.author,
                            publisher=s_data.publisher,
                            publication_date=s_data.publication_date,
                            accessed_date=s_data.accessed_date,
                            source_type=s_data.source_type,
                            key_points=s_data.key_points,
                            relevance=s_data.relevance
                        )
                        self.db.add(rs_row)
                    self.db.commit()

                    for s_idx, subtopic in enumerate(subtopics, start=1):
                        if self._check_cancellation():
                            self._log_event("warning", "Generation job cancelled by user.")
                            return

                        job.current_stage = f"Drafting: Chapter {u_idx} > {topic.title}"
                        job.current_item = subtopic.title
                        self.db.commit()

                        # Check for existing section checkpoint (partial recovery)
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
                            self._log_event("log", f"✍️ Writing Treatise {u_idx}.{t_idx}.{s_idx}: {subtopic.title}...")

                            # Stage 6: Paragraph-First Content Writing with failure recovery (retry -> partial -> continue)
                            write_retries = 2
                            content = None
                            topic_is_partial = False
                            for attempt in range(write_retries):
                                try:
                                    content = await self.writer_agent.write_section(
                                        book_title=book.title,
                                        subject=subject,
                                        unit_title=unit.title,
                                        topic_title=topic.title,
                                        subtopic_title=subtopic.title,
                                        context_manager=context_mgr,
                                        writing_depth=writing_depth,
                                        research_notes=research_res.research_notes,
                                        requires_derivation=requires_derivation,
                                        include_numericals=requires_numericals,
                                        include_questions=include_questions,
                                        include_examples=include_examples
                                    )
                                    if content and len(content.split()) >= 150:
                                        break
                                except Exception as write_err:
                                    logger.warning(f"Drafting attempt {attempt+1} failed for {subtopic.title}: {write_err}")
                                    if attempt == write_retries - 1:
                                        failed_subtopics += 1
                                        topic_is_partial = True
                                        self._log_event("warning", f"⚠️ Section {subtopic.title} marked partial after retry.")
                                        content = self.writer_agent._generate_deterministic_content(
                                            book.title, subject, unit.title, topic.title, subtopic.title,
                                            requires_derivation, requires_numericals, include_questions
                                        )

                            # Stage 7: Derivation Engine Integration
                            if requires_derivation and any(kw in subtopic.title.lower() for kw in ["equation", "derivation", "proof", "formulation", "model", "box", "well", "wave", "hypothesis", "relativity"]):
                                try:
                                    self._log_event("log", f"📐 DerivationAgent: Formulating analytical proof for {subtopic.title}...")
                                    deriv_res = await self.derivation_agent.generate_derivation(
                                        topic=topic.title,
                                        equation_name=subtopic.title,
                                        subject=subject,
                                        academic_level=book.academic_level
                                    )
                                    deriv_md = deriv_res.get("markdown_content")
                                    if deriv_md and deriv_md not in content:
                                        content += f"\n\n#### Formal Analytical Derivation of {subtopic.title}\n\n{deriv_md}"
                                except Exception as d_err:
                                    logger.warning(f"Derivation generation fallback: {d_err}")

                            profile = ChapterDepthController.get_profile(writing_depth)
                            word_count = len(content.split())

                            # Stage 11: Content Review & Quality Audit
                            review_res = await self.review_agent.review_section(
                                book_title=book.title,
                                subtopic_title=subtopic.title,
                                content=content,
                                target_word_count=profile["target_words"]
                            )
                            audits_summary.append(review_res)

                            # Auto-rewrite loop if quality is below threshold up to max retries
                            retries_left = settings.MAX_CONTENT_REVIEW_RETRIES
                            while review_res.get("rewrite_required") and retries_left > 0:
                                self._log_event("warning", f"⚠️ Refactoring section for academic rigor (attempt {settings.MAX_CONTENT_REVIEW_RETRIES - retries_left + 1}): {subtopic.title}")
                                content = await self.writer_agent.write_section(
                                    book_title=book.title,
                                    subject=subject,
                                    unit_title=unit.title,
                                    topic_title=topic.title,
                                    subtopic_title=subtopic.title,
                                    context_manager=context_mgr,
                                    writing_depth=writing_depth,
                                    research_notes=research_res.research_notes,
                                    requires_derivation=requires_derivation,
                                    include_numericals=requires_numericals,
                                    include_questions=include_questions,
                                    include_examples=include_examples
                                )
                                word_count = len(content.split())
                                review_res = await self.review_agent.review_section(
                                    book_title=book.title,
                                    subtopic_title=subtopic.title,
                                    content=content,
                                    target_word_count=profile["target_words"]
                                )
                                retries_left -= 1

                            # Stage 12: Fact Check & Consistency Audit
                            fact_check = await self.fact_check_agent.verify_section(
                                content=content,
                                topic=subtopic.title,
                                sources=research_res.sources
                            )

                            await self.consistency_agent.audit_and_update(content, context_mgr)

                            # Originality Audit
                            orig_report = self.research_agent.assess_originality(content, research_res.sources)

                            # Persist Section in DB
                            gen_sec = GeneratedSection(
                                book_id=book.id,
                                unit_id=unit.id,
                                topic_id=topic.id,
                                subtopic_id=subtopic.id,
                                content=content,
                                status="partial" if topic_is_partial else "reviewed",
                                word_count=word_count,
                                review_status="needs_review" if topic_is_partial else "approved",
                                quality_score=review_res.get("overall_score", 88.0)
                            )
                            self.db.add(gen_sec)
                            self.db.flush()

                            # Persist Review Result in DB
                            rev_row = ReviewResult(
                                book_id=book.id,
                                section_id=gen_sec.id,
                                agent="ContentReviewAgent",
                                status="partial" if topic_is_partial else "approved",
                                quality_score=review_res.get("overall_score", 88.0),
                                fact_check_status=fact_check.get("verdict", "verified"),
                                originality_score=orig_report.get("originality_score", 98.0),
                                issues=review_res.get("issues", []),
                                recommendations=review_res.get("corrections", [])
                            )
                            self.db.add(rev_row)

                            subtopic.status = "partial" if topic_is_partial else "completed"
                            self.db.commit()

                        # Update context memory
                        context_mgr.record_section_summary(
                            unit.title, topic.title, subtopic.title,
                            summary=f"{subtopic.title}: established with {word_count} words."
                        )

                        # Stage 9 & 10: Diagram Planning & Generation
                        img_path = None
                        img_caption = None
                        placeholder_box = None

                        if include_images or include_diagrams:
                            diag_plan = await self.diagram_planner.plan_diagram(
                                book_title=book.title,
                                subtopic_title=subtopic.title,
                                section_content=content,
                                chapter_idx=u_idx,
                                figure_idx=figure_counter
                            )

                            if diag_plan.get("needs_diagram"):
                                output_dir = os.path.join(settings.STORAGE_LOCAL_DIR, "assets", book.id)
                                asset_res = await self.diagram_generator.generate_asset(
                                    diag_plan, output_dir=output_dir, topic_title=subtopic.title
                                )
                                img_path = asset_res.get("path")
                                img_caption = asset_res.get("caption") or f"Figure {u_idx}.{figure_counter} — Technical Diagram of {subtopic.title}"
                                placeholder_box = asset_res.get("placeholder")
                                compiled_assets.append(asset_res)
                                figure_counter += 1

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
                        progress_pct = (completed_subtopics / total_subtopics) * 70.0 + 15.0
                        self._log_event("progress", f"Completed {subtopic.title} ({completed_subtopics}/{total_subtopics})", progress_pct)

            # Stage 13: Formatting & DOCX Export
            job.status = "EXPORTING"
            job.current_stage = "Stage 13: Master DOCX Compilation & Formatting"
            self._log_event("stage", "📚 Compiling master academic DOCX...", 88.0)

            # Structure document layout via DocumentStructureAgent
            doc_structure = DocumentStructureAgent.plan_document_structure(
                book_title=book.title,
                subject=subject,
                academic_level=book.academic_level,
                chapters=[{"number": u.position, "title": u.title, "topics": [t.title for t in u.topics]} for u in units],
                include_references=include_references
            )

            # Bibliography generation if references enabled
            if include_references and all_sources:
                bib_md = self.research_agent.generate_bibliography_markdown(citation_style=meta.get("citation_style", "IEEE"))
                if bib_md:
                    compiled_sections.append({
                        "unit": "References",
                        "topic": "Academic Bibliography",
                        "subtopic": "References",
                        "is_first_in_topic": True,
                        "content": bib_md,
                        "word_count": len(bib_md.split())
                    })

            # Prepare TOC dict
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

            # Export DOCX
            safe_title = "".join(c for c in book.title if c.isalnum() or c in (" ", "_", "-")).replace(" ", "_")
            out_filename = f"{safe_title}_{uuid.uuid4().hex[:6]}.docx"
            out_filepath = os.path.join(settings.STORAGE_LOCAL_DIR, out_filename)

            self.docx_exporter.export(
                book_title=book.title,
                subtitle=book.subtitle,
                author=book.author,
                academic_level=book.academic_level,
                toc_data=toc_dict,
                sections=compiled_sections,
                assets=compiled_assets,
                output_path=out_filepath,
                quality_report=None
            )

            # Stage 14: Document Validation & Quality Reports
            job.status = "REVIEWING"
            job.current_stage = "Stage 14: Document Validation & Quality Scoring"
            self._log_event("stage", "🔍 Programmatically verifying document quality...", 95.0)

            doc_quality = DocumentValidationAgent.validate_docx(
                docx_path=out_filepath,
                expected_chapters=len(units),
                expected_topics=total_subtopics,
                include_diagrams=include_diagrams
            )

            coverage_report_path = out_filepath.replace(".docx", "_syllabus_coverage.json")
            coverage_report = DocumentValidationAgent.generate_syllabus_coverage_report(
                syllabus_chapters=[{"number": u.position, "title": u.title, "topics": [t.title for t in u.topics]} for u in units],
                generated_sections=compiled_sections,
                output_path=coverage_report_path
            )

            # Persist DocumentExport
            doc_export = DocumentExport(
                book_id=book.id,
                job_id=job.id,
                format="docx",
                file_path=out_filepath,
                file_size=os.path.getsize(out_filepath) if os.path.exists(out_filepath) else 0,
                validation_report=doc_quality,
                syllabus_coverage=coverage_report
            )
            self.db.add(doc_export)

            # Register Final Asset
            docx_asset = GeneratedAsset(
                book_id=book.id,
                job_id=job.id,
                type="docx",
                storage_key=out_filename,
                url=f"/api/v1/files/{out_filename}",
                asset_metadata={
                    "quality_report": doc_quality,
                    "syllabus_coverage": coverage_report
                }
            )
            self.db.add(docx_asset)

            # Finalize Job
            final_status = "PARTIAL" if failed_subtopics > 0 else "COMPLETED"
            job.status = final_status
            job.current_stage = "Completed"
            job.progress = 100.0
            job.completed_at = datetime.now(timezone.utc)
            book.status = "completed"
            self.db.commit()

            self._log_event("complete", f"Academic book publishing pipeline finished ({final_status})!", 100.0, {
                "download_url": f"/api/v1/files/{out_filename}",
                "filename": out_filename,
                "quality_report": doc_quality,
                "syllabus_coverage": coverage_report
            })

        except Exception as e:
            logger.exception(f"Pipeline execution error: {e}")
            job.status = "FAILED"
            job.error = str(e)
            job.updated_at = datetime.now(timezone.utc)
            self.db.commit()
            self._log_event("error", f"Pipeline failed: {str(e)}", job.progress)
            raise

# Semantic Alias
BookGenerationPipeline = BookGenerationOrchestrator
