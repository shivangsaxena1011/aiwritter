# AIWritter — REST API Specification

The AIWritter platform provides a versioned REST API mounted at `/api/v1/` alongside Server-Sent Events (SSE) for streaming real-time publishing status.

---

## 1. System Endpoints

### `GET /api/v1/health`
Checks backend health, database connectivity, and configured AI models.

**Response `200 OK`**:
```json
{
  "status": "healthy",
  "app_name": "AIWritter",
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
  "text": "\"Quantum Mechanics\"\n1. Wave Mechanics\n- de Broglie hypothesis\n- Heisenberg uncertainty\n2. Potential Wells",
  "api_key": "AIzaSy... (optional)"
}
```

**Response `200 OK`**:
```json
{
  "title": "Quantum Mechanics",
  "units": [
    {
      "name": "Unit 1: Wave Mechanics",
      "topics": [
        {
          "name": "de Broglie hypothesis and Uncertainty",
          "subtopics": ["de Broglie hypothesis", "Heisenberg uncertainty"]
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
  "title": "Engineering Physics",
  "writing_depth": "Standard",
  "generate_images": true,
  "toc": { "units": [...] }
}
```

**Response `200 OK`**:
```json
{
  "total_units": 6,
  "total_topics": 18,
  "total_subtopics": 54,
  "estimated_words": 150000,
  "estimated_pages": 412,
  "estimated_ai_requests": 65,
  "estimated_image_requests": 54,
  "estimated_minutes": 15
}
```

---

### `POST /api/v1/books`
Registers a new textbook project with full academic publishing controls.

**Request Body**:
```json
{
  "title": "Quantum Mechanics: Theoretical Foundations",
  "subtitle": "An Academic Reference Monograph",
  "author": "Prof. Quantum",
  "academic_level": "Undergraduate",
  "subject": "Physics",
  "writing_depth": "Standard",
  "research_depth": "Standard",
  "citation_style": "IEEE",
  "include_numericals": true,
  "include_questions": true,
  "include_examples": true,
  "include_references": true,
  "generate_images": true,
  "toc": { "units": [...] }
}
```

**Response `201 Created`**:
```json
{
  "id": "c8f2b740-b6df-4a61-8f83-e18d6e3557e2",
  "title": "Quantum Mechanics: Theoretical Foundations",
  "status": "DRAFT",
  "created_at": "2026-09-23T02:00:00Z"
}
```

---

## 3. Job & Execution Endpoints

### `POST /api/v1/jobs`
Enqueues a durable background job for a registered book.

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
Returns current job status (`CREATED`, `QUEUED`, `RUNNING`, `COMPLETED`, `PARTIAL`, `FAILED`), execution stage, progress, and download URLs.

---

### `POST /api/v1/jobs/{job_id}/cancel`
Cancels an active generation job gracefully.

---

### `POST /api/v1/jobs/{job_id}/retry`
Resumes a interrupted or failed generation job utilizing saved checkpoint sections.

---

### `GET /api/v1/jobs/{job_id}/stream`
Server-Sent Events (SSE) stream emitting real-time structured progress updates:
```text
event: message
data: {"event_id": "evt_123", "job_id": "job_01h8x9p3...", "type": "log", "message": "Writing Subtopic: de Broglie Hypothesis", "progress": 25.0, "timestamp": "2026-09-23T02:10:00Z"}
```

---

## 4. File Download & Reports

### `GET /api/v1/files/{filename}`
Streams the finalized Word `.docx` book or `document_quality_report.json` with strict path traversal defenses.

---

## 5. Backward Compatibility (v2 / v1 Clients)

The following routes are transparently maintained for legacy clients:
- `POST /api/generate` -> Wraps `v1/books` + `v1/jobs`
- `POST /api/parse-syllabus` -> Wraps `v1/books/parse-syllabus`
- `GET /api/stream/{task_id}` -> Wraps `v1/jobs/{task_id}/stream`
- `GET /api/download/{filename}` -> Wraps `v1/files/{filename}`
