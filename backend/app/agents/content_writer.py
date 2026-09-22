import logging
from typing import Dict, Any, List
from backend.app.services.ai.base import AIProvider
from backend.app.services.prompt_service import prompt_service
from backend.app.agents.book_context_manager import BookContextManager
from backend.app.agents.chapter_depth_controller import ChapterDepthController

logger = logging.getLogger(__name__)

class ContentWriter:
    """Generates authoritative academic chapters, unit overviews, and subtopic content."""

    def __init__(self, ai_provider: AIProvider):
        self.ai = ai_provider

    async def write_unit_overview(
        self,
        book_title: str,
        unit_title: str,
        topics: List[str],
        academic_level: str = "University / Reference"
    ) -> Dict[str, Any]:
        """Generates scholarly roadmap and introduction for a unit/chapter."""
        prompt = prompt_service.get_prompt(
            "chapter_planner.txt",
            book_title=book_title,
            unit_title=unit_title,
            topics_list=", ".join(topics),
            academic_level=academic_level
        )
        try:
            return await self.ai.generate_structured(prompt)
        except Exception as e:
            logger.warning(f"Structured unit overview generation failed ({e}), using markdown fallback")
            text = await self.ai.generate_text(prompt)
            return {
                "unit_introduction": text,
                "learning_outcomes": [f"Master core concepts of {unit_title}"],
                "prerequisites": ["Foundational knowledge"],
                "key_thematic_concepts": topics
            }

    async def write_subtopic_section(
        self,
        book_title: str,
        unit_title: str,
        topic_title: str,
        subtopic_title: str,
        context_manager: BookContextManager,
        writing_depth: str = "Detailed"
    ) -> str:
        """Generates comprehensive, multi-page academic subtopic text."""
        profile = ChapterDepthController.get_profile(writing_depth)
        target_word_count = profile["target_words"]

        previous_context = context_manager.get_hierarchical_context(unit_title, topic_title)
        terminology_rules = context_manager.get_terminology_rules()

        prompt = prompt_service.get_prompt(
            "content_writer.txt",
            book_title=book_title,
            unit_title=unit_title,
            topic_title=topic_title,
            subtopic_title=subtopic_title,
            target_audience=context_manager.target_audience,
            academic_level=context_manager.academic_level,
            target_word_count=target_word_count,
            writing_depth=writing_depth,
            previous_context=previous_context,
            terminology_rules=terminology_rules
        )

        content = await self.ai.generate_text(
            prompt,
            temperature=0.6,
            max_output_tokens=profile["max_tokens"]
        )

        return content.strip()
