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
        topic_match = re.search(r"SUBTOPIC:\s*([^\n\r]+)", prompt)
        subtopic = topic_match.group(1).strip() if topic_match else "Core Principles"

        return f"""### Learning Objectives
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
| Durability Lifecycle | 15,000 Hours | 40,000 Hours | 80,000 Hours |

### 4. Worked Empirical Example
**Problem Statement:** Consider a reference installation operating under nominal boundary conditions with an input mass flux of $2.5\\text{{ kg/s}}$ and an active surface area of $14.2\\text{{ m}}^2$. Calculate the net specific flux and resultant dissipation factor.

**Solution:**
1. Determine the nominal area-specific flux:
   $$J = \\frac{{\\dot{{m}}}}{{A}} = \\frac{{2.5}}{{14.2}} = 0.1761\\text{{ kg/(m}}^2\\cdot\\text{{s)}}$$
2. Substituting into the dissipation integral yields an empirical loss factor of $\\eta_{{loss}} = 0.042$, demonstrating compliance with ISO technical standards.

### 5. Summary and Key Takeaways
- {subtopic} demonstrates non-linear dependencies across boundary operational regimes.
- Architectural selection dictates thermal management, longevity, and overall system scalability.

### 6. Review Questions and Academic Exercises
1. *Analytical*: Derive the steady-state solution for $\\Psi(x)$ assuming 1D planar symmetry and zero generation.
2. *Conceptual*: Contrast the mechanical failure modes between Configuration Alpha and Beta under cyclic loading.
"""

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
            return {
                "needs_diagram": True,
                "modality": "chart",
                "diagram_type": "Scientific Graph",
                "caption": "Figure 1.1 — Empirical Polarization and Efficiency Curve",
                "description": "Graph showing the cell voltage vs current density and activation losses",
                "ai_prompt": "Clean scientific diagram of a fuel cell polarization curve",
                "chart_code": "",
                "labels": ["Activation Loss", "Ohmic Loss", "Concentration Loss"]
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
        img = Image.new("RGB", (800, 450), color=(18, 24, 38))
        draw = ImageDraw.Draw(img)
        # Draw mock technical schematic
        draw.rectangle([50, 50, 750, 400], outline=(79, 140, 255), width=3)
        draw.rectangle([80, 80, 280, 370], fill=(26, 36, 56), outline=(168, 85, 247), width=2)
        draw.rectangle([520, 80, 720, 370], fill=(26, 36, 56), outline=(34, 197, 94), width=2)
        draw.line([(280, 225), (520, 225)], fill=(79, 140, 255), width=3)
        draw.text((320, 200), "Electrolyte Layer", fill=(240, 240, 240))
        draw.text((120, 215), "Anode (-)", fill=(168, 85, 247))
        draw.text((560, 215), "Cathode (+)", fill=(34, 197, 94))
        draw.text((60, 20), f"Academic Diagram: {prompt[:45]}...", fill=(200, 200, 200))
        img.save(output_path, "PNG")

        return {
            "success": True,
            "path": output_path,
            "prompt": prompt
        }

MockAIProvider = MockProvider

