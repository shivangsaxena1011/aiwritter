"""
AIWritter — Specialized Academic Publishing Agents
"""

from backend.app.agents.base import BaseAgent, AgentContext, AgentResult
from backend.app.agents.syllabus_analysis_agent import SyllabusAnalysisAgent
from backend.app.agents.topic_decomposition_agent import TopicDecompositionAgent
from backend.app.agents.research_agent import ResearchAgent
from backend.app.agents.content_planning_agent import ContentPlanningAgent
from backend.app.agents.content_writer_agent import ContentWriterAgent
from backend.app.agents.derivation_agent import DerivationAgent
from backend.app.agents.diagram_prompt_agent import DiagramPromptAgent
from backend.app.agents.diagram_system import (
    DiagramPlanner, DiagramGenerator, DiagramPlannerAgent, DiagramGeneratorAgent
)
from backend.app.agents.review_agent import ReviewAgent, ContentReviewAgent
from backend.app.agents.fact_check_agent import FactCheckAgent
from backend.app.agents.consistency_auditor import ConsistencyAuditor, BookConsistencyAgent
from backend.app.agents.book_context_manager import BookContextManager
from backend.app.agents.chapter_depth_controller import ChapterDepthController
from backend.app.agents.quality_controller import QualityController
from backend.app.agents.document_structure_agent import DocumentStructureAgent
from backend.app.agents.document_validation_agent import DocumentValidationAgent
from backend.app.agents.toc_planner import TOCPlanner
from backend.app.agents.content_writer import ContentWriter
from backend.app.agents.subject_knowledge_model import SubjectKnowledgeModel
from backend.app.agents.topic_classifier import TopicTypeClassifier, TopicType
from backend.app.agents.equation_validation_agent import EquationValidationAgent, EquationValidationResult
from backend.app.agents.repetition_detection_agent import RepetitionDetectionAgent
from backend.app.agents.book_terminology_registry import BookTerminologyRegistry
from backend.app.agents.academic_content_quality_agent import AcademicContentQualityAgent, ContentQualityMetrics
from backend.app.agents.book_fact_check_agent import BookFactCheckAgent

__all__ = [
    "BaseAgent",
    "AgentContext",
    "AgentResult",
    "SyllabusAnalysisAgent",
    "TopicDecompositionAgent",
    "ResearchAgent",
    "ContentPlanningAgent",
    "ContentWriterAgent",
    "DerivationAgent",
    "DiagramPromptAgent",
    "DiagramPlanner",
    "DiagramGenerator",
    "DiagramPlannerAgent",
    "DiagramGeneratorAgent",
    "ReviewAgent",
    "ContentReviewAgent",
    "FactCheckAgent",
    "ConsistencyAuditor",
    "BookConsistencyAgent",
    "BookContextManager",
    "ChapterDepthController",
    "QualityController",
    "DocumentStructureAgent",
    "DocumentValidationAgent",
    "TOCPlanner",
    "ContentWriter",
    "SubjectKnowledgeModel",
    "TopicTypeClassifier",
    "TopicType",
    "EquationValidationAgent",
    "EquationValidationResult",
    "RepetitionDetectionAgent",
    "BookTerminologyRegistry",
    "AcademicContentQualityAgent",
    "ContentQualityMetrics",
    "BookFactCheckAgent"
]
