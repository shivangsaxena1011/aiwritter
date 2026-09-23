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

        # Determine topic complexity class: low (1-2), medium (2-3), high/derivation (4-6)
        is_intro = any(w in topic_lower for w in ["introduction", "overview", "history", "basic", "foundations"])
        is_app = any(w in topic_lower for w in ["application", "advantages", "devices"]) and not any(w in topic_lower for w in ["laser", "diode", "transistor"])
        is_complex = requires_derivation or any(w in topic_lower for w in [
            "schrödinger", "schrodinger", "box", "well", "newton", "thin film", "einstein",
            "numerical aperture", "hall effect", "dispersion", "grating", "interferometer", "cavity", "ruby", "he-ne"
        ])

        sections = []
        if is_intro:
            # Concise foundational treatment (1-2 sections)
            sections.append({
                "title": f"Historical Evolution and Theoretical Need for {topic_title}",
                "purpose": f"Foundational background, classical inadequacies, and modern emergence of {topic_title}.",
                "section_type": "concept"
            })
            sections.append({
                "title": f"Governing Principles and Core Postulates of {topic_title}",
                "purpose": f"Essential operational definitions, physical meaning, and domain scope.",
                "section_type": "concept"
            })
        elif is_app:
            # Applications & engineering scope (2 sections)
            sections.append({
                "title": f"Industrial and Engineering Implementations of {topic_title}",
                "purpose": f"Comprehensive exploration of field applications and operational case studies.",
                "section_type": "application"
            })
            sections.append({
                "title": f"Technological Frontiers and Performance Limits of {topic_title}",
                "purpose": f"Analysis of operational trade-offs, degradation mechanisms, and efficiency limits.",
                "section_type": "application"
            })
        elif is_complex:
            # Deep analytical & mathematical treatment (4-6 sections)
            sections.append({
                "title": f"Theoretical Framework and Physical Postulates of {topic_title}",
                "purpose": f"Underlying physical laws, conservation symmetries, and starting hypotheses.",
                "section_type": "concept"
            })
            sections.append({
                "title": f"Mathematical Formulation and Boundary Conditions for {topic_title}",
                "purpose": f"Establishing coordinates, boundary conditions, and differential equations.",
                "section_type": "concept"
            })
            if requires_derivation:
                sections.append({
                    "title": f"Formal Step-by-Step Analytical Derivation of {topic_title}",
                    "purpose": f"Rigorous proof moving from axioms through substitution to final closed-form result.",
                    "section_type": "derivation"
                })
            sections.append({
                "title": f"Physical Interpretation and Eigenstate Analysis of {topic_title}",
                "purpose": f"Examining physical meaning of solutions, quantization, and spatial probability distributions.",
                "section_type": "concept"
            })
            sections.append({
                "title": f"Engineering Applications and Experimental Verification of {topic_title}",
                "purpose": f"Metrology, technological devices, and laboratory validation.",
                "section_type": "application"
            })
            sections.append({
                "title": f"Domain Boundaries and Analytical Limitations of {topic_title}",
                "purpose": f"Operating limits, high-energy breakdown, and real-world non-idealities.",
                "section_type": "concept"
            })
        else:
            # Standard analytical treatment (2-3 sections)
            sections.append({
                "title": f"Conceptual Axioms and Physical Mechanism of {topic_title}",
                "purpose": f"Core theory, operational definitions, and physical phenomena.",
                "section_type": "concept"
            })
            sections.append({
                "title": f"Quantitative Properties and Analytical Behavior of {topic_title}",
                "purpose": f"Governing relations, physical variables, and mathematical consequences.",
                "section_type": "concept"
            })
            sections.append({
                "title": f"Technological Applications and Observational Insights in {topic_title}",
                "purpose": f"Practical significance and real-world manifestation in modern engineering.",
                "section_type": "application"
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
            "complexity_level": "High" if is_complex else ("Low" if (is_intro or is_app) else "Medium"),
            "sections": sections
        }
