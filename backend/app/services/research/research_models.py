"""
ResearchModels — Structured representations for research synthesis,
claim-to-source traceability, and explicit source tier hierarchy.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class ClaimEvidenceRecord(BaseModel):
    """
    Tracks atomic factual/mathematical claims to supporting source evidence.
    Used internally for academic quality auditing and hallucination prevention.
    """
    claim: str
    topic: str
    supporting_sources: List[str] = Field(default_factory=list)
    evidence_type: str = "conceptual"  # "equation" | "experimental" | "definition" | "conceptual" | "application"
    confidence: str = "high"  # "high" | "medium" | "low"

class ResearchSynthesis(BaseModel):
    """
    Comprehensive research synthesis object produced BEFORE content planning and writing.
    Supplies the authoring pipeline with verified definitions, equations, historical context,
    applications, and source-to-claim mappings.
    """
    topic: str
    authoritative_definitions: List[str] = Field(default_factory=list)
    core_concepts: List[str] = Field(default_factory=list)
    important_equations: List[Dict[str, Any]] = Field(default_factory=list)
    derivations: List[Dict[str, Any]] = Field(default_factory=list)
    experimental_evidence: List[str] = Field(default_factory=list)
    historical_context: List[str] = Field(default_factory=list)
    applications: List[str] = Field(default_factory=list)
    limitations: List[str] = Field(default_factory=list)
    misconceptions: List[str] = Field(default_factory=list)
    terminology: Dict[str, str] = Field(default_factory=dict)
    source_claim_mapping: List[ClaimEvidenceRecord] = Field(default_factory=list)
    source_quality: Dict[str, Any] = Field(default_factory=dict)
    conflicting_claims: List[str] = Field(default_factory=list)
    unresolved_questions: List[str] = Field(default_factory=list)
