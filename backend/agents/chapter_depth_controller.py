import re
import logging

logger = logging.getLogger(__name__)

class ChapterDepthController:
    def __init__(self, min_words: int = 1200, target_words: int = 2500):
        self.min_words = min_words
        self.target_words = target_words

    def analyze_chapter(self, text: str) -> dict:
        """Calculates educational depth metrics for a chapter markdown draft."""
        words = len(re.findall(r'\b\w+\b', text))
        subtopics = len(re.findall(r'^##\s+', text, re.MULTILINE))
        table_count = len(re.findall(r'\|.*\|', text)) // 3
        example_count = len(re.findall(r'example|case study|for instance', text, re.IGNORECASE))
        diagram_count = len(re.findall(r'\[DIAGRAM_PLACEHOLDER', text))

        return {
            "total_words": words,
            "subtopic_count": subtopics,
            "table_count": max(0, table_count),
            "example_count": example_count,
            "diagram_count": diagram_count,
            "depth_status": "SUFFICIENT" if words >= self.min_words else "INSUFFICIENT"
        }

    def get_adjustment_instructions(self, metrics: dict) -> str:
        """Generates specific prompt instructions to expand or condense content."""
        instructions = []
        if metrics["total_words"] < self.min_words:
            instructions.append(f"- EXPAND: Draft has {metrics['total_words']} words (minimum target is {self.min_words}). Add detailed technical explanations, clear sub-sections, and real-world examples.")
        if metrics["example_count"] < 2:
            instructions.append("- EXAMPLES: Include at least 2 structured practical examples or worked case studies.")
        if metrics["table_count"] < 1:
            instructions.append("- COMPARISON TABLE: Include a structured markdown comparison or reference table.")

        return "\n".join(instructions) if instructions else "- MAINTAIN: Maintain current academic depth and terminology rigor."
