import os
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

def build_master_template(output_path: str):
    doc = Document()
    sections = doc.sections
    for section in sections:
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

    headings = {
        'Heading 1': {'size': 20, 'bold': True, 'italic': False, 'space_before': 24, 'space_after': 12, 'color': (26, 54, 93)},
        'Heading 2': {'size': 15, 'bold': True, 'italic': False, 'space_before': 16, 'space_after': 8, 'color': (43, 108, 176)},
        'Heading 3': {'size': 13, 'bold': True, 'italic': True, 'space_before': 12, 'space_after': 6, 'color': (45, 55, 72)}
    }

    for h_name, h_opts in headings.items():
        if h_name in doc.styles:
            h_style = doc.styles[h_name]
            h_font = h_style.font
            h_font.name = 'Times New Roman'
            h_font.size = Pt(h_opts['size'])
            h_font.bold = h_opts['bold']
            h_font.italic = h_opts['italic']
            h_font.color.rgb = RGBColor(*h_opts['color'])
            h_style.paragraph_format.space_before = Pt(h_opts['space_before'])
            h_style.paragraph_format.space_after = Pt(h_opts['space_after'])

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    doc.save(output_path)
    print(f"Master template created at: {output_path}")

if __name__ == "__main__":
    base = os.path.dirname(os.path.abspath(__file__))
    build_master_template(os.path.join(base, "templates", "master_book_template.docx"))
