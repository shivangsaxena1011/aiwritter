import logging

logger = logging.getLogger(__name__)

class ContentWriter:
    def __init__(self, openai_key: str = "", gemini_key: str = ""):
        self.openai_key = openai_key
        self.gemini_key = gemini_key

    def _call_model(self, prompt: str) -> str:
        if self.openai_key:
            try:
                import openai
                client = openai.OpenAI(api_key=self.openai_key)
                res = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": prompt}]
                )
                return res.choices[0].message.content
            except Exception as e:
                logger.warning(f"OpenAI writing failed ({e}). Falling back to Gemini...")

        if self.gemini_key:
            try:
                from google import genai
                client = genai.Client(api_key=self.gemini_key)
                res = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt
                )
                return res.text
            except Exception as e:
                logger.error(f"Gemini writing failed: {e}")

        return "Content generation unavailable. Please check API keys."

    def generate_chapter_intro(self, title: str, ch_num: int, objectives: list, book_context: dict = None) -> str:
        prompt = (
            f"You are a university professor writing Chapter {ch_num}: {title}.\n"
            f"Write a rigorous, engaging 3-paragraph introduction for this chapter.\n"
            f"Include learning objectives as bullet points.\n"
            f"Book context: {book_context.get('about_book', '') if book_context else ''}\n"
        )
        return self._call_model(prompt)

    def generate_subtopic_content(self, ch_title: str, ch_num: int, subtopic: dict, book_context: dict = None) -> str:
        sub_title = subtopic.get("title", "")
        needs_diagram = subtopic.get("needs_diagram", False)
        diagram_topic = subtopic.get("diagram_topic", "")
        
        diag_placeholder = f"\n\n[DIAGRAM_PLACEHOLDER: {diagram_topic}]\n\n" if needs_diagram else ""

        prompt = (
            f"Write a detailed academic textbook section for Subtopic: '{sub_title}' inside Chapter {ch_num}: {ch_title}.\n"
            f"Include formal definitions, technical explanations, worked examples, and a markdown comparison table if applicable.\n"
            f"Use markdown headings (## {sub_title}).\n"
        )
        content = self._call_model(prompt)
        return content + diag_placeholder

    def generate_chapter_summary(self, title: str, ch_num: int) -> str:
        prompt = (
            f"Write a comprehensive Chapter Summary and 5 Review Questions (Conceptual & Analytical) for Chapter {ch_num}: {title}.\n"
            f"Format as markdown under '## Chapter Summary' and '## Review Questions'."
        )
        return self._call_model(prompt)
