import os
import json
import logging

logger = logging.getLogger(__name__)

class BookContextManager:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.data = {
            "book_title": "",
            "about_book": "",
            "chapters_metadata": {},
            "terminology_registry": {},
            "concept_dependencies": {}
        }
        if os.path.exists(self.filepath):
            self.load()

    def initialize_book(self, title: str, about_book: str, toc_data: dict):
        """Initializes the database with Book Title, Description and Chapter hierarchy."""
        self.data["book_title"] = title
        self.data["about_book"] = about_book
        
        chapters = toc_data.get("chapters", [])
        for index, ch in enumerate(chapters):
            ch_num = str(ch.get("chapter_number", index + 1))
            self.data["chapters_metadata"][ch_num] = {
                "title": ch.get("title", f"Chapter {ch_num}"),
                "summary": "",
                "status": "PLANNED"
            }
        self.save()

    def get_chapter_context(self, chapter_num: int) -> dict:
        """
        Compiles historical book memory needed to write or review chapter_num.
        Contains summaries of all chapters < chapter_num, and all previously defined terminology.
        """
        previous_summaries = {}
        for ch_key, ch_meta in self.data["chapters_metadata"].items():
            try:
                ch_val = int(ch_key)
                if ch_val < chapter_num and ch_meta.get("summary"):
                    previous_summaries[ch_key] = {
                        "title": ch_meta["title"],
                        "summary": ch_meta["summary"]
                    }
            except ValueError:
                pass

        # Collect terminology defined in previous chapters
        historical_terminology = {}
        for term, term_data in self.data["terminology_registry"].items():
            introduced_ch = term_data.get("chapter_introduced", 1)
            if introduced_ch < chapter_num:
                historical_terminology[term] = term_data.get("definition", "")

        return {
            "book_title": self.data["book_title"],
            "about_book": self.data["about_book"],
            "previous_chapter_summaries": previous_summaries,
            "introduced_terminology": historical_terminology
        }

    def register_chapter_results(self, chapter_num: int, summary: str, terminology: dict):
        """Saves the resulting summary and newly introduced terminology of a completed chapter."""
        ch_key = str(chapter_num)
        
        if ch_key in self.data["chapters_metadata"]:
            self.data["chapters_metadata"][ch_key]["summary"] = summary
            self.data["chapters_metadata"][ch_key]["status"] = "COMPLETED"
        else:
            self.data["chapters_metadata"][ch_key] = {
                "title": f"Chapter {ch_key}",
                "summary": summary,
                "status": "COMPLETED"
            }

        if isinstance(terminology, dict):
            for term, definition in terminology.items():
                if term not in self.data["terminology_registry"] or not self.data["terminology_registry"][term].get("definition"):
                    self.data["terminology_registry"][term] = {
                        "definition": definition,
                        "chapter_introduced": chapter_num
                    }
        
        self.save()

    def save(self):
        """Saves current state to persistent JSON file."""
        try:
            os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=2)
            logger.info(f"BookContext saved to: {self.filepath}")
        except Exception as e:
            logger.error(f"Failed to save BookContext: {e}")

    def load(self):
        """Loads state from JSON file."""
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                self.data = json.load(f)
            logger.info(f"BookContext loaded from: {self.filepath}")
        except Exception as e:
            logger.error(f"Failed to load BookContext: {e}")
