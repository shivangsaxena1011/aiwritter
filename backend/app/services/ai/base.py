from abc import ABC, abstractmethod
from typing import Optional, Dict, Any

class AIProvider(ABC):
    """Abstract interface for AI generation providers."""

    @abstractmethod
    async def generate_text(
        self,
        prompt: str,
        system_instruction: Optional[str] = None,
        temperature: float = 0.7,
        max_output_tokens: Optional[int] = None
    ) -> str:
        """Generates raw text from a prompt."""
        pass

    @abstractmethod
    async def generate_structured(
        self,
        prompt: str,
        system_instruction: Optional[str] = None,
        temperature: float = 0.2
    ) -> Dict[str, Any]:
        """Generates a validated JSON structured response."""
        pass

    @abstractmethod
    async def generate_image(
        self,
        prompt: str,
        output_path: str
    ) -> Dict[str, Any]:
        """Generates an image and writes it to output_path."""
        pass
