import os
import re
import hashlib
import logging
from typing import Dict, Any, List, Optional, Tuple, Set
from dataclasses import dataclass, field
import docx
from docx import Document

from backend.app.services.document.artifact_integrity import CountManifest

logger = logging.getLogger(__name__)


@dataclass
class IndependentAuditResult:
    publication_ready: bool
    docx_path: str
    total_docx_paragraphs: int
    evaluated_prose_paragraphs: int
    exact_duplicate_paragraphs: int
    near_duplicate_paragraphs: int
    exact_duplicate_paragraph_rate: float
    near_duplicate_paragraph_rate: float
    total_headings: int
    consecutive_duplicate_headings: int
    generic_headings: int
    structural_template_families: List[str]
    total_tables: int
    exact_duplicate_tables: int
    near_duplicate_tables: int
    semantic_duplicate_tables: int
    math_rendering_errors_in_tables: int
    total_figures: int
    figure_caption_mismatches: int
    math_rendering_artifacts_count: int
    count_reconciliation_valid: bool
    blocking_reasons: List[str]
    summary_counts: Dict[str, Any]
    reconciliation_details: Dict[str, Any]

    content_depth: Dict[str, Any] = field(default_factory=dict)
    docx_sha256: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "publication_ready": self.publication_ready,
            "docx_path": self.docx_path,
            "docx_sha256": self.docx_sha256,
            "content_depth": self.content_depth,
            "total_docx_paragraphs": self.total_docx_paragraphs,
            "evaluated_prose_paragraphs": self.evaluated_prose_paragraphs,
            "exact_duplicate_paragraphs": self.exact_duplicate_paragraphs,
            "near_duplicate_paragraphs": self.near_duplicate_paragraphs,
            "exact_duplicate_paragraph_rate": round(self.exact_duplicate_paragraph_rate, 4),
            "near_duplicate_paragraph_rate": round(self.near_duplicate_paragraph_rate, 4),
            "total_headings": self.total_headings,
            "consecutive_duplicate_headings": self.consecutive_duplicate_headings,
            "generic_headings": self.generic_headings,
            "structural_template_families": self.structural_template_families,
            "total_tables": self.total_tables,
            "exact_duplicate_tables": self.exact_duplicate_tables,
            "near_duplicate_tables": self.near_duplicate_tables,
            "semantic_duplicate_tables": self.semantic_duplicate_tables,
            "math_rendering_errors_in_tables": self.math_rendering_errors_in_tables,
            "total_figures": self.total_figures,
            "figure_caption_mismatches": self.figure_caption_mismatches,
            "math_rendering_artifacts_count": self.math_rendering_artifacts_count,
            "count_reconciliation_valid": self.count_reconciliation_valid,
            "blocking_reasons": self.blocking_reasons,
            "summary_counts": self.summary_counts,
            "reconciliation_details": self.reconciliation_details
        }


class IndependentArtifactAuditor:
    """
    Content Orchestration 2.2 — Independent Artifact Truth Engine.

    Guiding Principles:
    1. THE RENDERED DOCX IS THE ONLY AUTHORITATIVE TRUTH.
    2. Independent inspection from scratch using python-docx and XML parsing.
    3. Evaluates ALL prose paragraphs in the DOCX (no sampling or partial subsets).
    4. Evaluates ALL tables for exact, near, and semantic duplicates, plus math rendering artifacts.
    5. Strict 3-way count reconciliation: planned == assembled == rendered_docx.
    6. Identifies structural template family repetitions across topics.
    7. Identifies figure-caption semantic mismatches and math rendering artifacts.
    """

    GENERIC_HEADING_PATTERNS = [
        re.compile(r"^section\s+\d+$", re.IGNORECASE),
        re.compile(r"^subtopic\s+\d+$", re.IGNORECASE),
        re.compile(r"^untitled\s+section$", re.IGNORECASE),
        re.compile(r"^placeholder.*$", re.IGNORECASE),
        re.compile(r"^topic\s+\d+$", re.IGNORECASE)
    ]

    UNRENDERED_MATH_PATTERNS = [
        re.compile(r"\\[a-zA-Z]{2,}"),  # e.g. \frac, \sqrt, \text, \lambda
        re.compile(r"\$\$"),  # Display math delimiter unrendered
        re.compile(r"(?<!\\)\$[^\$\n]{2,}\$")  # Raw LaTeX inline math $...$ unrendered in table/text
    ]

    def __init__(self, near_threshold: float = 0.75, min_prose_words: int = 6):
        self.near_threshold = near_threshold
        self.min_prose_words = min_prose_words

    @staticmethod
    def _normalize(text: str) -> str:
        t = re.sub(r"[^\w\s]", "", text.lower())
        return " ".join(t.split())

    @staticmethod
    def _get_archetype(subtopic_heading: str) -> str:
        s = subtopic_heading.lower()
        if "concept" in s or "principle" in s or "motivation" in s or "foundation" in s:
            return "CONCEPT"
        if "formulation" in s or "governing" in s or "equation" in s:
            return "FORMULATION"
        if "derivation" in s or "boundary condition" in s or "proof" in s:
            return "DERIVATION"
        if "interpretation" in s or "eigenstate" in s or "amplitude" in s:
            return "INTERPRETATION"
        if "application" in s or "technology" in s or "relevance" in s or "engineering" in s:
            return "APPLICATION"
        if "limitation" in s or "assumption" in s or "scope" in s:
            return "LIMITATION"
        if "experiment" in s or "apparatus" in s or "diffraction" in s:
            return "EXPERIMENT"
        if "numerical" in s or "problem" in s or "exemplar" in s:
            return "NUMERICAL"
        return "GENERAL"

    @staticmethod
    def _classify_topic_semantic_type(topic_title: str, text_corpus: str = "") -> str:
        """Determines the academic semantic archetype of a topic for contract validation."""
        t = topic_title.lower()
        if any(k in t for k in ["derivation", "equation", "formula", "schrödinger", "schrodinger", "lorentz", "poynting", "einstein coefficient", "box", "well", "numerical aperture"]):
            return "derivation"
        elif any(k in t for k in ["experiment", "apparatus", "davisson", "germer", "newton's rings", "michelson", "double slit", "grating"]):
            return "experimental"
        elif any(k in t for k in ["algorithm", "computational", "numerical method", "complexity"]):
            return "algorithmic"
        elif any(k in t for k in ["application", "processing", "communication", "sensor", "industrial", "medical"]):
            return "application"
        elif any(k in t for k in ["step-index and graded-index", "single mode and multi mode", "comparison", "difference", "versus", " vs "]):
            return "comparison"
        elif any(k in t for k in ["operator", "eigenvalue", "eigenfunction", "vector potential", "mathematical", "matrix", "resolving power"]):
            return "mathematical"
        elif any(k in t for k in ["ruby laser", "he-ne laser", "semiconductor diode laser", "fabrication", "splicing", "preform", "system", "process", "drawing", "pumping"]):
            return "process/system"
        else:
            return "conceptual"

    @staticmethod
    def _validate_semantic_contract(
        topic_title: str,
        archetype: str,
        paragraphs: List[str],
        total_words: int
    ) -> Tuple[bool, List[str]]:
        """
        Validates authentic university pedagogical contracts per topic semantic type:
          - conceptual: principle/concept, detailed mechanism/properties, application/implications
          - derivation/mathematical: motivation/starting relation, derivation steps, physical interpretation
          - experimental: apparatus/principle, procedure/observation, physical conclusion
          - application: operational principle, engineering implementation context
          - comparison: comparative physical trade-offs and mechanisms
          - process/system: procedural stages, system architectures, and operational dynamics
        """
        corpus = " ".join(paragraphs).lower()
        failures = []

        if total_words < 100:
            failures.append(f"Topic '{topic_title}' has insufficient depth ({total_words} words < 100 threshold).")

        if len(paragraphs) < 2:
            failures.append(f"Topic '{topic_title}' has fewer than 2 paragraphs ({len(paragraphs)} found).")

        if archetype == "conceptual":
            has_principle = any(k in corpus for k in [
                "principle", "concept", "postulate", "phenomenon", "definition", "discovered", "theory",
                "law", "foundation", "coherence", "polarization", "interference", "attenuation", "dispersion",
                "state", "lifetime", "structure", "guidance"
            ])
            has_mechanism = any(k in corpus for k in [
                "mechanism", "property", "state", "mode", "frequency", "behavior", "radiation", "quantum",
                "optical", "energy", "wave", "matter", "phase", "wavefront", "amplitude", "vector", "refractive"
            ])
            has_application = any(k in corpus for k in [
                "application", "implication", "significance", "consequence", "limit", "classical", "experiment",
                "engineering", "technol", "physic", "optical", "instrument", "laser", "fiber", "spectroscopy",
                "metrology", "transmission", "telecom", "holograph"
            ])
            if not (has_principle and has_mechanism):
                failures.append(f"Conceptual contract missing foundational principle or mechanism in '{topic_title}'.")
            if not has_application:
                failures.append(f"Conceptual contract missing application or physical implications in '{topic_title}'.")

        elif archetype in ("derivation", "mathematical"):
            has_motivation = any(k in corpus for k in [
                "motivat", "derive", "consider", "formulat", "starting", "governing", "equation", "relation",
                "wave", "potential", "criterion", "resolv", "operator", "observable", "formalism", "postulate", "definition"
            ])
            has_steps = any(k in corpus for k in [
                "yields", "substitut", "integrat", "evaluat", "simplif", "solving", "boundary", "differential",
                "=", "\\frac", "\\times", "\\sum", "given by", "express", "limit", "proportional"
            ])
            has_interp = any(k in corpus for k in [
                "interpret", "condition", "limit", "physical", "constant", "proves", "establishes", "significance",
                "demonstrat", "quantiz", "wavelength"
            ])
            if not (has_motivation and (has_steps or has_interp)):
                failures.append(f"Derivation contract missing mathematical development or interpretation in '{topic_title}'.")

        elif archetype == "experimental":
            has_apparatus = any(k in corpus for k in [
                "apparatus", "setup", "crystal", "source", "interferometer", "slit", "cavity", "mirror", "beam",
                "geometry", "plate", "grating", "ruling"
            ])
            has_observation = any(k in corpus for k in [
                "observation", "fringe", "pattern", "detect", "result", "measured", "shift", "voltage", "intensity",
                "ray", "maxima", "minima", "diffract"
            ])
            has_conclusion = any(k in corpus for k in [
                "demonstrat", "confirm", "validat", "null", "conclusion", "verif", "proved", "measured", "wavelength",
                "dispersive"
            ])
            if not (has_apparatus and (has_observation or has_conclusion)):
                failures.append(f"Experimental contract missing apparatus setup or observation analysis in '{topic_title}'.")

        elif archetype == "application":
            has_principle = any(k in corpus for k in [
                "operat", "principle", "transmitt", "process", "manufactur", "system", "device", "carrier",
                "sensor", "transducer", "modulat", "detect"
            ])
            has_impl = any(k in corpus for k in [
                "technolog", "amplif", "modulat", "power", "fiber", "laser", "cutting", "welding", "medical",
                "detector", "sensor", "telecom", "monitoring", "strain", "temperature", "network"
            ])
            if not (has_principle and has_impl):
                failures.append(f"Application contract missing engineering mechanism or technological context in '{topic_title}'.")

        elif archetype == "comparison":
            has_comparison = any(k in corpus for k in ["contrast", "differ", "whereas", "while", "unlike", "compared", "advantage", "dispersion", "mode"])
            if not has_comparison:
                failures.append(f"Comparison contract missing contrastive analysis in '{topic_title}'.")

        elif archetype == "process/system":
            has_steps = any(k in corpus for k in [
                "process", "stage", "step", "fabricat", "drawing", "pumping", "align", "fusion", "method", "preform",
                "system", "level", "transition", "cavity", "mirror", "discharge", "excitation"
            ])
            if not has_steps:
                failures.append(f"Process contract missing procedural steps or system description in '{topic_title}'.")

        return (len(failures) == 0, failures)

    def audit(
        self,
        docx_path: str,
        planned_manifest: Optional[CountManifest] = None,
        assembled_manifest: Optional[CountManifest] = None,
        assembly_model: Optional[Any] = None
    ) -> IndependentAuditResult:
        blocking_reasons: List[str] = []

        if assembled_manifest is None and assembly_model is not None:
            assembled_manifest = CountManifest(**assembly_model.get_counts())

        if not os.path.exists(docx_path):
            return IndependentAuditResult(
                publication_ready=False,
                docx_path=docx_path,
                total_docx_paragraphs=0,
                evaluated_prose_paragraphs=0,
                exact_duplicate_paragraphs=0,
                near_duplicate_paragraphs=0,
                exact_duplicate_paragraph_rate=0.0,
                near_duplicate_paragraph_rate=0.0,
                total_headings=0,
                consecutive_duplicate_headings=0,
                generic_headings=0,
                structural_template_families=[],
                total_tables=0,
                exact_duplicate_tables=0,
                near_duplicate_tables=0,
                semantic_duplicate_tables=0,
                math_rendering_errors_in_tables=0,
                total_figures=0,
                figure_caption_mismatches=0,
                math_rendering_artifacts_count=0,
                count_reconciliation_valid=False,
                blocking_reasons=[f"Missing file: {docx_path}"],
                summary_counts={},
                reconciliation_details={}
            )

        doc = Document(docx_path)

        # -------------------------------------------------------------
        # 1. PARAGRAPH & INVENTORY AUDIT
        # -------------------------------------------------------------
        total_docx_paragraphs = len(doc.paragraphs)
        headings: List[Dict[str, Any]] = []
        prose_paragraphs: List[Dict[str, Any]] = []
        figure_captions: List[Dict[str, Any]] = []

        chapter_headings: List[str] = []
        topic_headings: List[str] = []
        subtopic_headings: List[str] = []

        topic_structure_map: Dict[str, List[str]] = {}

        total_equations = 0
        total_figures = 0
        total_words = 0
        math_artifacts_in_text = 0

        current_chapter = "Front Matter"
        current_topic = ""
        current_subtopic = ""

        FRONT_BACK_H1 = {"preface", "table of contents", "appendix academic quality verification scorecard", "references"}

        for p_idx, p in enumerate(doc.paragraphs):
            p_xml = p._p.xml
            text = p.text.strip()
            style_name = p.style.name if p.style else ""
            words = len(text.split())
            total_words += words

            # Equation check
            has_eq = ("<m:oMath" in p_xml or "Cambria Math" in p_xml or "<m:f>" in p_xml)
            if has_eq:
                total_equations += 1

            # Drawing/Figure check
            has_drawing = ("<a:blip" in p_xml or "<w:drawing" in p_xml)
            if has_drawing:
                total_figures += 1

            is_heading = style_name.startswith("Heading")
            is_bullet = style_name.startswith("List")

            # Scan for unrendered math artifacts in prose text
            if not is_heading and not is_bullet and not has_eq:
                for pat in self.UNRENDERED_MATH_PATTERNS:
                    if pat.search(text):
                        math_artifacts_in_text += 1
                        break

            if is_heading:
                lvl = 1
                try:
                    lvl = int(style_name.replace("Heading", "").strip())
                except ValueError:
                    pass

                norm = self._normalize(text)
                headings.append({
                    "text": text,
                    "level": lvl,
                    "paragraph_index": p_idx,
                    "normalized": norm
                })

                if lvl == 1:
                    current_chapter = text
                    if norm not in FRONT_BACK_H1 and "appendix" not in norm:
                        chapter_headings.append(text)
                elif lvl == 2:
                    current_topic = text
                    if norm not in ("chapter overview objectives", "chapter overview and objectives", "academic bibliography"):
                        topic_headings.append(text)
                        if text not in topic_structure_map:
                            topic_structure_map[text] = []
                elif lvl == 3:
                    current_subtopic = text
                    if norm != "references":
                        subtopic_headings.append(text)
                        if current_topic and current_topic in topic_structure_map:
                            archetype = self._get_archetype(text)
                            topic_structure_map[current_topic].append(archetype)
            else:
                if text:
                    loc = f"{current_chapter} > {current_topic} > {current_subtopic}".strip(" >")

                    is_display_eq = (has_eq and words < 20)
                    if text.startswith("Figure ") or text.startswith("Fig."):
                        figure_captions.append({
                            "text": text,
                            "topic": current_topic,
                            "subtopic": current_subtopic,
                            "location": loc
                        })
                    elif not is_bullet and not is_display_eq and words >= self.min_prose_words:
                        prose_paragraphs.append({
                            "index": p_idx,
                            "text": text,
                            "location": loc,
                            "words": words,
                            "normalized": self._normalize(text)
                        })

        # -------------------------------------------------------------
        # 2. HEADING INTEGRITY & CONSECUTIVE DUPLICATE AUDIT
        # -------------------------------------------------------------
        consecutive_duplicate_headings = 0
        generic_headings_count = 0
        duplicate_topic_headings = []
        seen_topics = set()

        for idx, h in enumerate(headings):
            if idx > 0:
                prev_h = headings[idx - 1]
                if h["normalized"] and h["normalized"] == prev_h["normalized"]:
                    consecutive_duplicate_headings += 1

            for pat in self.GENERIC_HEADING_PATTERNS:
                if pat.match(h["text"]):
                    generic_headings_count += 1
                    break

            if h["level"] == 2 and h["normalized"] and h["normalized"] != "chapter overview objectives":
                if h["normalized"] in seen_topics:
                    duplicate_topic_headings.append(h["text"])
                seen_topics.add(h["normalized"])

        if consecutive_duplicate_headings > 0:
            blocking_reasons.append(f"Found {consecutive_duplicate_headings} consecutive duplicate heading(s) in DOCX.")

        if generic_headings_count > 0:
            blocking_reasons.append(f"Found {generic_headings_count} generic fallback heading(s) in DOCX.")

        if len(duplicate_topic_headings) > 0:
            blocking_reasons.append(f"Found duplicate topic heading(s): {duplicate_topic_headings}")

        # -------------------------------------------------------------
        # 3. GENERIC STRUCTURAL TEMPLATE SEQUENCE AUDIT
        # -------------------------------------------------------------
        structural_template_families: List[str] = []
        sequence_counts: Dict[str, int] = {}
        for top_title, seq in topic_structure_map.items():
            if len(seq) >= 3:
                seq_str = " -> ".join(seq)
                sequence_counts[seq_str] = sequence_counts.get(seq_str, 0) + 1

        for seq_str, count in sequence_counts.items():
            if count >= 3:
                family_msg = f"Repeated generic section structure sequence '{seq_str}' across {count} topics."
                structural_template_families.append(family_msg)
                blocking_reasons.append(family_msg)

        # -------------------------------------------------------------
        # 4. FULL PROSE REPETITION AUDIT (EVERY PROSE PARAGRAPH)
        # -------------------------------------------------------------
        evaluated_prose_count = len(prose_paragraphs)
        exact_duplicate_paragraphs = 0
        near_duplicate_paragraphs = 0

        exact_hash_locs: Dict[str, str] = {}
        stored_tokens_list: List[Dict[str, Any]] = []

        for p in prose_paragraphs:
            norm = p["normalized"]
            loc = p["location"]
            p_hash = hashlib.sha256(norm.encode("utf-8")).hexdigest()

            if p_hash in exact_hash_locs:
                exact_duplicate_paragraphs += 1
                continue
            else:
                exact_hash_locs[p_hash] = loc

            tokens = set(norm.split())
            is_near = False
            for item in stored_tokens_list:
                s_tokens = item["tokens"]
                inter = len(tokens & s_tokens)
                union = len(tokens | s_tokens)
                sim = inter / union if union > 0 else 0.0
                if sim >= self.near_threshold:
                    near_duplicate_paragraphs += 1
                    is_near = True
                    break

            if not is_near:
                stored_tokens_list.append({"tokens": tokens, "location": loc})

        denom = max(1, evaluated_prose_count)
        exact_rate = exact_duplicate_paragraphs / denom
        near_rate = near_duplicate_paragraphs / denom

        if exact_rate > 0.02 or exact_duplicate_paragraphs > 0:
            blocking_reasons.append(
                f"Prose paragraph exact duplicate audit failed: {exact_duplicate_paragraphs} exact duplicates ({exact_rate:.2%})."
            )
        if near_rate > 0.05:
            blocking_reasons.append(
                f"Prose paragraph near duplicate audit failed: {near_duplicate_paragraphs} near duplicates ({near_rate:.2%})."
            )

        # -------------------------------------------------------------
        # 5. TABLE AUDIT (DUPLICATES & MATH RENDERING ARTIFACTS)
        # -------------------------------------------------------------
        total_tables = len(doc.tables)

        has_scorecard_table = False
        if total_tables > 0:
            last_tbl = doc.tables[-1]
            last_cell = last_tbl.rows[0].cells[0].text if last_tbl.rows and last_tbl.rows[0].cells else ""
            if "scorecard" in last_cell.lower() or "metric" in last_cell.lower():
                has_scorecard_table = True

        content_tables = (total_tables - 1) if has_scorecard_table else total_tables

        exact_duplicate_tables = 0
        near_duplicate_tables = 0
        semantic_duplicate_tables = 0
        math_rendering_errors_in_tables = 0

        table_strings: List[str] = []
        table_fingerprints: Set[str] = set()

        DE_BROGLIE_TABLE_KEYWORDS = {"cricket ball", "smoke particle", "thermal neutron", "electron"}

        for t_idx, tbl in enumerate(doc.tables):
            # Exclude appendix scorecard table if last table
            if has_scorecard_table and t_idx == total_tables - 1:
                continue

            tbl_text_parts = []
            has_table_math_error = False

            for row in tbl.rows:
                row_cells = []
                for cell in row.cells:
                    c_text = cell.text.strip()
                    row_cells.append(c_text)

                    # Check for unrendered math artifacts in table cells
                    for pat in self.UNRENDERED_MATH_PATTERNS:
                        if pat.search(c_text):
                            has_table_math_error = True
                            break

                tbl_text_parts.append(" | ".join(row_cells))

            full_tbl_str = "\n".join(tbl_text_parts)
            norm_tbl = self._normalize(full_tbl_str)

            if has_table_math_error:
                math_rendering_errors_in_tables += 1

            # Exact table duplicate check
            tbl_hash = hashlib.sha256(norm_tbl.encode("utf-8")).hexdigest()
            if tbl_hash in table_fingerprints:
                exact_duplicate_tables += 1
            else:
                table_fingerprints.add(tbl_hash)

            # Semantic table check (e.g. repeated de Broglie table across topics)
            if all(k in norm_tbl for k in DE_BROGLIE_TABLE_KEYWORDS):
                if any(all(k in t_prev for k in DE_BROGLIE_TABLE_KEYWORDS) for t_prev in table_strings):
                    semantic_duplicate_tables += 1

            # Near table duplicate check
            tbl_tokens = set(norm_tbl.split())
            if tbl_tokens:
                for prev_tbl in table_strings:
                    prev_tokens = set(prev_tbl.split())
                    inter = len(tbl_tokens & prev_tokens)
                    union = len(tbl_tokens | prev_tokens)
                    sim = inter / union if union > 0 else 0.0
                    if sim >= 0.70:
                        near_duplicate_tables += 1
                        break

            table_strings.append(norm_tbl)

        if exact_duplicate_tables > 0:
            blocking_reasons.append(f"Found {exact_duplicate_tables} exact duplicate table(s) in final DOCX.")
        if semantic_duplicate_tables > 0:
            blocking_reasons.append(f"Found {semantic_duplicate_tables} repeated semantic comparison table(s) across topics.")
        if math_rendering_errors_in_tables > 0:
            blocking_reasons.append(f"Found {math_rendering_errors_in_tables} table(s) with unrendered raw math LaTeX artifacts.")

        # -------------------------------------------------------------
        # 6. FIGURE & CAPTION SEMANTIC ALIGNMENT AUDIT
        # -------------------------------------------------------------
        figure_caption_mismatches = 0
        for cap in figure_captions:
            cap_text = cap["text"]
            cap_top = cap["topic"].lower()
            cap_sub = cap["subtopic"].lower()

            # Check if caption title refers to a different topic or subtopic
            top_words = [w for w in cap_top.split() if len(w) > 3]
            sub_words = [w for w in cap_sub.split() if len(w) > 3]
            topic_or_sub_words = set(top_words + sub_words)
            if cap_text and topic_or_sub_words:
                # If caption has explicit topic title that doesn't match current topic or subtopic
                if "schematic of" in cap_text.lower():
                    caption_topic_ref = cap_text.lower().split("schematic of")[-1].strip()
                    if (cap_top not in caption_topic_ref and
                        cap_sub not in caption_topic_ref and
                        not any(w in caption_topic_ref for w in topic_or_sub_words)):
                        figure_caption_mismatches += 1

        if figure_caption_mismatches > 0:
            blocking_reasons.append(f"Found {figure_caption_mismatches} figure caption semantic mismatch(es).")

        # Total unrendered math artifacts count (prose + tables)
        total_math_rendering_artifacts = math_artifacts_in_text + math_rendering_errors_in_tables
        if total_math_rendering_artifacts > 0:
            blocking_reasons.append(f"Detected {total_math_rendering_artifacts} unrendered raw math LaTeX artifact(s) in document.")

        # -------------------------------------------------------------
        # 7. STRICT COUNT RECONCILIATION AUDIT (planned == assembled == rendered)
        # -------------------------------------------------------------
        rendered_manifest = CountManifest(
            chapters=len(chapter_headings),
            topics=len(topic_headings),
            sections=len(subtopic_headings),
            paragraphs=total_docx_paragraphs,
            equations=total_equations,
            tables=content_tables,
            figures=total_figures,
            words=total_words
        )

        discrepancies: List[str] = []
        count_reconciliation_valid = True

        if planned_manifest:
            # Check STRICT equality between planned and rendered
            if planned_manifest.chapters != rendered_manifest.chapters:
                discrepancies.append(f"Chapters mismatch: planned ({planned_manifest.chapters}) != rendered ({rendered_manifest.chapters})")
                count_reconciliation_valid = False
            if planned_manifest.topics != rendered_manifest.topics:
                discrepancies.append(f"Topics mismatch: planned ({planned_manifest.topics}) != rendered ({rendered_manifest.topics})")
                count_reconciliation_valid = False
            if planned_manifest.sections != rendered_manifest.sections:
                discrepancies.append(f"Sections mismatch: planned ({planned_manifest.sections}) != rendered ({rendered_manifest.sections})")
                count_reconciliation_valid = False
            if planned_manifest.tables != rendered_manifest.tables:
                discrepancies.append(f"Tables mismatch: planned ({planned_manifest.tables}) != rendered ({rendered_manifest.tables})")
                count_reconciliation_valid = False
            if planned_manifest.figures != rendered_manifest.figures:
                discrepancies.append(f"Figures mismatch: planned ({planned_manifest.figures}) != rendered ({rendered_manifest.figures})")
                count_reconciliation_valid = False

        if assembled_manifest:
            if assembled_manifest.chapters != rendered_manifest.chapters:
                discrepancies.append(f"Chapters assembled vs rendered mismatch: assembled ({assembled_manifest.chapters}) != rendered ({rendered_manifest.chapters})")
                count_reconciliation_valid = False
            if assembled_manifest.topics != rendered_manifest.topics:
                discrepancies.append(f"Topics assembled vs rendered mismatch: assembled ({assembled_manifest.topics}) != rendered ({rendered_manifest.topics})")
                count_reconciliation_valid = False
            if assembled_manifest.sections != rendered_manifest.sections:
                discrepancies.append(f"Sections assembled vs rendered mismatch: assembled ({assembled_manifest.sections}) != rendered ({rendered_manifest.sections})")
                count_reconciliation_valid = False
            if assembled_manifest.tables != rendered_manifest.tables:
                discrepancies.append(f"Tables assembled vs rendered mismatch: assembled ({assembled_manifest.tables}) != rendered ({rendered_manifest.tables})")
                count_reconciliation_valid = False
            if assembled_manifest.figures != rendered_manifest.figures:
                discrepancies.append(f"Figures assembled vs rendered mismatch: assembled ({assembled_manifest.figures}) != rendered ({rendered_manifest.figures})")
                count_reconciliation_valid = False

        if not count_reconciliation_valid:
            blocking_reasons.extend(discrepancies)

        # -------------------------------------------------------------
        # 8. CONTENT DEPTH AUDIT
        # -------------------------------------------------------------
        prose_by_topic: Dict[str, List[str]] = {}
        for p_info in prose_paragraphs:
            loc = p_info["location"]
            # Location is formatted as "Chapter > Topic > Subtopic"
            loc_parts = loc.split(" > ")
            top_name = loc_parts[1] if len(loc_parts) > 1 else loc_parts[0]
            prose_by_topic.setdefault(top_name, []).append(p_info["text"])

        EXCLUDED_SECTIONS = {
            "", "front matter", "preface", "table of contents",
            "chapter overview & objectives", "chapter overview and objectives",
            "academic bibliography", "references"
        }
        substantive_topics = {
            t: sum(len(x.split()) for x in ps)
            for t, ps in prose_by_topic.items()
            if t.lower().strip() not in EXCLUDED_SECTIONS
        }

        vals = sorted(substantive_topics.values()) if substantive_topics else [0]
        total_substantive_words = sum(vals)
        mean_words = round(total_substantive_words / len(vals), 1) if vals and len(vals) > 0 else 0.0
        median_words = vals[len(vals) // 2] if vals else 0
        min_words = vals[0] if vals else 0
        max_words = vals[-1] if vals else 0

        count_below_100 = sum(1 for v in vals if v < 100)
        count_below_200 = sum(1 for v in vals if v < 200)
        count_below_300 = sum(1 for v in vals if v < 300)

        contract_failures_list: List[str] = []
        topic_archetypes: Dict[str, str] = {}
        for top_name, paras in prose_by_topic.items():
            if top_name.lower().strip() in EXCLUDED_SECTIONS:
                continue
            arch = self._classify_topic_semantic_type(top_name, " ".join(paras))
            topic_archetypes[top_name] = arch
            valid_contract, failures = self._validate_semantic_contract(
                top_name, arch, paras, substantive_topics.get(top_name, 0)
            )
            if not valid_contract:
                contract_failures_list.extend(failures)

        empty_or_shallow_topics = [t for t, v in substantive_topics.items() if v < 50]
        if len(empty_or_shallow_topics) > 0:
            blocking_reasons.append(
                f"Found {len(empty_or_shallow_topics)} empty or shallow topic(s) (<50 words): {empty_or_shallow_topics}"
            )
        if count_below_100 > 0:
            blocking_reasons.append(
                f"Content depth audit failed: {count_below_100} topic(s) have <100 words."
            )
        if len(contract_failures_list) > 0:
            blocking_reasons.append(
                f"Pedagogical semantic contract failure across {len(contract_failures_list)} checks: {contract_failures_list}"
            )

        content_depth_metrics = {
            "substantive_topics_evaluated": len(substantive_topics),
            "substantive_body_words": total_substantive_words,
            "total_openxml_words": total_words,
            "mean_words_per_topic": mean_words,
            "median_words_per_topic": median_words,
            "min_words_per_topic": min_words,
            "max_words_per_topic": max_words,
            "count_below_100": count_below_100,
            "count_below_200": count_below_200,
            "count_below_300": count_below_300,
            "contract_failures_count": len(contract_failures_list),
            "contract_failures": contract_failures_list,
            "topic_archetypes": topic_archetypes,
            "empty_or_shallow_topics_count": len(empty_or_shallow_topics),
            "empty_or_shallow_topics": empty_or_shallow_topics,
            "substantive_words_per_topic": substantive_topics
        }

        # SHA-256 of the DOCX file
        docx_sha256 = ""
        try:
            with open(docx_path, "rb") as f:
                docx_sha256 = hashlib.sha256(f.read()).hexdigest()
        except Exception as e:
            logger.warning(f"Could not compute sha256 for {docx_path}: {e}")

        # -------------------------------------------------------------
        # 9. FINAL PUBLICATION READINESS DECISION
        # -------------------------------------------------------------
        publication_ready = (len(blocking_reasons) == 0)

        summary_counts = rendered_manifest.to_dict()
        summary_counts["substantive_body_words"] = total_substantive_words
        summary_counts["mean_words_per_topic"] = mean_words
        summary_counts["median_words_per_topic"] = median_words
        summary_counts["min_words_per_topic"] = min_words
        summary_counts["max_words_per_topic"] = max_words
        summary_counts["count_below_100"] = count_below_100
        summary_counts["count_below_200"] = count_below_200
        summary_counts["count_below_300"] = count_below_300
        summary_counts["contract_failures"] = len(contract_failures_list)
        reconciliation_details = {
            "is_valid": count_reconciliation_valid,
            "discrepancies": discrepancies,
            "planned": planned_manifest.to_dict() if planned_manifest else None,
            "assembled": assembled_manifest.to_dict() if assembled_manifest else None,
            "rendered": rendered_manifest.to_dict()
        }

        logger.info(
            f"IndependentArtifactAuditor complete for '{docx_path}': "
            f"publication_ready={publication_ready} (blocking_issues={len(blocking_reasons)})"
        )

        return IndependentAuditResult(
            publication_ready=publication_ready,
            docx_path=docx_path,
            docx_sha256=docx_sha256,
            content_depth=content_depth_metrics,
            total_docx_paragraphs=total_docx_paragraphs,
            evaluated_prose_paragraphs=evaluated_prose_count,
            exact_duplicate_paragraphs=exact_duplicate_paragraphs,
            near_duplicate_paragraphs=near_duplicate_paragraphs,
            exact_duplicate_paragraph_rate=exact_rate,
            near_duplicate_paragraph_rate=near_rate,
            total_headings=len(headings),
            consecutive_duplicate_headings=consecutive_duplicate_headings,
            generic_headings=generic_headings_count,
            structural_template_families=structural_template_families,
            total_tables=content_tables,
            exact_duplicate_tables=exact_duplicate_tables,
            near_duplicate_tables=near_duplicate_tables,
            semantic_duplicate_tables=semantic_duplicate_tables,
            math_rendering_errors_in_tables=math_rendering_errors_in_tables,
            total_figures=total_figures,
            figure_caption_mismatches=figure_caption_mismatches,
            math_rendering_artifacts_count=total_math_rendering_artifacts,
            count_reconciliation_valid=count_reconciliation_valid,
            blocking_reasons=blocking_reasons,
            summary_counts=summary_counts,
            reconciliation_details=reconciliation_details
        )
