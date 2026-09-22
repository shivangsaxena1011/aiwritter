import os
from typing import Dict, Any

PROMPTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "prompts"))

class PromptService:
    @staticmethod
    def get_prompt(template_name: str, **kwargs: Any) -> str:
        """Loads and formats a prompt template from prompts/ directory."""
        if not template_name.endswith(".txt"):
            template_name = f"{template_name}.txt"
        file_path = os.path.join(PROMPTS_DIR, template_name)
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Prompt template '{template_name}' not found at {file_path}")
        
        with open(file_path, "r", encoding="utf-8") as f:
            template = f.read()
        
        # Safely format template allowing unused keys
        try:
            return template.format(**kwargs)
        except KeyError:
            # Fallback for templates with nested braces like JSON examples
            for key, val in kwargs.items():
                template = template.replace(f"{{{key}}}", str(val))
            return template

prompt_service = PromptService()
