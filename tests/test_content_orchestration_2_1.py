import pytest
import os
import tempfile
import docx
from docx import Document

from backend.app.agents.syllabus_analysis_agent import SyllabusAnalysisAgent
from backend.app.agents.repetition_detector_2 import RepetitionDetector2
from backend.app.services.document.book_assembly_model import (
    BookAssemblyModel,
    AssemblyChapter,
    AssemblyTopic,
    AssemblySection,
    AssemblyFrontMatter,
    AssemblyBackMatter
)
from backend.app.services.document.docx_engine import DOCXExporter
from backend.app.services.document.artifact_integrity import (
    CountManifest,
    ArtifactIntegrityManifest,
    IntegrityAuditResult
)
from backend.app.services.document.final_docx_auditor import FinalDocxAuditor


class TestContentOrchestration21:
    """Rigorous negative and positive regression test suite for Content Orchestration 2.1."""

    def test_preamble_metadata_not_promoted_to_topic_or_chapter(self):
        """Negative test: Preamble metadata like 'B.Tech First Year — Engineering Physics'
        must NEVER become a chapter or a topic."""
        syllabus_text = """
B.Tech First Year — Engineering Physics
Semester 1 & 2 Core Curriculum

Chapter 1: Quantum Mechanics
1. Wave-particle duality and de Broglie hypothesis
2. Davisson-Germer experiment and matter wave verification
3. Wave packets, phase velocity, and group velocity
4. Heisenberg uncertainty principle and physical applications
"""
        agent = SyllabusAnalysisAgent()
        result = agent.analyze_deterministic(syllabus_text)

        # Must have exactly 1 chapter: Quantum Mechanics
        assert len(result["chapters"]) == 1
        ch = result["chapters"][0]
        assert "Quantum Mechanics" in ch["title"]
        assert "B.Tech" not in ch["title"]

        # Check topics: None may contain B.Tech or metadata
        topic_names = [(t.get("title") or t.get("name") if isinstance(t, dict) else t) for t in ch["topics"]]
        for t_name in topic_names:
            assert "B.Tech" not in t_name
            assert "Semester" not in t_name
            assert "Curriculum" not in t_name
        assert len(topic_names) == 4

    def test_consecutive_duplicate_heading_detection_and_rejection(self):
        """Negative test: A DOCX containing consecutive duplicate headings must fail publication gate."""
        with tempfile.TemporaryDirectory() as tmpdir:
            bad_docx_path = os.path.join(tmpdir, "bad_duplicate_heading.docx")
            doc = Document()
            doc.add_heading("Quantum Mechanics", level=1)
            doc.add_heading("De Broglie Hypothesis", level=3)
            doc.add_heading("De Broglie Hypothesis", level=3)  # Duplicate!
            doc.add_paragraph("This is connected academic prose discussing matter waves and particle wavelengths.")
            doc.save(bad_docx_path)

            auditor = FinalDocxAuditor(subject="Engineering Physics")
            res = auditor.audit(bad_docx_path)

            assert res["publication_ready"] is False
            assert len(res["heading_audit"]["consecutive_duplicates"]) > 0
            assert any("consecutive duplicate" in r.lower() for r in res["blocking_reasons"])

    def test_generic_fallback_heading_detection_and_rejection(self):
        """Negative test: Headings like 'Section 1' or 'Subtopic 2' must fail the audit."""
        with tempfile.TemporaryDirectory() as tmpdir:
            bad_docx_path = os.path.join(tmpdir, "bad_generic_heading.docx")
            doc = Document()
            doc.add_heading("Quantum Mechanics", level=1)
            doc.add_heading("Section 1", level=3)  # Generic fallback!
            doc.add_paragraph("Prose paragraph describing the quantum wave function formulation.")
            doc.save(bad_docx_path)

            auditor = FinalDocxAuditor(subject="Engineering Physics")
            res = auditor.audit(bad_docx_path)

            assert res["publication_ready"] is False
            assert len(res["heading_audit"]["generic_headings"]) > 0
            assert any("generic fallback" in r.lower() for r in res["blocking_reasons"])

    def test_count_reconciliation_detects_mismatch(self):
        """Negative test: ArtifactIntegrityManifest must flag discrepancies if planned != assembled or assembled != rendered."""
        planned = CountManifest(chapters=1, topics=4, sections=8, tables=2, figures=1)
        assembled = CountManifest(chapters=1, topics=4, sections=8, tables=2, figures=1)
        rendered_docx = CountManifest(chapters=1, topics=3, sections=8, tables=2, figures=1)  # Missing topic!

        manifest = ArtifactIntegrityManifest(planned=planned, assembled=assembled, rendered_docx=rendered_docx)
        audit_res = manifest.reconcile()

        assert audit_res.is_valid is False
        assert any("Topic count mismatch" in d for d in audit_res.discrepancies)

    def test_assembly_model_integrity_validation_duplicate_ids(self):
        """Negative test: BookAssemblyModel.validate_integrity must catch duplicate IDs or missing titles."""
        sec1 = AssemblySection(section_id="sec_dup", title="Topic A", purpose="Concept", content="Valid text.")
        sec2 = AssemblySection(section_id="sec_dup", title="Topic B", purpose="Concept", content="Valid text.")
        top1 = AssemblyTopic(topic_id="top_1", title="Topic 1", position=1, sections=[sec1, sec2])
        ch1 = AssemblyChapter(chapter_id="ch_1", title="Chapter 1", position=1, topics=[top1])

        model = BookAssemblyModel(
            front_matter=AssemblyFrontMatter(title="Test Book"),
            chapters=[ch1]
        )

        issues = model.validate_integrity()
        assert len(issues) > 0
        assert any("Duplicate section ID" in issue for issue in issues)

    def test_repetition_rate_bounding_and_audit(self):
        """Test: RepetitionDetector2 rate must be bounded between 0.0 and 1.0."""
        detector = RepetitionDetector2(near_threshold=0.70, min_word_count=10)
        p1 = "The Schrödinger wave equation governs the spatial and temporal evolution of quantum matter waves."

        # Register first
        detector.register_paragraph(p1, "Section 1")

        # Evaluate duplicate candidates
        for i in range(15):
            res = detector.check_candidate(p1, f"Section {i+2}")
            assert res.is_duplicate is True

        summary = detector.get_summary()
        assert 0.0 <= summary["exact_duplicate_rate"] <= 1.0
        assert summary["total_candidates_evaluated"] == 15
        assert summary["exact_duplicates_detected"] == 15
        assert summary["exact_duplicate_rate"] == 1.0

    def test_legitimate_repeated_terminology_passes_without_false_flagging(self):
        """Positive test: Repeating domain terms ('Schrödinger equation', 'wave function') in distinct pedagogical contexts passes."""
        detector = RepetitionDetector2(near_threshold=0.75, min_word_count=15)
        p1 = ("In the historical development of modern quantum mechanics, the Schrödinger equation "
              "emerged from Louis de Broglie's pioneering hypothesis regarding matter waves and "
              "the wave nature of moving atomic particles.")
        p2 = ("From a rigorous mathematical perspective, the time-dependent Schrödinger equation "
              "represents a linear partial differential equation describing the state vector's "
              "unitary time translation in an abstract Hilbert space.")

        detector.register_paragraph(p1, "Historical Context")
        res = detector.check_candidate(p2, "Mathematical Formulation")

        # Must NOT be flagged as duplicate
        assert res.is_duplicate is False

    def test_docx_exporter_strips_duplicate_headings(self):
        """Positive test: DOCXExporter strips markdown headings matching subtopic so Word has ZERO duplicate headings."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_docx = os.path.join(tmpdir, "test_clean_headings.docx")

            exporter = DOCXExporter()
            toc_data = {
                "units": [
                    {
                        "name": "Chapter 1: Quantum Mechanics",
                        "topics": [
                            {
                                "name": "Wave Mechanics",
                                "subtopics": ["De Broglie Hypothesis"]
                            }
                        ]
                    }
                ]
            }

            # Content has markdown heading that duplicates subtopic title!
            content_with_redundant_heading = (
                "### De Broglie Hypothesis\n\n"
                "The de Broglie hypothesis asserts that every moving particle is associated with a matter wave.\n\n"
                "#### Experimental Verification\n\n"
                "The Davisson-Germer experiment quantitatively demonstrated electron diffraction through nickel crystals."
            )

            sections = [
                {
                    "unit": "Chapter 1: Quantum Mechanics",
                    "topic": "Wave Mechanics",
                    "subtopic": "De Broglie Hypothesis",
                    "is_first_in_topic": True,
                    "content": content_with_redundant_heading,
                    "word_count": 40
                }
            ]

            exporter.export(
                book_title="Engineering Physics",
                subtitle="Quantum Foundations",
                author="Academic Press",
                academic_level="B.Tech First Year",
                toc_data=toc_data,
                sections=sections,
                assets=[],
                output_path=out_docx
            )

            auditor = FinalDocxAuditor(subject="Engineering Physics")
            audit_res = auditor.audit(out_docx)

            # ZERO consecutive duplicate headings!
            assert len(audit_res["heading_audit"]["consecutive_duplicates"]) == 0
            assert "De Broglie Hypothesis" in audit_res["heading_audit"]["subtopic_headings"]

    def test_export_assembly_model_roundtrip_integrity(self):
        """Positive test: Exporting BookAssemblyModel and reopening passes count reconciliation and audit."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_docx = os.path.join(tmpdir, "assembly_model_test.docx")

            sec1 = AssemblySection(
                section_id="sec_qm_1",
                title="De Broglie Matter Waves",
                purpose="Theoretical foundations",
                content=(
                    "The de Broglie hypothesis represents a foundational milestone in twentieth-century physics. "
                    "According to this principle, any entity with relativistic momentum $p = mv$ possesses an associated "
                    "matter wavelength given by $\\lambda = \\frac{h}{p}$. This duality resolves inconsistencies in the photoelectric effect."
                ),
                is_first_in_topic=True
            )
            top1 = AssemblyTopic(
                topic_id="top_qm_1",
                title="Wave-Particle Duality",
                position=1,
                sections=[sec1]
            )
            ch1 = AssemblyChapter(
                chapter_id="ch_qm_1",
                title="Chapter 1: Quantum Mechanics",
                position=1,
                topics=[top1]
            )
            assembly_model = BookAssemblyModel(
                front_matter=AssemblyFrontMatter(
                    title="Principles of Quantum Mechanics",
                    subtitle="A Rigorous Introduction",
                    author="Physics Department",
                    academic_level="Undergraduate"
                ),
                chapters=[ch1]
            )

            exporter = DOCXExporter()
            exporter.export_assembly_model(assembly_model, out_docx)

            auditor = FinalDocxAuditor(subject="Physics")
            audit_res = auditor.audit(
                out_docx,
                planned_manifest=CountManifest(chapters=1, topics=1, sections=1),
                assembly_model=assembly_model
            )

            assert audit_res["publication_ready"] is True
            assert audit_res["reconciliation"]["is_valid"] is True
            assert audit_res["reconciliation"]["reconciliation_table"]["chapters"]["match"] is True
            assert audit_res["reconciliation"]["reconciliation_table"]["topics"]["match"] is True
            assert audit_res["reconciliation"]["reconciliation_table"]["sections"]["match"] is True
