import os
import re
import logging
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

logger = logging.getLogger(__name__)

class DOCXExporter:
    def set_cell_background(self, cell, hex_color: str):
        try:
            tcPr = cell._element.get_or_add_tcPr()
            shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
            tcPr.append(shd)
        except Exception as e:
            logger.error(f"Error shading cell background: {e}")

    def export_textbook(self, toc_data: dict, chapters_content: dict, images_dir: str, output_path: str, template_path: str = None) -> str:
        logger.info("Initializing Word document generation...")
        
        if template_path and os.path.exists(template_path):
            doc = Document(template_path)
        else:
            doc = Document()
            for section in doc.sections:
                section.top_margin = Inches(1)
                section.bottom_margin = Inches(1)
                section.left_margin = Inches(1)
                section.right_margin = Inches(1)

            style = doc.styles['Normal']
            style.font.name = 'Times New Roman'
            style.font.size = Pt(12)
            style.font.color.rgb = RGBColor(0, 0, 0)
            style.paragraph_format.line_spacing = 1.5
            style.paragraph_format.space_after = Pt(8)

        # COVER PAGE
        if doc.paragraphs:
            title_p = doc.paragraphs[0]
            title_p.text = ""
        else:
            title_p = doc.add_paragraph()
            
        title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        title_p.paragraph_format.space_before = Pt(120)
        title_run = title_p.add_run(toc_data.get("title", "Academic Textbook").upper())
        title_run.font.size = Pt(28)
        title_run.font.bold = True
        title_run.font.color.rgb = RGBColor(26, 54, 93)

        sub_p = doc.add_paragraph()
        sub_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        sub_p.paragraph_format.space_after = Pt(180)
        sub_run = sub_p.add_run("A Comprehensive Engineering and University Reference")
        sub_run.font.size = Pt(14)
        sub_run.font.italic = True
        sub_run.font.color.rgb = RGBColor(74, 85, 104)

        pub_p = doc.add_paragraph()
        pub_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        pub_run = pub_p.add_run("Published by\nAI Academic Press Ltd.\n\nFirst Edition")
        pub_run.font.size = Pt(12)
        pub_run.font.bold = True
        pub_run.font.color.rgb = RGBColor(113, 128, 150)
        
        doc.add_page_break()

        # COPYRIGHT PAGE
        copy_p = doc.add_paragraph()
        copy_p.paragraph_format.space_before = Pt(100)
        copy_p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        copy_run = copy_p.add_run(
            "Copyright © 2026 AI Academic Press Ltd.\n"
            "All rights reserved. No part of this publication may be reproduced, stored in a retrieval system, "
            "or transmitted in any form or by any means, electronic, mechanical, photocopying, recording, or otherwise "
            "without the prior written permission of the publisher.\n\n"
            "This book is generated in its entirety using advanced AI systems, representing publication-quality academic reference material.\n\n"
            "ISBN: 978-1-23456-789-0\n"
            "Printed in the United States of America."
        )
        copy_run.font.size = Pt(10)
        copy_run.font.color.rgb = RGBColor(113, 128, 150)
        
        doc.add_page_break()

        # ABOUT THE BOOK
        about_h = doc.add_heading("ABOUT THE BOOK", level=1)
        about_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
        about_p = doc.add_paragraph(toc_data.get("about_book", "This textbook covers engineering and scientific fundamentals."))
        about_p.paragraph_format.space_before = Pt(12)
        doc.add_page_break()

        # TABLE OF CONTENTS
        toc_h = doc.add_heading("TABLE OF CONTENTS", level=1)
        toc_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
        toc_p = doc.add_paragraph()
        toc_p.paragraph_format.space_before = Pt(12)
        
        for ch in toc_data.get("chapters", []):
            ch_num = ch.get("chapter_number", 1)
            ch_title = ch.get("title", "")
            toc_p.add_run(f"Chapter {ch_num}: {ch_title}\n").bold = True
            for sub in ch.get("subtopics", []):
                sub_title = sub.get("title", "")
                toc_p.add_run(f"    - {sub_title}\n")
            toc_p.add_run("\n")
            
        doc.add_page_break()

        # CHAPTERS CONTENT
        fig_count = 1
        for ch in toc_data.get("chapters", []):
            ch_num = ch.get("chapter_number", 1)
            ch_title = ch.get("title", "")
            ch_key = str(ch_num)
            
            doc.add_heading(f"Chapter {ch_num}: {ch_title}", level=1)
            content = chapters_content.get(ch_key, "")
            lines = content.split('\n')
            
            in_table = False
            table_lines = []
            
            i = 0
            while i < len(lines):
                line = lines[i]
                stripped = line.strip()
                
                if stripped.startswith('|') and stripped.endswith('|'):
                    in_table = True
                    table_lines.append(line)
                    i += 1
                    continue
                else:
                    if in_table and table_lines:
                        self._add_word_table(doc, table_lines)
                        table_lines = []
                        in_table = False
                
                if stripped.startswith('### '):
                    doc.add_heading(stripped[4:], level=3)
                elif stripped.startswith('## '):
                    doc.add_heading(stripped[3:], level=2)
                elif stripped.startswith('# '):
                    title_text = stripped[2:]
                    if not title_text.lower().startswith(f"chapter {ch_num}"):
                        doc.add_heading(title_text, level=1)
                elif stripped.startswith('[DIAGRAM_PLACEHOLDER:'):
                    match = re.match(r'\[DIAGRAM_PLACEHOLDER:\s*(.*?)\]', stripped)
                    if match:
                        diagram_topic = match.group(1)
                        img_filename = f"fig_{ch_num}_{fig_count}.png"
                        img_path = os.path.join(images_dir, img_filename)
                        
                        if os.path.exists(img_path):
                            img_p = doc.add_paragraph()
                            img_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                            img_p.paragraph_format.space_before = Pt(12)
                            img_p.paragraph_format.space_after = Pt(4)
                            img_run = img_p.add_run()
                            img_run.add_picture(img_path, width=Inches(5.5))
                            
                            try:
                                caption_p = doc.add_paragraph(style='Caption')
                            except Exception:
                                caption_p = doc.add_paragraph()
                                caption_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                                caption_run = caption_p.add_run()
                                caption_run.font.size = Pt(10)
                                caption_run.font.italic = True
                                caption_run.font.color.rgb = RGBColor(74, 85, 104)
                                
                            caption_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                            cap_run = caption_p.runs[0] if caption_p.runs else caption_p.add_run()
                            cap_run.text = f"Figure {ch_num}.{fig_count}: {diagram_topic}"
                            fig_count += 1
                        else:
                            fig_count += 1
                elif stripped.startswith('- ') or stripped.startswith('* '):
                    p = doc.add_paragraph(style='List Bullet')
                    self._add_inline_formatting(p, stripped[2:])
                elif re.match(r'^\d+\.\s', stripped):
                    p = doc.add_paragraph(style='List Number')
                    match_num = re.match(r'^(\d+)\.\s(.*)', stripped)
                    self._add_inline_formatting(p, match_num.group(2))
                elif not stripped:
                    pass
                else:
                    p = doc.add_paragraph()
                    self._add_inline_formatting(p, stripped)
                i += 1
            
            if in_table and table_lines:
                self._add_word_table(doc, table_lines)
            doc.add_page_break()

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        doc.save(output_path)
        logger.info(f"DOCX textbook compiled successfully at: {output_path}")

        pdf_path = output_path.replace(".docx", ".pdf")
        self._convert_to_pdf(output_path, pdf_path)
        return output_path

    def _add_inline_formatting(self, paragraph, text: str):
        tokens = re.split(r'(\*\*.*?\*\*|\*.*?\*)', text)
        for token in tokens:
            if token.startswith('**') and token.endswith('**'):
                run = paragraph.add_run(token[2:-2])
                run.bold = True
            elif token.startswith('*') and token.endswith('*'):
                run = paragraph.add_run(token[1:-1])
                run.italic = True
            else:
                paragraph.add_run(token)

    def _add_word_table(self, doc, table_lines: list):
        try:
            rows_data = []
            for line in table_lines:
                cells = [c.strip() for c in line.split('|')[1:-1]]
                if all(re.match(r'^-+$', c) for c in cells if c):
                    continue
                rows_data.append(cells)

            if not rows_data or len(rows_data) < 2:
                return

            num_rows = len(rows_data)
            num_cols = max(len(r) for r in rows_data)
            table = doc.add_table(rows=num_rows, cols=num_cols)
            table.style = 'Table Grid'
            
            for r_idx, row_cells in enumerate(rows_data):
                row = table.rows[r_idx]
                is_header = (r_idx == 0)
                for c_idx, cell_value in enumerate(row_cells):
                    if c_idx < len(row.cells):
                        cell = row.cells[c_idx]
                        p = cell.paragraphs[0]
                        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                        run = p.add_run(cell_value)
                        if is_header:
                            run.bold = True
                            run.font.color.rgb = RGBColor(255, 255, 255)
                            self.set_cell_background(cell, "2B6CB0")
                        else:
                            if r_idx % 2 == 0:
                                self.set_cell_background(cell, "F7FAFC")
        except Exception as e:
            logger.error(f"Failed to generate table: {e}")

    def _convert_to_pdf(self, docx_path: str, pdf_path: str):
        try:
            from docx2pdf import convert
            convert(docx_path, pdf_path)
        except Exception as e:
            logger.warning(f"PDF conversion skipped: {e}")
