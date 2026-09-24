"""
Comprehensive Regression Test Suite for Content Orchestration 2.0.
Verifies blueprint contracts, topic boundary contracts, concept ownership,
elimination of generic derivations, table & diagram necessity gating,
3-level repetition detection, intermediate book assembly compilation,
adversarial review & publication gating, and dynamic front-matter toggle reflection.
"""

import pytest
from unittest.mock import AsyncMock
from docx import Document

from backend.app.agents.content_blueprint import (
    ContentBlueprintPlanner,
    SectionPurposeType,
    TopicBoundaryContract,
)
from backend.app.agents.concept_ownership_registry import (
    ConceptOwnershipRegistry,
    ConceptRecord,
    EquationRecord,
)
from backend.app.agents.topic_contamination_detector import (
    TopicContaminationDetector,
)
from backend.app.agents.derivation_agent import DerivationAgent
from backend.app.agents.table_planner import TablePlanner, TableNecessityDecision
from backend.app.agents.diagram_system import DiagramPlanner
from backend.app.agents.repetition_detector_2 import RepetitionDetector2
from backend.app.services.document.book_assembly_model import (
    BookAssemblyModel,
    AssemblyChapter,
    AssemblyTopic,
    AssemblySection,
    AssemblyFrontMatter,
    AssemblyBackMatter,
)
from backend.app.agents.adversarial_reviewer_agent import (
    AdversarialReviewerAgent,
    AdversarialIssue,
    AdversarialReviewResult,
)
from backend.app.services.document.docx_engine import DOCXExporter
from backend.app.agents.subject_knowledge_model import SubjectKnowledgeModel


class TestContentOrchestration2:
    """15 required regression tests for Content Orchestration 2.0."""

    # 1. Blueprint purpose uniqueness
    def test_blueprint_purpose_uniqueness(self):
        blueprint = ContentBlueprintPlanner.create_blueprint("de Broglie Hypothesis")
        purposes = [s.purpose for s in blueprint.section_plan]
        # In de Broglie hypothesis, all 5 subtopic purposes are distinct:
        # HISTORICAL_MOTIVATION, CORE_CONCEPT, DERIVATION, EXPERIMENTAL_EVIDENCE, APPLICATION
        assert len(purposes) == len(set(purposes)), f"Duplicate purposes found in blueprint: {purposes}"
        assert SectionPurposeType.HISTORICAL_MOTIVATION in purposes
        assert SectionPurposeType.DERIVATION in purposes

    # 2. Boundary contract enforcement
    def test_boundary_contract_enforcement(self):
        detector = TopicContaminationDetector()
        boundary = TopicBoundaryContract(
            topic_id="qm_photoelectric",
            topic_title="Photoelectric Effect",
            allowed_concepts=["work function", "stopping potential", "Einstein relation"],
            forbidden_concepts=["population inversion", "stimulated emission", "optical resonator"]
        )
        clean_para = "In the photoelectric effect, photons transfer their energy to bound electrons, overcoming the work function."
        res_clean = detector.check_paragraph(clean_para, boundary.topic_title, forbidden_concepts=boundary.forbidden_concepts)
        assert not res_clean.is_contaminated
        assert res_clean.verdict == "clean"

        contaminated_para = "The electrons undergo population inversion within an optical resonator to amplify light."
        res_bad = detector.check_paragraph(contaminated_para, boundary.topic_title, forbidden_concepts=boundary.forbidden_concepts)
        assert res_bad.is_contaminated
        assert res_bad.verdict == "rejected"
        assert any("population inversion" in item.lower() for item in res_bad.forbidden_terms_found + res_bad.irrelevant_physics_detected)

    # 3. Subtopic independence
    def test_subtopic_independence(self):
        # Different subtopics of Particle in a 1D Box should produce focused, distinct content
        sec_intro = SubjectKnowledgeModel.generate_academic_section(
            topic="Particle in a 1D Box",
            subtopic="Physical Model and Boundary Conditions",
            subject="Engineering Physics"
        )
        sec_derivation = SubjectKnowledgeModel.generate_academic_section(
            topic="Particle in a 1D Box",
            subtopic="Derivation of Energy Eigenvalues and Normalization",
            subject="Engineering Physics"
        )
        assert "infinite potential well" in sec_intro or "boundary conditions" in sec_intro
        assert "\\psi(0) = 0" in sec_intro or "\\psi_n(x)" in sec_intro
        # The derivation subtopic specifically focuses on energy quantization
        assert "E_n = \\frac{n^2 h^2}{8mL^2}" in sec_derivation or "8mL^2" in sec_derivation
        # They should have distinct opening sentences and distinct content slices
        assert sec_intro[:100] != sec_derivation[:100]

    # 4. Concept ownership single primary
    def test_concept_ownership_single_primary(self):
        registry = ConceptOwnershipRegistry()
        registry.register_concept(
            concept_id="c_box_energy",
            name="Infinite Well Quantized Energy",
            primary_topic="Particle in a 1D Box",
            secondary_topics=["Quantum Technologies", "Wave Nature of Particles"],
            allowed_reuse_mode="SUMMARY"
        )

        owner_policy = registry.get_concept_policy("Infinite Well Quantized Energy", "Particle in a 1D Box")
        assert owner_policy["is_owner"] is True
        assert owner_policy["mode"] == "FULL"

        secondary_policy = registry.get_concept_policy("Infinite Well Quantized Energy", "Quantum Technologies")
        assert secondary_policy["is_owner"] is False
        assert secondary_policy["mode"] == "SUMMARY"

    # 5. Forbidden derivations eliminated
    def test_forbidden_derivations_eliminated(self):
        agent = DerivationAgent(ai_provider=AsyncMock())
        # Generic diffusion equation should NOT produce any steps or derivations
        deriv_diff = agent._canonical_derivation("Diffusion", "Diffusion Equation", "Engineering Physics")
        assert deriv_diff["steps"] == []
        assert "\\dot{S}_{gen}" not in deriv_diff["markdown_content"]
        assert "Configuration Alpha" not in deriv_diff["markdown_content"]

        # Only subject-grounded quantum derivations should produce valid steps
        d_qm = agent._canonical_derivation("de Broglie Hypothesis", "lambda = h/p", "Engineering Physics")
        assert len(d_qm["steps"]) > 0
        assert "\\lambda" in d_qm["final_result"]["latex_equation"]
        assert "\\dot{S}_{gen}" not in d_qm["markdown_content"]

        d_box = agent._canonical_derivation("Particle in a 1D Box", "Energy Eigenvalues", "Engineering Physics")
        assert len(d_box["steps"]) > 0
        assert "8mL^2" in d_box["final_result"]["latex_equation"] or "8m L^2" in d_box["final_result"]["latex_equation"]

    # 6. Table necessity rejection
    def test_table_necessity_rejection(self):
        decision = TablePlanner.evaluate_necessity(
            subtopic_title="Physical Interpretation of the Wavefunction",
            topic_title="Wave Function and Born Interpretation",
            purpose="PHYSICAL_INTERPRETATION",
            section_content="Born proposed that the square of the wavefunction represents probability density..."
        )
        assert not decision.needs_table
        assert not decision.is_necessary
        assert "connected academic prose" in decision.reason

    # 7. Table necessity acceptance
    def test_table_necessity_acceptance(self):
        # 1. Phase vs Group Velocity
        dec1 = TablePlanner.evaluate_necessity(
            subtopic_title="Mathematical Relation Between Phase and Group Velocity",
            topic_title="Phase Velocity and Group Velocity",
            purpose="COMPARISON"
        )
        assert dec1.needs_table
        assert dec1.table_type == "COMPARISON"
        assert len(dec1.candidate_entities) >= 3
        assert dec1.markdown_content is not None
        assert "Propagation Regime" in dec1.markdown_content

        # 2. de Broglie macroscopic vs microscopic scales
        dec2 = TablePlanner.evaluate_necessity(
            subtopic_title="Scale Comparison of Matter Waves",
            topic_title="de Broglie Hypothesis",
            purpose="COMPARISON"
        )
        assert dec2.needs_table
        assert len(dec2.candidate_entities) >= 4
        assert "Cricket Ball" in dec2.markdown_content

    # 8. Diagram planner necessity and deduplication
    @pytest.mark.asyncio
    async def test_diagram_planner_necessity(self):
        mock_ai = AsyncMock()
        mock_ai.generate_structured.return_value = {
            "needs_diagram": True,
            "caption": "Schematic of Experimental Setup",
            "diagram_type": "schematic"
        }
        planner = DiagramPlanner(ai_provider=mock_ai)

        # First subtopic in topic gets diagram
        plan1 = await planner.plan_diagram(
            book_title="Engineering Physics",
            subtopic_title="Experimental Setup of Davisson-Germer",
            section_content="The electron beam from a tungsten filament strikes a nickel crystal...",
            parent_topic="de Broglie Hypothesis"
        )
        assert plan1["needs_diagram"] is True
        assert "de broglie hypothesis" in planner.illustrated_topics

        # Second subtopic in SAME topic should be rejected to prevent diagram explosion
        plan2 = await planner.plan_diagram(
            book_title="Engineering Physics",
            subtopic_title="G. P. Thomson Diffraction Analysis",
            section_content="Diffraction rings formed on photographic plates...",
            parent_topic="de Broglie Hypothesis"
        )
        assert plan2["needs_diagram"] is False
        assert "already visually illustrated" in plan2["reason"]

        # Explicitly disabled by blueprint
        plan3 = await planner.plan_diagram(
            book_title="Engineering Physics",
            subtopic_title="Mathematical Operator Properties",
            section_content="Hermitian operators have real eigenvalues...",
            parent_topic="Operators",
            blueprint_diagram_required=False
        )
        assert plan3["needs_diagram"] is False
        assert "Blueprint specifies no diagram" in plan3["reason"]

    # 9. Repetition detector exact duplicate (Level 1)
    def test_repetition_detector_exact_duplicate(self):
        detector = RepetitionDetector2()
        text = "The de Broglie hypothesis asserts that any particulate matter with momentum p possesses an intrinsic pilot wavelength lambda = h/p."
        detector.register_paragraph(text, "Chapter 1 > Section 1")

        check = detector.check_candidate(text, "Chapter 1 > Section 2")
        assert check.is_duplicate is True
        assert check.duplicate_level == "EXACT"
        assert check.similarity_score == 1.0
        assert check.matching_location == "Chapter 1 > Section 1"

    # 10. Repetition detector near duplicate (Level 2)
    def test_repetition_detector_near_duplicate(self):
        detector = RepetitionDetector2(near_threshold=0.70)
        p1 = "Under the de Broglie postulate every material entity carrying linear momentum p exhibits an associated pilot wave of wavelength lambda equal to Planck constant divided by momentum."
        detector.register_paragraph(p1, "Chapter 1 > Section 1")

        # Slight rephrasing with high token overlap (> 70%)
        p2 = "Under the de Broglie postulate every material particle carrying linear momentum p exhibits an associated pilot wave of wavelength lambda equal to Planck constant divided by momentum."
        check = detector.check_candidate(p2, "Chapter 1 > Section 2")
        assert check.is_duplicate is True
        assert check.duplicate_level == "NEAR"
        assert check.similarity_score >= 0.70

    # 11. Repetition detector conceptual duplicate (Level 3)
    def test_repetition_detector_conceptual_duplicate(self):
        detector = RepetitionDetector2(near_threshold=0.85)  # High near threshold so near doesn't catch it
        p1 = "For a particle in a one-dimensional box, the normalized eigenfunction is $\\psi_n(x) = \\sqrt{\\frac{2}{L}} \\sin\\left(\\frac{n \\pi x}{L}\\right)$ with energies $E_n = \\frac{n^2 h^2}{8mL^2}$."
        detector.register_paragraph(p1, "Chapter 1 > Section 3.1")

        # Rephrased wording with the exact same two core equations
        p2 = "The bound quantum particle within an infinite potential well has stationary state $\\psi_n(x) = \\sqrt{\\frac{2}{L}} \\sin\\left(\\frac{n \\pi x}{L}\\right)$ yielding quantized spectrum $E_n = \\frac{n^2 h^2}{8mL^2}$."
        check = detector.check_candidate(p2, "Chapter 1 > Section 3.3")
        assert check.is_duplicate is True
        assert check.duplicate_level == "CONCEPTUAL"
        assert "shared equations" in check.details.lower() or "conceptual duplicate" in check.details.lower()

    # 12. Intermediate assembly model compilation
    def test_assembly_model_compilation(self):
        front_matter = AssemblyFrontMatter(
            title="Engineering Physics",
            subtitle="Quantum Mechanics Volume",
            author="Academic Press",
            academic_level="Undergraduate",
            preface="Standard preface."
        )
        sec1 = AssemblySection(
            section_id="sec_1",
            title="Matter Waves Postulate",
            purpose="CORE_CONCEPT",
            content="Matter behaves with dual wave-particle characteristics.",
            word_count=50,
            table_markdown="| Col 1 | Col 2 |\n| --- | --- |\n| A | B |"
        )
        topic1 = AssemblyTopic(
            topic_id="top_1",
            title="de Broglie Hypothesis",
            position=1,
            sections=[sec1]
        )
        ch1 = AssemblyChapter(
            chapter_id="ch_1",
            title="Chapter 1: Quantum Mechanics",
            position=1,
            introduction="Introductory overview of quantum physics.",
            topics=[topic1]
        )
        model = BookAssemblyModel(
            front_matter=front_matter,
            chapters=[ch1],
            back_matter=AssemblyBackMatter(bibliography="1. de Broglie (1924)")
        )

        compiled = model.to_compiled_sections()
        assert len(compiled) == 3  # 1 chapter overview + 1 topic section + 1 bibliography back matter
        assert compiled[0]["is_unit_overview"] is True
        assert compiled[0]["unit"] == "Chapter 1: Quantum Mechanics"
        assert compiled[1]["topic"] == "de Broglie Hypothesis"
        assert compiled[1]["subtopic"] == "Matter Waves Postulate"
        assert compiled[1]["table_markdown"] is not None
        assert compiled[2]["unit"] == "References"
        assert compiled[2]["topic"] == "Academic Bibliography"

    # 13. Adversarial reviewer catches contamination
    def test_adversarial_reviewer_catches_contamination(self):
        reviewer = AdversarialReviewerAgent()
        contaminated_sections = [
            {
                "topic": "Photoelectric Effect",
                "subtopic": "Experimental Observations",
                "content": "The stopping potential varies linearly with incident frequency. Configuration Alpha produced 45% efficiency with \\dot{S}_{gen} diffusion."
            },
            {
                "topic": "Photoelectric Effect",
                "subtopic": "Threshold Frequency",
                "content": "Under intense optical resonator pumping, population inversion is observed in the emitter cathode."
            }
        ]
        result = reviewer.review_chapter(contaminated_sections, "Quantum Mechanics", "Physics")
        assert result.critical_count >= 2  # Configuration Alpha + \dot{S}_{gen}
        assert result.error_count >= 1     # population inversion contamination
        assert result.passed is False
        assert result.publication_ready is False

    # 14. Publication ready gate blocks on error
    def test_publication_ready_gate_blocks_on_error(self):
        reviewer = AdversarialReviewerAgent()
        clean_sections = [
            {
                "topic": "de Broglie Hypothesis",
                "subtopic": "Pilot Wave Concept",
                "content": "Louis de Broglie hypothesized in 1924 that particles of matter display wave-like properties with wavelength lambda = h/p."
            },
            {
                "topic": "Particle in a 1D Box",
                "subtopic": "Boundary Quantization",
                "content": "Confining a quantum particle to an infinite potential well yields discrete energy eigenstates through standing wave interference."
            }
        ]
        # Clean section pass
        clean_res = reviewer.review_chapter(clean_sections, "Quantum Mechanics", "Physics")
        assert clean_res.critical_count == 0
        assert clean_res.error_count == 0
        assert clean_res.publication_ready is True

        # Repeated opening sentences across sections must block publication readiness
        repeated_sentence_sections = [
            {
                "topic": "Topic A",
                "subtopic": "Sub A",
                "content": "Quantum mechanics provides the mathematical framework for understanding physical systems at atomic and molecular scales where classical laws break down completely."
            },
            {
                "topic": "Topic B",
                "subtopic": "Sub B",
                "content": "Quantum mechanics provides the mathematical framework for understanding physical systems at atomic and molecular scales where classical laws break down completely."
            }
        ]
        repeat_res = reviewer.review_chapter(repeated_sentence_sections, "Quantum Mechanics", "Physics")
        assert repeat_res.error_count >= 1
        assert repeat_res.publication_ready is False

    # 15. Dynamic front matter reflects toggles
    def test_dynamic_front_matter_reflects_toggles(self):
        doc = Document()
        exporter = DOCXExporter()

        # Config with numericals=OFF and questions=OFF
        config_no_num_no_qa = {
            "include_numericals": False,
            "include_questions": False,
            "include_diagrams": True,
            "include_references": True
        }
        exporter._build_front_matter(
            doc,
            title="Engineering Physics",
            level="Undergraduate",
            toc_data={"chapters": []},
            config=config_no_num_no_qa
        )

        preface_text = ""
        for p in doc.paragraphs:
            if "academic textbook" in p.text:
                preface_text = p.text
                break

        assert "worked numerical problem solutions" not in preface_text
        assert "academic review questions" not in preface_text
        assert "theoretical foundational principles" in preface_text
        assert "technical schematics and diagrams" in preface_text
        assert "research-grounded citations" in preface_text
