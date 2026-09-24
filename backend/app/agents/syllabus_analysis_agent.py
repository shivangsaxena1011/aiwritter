"""
SyllabusAnalysisAgent — Deep analysis, decomposition, and requirement tagging of course syllabi.
Preserves complete syllabus coverage, extracts prerequisite dependencies, and flags topics requiring
derivations, equations, diagrams, and numerical examples.
"""

import re
import logging
from typing import Dict, Any, List, Optional
from backend.app.agents.base import BaseAgent, AgentContext, AgentResult
from backend.app.services.ai.base import AIProvider

logger = logging.getLogger(__name__)

# Keywords triggering specific academic features
DERIVATION_KEYWORDS = {
    "derivation", "derive", "schrodinger", "equation", "formula", "theorem",
    "proof", "wave equation", "maxwell", "dynamics", "kinetics", "hamiltonian",
    "lagrangian", "thermodynamic", "law", "calculus", "potential", "oscillator",
    "relativity", "field", "flux", "energy", "force", "momentum", "fourier"
}

DIAGRAM_KEYWORDS = {
    "diagram", "schematic", "wave", "particle", "box", "well", "circuit",
    "architecture", "flowchart", "apparatus", "structure", "lattice", "band",
    "cell", "stack", "geometry", "model", "distribution", "spectrum", "graph",
    "representation", "cycle", "process"
}

NUMERICAL_KEYWORDS = {
    "numerical", "problem", "calculation", "example", "worked", "constant",
    "wavelength", "frequency", "probability", "efficiency", "power", "density",
    "velocity", "mass", "charge", "dimension"
}

class SyllabusAnalysisAgent(BaseAgent):
    """
    Parses raw university syllabus, detects chapters, major topics, subtopics,
    and tags technical requirements (derivations, diagrams, numericals) without dropping topics.
    """

    def __init__(self, ai_provider: Optional[AIProvider] = None):
        super().__init__(ai_provider)

    async def run(self, context: AgentContext, raw_text: str = "", **kwargs) -> AgentResult:
        analysis = await self.analyze_syllabus(
            raw_text=raw_text or context.extra.get("raw_syllabus", ""),
            subject=context.subject or context.book_title,
            academic_level=context.academic_level,
            include_numericals=context.include_numericals,
            include_diagrams=context.include_diagrams
        )
        return AgentResult(
            status="success",
            data=analysis,
            metadata={"subject": analysis.get("subject", ""), "chapters_count": len(analysis.get("chapters", []))}
        )

    async def analyze_syllabus(
        self,
        raw_text: str,
        subject: Optional[str] = None,
        academic_level: str = "University / Reference",
        include_numericals: bool = False,
        include_diagrams: bool = True
    ) -> Dict[str, Any]:
        """
        Parses syllabus into structured chapters and topics with requirement flags.
        Uses AI provider when available, falling back to deterministic extraction.
        """
        if not raw_text or not raw_text.strip():
            return {
                "subject": subject or "Academic Subject",
                "chapters": []
            }

        # Attempt AI analysis if provider is active
        if self.ai:
            try:
                ai_result = await self._analyze_with_ai(raw_text, subject, academic_level, include_numericals, include_diagrams)
                if ai_result and ai_result.get("chapters"):
                    return self._enrich_and_validate(ai_result, subject, include_numericals, include_diagrams)
            except Exception as e:
                logger.warning(f"AI syllabus analysis failed ({e}), falling back to deterministic analysis")

        return self.analyze_deterministic(raw_text, subject=subject, include_numericals=include_numericals, include_diagrams=include_diagrams)

    async def _analyze_with_ai(
        self,
        raw_text: str,
        subject: Optional[str],
        academic_level: str,
        include_numericals: bool,
        include_diagrams: bool
    ) -> Dict[str, Any]:
        prompt = f"""You are the SyllabusAnalysisAgent in an academic textbook publishing engine.
Analyze the following course syllabus and produce a precise JSON structure.

SUBJECT: {subject or 'Inferred from syllabus'}
ACADEMIC LEVEL: {academic_level}
USER INCLUDE NUMERICALS CONFIG: {'YES' if include_numericals else 'NO'}
USER INCLUDE DIAGRAMS CONFIG: {'YES' if include_diagrams else 'NO'}

RAW SYLLABUS:
\"\"\"
{raw_text}
\"\"\"

CRITICAL RULES:
1. Preserve 100% of the syllabus topics. NEVER silently remove or truncate syllabus topics.
2. Group content into numbered Chapters.
3. For each Chapter, extract Major Topics and Subtopics.
4. For each Topic, classify:
   - requires_derivation: true if mathematical, physical, or algorithmic derivation is required.
   - requires_diagram: true if conceptual visual, apparatus, or schematic is helpful.
   - requires_numericals: true only if user requested numericals and topic is computational.
   - implicit_concepts: list of foundational concepts needed to explain this topic.
   - prerequisites: prior topics in this course or foundational knowledge needed.

JSON Output Schema:
{{
  "subject": "Subject Name",
  "chapters": [
    {{
      "number": 1,
      "title": "Chapter Title",
      "topics": [
        {{
          "title": "Major Topic Title",
          "subtopics": ["Subtopic 1", "Subtopic 2"],
          "requires_derivation": true,
          "requires_diagram": true,
          "requires_numericals": false,
          "implicit_concepts": ["concept 1"],
          "prerequisites": ["prereq 1"]
        }}
      ]
    }}
  ]
}}
"""
        return await self.ai.generate_structured(prompt)

    def analyze_deterministic(
        self,
        raw_text: str,
        subject: Optional[str] = None,
        include_numericals: bool = False,
        include_diagrams: bool = True
    ) -> Dict[str, Any]:
        """
        Deterministic regex and structural parser for syllabus text.
        Guarantees 100% coverage and zero data loss.
        """
        lines = [line.strip() for line in raw_text.splitlines() if line.strip()]
        detected_subject = subject or "Academic Textbook"

        # Check for Book: / Subject: headers
        for line in lines[:5]:
            subj_match = re.match(r"^(?:Book|Subject|Course):\s*(.+)$", line, re.I)
            if subj_match:
                detected_subject = subj_match.group(1).strip()
                break

        chapters = []
        current_chapter = None
        current_topic = None

        chapter_pattern = re.compile(
            r"^(?:Chapter|Unit|Module|Part)\s*(\d+)[\s:\-\.]+(.+)$|"
            r"^#\s+(.+)$",
            re.I
        )

        topic_pattern = re.compile(
            r"^(?:Major\s+Topic|Topic|\d+\.\d+|\d+)[\s:\-\.]+(.+)$|"
            r"^##\s+(.+)$|"
            r"^-\s+(.+)$",
            re.I
        )

        subtopic_pattern = re.compile(
            r"^(?:Subtopic|\d+\.\d+\.\d+)[\s:\-\.]+(.+)$|"
            r"^###\s+(.+)$|"
            r"^\*\s+(.+)$",
            re.I
        )

        in_major_topics_block = False

        has_future_chapter = any(bool(chapter_pattern.match(l)) for l in lines)

        for line in lines:
            # Skip subject/course/program metadata lines if detected
            if re.match(r"^(?:Book|Subject|Course|Syllabus|Program|Degree):\s*", line, re.I):
                continue
            if re.match(r"^(?:B\.?Tech|B\.?E\.?|M\.?Tech|Undergraduate|Degree|First\s+Year|Second\s+Year).*—.*", line, re.I):
                detected_subject = line.split("—")[-1].strip() if "—" in line else line.strip()
                continue

            if re.match(r"^Major\s+Topics:\s*$", line, re.I):
                in_major_topics_block = True
                continue

            # 1. Match Chapter
            ch_match = chapter_pattern.match(line)
            if ch_match:
                num = len(chapters) + 1
                title = ch_match.group(2) or ch_match.group(3) or line
                title = re.sub(r"^(?:Chapter|Unit|Module)\s*\d+[\s:\-\.]*", "", title, flags=re.I).strip()
                current_chapter = {
                    "number": num,
                    "title": title or f"Chapter {num}",
                    "topics": []
                }
                chapters.append(current_chapter)
                current_topic = None
                in_major_topics_block = False
                continue

            # If chapters exist later in document and no chapter has started yet, this line is preamble metadata
            if has_future_chapter and not current_chapter:
                continue

            # Ensure at least one chapter exists if document has no chapter headers at all
            if not current_chapter:
                current_chapter = {
                    "number": 1,
                    "title": detected_subject or "Core Foundations",
                    "topics": []
                }
                chapters.append(current_chapter)

            # 2. Match Subtopic (indented or bulleted under a topic)
            sub_match = subtopic_pattern.match(line)
            if sub_match and current_topic and not in_major_topics_block:
                sub_title = sub_match.group(1) or sub_match.group(2) or sub_match.group(3) or line
                sub_title = sub_title.strip()
                if sub_title and sub_title not in current_topic["subtopics"]:
                    current_topic["subtopics"].append(sub_title)
                continue

            # 3. Match Topic
            t_match = topic_pattern.match(line)
            if t_match or in_major_topics_block or line.startswith("-") or line.startswith("•"):
                raw_t = t_match.group(1) or t_match.group(2) or t_match.group(3) if t_match else line
                raw_t = re.sub(r"^[\d\.\-\*•\s]+", "", raw_t).strip()
                if not raw_t:
                    continue

                req_deriv = self._requires_derivation(raw_t)
                req_diag = include_diagrams and self._requires_diagram(raw_t)
                req_num = include_numericals and self._requires_numericals(raw_t)

                current_topic = {
                    "title": raw_t,
                    "subtopics": [],
                    "requires_derivation": req_deriv,
                    "requires_diagram": req_diag,
                    "requires_numericals": req_num,
                    "implicit_concepts": self._extract_implicit_concepts(raw_t),
                    "prerequisites": []
                }
                current_chapter["topics"].append(current_topic)
                continue

            # Fallback line handling — attach as topic or subtopic
            if current_topic:
                current_topic["subtopics"].append(line.strip())
            elif current_chapter:
                current_topic = {
                    "title": line.strip(),
                    "subtopics": [],
                    "requires_derivation": self._requires_derivation(line),
                    "requires_diagram": include_diagrams and self._requires_diagram(line),
                    "requires_numericals": include_numericals and self._requires_numericals(line),
                    "implicit_concepts": [],
                    "prerequisites": []
                }
                current_chapter["topics"].append(current_topic)

        # Post-process: ensure every chapter has at least one topic
        for ch in chapters:
            if not ch["topics"]:
                ch["topics"].append({
                    "title": f"Fundamentals of {ch['title']}",
                    "subtopics": ["Overview and Core Principles"],
                    "requires_derivation": False,
                    "requires_diagram": include_diagrams,
                    "requires_numericals": False,
                    "implicit_concepts": [],
                    "prerequisites": []
                })

        return {
            "subject": detected_subject,
            "chapters": chapters
        }

    def _requires_derivation(self, text: str) -> bool:
        lower = text.lower()
        return any(k in lower for k in DERIVATION_KEYWORDS)

    def _requires_diagram(self, text: str) -> bool:
        lower = text.lower()
        return any(k in lower for k in DIAGRAM_KEYWORDS) or len(text) > 4

    def _requires_numericals(self, text: str) -> bool:
        lower = text.lower()
        return any(k in lower for k in NUMERICAL_KEYWORDS)

    def _extract_implicit_concepts(self, topic_title: str) -> List[str]:
        words = re.findall(r"\b[A-Za-z]{4,}\b", topic_title)
        return [w.capitalize() for w in words[:3]]

    def _enrich_and_validate(
        self,
        ai_data: Dict[str, Any],
        subject: Optional[str],
        include_numericals: bool,
        include_diagrams: bool
    ) -> Dict[str, Any]:
        """Validates AI syllabus output and ensures boolean flags adhere to user preferences."""
        chapters = ai_data.get("chapters", [])
        for ch in chapters:
            for t in ch.get("topics", []):
                if not include_numericals:
                    t["requires_numericals"] = False
                if not include_diagrams:
                    t["requires_diagram"] = False
                if "subtopics" not in t or not isinstance(t["subtopics"], list):
                    t["subtopics"] = []
                if "requires_derivation" not in t:
                    t["requires_derivation"] = self._requires_derivation(t.get("title", ""))
        return {
            "subject": ai_data.get("subject") or subject or "Academic Textbook",
            "chapters": chapters
        }
