import pytest
from backend.app.agents.toc_planner import TOCPlanner
from backend.app.services.ai.mock_provider import MockAIProvider

@pytest.mark.asyncio
async def test_toc_parser_regex_numbered():
    mock_ai = MockAIProvider()
    planner = TOCPlanner(mock_ai)

    raw_text = """
    "Fuel Cell Technology: Powering the Future"

    1. *Chapter 1: Introduction to Fuel Cells*
        - Overview, History, and Types
    2. *Chapter 2: Fuel Cell Fundamentals*
        - Thermodynamics, Kinetics, and Electrochemistry
    """

    res = planner.parse_syllabus_regex(raw_text)
    assert res is not None
    assert "Fuel Cell Technology" in res["title"]
    assert len(res["units"]) == 2
    assert "Introduction to Fuel Cells" in res["units"][0]["name"]

    assert len(res["units"][0]["topics"]) >= 1

@pytest.mark.asyncio
async def test_toc_parser_regex_markdown():
    mock_ai = MockAIProvider()
    planner = TOCPlanner(mock_ai)

    raw_text = """
    # Advanced Quantum Computing
    ## Unit 1: Quantum Mechanics
    ### Topic 1.1: Superposition
    - Pure States and Density Matrices
    - Bloch Sphere Representation
    ## Unit 2: Quantum Algorithms
    ### Topic 2.1: Shor's Algorithm
    - Quantum Fourier Transform
    """

    res = planner.parse_syllabus_regex(raw_text)
    assert res is not None
    assert len(res["units"]) >= 1

@pytest.mark.asyncio
async def test_toc_planner_with_mock_ai():
    mock_ai = MockAIProvider()
    planner = TOCPlanner(mock_ai)

    res = await planner.plan_toc("Artificial Intelligence Ethics and Governance")
    assert res is not None
    assert "units" in res
    assert len(res["units"]) >= 1
    assert "topics" in res["units"][0]
    assert len(res["units"][0]["topics"]) >= 1

@pytest.mark.asyncio
async def test_toc_planner_empty_fallback():
    mock_ai = MockAIProvider()
    planner = TOCPlanner(mock_ai)

    res = await planner.plan_toc("")
    assert res is not None
    assert len(res["units"]) >= 1
    assert "Introduction" in res["units"][0]["name"]
