import re
import logging
from typing import Dict, Any, List, Optional
from backend.app.services.ai.base import AIProvider
from backend.app.services.prompt_service import prompt_service

logger = logging.getLogger(__name__)

class TOCPlanner:
    """Plans, parses, validates, and normalizes Table of Contents structures."""

    def __init__(self, ai_provider: AIProvider):
        self.ai = ai_provider

    async def plan_toc(
        self,
        raw_syllabus: str,
        title: Optional[str] = None,
        academic_level: str = "University / Reference",
        target_audience: str = "Undergraduate & Graduate"
    ) -> Dict[str, Any]:
        """
        Attempts AI structured planning with automatic regex-based fallback.
        """
        # Try AI structured generation
        prompt = prompt_service.get_prompt(
            "toc_planner.txt",
            title=title or "Academic Textbook",
            target_audience=target_audience,
            academic_level=academic_level,
            raw_syllabus=raw_syllabus
        )

        try:
            result = await self.ai.generate_structured(prompt)
            validated = self.validate_and_normalize(result, fallback_title=title)
            if validated and len(validated.get("units", [])) > 0:
                return validated
        except Exception as e:
            logger.warning(f"AI TOC planning failed ({e}), falling back to deterministic parser")

        # Fallback to deterministic regex parser
        return self.parse_deterministic(raw_syllabus, fallback_title=title)

    def validate_and_normalize(self, data: Dict[str, Any], fallback_title: Optional[str] = None) -> Dict[str, Any]:
        """Ensures schema integrity, removes duplicates, and standardizes numbering."""
        title = data.get("title") or fallback_title or "Academic Textbook"
        units_raw = data.get("units") or []
        normalized_units = []

        seen_unit_titles = set()

        for u_idx, u in enumerate(units_raw, start=1):
            u_name = str(u.get("name", "")).strip()
            if not u_name or u_name.lower() in seen_unit_titles:
                continue
            seen_unit_titles.add(u_name.lower())

            # Normalize unit name prefix
            clean_u_name = re.sub(r"^(?:Unit|Chapter)\s*\d+[\s:\-]*", "", u_name, flags=re.I).strip()
            final_unit_name = f"Unit {u_idx}: {clean_u_name or u_name}"

            topics_raw = u.get("topics") or []
            normalized_topics = []
            seen_topics = set()

            for t_idx, t in enumerate(topics_raw, start=1):
                t_name = str(t.get("name", "")).strip()
                if not t_name or t_name.lower() in seen_topics:
                    continue
                seen_topics.add(t_name.lower())

                clean_t_name = re.sub(r"^\d+\.\d+[\s:\-]*", "", t_name).strip()
                final_topic_name = f"{u_idx}.{t_idx} {clean_t_name or t_name}"

                subtopics_raw = t.get("subtopics") or []
                normalized_subtopics = []
                seen_sub = set()

                for s_idx, s in enumerate(subtopics_raw, start=1):
                    s_name = str(s).strip()
                    if not s_name or s_name.lower() in seen_sub:
                        continue
                    seen_sub.add(s_name.lower())
                    clean_s_name = re.sub(r"^\d+\.\d+\.\d+[\s:\-]*", "", s_name).strip()
                    final_sub_name = f"{u_idx}.{t_idx}.{s_idx} {clean_s_name or s_name}"
                    normalized_subtopics.append(final_sub_name)

                if not normalized_subtopics:
                    normalized_subtopics.append(f"{u_idx}.{t_idx}.1 Overview and Foundations")

                normalized_topics.append({
                    "name": final_topic_name,
                    "subtopics": normalized_subtopics
                })

            if not normalized_topics:
                normalized_topics.append({
                    "name": f"{u_idx}.1 Core Foundations",
                    "subtopics": [f"{u_idx}.1.1 Overview and Fundamentals"]
                })

            normalized_units.append({
                "name": final_unit_name,
                "topics": normalized_topics
            })

        return {
            "title": title,
            "units": normalized_units
        }

    def parse_deterministic(self, text: str, fallback_title: Optional[str] = None) -> Dict[str, Any]:
        """High-precision regex parser for Markdown and numbered outlines."""
        lines = [l.strip() for l in text.split("\n") if l.strip()]
        title = fallback_title or ""

        # Extract title from markdown bold or quotes
        title_m = re.search(r'\*\*([^*]+)\*\*', text) or re.search(r'"([^"]+)"', text)
        if title_m and not title:
            title = title_m.group(1).strip()

        units = []
        curr_unit = None
        curr_topic = None

        for line in lines:
            if line in ["---", "***"] or "book title" in line.lower():
                continue
            clean = line.replace("*", "").replace("#", "").strip()
            if title and title in clean:
                continue

            # Unit / Chapter level
            if line.startswith("# ") or re.match(r"^\d+\.\s*\*?(?:Chapter|Unit)", line, re.I):
                unit_name = re.sub(r"^\d+\.\s*", "", clean).strip()
                curr_unit = {"name": unit_name, "topics": []}
                units.append(curr_unit)
                curr_topic = None
            elif line.startswith("## ") or re.match(r"^\d+\.\d+\s+", clean):
                if not curr_unit:
                    curr_unit = {"name": "Unit 1: Overview", "topics": []}
                    units.append(curr_unit)
                curr_topic = {"name": clean, "subtopics": []}
                curr_unit["topics"].append(curr_topic)
            elif line.startswith("### ") or re.match(r"^\d+\.\d+\.\d+\s+", clean) or line.startswith("-"):
                if not curr_unit:
                    curr_unit = {"name": "Unit 1: Overview", "topics": []}
                    units.append(curr_unit)
                if not curr_topic:
                    curr_topic = {"name": curr_unit["name"], "subtopics": []}
                    curr_unit["topics"].append(curr_topic)

                sub_text = re.sub(r"^[-*•]\s*", "", clean).strip()
                if "," in sub_text and "." not in sub_text and not line.startswith("###"):
                    parts = [p.strip() for p in re.split(r",|\band\b", sub_text) if p.strip()]
                    curr_topic["subtopics"].extend(parts)
                else:
                    curr_topic["subtopics"].append(sub_text)

        raw_result = {"title": title or "Academic Textbook", "units": units}
        return self.validate_and_normalize(raw_result, fallback_title=fallback_title)

    parse_syllabus_regex = parse_deterministic

