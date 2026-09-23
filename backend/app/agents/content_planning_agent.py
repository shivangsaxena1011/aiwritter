"""
ContentPlanningAgent — Synthesizes syllabus requirements, research notes,
and user configuration into a pedagogical chapter and section blueprint.
Enforces the PARAGRAPHS-FIRST policy and controls numericals/questions/examples.
"""

import logging
from typing import Dict, Any, List, Optional
from backend.app.agents.base import BaseAgent, AgentContext, AgentResult
from backend.app.services.ai.base import AIProvider

logger = logging.getLogger(__name__)

class ContentPlanningAgent(BaseAgent):
    """
    Plans chapter learning paths and sectional structural requirements.
    """

    def __init__(self, ai_provider: Optional[AIProvider] = None):
        super().__init__(ai_provider)

    async def run(self, context: AgentContext, unit_title: str = "", topics: List[str] = None, **kwargs) -> AgentResult:
        plan = await self.plan_chapter(
            book_title=context.book_title,
            subject=context.subject or context.book_title,
            unit_title=unit_title,
            topics=topics or [],
            academic_level=context.academic_level,
            writing_depth=context.writing_depth,
            include_numericals=context.include_numericals,
            include_questions=context.include_questions,
            include_examples=context.include_examples
        )
        return AgentResult(status="success", data=plan)

    async def plan_chapter(
        self,
        book_title: str,
        subject: str,
        unit_title: str,
        topics: List[str],
        academic_level: str = "University / Reference",
        writing_depth: str = "Detailed",
        include_numericals: bool = False,
        include_questions: bool = False,
        include_examples: bool = True
    ) -> Dict[str, Any]:
        """
        Builds a comprehensive roadmap for a textbook chapter.
        """
        if self.ai:
            try:
                prompt = f"""You are the ContentPlanningAgent in an academic publishing engine.
Generate an introductory chapter overview and pedagogical roadmap.

BOOK TITLE: {book_title}
SUBJECT: {subject}
CHAPTER/UNIT: {unit_title}
TOPICS LIST: {', '.join(topics)}
ACADEMIC LEVEL: {academic_level}
WRITING DEPTH: {writing_depth}
INCLUDE NUMERICAL PROBLEMS: {'YES' if include_numericals else 'NO'}
INCLUDE QUESTIONS & ANSWERS: {'YES' if include_questions else 'NO'}
INCLUDE EXAMPLES: {'YES' if include_examples else 'NO'}

CRITICAL GUIDELINES:
1. Write in prose paragraphs first. Avoid bulleted filler.
2. Outline clear learning objectives and foundational prerequisites.
3. Establish how this chapter connects with preceding and succeeding subject matter.

Return JSON:
{{
  "unit_introduction": "2-3 comprehensive academic paragraphs introducing the chapter themes and significance.",
  "learning_outcomes": ["Understand fundamental state formulations", "Analyze boundary dynamics"],
  "prerequisites": ["Foundational calculus and Newtonian mechanics"],
  "pedagogical_strategy": "Paragraph-first progression from physical intuition to mathematical rigor.",
  "key_thematic_concepts": {str(topics)}
}}
"""
                res = await self.ai.generate_structured(prompt)
                if res and res.get("unit_introduction"):
                    return res
            except Exception as e:
                logger.warning(f"AI chapter planning failed ({e}), using academic blueprint fallback")

        # Deterministic fallback
        intro_text = (
            f"The study of {unit_title} constitutes an essential cornerstone within {subject}. "
            "This chapter develops the conceptual architecture, physical laws, and analytical models necessary to investigate complex behaviors across static and dynamic regimes. "
            "Beginning with core theoretical postulates, the discourse systematically advances through governing differential equations, boundary value analyses, and real-world system implementations.\n\n"
            f"Throughout this unit, readers explore the interrelationships connecting {', '.join(topics[:3]) if topics else 'foundational topics'}. "
            "Special emphasis is placed on mathematical rigor and physical interpretation, ensuring students develop both analytical competence and conceptual intuition."
        )

        return {
            "unit_introduction": intro_text,
            "learning_outcomes": [
                f"Master the governing principles and theoretical foundations of {unit_title}.",
                "Formulate and evaluate quantitative state models and differential equations.",
                "Critically evaluate operational constraints, boundary phenomena, and industrial applications."
            ],
            "prerequisites": [
                f"Foundational knowledge of elementary calculus, linear algebra, and introductory {subject}."
            ],
            "pedagogical_strategy": "Paragraph-first expository prose with rigorous mathematical derivations and applied case studies.",
            "key_thematic_concepts": topics
        }
