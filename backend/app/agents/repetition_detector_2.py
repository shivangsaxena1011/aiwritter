import re
import hashlib
from typing import Dict, Any, List, Optional, Tuple, Set
from dataclasses import dataclass, field
import logging

logger = logging.getLogger(__name__)


@dataclass
class RepetitionCheckResult:
    is_duplicate: bool
    duplicate_level: Optional[str] = None  # "EXACT" | "NEAR" | "CONCEPTUAL" | None
    similarity_score: float = 0.0
    matching_location: Optional[str] = None
    details: str = "Unique content."

    def to_dict(self) -> Dict[str, Any]:
        return {
            "is_duplicate": self.is_duplicate,
            "duplicate_level": self.duplicate_level,
            "similarity_score": round(self.similarity_score, 3),
            "matching_location": self.matching_location,
            "details": self.details
        }


class RepetitionDetector2:
    """3-Level Repetition Detection System:
    Level 1: Exact duplicate (SHA-256 hash of normalized text)
    Level 2: Near duplicate (Token Jaccard / n-gram similarity >= 0.70)
    Level 3: Conceptual duplicate (Shared set of equations, claims, experiments)

    Mathematically sound duplicate rate tracking:
    duplicate_rate = duplicates / max(1, total_candidates_evaluated), bounded [0.0, 1.0].
    """

    def __init__(self, near_threshold: float = 0.70, min_word_count: int = 15):
        self.near_threshold = near_threshold
        self.min_word_count = min_word_count
        self.exact_hashes: Dict[str, str] = {}  # hash -> location
        self.stored_paragraphs: List[Dict[str, Any]] = []  # [{tokens, equations, claims, location, text}]
        self.total_candidates_evaluated = 0
        self.exact_duplicate_count = 0
        self.near_duplicate_count = 0
        self.conceptual_duplicate_count = 0
        self.unique_duplicate_strings: Set[str] = set()
        self.duplicate_occurrences = 0
        self.affected_paragraphs: List[Dict[str, Any]] = []

    @staticmethod
    def _normalize(text: str) -> str:
        t = re.sub(r"[^\w\s]", "", text.lower())
        return " ".join(t.split())

    @staticmethod
    def _extract_equations(text: str) -> Set[str]:
        # Extract latex equations $...$ or $$...$$
        eqs = set(re.findall(r"\$(?:\\\$|[^\$])+\$", text))
        return {e.replace("$", "").strip().lower() for e in eqs if len(e) > 3}

    def check_candidate(self, paragraph_text: str, location: str) -> RepetitionCheckResult:
        words = paragraph_text.split()
        if len(words) < self.min_word_count:
            return RepetitionCheckResult(is_duplicate=False)

        norm = self._normalize(paragraph_text)
        if not norm:
            return RepetitionCheckResult(is_duplicate=False)

        self.total_candidates_evaluated += 1

        # Level 1: Exact Duplicate Check
        h = hashlib.sha256(norm.encode("utf-8")).hexdigest()
        if h in self.exact_hashes:
            self.exact_duplicate_count += 1
            self.duplicate_occurrences += 1
            self.unique_duplicate_strings.add(norm[:100])
            self.affected_paragraphs.append({
                "location": location,
                "level": "EXACT",
                "matching_location": self.exact_hashes[h],
                "snippet": paragraph_text[:120]
            })
            return RepetitionCheckResult(
                is_duplicate=True,
                duplicate_level="EXACT",
                similarity_score=1.0,
                matching_location=self.exact_hashes[h],
                details=f"Exact duplicate paragraph previously introduced in '{self.exact_hashes[h]}'."
            )

        # Level 2: Near Duplicate Check
        tokens = set(norm.split())
        candidate_eqs = self._extract_equations(paragraph_text)

        best_sim = 0.0
        best_loc = None

        for item in self.stored_paragraphs:
            stored_tokens = item["tokens"]
            inter = len(tokens & stored_tokens)
            union = len(tokens | stored_tokens)
            sim = inter / union if union > 0 else 0.0

            if sim > best_sim:
                best_sim = sim
                best_loc = item["location"]

            if sim >= self.near_threshold:
                self.near_duplicate_count += 1
                self.duplicate_occurrences += 1
                self.unique_duplicate_strings.add(norm[:100])
                self.affected_paragraphs.append({
                    "location": location,
                    "level": "NEAR",
                    "matching_location": item["location"],
                    "similarity": round(sim, 3),
                    "snippet": paragraph_text[:120]
                })
                return RepetitionCheckResult(
                    is_duplicate=True,
                    duplicate_level="NEAR",
                    similarity_score=sim,
                    matching_location=item["location"],
                    details=f"Near-duplicate paragraph ({sim:.1%} token similarity) previously in '{item['location']}'."
                )

            # Level 3: Conceptual Duplicate (High equation & core keyword overlap even if prose varies)
            if candidate_eqs and item["equations"]:
                eq_inter = candidate_eqs & item["equations"]
                if len(eq_inter) >= 2 and sim >= 0.25:
                    self.conceptual_duplicate_count += 1
                    self.duplicate_occurrences += 1
                    self.affected_paragraphs.append({
                        "location": location,
                        "level": "CONCEPTUAL",
                        "matching_location": item["location"],
                        "similarity": round(sim, 3),
                        "snippet": paragraph_text[:120]
                    })
                    return RepetitionCheckResult(
                        is_duplicate=True,
                        duplicate_level="CONCEPTUAL",
                        similarity_score=sim,
                        matching_location=item["location"],
                        details=f"Conceptual duplicate sharing equations {list(eq_inter)} with '{item['location']}'."
                    )

        return RepetitionCheckResult(
            is_duplicate=False,
            similarity_score=best_sim,
            matching_location=best_loc
        )

    def register_paragraph(self, paragraph_text: str, location: str):
        words = paragraph_text.split()
        if len(words) < self.min_word_count:
            return

        norm = self._normalize(paragraph_text)
        if not norm:
            return

        h = hashlib.sha256(norm.encode("utf-8")).hexdigest()
        self.exact_hashes[h] = location

        tokens = set(norm.split())
        eqs = self._extract_equations(paragraph_text)

        self.stored_paragraphs.append({
            "tokens": tokens,
            "equations": eqs,
            "location": location,
            "text": paragraph_text[:120]
        })

    def get_summary(self) -> Dict[str, Any]:
        total_eval = max(1, self.total_candidates_evaluated)
        exact_rate = min(1.0, max(0.0, self.exact_duplicate_count / total_eval))
        near_rate = min(1.0, max(0.0, self.near_duplicate_count / total_eval))
        conceptual_rate = min(1.0, max(0.0, self.conceptual_duplicate_count / total_eval))

        return {
            "total_candidates_evaluated": self.total_candidates_evaluated,
            "total_registered_paragraphs": len(self.stored_paragraphs),
            "exact_duplicates_detected": self.exact_duplicate_count,
            "near_duplicates_detected": self.near_duplicate_count,
            "conceptual_duplicates_detected": self.conceptual_duplicate_count,
            "unique_duplicate_strings": len(self.unique_duplicate_strings),
            "duplicate_occurrences": self.duplicate_occurrences,
            "exact_duplicate_rate": round(exact_rate, 4),
            "near_duplicate_rate": round(near_rate, 4),
            "conceptual_duplicate_rate": round(conceptual_rate, 4),
            "affected_paragraphs_count": len(self.affected_paragraphs)
        }

    def audit_docx_paragraphs(self, paragraphs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Runs rigorous repetition audit on extracted DOCX paragraphs.
        
        Args:
            paragraphs: List of dicts, e.g. [{"text": str, "location": str, "is_heading": bool}]
        """
        auditor = RepetitionDetector2(near_threshold=self.near_threshold, min_word_count=self.min_word_count)
        
        for p in paragraphs:
            # Skip headings, captions, very short lines
            if p.get("is_heading"):
                continue
            text = p.get("text", "").strip()
            loc = p.get("location", "DOCX Paragraph")
            words = text.split()
            if len(words) < self.min_word_count:
                continue

            check = auditor.check_candidate(text, loc)
            if not check.is_duplicate:
                auditor.register_paragraph(text, loc)

        summary = auditor.get_summary()
        summary["passed"] = (
            summary["exact_duplicate_rate"] <= 0.02 and
            summary["near_duplicate_rate"] <= 0.05
        )
        summary["affected_paragraphs"] = auditor.affected_paragraphs[:20]  # top 20 for diagnosis
        return summary
