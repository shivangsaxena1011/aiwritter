# AIWritter Content Orchestration 2.0 Architecture

## 1. System Overview & Problem Statement

The previous content generation architecture (v1.x) relied on decomposing a syllabus into subtopics and allowing downstream agents (writer, derivation agent, diagram planner, table generation) to generate content for each subtopic independently. This caused several major structural deficiencies:

1. **Independent Subtopic Regeneration**: When a topic (e.g., "Particle in a 1D Box") was decomposed into 5-6 subtopics, each subtopic generator re-introduced the topic's basic premises, re-derived the governing equation, generated identical energy-level tables, and repeated the same zero-point energy discussion.
2. **Template-Driven Section Artifacts**: Every subtopic was forced into the same rigid mold (Concept, Mathematics, Derivation, Table, Application, Diagram), leading to an explosion of redundant tables (216+ tables) and repetitive diagrams (26+ figures).
3. **Topic Contamination**: Downstream agents lacked topic boundary contracts, causing out-of-context concepts (e.g., laser population inversion, semiconductor bandgaps) to leak into foundational topics (e.g., Photoelectric Effect).
4. **Weak Fact-Check Blocking**: Fact-checking warnings or errors did not block "Publication Ready" status.

## 2. Content Orchestration 2.0 Pipeline

The redesigned pipeline introduces a dependency-aware, content-driven architecture where no section exists simply because a template created it:

```
Syllabus
   ↓
Syllabus Knowledge Graph (BookKnowledgeGraph)
   ↓
Research Synthesis & Claim Evidence (ResearchSynthesis)
   ↓
Topic Intelligence & Boundary Contracts (TopicBoundaryContract)
   ↓
Learning Objectives & Blueprinting (ContentBlueprint & SectionContract)
   ↓
Dependency-Aware Incremental Generation (ContextDelta & ConceptOwnershipRegistry)
   ↓
Necessity-Driven Asset Planning (TablePlanner & DiagramPlanner)
   ↓
Inline Multi-Level Validation & Contamination Check (TopicContaminationDetector, RepetitionDetector 2.0)
   ↓
Self-Correction & Rewrite Loop (SectionValidator)
   ↓
Adversarial Review (AdversarialReviewerAgent)
   ↓
Book-Level Fact Checking & Terminology Enforcement (BookFactCheckAgent, TerminologyRegistry)
   ↓
Strict Publication-Ready Gate (CRITICAL/ERROR/WARNING blocking)
   ↓
Book Assembly Modeling (BookAssemblyModel)
   ↓
Deterministic Document Rendering (DOCX Engine)
```

## 3. Core Architectural Components

### 3.1 ContentBlueprint & SectionContract
Before any writing begins for a topic, a `ContentBlueprint` is created. It defines:
- Specific learning objectives and prerequisites.
- Required, optional, and strictly excluded concepts.
- Explicit flags for whether derivations, experiments, tables, and diagrams are required.
- A concrete sequence of `SectionContract` items, each with a semantic purpose (`HISTORICAL_MOTIVATION`, `CORE_CONCEPT`, `DERIVATION`, `EXPERIMENT`, `APPLICATION`, etc.).

### 3.2 TopicBoundaryContract & TopicContaminationDetector
Every topic has a boundary contract specifying allowed concepts, prerequisite concepts, and forbidden concepts.
The `TopicContaminationDetector` inspects every generated paragraph and rejects any paragraph introducing forbidden concepts or irrelevant physics.

### 3.3 BookKnowledgeGraph & ConceptOwnershipRegistry
Every major physical concept and derivation has a single designated owner topic:
- **Primary Owner**: The only topic allowed to give a full, foundational explanation or full derivation.
- **Secondary References**: Allowed only to reference (`REFERENCE`) or summarize (`SUMMARY`) the concept in context, with full regeneration prohibited.
- `ContextDelta` tracks what has already been introduced, ensuring that subsequent sections only teach incremental knowledge.

### 3.4 TablePlanner & DiagramPlanner (Necessity Logic)
- **Tables**: Generated only when $\ge 3$ entities/attributes require tabular comparison and prose would be less clear. No fixed tables per topic.
- **Diagrams**: Generated only when spatial geometry, energy levels, physical apparatus, or waveforms genuinely aid comprehension.

### 3.5 Multi-Level Repetition Detection
- **Level 1**: Exact duplicate hashing of normalized paragraphs.
- **Level 2**: Near-duplicate detection via token and n-gram similarity ($\ge 0.70$).
- **Level 3**: Conceptual duplication checking matching claim sets, equations, and experimental details.

### 3.6 BookAssemblyModel & Deterministic Rendering
All content generation outputs a clean intermediate representation (`BookAssemblyModel`). The DOCX exporter strictly renders this model without making any independent content decisions.
Front matter (preface, scope) is dynamically generated based on actual configuration (omitting references to numericals or Q&A if those features are disabled).

### 3.7 Strict Publication Gate
The system enforces that any `CRITICAL`, `ERROR`, or unresolved `WARNING` in fact-checking, topic contamination, duplicate content, or unsupported claims strictly sets `publication_ready = False`.
