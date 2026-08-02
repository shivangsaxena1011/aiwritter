import os
import logging
from PIL import Image, ImageDraw, ImageFont
from backend.agents.diagram_style_manager import DiagramStyleManager

logger = logging.getLogger(__name__)

class DiagramAgent:
    def __init__(self, api_key: str = ""):
        self.api_key = api_key
        self.style_manager = DiagramStyleManager()

    def generate_diagram(self, topic: str, output_path: str) -> str:
        """Generates an educational diagram for a topic and saves it to output_path."""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Try Imagen via Gemini API if key is present
        if self.api_key:
            try:
                from google import genai
                client = genai.Client(api_key=self.api_key)
                prompt = self.style_manager.get_enhanced_prompt(topic)
                
                result = client.models.generate_images(
                    model='imagen-3.0-generate-002',
                    prompt=prompt,
                    config=dict(
                        number_of_images=1,
                        output_mime_type="image/png",
                        aspect_ratio="16:9"
                    )
                )
                if result.generated_images:
                    image_bytes = result.generated_images[0].image.image_bytes
                    with open(output_path, "wb") as f:
                        f.write(image_bytes)
                    logger.info(f"Generated Imagen diagram for '{topic}' at {output_path}")
                    return output_path
            except Exception as e:
                logger.warning(f"Imagen generation failed ({e}). Falling back to local visual graphic renderer...")

        # Fallback local clean vector visual diagram renderer using PIL
        return self._generate_local_fallback_diagram(topic, output_path)

    def _generate_local_fallback_diagram(self, topic: str, output_path: str) -> str:
        width, height = 1200, 675
        img = Image.new("RGB", (width, height), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)

        category = self.style_manager.classify_topic(topic)

        # Border
        draw.rectangle([(20, 20), (width - 20, height - 20)], outline=(226, 232, 240), width=3)
        
        # Title Header Bar
        draw.rectangle([(20, 20), (width - 20, 90)], fill=(43, 108, 176))
        
        try:
            font_title = ImageFont.truetype("arial.ttf", 26)
            font_node = ImageFont.truetype("arial.ttf", 18)
        except Exception:
            font_title = font_node = ImageFont.load_default()

        draw.text((40, 42), f"FIGURE: {topic.upper()}", fill=(255, 255, 255), font=font_title)

        # Draw structured diagram layout based on category
        if category == "flowchart":
            steps = ["Input / Start", "Processing & Analysis", "Validation Check", "Output / Final Result"]
            for idx, s_text in enumerate(steps):
                x1 = 60 + idx * 270
                y1, y2 = 280, 380
                draw.rounded_rectangle([(x1, y1), (x1 + 220, y2)], radius=12, fill=(237, 242, 247), outline=(43, 108, 176), width=2)
                draw.text((x1 + 20, y1 + 35), s_text, fill=(26, 54, 93), font=font_node)
                if idx < len(steps) - 1:
                    draw.line([(x1 + 220, 330), (x1 + 270, 330)], fill=(43, 108, 176), width=3)

        elif category == "cyclic":
            center_x, center_y = width // 2, height // 2 + 30
            radius = 160
            phases = ["Phase 1: Init", "Phase 2: Exec", "Phase 3: Audit", "Phase 4: Adapt"]
            coords = [(center_x - radius, center_y - radius), (center_x + radius, center_y - radius),
                      (center_x + radius, center_y + radius), (center_x - radius, center_y + radius)]
            draw.ellipse([(center_x - radius, center_y - radius), (center_x + radius, center_y + radius)], outline=(203, 213, 225), width=4)
            for idx, p_text in enumerate(phases):
                cx, cy = coords[idx]
                draw.rounded_rectangle([(cx - 80, cy - 30), (cx + 80, cy + 30)], radius=8, fill=(237, 242, 247), outline=(43, 108, 176), width=2)
                draw.text((cx - 60, cy - 10), p_text, fill=(26, 54, 93), font=font_node)

        else:
            # Architecture / Conceptual Box layout
            draw.rounded_rectangle([(80, 160), (width - 80, 560)], radius=16, fill=(247, 250, 252), outline=(203, 213, 225), width=2)
            nodes = [("Core Layer", 140, 220), ("Logic & Analytics", 460, 220), ("Interface Engine", 780, 220)]
            for title, nx, ny in nodes:
                draw.rounded_rectangle([(nx, ny), (nx + 280, ny + 260)], radius=12, fill=(255, 255, 255), outline=(43, 108, 176), width=2)
                draw.rectangle([(nx, ny), (nx + 280, ny + 50)], fill=(43, 108, 176))
                draw.text((nx + 20, ny + 14), title, fill=(255, 255, 255), font=font_node)
                draw.text((nx + 20, ny + 80), f"• Functional Unit\n• Key Subsystem\n• {topic}", fill=(74, 85, 104), font=font_node)

        # Footer
        draw.text((40, height - 50), "AI Textbook Publishing Orchestrator - Publication Ready Visual Asset", fill=(160, 174, 192), font=font_node)

        img.save(output_path, "PNG")
        logger.info(f"Rendered local visual diagram for '{topic}' to {output_path}")
        return output_path
