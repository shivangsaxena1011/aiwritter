"""
AI Book Writer — Diagram Agent
Generates educational diagrams using Google Imagen 3.
Falls back to embedding a diagram prompt placeholder in the document.
"""

import os
import logging
from google import genai
from google.genai import types

logger = logging.getLogger(__name__)


class DiagramAgent:
    """Generates educational diagrams for textbook subtopics."""

    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)

    def generate_diagram(self, topic: str, subtopic: str, output_path: str) -> dict:
        """
        Attempt to generate a diagram using Imagen 3.
        Returns {"success": bool, "path": str|None, "prompt": str}
        On any failure, returns success=False with the prompt text for manual generation.
        """
        prompt = (
            f"A professional educational diagram illustrating '{subtopic}' "
            f"within the topic of '{topic}'. Clean academic style suitable for "
            f"a university textbook. Vector art, minimalist design, clear labels, "
            f"white background, no shadows or gradients, crisp typography."
        )

        try:
            response = self.client.models.generate_images(
                model='imagen-3.0-generate-002',
                prompt=prompt,
                config=types.GenerateImagesConfig(
                    number_of_images=1,
                )
            )

            if response.generated_images and len(response.generated_images) > 0:
                # Save the generated image
                image = response.generated_images[0].image
                # The image object has a save() method or image_bytes
                try:
                    image.save(output_path)
                except AttributeError:
                    # Fallback: try accessing raw bytes
                    img_bytes = getattr(image, 'image_bytes', None) or getattr(image, '_image_bytes', None)
                    if img_bytes:
                        with open(output_path, "wb") as f:
                            f.write(img_bytes)
                    else:
                        raise ValueError("Could not extract image data from response")

                logger.info(f"Diagram generated successfully: {output_path}")
                return {
                    "success": True,
                    "path": output_path,
                    "prompt": prompt
                }
            else:
                logger.warning(f"No images returned for: {subtopic}")
                return {
                    "success": False,
                    "path": None,
                    "prompt": prompt
                }

        except Exception as e:
            logger.warning(f"Imagen generation failed for '{subtopic}': {e}")
            return {
                "success": False,
                "path": None,
                "prompt": prompt
            }

    def create_placeholder_box(self, prompt_text: str) -> str:
        """Returns formatted markdown for a diagram prompt placeholder."""
        return (
            f"\n\n---\n"
            f"📊 **DIAGRAM PLACEHOLDER**\n\n"
            f"*Generate this diagram manually using the following prompt:*\n\n"
            f"> {prompt_text}\n\n"
            f"---\n\n"
        )
