"""
Test Suite for Content Intelligence Architecture & Subject-Aware Writing.
Validates SubjectKnowledgeModel, TopicTypeClassifier, EquationValidationAgent,
RepetitionDetectionAgent, BookTerminologyRegistry, AcademicContentQualityAgent,
and BookFactCheckAgent.
"""

import pytest
from backend.app.agents.subject_knowledge_model import SubjectKnowledgeModel
from backend.app.agents.topic_classifier import TopicTypeClassifier, TopicType
from backend.app.agents.equation_validation_agent import EquationValidationAgent
from backend.app.agents.repetition_detection_agent import RepetitionDetectionAgent
from backend.app.agents.book_terminology_registry import BookTerminologyRegistry
from backend.app.agents.academic_content_quality_agent import AcademicContentQualityAgent
from backend.app.agents.book_fact_check_agent import BookFactCheckAgent


class TestSubjectKnowledgeModel:
    """Verifies domain knowledge retrieval and authentic academic section generation."""

    def test_domain_identification(self):
        assert SubjectKnowledgeModel.get_subject_domain("Engineering Physics", "de Broglie Hypothesis") == "quantum mechanics"
        assert SubjectKnowledgeModel.get_subject_domain("Physics", "Newton's Rings") == "wave optics"
        assert SubjectKnowledgeModel.get_subject_domain("Optics", "Numerical Aperture") == "fiber optics"
        assert SubjectKnowledgeModel.get_subject_domain("Physics", "Einstein Coefficients") == "lasers"
        assert SubjectKnowledgeModel.get_subject_domain("Physics", "Hall Effect") == "semiconductor physics"

    def test_knowledge_retrieval(self):
        knowledge = SubjectKnowledgeModel.get_knowledge_for_topic("de Broglie Hypothesis", "Engineering Physics")
        assert "principles" in knowledge
        assert "equations" in knowledge
        assert len(knowledge["equations"]) > 0
        assert "de Broglie" in knowledge["equations"][0]["name"]
        assert "\\lambda = \\frac{h}{p}" in knowledge["equations"][0]["latex"]

    def test_de_broglie_academic_section_generation(self):
        section = SubjectKnowledgeModel.generate_academic_section(
            topic="de Broglie Hypothesis",
            subtopic="Dual Nature of Matter",
            subject="Engineering Physics",
            include_numericals=True,
            include_questions=True,
            requires_derivation=True
        )
        assert len(section.split()) >= 350
        # Check authentic physics content
        assert "Davisson and Germer" in section or "Davisson" in section
        assert "Bragg" in section or "diffraction" in section
        assert "\\lambda = \\frac{h}{p}" in section or "\\lambda = \\frac{h}{mv}" in section
        assert "1.227" in section or "\\sqrt{V}" in section
        # Check zero generic boilerplate
        assert "This treatise establishes" not in section
        assert "Configuration Alpha" not in section
        assert "Configuration Beta" not in section
        assert "42% - 48%" not in section
        assert "\\dot{S}_{gen}" not in section

    def test_particle_in_a_box_section_generation(self):
        section = SubjectKnowledgeModel.generate_academic_section(
            topic="Particle in a 1D Box",
            subtopic="Energy Eigenvalues and Wave Functions",
            subject="Engineering Physics",
            include_numericals=True,
            include_questions=True,
            requires_derivation=True
        )
        assert len(section.split()) >= 350
        assert "E_n = \\frac{n^2 h^2}{8mL^2}" in section or "8m" in section
        assert "Dirichlet" in section or "\\psi(0) = 0" in section
        assert "zero-point energy" in section.lower()
        # Zero generic boilerplate
        assert "Configuration Alpha" not in section
        assert "Operational Efficiency" not in section


class TestTopicTypeClassifier:
    """Verifies multi-label topic classification and pedagogical section blueprinting."""

    def test_topic_classification(self):
        classifier = TopicTypeClassifier()
        res_concept = classifier.classify_topic("Physical Interpretation of the Wave Function", "Quantum Mechanics")
        assert TopicType.CONCEPTUAL in res_concept["topic_types"]

        res_deriv = classifier.classify_topic("Derivation of Energy Eigenvalues for Particle in a Box", "Quantum Mechanics")
        assert TopicType.DERIVATION_HEAVY in res_deriv["topic_types"] or TopicType.MATHEMATICAL in res_deriv["topic_types"]

        res_exp = classifier.classify_topic("Davisson-Germer Electron Scattering Experiment", "Quantum Mechanics")
        assert TopicType.EXPERIMENTAL in res_exp["topic_types"]

    def test_pedagogical_structure_has_no_generic_titles(self):
        classifier = TopicTypeClassifier()
        structure = classifier.generate_pedagogical_structure("de Broglie Hypothesis", "Quantum Mechanics")
        sections = structure.get("recommended_sections", [])
        assert len(sections) >= 3
        generic_forbidden = [
            "Conceptual Axioms and Physical Mechanism",
            "Quantitative Properties and Parameter Dependencies",
            "Technological Applications and Engineering Implementations",
            "Theoretical Framework and Physical Postulates"
        ]
        for s in sections:
            assert s["title"] not in generic_forbidden


class TestEquationValidationAgent:
    """Verifies that mathematical equations match topic relevance and dimensional integrity."""

    def test_valid_quantum_equations(self):
        validator = EquationValidationAgent()
        content = """
        The matter wavelength is given by:
        $$\\lambda = \\frac{h}{p} = \\frac{h}{mv}$$
        where $\\lambda$ is wavelength, $h$ is Planck constant, and $p$ is momentum.
        """
        res = validator.validate_equations(content, "de Broglie Hypothesis", "Quantum Mechanics")
        assert res.total_equations >= 1
        assert res.valid_equations >= 1
        assert res.topic_relevance_score >= 0.70

    def test_banned_fake_equations(self):
        validator = EquationValidationAgent()
        content = """
        The dynamic balance is governed by:
        $$\\frac{d\\Psi}{dt} + \\nabla \\cdot (\\mathbf{v} \\Psi) = \\kappa \\nabla^2 \\Psi + \\dot{S}_{gen}$$
        """
        res = validator.validate_equations(content, "de Broglie Hypothesis", "Quantum Mechanics")
        assert any("banned generic" in issue.lower() or "unrelated" in issue.lower() for issue in res.issues)


class TestRepetitionDetectionAgent:
    """Verifies exact and near-duplicate paragraph detection across the book."""

    def test_repetition_detector(self):
        detector = RepetitionDetectionAgent()
        para1 = "The formulation of the de Broglie hypothesis marked one of the most profound conceptual revolutions in modern physics."
        para2 = "A particle confined within a one-dimensional box forms stationary standing waves resulting in discrete energy levels."

        issues1 = detector.register_section_paragraphs(para1, "Chapter 1 > Topic 1")
        assert len(issues1) == 0

        # Exact duplicate in another chapter/topic
        issues2 = detector.register_section_paragraphs(para1, "Chapter 1 > Topic 2")
        assert len(issues2) >= 1
        assert any(i["type"] == "exact_duplicate" for i in issues2)

        # Distinct paragraph
        issues3 = detector.register_section_paragraphs(para2, "Chapter 1 > Topic 3")
        assert len(issues3) == 0


class TestBookTerminologyRegistry:
    """Verifies consistent notation, symbols, and definitions across chapters."""

    def test_terminology_registration(self):
        registry = BookTerminologyRegistry()
        content = """
        The de Broglie wavelength is defined as $\\lambda = h/p$.
        Here $h$ is Planck's constant.
        """
        registry.register_from_content(content, "Chapter 1 > de Broglie")
        summary = registry.get_summary()
        assert summary["total_registered_terms"] >= 1
        assert len(summary["conflicts"]) == 0


class TestAcademicContentQualityAgent:
    """Verifies genericity score, topic alignment score, and unsupported claim detection."""

    def test_genuine_content_scores(self):
        agent = AcademicContentQualityAgent()
        genuine_text = SubjectKnowledgeModel.generate_academic_section(
            topic="de Broglie Hypothesis",
            subtopic="Dual Nature of Matter",
            subject="Engineering Physics"
        )
        metrics = agent.evaluate_content(genuine_text, "de Broglie Hypothesis", "Engineering Physics")
        assert metrics.genericity_score < 0.20
        assert metrics.topic_alignment_score > 0.70
        assert metrics.unsupported_claims_count == 0
        assert metrics.fabricated_data_count == 0
        assert metrics.is_publication_ready is True

    def test_generic_boilerplate_is_rejected(self):
        agent = AcademicContentQualityAgent()
        bad_text = """
        This treatise establishes the rigorous theoretical framework and physical principles governing de Broglie Hypothesis.
        Modern engineering applications rely directly on these foundational dynamics to achieve stable, high-efficiency system performance.
        Configuration Alpha achieves 42% - 48% efficiency under 15,000 Hours durability lifecycle.
        Configuration Beta achieves 55% - 62% efficiency.
        """
        metrics = agent.evaluate_content(bad_text, "de Broglie Hypothesis", "Engineering Physics")
        assert metrics.genericity_score > 0.30
        assert metrics.fabricated_data_count > 0
        assert metrics.is_publication_ready is False


class TestBookFactCheckAgent:
    """Verifies physical constant definitions and mathematical invariants across chapters."""

    def test_fact_check_consistency(self):
        fact_checker = BookFactCheckAgent()
        sections = [
            {
                "topic": "de Broglie Hypothesis",
                "subtopic": "Matter Waves",
                "content": "Planck's constant is approximately $6.626 \\times 10^{-34}\\text{ J}\\cdot\\text{s}$."
            },
            {
                "topic": "Particle in a Box",
                "subtopic": "Energy Levels",
                "content": "Using $h = 6.626 \\times 10^{-34}\\text{ J}\\cdot\\text{s}$ and $m_e = 9.109 \\times 10^{-31}\\text{ kg}$."
            }
        ]
        summary = fact_checker.audit_book_consistency(sections)
        assert summary["constants_checked"] >= 1
        assert summary["inconsistencies_found"] == 0
        assert summary["status"] == "passed"
