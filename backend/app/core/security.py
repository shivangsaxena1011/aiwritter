import os
import re
import html
from typing import Optional
from fastapi import HTTPException
from backend.app.core.config import settings

def sanitize_api_key(key: Optional[str]) -> str:
    """Safely masks API key for logs and responses."""
    if not key:
        return ""
    if len(key) <= 8:
        return "***"
    return f"{key[:4]}...{key[-4:]}"

mask_api_key = sanitize_api_key

def resolve_gemini_api_key(client_provided_key: Optional[str] = None) -> str:
    """
    Resolves Gemini API key with strict isolation:
    - If client provides a key (BYOK), it uses ONLY that key and NEVER falls back to server keys.
    - If no key was provided by client, server environment setting (GEMINI_API_KEY) is used.
    """
    if client_provided_key is not None:
        key = client_provided_key.strip()
        if key and key.lower() not in ("null", "none"):
            return key
        raise HTTPException(
            status_code=400,
            detail="BYOK key was empty or invalid. BYOK requests will never fall back to server keys."
        )

    if settings.GEMINI_API_KEY and settings.GEMINI_API_KEY.strip():
        return settings.GEMINI_API_KEY.strip()

    if settings.APP_ENV == "production" or not settings.ALLOW_MOCK_PROVIDERS:
        raise HTTPException(
            status_code=500,
            detail="No Gemini API key configured on server. Please configure GEMINI_API_KEY or provide a valid BYOK key."
        )

    if settings.AI_MODE == "mock":
        return "mock-key"

    raise HTTPException(
        status_code=400,
        detail="No Gemini API key provided. Please provide an API key in the request or set GEMINI_API_KEY on the server."
    )

def verify_api_auth(
    authorization: Optional[str] = None,
    x_api_key: Optional[str] = None
) -> bool:
    """
    Verifies authentication for private endpoints.
    If AUTH_REQUIRED is enabled or in production with an API_AUTH_SECRET configured,
    requests must provide the matching bearer token or X-API-Key header.
    """
    is_auth_enforced = settings.AUTH_REQUIRED or (settings.APP_ENV == "production" and bool(settings.API_AUTH_SECRET))
    if not is_auth_enforced:
        return True

    expected = settings.API_AUTH_SECRET or settings.SECRET_KEY
    if not expected:
        return True

    # Check X-API-Key header
    if x_api_key and x_api_key.strip() == expected:
        return True

    # Check Authorization: Bearer <token>
    if authorization:
        parts = authorization.strip().split()
        if len(parts) == 2 and parts[0].lower() == "bearer" and parts[1] == expected:
            return True

    raise HTTPException(
        status_code=401,
        detail="Unauthorized: Access to private API requires valid API key or Bearer token.",
        headers={"WWW-Authenticate": "Bearer"}
    )

def sanitize_filename(filename: str) -> str:
    """Sanitizes a filename to remove dangerous path traversal sequences and illegal chars."""
    if not filename:
        return "unnamed_file"
    base, ext = os.path.splitext(filename.strip())
    clean_base = re.sub(r'[\.\/\\\:]+', '', base)
    clean_base = re.sub(r'[^a-zA-Z0-9_\-]', '_', clean_base)
    clean_base = re.sub(r'_+', '_', clean_base).strip('_')
    clean_ext = re.sub(r'[^a-zA-Z0-9]', '', ext.lower())
    if clean_ext:
        return f"{clean_base or 'file'}.{clean_ext}"
    return clean_base or "unnamed_file"

def validate_safe_filename(filename: str) -> str:
    """
    Validates and prevents path traversal or unsafe file access.
    Raises HTTPException(400) if unsafe.
    """
    if not filename or not filename.strip():
        raise HTTPException(status_code=400, detail="Invalid filename")

    clean_name = os.path.basename(filename.strip())

    # Check for path traversal or hidden files
    if ".." in filename or "/" in filename or "\\" in filename or filename.startswith("."):
        raise HTTPException(status_code=400, detail="Path traversal or invalid characters detected in filename")

    # Only allow alphanumeric, underscore, hyphen, and period
    if not re.match(r'^[a-zA-Z0-9_\-\.]+$', clean_name):
        raise HTTPException(status_code=400, detail="Filename contains disallowed characters")

    return clean_name

def validate_safe_path(base_dir: str, filename: str) -> str:
    """
    Validates that resolving filename against base_dir does not traverse outside base_dir.
    Raises ValueError if path traversal is detected.
    """
    if not filename:
        raise ValueError("Filename cannot be empty")

    base_abs = os.path.abspath(base_dir)
    target_abs = os.path.abspath(os.path.join(base_abs, filename))

    # Verify target is inside base_dir
    common = os.path.commonpath([base_abs, target_abs])
    if common != base_abs or target_abs == base_abs:
        raise ValueError(f"Path traversal detected: {filename} resolves outside {base_dir}")

    return target_abs

def safe_slugify(text: str) -> str:
    """Converts a title into a filesystem/URL safe slug."""
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    return text.strip('-') or "untitled-book"

def sanitize_html_content(text: str) -> str:
    """Escapes raw HTML in generated strings to prevent XSS."""
    if not text:
        return ""
    return html.escape(text)
