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
    Resolves Gemini API key with priority:
    1. Client provided key (for self-hosted / personal mode)
    2. Server environment setting (GEMINI_API_KEY)
    """
    if client_provided_key and client_provided_key.strip():
        return client_provided_key.strip()
    if settings.GEMINI_API_KEY and settings.GEMINI_API_KEY.strip():
        return settings.GEMINI_API_KEY.strip()
    if settings.AI_MODE == "mock":
        return "mock-key"
    raise HTTPException(
        status_code=400,
        detail="No Gemini API key provided. Please provide an API key in the request or set GEMINI_API_KEY on the server."
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
