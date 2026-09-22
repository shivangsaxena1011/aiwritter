# AI Book Writer v3.0 — REST API Specification

The AI Book Writer platform provides a versioned REST API mounted at `/api/v1/` alongside Server-Sent Events (SSE) for streaming generation status.

---

## 1. System Endpoints

### `GET /api/v1/health`
Checks backend health, database connectivity, and configured AI models.

**Response `200 OK`**:
```json
{
  "status": "healthy",
  "app_name": "AI Book Writer",
  "version": "3.0.0",
  "env": "production",
  "ai_mode": "gemini",
  "text_model": "gemini-2.5-flash",
  "image_model": "imagen-3.0-generate-002"
}
```

---

## 2. Books & Syllabus Endpoints

### `POST /api/v1/books/parse-syllabus`
Extracts hierarchical Table of Contents from unstructured syllabus text, numbered outlines, or markdown headings.

**Request Body**:
```json
{
  "text": "\"Fuel Cell Technology\"\n1. Chapter 1: Introduction\n- Overview\n- Types",
  "api_key": "AIzaSy... (optional)"
}
```

**Response `200 OK`**:
```json
{
  "title": "Fuel Cell Technology",
  "units": [
    {
      "name": "Unit 1: Introduction",
      "topics": [
        {
          "name": "Overview and Types",
          "subtopics": ["Overview", "Types"]
        }
      ]
    }
  ]
}
```

---

### `POST /api/v1/books/estimate`
Calculates pre-generation estimates for words, pages, duration, and AI requests based on the selected depth tier.

**Request Body**:
```json
{
  "title": "Machine Learning Systems",
  "writing_depth": "Detailed",
  "generate_images": true,
  "toc": { "units": [...] }
}
```

**Response `200 OK`**:
```json
{
  "total_units": 8,
  "total_topics": 24,
  "total_subtopics": 72,
  "estimated_words": 208000,
  "estimated_pages": 547,
  "estimated_ai_requests": 85,
  "estimated_image_requests": 72,
  "estimated_minutes": 18
}
```

---

### `POST /api/v1/books`
Creates and registers a new textbook structure and hierarchy in the database.

**Request Body**:
```json
{
  "title": "Quantum Computing",
  "subtitle": "Foundations and Algorithms",
  "author": "AI Academic Press",
  "academic_level": "Graduate",
  "writing_depth": "Detailed",
  "citation_style": "IEEE",
  "generate_images": true,
  "toc": { "units": [...] }
}
```

**Response `201 Created`**:
```json
{
  "id": "c8f2b740-b6df-4a61-8f83-e18d6e3557e2",
  "title": "Quantum Computing",
  "status": "DRAFT",
  "created_at": "2026-09-23T02:00:00Z"
}
```

---

## 3. Job & Execution Endpoints

### `POST /api/v1/jobs`
Enqueues a durable background job for a book.

**Request Body**:
```json
{
  "book_id": "c8f2b740-b6df-4a61-8f83-e18d6e3557e2",
  "api_key": "AIzaSy... (optional)"
}
```

**Response `201 Created`**:
```json
{
  "id": "job_01h8x9p3...",
  "book_id": "c8f2b740-b6df-4a61-8f83-e18d6e3557e2",
  "status": "QUEUED",
  "progress": 0.0,
  "current_stage": "Queued in background worker",
  "download_url": null
}
```

---

### `GET /api/v1/jobs/{job_id}`
Returns current job status, execution stage, error messages, and completed download URL.

---

### `POST /api/v1/jobs/{job_id}/cancel`
Cancels an active generation job.

---

### `POST /api/v1/jobs/{job_id}/retry`
Resumes a failed or cancelled generation job with partial recovery.

---

### `GET /api/v1/jobs/{job_id}/stream`
Server-Sent Events (SSE) real-time stream emitting live pipeline events:
- `event: data` with JSON payloads:
  ```json
  {
    "type": "log",
    "message": "Writing Section 2.1.1: Gibbs Free Energy",
    "progress": 32.5,
    "metadata": { "unit": "Unit 2", "subtopic": "Gibbs Free Energy" }
  }
  ```
- Includes automatic `: keepalive` pings every 2 seconds.

---

## 4. File Download Endpoints

### `GET /api/v1/files/{filename}`
Safely streams generated `.docx` or `.pdf` artifacts with path-traversal prevention.

---

## 5. Backward Compatibility (v2 / v1 Clients)

The following routes are transparently maintained for legacy clients:
- `POST /api/generate` -> Wraps `v1/books` + `v1/jobs`
- `POST /api/parse-syllabus` -> Wraps `v1/books/parse-syllabus`
- `GET /api/stream/{task_id}` -> Wraps `v1/jobs/{task_id}/stream`
- `GET /api/download/{filename}` -> Wraps `v1/files/{filename}`
