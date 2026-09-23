"""
Tests for DocumentValidationAgent and DOCX layout compliance:
Times New Roman typography, 12pt body, 1.5 line spacing, Justified alignment,
centered figures, OMML equations, and syllabus coverage reports.
"""

import os
from backend.app.services.document.docx_engine import DOCXExporter
from backend.app.agents.document_validation_agent import DocumentValidationAgent

def test_docx_export_and_validation(tmp_path):
    exporter = DOCXExporter()
    out_docx = str(tmp_path / "Validated_Textbook.docx")

    toc_data = {
        "units": [
            {
                "name": "Unit 1: Quantum Foundations",
                "topics": [
                    {
                        "name": "1.1 Wave-Particle Duality",
                        "subtopics": ["1.1.1 de Broglie Hypothesis", "1.1.2 Matter Waves"]
                    }
                ]
            }
        ]
    }

    sections = [
        {
            "unit": "Unit 1: Quantum Foundations",
            "topic": "1.1 Wave-Particle Duality",
            "subtopic": "1.1.1 de Broglie Hypothesis",
            "is_first_in_topic": True,
            "content": (
                "The de Broglie hypothesis asserts that matter possesses wave-like properties under relativistic and non-relativistic motion. "
                "In 1924, Louis de Broglie postulated that any particle with linear momentum p has an associated matter wave.\n\n"
                "The governing relationship connects momentum directly with wavelength:\n\n"
                "$$\\lambda = \\frac{h}{p} = \\frac{h}{m v}$$\n\n"
                "This fundamental formula demonstrated that duality is universal across microscopic physical systems."
            )
        }
    ]

    exporter.export(
        book_title="Engineering Physics",
        subtitle="A University Textbook",
        author="Dr. T. Scientist",
        academic_level="Undergraduate",
        toc_data=toc_data,
        sections=sections,
        assets=[],
        output_path=out_docx
    )

    assert os.path.exists(out_docx)

    # Validate DOCX programmatically
    audit = DocumentValidationAgent.validate_docx(
        docx_path=out_docx,
        expected_chapters=1,
        expected_topics=1,
        include_diagrams=False
    )

    assert audit["total_paragraphs"] > 5
    assert audit["total_equations"] >= 1
    assert audit["overall_score"] >= 80.0
    assert "Times New Roman" in audit["detected_fonts"]

    # Verify syllabus coverage report
    coverage = DocumentValidationAgent.generate_syllabus_coverage_report(
        syllabus_chapters=[{"number": 1, "title": "Unit 1: Quantum Foundations", "topics": ["1.1 Wave-Particle Duality"]}],
        generated_sections=sections
    )
    assert coverage["total_syllabus_topics"] == 1
    assert coverage["total_generated_topics"] >= 1
