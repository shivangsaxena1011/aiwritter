# AIWritter — Troubleshooting & Operations FAQ

## 1. Google Gemini API Issues

### `429 Too Many Requests / Resource Exhausted`
- **Cause:** Exceeding Google Gemini API quotas for requests per minute (RPM) or tokens per minute (TPM).
- **Solution:**
  - AIWritter includes built-in exponential backoff retrying up to `MAX_RETRIES` (default: 3) with jitter.
  - Lower the depth tier from `Reference` or `Deep Academic` to `Standard` or `Detailed` in the Book Setup form.
  - Switch to a paid tier Google Cloud Project Gemini API key.
  - Set `MAX_CONCURRENT_JOBS=1` in `.env` to avoid multi-job resource contention.

### `Unexpected token 'A', "A server e"... is not valid JSON`
- **Cause:** Occurs if an upstream proxy or server crashes and returns an HTML error page (e.g. *"A server error occurred"*) instead of JSON.
- **Solution:**
  - The `ApiClient` (`frontend/api.js`) catches non-JSON responses and extracts the HTTP status text gracefully.
  - Check the backend terminal console for tracebacks.
  - Verify that the Gemini API key provided has valid permissions.

---

## 2. Document & Mathematical Rendering Issues

### Missing OMML Equations / Display Equations Treated as Monospace
- **Behavior:** Older exporters treated formulas as raw `$$...$$` text.
- **Solution:** AIWritter's `OMMLEngine` parses LaTeX into native Word OMML XML elements (`<m:oMathPara>`). Ensure `python-docx` has write access to document XML.

### Matplotlib GUI / Backend Errors on Headless Servers
- **Cause:** Running Matplotlib on headless Linux or background Windows services without an active display server.
- **Solution:** AIWritter explicitly enforces `matplotlib.use("Agg")` across all visual and diagram agents prior to importing pyplot.

### Markdown Tables Rendered as Raw Monospace Text
- **In older versions:** Tables were sometimes inserted as monospace code blocks.
- **In AIWritter:** `DOCXExportEngine` automatically parses markdown table headers and rows, converting them into native Word tables (`<w:tbl>`) with dark slate header shading (`#1E293B`) and alternating row fills.

---

## 3. Database & Concurrency Issues

### `database is locked` (SQLite)
- **Cause:** Multiple concurrent processes writing to SQLite without WAL mode.
- **Solution:**
  - AIWritter database initialization automatically runs `PRAGMA journal_mode=WAL;` and `PRAGMA busy_timeout=5000;`.
  - For high-volume production deployments with multiple workers, switch to PostgreSQL by setting `DATABASE_URL` in `.env`.

---

## 4. Pipeline Resume & Partial Recovery

### How do I resume an interrupted job?
1. If generation fails due to a network drop, click the **Resume / Retry** button in the generation progress view or call `POST /api/v1/jobs/{job_id}/retry`.
2. The pipeline scans `GeneratedSection` in the database and skips sections that have already been generated and reviewed.
3. Generation will continue seamlessly from the last incomplete section.
