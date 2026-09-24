import re
import os
import json
import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)

FORBIDDEN_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "forbidden_quantum_content.json"))


@dataclass
class ContaminationCheckResult:
    is_contaminated: bool
    contamination_score: float  # 0.0 to 1.0 (0.0 = completely clean)
    forbidden_terms_found: List[str] = field(default_factory=list)
    irrelevant_physics_detected: List[str] = field(default_factory=list)
    verdict: str = "clean"  # "clean" | "warning" | "rejected"
    details: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "is_contaminated": self.is_contaminated,
            "contamination_score": self.contamination_score,
            "forbidden_terms_found": self.forbidden_terms_found,
            "irrelevant_physics_detected": self.irrelevant_physics_detected,
            "verdict": self.verdict,
            "details": self.details
        }


class TopicContaminationDetector:
    """Detects topic contamination and cross-leakage before content reaches assembly."""

    def __init__(self):
        self.global_forbidden: List[str] = []
        self.topic_specific_forbidden: Dict[str, List[str]] = {}
        self._load_forbidden_rules()

    def _load_forbidden_rules(self):
        if os.path.exists(FORBIDDEN_FILE):
            try:
                with open(FORBIDDEN_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.global_forbidden = data.get("forbidden_global_phrases", [])
                    self.topic_specific_forbidden = data.get("forbidden_topic_contamination", {})
            except Exception as e:
                logger.warning(f"Failed to load forbidden quantum content: {e}")

    def check_paragraph(
        self,
        paragraph_text: str,
        topic_title: str,
        allowed_concepts: Optional[List[str]] = None,
        forbidden_concepts: Optional[List[str]] = None
    ) -> ContaminationCheckResult:
        """Inspects a single paragraph for banned phrases, foreign topic overlap, or forbidden concepts."""
        p_clean = paragraph_text.lower()
        forbidden_found: List[str] = []

        # 1. Check global synthetic phrases
        for phrase in self.global_forbidden:
            if phrase.lower() in p_clean:
                forbidden_found.append(phrase)

        # 2. Check topic-specific forbidden concepts from config
        topic_lower = topic_title.lower()
        for t_key, terms in self.topic_specific_forbidden.items():
            if t_key.lower() in topic_lower:
                for term in terms:
                    if term.lower() in p_clean:
                        forbidden_found.append(term)

        # 3. Check dynamically supplied forbidden concepts from TopicBoundaryContract
        if forbidden_concepts:
            for f_term in forbidden_concepts:
                if f_term.lower() in p_clean and f_term not in forbidden_found:
                    forbidden_found.append(f_term)

        # 4. Check for obvious out-of-domain engineering leaks (laser terms in photoelectric, etc.)
        irrelevant_physics: List[str] = []
        laser_terms = ["population inversion", "stimulated emission", "metastable state", "optical resonator"]
        fiber_terms = ["acceptance cone", "numerical aperture", "core-cladding boundary", "v-number"]

        if "photoelectric" in topic_lower or "de broglie" in topic_lower or "operators" in topic_lower:
            for lt in laser_terms:
                if lt in p_clean:
                    irrelevant_physics.append(f"Laser physics term '{lt}' leaked into {topic_title}")
            for ft in fiber_terms:
                if ft in p_clean:
                    irrelevant_physics.append(f"Fiber optics term '{ft}' leaked into {topic_title}")

        all_violations = forbidden_found + irrelevant_physics
        is_contaminated = len(all_violations) > 0
        score = min(1.0, len(all_violations) * 0.35)

        verdict = "rejected" if is_contaminated else "clean"
        details = f"Detected {len(all_violations)} violations: {', '.join(all_violations)}" if is_contaminated else "Paragraph clean."

        return ContaminationCheckResult(
            is_contaminated=is_contaminated,
            contamination_score=score,
            forbidden_terms_found=forbidden_found,
            irrelevant_physics_detected=irrelevant_physics,
            verdict=verdict,
            details=details
        )

    def filter_clean_paragraphs(
        self,
        section_content: str,
        topic_title: str,
        forbidden_concepts: Optional[List[str]] = None
    ) -> str:
        """Splits section into paragraphs and removes any contaminated paragraphs."""
        paragraphs = section_content.split("\n\n")
        clean_paras = []
        for p in paragraphs:
            if not p.strip() or p.strip().startswith("#"):
                clean_paras.append(p)
                continue
            if not hasattr(self, "total_inspections"):
                self.total_inspections = 0
                self.cleaned_paragraphs = 0
            self.total_inspections += 1
            res = self.check_paragraph(p, topic_title, forbidden_concepts=forbidden_concepts)
            if not res.is_contaminated:
                clean_paras.append(p)
            else:
                self.cleaned_paragraphs += 1
                logger.warning(f"TopicContaminationDetector filtered out paragraph in '{topic_title}': {res.details}")

        return "\n\n".join(clean_paras)

    def get_summary(self) -> Dict[str, Any]:
        return {
            "total_inspections": getattr(self, "total_inspections", 0),
            "cleaned_paragraphs": getattr(self, "cleaned_paragraphs", 0)
        }
