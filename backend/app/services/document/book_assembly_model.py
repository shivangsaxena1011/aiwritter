from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field


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
    is_first_in_topic: bool = False

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


@dataclass
class AssemblyBackMatter:
    bibliography: Optional[str] = None
    quality_scorecard: Optional[Dict[str, Any]] = None


@dataclass
class BookAssemblyModel:
    """Rigorous intermediate representation decoupling Content Generation from DOCX Rendering."""
    front_matter: AssemblyFrontMatter
    chapters: List[AssemblyChapter] = field(default_factory=list)
    back_matter: AssemblyBackMatter = field(default_factory=lambda: AssemblyBackMatter())

    def to_compiled_sections(self) -> List[Dict[str, Any]]:
        """Converts structured assembly model into linear compiled sections for DOCX exporter."""
        compiled = []
        for ch in self.chapters:
            # Chapter Overview
            if ch.introduction:
                compiled.append({
                    "unit": ch.title,
                    "is_unit_overview": True,
                    "content": ch.introduction
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
                        "table_markdown": sec.table_markdown
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
