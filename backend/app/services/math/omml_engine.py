"""
OMML (Office Math Markup Language) Engine for Word Equation Rendering.
Converts LaTeX and mathematical formulas into genuine Microsoft Word OMML XML elements.
Supports fractions, superscripts, subscripts, radicals, operators, Greek symbols,
accents, mathematical functions, and composite expressions.
"""

import re
import html
import logging
from typing import Optional, Tuple
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

logger = logging.getLogger(__name__)

# Complete LaTeX to Unicode / Symbol Mappings
GREEK_AND_SYMBOLS = {
    # Lowercase Greek
    r"\alpha": "α", r"\beta": "β", r"\gamma": "γ", r"\delta": "δ", r"\epsilon": "ε",
    r"\varepsilon": "ε", r"\zeta": "ζ", r"\eta": "η", r"\theta": "θ", r"\vartheta": "ϑ",
    r"\iota": "ι", r"\kappa": "κ", r"\lambda": "λ", r"\mu": "μ", r"\nu": "ν",
    r"\xi": "ξ", r"\pi": "π", r"\varpi": "ϖ", r"\rho": "ρ", r"\varrho": "ϱ",
    r"\sigma": "σ", r"\varsigma": "ς", r"\tau": "τ", r"\upsilon": "υ", r"\phi": "φ",
    r"\varphi": "ϕ", r"\chi": "χ", r"\psi": "ψ", r"\omega": "ω",
    # Uppercase Greek
    r"\Gamma": "Γ", r"\Delta": "Δ", r"\Theta": "Θ", r"\Lambda": "Λ", r"\Xi": "Ξ",
    r"\Pi": "Π", r"\Sigma": "Σ", r"\Upsilon": "Υ", r"\Phi": "Φ", r"\Psi": "Ψ", r"\Omega": "Ω",
    # Physics and Calculus Symbols
    r"\hbar": "ħ", r"\partial": "∂", r"\nabla": "∇", r"\infty": "∞",
    r"\int": "∫", r"\iint": "∬", r"\iiint": "∭", r"\oint": "∮",
    r"\sum": "∑", r"\prod": "∏",
    # Arithmetic & Comparison Operators
    r"\pm": "±", r"\mp": "∓", r"\times": "×", r"\div": "÷", r"\cdot": "·",
    r"\ast": "∗", r"\star": "⋆", r"\circ": "∘", r"\bullet": "∙",
    r"\leq": "≤", r"\geq": "≥", r"\neq": "≠", r"\approx": "≈",
    r"\equiv": "≡", r"\sim": "∼", r"\simeq": "≃", r"\propto": "∝",
    r"\ll": "≪", r"\gg": "≫",
    # Set and Logic
    r"\in": "∈", r"\notin": "∉", r"\subset": "⊂", r"\subseteq": "⊆",
    r"\supset": "⊃", r"\supseteq": "⊇", r"\cup": "∪", r"\cap": "∩",
    r"\forall": "∀", r"\exists": "∃", r"\neg": "¬", r"\emptyset": "∅",
    # Arrows
    r"\rightarrow": "→", r"\Rightarrow": "⇒", r"\leftarrow": "←", r"\Leftarrow": "⇐",
    r"\leftrightarrow": "↔", r"\Leftrightarrow": "⇔", r"\to": "→",
    # Brackets / Delimiters
    r"\{": "{", r"\}": "}", r"\|": "‖"
}

MATH_FUNCTIONS = [
    r"\arcsin", r"\arccos", r"\arctan",
    r"\sinh", r"\cosh", r"\tanh",
    r"\sin", r"\cos", r"\tan", r"\sec", r"\csc", r"\cot",
    r"\ln", r"\log", r"\exp", r"\lim", r"\det", r"\max", r"\min",
    r"\dim", r"\ker", r"\deg"
]

MATH_NS = 'xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"'

class OMMLEngine:
    """
    Transforms mathematical notation into native Word OMML XML elements.
    """

    @classmethod
    def sanitize_math_text(cls, latex: str) -> str:
        """Replaces LaTeX commands with standard mathematical symbols and clean notation."""
        clean = latex.strip()
        # Remove outer display/inline delimiters
        if clean.startswith("$$") and clean.endswith("$$") and len(clean) >= 4:
            clean = clean[2:-2].strip()
        elif clean.startswith("$") and clean.endswith("$") and len(clean) >= 2:
            clean = clean[1:-1].strip()

        # Remove \left and \right
        clean = clean.replace(r"\left", "").replace(r"\right", "")

        # Unpack text and font wrappers
        clean = re.sub(r"\\(?:text|mathrm|mathbf|mathit|boldsymbol|operatorname)\{([^}]+)\}", r"\1", clean)

        # Handle math accents
        clean = re.sub(r"\\hat\{([^}]+)\}", r"\1̂", clean)
        clean = re.sub(r"\\vec\{([^}]+)\}", r"\1⃗", clean)
        clean = re.sub(r"\\bar\{([^}]+)\}", r"\1̄", clean)
        clean = re.sub(r"\\dot\{([^}]+)\}", r"\1̇", clean)
        clean = re.sub(r"\\ddot\{([^}]+)\}", r"\1̈", clean)

        # Spacing commands
        clean = re.sub(r"\\(?:quad|qquad)", "  ", clean)
        clean = re.sub(r"\\[,;:]", " ", clean)

        # Function names without backslash
        for fn in MATH_FUNCTIONS:
            clean = re.sub(re.escape(fn) + r"(?![a-zA-Z])", fn[1:], clean)

        # Symbols and Greek letters
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
            return f'<m:oMathPara {MATH_NS}><m:oMath>{inner_xml}</m:oMath></m:oMathPara>'
        else:
            return f'<m:oMath {MATH_NS}>{inner_xml}</m:oMath>'

    @classmethod
    def _extract_braced_arg(cls, text: str, pos: int) -> Tuple[Optional[str], int]:
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
    def _extract_bracket_arg(cls, text: str, pos: int) -> Tuple[Optional[str], int]:
        """Extracts optional bracket argument [arg] starting at pos."""
        if pos >= len(text) or text[pos] != "[":
            return None, pos
        depth = 0
        start = pos + 1
        for idx in range(pos, len(text)):
            if text[idx] == "[":
                depth += 1
            elif text[idx] == "]":
                depth -= 1
                if depth == 0:
                    return text[start:idx], idx + 1
        return None, pos

    @classmethod
    def _extract_base(cls, text: str, pos: int) -> Tuple[Optional[str], int]:
        """Extracts base preceding ^ or _."""
        if pos < 0:
            return None, pos
        # If preceding character is '}' or ')'
        if text[pos] in ("}", ")"):
            open_char = "{" if text[pos] == "}" else "("
            close_char = text[pos]
            depth = 1
            start = pos - 1
            while start >= 0 and depth > 0:
                if text[start] == close_char:
                    depth += 1
                elif text[start] == open_char:
                    depth -= 1
                start -= 1
            return text[start + 1:pos + 1], start + 1
        return text[pos], pos

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

            # 2. Radical / Square Root: \sqrt[degree]{arg} or \sqrt{arg} or √{arg}
            is_sqrt = text[i:].startswith(r"\sqrt")
            is_rad_char = text[i] == "√"
            if is_sqrt or is_rad_char:
                pos = i + (5 if is_sqrt else 1)
                deg_content = None
                if pos < n and text[pos] == "[":
                    deg_content, pos = cls._extract_bracket_arg(text, pos)
                while pos < n and text[pos].isspace():
                    pos += 1
                rad_content, pos = cls._extract_braced_arg(text, pos)
                if rad_content is not None:
                    rad_xml = cls._parse_tokens_to_omml(rad_content)
                    if deg_content:
                        deg_xml = cls._parse_tokens_to_omml(deg_content)
                        xml_parts.append(
                            f'<m:rad><m:deg>{deg_xml}</m:deg><m:e>{rad_xml}</m:e></m:rad>'
                        )
                    else:
                        xml_parts.append(
                            f'<m:rad><m:radPr><m:degHide m:val="1"/></m:radPr><m:deg/><m:e>{rad_xml}</m:e></m:rad>'
                        )
                    i = pos
                    continue

            # 3. Superscript and Subscript combined: base_sub^sup or base^sup_sub
            subsup_pattern = (
                r"^([A-Za-z0-9α-ωΑ-Ωħ∂∇∫∑∏\(\)\[\]\{\}]|\{[^{}]+\}|\([^{}]+\))"
                r"(_([A-Za-z0-9\+\-\*\/]+|\{[^{}]+\})\^([A-Za-z0-9\+\-\*\/]+|\{[^{}]+\})|"
                r"\^([A-Za-z0-9\+\-\*\/]+|\{[^{}]+\})_([A-Za-z0-9\+\-\*\/]+|\{[^{}]+\}))"
            )
            m_subsup = re.match(subsup_pattern, text[i:])
            if m_subsup:
                base_raw = m_subsup.group(1).strip("{}")
                if m_subsup.group(3) is not None:
                    sub_raw = m_subsup.group(3).strip("{}")
                    sup_raw = m_subsup.group(4).strip("{}")
                else:
                    sup_raw = m_subsup.group(5).strip("{}")
                    sub_raw = m_subsup.group(6).strip("{}")

                base_xml = cls._parse_tokens_to_omml(base_raw)
                sub_xml = cls._parse_tokens_to_omml(sub_raw)
                sup_xml = cls._parse_tokens_to_omml(sup_raw)

                xml_parts.append(
                    f'<m:sSubSup><m:e>{base_xml}</m:e>'
                    f'<m:sub>{sub_xml}</m:sub>'
                    f'<m:sup>{sup_xml}</m:sup></m:sSubSup>'
                )
                i += m_subsup.end()
                continue

            # 4. Standalone Superscript: base^exp
            sup_pattern = r"^([A-Za-z0-9α-ωΑ-Ωħ∂∇∫∑∏\(\)\[\]]|\{[^{}]+\}|\([^{}]+\))\^([A-Za-z0-9\+\-\*\/]+|\{[^{}]+\})"
            m_sup = re.match(sup_pattern, text[i:])
            if m_sup:
                base_raw = m_sup.group(1).strip("{}")
                sup_raw = m_sup.group(2).strip("{}")
                base_xml = cls._parse_tokens_to_omml(base_raw)
                sup_xml = cls._parse_tokens_to_omml(sup_raw)
                xml_parts.append(f'<m:sSup><m:e>{base_xml}</m:e><m:sup>{sup_xml}</m:sup></m:sSup>')
                i += m_sup.end()
                continue

            # 5. Standalone Subscript: base_sub
            sub_pattern = r"^([A-Za-z0-9α-ωΑ-Ωħ∂∇∫∑∏\(\)\[\]]|\{[^{}]+\}|\([^{}]+\))_([A-Za-z0-9\+\-\*\/]+|\{[^{}]+\})"
            m_sub = re.match(sub_pattern, text[i:])
            if m_sub:
                base_raw = m_sub.group(1).strip("{}")
                sub_raw = m_sub.group(2).strip("{}")
                base_xml = cls._parse_tokens_to_omml(base_raw)
                sub_xml = cls._parse_tokens_to_omml(sub_raw)
                xml_parts.append(f'<m:sSub><m:e>{base_xml}</m:e><m:sub>{sub_xml}</m:sub></m:sSub>')
                i += m_sub.end()
                continue

            # 6. Standard text/character run
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
            logger.warning(f"Failed to insert OMML equation ({e}), falling back to Cambria Math text run")
            clean_text = cls.sanitize_math_text(latex_str)
            run = paragraph.add_run(clean_text)
            run.font.name = "Cambria Math"
            run.font.italic = True
            return False
