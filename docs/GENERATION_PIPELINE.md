# AI Book Writer v3.0 — Generation Pipeline Execution

The generation process is governed by `BookGenerationPipeline` (`backend/app/workers/pipeline.py`), executing a 14-stage sequence with durable checkpoints.

```
       +-----------------------------------------------------------+
[Stage 1]  Initialize Job & Context Manager
       +-----------------------------------------------------------+
                                   |
[Stage 2]  Verify & Cache Master Table of Contents
                                   |
[Stage 3]  Pre-Flight Model & API Verification
                                   |
[Stage 4]  Check Partial Checkpoints (Resume Capability)
                                   |
[Stage 5]  For Each Unit: Generate Academic Overview & Roadmap
                                   |
[Stage 6]  For Each Subtopic: Retrieve Hierarchical Context
                                   |
[Stage 7]  Generate Academic Content (Equations, Tables, Problems)
                                   |
[Stage 8]  Peer Review Evaluation (Scored 1-100; Rewrite if <70)
                                   |
[Stage 9]  Cross-Chapter Consistency Audit (Nomenclature & Symbols)
                                   |
[Stage 10] Diagram Planning & Execution (Imagen 3 / Matplotlib)
                                   |
[Stage 11] Checkpoint Section to Database & Storage
                                   |
[Stage 12] Final Comprehensive Quality Audit & Metrics Compilation
                                   |
[Stage 13] Production Word Compilation (DOCXEngine & Native Tables)
                                   |
[Stage 14] Asset Registration & Job Completion
```

---

## 1. Step-by-Step Stage Breakdown

### Stage 1: Initialization & Context Manager
- Queries the `Book` record from the database.
- Initializes the `BookContextManager` with metadata (title, academic level, depth, citation style).
- Logs initial event to `GenerationEvent` table.

### Stage 2: Table of Contents Verification
- Traverses the database hierarchy (`BookUnit` -> `BookTopic` -> `BookSubtopic`).
- Calculates total section counts for granular progress reporting.

### Stage 3: Pre-Flight Verification
- Validates that the AI provider is authenticated and operational before beginning lengthy generation loops.

### Stage 4: Partial Recovery & Checkpoint Scan
- Queries `GeneratedSection` for previously written sections associated with this book.
- If a job is retried or resumed, existing sections are loaded into memory and skipped, saving API costs and execution time.

### Stages 5–11: Chapter & Section Generation Loop
- **Unit Overview (Stage 5):** Emits learning objectives, prerequisites, and overarching themes.
- **Hierarchical Context (Stage 6):** Prepares previous chapter summaries so the writer can reference earlier concepts organically.
- **Drafting (Stage 7):** Writes the core text adhering to the target word count and pedagogical structure.
- **Peer Review (Stage 8):** Checks for depth, accuracy, and filler. If the score falls below 70, triggers a revision.
- **Consistency Audit (Stage 9):** Identifies newly introduced terms, acronyms, and symbols, registering them in `BookContextManager`.
- **Diagram Generation (Stage 10):** Generates figures via Imagen 3 or creates a Matplotlib chart.
- **Checkpoint (Stage 11):** Saves the section content and figure paths to disk (`output/sections/`) and database.

### Stage 12: Quality Controller Audit
- Calculates book-wide statistics: total word count, total pages, section completeness percentage, formatting compliance.

### Stage 13: Document Compilation (DOCXEngine)
- Reads `templates/master_book_template.docx` (preserving margins, fonts, and headers).
- Builds formatted cover page and front matter.
- **Native Word Tables:** Detects markdown table structures (`| ... |`) and builds native Word tables with colored headers and alternating zebra row striping.
- Inserts figures with centered captions.
- Applies Arabic numerals to section footers (`Page X of Y`).
- Writes the completed document to `output/<slugified_title>.docx`.

### Stage 14: Job Finalization
- Updates `GenerationJob.status = "COMPLETED"`, sets `progress = 100.0`.
- Inserts `GeneratedAsset` record with download URL.
- Emits final SSE completion event to connected frontend clients.
