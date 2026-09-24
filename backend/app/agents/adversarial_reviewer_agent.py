import re
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
import logging

logger = logging.getLogger(__name__)


@dataclass
class AdversarialIssue:
    severity: str  # "CRITICAL" | "ERROR" | "WARNING" | "INFO"
    category: str  # "REPETITION" | "CONTAMINATION" | "UNSUPPORTED_CLAIM" | "IRRELEVANT_EQUATION" | "PEDAGOGICAL"
    location: str
    description: str
    recommendation: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "severity": self.severity,
            "category": self.category,
            "location": self.location,
            "description": self.description,
            "recommendation": self.recommendation
        }


@dataclass
class AdversarialReviewResult:
    passed: bool
    issues: List[AdversarialIssue] = field(default_factory=list)
    critical_count: int = 0
    error_count: int = 0
    warning_count: int = 0
    info_count: int = 0
    publication_ready: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "passed": self.passed,
            "publication_ready": self.publication_ready,
            "critical_count": self.critical_count,
            "error_count": self.error_count,
            "warning_count": self.warning_count,
            "info_count": self.info_count,
            "issues": [i.to_dict() for i in self.issues]
        }


class AdversarialReviewerAgent:
    """Rigorous adversarial reviewer checking chapter integrity before publication release."""

    def review_chapter(
        self,
        sections: List[Dict[str, Any]],
        chapter_title: str,
        subject: str,
        allow_warnings: bool = False
    ) -> AdversarialReviewResult:
        issues: List[AdversarialIssue] = []

        seen_derivations: Dict[str, str] = {}
        seen_intro_phrases: Dict[str, str] = {}

        for sec in sections:
            loc = f"{sec.get('topic', 'General')} > {sec.get('subtopic', 'Section')}"
            content = sec.get("content", "")
            content_lower = content.lower()

            # 1. Check for banned synthetic phrases
            if "configuration alpha" in content_lower or "configuration beta" in content_lower:
                issues.append(AdversarialIssue(
                    severity="CRITICAL",
                    category="UNSUPPORTED_CLAIM",
                    location=loc,
                    description="Detected synthetic placeholder 'Configuration Alpha/Beta'.",
                    recommendation="Remove fabricated configuration references."
                ))

            if "\\dot{s}_{gen}" in content_lower or "dot{s}_{gen}" in content_lower:
                issues.append(AdversarialIssue(
                    severity="CRITICAL",
                    category="IRRELEVANT_EQUATION",
                    location=loc,
                    description="Detected irrelevant generic entropy generation/diffusion equation.",
                    recommendation="Replace with subject-specific quantum mechanical equation."
                ))

            # 2. Check for topic contamination
            t_name = sec.get("topic", "").lower()
            if "photoelectric" in t_name and ("population inversion" in content_lower or "optical resonator" in content_lower):
                issues.append(AdversarialIssue(
                    severity="ERROR",
                    category="CONTAMINATION",
                    location=loc,
                    description="Detected laser physics terms inside Photoelectric Effect.",
                    recommendation="Remove out-of-context laser concepts from photoelectric topic."
                ))

            # 3. Check for repeated analytical derivations
            if "e_n = \\frac{n^2 h^2}{8ml^2}" in content_lower or "8ml^2" in content_lower:
                if "particle in a 1d box" not in t_name and "applications" not in t_name:
                    issues.append(AdversarialIssue(
                        severity="WARNING",
                        category="REPETITION",
                        location=loc,
                        description="Particle in a box energy equation reappearing outside its owner topic.",
                        recommendation="Reference the canonical derivation rather than re-introducing."
                    ))

            # 4. Check for repeated identical introductory prose sentences (strip headings first)
            prose_content = re.sub(r"^#+.*$", "", content, flags=re.MULTILINE).strip()
            first_sentence = re.split(r"[.!?]", prose_content)[0].strip() if prose_content else ""
            if len(first_sentence.split()) > 10:
                first_norm = " ".join(re.sub(r"[^\w\s]", "", first_sentence.lower()).split())
                if first_norm in seen_intro_phrases:
                    issues.append(AdversarialIssue(
                        severity="ERROR",
                        category="REPETITION",
                        location=loc,
                        description=f"Identical opening sentence previously used in '{seen_intro_phrases[first_norm]}'.",
                        recommendation="Diversify pedagogical transitions and avoid repeating identical thesis sentences."
                    ))
                else:
                    seen_intro_phrases[first_norm] = loc

        crit = sum(1 for i in issues if i.severity == "CRITICAL")
        err = sum(1 for i in issues if i.severity == "ERROR")
        warn = sum(1 for i in issues if i.severity == "WARNING")
        info = sum(1 for i in issues if i.severity == "INFO")

        # Publication ready condition
        if allow_warnings:
            pub_ready = (crit == 0 and err == 0)
        else:
            pub_ready = (crit == 0 and err == 0 and warn == 0)

        passed = (crit == 0 and err == 0)

        return AdversarialReviewResult(
            passed=passed,
            issues=issues,
            critical_count=crit,
            error_count=err,
            warning_count=warn,
            info_count=info,
            publication_ready=pub_ready
        )
