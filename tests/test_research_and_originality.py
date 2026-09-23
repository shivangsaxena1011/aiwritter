"""
Tests for ResearchAgent and WebResearchProvider:
Authoritative educational source gathering, bibliography generation,
prompt injection barriers, and originality auditing.
"""

import pytest
from backend.app.agents.research_agent import ResearchAgent
from backend.app.services.research.mock_research_provider import MockResearchProvider
from backend.app.services.research.base import ResearchSourceData

@pytest.mark.asyncio
async def test_research_gathering_and_bibliography():
    agent = ResearchAgent(research_provider=MockResearchProvider())
    res = await agent.research_topic(
        topic="Wave Nature of Particles",
        subject="Engineering Physics"
    )
    assert res.status == "success"
    assert len(res.sources) >= 1
    assert len(res.research_notes) >= 1

    # Check bibliography generation
    bib_ieee = agent.generate_bibliography_markdown("IEEE")
    assert "References" in bib_ieee
    assert "[1]" in bib_ieee

    bib_apa = agent.generate_bibliography_markdown("APA")
    assert "(" in bib_apa

def test_originality_audit_detects_synthesis_vs_copied_text():
    agent = ResearchAgent(research_provider=MockResearchProvider())
    sources = [
        ResearchSourceData(
            title="MIT Foundations",
            key_points=[
                "Spatial confinement imposes standing wave nodes at the boundaries dictating discrete energy states."
            ]
        )
    ]

    # Test completely original text
    original_text = (
        "In this analysis, the continuous potential well restricts the admissible states of the wave packet. "
        "As a result of Dirichlet boundary constraints, the mathematical solutions are quantized into distinct harmonics."
    )
    audit_original = agent.assess_originality(original_text, sources)
    assert audit_original["originality_score"] >= 90.0

    # Test verbatim duplicated sentence
    copied_text = (
        "Spatial confinement imposes standing wave nodes at the boundaries dictating discrete energy states. "
        "This is an exact copied sentence."
    )
    audit_copied = agent.assess_originality(copied_text, sources)
    assert audit_copied["verbatim_matches_found"] >= 1
