from typing import Optional
from backend.app.core.config import settings
from backend.app.services.ai.base import AIProvider
from backend.app.services.ai.gemini_provider import GeminiProvider
from backend.app.services.ai.mock_provider import MockProvider

def get_ai_provider(api_key: Optional[str] = None, force_mock: bool = False) -> AIProvider:
    """Factory to retrieve configured AI Provider."""
    if force_mock or settings.AI_MODE == "mock" or api_key == "mock":
        return MockProvider(api_key=api_key or "mock-key")
    
    key = api_key or settings.GEMINI_API_KEY
    if not key:
        # If no key is set anywhere, gracefully fall back to mock provider for local demo
        return MockProvider(api_key="mock-key")
    
    return GeminiProvider(api_key=key)
