import os
import re
from typing import Optional, Dict, Any
from PIL import Image, ImageDraw, ImageFont
from backend.app.services.ai.base import AIProvider

class MockProvider(AIProvider):
    """Deterministic offline provider for testing and offline development."""

    def __init__(self, api_key: str = "mock-key"):
        self.api_key = api_key

    async def generate_text(
        self,
        prompt: str,
        system_instruction: Optional[str] = None,
        temperature: float = 0.7,
        max_output_tokens: Optional[int] = None
    ) -> str:
        from backend.app.agents.subject_knowledge_model import SubjectKnowledgeModel

        # Extract metadata from prompt
        subtopic_match = re.search(r"(?:SUBTOPIC SECTION|SUBTOPIC):\s*([^\n\r]+)", prompt)
        subtopic = subtopic_match.group(1).strip() if subtopic_match else "Core Principles"

        topic_match = re.search(r"(?:MAJOR TOPIC|TOPIC):\s*([^\n\r]+)", prompt)
        topic = topic_match.group(1).strip() if topic_match else subtopic

        subject_match = re.search(r"(?:SUBJECT / DISCIPLINE|SUBJECT):\s*([^\n\r]+)", prompt)
        subject = subject_match.group(1).strip() if subject_match else "Engineering Physics"

        include_num = "INCLUDE WORKED NUMERICAL EXAMPLES" in prompt
        include_qa = "INCLUDE REVIEW QUESTIONS" in prompt
        requires_derivation = any(k in f"{subtopic} {topic}".lower() for k in ["derivation", "equation", "box", "well", "hypothesis", "uncertainty", "velocity", "constant"])

        return SubjectKnowledgeModel.generate_academic_section(
            topic=topic,
            subtopic=subtopic,
            subject=subject,
            include_numericals=include_num,
            include_questions=include_qa,
            requires_derivation=requires_derivation
        )

    async def generate_structured(
        self,
        prompt: str,
        system_instruction: Optional[str] = None,
        temperature: float = 0.2
    ) -> Dict[str, Any]:
        prompt_lower = prompt.lower()

        # TOC planning
        if "table of contents" in prompt_lower or "syllabus" in prompt_lower:
            return {
                "title": "Fuel Cell Technology: Powering the Future",
                "units": [
                    {
                        "name": "Unit 1: Introduction to Fuel Cells",
                        "topics": [
                            {
                                "name": "1.1 Overview and History",
                                "subtopics": [
                                    "1.1.1 Historical Evolution",
                                    "1.1.2 Modern Energy Landscape"
                                ]
                            },
                            {
                                "name": "1.2 Fundamental Working Principles",
                                "subtopics": [
                                    "1.2.1 Electrochemical Foundations",
                                    "1.2.2 Comparison with Batteries and Engines"
                                ]
                            }
                        ]
                    },
                    {
                        "name": "Unit 2: Fuel Cell Fundamentals",
                        "topics": [
                            {
                                "name": "2.1 Thermodynamics and Kinetics",
                                "subtopics": [
                                    "2.1.1 Gibbs Free Energy and Enthalpy",
                                    "2.1.2 Nernst Equation and Polarization"
                                ]
                            }
                        ]
                    }
                ]
            }

        # Diagram planning — Content-driven selection based on genuine visual necessity
        if "diagram" in prompt_lower or "illustration" in prompt_lower:
            subtopic_match = re.search(r"(?:subtopic|section):\s*([^\n\r]+)", prompt, re.I)
            if not subtopic_match:
                subtopic_match = re.search(r"(?:topic|title):\s*([^\n\r]+)", prompt, re.I)
            subtopic = subtopic_match.group(1).strip() if subtopic_match else "Governing Physical Phenomenon"
            subtopic_lower = subtopic.lower()

            # Skip non-visual, abstract, overview, or purely mathematical sections
            skip_words = ["introduction", "overview", "history", "operators", "summary", "conclusion", "postulate", "axiom", "definition", "limitations"]
            if any(sw in subtopic_lower for sw in skip_words) and not any(kw in subtopic_lower for kw in ["ruby", "he-ne", "fiber structure", "box", "well"]):
                needs_diagram = False
                diag_type = "none"
            else:
                # Rigorous check: Does a visual materially improve understanding?
                visual_candidates = {
                    "energy-level diagram": ["box", "well", "infinite potential", "potential well", "energy band", "band gap", "three-level", "four-level"],
                    "apparatus diagram": ["young", "double slit", "newton", "ring", "diffraction grating", "single slit", "interferometer", "hall effect", "ruby laser", "he-ne laser"],
                    "geometric illustration": ["optical fiber", "fiber structure", "total internal reflection", "acceptance angle", "acceptance cone", "numerical aperture", "step-index", "graded-index"],
                    "graph": ["polarization characteristic", "fringe intensity", "resonance curve", "dispersion curve"]
                }
                needs_diagram = False
                diag_type = "scientific schematic"
                for v_type, keywords in visual_candidates.items():
                    if any(kw in subtopic_lower for kw in keywords):
                        needs_diagram = True
                        diag_type = v_type
                        break

            return {
                "needs_diagram": needs_diagram,
                "modality": "chart" if diag_type == "graph" else "ai_illustration",
                "diagram_type": diag_type,
                "caption": f"Figure — {diag_type.title()}: Schematic of {subtopic}",
                "description": f"Publication-grade {diag_type} illustrating the physical geometry, coordinate constraints, and boundary behavior of {subtopic}",
                "ai_prompt": f"Clean monochrome textbook {diag_type} showing {subtopic} with labeled coordinate axes and boundary conditions on pure white background",
                "chart_code": "",
                "labels": ["Boundary Interface", "Eigenmode Waveprofile", "Ground State"]
            }

        # Review agent
        if "peer review" in prompt_lower or "reviewer" in prompt_lower or "evaluation" in prompt_lower:
            return {
                "overall_score": 92,
                "depth_score": 19,
                "pedagogy_score": 18,
                "filler_score": 19,
                "accuracy_score": 18,
                "completeness_score": 18,
                "issues": [],
                "missing_topics": [],
                "corrections": [],
                "rewrite_required": False
            }

        # Consistency auditor
        if "consistency" in prompt_lower:
            return {
                "is_consistent": True,
                "inconsistencies": [],
                "new_terms_introduced": [
                    {"term": "Electrochemical Activation", "definition": "Energy required to initiate charge transfer across electrode interface"}
                ],
                "new_acronyms": [
                    {"acronym": "PEMFC", "full_form": "Proton Exchange Membrane Fuel Cell"}
                ]
            }

        # Quality controller
        return {
            "content_completeness": 96.0,
            "structure_consistency": 98.0,
            "terminology_consistency": 97.0,
            "section_coverage": 98.0,
            "formatting_validation": 100.0,
            "overall_score": 97.8,
            "strengths": ["Comprehensive mathematical treatment", "Zero banned AI tropes"],
            "warnings": [],
            "publication_status": "Ready for Publication"
        }

    async def generate_image(
        self,
        prompt: str,
        output_path: str
    ) -> Dict[str, Any]:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        # Requirement 7: Black and white, grayscale, white background, high contrast, clean, technical
        img = Image.new("RGB", (800, 450), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)
        # Draw high-contrast monochrome technical schematic
        draw.rectangle([50, 50, 750, 400], outline=(15, 23, 42), width=3)
        draw.rectangle([80, 80, 280, 370], fill=(248, 250, 252), outline=(71, 85, 105), width=2)
        draw.rectangle([520, 80, 720, 370], fill=(248, 250, 252), outline=(71, 85, 105), width=2)
        draw.line([(280, 225), (520, 225)], fill=(15, 23, 42), width=2)
        # Coordinate axes
        draw.line([(60, 390), (740, 390)], fill=(15, 23, 42), width=2)
        draw.line([(60, 60), (60, 390)], fill=(15, 23, 42), width=2)
        draw.text((310, 205), "Boundary Flux Interface", fill=(15, 23, 42))
        draw.text((120, 215), "Potential State V_1", fill=(51, 65, 85))
        draw.text((560, 215), "Potential State V_2", fill=(51, 65, 85))
        draw.text((60, 25), f"Technical Schematic: {prompt[:50]}...", fill=(15, 23, 42))
        img.save(output_path, "PNG")

        return {
            "success": True,
            "path": output_path,
            "prompt": prompt
        }

MockAIProvider = MockProvider

