from abc import ABC, abstractmethod
from typing import Dict, Any, List

class DocumentExporter(ABC):
    @abstractmethod
    def export(
        self,
        book_title: str,
        subtitle: str,
        author: str,
        academic_level: str,
        toc_data: Dict[str, Any],
        sections: List[Dict[str, Any]],
        assets: List[Dict[str, Any]],
        output_path: str,
        quality_report: Dict[str, Any]
    ) -> str:
        """Exports the book to a designated target file format."""
        pass
