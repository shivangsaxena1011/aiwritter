from typing import Optional
from backend.app.core.config import settings
from backend.app.services.ai.base import AIProvider
from backend.app.services.ai.gemini_provider import GeminiProvider
from backend.app.services.ai.mock_provider import MockProvider

def get_ai_provider(api_key: Optional[str] = None, force_mock: bool = False) -> AIProvider:
    """
    Factory to retrieve configured AI Provider.
    Enforces strict invariants:
    1. In production, MockProvider is strictly forbidden.
    2. BYOK (client-provided API key) must NEVER fall back to server keys or rotate through server keys.
    3. Server keys are only used when no client key was supplied.
    """
    # 1. Check if mock provider is requested
    is_mock_requested = force_mock or settings.AI_MODE == "mock" or api_key == "mock"
    if is_mock_requested:
        if settings.APP_ENV == "production" or not settings.ALLOW_MOCK_PROVIDERS:
            raise RuntimeError("MockProvider is strictly prohibited in production mode or when ALLOW_MOCK_PROVIDERS=False.")
        return MockProvider(api_key=api_key or "mock-key")

    # 2. BYOK Mode: Client explicitly provided their own API key
    if api_key and api_key.strip() and api_key.lower() not in ("mock", "null", "none"):
        # BYOK must NEVER fall back to or rotate into server keys!
        return GeminiProvider(api_key=api_key.strip(), backup_keys=None)

    # 3. Server Key Mode: Use server-configured keys with rotation among server keys only
    server_keys = settings.all_gemini_keys
    if server_keys:
        return GeminiProvider(api_key=server_keys[0], backup_keys=server_keys[1:] if len(server_keys) > 1 else None)

    # 4. No keys available anywhere
    if settings.APP_ENV == "production" or not settings.ALLOW_MOCK_PROVIDERS:
        raise RuntimeError(
            "FATAL: No Gemini API keys configured on server and no BYOK key provided. "
            "Mock fallback is disabled in production."
        )

    return MockProvider(api_key="mock-key")
