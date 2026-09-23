# AIWritter — Academic Document Engine & DOCX Typography

The Document Engine (`backend/app/services/document/docx_engine.py`) transforms multi-agent markdown text into publication-grade Microsoft Word (`.docx`) textbooks meeting rigorous academic press standards.

---

## 1. Typography & Formatting Standards

AIWritter strictly enforces traditional academic textbook typography:

| Document Element | Font Family | Size | Weight / Style | Line Spacing | Alignment | Space Before / After |
|------------------|-------------|------|----------------|--------------|-----------|----------------------|
| **Book Title** | Times New Roman | 28pt | Bold | 1.15 | Centered | 120pt / 18pt |
| **Book Subtitle** | Times New Roman | 16pt | Regular | 1.15 | Centered | 0pt / 24pt |
| **Author Byline** | Times New Roman | 13pt | Regular | 1.15 | Centered | 0pt / 200pt |
| **Heading 1 (Chapter)** | Times New Roman | 18pt | Bold | 1.15 | Left | 18pt / 8pt (Page Break Before) |
| **Heading 2 (Topic)** | Times New Roman | 14pt | Bold | 1.15 | Left | 14pt / 4pt |
| **Heading 3 (Subtopic)**| Times New Roman | 12pt | Bold | 1.15 | Left | 10pt / 2pt |
| **Body Paragraphs** | Times New Roman | 12pt | Regular | 1.50 | **Justified** | 0pt / 4pt |
| **Equation Displays** | Cambria Math | 11pt | Regular | Single | Centered | 6pt / 6pt |
| **Table Header** | Times New Roman | 10.5pt| Bold | 1.15 | Left / Center | 3pt / 3pt |
| **Table Data Cells** | Times New Roman | 10pt | Regular | 1.15 | Left | 2pt / 2pt |
| **Figure Captions** | Times New Roman | 10pt | Italic | 1.15 | Centered | 4pt / 12pt |

---

## 2. Page Setup & Document Layout

- **Page Margins:** Standard 1.0 inch (72 points / 1440 twips) on Top, Bottom, Left, and Right.
- **Section Breaks:** Standard Next-Page section breaks between major document divisions.
- **Headers & Footers:**
  - **Running Header:** Book title or active chapter name in 9pt Times New Roman, right-aligned with a subtle divider line.
  - **Running Footer:** Centered Arabic page numbers (`1, 2, 3...`) starting after the front matter.
- **Page Break Before Chapters:** Every Heading 1 automatically triggers a page break.

---

## 3. Native XML Table Rendering

AIWritter converts markdown tables into genuine Microsoft Word XML tables (`<w:tbl>`):
- **Header Formatting:**
  - Background fill: Dark Slate (`#1E293B`)
  - Font: Bold, 10.5pt, White (`#FFFFFF`)
  - Repeat header row across page splits: `<w:tblHeader/>`
- **Data Rows:**
  - Alternating zebra striping: Even rows have clean white background, odd rows have light shading (`#F8FAFC`).
  - Subtle borders: Light grey borders (`#E2E8F0`).
  - Cell padding: 6pt top/bottom, 8pt left/right.
  - Alignment: Automatic right-alignment for numerical columns, left-alignment for text.

---

## 4. Programmatic Document Quality Verification

After export, `DocumentValidationAgent` inspects the `.docx` package directly:
1. **Paragraph Inspection:** Verifies that body paragraphs use Times New Roman, 12pt font, 1.5 line spacing, and justified alignment.
2. **Empty Paragraph Filtering:** Ignores pure whitespace paragraphs while preserving OMML equation paragraphs.
3. **Table Styling:** Checks that tables feature styled headers, cell shading, and proper cell count.
4. **Image & Caption Integrity:** Ensures every embedded figure has an accompanying italic caption beginning with `Figure X.Y`.
5. **Quality Report Output:** Emits `document_quality_report.json` with itemized compliance scores and defect tallies.
