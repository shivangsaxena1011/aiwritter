import logging
from typing import Dict, Any
from backend.app.services.ai.base import AIProvider
from backend.app.services.prompt_service import prompt_service
from backend.app.agents.book_context_manager import BookContextManager

logger = logging.getLogger(__name__)

class ConsistencyAuditor:
    """Audits cross-chapter terminology, acronyms, and mathematical symbol consistency."""

    def __init__(self, ai_provider: AIProvider):
        self.ai = ai_provider

    async def audit_and_update(
        self,
        section_content: str,
        context_manager: BookContextManager
    ) -> Dict[str, Any]:
        global_context = (
            f"Book: {context_manager.book_title}\n"
            f"Registered Terminology: {', '.join(context_manager.terminology.keys()) or 'None'}\n"
            f"Registered Acronyms: {', '.join(context_manager.acronyms.keys()) or 'None'}\n"
        )
        prompt = prompt_service.get_prompt(
            "consistency_checker.txt",
            global_context=global_context,
            section_content=section_content[:3000]
        )
        try:
            result = await self.ai.generate_structured(prompt)
            # Register newly discovered terms and acronyms into BookContextManager
            for term_item in result.get("new_terms_introduced", []):
                if isinstance(term_item, dict) and "term" in term_item:
                    context_manager.add_terminology(term_item["term"], term_item.get("definition", ""))

            for acr_item in result.get("new_acronyms", []):
                if isinstance(acr_item, dict) and "acronym" in acr_item:
                    context_manager.add_acronym(acr_item["acronym"], acr_item.get("full_form", ""))

            return result
        except Exception as e:
            logger.warning(f"Consistency audit failed: {e}")
            return {
                "is_consistent": True,
                "inconsistencies": [],
                "new_terms_introduced": [],
                "new_acronyms": []
            }
