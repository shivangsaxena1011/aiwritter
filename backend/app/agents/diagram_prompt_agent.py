"""
DiagramPromptAgent — Generates structured prompts for Black-and-White / Grayscale
academic textbook schematics and scientific diagrams.
Enforces high contrast, technical line art, zero cartoon aesthetic, and print-ready formatting.
"""

from typing import Dict, Any

class DiagramPromptAgent:
    """
    Constructs rigorous, black-and-white academic visual prompts for image generation models.
    """

    @classmethod
    def create_textbook_diagram_prompt(
        cls,
        topic: str,
        subject: str,
        concept_description: str = "",
        diagram_type: str = "schematic"
    ) -> str:
        """
        Creates an explicit prompt mandating black and white textbook line drawing standards.
        """
        clean_topic = topic.strip()
        desc = concept_description.strip() if concept_description else f"Technical schematic of {clean_topic} in {subject}."

        prompt = (
            f"Create a clean, black-and-white academic textbook diagram showing {clean_topic} for a university {subject} textbook.\n\n"
            f"Core Subject Matter: {desc}\n"
            f"Diagram Modality: {diagram_type}\n\n"
            "MANDATORY STYLE REQUIREMENTS:\n"
            "- Pure white background (#FFFFFF).\n"
            "- Crisp black and dark grayscale line drawing only.\n"
            "- Minimal, technical, and scientifically accurate layout.\n"
            "- Clear, legible scientific annotations and structural callouts.\n"
            "- High contrast, suitable for monochrome academic textbook printing.\n"
            "- Centered, balanced composition with clean margins.\n"
            "- STRICTLY NO cartoon styles, NO 3D rendering, NO decorative gradients, NO bright colors, NO childish illustrations."
        )
        return prompt
