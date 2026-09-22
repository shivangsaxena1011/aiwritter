from typing import Dict, List, Any, Optional

class BookContextManager:
    """
    Maintains hierarchical context across the entire book generation lifecycle.
    Tracks book-level settings, glossary, notation, symbols, and summaries of past chapters.
    """

    def __init__(
        self,
        book_title: str,
        academic_level: str = "University / Reference",
        target_audience: str = "Undergraduate & Graduate",
        writing_depth: str = "Detailed",
        citation_style: str = "IEEE"
    ):
        self.book_title = book_title
        self.academic_level = academic_level
        self.target_audience = target_audience
        self.writing_depth = writing_depth
        self.citation_style = citation_style

        # Global registries
        self.terminology: Dict[str, str] = {}
        self.acronyms: Dict[str, str] = {}
        self.symbols: Dict[str, str] = {}
        self.chapter_summaries: Dict[str, str] = {}
        self.section_summaries: List[Dict[str, str]] = []

    def add_terminology(self, term: str, definition: str):
        if term and term not in self.terminology:
            self.terminology[term] = definition

    def add_acronym(self, acronym: str, full_form: str):
        if acronym and acronym not in self.acronyms:
            self.acronyms[acronym] = full_form

    def add_symbol(self, symbol: str, meaning: str):
        if symbol and symbol not in self.symbols:
            self.symbols[symbol] = meaning

    def record_section_summary(self, unit_name: str, topic_name: str, subtopic_name: str, summary: str):
        self.section_summaries.append({
            "unit": unit_name,
            "topic": topic_name,
            "subtopic": subtopic_name,
            "summary": summary
        })

    def get_hierarchical_context(self, current_unit: str, current_topic: str) -> str:
        """
        Returns a concise context summary of preceding chapters to ensure continuity
        without blowing up prompt token limits.
        """
        context_parts = []

        # Recent section summaries (last 3 sections)
        if self.section_summaries:
            context_parts.append("Summary of Immediately Preceding Sections:")
            for s in self.section_summaries[-3:]:
                context_parts.append(f"- [{s['unit']} > {s['topic']} > {s['subtopic']}]: {s['summary']}")

        # Established terminology (up to 10 key terms)
        if self.terminology:
            terms_sample = list(self.terminology.items())[-8:]
            terms_str = "; ".join([f"{k}: {v}" for k, v in terms_sample])
            context_parts.append(f"Established Terminology: {terms_str}")

        # Established acronyms
        if self.acronyms:
            acronyms_str = ", ".join([f"{k} = {v}" for k, v in list(self.acronyms.items())[-8:]])
            context_parts.append(f"Standard Acronyms: {acronyms_str}")

        return "\n\n".join(context_parts) if context_parts else "This is the initial section of the textbook."

    def get_terminology_rules(self) -> str:
        rules = [
            "Use precise academic definitions and avoid colloquial re-explanations.",
            f"Adhere strictly to {self.citation_style} style conventions.",
            "Maintain consistent variable names and Greek symbols across all chapters."
        ]
        if self.acronyms:
            rules.append(f"Use existing acronym definitions: {', '.join([f'{k} ({v})' for k, v in list(self.acronyms.items())[:6]])}")
        return "\n".join([f"- {r}" for r in rules])
