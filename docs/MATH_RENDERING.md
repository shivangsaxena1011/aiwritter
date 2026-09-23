# AIWritter — Mathematical Rendering & OMML Engine

Mathematical rigor is a cornerstone of academic publishing. Rather than rendering blurry raster images or embedding raw LaTeX strings, AIWritter translates LaTeX equations directly into native **Microsoft Word OMML (Office Math Markup Language)** XML structures.

---

## 1. Why Native OMML Matters

Standard automated text generators output equations as:
1. Raw LaTeX strings (e.g. `$$\int f(x) dx$$`): Unreadable for non-technical readers and rejected by commercial publishers.
2. Raster images (PNG/SVG): Cause visual pixelation on zoom, misalign with text line heights, and break document reflow.

By compiling LaTeX directly into OMML (`<m:oMath>` and `<m:oMathPara>`), Word treats equations as editable, vectorized mathematical objects rendered via the Microsoft Cambria Math engine.

---

## 2. OMMLEngine Architecture (`backend/app/services/math/omml_engine.py`)

The `OMMLEngine` parses LaTeX strings using balanced-brace tokenization and builds compliant XML structures:

```
[LaTeX String: "\sqrt{\frac{2}{L}} \sin(kx)"]
                     │
                     ▼
             OMMLEngine.sanitize_math_text()
  - Replaces Greek commands (\alpha -> α, \hbar -> ħ)
  - Strips \left, \right, and \text{} wrappers
                     │
                     ▼
             OMMLEngine._parse_tokens_to_omml()
  - Extracts balanced braces via _extract_braced_arg()
  - Recursively maps constructs into OMML tags
                     │
                     ▼
[Word OMML XML: <m:oMath><m:rad>...</m:rad>...</m:oMath>]
                     │
                     ▼
            docx.oxml.parse_xml()
                     │
                     ▼
    Appended to python-docx Paragraph element
```

---

## 3. Supported OMML Constructs

| LaTeX Construct | Description | OMML XML Tag Structure |
|-----------------|-------------|------------------------|
| `\frac{A}{B}` | Built-in vertical fraction | `<m:f><m:num>A</m:num><m:den>B</m:den></m:f>` |
| `\sqrt{X}` or `\sqrt{A/B}` | Radical / Square Root | `<m:rad><m:radPr><m:degHide m:val="1"/></m:radPr><m:deg/><m:e>X</m:e></m:rad>` |
| `X^2` | Superscript | `<m:sSup><m:e>X</m:e><m:sup>2</m:sup></m:sSup>` |
| `X_i` | Subscript | `<m:sSub><m:e>X</m:e><m:sub>i</m:sub></m:sSub>` |
| `X_i^2` | Combined Sub/Superscript | `<m:sSubSup><m:e>X</m:e><m:sub>i</m:sub><m:sup>2</m:sup></m:sSubSup>` |
| Greek & Symbols | `\alpha, \beta, \hbar, \partial, \nabla, \infty` | Unicode symbols embedded in `<m:r><m:t>α</m:t></m:r>` |
| Display Equations | Centered standalone formula | `<m:oMathPara xmlns:m="..."><m:oMath>...</m:oMath></m:oMathPara>` |

---

## 4. Balanced Brace Extraction

To support nested formulas such as `\sqrt{\frac{2}{L}}` or `\frac{a + \sqrt{b}}{c + d}`, `OMMLEngine` utilizes `_extract_braced_arg(text, pos)`:

```python
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
```

---

## 5. MathValidator & Numerical Problem Structure

The `MathValidator` (`backend/app/services/math/math_validator.py`) enforces strict canonical structure for worked examples:

1. **Problem Statement:** Concise technical question.
2. **Given Data:** Explicit variables and physical units.
3. **Governing Formula:** Core theoretical equation in display format.
4. **Substitution:** Values substituted into the formula with units.
5. **Calculation Steps:** Step-by-step arithmetic operations.
6. **Final Answer:** Bolded numerical result.
7. **Unit:** Explicit physical SI or engineering unit.

### Arithmetic Sanity Checks:
`MathValidator.verify_arithmetic_sanity` extracts elementary numerical calculations (e.g. `2.5 / 14.2 = 0.1761`) and verifies arithmetic equality within a 5% margin of error, flagging discrepancies before publication.
