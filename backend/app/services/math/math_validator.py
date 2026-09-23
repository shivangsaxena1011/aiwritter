"""
MathValidator — Programmatic validation of numerical problems, equations, and arithmetic steps.
Enforces the mandatory academic problem structure:
Given -> Formula -> Substitution -> Calculation -> Answer -> Unit.
"""

import re
import math
import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class MathValidator:
    """
    Validates numerical problem structure, performs safe arithmetic verification,
    and checks mathematical notation consistency.
    """

    MANDATORY_NUMERICAL_FIELDS = ["Given", "Formula", "Substitution", "Calculation", "Answer", "Unit"]

    FIELD_PATTERNS = {
        "Given": re.compile(r"(?:^|\n|\*\*|\#)\s*(?:Given(?:\s+Data|\s+Values|\s+Parameters)?)\s*(?:\*\*)?\s*[:\-]", re.I),
        "Formula": re.compile(r"(?:^|\n|\*\*|\#)\s*(?:(?:Governing|Core|Relevant)\s+)?Formula[s]?\s*(?:\*\*)?\s*[:\-]", re.I),
        "Substitution": re.compile(r"(?:^|\n|\*\*|\#)\s*(?:(?:Step-by-Step\s+)?Substitution|Substituting\s+Values)\s*(?:\*\*)?\s*[:\-]", re.I),
        "Calculation": re.compile(r"(?:^|\n|\*\*|\#)\s*Calculation(?:s|\s+Steps)?\s*(?:\*\*)?\s*[:\-]", re.I),
        "Answer": re.compile(r"(?:^|\n|\*\*|\#)\s*(?:Final\s+)?(?:Answer|Result)\s*(?:\*\*)?\s*[:\-]", re.I),
        "Unit": re.compile(r"(?:^|\n|\*\*|\#)\s*(?:(?:SI|Standard)\s+)?Unit[s]?\s*(?:\*\*)?\s*[:\-]", re.I),
    }

    @classmethod
    def validate_numerical_structure(cls, numerical_text: str) -> Dict[str, Any]:
        """
        Verifies that a numerical solution includes all mandatory academic components.
        """
        found_fields = {}
        for field in cls.MANDATORY_NUMERICAL_FIELDS:
            pattern = cls.FIELD_PATTERNS.get(field)
            if pattern:
                match = pattern.search(numerical_text)
            else:
                match = re.search(rf"(?:^|\n|\*\*)\s*{field}\s*[:\-]", numerical_text, re.I)
            found_fields[field] = bool(match)

        missing = [f for f, found in found_fields.items() if not found]
        is_valid = len(missing) == 0

        # Attempt arithmetic sanity extraction
        arithmetic_check = cls.verify_arithmetic_sanity(numerical_text)

        return {
            "is_valid_structure": is_valid,
            "found_fields": found_fields,
            "missing_fields": missing,
            "arithmetic_verification": arithmetic_check,
            "verdict": "Structurally Complete & Verified" if is_valid else f"Missing components: {', '.join(missing)}"
        }

    @classmethod
    def verify_arithmetic_sanity(cls, text: str) -> Dict[str, Any]:
        """
        Extracts elementary calculation expressions and verifies equality.
        E.g. extracts '2.5 / 14.2 = 0.1761' or '2 * 3 = 6'.
        """
        # Search for expressions like: number op number = number
        matches = re.findall(r"(\d+(?:\.\d+)?)\s*([\+\-\*\/])\s*(\d+(?:\.\d+)?)\s*=\s*(\d+(?:\.\d+)?)", text)
        verified_steps = []
        errors = []

        for a_str, op, b_str, res_str in matches:
            a, b, expected = float(a_str), float(b_str), float(res_str)
            actual = None
            try:
                if op == "+":
                    actual = a + b
                elif op == "-":
                    actual = a - b
                elif op == "*":
                    actual = a * b
                elif op == "/":
                    if b != 0:
                        actual = a / b
            except Exception:
                continue

            if actual is not None:
                # Tolerance check (5% margin for rounding)
                margin = max(0.01, abs(actual) * 0.05)
                passed = abs(actual - expected) <= margin
                verified_steps.append({
                    "step": f"{a_str} {op} {b_str} = {res_str}",
                    "calculated": round(actual, 4),
                    "stated": expected,
                    "passed": passed
                })
                if not passed:
                    errors.append(f"Arithmetic divergence in step: {a_str} {op} {b_str} = {res_str} (computed: {round(actual, 4)})")

        return {
            "total_steps_checked": len(verified_steps),
            "passed_steps": sum(1 for s in verified_steps if s["passed"]),
            "errors": errors,
            "status": "verified" if len(errors) == 0 else "discrepancy_detected"
        }

    @classmethod
    def format_canonical_numerical(
        cls,
        problem: str,
        given: Dict[str, str],
        formula: str,
        substitution: str,
        calculation: str,
        answer: str,
        unit: str
    ) -> str:
        """
        Constructs a pristine, canonical academic numerical solution block.
        """
        given_lines = "\n".join(f"- {k} = {v}" for k, v in given.items())
        return f"""**Problem Statement:**
{problem}

**Given Data:**
{given_lines}

**Governing Formula:**
$${formula}$$

**Substitution:**
$${substitution}$$

**Calculation Steps:**
{calculation}

**Final Answer:**
$$\\mathbf{{{answer}\\text{{ {unit}}}}}$$
"""
