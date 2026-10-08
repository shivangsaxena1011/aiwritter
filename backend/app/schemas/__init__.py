from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator

class SubtopicSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        s = v.strip()
        if not s:
            raise ValueError("Subtopic name cannot be blank or whitespace-only")
        return s

class TopicSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    subtopics: List[str] = Field(default_factory=list, max_length=20)

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        s = v.strip()
        if not s:
            raise ValueError("Topic name cannot be blank or whitespace-only")
        return s

    @field_validator("subtopics", mode="before")
    @classmethod
    def normalize_subtopics(cls, v):
        if not isinstance(v, list):
            return ["Foundational Analysis"]
        normalized = []
        for item in v:
            if isinstance(item, dict):
                name = item.get("name") or item.get("title") or str(item)
                s = str(name).strip()
                if s:
                    normalized.append(s)
            elif isinstance(item, str):
                s = item.strip()
                if s:
                    normalized.append(s)
            elif item is not None:
                s = str(item).strip()
                if s:
                    normalized.append(s)
        if len(normalized) > 20:
            raise ValueError("A single topic cannot exceed 20 subtopics")
        return normalized or ["Foundational Analysis"]

class UnitSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    topics: List[TopicSchema] = Field(default_factory=list, max_length=25)

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        s = v.strip()
        if not s:
            raise ValueError("Unit name cannot be blank or whitespace-only")
        return s

class TableOfContentsSchema(BaseModel):
    units: List[UnitSchema] = Field(..., min_length=1, max_length=30)

    @field_validator("units")
    @classmethod
    def validate_total_subtopics(cls, v: List[UnitSchema]) -> List[UnitSchema]:
        total_subtopics = 0
        for u in v:
            for t in u.topics:
                total_subtopics += len(t.subtopics)
        if total_subtopics > 120:
            raise ValueError(f"Total book subtopics ({total_subtopics}) exceeds maximum allowed limit of 120")
        return v

class ParseSyllabusRequest(BaseModel):
    text: str = Field(..., min_length=5, max_length=50000, description="Raw syllabus, outline, or markdown text")
    api_key: Optional[str] = None

    @field_validator("text")
    @classmethod
    def validate_non_blank_text(cls, v: str) -> str:
        s = v.strip()
        if len(s) < 5:
            raise ValueError("Syllabus text must contain at least 5 non-whitespace characters")
        return s

class ParseSyllabusResponse(BaseModel):
    title: str
    units: List[UnitSchema]

class CreateBookRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    subtitle: Optional[str] = Field(None, max_length=255)

    @field_validator("title")
    @classmethod
    def validate_non_blank_title(cls, v: str) -> str:
        s = v.strip()
        if not s:
            raise ValueError("Book title cannot be blank or whitespace-only")
        return s
    author: Optional[str] = Field("AI Academic Press", max_length=100)
    academic_level: Optional[str] = Field("University / Reference", max_length=50)
    target_audience: Optional[str] = Field("Undergraduate & Graduate", max_length=100)
    subject: Optional[str] = Field(None, max_length=255)
    writing_depth: Optional[str] = Field("Detailed", description="Concise | Standard | Detailed | Deep Academic | Reference")
    research_depth: Optional[str] = Field("Standard", description="None | Basic | Standard | Deep")
    language: Optional[str] = Field("en", max_length=10)
    citation_style: Optional[str] = Field("IEEE", max_length=20)
    generate_images: bool = False
    include_diagrams: bool = True
    include_numericals: bool = False
    include_questions: bool = False
    include_examples: bool = True
    include_references: bool = True
    api_key: Optional[str] = None
    toc: TableOfContentsSchema

    @field_validator("writing_depth")
    @classmethod
    def validate_depth(cls, v):
        valid_depths = {"Concise", "Standard", "Detailed", "Deep Academic", "Reference"}
        if v not in valid_depths:
            return "Detailed"
        return v

    @field_validator("research_depth")
    @classmethod
    def validate_research_depth(cls, v):
        valid = {"None", "Basic", "Standard", "Deep"}
        if v not in valid:
            return "Standard"
        return v

class EstimationResponse(BaseModel):
    total_units: int
    total_topics: int
    total_subtopics: int
    estimated_words: int
    estimated_pages: int
    estimated_ai_requests: int
    estimated_image_requests: int
    estimated_minutes: int

class JobResponse(BaseModel):
    id: str
    book_id: str
    status: str
    progress: float
    current_stage: str
    current_item: Optional[str] = None
    error: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    download_url: Optional[str] = None

class EventResponse(BaseModel):
    id: str
    job_id: str
    event_type: str
    message: str
    progress: Optional[float] = None
    created_at: datetime

class QualityReportResponse(BaseModel):
    book_id: str
    title: str
    content_completeness: float
    structure_consistency: float
    terminology_consistency: float
    section_coverage: float
    formatting_validation: float
    overall_score: float
    total_words: int
    total_chapters: int
    total_sections: int
    total_figures: int
    total_tables: int
    warnings: List[str]
