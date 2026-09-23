"""
RepetitionDetectionAgent — Identifies duplicate and near-duplicate text across sections.
Detects redundant paragraphs, repeated introductory boilerplate, and duplicate examples
to guarantee fresh, progressive academic prose across the textbook.
"""

import re
from typing import Dict, Any, List, Set

class RepetitionDetectionAgent:
    """
    Maintains a rolling registry of generated paragraphs and detects verbatim or
    near-verbatim redundancy across chapters and sections.
    """

    def __init__(self, similarity_threshold: float = 0.80):
        self.similarity_threshold = similarity_threshold
        self.seen_paragraphs: List[Dict[str, Any]] = []  # {"hash": int, "words": Set[str], "text": str, "section": str}

    def _tokenize(self, text: str) -> Set[str]:
        words = re.findall(r"\b\w{3,}\b", text.lower())
        return set(words)

    def _jaccard_similarity(self, set_a: Set[str], set_b: Set[str]) -> float:
        if not set_a or not set_b:
            return 0.0
        intersection = len(set_a & set_b)
        union = len(set_a | set_b)
        return intersection / union if union > 0 else 0.0

    def audit_section(self, section_title: str, content: str) -> Dict[str, Any]:
        """
        Audits a newly generated section against all previously seen paragraphs.
        """
        paragraphs = [p.strip() for p in content.split("\n\n") if len(p.strip().split()) >= 15]
        duplicates_found = []

        for p_idx, p_text in enumerate(paragraphs):
            p_words = self._tokenize(p_text)
            for prev in self.seen_paragraphs:
                # Direct exact match check
                if p_text == prev["text"]:
                    duplicates_found.append({
                        "type": "exact_duplicate",
                        "current_section": section_title,
                        "matched_section": prev["section"],
                        "excerpt": p_text[:80]
                    })
                    break
                # Near-duplicate Jaccard check
                sim = self._jaccard_similarity(p_words, prev["words"])
                if sim >= self.similarity_threshold:
                    duplicates_found.append({
                        "type": "near_duplicate",
                        "similarity": round(sim, 2),
                        "current_section": section_title,
                        "matched_section": prev["section"],
                        "excerpt": p_text[:80]
                    })
                    break

            # Register current paragraph for future checks
            self.seen_paragraphs.append({
                "words": p_words,
                "text": p_text,
                "section": section_title
            })

        return {
            "duplicate_count": len(duplicates_found),
            "duplicates": duplicates_found,
            "has_critical_redundancy": len(duplicates_found) > 0
        }

    def register_section_paragraphs(self, content: str, section_title: str) -> List[Dict[str, Any]]:
        """Audits content and returns list of duplicate issues found."""
        res = self.audit_section(section_title, content)
        return res.get("duplicates", [])

    def get_summary(self) -> Dict[str, Any]:
        """Returns overall repetition statistics."""
        return {
            "total_registered_paragraphs": len(self.seen_paragraphs),
            "similarity_threshold": self.similarity_threshold
        }
