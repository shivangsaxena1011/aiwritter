import time
import logging
from google import genai
from google.genai import types

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ContentWriter:
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)

    def generate_subtopic_content(self, book_title: str, unit_title: str, topic_title: str, subtopic_title: str, previous_context: str = "") -> str:
        prompt = f"""You are a seasoned professor authoring a definitive, comprehensive reference textbook.
Book Title: {book_title}
Unit: {unit_title}
Topic: {topic_title}
Subtopic to write about: {subtopic_title}

Previous context (for continuity):
{previous_context}

INSTRUCTIONS:
- Write a massive, deeply detailed section targeting 4,000-6,000 words.
- Write as a seasoned professor.
- NEVER use these AI phrases: 'In conclusion', 'It's important to note', 'Delving into', 'Let's explore', 'In today's world'.
- Include: narrative examples, case studies, historical context, worked problems, and comparison tables.
- Format output in Markdown.
"""
        return self._call_gemini_with_retry(prompt)

    def generate_unit_introduction(self, book_title: str, unit_title: str, topics_list: list) -> str:
        prompt = f"""You are a seasoned professor authoring a definitive reference textbook.
Book Title: {book_title}
Unit: {unit_title}
Topics in this unit: {', '.join(topics_list)}

INSTRUCTIONS:
- Write an engaging 1000-word introduction for this unit.
- NEVER use these AI phrases: 'In conclusion', 'It's important to note', 'Delving into', 'Let's explore', 'In today's world'.
- Format output in Markdown.
"""
        return self._call_gemini_with_retry(prompt)

    def _call_gemini_with_retry(self, prompt: str, retries: int = 3) -> str:
        backoff = 2
        for attempt in range(retries):
            try:
                response = self.client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        temperature=0.7,
                        max_output_tokens=16000
                    )
                )
                return response.text
            except Exception as e:
                logger.error(f"Error generating content (attempt {attempt + 1}): {e}")
                if attempt == retries - 1:
                    raise e
                time.sleep(backoff)
                backoff *= 2
        return ""
