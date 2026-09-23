"""
Tests for OMMLEngine and MathValidator:
OMML XML conversion, Greek symbols, fractions, superscripts, radicals,
and numerical structure verification.
"""

from backend.app.services.math.omml_engine import OMMLEngine
from backend.app.services.math.math_validator import MathValidator

def test_omml_greek_and_symbol_sanitization():
    latex = r"E = \hbar \omega + \frac{1}{2} k x^2 \quad \lambda = \frac{h}{p}"
    sanitized = OMMLEngine.sanitize_math_text(latex)
    assert "ħ" in sanitized
    assert "ω" in sanitized
    assert "λ" in sanitized

def test_omml_fraction_xml_generation():
    latex = r"\frac{n^2 \pi^2 \hbar^2}{2m L^2}"
    xml = OMMLEngine.latex_to_omml_xml(latex, is_display=True)
    assert "<m:oMathPara" in xml
    assert "<m:f>" in xml
    assert "<m:num>" in xml
    assert "<m:den>" in xml

def test_omml_radical_and_superscript_xml():
    latex = r"\sqrt{\frac{2}{L}} \sin(kx)"
    xml = OMMLEngine.latex_to_omml_xml(latex, is_display=False)
    assert "<m:oMath" in xml
    assert "<m:rad>" in xml

def test_math_validator_numerical_structure():
    canonical_text = """
**Problem Statement:** Calculate de Broglie wavelength for electron.
**Given Data:**
- m = 9.11e-31 kg
- v = 1e6 m/s
**Governing Formula:**
$$\\lambda = \\frac{h}{m v}$$
**Substitution:**
$$\\lambda = \\frac{6.626 \\times 10^{-34}}{(9.11 \\times 10^{-31}) \\times (10^6)}$$
**Calculation Steps:**
1. Compute denominator: 9.11e-25.
2. Invert: 7.27e-10 m.
**Final Answer:**
$$\\mathbf{0.727\\text{ nm}}$$
**Unit:**
Nanometers (nm)
"""
    result = MathValidator.validate_numerical_structure(canonical_text)
    assert result["is_valid_structure"] is True
    assert len(result["missing_fields"]) == 0

def test_math_validator_detects_missing_component():
    incomplete_text = """
**Problem Statement:** Compute energy.
**Formula:** E = mc^2
**Answer:** 9e16 J
"""
    result = MathValidator.validate_numerical_structure(incomplete_text)
    assert result["is_valid_structure"] is False
    assert "Given" in result["missing_fields"]
    assert "Substitution" in result["missing_fields"]
