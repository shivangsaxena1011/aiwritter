"""
DocumentStructureAgent — Plans the formal academic monograph architecture:
Cover / Title Page -> Preface -> Table of Contents -> Chapter Treatises ->
Worked Derivations & Numericals -> References & Bibliography -> Publication Quality Audit.
"""

from typing import Dict, Any, List

class DocumentStructureAgent:
    """
    Synthesizes chapters, sections, and metadata into a standardized academic layout.
    """

    @classmethod
    def plan_document_structure(
        cls,
        book_title: str,
        subject: str,
        academic_level: str,
        chapters: List[Dict[str, Any]],
        include_references: bool = True
    ) -> Dict[str, Any]:
        """
        Organizes the book's sections into logical publishing order.
        """
        structure = {
            "front_matter": [
                {"type": "title_page", "title": book_title, "subject": subject, "level": academic_level},
                {"type": "preface", "title": "Preface & Academic Scope"},
                {"type": "table_of_contents", "title": "Table of Contents"}
            ],
            "body": [],
            "back_matter": []
        }

        for ch in chapters:
            ch_item = {
                "chapter_number": ch.get("number", 1),
                "title": ch.get("title", ""),
                "overview_included": True,
                "topics": ch.get("topics", [])
            }
            structure["body"].append(ch_item)

        if include_references:
            structure["back_matter"].append({
                "type": "references",
                "title": "References & Academic Bibliography"
            })

        structure["back_matter"].append({
            "type": "quality_scorecard",
            "title": "Academic Quality & Publication Audit"
        })

        return structure
