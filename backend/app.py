"""
AI Book Writer — Backend Entry Point (v3.0 Adapter)
Delegates directly to the modular production FastAPI application in backend.app.main.
"""

from backend.app.main import app

__all__ = ["app"]
