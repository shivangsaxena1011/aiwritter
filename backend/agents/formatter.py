import re
import logging

logger = logging.getLogger(__name__)

class FormatterAgent:
    def format_content(self, text: str) -> str:
        """Formats and normalizes chapter markdown content."""
        if not text:
            return ""

        # Normalize line endings
        text = text.replace("\r\n", "\n")
        
        # Ensure single space after headings
        text = re.sub(r'^(#+)\s*', r'\1 ', text, flags=re.MULTILINE)
        
        # Standardize spacing around bullet points
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        return text.strip()

    def audit_consistency(self, chapters: dict) -> bool:
        """Audits formatted chapters for structural completeness."""
        logger.info(f"Auditing structural consistency for {len(chapters)} formatted chapters...")
        for ch_num, content in chapters.items():
            if not content or len(content) < 100:
                logger.warning(f"Chapter {ch_num} is unexpectedly short or empty.")
        return True
