import os
import logging
from typing import Dict, Any, List, Optional
from backend.app.services.document.base import DocumentExporter
from backend.app.services.document.docx_engine import DOCXExporter

logger = logging.getLogger(__name__)

class PDFExporter(DocumentExporter):
    """PDF Document Exporter with clean conversion adapter and informative fallback."""

    def __init__(self):
        self.docx_exporter = DOCXExporter()

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
        quality_report: Optional[Dict[str, Any]] = None
    ) -> str:
        # First compile into temporary DOCX
        docx_temp_path = output_path.replace(".pdf", ".docx")
        self.docx_exporter.export(
            book_title=book_title,
            subtitle=subtitle,
            author=author,
            academic_level=academic_level,
            toc_data=toc_data,
            sections=sections,
            assets=assets,
            output_path=docx_temp_path,
            quality_report=quality_report
        )

        try:
            from docx2pdf import convert
            convert(docx_temp_path, output_path)
            logger.info(f"Successfully converted DOCX to PDF: {output_path}")
            return output_path
        except Exception as e:
            logger.warning(f"Server-side PDF conversion unavailable: {e}")
            raise RuntimeError(
                f"PDF conversion adapter could not complete ({e}). "
                "In cloud/headless environments, install LibreOffice or download the publication-ready DOCX edition."
            )
