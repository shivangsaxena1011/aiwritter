"""
Tests for SyllabusAnalysisAgent:
Chapter detection, topic decomposition, requirement tagging (derivations, diagrams, numericals),
malformed syllabus handling, and zero topic omission.
"""

import pytest
from backend.app.agents.syllabus_analysis_agent import SyllabusAnalysisAgent

@pytest.mark.asyncio
async def test_syllabus_analysis_chapter_and_topic_detection():
    agent = SyllabusAnalysisAgent(ai_provider=None)
    syllabus_text = """
Book: Engineering Physics
Course: B.Tech First Year

Chapter 1: Quantum Mechanics
Major Topics:
1. Introduction to Quantum Mechanics
2. Wave Nature of Particles
3. Operators and Commutators
4. Time-dependent Schrödinger Equation
5. Time-independent Schrödinger Equation
6. Particle in a Box

Chapter 2: Solid State Physics
Major Topics:
1. Crystal Lattices and Unit Cells
2. Band Theory of Solids
"""
    result = await agent.analyze_syllabus(
        raw_text=syllabus_text,
        subject="Engineering Physics",
        include_numericals=True,
        include_diagrams=True
    )

    assert result["subject"] == "Engineering Physics"
    chapters = result["chapters"]
    assert len(chapters) == 2

    # Chapter 1 checks
    ch1 = chapters[0]
    assert "Quantum Mechanics" in ch1["title"]
    assert len(ch1["topics"]) == 6

    # Verify requirement tagging
    schrodinger_topic = next(t for t in ch1["topics"] if "Schrödinger" in t["title"])
    assert schrodinger_topic["requires_derivation"] is True

    wave_topic = next(t for t in ch1["topics"] if "Wave Nature" in t["title"])
    assert wave_topic["requires_diagram"] is True

@pytest.mark.asyncio
async def test_syllabus_analysis_zero_omission_on_malformed_input():
    agent = SyllabusAnalysisAgent(ai_provider=None)
    malformed_text = """
Random header line with no formatting
- Subtopic line alpha
- Subtopic line beta
Another loose topic
### Subsection gamma
"""
    result = await agent.analyze_syllabus(raw_text=malformed_text, subject="Test Subject")
    assert len(result["chapters"]) >= 1
    total_topics = sum(len(ch["topics"]) for ch in result["chapters"])
    assert total_topics >= 1

@pytest.mark.asyncio
async def test_syllabus_numericals_toggle_respected():
    agent = SyllabusAnalysisAgent(ai_provider=None)
    text = "Chapter 1: Mechanics\n1. Kinetic Energy and Momentum Calculation"

    # With numericals disabled
    res_no_num = await agent.analyze_syllabus(text, include_numericals=False)
    assert res_no_num["chapters"][0]["topics"][0]["requires_numericals"] is False

    # With numericals enabled
    res_with_num = await agent.analyze_syllabus(text, include_numericals=True)
    assert res_with_num["chapters"][0]["topics"][0]["requires_numericals"] is True
