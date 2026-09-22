import pytest
from backend.app.services.ai.mock_provider import MockAIProvider
from backend.app.agents.book_context_manager import BookContextManager
from backend.app.agents.chapter_depth_controller import ChapterDepthController
from backend.app.agents.content_writer import ContentWriter
from backend.app.agents.review_agent import ReviewAgent
from backend.app.agents.consistency_auditor import ConsistencyAuditor

@pytest.mark.asyncio
async def test_content_writer_generation():
    ai = MockAIProvider()
    context_mgr = BookContextManager("Machine Learning Systems")
    writer = ContentWriter(ai)

    section_text = await writer.write_subtopic_section(
        book_title="Machine Learning Systems",
        unit_title="Unit 1: Supervised Learning",
        topic_title="Gradient Descent Optimization",
        subtopic_title="Stochastic vs Batch Gradient Descent",
        context_manager=context_mgr,
        writing_depth="Detailed"
    )

    assert section_text is not None
    assert len(section_text) > 200
    assert "Gradient Descent" in section_text

@pytest.mark.asyncio
async def test_context_manager_tracking():
    context_mgr = BookContextManager("Distributed Computing")
    assert context_mgr.book_title == "Distributed Computing"

    context_mgr.add_terminology("Paxos", "Consensus protocol across unreliable networks")
    context_mgr.add_terminology("Raft", "Understandable consensus algorithm")

    assert "Paxos" in context_mgr.terminology
    assert "Raft" in context_mgr.terminology

    context_mgr.record_section_summary(
        "Unit 1", "Consensus Algorithms", "Overview",
        "Discussed Paxos and Raft protocols and quorum requirements."
    )
    prompt_ctx = context_mgr.get_hierarchical_context("Unit 2", "Topic 1")
    assert "Paxos" in prompt_ctx

@pytest.mark.asyncio
async def test_review_agent_scoring():
    ai = MockAIProvider()
    reviewer = ReviewAgent(ai)

    sample_content = """
    # Gradient Descent Optimization
    Gradient descent is a first-order iterative optimization algorithm for finding a local minimum of a differentiable function.
    ## Mathematical Formulation
    The weight update rule is given by:
    $$w_{t+1} = w_t - \\eta \\nabla L(w_t)$$
    ## Worked Example
    Consider a single variable objective function f(x) = x^2.
    """

    res = await reviewer.review_section(
        book_title="Machine Learning",
        subtopic_title="Optimization",
        content=sample_content,
        target_word_count=1500
    )

    assert res is not None
    assert "overall_score" in res
    assert res["overall_score"] >= 80
    assert res["rewrite_required"] is False

@pytest.mark.asyncio
async def test_consistency_auditor():
    ai = MockAIProvider()
    auditor = ConsistencyAuditor(ai)
    context_mgr = BookContextManager("Quantum Algorithms")
    context_mgr.add_terminology("Qubit", "Quantum bit superposition state")

    sample_content = "Each qubit is represented on the Bloch sphere."
    audit_res = await auditor.audit_and_update(sample_content, context_mgr)
    assert audit_res is not None
    assert audit_res.get("is_consistent", True) is True
