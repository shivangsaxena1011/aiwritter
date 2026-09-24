import os
import re
import logging
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
import docx
from docx import Document

from backend.app.services.document.artifact_integrity import (
    CountManifest,
    ArtifactIntegrityManifest,
    IntegrityAuditResult
)
from backend.app.agents.repetition_detector_2 import RepetitionDetector2
from backend.app.agents.adversarial_reviewer_agent import AdversarialReviewerAgent, AdversarialReviewResult
from backend.app.services.document.book_assembly_model import BookAssemblyModel

logger = logging.getLogger(__name__)


@dataclass
class HeadingItem:
    text: str
    level: int
    paragraph_index: int
    normalized_text: str


@dataclass
class ParagraphItem:
    index: int
    text: str
    style_name: str
    word_count: int
    is_heading: bool
    is_bullet: bool
    is_equation: bool
    location: str


class FinalDocxAuditor:
    """Authoritative Auditor for the Rendered Word Document (.docx).
    
    Principles:
    1. INTERNAL METRICS != FINAL TRUTH. Only the reopened DOCX is canonical.
    2. Zero consecutive duplicate headings allowed.
    3. Zero generic fallback headings or fake boilerplate sections allowed.
    4. Exact duplicate rate must be bounded and < 2%.
    5. Count reconciliation: planned == assembled == rendered.
    6. Adversarial reviewer must pass on the actual extracted DOCX text.
    """

    GENERIC_HEADING_PATTERNS = [
        re.compile(r"^section\s+\d+$", re.IGNORECASE),
        re.compile(r"^subtopic\s+\d+$", re.IGNORECASE),
        re.compile(r"^untitled\s+section$", re.IGNORECASE),
        re.compile(r"^placeholder.*$", re.IGNORECASE),
        re.compile(r"^topic\s+\d+$", re.IGNORECASE)
    ]

    def __init__(self, subject: str = "Engineering Physics"):
        self.subject = subject
        self.adversarial_reviewer = AdversarialReviewerAgent()

    @staticmethod
    def _normalize(text: str) -> str:
        t = re.sub(r"[^\w\s]", "", text.lower())
        return " ".join(t.split())

    def audit(
        self,
        docx_path: str,
        planned_manifest: Optional[CountManifest] = None,
        assembly_model: Optional[BookAssemblyModel] = None
    ) -> Dict[str, Any]:
        """Performs comprehensive physical and semantic audit of the generated DOCX."""
        if not os.path.exists(docx_path):
            return {
                "publication_ready": False,
                "error": f"DOCX file does not exist at {docx_path}",
                "blocking_reasons": [f"Missing file: {docx_path}"]
            }

        doc = Document(docx_path)

        # 1. Inventory Headings & Paragraphs
        headings: List[HeadingItem] = []
        paragraphs: List[ParagraphItem] = []
        total_equations = 0
        total_figures = 0
        total_words = 0

        current_chapter = "Front Matter"
        current_topic = ""
        current_subtopic = ""

        # Track structural counts
        chapter_headings: List[str] = []
        topic_headings: List[str] = []
        subtopic_headings: List[str] = []

        # Ignore non-chapter H1s like Preface, Table of Contents, Appendix
        FRONT_BACK_H1 = {"preface", "table of contents", "appendix academic quality verification scorecard", "references"}

        for p_idx, p in enumerate(doc.paragraphs):
            p_xml = p._p.xml
            text = p.text.strip()
            style_name = p.style.name if p.style else ""
            words = len(text.split())
            total_words += words

            # Check equation
            has_eq = ("<m:oMath" in p_xml or "Cambria Math" in p_xml or "<m:f>" in p_xml)
            if has_eq:
                total_equations += 1

            # Check figure / image
            has_drawing = ("<a:blip" in p_xml or "<w:drawing" in p_xml)
            if has_drawing:
                total_figures += 1

            is_heading = style_name.startswith("Heading")
            is_bullet = style_name.startswith("List")

            # Extract heading levels
            if is_heading:
                lvl = 1
                try:
                    lvl = int(style_name.replace("Heading", "").strip())
                except ValueError:
                    pass

                norm = self._normalize(text)
                headings.append(HeadingItem(
                    text=text,
                    level=lvl,
                    paragraph_index=p_idx,
                    normalized_text=norm
                ))

                if lvl == 1:
                    current_chapter = text
                    if norm not in FRONT_BACK_H1 and "appendix" not in norm:
                        chapter_headings.append(text)
                elif lvl == 2:
                    current_topic = text
                    if norm not in ("chapter overview objectives", "chapter overview and objectives", "academic bibliography"):
                        topic_headings.append(text)
                elif lvl == 3:
                    current_subtopic = text
                    if norm != "references":
                        subtopic_headings.append(text)

            location = f"{current_chapter} > {current_topic} > {current_subtopic}".strip(" >")
            paragraphs.append(ParagraphItem(
                index=p_idx,
                text=text,
                style_name=style_name,
                word_count=words,
                is_heading=is_heading,
                is_bullet=is_bullet,
                is_equation=has_eq,
                location=location
            ))

        # 2. Check for Duplicate and Generic Headings
        consecutive_duplicate_headings = []
        generic_headings = []
        duplicate_topic_headings = []
        seen_topics = set()

        for idx, h in enumerate(headings):
            # Consecutive duplicate check
            if idx > 0:
                prev_h = headings[idx - 1]
                if h.normalized_text and h.normalized_text == prev_h.normalized_text:
                    consecutive_duplicate_headings.append({
                        "heading_1": prev_h.text,
                        "heading_2": h.text,
                        "level": h.level,
                        "paragraph_indices": [prev_h.paragraph_index, h.paragraph_index]
                    })

            # Generic fallback heading check
            for pat in self.GENERIC_HEADING_PATTERNS:
                if pat.match(h.text.strip()):
                    generic_headings.append({
                        "heading": h.text,
                        "level": h.level,
                        "paragraph_index": h.paragraph_index
                    })
                    break

            # Duplicate topics check (H2)
            if h.level == 2 and h.normalized_text and h.normalized_text != "chapter overview  objectives":
                if h.normalized_text in seen_topics:
                    duplicate_topic_headings.append(h.text)
                seen_topics.add(h.normalized_text)

        # 3. Total Tables
        raw_tables_count = len(doc.tables)
        # Content tables (exclude the scorecard appendix table if present)
        content_tables_count = max(0, raw_tables_count - 1) if raw_tables_count > 0 else 0

        # Rendered Count Manifest
        rendered_manifest = CountManifest(
            chapters=len(chapter_headings),
            topics=len(topic_headings),
            sections=len(subtopic_headings),
            paragraphs=len(paragraphs),
            equations=total_equations,
            tables=content_tables_count,
            figures=total_figures,
            words=total_words
        )

        # 4. Count Reconciliation via ArtifactIntegrityManifest
        assembled_manifest = (
            CountManifest(**assembly_model.get_counts())
            if assembly_model
            else rendered_manifest
        )
        if not planned_manifest:
            planned_manifest = assembled_manifest

        integrity_manifest = ArtifactIntegrityManifest(
            planned=planned_manifest,
            assembled=assembled_manifest,
            rendered_docx=rendered_manifest
        )
        integrity_result: IntegrityAuditResult = integrity_manifest.reconcile()

        # 5. Extract Extracted Sections for Adversarial Review & Repetition Check
        sections_dict_list: List[Dict[str, Any]] = []
        curr_sec_title = ""
        curr_sec_paras: List[str] = []
        curr_unit = chapter_headings[0] if chapter_headings else "Chapter 1"
        curr_top = topic_headings[0] if topic_headings else "Topic 1"

        prose_paragraphs_for_rep: List[Dict[str, Any]] = []

        for p_item in paragraphs:
            if p_item.is_heading:
                if p_item.style_name.startswith("Heading 3"):
                    if curr_sec_title and curr_sec_paras:
                        sections_dict_list.append({
                            "unit": curr_unit,
                            "topic": curr_top,
                            "subtopic": curr_sec_title,
                            "content": "\n\n".join(curr_sec_paras),
                            "word_count": sum(len(p.split()) for p in curr_sec_paras)
                        })
                    curr_sec_title = p_item.text
                    curr_sec_paras = []
                elif p_item.style_name.startswith("Heading 2"):
                    curr_top = p_item.text
                elif p_item.style_name.startswith("Heading 1"):
                    curr_unit = p_item.text
            else:
                if p_item.text.strip():
                    curr_sec_paras.append(p_item.text)
                    if not p_item.is_bullet and not p_item.is_equation:
                        p_text_strip = p_item.text.strip()
                        if not p_text_strip.startswith("Figure ") and not p_text_strip.startswith("Table ") and not p_text_strip.startswith("|"):
                            prose_paragraphs_for_rep.append({
                                "text": p_item.text,
                                "location": p_item.location,
                                "is_heading": False
                            })

        if curr_sec_title and curr_sec_paras:
            sections_dict_list.append({
                "unit": curr_unit,
                "topic": curr_top,
                "subtopic": curr_sec_title,
                "content": "\n\n".join(curr_sec_paras),
                "word_count": sum(len(p.split()) for p in curr_sec_paras)
            })

        # 6. Repetition Audit on Actual DOCX Paragraphs
        rep_detector = RepetitionDetector2()
        repetition_audit = rep_detector.audit_docx_paragraphs(prose_paragraphs_for_rep)

        # 7. Adversarial Review on Actual DOCX Extracted Sections
        adversarial_result: AdversarialReviewResult = self.adversarial_reviewer.review_chapter(
            sections=sections_dict_list,
            chapter_title=chapter_headings[0] if chapter_headings else "Chapter 1",
            subject=self.subject,
            allow_warnings=False
        )

        # 8. Determine Publication Readiness
        blocking_reasons: List[str] = []

        if len(consecutive_duplicate_headings) > 0:
            blocking_reasons.append(
                f"Found {len(consecutive_duplicate_headings)} consecutive duplicate heading(s) in final DOCX."
            )
        if len(generic_headings) > 0:
            blocking_reasons.append(
                f"Found {len(generic_headings)} generic fallback heading(s) in final DOCX."
            )
        if len(duplicate_topic_headings) > 0:
            blocking_reasons.append(
                f"Found {len(duplicate_topic_headings)} duplicate topic heading(s): {duplicate_topic_headings}"
            )
        if not integrity_result.is_valid:
            blocking_reasons.extend(integrity_result.discrepancies)
        if not repetition_audit.get("passed", False):
            blocking_reasons.append(
                f"DOCX repetition audit failed: exact_duplicate_rate={repetition_audit.get('exact_duplicate_rate'):.2%}, "
                f"near_duplicate_rate={repetition_audit.get('near_duplicate_rate'):.2%}"
            )
        if not adversarial_result.publication_ready:
            blocking_reasons.extend([f"Adversarial review {i.severity} [{i.category}]: {i.description}" for i in adversarial_result.issues if i.severity in ("CRITICAL", "ERROR")])

        publication_ready = (len(blocking_reasons) == 0)

        logger.info(
            f"Final DOCX Audit complete for '{docx_path}': "
            f"publication_ready={publication_ready} (blocking_issues={len(blocking_reasons)})"
        )

        return {
            "docx_path": docx_path,
            "publication_ready": publication_ready,
            "blocking_reasons": blocking_reasons,
            "summary_counts": rendered_manifest.to_dict(),
            "reconciliation": integrity_result.to_dict(),
            "heading_audit": {
                "total_headings": len(headings),
                "consecutive_duplicates": consecutive_duplicate_headings,
                "generic_headings": generic_headings,
                "duplicate_topics": duplicate_topic_headings,
                "chapter_headings": chapter_headings,
                "topic_headings": topic_headings,
                "subtopic_headings": subtopic_headings
            },
            "repetition_audit": repetition_audit,
            "adversarial_review": adversarial_result.to_dict()
        }
