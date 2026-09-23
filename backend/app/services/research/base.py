"""
ResearchProvider Interface for AIWritter Engine.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

from backend.app.services.research.research_models import ResearchSynthesis, ClaimEvidenceRecord

class ResearchSourceData(BaseModel):
    title: str
    url: Optional[str] = None
    author: Optional[str] = None
    publisher: Optional[str] = None
    publication_date: Optional[str] = None
    accessed_date: Optional[str] = None
    source_type: str = "educational"  # university | textbook | paper | standard | web | book | journal | conference | encyclopedia
    peer_review_status: str = "unknown"  # verified | unknown | not_applicable
    tier: int = Field(default=4, description="1=Gov/Univ/Standard, 2=Peer-reviewed, 3=Official docs, 4=Educational, 5=Encyclopedia, 6=General")
    tier_name: str = Field(default="Established educational resources")
    relevance: str = "High"
    key_points: List[str] = Field(default_factory=list)

class ResearchResult(BaseModel):
    topic: str
    sources: List[ResearchSourceData] = Field(default_factory=list)
    research_notes: List[str] = Field(default_factory=list)
    originality_guidelines: List[str] = Field(default_factory=list)
    synthesis: Optional[ResearchSynthesis] = None
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
