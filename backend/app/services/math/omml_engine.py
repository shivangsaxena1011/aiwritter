"""
OMML (Office Math Markup Language) Engine for Word Equation Rendering.
Converts LaTeX and mathematical formulas into genuine Microsoft Word OMML XML elements.
Supports fractions, superscripts, subscripts, radicals, operators, and Greek symbols.
"""

import re
import html
import logging
from typing import Optional
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

logger = logging.getLogger(__name__)

# Common LaTeX to Unicode / Symbol Mappings
GREEK_AND_SYMBOLS = {
    r"\alpha": "α", r"\beta": "β", r"\gamma": "γ", r"\delta": "δ", r"\epsilon": "ε",
    r"\zeta": "ζ", r"\eta": "η", r"\theta": "θ", r"\iota": "ι", r"\kappa": "κ",
    r"\lambda": "λ", r"\mu": "μ", r"\nu": "ν", r"\xi": "ξ", r"\pi": "π",
    r"\rho": "ρ", r"\sigma": "σ", r"\tau": "τ", r"\upsilon": "υ", r"\phi": "φ",
    r"\chi": "χ", r"\psi": "ψ", r"\omega": "ω",
    r"\Gamma": "Γ", r"\Delta": "Δ", r"\Theta": "Θ", r"\Lambda": "Λ", r"\Xi": "Ξ",
    r"\Pi": "Π", r"\Sigma": "Σ", r"\Phi": "Φ", r"\Psi": "Ψ", r"\Omega": "Ω",
    r"\hbar": "ħ", r"\partial": "∂", r"\nabla": "∇", r"\infty": "∞",
    r"\pm": "±", r"\times": "×", r"\div": "÷", r"\cdot": "·",
    r"\leq": "≤", r"\geq": "≥", r"\neq": "≠", r"\approx": "≈",
    r"\in": "∈", r"\notin": "∉", r"\subset": "⊂", r"\subseteq": "⊆",
    r"\cup": "∪", r"\cap": "∩", r"\int": "∫", r"\oint": "∮",
    r"\sum": "∑", r"\prod": "∏", r"\rightarrow": "→", r"\Rightarrow": "⇒",
    r"\leftrightarrow": "↔", r"\Leftrightarrow": "⇔", r"\to": "→"
}

MATH_NS = 'xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"'

class OMMLEngine:
    """
    Transforms mathematical notation into native Word OMML XML elements.
    """

    @classmethod
    def sanitize_math_text(cls, latex: str) -> str:
        """Replaces common LaTeX commands with equivalent mathematical symbols."""
        clean = latex.strip()
        # Remove outer $$ if present
        if clean.startswith("$$") and clean.endswith("$$"):
            clean = clean[2:-2].strip()
        elif clean.startswith("$") and clean.endswith("$"):
            clean = clean[1:-1].strip()

        # Remove \left and \right
        clean = clean.replace(r"\left", "").replace(r"\right", "")
        # Remove \text{...} or \mathrm{...} wrapper
        clean = re.sub(r"\\(?:text|mathrm|mathbf)\{([^}]+)\}", r"\1", clean)

        for cmd, sym in GREEK_AND_SYMBOLS.items():
            clean = re.sub(re.escape(cmd) + r"(?![a-zA-Z])", sym, clean)

        return clean

    @classmethod
    def latex_to_omml_xml(cls, latex_str: str, is_display: bool = True) -> str:
        """
        Converts a LaTeX expression into an OMML XML string.
        Handles fractions, radicals, superscripts, subscripts, and symbols.
        """
        clean_eq = cls.sanitize_math_text(latex_str)

        inner_xml = cls._parse_tokens_to_omml(clean_eq)

        if is_display:
            # Word display equation paragraph wrapper
            return f'<m:oMathPara {MATH_NS}><m:oMath>{inner_xml}</m:oMath></m:oMathPara>'
        else:
            # Inline math wrapper
            return f'<m:oMath {MATH_NS}>{inner_xml}</m:oMath>'

    @classmethod
    def _extract_braced_arg(cls, text: str, pos: int) -> tuple[Optional[str], int]:
        """
        Extracts balanced curly brace content starting at pos (where text[pos] == '{').
        Returns (content, next_pos) where next_pos is the index immediately following '}'.
        """
        if pos >= len(text) or text[pos] != "{":
            return None, pos
        depth = 0
        start = pos + 1
        for idx in range(pos, len(text)):
            if text[idx] == "{":
                depth += 1
            elif text[idx] == "}":
                depth -= 1
                if depth == 0:
                    return text[start:idx], idx + 1
        return None, pos

    @classmethod
    def _parse_tokens_to_omml(cls, text: str) -> str:
        """Recursively parses fractions, superscripts, subscripts, radicals, and runs into OMML XML."""
        xml_parts = []
        i = 0
        n = len(text)

        while i < n:
            # 1. Fraction: \frac{num}{den}
            if text[i:].startswith(r"\frac"):
                pos = i + 5
                while pos < n and text[pos].isspace():
                    pos += 1
                num_content, pos = cls._extract_braced_arg(text, pos)
                while pos < n and text[pos].isspace():
                    pos += 1
                den_content, pos = cls._extract_braced_arg(text, pos)
                if num_content is not None and den_content is not None:
                    num_xml = cls._parse_tokens_to_omml(num_content)
                    den_xml = cls._parse_tokens_to_omml(den_content)
                    xml_parts.append(
                        f'<m:f><m:num>{num_xml}</m:num><m:den>{den_xml}</m:den></m:f>'
                    )
                    i = pos
                    continue

            # 2. Square Root: \sqrt{arg} or √{arg}
            is_sqrt = text[i:].startswith(r"\sqrt")
            is_rad_char = text[i] == "√"
            if is_sqrt or is_rad_char:
                pos = i + (5 if is_sqrt else 1)
                while pos < n and text[pos].isspace():
                    pos += 1
                rad_content, pos = cls._extract_braced_arg(text, pos)
                if rad_content is not None:
                    rad_xml = cls._parse_tokens_to_omml(rad_content)
                    xml_parts.append(
                        f'<m:rad><m:radPr><m:degHide m:val="1"/></m:radPr><m:deg/><m:e>{rad_xml}</m:e></m:rad>'
                    )
                    i = pos
                    continue

            # 3. Superscript and Subscript combined: x_i^2 or x^2_i
            subsup_match = re.match(r"^([A-Za-z0-9α-ωΑ-Ωħ∂∇])(?:_([A-Za-z0-9\+\-]+|\{[^{}]+\}))?\^(?:([A-Za-z0-9\+\-]+|\{[^{}]+\}))", text[i:])
            if subsup_match:
                base = subsup_match.group(1)
                sub_val = (subsup_match.group(2) or "").strip("{}")
                sup_val = (subsup_match.group(3) or "").strip("{}")
                if sub_val and sup_val:
                    xml_parts.append(
                        f'<m:sSubSup><m:e><m:r><m:t>{html.escape(base)}</m:t></m:r></m:e>'
                        f'<m:sub><m:r><m:t>{html.escape(sub_val)}</m:t></m:r></m:sub>'
                        f'<m:sup><m:r><m:t>{html.escape(sup_val)}</m:t></m:r></m:sup></m:sSubSup>'
                    )
                    i += subsup_match.end()
                    continue

            # 4. Standalone Superscript: base^exp or {base}^exp
            sup_match = re.match(r"^([A-Za-z0-9α-ωΑ-Ωħ∂∇\)])\^([A-Za-z0-9\+\-]+|\{[^{}]+\})", text[i:])
            if sup_match:
                base = sup_match.group(1)
                sup_val = sup_match.group(2).strip("{}")
                xml_parts.append(
                    f'<m:sSup><m:e><m:r><m:t>{html.escape(base)}</m:t></m:r></m:e>'
                    f'<m:sup><m:r><m:t>{html.escape(sup_val)}</m:t></m:r></m:sup></m:sSup>'
                )
                i += sup_match.end()
                continue

            # 5. Standalone Subscript: base_sub
            sub_match = re.match(r"^([A-Za-z0-9α-ωΑ-Ωħ∂∇\)])_([A-Za-z0-9\+\-]+|\{[^{}]+\})", text[i:])
            if sub_match:
                base = sub_match.group(1)
                sub_val = sub_match.group(2).strip("{}")
                xml_parts.append(
                    f'<m:sSub><m:e><m:r><m:t>{html.escape(base)}</m:t></m:r></m:e>'
                    f'<m:sub><m:r><m:t>{html.escape(sub_val)}</m:t></m:r></m:sub></m:sSub>'
                )
                i += sub_match.end()
                continue

            # 6. Standard character / symbol run
            char = text[i]
            # Accumulate normal characters
            j = i + 1
            while j < n and text[j] not in ('\\', '^', '_', '{', '}'):
                j += 1
            chunk = text[i:j]
            xml_parts.append(f'<m:r><m:t>{html.escape(chunk)}</m:t></m:r>')
            i = j

        return "".join(xml_parts)

    @classmethod
    def insert_equation_into_paragraph(cls, paragraph, latex_str: str, is_display: bool = True) -> bool:
        """
        Inserts an OMML equation element directly into a python-docx Paragraph.
        Returns True on success, False if XML parsing failed.
        """
        try:
            omml_xml = cls.latex_to_omml_xml(latex_str, is_display=is_display)
            element = parse_xml(omml_xml)
            paragraph._p.append(element)
            return True
        except Exception as e:
            logger.warning(f"Failed to insert OMML equation ({e}), falling back to text run")
            clean_text = cls.sanitize_math_text(latex_str)
            run = paragraph.add_run(clean_text)
            run.font.name = "Cambria Math"
            run.font.italic = True
            return False
