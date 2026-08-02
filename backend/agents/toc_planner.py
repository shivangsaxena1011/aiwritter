import json
import logging

logger = logging.getLogger(__name__)

class TOCPlanner:
    def __init__(self, openai_key: str = "", gemini_key: str = ""):
        self.openai_key = openai_key
        self.gemini_key = gemini_key

    def plan_toc(self, syllabus: str, target_chapters: int = 5) -> dict:
        prompt = (
            f"You are an expert academic curriculum designer and textbook author.\n"
            f"Synthesize the following syllabus into a structured Table of Contents for a university textbook with exactly {target_chapters} chapters.\n\n"
            f"Syllabus Guidelines:\n{syllabus}\n\n"
            f"Return strictly valid JSON format with the following structure:\n"
            f"{{\n"
            f'  "title": "Book Title",\n'
            f'  "about_book": "2-3 paragraph overview of the textbook and target audience",\n'
            f'  "chapters": [\n'
            f'    {{\n'
            f'      "chapter_number": 1,\n'
            f'      "title": "Chapter Title",\n'
            f'      "objectives": ["Objective 1", "Objective 2"],\n'
            f'      "subtopics": [\n'
            f'        {{\n'
            f'          "title": "Subtopic Title",\n'
            f'          "needs_diagram": true,\n'
            f'          "diagram_topic": "Detailed description of illustration required"\n'
            f'        }}\n'
            f'      ]\n'
            f'    }}\n'
            f'  ]\n'
            f"}}\n"
        )

        # Try OpenAI if key exists
        if self.openai_key:
            try:
                import openai
                client = openai.OpenAI(api_key=self.openai_key)
                res = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": prompt}],
                    response_format={"type": "json_object"}
                )
                return json.loads(res.choices[0].message.content)
            except Exception as e:
                logger.warning(f"OpenAI TOC planning failed ({e}). Attempting Gemini fallback...")

        # Try Gemini fallback
        if self.gemini_key:
            try:
                from google import genai
                client = genai.Client(api_key=self.gemini_key)
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt,
                    config=dict(response_mime_type="application/json")
                )
                return json.loads(response.text)
            except Exception as e:
                logger.error(f"Gemini TOC planning failed: {e}")

        # Basic fallback template
        return {
            "title": "Academic Reference Manual",
            "about_book": "A comprehensive engineering and academic guide synthesized from course topics.",
            "chapters": [
                {
                    "chapter_number": i + 1,
                    "title": f"Unit {i + 1}: Fundamentals and Principles",
                    "objectives": ["Understand core concepts", "Apply analytical methods"],
                    "subtopics": [
                        {"title": f"Overview of Topic {i + 1}.1", "needs_diagram": True, "diagram_topic": f"System architecture for topic {i + 1}.1"},
                        {"title": f"Detailed Analysis {i + 1}.2", "needs_diagram": False, "diagram_topic": ""}
                    ]
                } for i in range(target_chapters)
            ]
        }
