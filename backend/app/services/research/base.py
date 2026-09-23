"""
ResearchProvider Interface for AIWritter Engine.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

class ResearchSourceData(BaseModel):
    title: str
    url: Optional[str] = None
    author: Optional[str] = None
    publisher: Optional[str] = None
    publication_date: Optional[str] = None
    accessed_date: Optional[str] = None
    source_type: str = "educational"  # university | textbook | paper | standard | web
    relevance: str = "High"
    key_points: List[str] = Field(default_factory=list)

class ResearchResult(BaseModel):
    topic: str
    sources: List[ResearchSourceData] = Field(default_factory=list)
    research_notes: List[str] = Field(default_factory=list)
    originality_guidelines: List[str] = Field(default_factory=list)
    status: str = "success"  # success | partial | failed | offline

class ResearchProvider(ABC):
    @abstractmethod
    async def conduct_research(
        self,
        topic: str,
        subject: str,
        depth: str = "Standard"
    ) -> ResearchResult:
        """Conducts research for a given academic topic and subject."""
        pass
