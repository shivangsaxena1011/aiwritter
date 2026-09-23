"""
Base Agent Interface and Contracts for AIWritter Engine.
Defines standard AgentContext, AgentResult, and BaseAgent abstractions.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

class AgentContext(BaseModel):
    book_id: str = ""
    job_id: Optional[str] = None
    book_title: str = "Academic Textbook"
    subject: Optional[str] = None
    academic_level: str = "University / Reference"
    target_audience: str = "Undergraduate & Graduate"
    writing_depth: str = "Detailed"
    research_depth: str = "Standard"
    include_numericals: bool = False
    include_questions: bool = False
    include_examples: bool = True
    include_references: bool = True
    include_diagrams: bool = True
    language: str = "en"
    citation_style: str = "IEEE"
    extra: Dict[str, Any] = Field(default_factory=dict)

class AgentResult(BaseModel):
    status: str = "success"  # success | partial | failed | warning
    data: Dict[str, Any] = Field(default_factory=dict)
    warnings: List[str] = Field(default_factory=list)
    errors: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    @property
    def is_success(self) -> bool:
        return self.status in ("success", "partial")

class BaseAgent(ABC):
    """Abstract base class for all specialized publication agents."""

    def __init__(self, ai_provider=None):
        self.ai = ai_provider

    @abstractmethod
    async def run(self, context: AgentContext, **kwargs) -> AgentResult:
        """Executes the agent task given the context and returns an AgentResult."""
        pass
