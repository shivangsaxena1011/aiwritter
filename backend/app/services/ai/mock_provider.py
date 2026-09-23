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
        # Extract topic/subtopic from prompt if present
        topic_match = re.search(r"(?:SUBTOPIC SECTION|SUBTOPIC):\s*([^\n\r]+)", prompt)
        subtopic = topic_match.group(1).strip() if topic_match else "Core Principles"

        include_num = "INCLUDE WORKED NUMERICAL EXAMPLES" in prompt
        include_qa = "INCLUDE REVIEW QUESTIONS" in prompt

        content_parts = [
            f"""### Learning Objectives
1. Understand the theoretical foundations and core dynamics of {subtopic}.
2. Formulate governing quantitative relationships and state equations.
3. Critically analyze industrial trade-offs, operational constraints, and failure modes.

### 1. Introduction and Historical Context
The development of {subtopic} represents a foundational milestone in contemporary technical systems. Historically developed to address operational inefficiencies, early architectures prioritized basic functionality over thermodynamic or computational efficiency. Modern methodologies integrate rigorous closed-loop optimization to achieve optimal performance metrics.

### 2. Theoretical Foundations and Analytical Formulation
At its core, {subtopic} operates under established physical and empirical principles. The dynamic behavior can be modeled using the generalized governing equation:

$$\\frac{{d\\Psi}}{{dt}} + \\nabla \\cdot (\\mathbf{{v}} \\Psi) = \\kappa \\nabla^2 \\Psi + \\dot{{S}}_{{gen}}$$

Where:
- $\\Psi$ represents the state variable of the system.
- $\\mathbf{{v}}$ denotes the convective velocity field vector.
- $\\kappa$ is the effective transport diffusivity coefficient.
- $\\dot{{S}}_{{gen}}$ is the net volumetric internal generation rate.

### 3. Comparison of Core Architectures
The table below contrasts standard configurations used across modern academic and commercial implementations:

| Parameter | Configuration Alpha | Configuration Beta | Configuration Gamma |
| :--- | :--- | :--- | :--- |
| Operational Efficiency | 42% - 48% | 55% - 62% | 68% - 74% |
| Temperature Range | 60°C - 80°C | 120°C - 180°C | 600°C - 800°C |
| Response Latency | < 5 ms | 25 ms | > 100 ms |
| Capital Cost Index | Moderate | High | Premium |
| Durability Lifecycle | 15,000 Hours | 40,000 Hours | 80,000 Hours |"""
        ]

        if include_num:
            content_parts.append(f"""
### 4. Worked Solved Numerical Problem
**Problem Statement:** Consider a reference installation of {subtopic} operating under nominal boundary conditions with an input flux of $2.5\\text{{ kg/s}}$ and an active area of $14.2\\text{{ m}}^2$. Calculate the net specific flux and resultant dissipation factor.

- **Given:**
  - Influx rate $\\dot{{m}} = 2.5\\text{{ kg/s}}$
  - Cross-sectional surface area $A = 14.2\\text{{ m}}^2$
- **Formula:**
  $$J = \\frac{{\\dot{{m}}}}{{A}}$$
- **Substitution:**
  $$J = \\frac{{2.5}}{{14.2}}$$
- **Calculation:**
  $$J = 0.176056\\dots$$
- **Answer:**
  $$J = 0.1761$$
- **Unit:**
  $$\\text{{kg}}/(m^2\\cdot\\text{{s}})$$""")

        content_parts.append(f"""
### 5. Summary and Key Takeaways
- {subtopic} demonstrates non-linear dependencies across boundary operational regimes.
- Architectural selection dictates thermal management, longevity, and overall system scalability.""")

        if include_qa:
            content_parts.append("""
### 6. Review Questions and Academic Exercises
1. *Analytical*: Derive the steady-state solution for $\\Psi(x)$ assuming 1D planar symmetry and zero generation.
2. *Conceptual*: Contrast the mechanical failure modes between Configuration Alpha and Beta under cyclic loading.""")

        return "\n\n".join(content_parts)

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

        # Diagram planning
        if "diagram" in prompt_lower or "illustration" in prompt_lower:
            topic_match = re.search(r"(?:topic|subtopic|title):\s*([^\n\r]+)", prompt, re.I)
            subtopic = topic_match.group(1).strip() if topic_match else "Governing Physical Phenomenon"
            subtopic_lower = subtopic.lower()

            skip_words = ["introduction", "overview", "history", "operators", "summary", "conclusion"]
            if any(sw in subtopic_lower for sw in skip_words) and not any(kw in subtopic_lower for kw in ["ruby", "he-ne", "fiber structure"]):
                needs_diagram = False
            else:
                diagram_keywords = [
                    "matter wave", "de broglie", "uncertainty", "box", "well", "potential", "schrödinger", "schrodinger",
                    "young", "double slit", "slit", "interference", "thin film", "newton", "ring", "diffraction", "grating", "resolving power",
                    "stimulated emission", "emission", "population inversion", "metastable", "energy level", "ruby", "he-ne", "semiconductor laser", "laser",
                    "optical fiber", "fiber", "internal reflection", "acceptance", "numerical aperture", "step-index", "graded-index", "dispersion",
                    "energy band", "band", "intrinsic", "extrinsic", "n-type", "p-type", "fermi", "hall effect"
                ]
                needs_diagram = any(kw in subtopic_lower for kw in diagram_keywords)

            return {
                "needs_diagram": needs_diagram,
                "modality": "chart" if any(w in subtopic_lower for w in ["characteristic", "plot", "distribution", "response", "band", "spectrum"]) else "ai_illustration",
                "diagram_type": "Scientific Schematic",
                "caption": f"Figure — Technical Schematic and Operational Characteristics of {subtopic}",
                "description": f"Technical illustration showing the operational behavior, potential distribution, and wave profiles of {subtopic}",
                "ai_prompt": f"Clean monochrome academic textbook diagram showing {subtopic} with boundary conditions",
                "chart_code": "",
                "labels": ["Boundary Condition", "Eigenmode Distribution", "Equilibrium State"]
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

