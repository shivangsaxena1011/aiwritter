from typing import Optional
from backend.app.core.config import settings
from backend.app.services.ai.base import AIProvider
from backend.app.services.ai.gemini_provider import GeminiProvider
from backend.app.services.ai.mock_provider import MockProvider

def get_ai_provider(api_key: Optional[str] = None, force_mock: bool = False) -> AIProvider:
    """Factory to retrieve configured AI Provider with multi-key rotation support."""
    if force_mock or settings.AI_MODE == "mock" or api_key == "mock":
        return MockProvider(api_key=api_key or "mock-key")
    
    keys = []
    if api_key and api_key.strip() and api_key.lower() not in ("mock", "null", "none"):
        keys.append(api_key.strip())
    
    for k in settings.all_gemini_keys:
        if k not in keys:
            keys.append(k)

    if not keys:
        return MockProvider(api_key="mock-key")
    
    return GeminiProvider(api_key=keys[0], backup_keys=keys[1:])
