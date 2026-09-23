"""
Tests for DiagramPromptAgent, DefaultImageProvider, and Diagram System:
Academic black-and-white prompt generation, image validation,
deterministic plot generation, and chapter-aware captions.
"""

import os
import pytest
from backend.app.agents.diagram_prompt_agent import DiagramPromptAgent
from backend.app.services.image.image_provider import DefaultImageProvider
from backend.app.agents.diagram_system import DiagramPlannerAgent, DiagramGeneratorAgent
from backend.app.services.ai.mock_provider import MockProvider

def test_diagram_prompt_black_and_white_enforcement():
    prompt = DiagramPromptAgent.create_textbook_diagram_prompt(
        topic="One-Dimensional Potential Well",
        subject="Quantum Mechanics",
        concept_description="Particle confined between rigid infinite barriers at x=0 and x=L."
    )
    assert "white background" in prompt.lower()
    assert "black" in prompt.lower()
    assert "no cartoon" in prompt.lower()
    assert "high contrast" in prompt.lower()

def test_deterministic_technical_figure_generation(tmp_path):
    output_png = str(tmp_path / "test_schematic.png")
    success = DefaultImageProvider.generate_deterministic_technical_figure(
        output_path=output_png,
        topic_title="Wavefunction Spatial Probability Density"
    )
    assert success is True
    assert os.path.exists(output_png)
    assert os.path.getsize(output_png) > 1000
    assert DefaultImageProvider.validate_image(output_png) is True

@pytest.mark.asyncio
async def test_diagram_planner_chapter_aware_caption():
    ai = MockProvider()
    planner = DiagramPlannerAgent(ai_provider=ai)
    plan = await planner.plan_diagram(
        book_title="Engineering Physics",
        subtopic_title="Infinite Potential Well",
        section_content="The wavefunction satisfies Dirichlet boundary conditions.",
        chapter_idx=2,
        figure_idx=3
    )
    assert "Figure 2.3" in plan["caption"]
