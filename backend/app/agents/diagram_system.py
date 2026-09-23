import os
import re
import uuid
import logging
from typing import Dict, Any, Optional
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend for headless server execution
import matplotlib.pyplot as plt
import numpy as np

from backend.app.services.ai.base import AIProvider
from backend.app.services.prompt_service import prompt_service
from backend.app.agents.diagram_prompt_agent import DiagramPromptAgent
from backend.app.services.image.image_provider import DefaultImageProvider

logger = logging.getLogger(__name__)

class DiagramPlanner:
    def __init__(self, ai_provider: AIProvider):
        self.ai = ai_provider

    async def plan_diagram(
        self,
        book_title: str,
        subtopic_title: str,
        section_content: str,
        chapter_idx: int = 1,
        figure_idx: int = 1
    ) -> Dict[str, Any]:
        """Evaluates whether this section benefits from visual diagrams with chapter-aware captions."""
        excerpt = section_content[:2000]
        prompt = prompt_service.get_prompt(
            "diagram_planner.txt",
            book_title=book_title,
            subtopic_title=subtopic_title,
            section_content_excerpt=excerpt
        )
        caption_default = f"Figure {chapter_idx}.{figure_idx} — Technical Diagram of {subtopic_title}"

        try:
            res = await self.ai.generate_structured(prompt)
            if res.get("needs_diagram"):
                caption_raw = res.get("caption") or ""
                clean_caption = re.sub(r"^figure(?:\s*\d+(?:\.\d+)*)?\s*[\-—:]*\s*", "", caption_raw, flags=re.IGNORECASE).strip()
                if not clean_caption:
                    clean_caption = f"Technical Diagram of {subtopic_title}"
                res["caption"] = f"Figure {chapter_idx}.{figure_idx} — {clean_caption}"

                # Generate high-contrast academic monochrome prompt
                if not res.get("ai_prompt"):
                    res["ai_prompt"] = DiagramPromptAgent.create_textbook_diagram_prompt(
                        topic=subtopic_title,
                        subject=book_title,
                        concept_description=res.get("description", ""),
                        diagram_type=res.get("modality", "schematic")
                    )
                return res
        except Exception as e:
            logger.warning(f"Diagram planning failed: {e}")

        # Deterministic diagram plan: content-driven selection based on genuine visual necessity
        sub_lower = subtopic_title.lower()
        skip_words = ["introduction", "overview", "history", "operators", "summary", "conclusion", "postulate", "axiom", "definition", "limitations"]
        if any(sw in sub_lower for sw in skip_words) and not any(kw in sub_lower for kw in ["ruby", "he-ne", "fiber structure", "box", "well"]):
            has_schematic_need = False
            diag_type = "none"
        else:
            visual_candidates = {
                "energy-level diagram": ["box", "well", "infinite potential", "potential well", "energy band", "band gap", "three-level", "four-level"],
                "apparatus diagram": ["young", "double slit", "newton", "ring", "diffraction grating", "single slit", "interferometer", "hall effect", "ruby laser", "he-ne laser"],
                "geometric illustration": ["optical fiber", "fiber structure", "total internal reflection", "acceptance angle", "acceptance cone", "numerical aperture", "step-index", "graded-index"],
                "graph": ["polarization characteristic", "fringe intensity", "resonance curve", "dispersion curve"]
            }
            has_schematic_need = False
            diag_type = "scientific schematic"
            for v_type, keywords in visual_candidates.items():
                if any(kw in sub_lower for kw in keywords):
                    has_schematic_need = True
                    diag_type = v_type
                    break

        return {
            "needs_diagram": has_schematic_need,
            "modality": "chart" if diag_type == "graph" else "ai_illustration",
            "diagram_type": diag_type,
            "caption": f"Figure {chapter_idx}.{figure_idx} — {diag_type.title()}: {subtopic_title}",
            "description": f"Publication-grade {diag_type} illustrating physical constraints and boundary behavior of {subtopic_title}.",
            "ai_prompt": DiagramPromptAgent.create_textbook_diagram_prompt(
                topic=subtopic_title,
                subject=book_title,
                concept_description=f"{diag_type} showing {subtopic_title}"
            )
        }

class DiagramGenerator:
    def __init__(self, ai_provider: AIProvider):
        self.ai = ai_provider
        self.image_provider = DefaultImageProvider(ai_provider)

    async def generate_asset(
        self,
        plan: Dict[str, Any],
        output_dir: str,
        topic_title: str
    ) -> Dict[str, Any]:
        """
        Executes diagram generation based on chosen modality.
        Returns asset metadata dict: {success: bool, path: Optional[str], caption: str, placeholder: str}
        """
        caption = plan.get("caption") or f"Figure — Technical Diagram for {topic_title}"
        modality = plan.get("modality", "ai_illustration")
        file_id = uuid.uuid4().hex[:8]

        os.makedirs(output_dir, exist_ok=True)

        # 1. Deterministic Scientific Chart (Matplotlib)
        if modality == "chart":
            chart_path = os.path.join(output_dir, f"chart_{file_id}.png")
            success = self._generate_scientific_plot(plan, chart_path, topic_title)
            if success:
                return {
                    "success": True,
                    "path": chart_path,
                    "caption": caption,
                    "modality": "chart",
                    "provenance": {
                        "asset_id": file_id,
                        "provider": "matplotlib",
                        "model": "matplotlib-vector-graph-engine",
                        "generation_mode": "deterministic"
                    }
                }

        # 2. AI Illustration (Imagen / Gemini Provider with validation & fallback)
        ai_prompt = plan.get("ai_prompt") or DiagramPromptAgent.create_textbook_diagram_prompt(
            topic=topic_title,
            subject="Academic Subject"
        )
        img_path = os.path.join(output_dir, f"fig_{file_id}.png")

        return await self.image_provider.generate_diagram(
            prompt=ai_prompt,
            output_path=img_path,
            topic_title=topic_title,
            caption=caption
        )

    def _generate_scientific_plot(self, plan: Dict[str, Any], output_path: str, title: str) -> bool:
        """Generates a clean, publication-grade academic chart."""
        try:
            fig, ax = plt.subplots(figsize=(7, 4.2), dpi=150)
            fig.patch.set_facecolor("#ffffff")
            ax.set_facecolor("#fafbfc")

            # Sample scientific curves for educational plots
            x = np.linspace(0.01, 2.0, 200)
            y_ideal = 1.23 - 0.05 * np.log(x + 0.1)
            y_actual = y_ideal - (0.15 * np.log10(x * 10 + 1)) - (0.12 * x) - (0.05 / (2.1 - x))
            y_actual = np.clip(y_actual, 0.1, 1.3)

            ax.plot(x, y_ideal, label="Reversible Nernst Potential (E_rev)", color="#2563eb", lw=2, linestyle="--")
            ax.plot(x, y_actual, label="Operating Polarization Characteristic", color="#dc2626", lw=2.5)

            labels = plan.get("labels") or ["Activation Losses", "Ohmic Resistance", "Mass Transport"]
            if len(labels) >= 3:
                ax.annotate(labels[0], xy=(0.15, 0.95), xytext=(0.3, 1.1),
                            arrowprops=dict(facecolor="#4b5563", shrink=0.05, width=1, headwidth=5))
                ax.annotate(labels[1], xy=(1.0, 0.72), xytext=(1.1, 0.9),
                            arrowprops=dict(facecolor="#4b5563", shrink=0.05, width=1, headwidth=5))
                ax.annotate(labels[2], xy=(1.8, 0.35), xytext=(1.4, 0.2),
                            arrowprops=dict(facecolor="#4b5563", shrink=0.05, width=1, headwidth=5))

            ax.set_title(f"Characteristic Response: {title}", fontsize=11, fontweight="bold", pad=12, color="#1e293b")
            ax.set_xlabel("Normalized Load Parameter (J / J_max)", fontsize=10, labelpad=8)
            ax.set_ylabel("Specific Potential (V_cell [V])", fontsize=10, labelpad=8)
            ax.grid(True, linestyle=":", alpha=0.6, color="#cbd5e1")
            ax.legend(frameon=True, facecolor="#ffffff", edgecolor="#e2e8f0", fontsize=9)

            plt.tight_layout()
            plt.savefig(output_path, dpi=150, bbox_inches="tight")
            plt.close(fig)
            return True
        except Exception as e:
            logger.warning(f"Matplotlib scientific plot generation failed: {e}")
            plt.close("all")
            return False

    def create_placeholder_box(self, caption: str, prompt_text: str, description: str) -> str:
        """Produces a styled academic callout for the document."""
        return (
            f"\n\n> 📊 **{caption}**\n"
            f"> *Description*: {description}\n"
            f"> *Visual Specification*: `{prompt_text}`\n\n"
        )

# Semantic Aliases
DiagramPlannerAgent = DiagramPlanner
DiagramGeneratorAgent = DiagramGenerator

