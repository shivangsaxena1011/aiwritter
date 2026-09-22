# AI Book Writer v3.0 — Database Schema & Data Layer

AI Book Writer uses **SQLAlchemy 2.0** ORM supporting both lightweight embedded SQLite (Mode A) and enterprise PostgreSQL (Mode B).

---

## 1. Entity-Relationship Model

```
+---------------+       +------------------+       +------------------+
|     Book      | 1---* |     BookUnit     | 1---* |    BookTopic     |
+---------------+       +------------------+       +------------------+
  |       |                                                  |
  | 1     | 1                                                | 1
  |       |                                                  |
  | *     | *                                                | *
  |     +------------------+                       +------------------+
  |     |  GenerationJob   |                       |   BookSubtopic   |
  |     +------------------+                       +------------------+
  |       |          |                                       |
  |       | 1        | 1                                     | 1
  |       |          |                                       |
  |       | *        | *                                     | *
  |     +---------+ +----------------+             +------------------+
  |     | GenEvt  | | GeneratedAsset |             | GeneratedSection |
  |     +---------+ +----------------+             +------------------+
  v
+------------------+
| GeneratedSection |
+------------------+
```

---

## 2. Table Definitions

### `books`
Stores core metadata and publishing settings for each textbook project.
- `id` (VARCHAR(36), PK): UUID string.
- `title` (VARCHAR(255), Not Null): Book title.
- `subtitle` (VARCHAR(255), Nullable): Optional subtitle.
- `author` (VARCHAR(255)): Author credit or publishing affiliation.
- `academic_level` (VARCHAR(100)): Target level (Undergraduate, Graduate, etc.).
- `target_audience` (VARCHAR(255)): Audience profile.
- `language` (VARCHAR(10)): Defaults to `en`.
- `status` (VARCHAR(50)): `DRAFT`, `PUBLISHED`, `ARCHIVED`.
- `book_metadata` (JSON): Stores writing depth, citation style, image toggles.
- `created_at`, `updated_at` (TIMESTAMP).

### `book_units`
Top-level structural chapters or modules.
- `id` (VARCHAR(36), PK): UUID.
- `book_id` (VARCHAR(36), FK -> `books.id` on delete cascade).
- `position` (INTEGER): Sequence order (1-indexed).
- `title` (VARCHAR(255)): Chapter title.
- `unit_metadata` (JSON): Chapter roadmap, prerequisites, learning outcomes.

### `book_topics`
Sections within a unit.
- `id` (VARCHAR(36), PK).
- `unit_id` (VARCHAR(36), FK -> `book_units.id` on delete cascade).
- `position` (INTEGER): Ordering within unit.
- `title` (VARCHAR(255)): Topic name.

### `book_subtopics`
Subsections within a topic (primary unit of generation).
- `id` (VARCHAR(36), PK).
- `topic_id` (VARCHAR(36), FK -> `book_topics.id` on delete cascade).
- `position` (INTEGER): Ordering within topic.
- `title` (VARCHAR(255)): Subsection title.

### `generation_jobs`
Durable state tracking for generation runs.
- `id` (VARCHAR(36), PK): UUID string.
- `book_id` (VARCHAR(36), FK -> `books.id`).
- `status` (VARCHAR(50)): `QUEUED`, `PLANNING`, `GENERATING`, `REVIEWING`, `FORMATTING`, `EXPORTING`, `COMPLETED`, `FAILED`, `CANCELLED`.
- `progress` (FLOAT): 0.0 to 100.0.
- `current_stage` (VARCHAR(100)): Human-readable task description.
- `current_item` (VARCHAR(255)): Subtopic currently being processed.
- `error` (TEXT): Error message if failed.
- `started_at`, `completed_at`, `created_at`, `updated_at` (TIMESTAMP).

### `generation_events`
Audit log of every pipeline action and event.
- `id` (VARCHAR(36), PK).
- `job_id` (VARCHAR(36), FK -> `generation_jobs.id`).
- `event_type` (VARCHAR(50)): `log`, `stage`, `error`, `complete`.
- `message` (TEXT): Event description.
- `progress` (FLOAT).
- `event_metadata` (JSON).
- `created_at` (TIMESTAMP).

### `generated_sections`
Checkpointed section text and review scores for partial recovery.
- `id` (VARCHAR(36), PK).
- `book_id` (VARCHAR(36), FK -> `books.id`).
- `subtopic_id` (VARCHAR(36), Nullable).
- `unit_name`, `topic_name`, `subtopic_name` (VARCHAR(255)).
- `content` (TEXT): Generated markdown.
- `word_count` (INTEGER).
- `review_score` (FLOAT): 0.0 to 100.0.
- `image_path` (VARCHAR(500), Nullable).
- `status` (VARCHAR(50)): `DRAFT`, `ACCEPTED`, `REVISED`.

### `generated_assets`
Published document files (.docx, .pdf).
- `id` (VARCHAR(36), PK).
- `job_id` (VARCHAR(36), FK -> `generation_jobs.id`).
- `type` (VARCHAR(50)): `docx`, `pdf`, `image`.
- `url` (VARCHAR(500)): Local file URL or cloud storage URI.
- `file_size` (BIGINT).
- `created_at` (TIMESTAMP).

---

## 3. Database Initialisation & Migrations

- Automatically calls `Base.metadata.create_all(bind=engine)` upon application startup (`init_db()`).
- In SQLite mode, enables `PRAGMA foreign_keys=ON;` and WAL journal mode.
- In PostgreSQL mode, supports connection pooling (`pool_size=10`, `max_overflow=20`).
