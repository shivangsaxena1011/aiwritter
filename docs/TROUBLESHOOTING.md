# AI Book Writer v3.0 — Troubleshooting & Operations FAQ

## 1. Google Gemini API Issues

### `429 Too Many Requests / Resource Exhausted`
- **Cause:** Exceeding Google Gemini API quotas for requests per minute (RPM) or tokens per minute (TPM).
- **Solution:**
  - AI Book Writer includes built-in exponential backoff retrying up to `MAX_RETRIES` (default: 3) with jitter.
  - Lower the depth tier from `Reference` or `Deep Academic` to `Standard` or `Detailed` in the Book Setup form.
  - Switch to a paid tier Google Cloud Project Gemini API key.
  - Set `MAX_CONCURRENT_JOBS=1` in `.env` to avoid multi-job resource contention.

### `Unexpected token 'A', "A server e"... is not valid JSON`
- **Cause:** Occurs if an upstream proxy or server crashes and returns an HTML error page (e.g. *"A server error occurred"*) instead of JSON.
- **Solution:**
  - In v3.0, the `ApiClient` (`frontend/api.js`) catches non-JSON responses and extracts the HTTP status text gracefully.
  - Check the backend terminal console for tracebacks.
  - Verify that the Gemini API key provided has valid permissions.

---

## 2. Document & Template Issues

### `templates/master_book_template.docx Not Found`
- **Behavior:** The engine automatically creates a fresh clean `Document()` if the template is absent.
- **To Restore:** Place a standard formatted Word document with predefined typography styles at `templates/master_book_template.docx`.

### Markdown Tables Rendered as Raw Text
- **In v2:** Tables were sometimes inserted as monospace code blocks.
- **In v3:** `DOCXExporter` automatically parses markdown table headers and rows, converting them into native Word tables with styled borders and cell shading.

---

## 3. Database & Concurrency Issues

### `database is locked` (SQLite)
- **Cause:** Multiple concurrent processes writing to SQLite without WAL mode.
- **Solution:**
  - The v3 database initialization automatically runs `PRAGMA journal_mode=WAL;` and `PRAGMA busy_timeout=5000;`.
  - For high-volume production deployments with multiple workers, switch to PostgreSQL by setting `DATABASE_URL` in `.env`.

---

## 4. Pipeline Resume & Partial Recovery

### How do I resume an interrupted job?
1. If generation fails due to a network drop, click the **Resume / Retry** button in the generation progress view.
2. The pipeline scans `GeneratedSection` in the database and skips sections that have already been generated and reviewed.
3. Generation will continue seamlessly from the last incomplete section.
