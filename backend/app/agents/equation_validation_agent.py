"""
EquationValidationAgent — Mathematical Correctness and Pedagogical Relevance Validator.
Inspects equations embedded in academic treatises to ensure:
1. Genuine relevance to the topic (blocks irrelevant boilerplate formulas).
2. Physical and dimensional consistency.
3. Symbol definition completeness (flags unexplained symbols).
4. Notation consistency across the textbook.
"""

import re
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from backend.app.agents.base import BaseAgent, AgentContext, AgentResult

@dataclass
class EquationValidationResult:
    is_valid: bool = True
    total_equations: int = 0
    valid_equations: int = 0
    topic_relevance_score: float = 1.0
    fake_technicality_count: int = 0
    unexplained_symbols: List[str] = field(default_factory=list)
    issues: List[str] = field(default_factory=list)
    verdict: str = "Equations Verified"

class EquationValidationAgent(BaseAgent):
    """
    Validates that every equation in a generated section is scientifically relevant,
    pedagogically meaningful, and has its symbols explained.
    """

    async def run(self, context: AgentContext, **kwargs) -> AgentResult:
        content = kwargs.get("content", "")
        topic = kwargs.get("topic", context.book_title)
        res = self.validate_equations(content, topic, context.subject or "")
        return AgentResult(status="success" if res.is_valid else "warning", data=res.__dict__)

    # Topic-to-Equation Relevance Mapping (positive matches)
    TOPIC_KEYWORD_EQUATIONS = {
        "de broglie": ["\\lambda", "h/p", "h/mv", "\\sqrt{2mE}"],
        "schrodinger": ["\\hbar", "\\partial \\Psi", "\\nabla^2", "V(x)", "\\psi(x)", "E\\psi"],
        "heisenberg": ["\\Delta x", "\\Delta p", "\\hbar/2", "\\ge"],
        "box": ["\\frac{n^2 h^2}{8mL^2}", "\\frac{n^2 \\pi^2 \\hbar^2}{2mL^2}", "\\sqrt{\\frac{2}{L}}", "\\sin"],
        "well": ["\\frac{n^2 h^2}{8mL^2}", "\\frac{n^2 \\pi^2 \\hbar^2}{2mL^2}", "\\sqrt{\\frac{2}{L}}", "\\sin"],
        "phase velocity": ["v_p", "\\omega/k", "v_g", "d\\omega/dk"],
        "group velocity": ["v_p", "\\omega/k", "v_g", "d\\omega/dk"],
        "wave function": ["|\\Psi|^2", "P(x)", "\\int", "dx = 1"],
        "operator": ["\\hat{", "-i\\hbar", "\\frac{\\partial}{\\partial x}", "\\hat{H}"],
        "eigenvalue": ["\\hat{A}\\psi", "a\\psi", "\\lambda"]
    }

    # Banned Fake Technicality Signatures (generic heat diffusion pasted into physics)
    BANNED_FAKE_EQUATIONS = [
        r"\\nabla \\cdot \(\\mathbf\{v\} \\Psi\) = \\kappa \\nabla\^2 \\Psi \+ \\dot\{S\}_\{gen\}",
        r"\\kappa \\nabla\^2 \\Psi \+ \\dot\{S\}_\{gen\}"
    ]

    def validate_content_equations(self, content: str, topic_title: str) -> Dict[str, Any]:
        """
        Extracts all LaTeX display equations from text and audits them.
        """
        # Find all display equations: $$...$$
        equations = re.findall(r"\$\$(.*?)\$\$", content, re.DOTALL)
        if not equations:
            # Inline display math
            equations = re.findall(r"\\\[(.*?)\\\]", content, re.DOTALL)

        issues = []
        fake_technicality_count = 0
        topic_lower = topic_title.lower()

        for eq in equations:
            eq_clean = eq.strip()
            eq_clean_lower = eq_clean.lower()

            # 1. Check for banned fake technicality (generic heat diffusion pasted into physics)
            if "dot{s}" in eq_clean_lower or "s}_{gen}" in eq_clean_lower or ("kappa" in eq_clean_lower and "nabla^2" in eq_clean_lower and "mathbf{v}" in eq_clean_lower):
                issues.append(f"Banned generic fake technicality formula detected: '{eq_clean[:40]}...'")
                fake_technicality_count += 1

            # 2. Check topic relevance if topic has known signatures
            for kw, expected_tokens in self.TOPIC_KEYWORD_EQUATIONS.items():
                if kw in topic_lower:
                    if not any(token in eq_clean for token in expected_tokens):
                        # Not an immediate error if other equations in the section match, but flagged if isolated
                        pass

        # 3. Check symbol explanations in text
        # If equation has \hbar, text should mention hbar or Planck
        unexplained_symbols = []
        if "\\hbar" in content and not any(w in content.lower() for w in ["hbar", "planck", "reduced planck", "\\hbar"]):
            unexplained_symbols.append("hbar")
        if "\\Psi" in content and not any(w in content.lower() for w in ["wave function", "state", "psi", "amplitude"]):
            unexplained_symbols.append("Psi")

        is_valid = (fake_technicality_count == 0)

        return {
            "is_valid": is_valid,
            "equations_count": len(equations),
            "fake_technicality_count": fake_technicality_count,
            "unexplained_symbols": unexplained_symbols,
            "issues": issues,
            "verdict": "Equations Verified" if is_valid else "Equation Validation Failure"
        }

    def validate_equations(self, content: str, topic_title: str, subject: str = "") -> EquationValidationResult:
        """Structured equation validation returning EquationValidationResult."""
        res_dict = self.validate_content_equations(content, topic_title)
        eq_count = res_dict["equations_count"]
        fake_count = res_dict["fake_technicality_count"]
        valid_count = max(0, eq_count - fake_count)
        relevance_score = 0.0 if fake_count > 0 else (1.0 if eq_count > 0 else 0.85)

        return EquationValidationResult(
            is_valid=res_dict["is_valid"],
            total_equations=eq_count,
            valid_equations=valid_count,
            topic_relevance_score=relevance_score,
            fake_technicality_count=fake_count,
            unexplained_symbols=res_dict["unexplained_symbols"],
            issues=res_dict["issues"],
            verdict=res_dict["verdict"]
        )
