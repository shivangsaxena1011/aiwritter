"""
Audit Requirements Test Suite:
Validates Topic Decomposition, Formal Derivations, Switch Toggles (Numericals, Q&A, Diagrams),
and DOCX XML Inspection for OMML equations (<m:f>, <m:sSup>, <m:sSub>) and Word tables (<w:tbl>).
"""

import os
import zipfile
import pytest
from xml.etree import ElementTree

from backend.app.agents.topic_decomposition_agent import TopicDecompositionAgent
from backend.app.agents.derivation_agent import DerivationAgent
from backend.app.agents.content_writer_agent import ContentWriterAgent
from backend.app.agents.diagram_system import DiagramPlannerAgent
from backend.app.services.ai.mock_provider import MockProvider
from backend.app.services.document.docx_engine import DOCXExporter

@pytest.mark.asyncio
async def test_topic_decomposition_particle_in_a_box():
    mock_ai = MockProvider()
    agent = TopicDecompositionAgent(mock_ai)
    decomp = await agent.decompose_topic(
        topic_title="Particle in a Box",
        subject="Physics",
        academic_level="Undergraduate",
        requires_derivation=True,
        requires_numericals=True
    )
    sections = decomp.get("sections", [])
    assert len(sections) >= 4
    # Verify non-trivial pedagogical sections exist
    sec_titles = [s["title"] if isinstance(s, dict) else str(s) for s in sections]
    sec_text = " ".join(sec_titles).lower()
    assert any(term in sec_text for term in ["concept", "formulation", "derivation", "interpretation", "application", "boundary", "model"])

@pytest.mark.asyncio
async def test_derivation_structure_particle_in_a_box():
    mock_ai = MockProvider()
    agent = DerivationAgent(mock_ai)
    deriv = await agent.generate_derivation(
        topic="Quantum Mechanics",
        equation_name="Particle in a one-dimensional box",
        subject="Engineering Physics"
    )
    assert deriv.get("equation_title")
    steps = deriv.get("steps", [])
    assert len(steps) >= 3
    # Check that steps contain explanatory prose and LaTeX display equations
    for step in steps:
        assert step.get("explanatory_prose")
        assert step.get("latex_equation")

    final = deriv.get("final_result", {})
    assert final.get("latex_equation")
    assert final.get("physical_interpretation")

@pytest.mark.asyncio
async def test_numerical_switch_on_vs_off():
    mock_ai = MockProvider()
    writer = ContentWriterAgent(mock_ai)

    # 1. Switch = OFF
    content_off = await writer.write_section(
        book_title="Engineering Physics",
        subject="Engineering Physics",
        unit_title="Quantum Mechanics",
        topic_title="Wave Nature",
        subtopic_title="de Broglie Hypothesis",
        requires_derivation=False,
        include_numericals=False
    )
    assert "### Solved Numerical Example" not in content_off
    assert "Given:" not in content_off

    # 2. Switch = ON
    content_on = await writer.write_section(
        book_title="Engineering Physics",
        subject="Engineering Physics",
        unit_title="Quantum Mechanics",
        topic_title="Wave Nature",
        subtopic_title="de Broglie Hypothesis",
        requires_derivation=False,
        include_numericals=True
    )
    assert "Given" in content_on
    assert "Formula" in content_on
    assert "Substitution" in content_on
    assert "Calculation" in content_on
    assert "Answer" in content_on

@pytest.mark.asyncio
async def test_qa_switch_on_vs_off():
    mock_ai = MockProvider()
    writer = ContentWriterAgent(mock_ai)

    # 1. Switch = OFF
    content_off = await writer.write_section(
        book_title="Engineering Physics",
        subject="Engineering Physics",
        unit_title="Quantum Mechanics",
        topic_title="Wave Nature",
        subtopic_title="de Broglie Hypothesis",
        include_questions=False
    )
    assert "### Academic Review & Conceptual Questions" not in content_off

    # 2. Switch = ON
    content_on = await writer.write_section(
        book_title="Engineering Physics",
        subject="Engineering Physics",
        unit_title="Quantum Mechanics",
        topic_title="Wave Nature",
        subtopic_title="de Broglie Hypothesis",
        include_questions=True
    )
    assert "Questions" in content_on

@pytest.mark.asyncio
async def test_diagram_switch_on_vs_off():
    mock_ai = MockProvider()
    planner = DiagramPlannerAgent(mock_ai)

    # Test diagram decision
    plan = await planner.plan_diagram(
        book_title="Engineering Physics",
        subtopic_title="Particle in an Infinite Potential Well",
        section_content="The potential V(x) is zero inside the well and infinite outside. The wave functions form standing waves.",
        chapter_idx=1,
        figure_idx=1
    )
    assert plan.get("needs_diagram") is True
    assert "potential" in plan.get("description", "").lower() or "wave" in plan.get("description", "").lower()
    assert "Figure 1.1" in plan.get("caption", "")

def test_docx_xml_inspection_omml_and_tables(tmp_path):
    exporter = DOCXExporter()
    out_docx = str(tmp_path / "xml_audit.docx")

    sections = [
        {
            "unit": "Quantum Foundations",
            "topic": "Wave Nature",
            "subtopic": "de Broglie Wavelength",
            "content": """The de Broglie relation connects momentum to wavelength:

$$
\\lambda = \\frac{h}{p}
$$

The quantized energy states in a box of width L are given by:

$$
E_n = \\frac{n^2 \\pi^2 \\hbar^2}{2m L^2}
$$

| Energy State | Quantum Number n | Characteristic Wavelength |
|---|---|---|
| Ground State | 1 | 2L |
| First Excited | 2 | L |
"""
        }
    ]

    exporter.export(
        book_title="XML Inspection Monograph",
        subtitle="Verification Treatise",
        author="Academic Reviewer",
        academic_level="Undergraduate",
        toc_data={"units": [{"name": "Quantum Foundations", "topics": [{"name": "Wave Nature", "subtopics": ["de Broglie Wavelength"]}]}]},
        sections=sections,
        assets=[],
        output_path=out_docx
    )

    assert os.path.exists(out_docx)

    # Unpack docx and inspect word/document.xml
    with zipfile.ZipFile(out_docx, 'r') as zf:
        xml_content = zf.read("word/document.xml").decode("utf-8")

    # 1. Verify OMML fraction XML element <m:f>
    assert "m:f" in xml_content

    # 2. Verify OMML superscript XML element <m:sSup>
    assert "m:sSup" in xml_content

    # 3. Verify Word table XML element <w:tbl>
    assert "w:tbl" in xml_content

    # 4. Verify Times New Roman font declaration
    assert "Times New Roman" in xml_content

    # 5. Verify Justified paragraph alignment
    assert 'w:jc w:val="both"' in xml_content
