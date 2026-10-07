import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class CountManifest:
    chapters: int = 0
    topics: int = 0
    sections: int = 0
    paragraphs: int = 0
    equations: int = 0
    tables: int = 0
    figures: int = 0
    words: int = 0

    def to_dict(self) -> Dict[str, int]:
        return {
            "chapters": self.chapters,
            "topics": self.topics,
            "sections": self.sections,
            "paragraphs": self.paragraphs,
            "equations": self.equations,
            "tables": self.tables,
            "figures": self.figures,
            "words": self.words
        }


@dataclass
class IntegrityAuditResult:
    is_valid: bool
    discrepancies: List[str]
    reconciliation_table: Dict[str, Dict[str, Any]]
    details: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "is_valid": self.is_valid,
            "discrepancies": self.discrepancies,
            "reconciliation_table": self.reconciliation_table,
            "details": self.details
        }


class ArtifactIntegrityManifest:
    """Enforces strict three-way count reconciliation:
    PLANNED == ASSEMBLED == RENDERED_DOCX.
    
    Hard failure if structural counts (chapters, topics, sections) do not match exactly.
    Hard failure if assembled figures and tables fail to render in DOCX.
    """

    def __init__(
        self,
        planned: CountManifest,
        assembled: CountManifest,
        rendered_docx: CountManifest
    ):
        self.planned = planned
        self.assembled = assembled
        self.rendered_docx = rendered_docx

    def reconcile(self) -> IntegrityAuditResult:
        discrepancies: List[str] = []

        # Structural reconciliation: Chapters
        if self.planned.chapters != self.assembled.chapters:
            discrepancies.append(
                f"Chapter count mismatch: planned={self.planned.chapters}, assembled={self.assembled.chapters}"
            )
        if self.assembled.chapters != self.rendered_docx.chapters:
            discrepancies.append(
                f"Chapter count mismatch: assembled={self.assembled.chapters}, rendered={self.rendered_docx.chapters}"
            )

        # Structural reconciliation: Topics
        if self.planned.topics != self.assembled.topics:
            discrepancies.append(
                f"Topic count mismatch: planned={self.planned.topics}, assembled={self.assembled.topics}"
            )
        if self.assembled.topics != self.rendered_docx.topics:
            discrepancies.append(
                f"Topic count mismatch: assembled={self.assembled.topics}, rendered={self.rendered_docx.topics}"
            )

        # Structural reconciliation: Sections / Subtopics
        if self.planned.sections != self.assembled.sections:
            discrepancies.append(
                f"Section count mismatch: planned={self.planned.sections}, assembled={self.assembled.sections}"
            )
        if self.assembled.sections != self.rendered_docx.sections:
            discrepancies.append(
                f"Section count mismatch: assembled={self.assembled.sections}, rendered={self.rendered_docx.sections}"
            )

        # Tables reconciliation: Assembled vs Rendered Word Tables
        # Rendered tables include scorecard table (+1) if back matter scorecard was added
        table_diff = abs(self.rendered_docx.tables - self.assembled.tables)
        tbl_match = False
        if self.planned.tables == 0 and self.assembled.tables == 0 and self.rendered_docx.tables == 0:
            tbl_match = True
        elif self.planned.tables == 0 and self.rendered_docx.tables > 1:
            tbl_match = False
            discrepancies.append(
                f"Table count discrepancy: planned=0, assembled={self.assembled.tables}, but rendered={self.rendered_docx.tables}"
            )
        elif table_diff <= 1:
            tbl_match = (self.planned.tables == self.assembled.tables) or (self.planned.tables == 0 and self.assembled.tables <= 1)
            if not tbl_match:
                discrepancies.append(
                    f"Table count mismatch: planned={self.planned.tables}, assembled={self.assembled.tables}, rendered={self.rendered_docx.tables}"
                )
        else:
            tbl_match = False
            discrepancies.append(
                f"Table count mismatch: assembled={self.assembled.tables}, rendered={self.rendered_docx.tables}"
            )

        # Figures reconciliation: Assembled vs Rendered Word Shapes / Figures
        fig_match = False
        if self.planned.figures == 0 and self.assembled.figures == 0 and self.rendered_docx.figures == 0:
            fig_match = True
        elif self.planned.figures == 0 and self.rendered_docx.figures > 0 and self.assembled.figures == 0:
            fig_match = False
            discrepancies.append(
                f"Figure count discrepancy: planned=0, assembled=0, but rendered={self.rendered_docx.figures}"
            )
        elif self.assembled.figures != self.rendered_docx.figures:
            fig_match = False
            discrepancies.append(
                f"Figure count mismatch: assembled={self.assembled.figures}, rendered={self.rendered_docx.figures}"
            )
        else:
            fig_match = (self.planned.figures == self.assembled.figures == self.rendered_docx.figures) or (self.planned.figures == 0 and self.assembled.figures == self.rendered_docx.figures)

        # Equation reconciliation: Strict rejection if planned=0 while rendered>0
        eq_match = False
        if self.planned.equations == 0 and self.assembled.equations == 0 and self.rendered_docx.equations == 0:
            eq_match = True
        elif self.planned.equations == 0 and self.rendered_docx.equations > 0 and self.assembled.equations == 0:
            eq_match = False
            discrepancies.append(
                f"Equation count discrepancy: planned=0, assembled=0, but rendered={self.rendered_docx.equations}"
            )
        elif self.assembled.equations == 0 and self.rendered_docx.equations > 0:
            eq_match = False
            discrepancies.append(
                f"Equation count discrepancy: assembled has 0 equations, but rendered={self.rendered_docx.equations} in DOCX"
            )
        elif self.assembled.equations > 0 and self.rendered_docx.equations == 0:
            eq_match = False
            discrepancies.append(
                f"Equation failure: assembled {self.assembled.equations} equations, but 0 rendered in DOCX"
            )
        else:
            # Both assembled > 0 and rendered > 0
            if self.planned.equations > 0:
                eq_match = (
                    self.planned.equations == self.assembled.equations == self.rendered_docx.equations
                    or abs(self.assembled.equations - self.rendered_docx.equations) <= max(2, int(0.15 * self.assembled.equations))
                )
                if not eq_match:
                    discrepancies.append(
                        f"Equation count mismatch: planned={self.planned.equations}, assembled={self.assembled.equations}, rendered={self.rendered_docx.equations}"
                    )
            else:
                eq_match = (self.assembled.equations == self.rendered_docx.equations)
                if not eq_match:
                    discrepancies.append(
                        f"Equation count mismatch: assembled={self.assembled.equations}, rendered={self.rendered_docx.equations}"
                    )

        # Paragraph & Word sanity checks
        if self.rendered_docx.words < 50:
            discrepancies.append(f"Suspiciously low word count in DOCX: {self.rendered_docx.words}")

        words_match = False
        if self.planned.words == 0 and self.assembled.words == 0 and self.rendered_docx.words == 0:
            words_match = True
        elif self.planned.words == 0:
            words_match = (self.rendered_docx.words >= max(50, int(0.7 * self.assembled.words))) if self.assembled.words > 0 else (self.rendered_docx.words >= 50)
        else:
            words_match = (self.rendered_docx.words >= max(50, int(0.7 * self.planned.words)))
            if not words_match:
                discrepancies.append(
                    f"Word count mismatch: planned={self.planned.words}, rendered={self.rendered_docx.words}"
                )

        table = {
            "chapters": {
                "planned": self.planned.chapters,
                "assembled": self.assembled.chapters,
                "rendered_docx": self.rendered_docx.chapters,
                "match": (self.planned.chapters == self.assembled.chapters == self.rendered_docx.chapters)
            },
            "topics": {
                "planned": self.planned.topics,
                "assembled": self.assembled.topics,
                "rendered_docx": self.rendered_docx.topics,
                "match": (self.planned.topics == self.assembled.topics == self.rendered_docx.topics)
            },
            "sections": {
                "planned": self.planned.sections,
                "assembled": self.assembled.sections,
                "rendered_docx": self.rendered_docx.sections,
                "match": (self.planned.sections == self.assembled.sections == self.rendered_docx.sections)
            },
            "tables": {
                "planned": self.planned.tables,
                "assembled": self.assembled.tables,
                "rendered_docx": self.rendered_docx.tables,
                "match": tbl_match
            },
            "figures": {
                "planned": self.planned.figures,
                "assembled": self.assembled.figures,
                "rendered_docx": self.rendered_docx.figures,
                "match": fig_match
            },
            "equations": {
                "planned": self.planned.equations,
                "assembled": self.assembled.equations,
                "rendered_docx": self.rendered_docx.equations,
                "match": eq_match
            },
            "words": {
                "planned": self.planned.words,
                "assembled": self.assembled.words,
                "rendered_docx": self.rendered_docx.words,
                "match": words_match
            }
        }

        is_valid = len(discrepancies) == 0
        details = "Artifact integrity verified: planned, assembled, and rendered counts reconcile." if is_valid else (
            f"Integrity check failed with {len(discrepancies)} discrepancies: " + "; ".join(discrepancies)
        )

        return IntegrityAuditResult(
            is_valid=is_valid,
            discrepancies=discrepancies,
            reconciliation_table=table,
            details=details
        )
