# AI Book Writer v3.0 — Security & Privacy Architecture

Security and privacy are core architectural tenets of AI Book Writer v3.0.

---

## 1. Path Traversal & File Access Defenses

All file serving and storage operations pass through rigorous path sanitization in `backend/app/core/security.py`:

```python
def validate_safe_path(base_dir: str, filename: str) -> str:
    """Verifies target path strictly resides within the approved base directory."""
    base_abs = os.path.abspath(base_dir)
    target_abs = os.path.abspath(os.path.join(base_abs, filename))
    common = os.path.commonpath([base_abs, target_abs])
    if common != base_abs or target_abs == base_abs:
        raise ValueError(f"Path traversal detected: {filename} resolves outside {base_dir}")
    return target_abs
```

### Protection Measures:
- Explicit rejection of `../`, `..\\`, absolute paths (`/etc/passwd`, `C:\Windows\...`), and null bytes.
- Download endpoint `/api/v1/files/{filename}` strips dangerous symbols and verifies file existence strictly within `STORAGE_LOCAL_DIR`.
- Only approved file extensions (`.docx`, `.pdf`, `.png`, `.jpg`) can be streamed to clients.

---

## 2. API Key Isolation & Privacy Guarantee

1. **Zero Client Storage:**
   The frontend application explicitly prevents storing user Gemini API keys in browser `localStorage` or `sessionStorage`. Even when textbook drafts are autosaved, credentials remain strictly isolated in runtime form memory.

2. **Zero Database Persistence:**
   The `Book` and `GenerationJob` database schemas do **not** have an `api_key` column. Keys are injected directly into the ephemeral background worker pipeline execution context and discarded when the job concludes.

3. **Masking & Log Scrubbing:**
   The logging infrastructure filters secret credentials using `mask_api_key()`:
   ```
   AIzaSy1234567890abcdef -> AIza...cdef
   ```

---

## 3. Strict Input Validation & Schema Bounds

All inbound API payloads are validated via **Pydantic v2**:
- `ParseSyllabusRequest`: Enforces minimum length (5 chars) and maximum length (50,000 chars) to prevent prompt injection or memory exhaustion attacks.
- `TableOfContentsSchema`: Enforces minimum of 1 unit, with validated character bounds on titles.
- `Content-Type` validation: Only JSON payloads are accepted on API mutation endpoints.

---

## 4. Cross-Origin Resource Sharing (CORS)

Configured via `backend/app/core/config.py`:
- In local development, defaults to `*`.
- In production, set `CORS_ORIGINS="https://yourdomain.com,https://your-frontend.vercel.app"` to restrict access.
