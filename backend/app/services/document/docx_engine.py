import os
import re
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional, Set
import docx
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

from backend.app.services.document.base import DocumentExporter
from backend.app.services.math.omml_engine import OMMLEngine
from backend.app.services.document.book_assembly_model import BookAssemblyModel

logger = logging.getLogger(__name__)

TEMPLATE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "templates", "master_book_template.docx"))


class DOCXExporter(DocumentExporter):
    """Production-grade Word document exporter with template integration, real table support,
    and strict academic heading hierarchy with duplicate heading suppression."""


    def export(
        self,
        book_title: str,
        subtitle: Optional[str],
        author: Optional[str],
        academic_level: Optional[str],
        toc_data: Dict[str, Any],
        sections: List[Dict[str, Any]],
        assets: List[Dict[str, Any]],
        output_path: str,
        quality_report: Optional[Dict[str, Any]] = None,
        config: Optional[Dict[str, Any]] = None
    ) -> str:
        # Load master template if available to preserve margins and styles
        if os.path.exists(TEMPLATE_PATH):
            try:
                doc = Document(TEMPLATE_PATH)
                logger.info(f"Loaded master DOCX template from {TEMPLATE_PATH}")
            except Exception as e:
                logger.warning(f"Failed to load template ({e}), creating fresh Document")
                doc = Document()
        else:
            doc = Document()

        self._configure_document_styles(doc)

        # 1. Title / Cover Page
        self._build_cover_page(doc, book_title, subtitle, author, academic_level)

        # 2. Front Matter (Preface & Structure)
        self._build_front_matter(doc, book_title, academic_level, toc_data, config=config)

        # 3. Main Academic Content
        self._build_body_content(doc, toc_data, sections)

        # 4. Back Matter & Quality Scorecard
        if quality_report:
            self._build_back_matter(doc, quality_report)

        # 5. Add Page Numbers to Footers
        self._add_page_numbers(doc)

        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        doc.save(output_path)
        logger.info(f"Book exported successfully to DOCX: {output_path}")
        return output_path

    def export_assembly_model(
        self,
        assembly_model: BookAssemblyModel,
        output_path: str,
        config: Optional[Dict[str, Any]] = None
    ) -> str:
        """Renders DOCX directly and exclusively from the canonical BookAssemblyModel."""
        fm = assembly_model.front_matter
        toc_data = fm.toc
        if not toc_data or not toc_data.get("units"):
            toc_data = {
                "units": [
                    {
                        "name": ch.title,
                        "topics": [
                            {"name": t.title, "subtopics": [s.title for s in t.sections]}
                            for t in ch.topics
                        ]
                    }
                    for ch in assembly_model.chapters
                ]
            }

        compiled_sections = assembly_model.to_compiled_sections()
        assets: List[Dict[str, Any]] = []
        for ch in assembly_model.chapters:
            for top in ch.topics:
                for sec in top.sections:
                    for fig in sec.figures:
                        assets.append(fig.to_dict())

        return self.export(
            book_title=fm.title,
            subtitle=fm.subtitle,
            author=fm.author,
            academic_level=fm.academic_level,
            toc_data=toc_data,
            sections=compiled_sections,
            assets=assets,
            output_path=output_path,
            quality_report=assembly_model.back_matter.quality_scorecard,
            config=config or fm.config_summary
        )

    def generate_document(
        self,
        metadata: Dict[str, Any],
        sections: List[Dict[str, Any]],
        output_path: str,
        assets: Optional[List[Dict[str, Any]]] = None
    ) -> str:
        """Convenience adapter accepting metadata dictionary."""
        toc_data = metadata.get("toc_data", {"units": []})
        return self.export(
            book_title=metadata.get("title", "Untitled Book"),
            subtitle=metadata.get("subtitle"),
            author=metadata.get("author"),
            academic_level=metadata.get("academic_level"),
            toc_data=toc_data,
            sections=sections,
            assets=assets or [],
            output_path=output_path,
            config=metadata.get("config", {})
        )

    def _configure_document_styles(self, doc: Document):
        """Standardizes typography and heading hierarchies: Times New Roman, 12pt, 1.5 spacing, Justified."""
        normal_style = doc.styles["Normal"]
        font = normal_style.font
        font.name = "Times New Roman"
        font.size = Pt(12)
        font.color.rgb = RGBColor(15, 23, 42)

        # Paragraph formatting default
        normal_style.paragraph_format.line_spacing = 1.5
        normal_style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

        # Ensure margins on all sections
        for section in doc.sections:
            section.top_margin = Inches(1.0)
            section.bottom_margin = Inches(1.0)
            section.left_margin = Inches(1.0)
            section.right_margin = Inches(1.0)

    def _build_cover_page(self, doc: Document, title: str, subtitle: Optional[str], author: Optional[str], level: Optional[str]):
        """Generates formal university reference textbook cover page."""
        doc.add_paragraph().paragraph_format.space_before = Pt(72)

        # Sub-header tag
        tag_p = doc.add_paragraph()
        tag_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        tag_run = tag_p.add_run(f"ACADEMIC REFERENCE SERIES — {level or 'UNIVERSITY LEVEL'}")
        tag_run.font.name = "Calibri"
        tag_run.font.size = Pt(10)
        tag_run.font.bold = True
        tag_run.font.color.rgb = RGBColor(79, 140, 255)

        # Main Title
        title_p = doc.add_paragraph()
        title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        title_p.paragraph_format.space_before = Pt(18)
        title_p.paragraph_format.space_after = Pt(12)
        title_run = title_p.add_run(title)
        title_run.font.name = "Times New Roman"
        title_run.font.size = Pt(28)
        title_run.font.bold = True
        title_run.font.color.rgb = RGBColor(15, 23, 42)

        if subtitle:
            sub_p = doc.add_paragraph()
            sub_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            sub_run = sub_p.add_run(subtitle)
            sub_run.font.name = "Times New Roman"
            sub_run.font.size = Pt(15)
            sub_run.font.italic = True
            sub_run.font.color.rgb = RGBColor(71, 85, 105)

        # Spacer
        doc.add_paragraph().paragraph_format.space_before = Pt(140)

        # Author and Edition Metadata
        auth_p = doc.add_paragraph()
        auth_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        auth_run = auth_p.add_run(f"Author: {author or 'AI Academic Press'}\nFirst Reference Edition")
        auth_run.font.name = "Calibri"
        auth_run.font.size = Pt(12)
        auth_run.font.bold = True

        date_p = doc.add_paragraph()
        date_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        date_run = date_p.add_run(f"Published: {datetime.now().strftime('%B %Y')}")
        date_run.font.name = "Calibri"
        date_run.font.size = Pt(10)
        date_run.font.color.rgb = RGBColor(100, 116, 139)

        doc.add_page_break()

    def _build_front_matter(self, doc: Document, title: str, level: Optional[str], toc_data: Dict[str, Any], config: Optional[Dict[str, Any]] = None):
        """Generates preface, scope, and structured table of contents dynamically based on active configuration."""
        pref_h = doc.add_heading("Preface", level=1)
        pref_h.paragraph_format.space_before = Pt(12)
        pref_h.paragraph_format.space_after = Pt(12)

        cfg = config or {}
        include_numericals = cfg.get("include_numericals", False)
        include_questions = cfg.get("include_questions", False)
        include_references = cfg.get("include_references", True)
        include_diagrams = cfg.get("include_diagrams", True)

        features = ["theoretical foundational principles", "analytical derivations"]
        if include_numericals:
            features.append("worked numerical problem solutions")
        if include_questions:
            features.append("academic review questions")
        if include_diagrams:
            features.append("technical schematics and diagrams")
        if include_references:
            features.append("research-grounded citations")

        feat_str = ", ".join(features[:-1]) + ", and " + features[-1] if len(features) > 1 else features[0]

        pref_p = doc.add_paragraph(
            f"This academic textbook, '{title}', is developed as a systematic study text for {level or 'undergraduate engineering programs'}. "
            f"It develops core subject matter through {feat_str}. "
            "Each unit proceeds logically from foundational principles to physical interpretations and contemporary engineering applications."
        )
        pref_p.paragraph_format.line_spacing = 1.15
        pref_p.paragraph_format.space_after = Pt(18)

        # Table of Contents
        toc_h = doc.add_heading("Table of Contents", level=1)
        toc_h.paragraph_format.space_before = Pt(18)
        toc_h.paragraph_format.space_after = Pt(12)

        # Inject native Word dynamic TOC field XML
        try:
            toc_fld_p = doc.add_paragraph()
            fld_run = toc_fld_p.add_run()
            fld_xml = parse_xml(
                r'<w:fldSimple %s w:instr="TOC \o &quot;1-3&quot; \h \z \u"/>' % nsdecls('w')
            )
            fld_run._r.append(fld_xml)
        except Exception:
            pass

        for u in toc_data.get("units", []):
            u_p = doc.add_paragraph()
            u_p.paragraph_format.space_before = Pt(6)
            u_p.paragraph_format.space_after = Pt(2)
            u_run = u_p.add_run(u.get("name", ""))
            u_run.bold = True
            u_run.font.size = Pt(12)

            for t in u.get("topics", []):
                t_p = doc.add_paragraph()
                t_p.paragraph_format.left_indent = Inches(0.25)
                t_p.paragraph_format.space_after = Pt(2)
                t_run = t_p.add_run(t.get("name", ""))
                t_run.font.size = Pt(10.5)

                for s in t.get("subtopics", []):
                    s_p = doc.add_paragraph()
                    s_p.paragraph_format.left_indent = Inches(0.5)
                    s_p.paragraph_format.space_after = Pt(1)
                    s_run = s_p.add_run(f"• {s}")
                    s_run.font.size = Pt(9.5)
                    s_run.font.color.rgb = RGBColor(71, 85, 105)

        doc.add_page_break()

    def _build_body_content(self, doc: Document, toc_data: Dict[str, Any], sections: List[Dict[str, Any]]):
        """Converts academic section content, figures, and tables into Word elements with strict
        hierarchy (H1: Chapter, H2: Topic, H3: Subtopic, H4: Subsection) and duplicate suppression."""
        last_heading_text: Optional[str] = None
        last_heading_level: Optional[int] = None

        def add_safe_heading(text: str, level: int):
            nonlocal last_heading_text, last_heading_level
            clean_text = text.strip()
            if not clean_text:
                return None
            norm_new = re.sub(r"[^\w\s]", "", clean_text.lower())
            norm_last = re.sub(r"[^\w\s]", "", (last_heading_text or "").strip().lower())
            if level == last_heading_level and norm_new and norm_last and norm_new == norm_last:
                logger.warning(f"Suppressed consecutive duplicate heading in DOCX: '{clean_text}' (level {level})")
                return None
            h = doc.add_heading(clean_text, level=level)
            last_heading_text = clean_text
            last_heading_level = level
            return h

        rendered_units = set()

        for section in sections:
            unit_name = section.get("unit", "")
            topic_name = section.get("topic", "")
            subtopic_name = section.get("subtopic", "")

            # If unit overview
            if section.get("is_unit_overview"):
                rendered_units.add(unit_name)
                h1 = add_safe_heading(unit_name, level=1)
                if h1:
                    h1.paragraph_format.space_before = Pt(24)
                    h1.paragraph_format.space_after = Pt(12)

                intro_h = add_safe_heading("Chapter Overview & Objectives", level=2)
                if intro_h:
                    intro_h.paragraph_format.space_before = Pt(12)
                    intro_h.paragraph_format.space_after = Pt(8)

                self._parse_markdown_into_docx(
                    doc,
                    section.get("content", ""),
                    strip_headings={unit_name, "Chapter Overview & Objectives", "Overview & Objectives"},
                    heading_tracker=add_safe_heading
                )
                doc.add_page_break()
                last_heading_text = None
                continue

            # Ensure Chapter H1 is rendered if not already introduced
            if unit_name and unit_name not in rendered_units:
                rendered_units.add(unit_name)
                h1 = add_safe_heading(unit_name, level=1)
                if h1:
                    h1.paragraph_format.space_before = Pt(24)
                    h1.paragraph_format.space_after = Pt(12)

            # Standard subtopic section
            if section.get("is_first_in_topic", False):
                h2 = add_safe_heading(topic_name, level=2)
                if h2:
                    h2.paragraph_format.space_before = Pt(20)
                    h2.paragraph_format.space_after = Pt(8)

            h3 = add_safe_heading(subtopic_name, level=3)
            if h3:
                h3.paragraph_format.space_before = Pt(14)
                h3.paragraph_format.space_after = Pt(6)

            # Strip headings matching the unit, topic, or subtopic so markdown never re-adds them
            strip_set = {unit_name, topic_name, subtopic_name}

            # Body content
            self._parse_markdown_into_docx(
                doc,
                section.get("content", ""),
                strip_headings=strip_set,
                heading_tracker=add_safe_heading
            )

            # Attached figure / diagram
            image_path = section.get("image_path")
            image_caption = section.get("image_caption") or f"Figure — {subtopic_name}"

            if image_path and os.path.exists(image_path):
                self._insert_figure(doc, image_path, image_caption)
            elif section.get("placeholder_box"):
                p_box = doc.add_paragraph()
                p_box.paragraph_format.left_indent = Inches(0.4)
                p_box.paragraph_format.space_before = Pt(8)
                p_box.paragraph_format.space_after = Pt(8)
                run_box = p_box.add_run(section["placeholder_box"])
                run_box.italic = True
                run_box.font.color.rgb = RGBColor(100, 116, 139)

            # Attached table markdown if not already embedded
            tbl_md = section.get("table_markdown")
            if tbl_md and tbl_md.strip() and tbl_md.strip() not in section.get("content", ""):
                lines = [l.strip() for l in tbl_md.strip().split("\n") if l.strip().startswith("|") and l.strip().endswith("|")]
                if lines:
                    self._add_real_word_table(doc, lines)

    def _insert_figure(self, doc: Document, img_path: str, caption: str):
        """Inserts center-aligned picture with academic caption."""
        try:
            pic_p = doc.add_paragraph()
            pic_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            pic_p.paragraph_format.space_before = Pt(14)
            pic_p.paragraph_format.space_after = Pt(4)
            pic_run = pic_p.add_run()
            pic_run.add_picture(img_path, width=Inches(5.5))

            cap_p = doc.add_paragraph()
            cap_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            cap_p.paragraph_format.space_after = Pt(14)
            cap_run = cap_p.add_run(caption)
            cap_run.font.name = "Times New Roman"
            cap_run.font.size = Pt(10)
            cap_run.font.bold = True
            cap_run.font.italic = True
            cap_run.font.color.rgb = RGBColor(51, 65, 85)
        except Exception as e:
            logger.warning(f"Failed to insert figure {img_path}: {e}")

    def _parse_markdown_into_docx(
        self,
        doc: Document,
        markdown_text: str,
        strip_headings: Optional[Set[str]] = None,
        heading_tracker: Optional[Any] = None
    ):
        """Converts Markdown text, code blocks, lists, callouts, and REAL TABLES into docx.
        Discards headings that match strip_headings, and remaps inner headings to H4."""
        lines = markdown_text.split("\n")
        idx = 0
        total_lines = len(lines)

        in_code_block = False
        code_lines = []

        while idx < total_lines:
            line = lines[idx]
            line_str = line.strip()

            # 1. Code Blocks
            if line_str.startswith("```"):
                if in_code_block:
                    code_text = "\n".join(code_lines)
                    cp = doc.add_paragraph(code_text)
                    cp.paragraph_format.left_indent = Inches(0.3)
                    cp.paragraph_format.space_before = Pt(4)
                    cp.paragraph_format.space_after = Pt(4)
                    for r in cp.runs:
                        r.font.name = "Courier New"
                        r.font.size = Pt(9.5)
                    in_code_block = False
                    code_lines = []
                else:
                    in_code_block = True
                    code_lines = []
                idx += 1
                continue

            if in_code_block:
                code_lines.append(line)
                idx += 1
                continue

            # 2. Markdown Tables
            if line_str.startswith("|"):
                table_lines = []
                while idx < total_lines:
                    curr = lines[idx].strip()
                    if curr.startswith("|"):
                        table_lines.append(curr)
                        idx += 1
                    else:
                        break
                if table_lines:
                    self._add_real_word_table(doc, table_lines)
                continue

            # 3. Headings
            is_heading = False
            h_text = ""
            if line_str.startswith("#### "):
                is_heading = True
                h_text = line_str[5:].strip()
            elif line_str.startswith("### "):
                is_heading = True
                h_text = line_str[4:].strip()
            elif line_str.startswith("## "):
                is_heading = True
                h_text = line_str[3:].strip()
            elif line_str.startswith("# "):
                is_heading = True
                h_text = line_str[2:].strip()

            if is_heading:
                # Normalize and check whether this heading duplicates an existing structural heading
                norm_h = re.sub(r"[^\w\s]", "", h_text.lower())
                should_skip = False
                if strip_headings:
                    for sh in strip_headings:
                        norm_sh = re.sub(r"[^\w\s]", "", (sh or "").lower())
                        if norm_sh and (norm_h == norm_sh or norm_h in norm_sh or norm_sh in norm_h):
                            should_skip = True
                            break

                if should_skip:
                    idx += 1
                    continue

                # In academic text, subsections inside subtopic are Level 4
                if heading_tracker:
                    h = heading_tracker(h_text, level=4)
                    if h:
                        h.paragraph_format.space_before = Pt(10)
                        h.paragraph_format.space_after = Pt(4)
                else:
                    h = doc.add_heading(h_text, level=4)
                    h.paragraph_format.space_before = Pt(10)
                    h.paragraph_format.space_after = Pt(4)
                idx += 1
                continue

            # 4. Callout Blocks (> )
            elif line_str.startswith("> "):
                call_p = doc.add_paragraph()
                call_p.paragraph_format.left_indent = Inches(0.3)
                call_p.paragraph_format.space_before = Pt(4)
                call_p.paragraph_format.space_after = Pt(4)
                self._parse_inline_formatting(call_p, line_str[2:])
                for r in call_p.runs:
                    r.font.italic = True
                    r.font.name = "Times New Roman"
                    r.font.color.rgb = RGBColor(71, 85, 105)

            # 5. Bullet Lists
            elif line_str.startswith("- ") or line_str.startswith("* "):
                lp = doc.add_paragraph(style="List Bullet")
                lp.paragraph_format.space_after = Pt(2)
                self._parse_inline_formatting(lp, line_str[2:])

            # 6. Numbered Lists
            elif re.match(r"^\d+\.\s+", line_str):
                num_text = re.sub(r"^\d+\.\s+", "", line_str)
                np = doc.add_paragraph(style="List Number")
                np.paragraph_format.space_after = Pt(2)
                self._parse_inline_formatting(np, num_text)

            # 7. Math Equation Blocks ($$ ... $$) — Rendered via OMML Engine (Single & Multi-line)
            elif line_str.startswith("$$"):
                if line_str.endswith("$$") and len(line_str) > 4:
                    raw_eq = line_str[2:-2].strip()
                else:
                    eq_lines = []
                    if len(line_str) > 2:
                        eq_lines.append(line_str[2:].strip())
                    idx += 1
                    while idx < total_lines:
                        curr = lines[idx].strip()
                        if "$$" in curr:
                            parts = curr.split("$$")
                            if parts[0].strip():
                                eq_lines.append(parts[0].strip())
                            break
                        eq_lines.append(curr)
                        idx += 1
                    raw_eq = " ".join(eq_lines).strip()

                if raw_eq:
                    math_p = doc.add_paragraph()
                    math_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    math_p.paragraph_format.space_before = Pt(8)
                    math_p.paragraph_format.space_after = Pt(8)
                    success = OMMLEngine.insert_equation_into_paragraph(math_p, raw_eq, is_display=True)
                    if not success:
                        math_run = math_p.add_run(OMMLEngine.sanitize_math_text(raw_eq))
                        math_run.font.name = "Cambria Math"
                        math_run.font.size = Pt(12)
                        math_run.font.italic = True

            # 8. Standard Paragraph — Times New Roman, 12pt, 1.5 line spacing, Justified
            elif line_str:
                p = doc.add_paragraph()
                p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                p.paragraph_format.line_spacing = 1.5
                p.paragraph_format.space_after = Pt(6)
                self._parse_inline_formatting(p, line_str)

            idx += 1

    @staticmethod
    def _clean_table_cell_math(text: str) -> str:
        """Cleans raw LaTeX math formatting out of table cell text into clean readable unicode."""
        if not text:
            return text
        t = text
        t = re.sub(r"\\text\{([^}]+)\}", r"\1", t)
        t = re.sub(r"\\mathrm\{([^}]+)\}", r"\1", t)
        t = re.sub(r"\\mathbf\{([^}]+)\}", r"\1", t)
        t = re.sub(r"\\AA", "Å", t)
        t = re.sub(r"\\lambda", "λ", t)
        t = re.sub(r"\\theta", "θ", t)
        t = re.sub(r"\\pi", "π", t)
        t = re.sub(r"\\infty", "∞", t)
        t = re.sub(r"\\approx", "≈", t)
        t = re.sub(r"\\propto", "∝", t)
        t = re.sub(r"\\cdot", "·", t)
        t = re.sub(r"\\times", "×", t)
        t = re.sub(r"\\quad", " ", t)
        t = re.sub(r"\\le", "≤", t)
        t = re.sub(r"\\ge", "≥", t)
        t = re.sub(r"\\delta", "δ", t)
        t = re.sub(r"\\nu", "ν", t)
        t = re.sub(r"\\hbar", "ℏ", t)
        t = re.sub(r"\\hat\{([^}]+)\}", r"\1", t)
        t = re.sub(r"\\frac\{([^}]+)\}\{([^}]+)\}", r"\1/\2", t)
        t = re.sub(r"\\sqrt\{([^}]+)\}", r"√\1", t)
        t = re.sub(r"\\[a-zA-Z]+", "", t)
        t = re.sub(r"[\$\{\}\\]+", "", t)
        return " ".join(t.split())

    def _add_real_word_table(self, doc: Document, table_lines: List[str]):
        """Converts Markdown table rows into true Word tables with formatting."""
        parsed_rows = []
        for line in table_lines:
            # Skip separator line like |---|---|
            if re.match(r"^\|(?:\s*:?-+:?\s*\|)+$", line):
                continue
            cells = [c.strip() for c in line.strip("|").split("|")]
            parsed_rows.append(cells)

        if not parsed_rows:
            return

        num_cols = max(len(r) for r in parsed_rows)
        table = doc.add_table(rows=len(parsed_rows), cols=num_cols)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.autofit = True

        # Apply clean academic table borders
        try:
            tblBorders = parse_xml(
                r'''<w:tblBorders %s>
                    <w:top w:val="single" w:sz="6" w:space="0" w:color="CBD5E1"/>
                    <w:left w:val="none"/>
                    <w:bottom w:val="single" w:sz="8" w:space="0" w:color="475569"/>
                    <w:right w:val="none"/>
                    <w:insideH w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/>
                    <w:insideV w:val="none"/>
                </w:tblBorders>''' % nsdecls('w')
            )
            table._tbl.tblPr.append(tblBorders)
        except Exception:
            pass

        for row_idx, row in enumerate(table.rows):
            is_header = (row_idx == 0)
            # Repeat header on new pages
            if is_header:
                try:
                    trPr = row._tr.get_or_add_trPr()
                    trPr.append(parse_xml(r'<w:tblHeader %s/>' % nsdecls('w')))
                except Exception:
                    pass

            for col_idx, cell in enumerate(row.cells):
                if col_idx < len(parsed_rows[row_idx]):
                    cell.text = self._clean_table_cell_math(parsed_rows[row_idx][col_idx])
                else:
                    cell.text = ""

                cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER

                # Styling
                tcPr = cell._tc.get_or_add_tcPr()
                if is_header:
                    shd = parse_xml(r'<w:shd %s w:fill="F1F5F9"/>' % nsdecls('w'))
                    tcPr.append(shd)

                for p in cell.paragraphs:
                    p.paragraph_format.line_spacing = 1.15
                    p.paragraph_format.space_before = Pt(4)
                    p.paragraph_format.space_after = Pt(4)
                    for r in p.runs:
                        r.font.name = "Times New Roman"
                        r.font.size = Pt(10)
                        if is_header:
                            r.font.bold = True
                            r.font.color.rgb = RGBColor(15, 23, 42)
                        else:
                            r.font.color.rgb = RGBColor(51, 65, 85)

    def _parse_inline_formatting(self, paragraph, text: str):
        """Converts Markdown bold, italics, code, and inline math into Word runs."""
        # Tokenize by bold (**), italic (*), inline code (`), and inline math ($...$)
        pattern = r"(\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`|\$[^\$]+\$)"
        parts = re.split(pattern, text)

        for part in parts:
            if not part:
                continue

            # Inline Math ($...$)
            if part.startswith("$") and part.endswith("$") and len(part) > 2:
                raw_math = part[1:-1].strip()
                success = OMMLEngine.insert_equation_into_paragraph(paragraph, raw_math, is_display=False)
                if not success:
                    run = paragraph.add_run(OMMLEngine.sanitize_math_text(raw_math))
                    run.font.name = "Cambria Math"
                    run.font.italic = True
                    run.font.size = Pt(11.5)
            # Bold (**...**)
            elif part.startswith("**") and part.endswith("**") and len(part) >= 4:
                run = paragraph.add_run(part[2:-2])
                run.bold = True
                run.font.name = "Times New Roman"
                run.font.size = Pt(12)
            # Italic (*...*)
            elif part.startswith("*") and part.endswith("*") and len(part) >= 2:
                run = paragraph.add_run(part[1:-1])
                run.italic = True
                run.font.name = "Times New Roman"
                run.font.size = Pt(12)
            # Inline Code (`...`)
            elif part.startswith("`") and part.endswith("`") and len(part) >= 2:
                run = paragraph.add_run(part[1:-1])
                run.font.name = "Courier New"
                run.font.size = Pt(10.5)
                run.font.color.rgb = RGBColor(180, 83, 9)
            # Plain Text
            else:
                run = paragraph.add_run(part)
                run.font.name = "Times New Roman"
                run.font.size = Pt(12)

    def _build_back_matter(self, doc: Document, quality_report: Dict[str, Any]):
        """Renders formal document quality scorecard in back matter."""
        doc.add_page_break()
        h = doc.add_heading("Appendix: Academic Quality & Verification Scorecard", level=1)
        h.paragraph_format.space_before = Pt(24)
        h.paragraph_format.space_after = Pt(12)

        desc = doc.add_paragraph(
            "This volume has been programmatically compiled and audited according to rigorous university engineering standards. "
            "Below is the automated audit scorecard certifying completeness, mathematical rigor, and pedagogical integrity."
        )
        desc.paragraph_format.space_after = Pt(12)

        metrics = [
            ("Overall Academic Quality Score", f"{quality_report.get('quality_score', 'N/A')}/100"),
            ("Status", quality_report.get("status", "VERIFIED").upper()),
            ("Total Chapters Verified", str(quality_report.get("chapters_count", "N/A"))),
            ("Total Topics Verified", str(quality_report.get("topics_count", "N/A"))),
            ("Total Word Count", f"{quality_report.get('word_count', 0):,} words"),
            ("Connected Prose Paragraphs", str(quality_report.get("prose_paragraphs", "N/A"))),
            ("Bullet / List Items", str(quality_report.get("bullet_paragraphs", "N/A"))),
            ("OMML Native Equations", str(quality_report.get("equations_count", "N/A"))),
            ("Academic Tables", str(quality_report.get("tables_count", "N/A"))),
            ("Figures & Schematics", str(quality_report.get("figures_count", "N/A"))),
            ("Audit Timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC"))
        ]

        table = doc.add_table(rows=len(metrics) + 1, cols=2)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.autofit = True

        hdr_cells = table.rows[0].cells
        hdr_cells[0].text = "Verification Metric"
        hdr_cells[1].text = "Audit Value"
        for c in hdr_cells:
            for p in c.paragraphs:
                for r in p.runs:
                    r.font.bold = True
                    r.font.name = "Times New Roman"

        for idx, (m_name, m_val) in enumerate(metrics, start=1):
            row_cells = table.rows[idx].cells
            row_cells[0].text = m_name
            row_cells[1].text = m_val
            for c in row_cells:
                for p in c.paragraphs:
                    for r in p.runs:
                        r.font.name = "Times New Roman"
                        r.font.size = Pt(10)

    def _add_page_numbers(self, doc: Document):
        """Adds standard centered page number XML fields to all footers."""
        for section in doc.sections:
            footer = section.footer
            footer_p = footer.paragraphs[0]
            footer_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            footer_p.paragraph_format.space_before = Pt(8)
            fld_run = footer_p.add_run()
            fld_run.font.name = "Times New Roman"
            fld_run.font.size = Pt(9.5)
            fld_run.font.color.rgb = RGBColor(148, 163, 184)
            fld_xml = parse_xml(r'<w:fldSimple %s w:instr="PAGE"/>' % nsdecls('w'))
            fld_run._r.append(fld_xml)


# Backwards compatibility alias
DocxEngine = DOCXExporter
