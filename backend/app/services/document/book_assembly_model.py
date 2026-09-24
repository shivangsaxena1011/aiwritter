from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
import re
import uuid


@dataclass
class AssemblyParagraph:
    id: str
    text: str
    paragraph_type: str = "prose"  # "prose" | "bullet" | "numbered" | "callout" | "heading"
    word_count: int = 0

    def __post_init__(self):
        if not self.word_count:
            self.word_count = len(self.text.split())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "text": self.text,
            "paragraph_type": self.paragraph_type,
            "word_count": self.word_count
        }


@dataclass
class AssemblyEquation:
    id: str
    latex: str
    omml_xml: Optional[str] = None
    is_inline: bool = False
    label: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "latex": self.latex,
            "omml_xml": self.omml_xml,
            "is_inline": self.is_inline,
            "label": self.label
        }


@dataclass
class AssemblyTable:
    id: str
    caption: str
    markdown: str
    num_rows: int = 0
    num_cols: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "caption": self.caption,
            "markdown": self.markdown,
            "num_rows": self.num_rows,
            "num_cols": self.num_cols
        }


@dataclass
class AssemblyFigure:
    id: str
    caption: str
    path: Optional[str] = None
    modality: str = "image_png"
    placeholder_box: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "caption": self.caption,
            "path": self.path,
            "modality": self.modality,
            "placeholder_box": self.placeholder_box
        }


@dataclass
class AssemblySection:
    section_id: str
    title: str
    purpose: str
    content: str
    word_count: int = 0
    image_path: Optional[str] = None
    image_caption: Optional[str] = None
    table_markdown: Optional[str] = None
    equations: List[str] = field(default_factory=list)
    paragraphs: List[AssemblyParagraph] = field(default_factory=list)
    tables: List[AssemblyTable] = field(default_factory=list)
    figures: List[AssemblyFigure] = field(default_factory=list)
    is_first_in_topic: bool = False

    def __post_init__(self):
        if not self.word_count and self.content:
            self.word_count = len(self.content.split())
        if not self.paragraphs and self.content:
            self._parse_internal_paragraphs()

    def _parse_internal_paragraphs(self):
        raw_paras = [p.strip() for p in self.content.split("\n\n") if p.strip()]
        for idx, p in enumerate(raw_paras):
            ptype = "prose"
            if p.startswith(("#", "###", "##")):
                ptype = "heading"
            elif p.startswith(("- ", "* ")):
                ptype = "bullet"
            elif re.match(r"^\d+\.\s+", p):
                ptype = "numbered"
            elif p.startswith("> "):
                ptype = "callout"
            self.paragraphs.append(
                AssemblyParagraph(
                    id=f"{self.section_id}_p{idx+1}",
                    text=p,
                    paragraph_type=ptype,
                    word_count=len(p.split())
                )
            )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "section_id": self.section_id,
            "title": self.title,
            "purpose": self.purpose,
            "content": self.content,
            "word_count": self.word_count,
            "image_path": self.image_path,
            "image_caption": self.image_caption,
            "table_markdown": self.table_markdown,
            "equations": self.equations,
            "paragraphs": [p.to_dict() for p in self.paragraphs],
            "tables": [t.to_dict() for t in self.tables],
            "figures": [f.to_dict() for f in self.figures],
            "is_first_in_topic": self.is_first_in_topic
        }


@dataclass
class AssemblyTopic:
    topic_id: str
    title: str
    position: int
    blueprint: Dict[str, Any] = field(default_factory=dict)
    sections: List[AssemblySection] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "topic_id": self.topic_id,
            "title": self.title,
            "position": self.position,
            "blueprint": self.blueprint,
            "sections": [s.to_dict() for s in self.sections]
        }


@dataclass
class AssemblyChapter:
    chapter_id: str
    title: str
    position: int
    introduction: str = ""
    topics: List[AssemblyTopic] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "chapter_id": self.chapter_id,
            "title": self.title,
            "position": self.position,
            "introduction": self.introduction,
            "topics": [t.to_dict() for t in self.topics]
        }


@dataclass
class AssemblyFrontMatter:
    title: str
    subtitle: Optional[str] = None
    author: Optional[str] = None
    academic_level: Optional[str] = None
    preface: str = ""
    toc: Dict[str, Any] = field(default_factory=dict)
    config_summary: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "subtitle": self.subtitle,
            "author": self.author,
            "academic_level": self.academic_level,
            "preface": self.preface,
            "toc": self.toc,
            "config_summary": self.config_summary
        }


@dataclass
class AssemblyBackMatter:
    bibliography: Optional[str] = None
    quality_scorecard: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "bibliography": self.bibliography,
            "quality_scorecard": self.quality_scorecard
        }


@dataclass
class BookAssemblyModel:
    """Rigorous intermediate representation decoupling Content Generation from DOCX Rendering."""
    front_matter: AssemblyFrontMatter
    chapters: List[AssemblyChapter] = field(default_factory=list)
    back_matter: AssemblyBackMatter = field(default_factory=lambda: AssemblyBackMatter())

    def get_counts(self) -> Dict[str, int]:
        total_chapters = len(self.chapters)
        total_topics = sum(len(ch.topics) for ch in self.chapters)
        total_sections = 0
        total_paragraphs = 0
        total_equations = 0
        total_tables = 0
        total_figures = 0
        total_words = 0

        for ch in self.chapters:
            if ch.introduction:
                total_words += len(ch.introduction.split())
                total_paragraphs += len([p for p in ch.introduction.split("\n\n") if p.strip()])
            for top in ch.topics:
                total_sections += len(top.sections)
                for sec in top.sections:
                    total_words += sec.word_count
                    total_paragraphs += len(sec.paragraphs) if sec.paragraphs else len([p for p in sec.content.split("\n\n") if p.strip()])
                    total_equations += len(sec.equations)
                    # Tables attached or inside content
                    if sec.tables:
                        total_tables += len(sec.tables)
                    elif sec.table_markdown:
                        total_tables += 1
                    elif "|---" in sec.content or "| --" in sec.content:
                        total_tables += 1
                    # Figures
                    if sec.figures:
                        total_figures += len(sec.figures)
                    elif sec.image_path:
                        total_figures += 1

        if self.back_matter.bibliography:
            total_words += len(self.back_matter.bibliography.split())
            total_paragraphs += len([p for p in self.back_matter.bibliography.split("\n\n") if p.strip()])

        return {
            "chapters": total_chapters,
            "topics": total_topics,
            "sections": total_sections,
            "paragraphs": total_paragraphs,
            "equations": total_equations,
            "tables": total_tables,
            "figures": total_figures,
            "words": total_words
        }

    def validate_integrity(self) -> List[str]:
        issues = []
        seen_section_ids = set()
        seen_topic_ids = set()
        seen_chapter_ids = set()

        if not self.chapters:
            issues.append("Assembly model contains no chapters.")

        for ch in self.chapters:
            if not ch.title or not ch.title.strip():
                issues.append(f"Chapter ID {ch.chapter_id} has empty title.")
            if ch.chapter_id in seen_chapter_ids:
                issues.append(f"Duplicate chapter ID: {ch.chapter_id}")
            seen_chapter_ids.add(ch.chapter_id)

            if not ch.topics:
                issues.append(f"Chapter '{ch.title}' has no topics.")

            for top in ch.topics:
                if not top.title or not top.title.strip():
                    issues.append(f"Topic ID {top.topic_id} in chapter '{ch.title}' has empty title.")
                if top.topic_id in seen_topic_ids:
                    issues.append(f"Duplicate topic ID: {top.topic_id}")
                seen_topic_ids.add(top.topic_id)

                if not top.sections:
                    issues.append(f"Topic '{top.title}' has no sections.")

                for sec in top.sections:
                    if not sec.title or not sec.title.strip():
                        issues.append(f"Section ID {sec.section_id} in topic '{top.title}' has empty title.")
                    if sec.section_id in seen_section_ids:
                        issues.append(f"Duplicate section ID: {sec.section_id}")
                    seen_section_ids.add(sec.section_id)

                    if not sec.content or not sec.content.strip():
                        issues.append(f"Section '{sec.title}' in topic '{top.title}' has empty content.")

        return issues

    def to_compiled_sections(self) -> List[Dict[str, Any]]:
        """Converts structured assembly model into linear compiled sections for DOCX exporter."""
        compiled = []
        for ch in self.chapters:
            # Chapter Overview (guarantees Chapter H1 is rendered)
            intro_text = ch.introduction or f"Comprehensive academic treatise and pedagogical framework on {ch.title}."
            compiled.append({
                "unit": ch.title,
                "is_unit_overview": True,
                "content": intro_text
            })
            for top in ch.topics:
                is_first = True
                for sec in top.sections:
                    compiled.append({
                        "unit": ch.title,
                        "topic": top.title,
                        "subtopic": sec.title,
                        "is_first_in_topic": is_first,
                        "content": sec.content,
                        "word_count": sec.word_count,
                        "image_path": sec.image_path,
                        "image_caption": sec.image_caption,
                        "table_markdown": sec.table_markdown,
                        "equations": sec.equations
                    })
                    is_first = False

        if self.back_matter.bibliography:
            compiled.append({
                "unit": "References",
                "topic": "Academic Bibliography",
                "subtopic": "References",
                "is_first_in_topic": True,
                "content": self.back_matter.bibliography,
                "word_count": len(self.back_matter.bibliography.split())
            })

        return compiled

    def to_dict(self) -> Dict[str, Any]:
        return {
            "front_matter": self.front_matter.to_dict(),
            "chapters": [ch.to_dict() for ch in self.chapters],
            "back_matter": self.back_matter.to_dict(),
            "counts": self.get_counts()
        }
