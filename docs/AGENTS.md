# AIWritter — Multi-Agent System Architecture & Specifications

AIWritter operates on a specialized multi-agent publishing pipeline. Rather than a single generative prompt, each stage of textbook production is owned by an autonomous, role-specific agent with strict input/output contracts, validation loops, and shared memory.

---

## 1. Agent Base Contracts

All agents inherit from `BaseAgent` (`backend/app/agents/base.py`) and operate with standardized contexts and results:

```python
class AgentContext(BaseModel):
    job_id: str
    book_id: str
    book_title: str
    subject: Optional[str]
    academic_level: str = "Undergraduate"
    writing_depth: str = "Standard"
    research_depth: str = "Standard"
    citation_style: str = "IEEE"
    include_numericals: bool = True
    include_questions: bool = True
    include_examples: bool = True
    include_references: bool = True
    generate_images: bool = True

class AgentResult(BaseModel):
    status: str  # "success", "partial", "failed"
    data: Dict[str, Any]
    error: Optional[str] = None
    metadata: Dict[str, Any] = {}
```

---

## 2. Agent Catalog & Responsibilities

| # | Agent Name | Source File | Core Role & Responsibilities |
|---|------------|-------------|------------------------------|
| 1 | **SyllabusAnalysisAgent** | `backend/app/agents/syllabus_analysis_agent.py` | Parses unstructured syllabi, course outlines, and topics. Extracts subject domain, academic level, and units/topics with zero omissions. |
| 2 | **TopicDecompositionAgent** | `backend/app/agents/topic_decomposition_agent.py` | Expands units into hierarchical chapter blueprints using domain blueprints (Physics, CS, Math, Engineering). Ensures mathematical depth and lab contexts. |
| 3 | **ResearchAgent** | `backend/app/agents/research_agent.py` | Gathers authoritative academic notes, tracks source attribution, formats IEEE/APA bibliographies, and performs 6-gram originality audits. |
| 4 | **ContentPlanningAgent** | `backend/app/agents/content_planning_agent.py` | Constructs pedagogical roadmaps, chapter overviews, learning objectives (Bloom's Taxonomy), and prerequisite structures. |
| 5 | **ContentWriterAgent** | `backend/app/agents/content_writer_agent.py` | Generates exhaustive, paragraph-first academic prose. Filters out banned AI tropes, enforces formula contexts, and constructs markdown tables. |
| 6 | **DerivationAgent** | `backend/app/agents/derivation_agent.py` | Structures formal mathematical proofs and derivations: Starting Equation → Physical Assumptions → Step-by-Step Transformations → Final Result. |
| 7 | **DiagramPromptAgent** | `backend/app/agents/diagram_prompt_agent.py` | Enforces publication-grade black-and-white monochrome diagram prompts. Strictly bans cartoonish, photorealistic, or decorative graphics. |
| 8 | **DiagramPlannerAgent** | `backend/app/agents/diagram_system.py` | Evaluates if a section requires visual aids. Assigns modality (chart vs. illustration) and generates chapter-aware captions (`Figure X.Y — ...`). |
| 9 | **DiagramGeneratorAgent** | `backend/app/agents/diagram_system.py` | Coordinates asset production: attempts AI image generation, falls back to deterministic Matplotlib figures, or outputs formatted callouts. |
| 10 | **ContentReviewAgent** | `backend/app/agents/review_agent.py` | Evaluates draft sections against an academic rubric (Depth, Pedagogy, Filler, Accuracy, Completeness). Triggers rewrite loops on low scores. |
| 11 | **FactCheckAgent** | `backend/app/agents/fact_check_agent.py` | Extracts factual and empirical claims, categorizing them as Verified, Needs Review, Conflicting, or Unsupported. |
| 12 | **BookConsistencyAgent** | `backend/app/agents/consistency_auditor.py` | Tracks terminology, notation conventions, and acronym definitions across chapters to maintain absolute stylistic cohesion. |
| 13 | **DocumentStructureAgent** | `backend/app/agents/document_structure_agent.py` | Plans the canonical academic textbook layout: Cover, Title, Copyright, Preface, TOC, Chapters, Appendices, Glossary, References, and Index. |
| 14 | **DOCXExportEngine** | `backend/app/services/document/docx_engine.py` | Assembles native Word `.docx` documents adhering to strict typography (Times New Roman, 12pt body, 1.5 line spacing, Justified alignment, native tables, OMML equations). |
| 15 | **DocumentValidationAgent** | `backend/app/agents/document_validation_agent.py` | Programmatically inspects the generated `.docx` file for typography compliance, table shading, equation XML tags, image captions, and syllabus coverage. |

---

## 3. Inter-Agent Communication & Data Flow

```
[Raw Syllabus]
      │
      ▼
SyllabusAnalysisAgent ────► TopicDecompositionAgent
                                   │
                                   ▼
                         ContentPlanningAgent
                                   │
                     ┌─────────────┴─────────────┐
                     ▼                           ▼
               ResearchAgent            ConsistencyAuditor
                     │                           │
                     ▼                           ▼
            ContentWriterAgent ◄───────── DerivationAgent
                     │
         ┌───────────┴───────────┐
         ▼                       ▼
DiagramPlannerAgent     ContentReviewAgent ──(Fail: <75)──┐
         │                       │                        │
         ▼                       ▼                        ▼
DiagramGeneratorAgent    FactCheckAgent          [Rewrite Loop]
         │                       │
         └───────────┬───────────┘
                     ▼
         DocumentStructureAgent
                     │
                     ▼
              DOCXExportEngine
                     │
                     ▼
          DocumentValidationAgent
                     │
                     ▼
       [Production .docx + Quality Report]
```

---

## 4. Multi-Agent Feedback Loops & Quality Control

### Review Loop
1. `ContentWriterAgent` drafts a section.
2. `ContentReviewAgent` inspects the text against 5 dimensions:
   - **Depth Score** (Max 20): Level of technical rigor.
   - **Pedagogy Score** (Max 20): Explanatory flow, examples, clarity.
   - **Filler Penalty** (Max 20): Absence of conversational AI filler.
   - **Accuracy Score** (Max 20): Soundness of theoretical statements.
   - **Completeness Score** (Max 20): Inclusion of all required subtopics.
3. If `overall_score < 75`, a targeted rewrite prompt is sent to `ContentWriterAgent` with specific issues and corrections.
4. Up to `MAX_CONTENT_REVIEW_RETRIES` (default: 2) attempts are made before accepting the best result.

### Consistency Audit
1. `BookConsistencyAgent` parses every completed chapter.
2. It extracts newly defined terms (e.g., *Hamiltonian operator*) and acronyms (e.g., *QED*).
3. Subsequent chapters receive these definitions in their generation context to prevent conflicting nomenclature.
