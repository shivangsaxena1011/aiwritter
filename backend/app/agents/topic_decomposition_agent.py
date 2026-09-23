"""
TopicDecompositionAgent — Decomposes Major Topics into pedagogically structured,
subject-aware sections. Adapts structure specifically for Physics, Engineering,
Mathematics, Computer Science, or General Sciences.
"""

import logging
from typing import Dict, Any, List, Optional
from backend.app.agents.base import BaseAgent, AgentContext, AgentResult
from backend.app.services.ai.base import AIProvider

logger = logging.getLogger(__name__)

# Subject Archetype Section Blueprints
PHYSICS_BLUEPRINT = [
    "Conceptual Introduction",
    "Physical Concept and Theory",
    "Mathematical Formulation",
    "Derivation of Governing Equations",
    "Physical Interpretation",
    "Practical Applications",
    "Limitations and Boundary Conditions"
]

CS_BLUEPRINT = [
    "Conceptual Overview",
    "Formal Definition and Specifications",
    "Algorithmic Working and Data Flow",
    "Implementation and Syntax",
    "Complexity Analysis",
    "Common Pitfalls and Edge Cases",
    "Industrial Applications"
]

MATH_BLUEPRINT = [
    "Rigorous Definition",
    "Fundamental Axioms and Theorems",
    "Formal Proof and Derivation",
    "Analytical Properties",
    "Worked Mathematical Example",
    "Applications and Generalizations"
]

ENGINEERING_BLUEPRINT = [
    "Engineering Principles and Foundations",
    "Governing Equations and Physical Laws",
    "System Architecture and Component Design",
    "Operational Working Mechanism",
    "Engineering Applications and Case Studies",
    "Design Constraints and Failure Modes"
]

GENERAL_BLUEPRINT = [
    "Introduction and Foundational Concepts",
    "Theoretical Framework",
    "Analytical Formulation",
    "Practical Applications",
    "Summary and Critical Observations"
]

class TopicDecompositionAgent(BaseAgent):
    """
    Intelligently breaks down major topics into subject-specific academic sections.
    """

    def __init__(self, ai_provider: Optional[AIProvider] = None):
        super().__init__(ai_provider)

    async def run(self, context: AgentContext, topic_title: str = "", **kwargs) -> AgentResult:
        topic_info = kwargs.get("topic_info", {"title": topic_title})
        decomp = await self.decompose_topic(
            topic_title=topic_title or topic_info.get("title", ""),
            subject=context.subject or context.book_title,
            academic_level=context.academic_level,
            requires_derivation=topic_info.get("requires_derivation", False),
            requires_numericals=topic_info.get("requires_numericals", False)
        )
        return AgentResult(status="success", data=decomp)

    async def decompose_topic(
        self,
        topic_title: str,
        subject: str,
        academic_level: str = "University / Reference",
        requires_derivation: bool = False,
        requires_numericals: bool = False
    ) -> Dict[str, Any]:
        """
        Generates an intelligent, non-templated decomposition adapted to the specific subject domain.
        """
        # Attempt AI decomposition
        if self.ai:
            try:
                ai_sections = await self._decompose_with_ai(
                    topic_title, subject, academic_level, requires_derivation, requires_numericals
                )
                if ai_sections and len(ai_sections.get("sections", [])) >= 3:
                    return ai_sections
            except Exception as e:
                logger.warning(f"AI Topic Decomposition failed ({e}), using domain heuristic blueprint")

        # Deterministic domain heuristic
        return self._decompose_heuristically(topic_title, subject, requires_derivation, requires_numericals)

    async def _decompose_with_ai(
        self,
        topic_title: str,
        subject: str,
        academic_level: str,
        requires_derivation: bool,
        requires_numericals: bool
    ) -> Dict[str, Any]:
        prompt = f"""You are the TopicDecompositionAgent in an academic publishing engine.
Decompose the following major topic into a coherent, pedagogically sound sequence of sub-sections.

SUBJECT: {subject}
MAJOR TOPIC: {topic_title}
ACADEMIC LEVEL: {academic_level}
REQUIRES DERIVATION: {requires_derivation}
REQUIRES NUMERICAL EXAMPLES: {requires_numericals}

INSTRUCTIONS:
1. Do NOT blindly output generic headings. The structure MUST be tailored to whether this is Physics, Computer Science, Mathematics, Engineering, or a general science.
2. If Physics: focus on Introduction -> Physical Concept -> Mathematical Formulation -> Derivation -> Physical Interpretation -> Applications -> Limitations.
3. If Computer Science: focus on Concept -> Formal Specs -> Working / Architecture -> Implementation -> Complexity -> Real-world Applications.
4. If Mathematics: focus on Definition -> Theorems -> Proof / Derivation -> Properties -> Applications.
5. If Engineering: focus on Principles -> Governing Equations -> System Design -> Operation -> Trade-offs / Failure Modes.
6. Only include Derivation section if mathematically applicable.
7. Only include Worked Numerical Example if computational/numerical requested.

Return JSON:
{{
  "topic": "{topic_title}",
  "subject_domain": "Physics | Computer Science | Mathematics | Engineering | General Science",
  "sections": [
    {{
      "title": "Section Title",
      "purpose": "Brief description of what this section explains",
      "section_type": "concept | derivation | numerical | diagram_focus | application"
    }}
  ]
}}
"""
        return await self.ai.generate_structured(prompt)

    def _decompose_heuristically(
        self,
        topic_title: str,
        subject: str,
        requires_derivation: bool,
        requires_numericals: bool
    ) -> Dict[str, Any]:
        subj_lower = subject.lower()
        topic_lower = topic_title.lower()

        # Identify subject domain
        if any(w in subj_lower for w in ["physic", "quantum", "thermodynamic", "mechanic", "optics", "electromagnet"]):
            domain = "Physics"
            raw_blueprint = list(PHYSICS_BLUEPRINT)
        elif any(w in subj_lower for w in ["computer", "software", "program", "data structure", "algorithm", "ai", "machine learning"]):
            domain = "Computer Science"
            raw_blueprint = list(CS_BLUEPRINT)
        elif any(w in subj_lower for w in ["math", "calculus", "linear algebra", "discrete", "geometry", "probability", "statistics"]):
            domain = "Mathematics"
            raw_blueprint = list(MATH_BLUEPRINT)
        elif any(w in subj_lower for w in ["engineer", "electrical", "mechanical", "chemical", "civil", "robot"]):
            domain = "Engineering"
            raw_blueprint = list(ENGINEERING_BLUEPRINT)
        else:
            domain = "General Science"
            raw_blueprint = list(GENERAL_BLUEPRINT)

        sections = []
        for name in raw_blueprint:
            # Skip derivation if not needed
            if "derivation" in name.lower() and not requires_derivation:
                continue
            # Skip proof if not mathematical
            if "proof" in name.lower() and not requires_derivation:
                continue

            sec_type = "concept"
            if "derivation" in name.lower() or "proof" in name.lower():
                sec_type = "derivation"
            elif "application" in name.lower():
                sec_type = "application"

            sections.append({
                "title": f"{name} of {topic_title}",
                "purpose": f"Detailed academic exploration of {name.lower()}.",
                "section_type": sec_type
            })

        if requires_numericals:
            sections.append({
                "title": f"Worked Numerical Examples on {topic_title}",
                "purpose": "Step-by-step verified numerical problem solutions with units.",
                "section_type": "numerical"
            })

        return {
            "topic": topic_title,
            "subject_domain": domain,
            "sections": sections
        }
