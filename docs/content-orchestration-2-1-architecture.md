# Content Orchestration 2.1 Architecture Specification
## Final Artifact Integrity & Semantic Assembly

---

## 1. Deep Audit of Current Implementation

### 1.1 Findings Matrix (11 Questions Addressed)

| Question | Current Implementation State | Architectural Vulnerability / Root Cause |
| :--- | :--- | :--- |
| **1. Where content is generated** | `backend/app/workers/pipeline.py` (L450-463) via `ContentWriterAgent.write_section()` delegating to `SubjectKnowledgeModel.generate_academic_section()`. Bibliography generated via `ResearchAgent.generate_bibliography_markdown()`. | Writers return raw Markdown containing embedded headings (`### Heading`), creating split authority between writer markup and document layout. |
| **2. Where sections are assembled** | `pipeline.py` (L657-667) manually appends dictionaries into `compiled_sections: List[Dict[str, Any]]`. | `BookAssemblyModel` was defined in 2.0 but bypassed in `pipeline.py`. Content was passed to the exporter as an untyped dictionary list. |
| **3. Where headings are created** | `backend/app/services/document/docx_engine.py`: L246 (Unit title H1), L250 (Chapter Overview H2), L260 (Topic H2), L264 (Subtopic H3). **AND** inside `_parse_markdown_into_docx` (L357-372) which parses markdown `#`, `##`, `###`, `####`. | **DUPLICATE HEADINGS:** The renderer adds `doc.add_heading(subtopic, level=3)` and then parses the writer's markdown content which ALSO starts with `### {subtopic}`, rendering back-to-back identical headings! |
| **4. Where paragraphs are created** | `docx_engine.py` (L403) inside `_parse_markdown_into_docx`, plus cover page and front matter. | Unfiltered Markdown paragraphs are emitted directly into Word paragraph objects without structural paragraph IDs or semantic tagging. |
| **5. Where tables are created** | Evaluated in `pipeline.py` (L484-495) via `TablePlanner`. Rendered into Word in `docx_engine.py` (L348-354) via `_add_real_word_table`. | Markdown tables that pass the necessity check are converted into native Word tables. However, count reconciliation between planned tables and rendered tables was never enforced. |
| **6. Where diagrams are inserted** | Planned in `pipeline.py` (L615) via `DiagramPlanner`, generated via `DiagramGenerator`, inserted into Word in `docx_engine.py` (L275-276) via `_insert_figure`. | Image files are inserted into Word drawings. Each drawing produces `<w:drawing>` and `<a:blip>`, creating count confusion if XML tags are counted blindly. |
| **7. Where equations are inserted** | Written as LaTeX math `$...$` or `$$...$$` in content; converted to native OMML in `docx_engine.py` via `OMMLEngine.latex_to_omml()`. | Inline and display equations are converted to Office Math XML (`<m:oMath>`). |
| **8. Where repetition detection occurs** | In `pipeline.py` (L496-508) via `RepetitionDetector2.check_candidate()` during drafting loop. | **CRITICAL DEFECT:** Repetition detection ran ONLY on in-memory candidate paragraphs during drafting. It NEVER ran on the final rendered DOCX! |
| **9. What exact object is passed to DOCX renderer** | `docx_exporter.export(...)` receives `sections=compiled_sections` (`List[Dict[str, Any]]`), `toc_data=toc_dict`, and `assets=compiled_assets`. | An untyped list of dictionaries, bypassing `BookAssemblyModel`. |
| **10. What exact artifact the quality gate evaluates** | `AdversarialReviewerAgent.review_chapter(...)` evaluated `compiled_sections` (the in-memory Python list). | The quality gate evaluated the intermediate model, not the rendered DOCX file. |
| **11. Whether quality gate evaluates final DOCX or only internal model** | **ONLY INTERNAL MODEL.** | `validate_docx()` only checked file existence and basic counts, while adversarial review and repetition detection ran solely on in-memory strings. |

### 1.2 Additional Critical Defects Identified

1. **Subject Metadata Leakage as Topic:**  
   In `SyllabusAnalysisAgent.analyze_deterministic()` (L217-220), when the syllabus starts with `B.Tech First Year — Engineering Physics`, that header line was not recognized as subject metadata and was erroneously instantiated as Unit 1 with a full topic of the same name.
2. **Repetition Rate Mathematics Bug:**  
   In `RepetitionDetector2.get_summary()`, `exact_duplicate_rate = count / len(stored_paragraphs)`. When 239 duplicates were rejected while only 99 unique paragraphs were stored, the formula produced `2.4141` (241.41%). The rate must be bounded between `0.0` and `1.0` (or `0% - 100%`) by dividing by `total_evaluated_paragraphs`.
3. **Generic Fallback Section Sets:**  
   The six canonical subtopic names (`Physical Concept and Fundamental Principles`, `Mathematical Formulation...`, etc.) were applied as an ungrounded fallback template rather than driven by explicit semantic necessity contracts.

---

## 2. Core Architecture for Content Orchestration 2.1

```
Syllabus
   ↓
Knowledge Model (Golden Quantum Data)
   ↓
Live Research (CrossRef / Wikipedia)
   ↓
Content Blueprint (TopicBoundaryContract & Purpose)
   ↓
Section Contracts (Specific pedagogical targets)
   ↓
Content Generation (Pure Semantic Content — No Markdown Headings)
   ↓
Validation (Equation, Contamination, Fact-Checking)
   ↓
BookAssemblyModel (Canonical Unified Representation)
   ↓
DOCX Rendering (BookAssemblyModel → Word Elements)
   ↓
RE-OPEN GENERATED DOCX (python-docx / zipfile XML)
   ↓
FINAL ARTIFACT EXTRACTION (Paragraph Inventory & Elements)
   ↓
FINAL ARTIFACT SEMANTIC AUDIT (AdversarialReviewer on Real DOCX)
   ↓
COUNT RECONCILIATION HARD GATE (Planned == Assembled == Rendered)
   ↓
PUBLICATION GATE (publication_ready = true ONLY if DOCX Passes)
```

---

## 3. The Canonical `BookAssemblyModel`

The DOCX renderer will consume exclusively `BookAssemblyModel`.

```python
@dataclass
class AssemblyParagraph:
    paragraph_id: str
    text: str
    style: str = "Normal"
    content_type: str = "prose"  # prose | bullet | callout
    concept_ids: List[str] = field(default_factory=list)
    source_ids: List[str] = field(default_factory=list)

@dataclass
class AssemblyEquation:
    equation_id: str
    latex: str
    is_display: bool = True
    annotation: Optional[str] = None

@dataclass
class AssemblyTable:
    table_id: str
    purpose: str
    headers: List[str]
    rows: List[List[str]]
    caption: str
    entities: List[str] = field(default_factory=list)

@dataclass
class AssemblyFigure:
    figure_id: str
    caption: str
    image_path: str
    diagram_type: str
    required_elements: List[str] = field(default_factory=list)

@dataclass
class AssemblySection:
    section_id: str
    title: str
    purpose: str
    why_this_section_exists: str
    paragraphs: List[AssemblyParagraph]
    equations: List[AssemblyEquation]
    tables: List[AssemblyTable]
    figures: List[AssemblyFigure]
    references: List[str]

@dataclass
class AssemblyTopic:
    topic_id: str
    title: str
    position: int
    sections: List[AssemblySection]

@dataclass
class AssemblyChapter:
    chapter_id: str
    title: str
    position: int
    introduction: str
    learning_objectives: List[str]
    topics: List[AssemblyTopic]

@dataclass
class BookAssemblyModel:
    metadata: Dict[str, Any]
    front_matter: AssemblyFrontMatter
    chapters: List[AssemblyChapter]
    back_matter: AssemblyBackMatter
```

---

## 4. Count Reconciliation & Artifact Integrity Manifest

The `ArtifactIntegrityManifest` tracks counts across all 3 phases:

```text
PLANNED  ==  ASSEMBLED  ==  RENDERED_DOCX
```

| Entity | Planned Source | Assembled Source | Rendered DOCX Source | Hard Gate Condition |
| :--- | :--- | :--- | :--- | :--- |
| **Chapters** | Blueprint Planner | `model.chapters` | Heading 1 (`unit`) count | Exact Match |
| **Topics** | Blueprint Planner | `chapter.topics` | Heading 2 (`topic`) count | Exact Match |
| **Sections** | Section Contracts | `topic.sections` | Heading 3 (`subtopic`) count | Exact Match |
| **Paragraphs** | Contract Paragraph Plans | `section.paragraphs` | Reopened DOCX Normal paragraphs | Reconciled within structural margin |
| **Tables** | TablePlanner Accepted | `section.tables` | Reopened `doc.tables` | Exact Match |
| **Figures** | DiagramPlanner Accepted | `section.figures` | Reopened `<w:drawing>` count | Exact Match |
| **Equations** | Derivations & Contracts | `section.equations` | Reopened `<m:oMath>` count | Reconciled within inline math margin |

Any count mismatch immediately triggers `integrity = "FAIL"` and blocks `publication_ready`.

---

## 5. Reopened DOCX Semantic Audit

After `docx_exporter.export()` writes the `.docx` file:
1. `FinalArtifactExtractor.extract_snapshot(docx_path)` re-opens the file using `python-docx` and XML parsing.
2. Extracts every paragraph into a `FinalParagraphInventory` with `paragraph_id`, `style`, `text`, and normalized tokens.
3. Extracts every heading into a `HeadingInventory` checking for:
   - Consecutive duplicate headings (`Heading \n Heading`)
   - Unwanted cross-topic duplicate headings (`Physical Concept and Fundamental Principles` duplicated across topics)
   - Subject metadata promoted to heading
4. Runs `RepetitionDetector2` on the actual extracted DOCX paragraphs (not intermediate models).
5. Runs `AdversarialReviewerAgent` on the actual extracted DOCX text.
6. Evaluates the Hard Publication Gate:
   ```python
   publication_ready = (
       manifest.integrity == "PASS"
       and count_reconciliation_pass
       and duplicate_headings_count == 0
       and exact_duplicates_count == 0
       and near_duplicates_count == 0
       and conceptual_duplicates_count == 0
       and topic_contamination_count == 0
       and generic_fallback_sections_count == 0
       and adversarial_review.passed
   )
   ```
