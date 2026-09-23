# AIWritter — AI Pipeline & Multi-Agent Architecture

AIWritter decouples textbook generation across 15 specialized agents. LLM and image calls are unified via the `AIProvider` base interface (`backend/app/services/ai/base.py`).

---

## 1. AI Provider Abstraction

```python
class AIProvider(ABC):
    async def generate_text(prompt, system_instruction, temperature, max_output_tokens) -> str: ...
    async def generate_structured(prompt, system_instruction, temperature) -> Dict[str, Any]: ...
    async def generate_image(prompt, output_path) -> Dict[str, Any]: ...
```

### Supported Providers:
1. **Google Gemini (`GeminiProvider`):**
   - Utilizes Google GenAI SDK (`google-genai>=1.0.0`).
   - Primary Text Model: Configurable via `GEMINI_TEXT_MODEL` (default: `gemini-2.5-flash`).
   - Image Model: Configurable via `GEMINI_IMAGE_MODEL` (default: `imagen-3.0-generate-002`).
   - Exponential Backoff & Retry: Automatically retries on 429 rate limits or 503 server overloads.
2. **Deterministic Mock Provider (`MockProvider`):**
   - Fully offline provider generating compliant structured JSON, technical markdown, and PIL technical schematics.
   - Used for zero-cost automated tests (`pytest`) and local continuous integration.

---

## 2. Centralized Prompt Registry (`prompts/`)

Prompts are separated from application code into parameterized text files with strict anti-filler instructions:

| Template | Purpose | Key Constraints |
|---|---|---|
| `syllabus_analysis.txt` | Syllabus analysis & topic decomposition | Extracts subject, level, units, and topics with zero omissions. |
| `topic_blueprints.txt` | Domain blueprint expansion | Specialized blueprints for Physics, CS, Math, and Engineering. |
| `chapter_planner.txt` | Chapter introductions & roadmaps | Prerequisites, learning outcomes (Bloom's Taxonomy), pedagogical flow. |
| `content_writer.txt` | Academic subsection text | Paragraph-first, strictly limits bullet points, mandates LaTeX and tables. Anti-AI clichés enforced. |
| `derivation_agent.txt` | Mathematical derivations | Starting Equation → Assumptions → Step-by-Step Transformations → Final Result. |
| `diagram_planner.txt` | Figure prompt design | High-contrast monochrome line art, chapter-aware captions (`Figure X.Y`). |
| `reviewer.txt` | Editorial peer review | Rigorous grading 1–100 across 5 dimensions. Scores < 75 trigger rewrite loop. |
| `fact_check.txt` | Claim categorization | Classifies assertions: Verified, Needs Review, Conflicting, Unsupported. |
| `consistency_checker.txt` | Cross-chapter audit | Verifies variable notation ($E$, $V$, $T$), unit conventions, acronyms. |
| `quality_controller.txt` | Final publication audit | Verifies word budgets, chapter completeness, formatting standards. |

---

## 3. Chapter Depth Controller

The `ChapterDepthController` regulates section length, token consumption, and academic density across 5 tiers:

| Tier | Target Words/Section | Max Tokens | Target Use Case |
|---|---|---|---|
| **Concise** | 750 words | 4,000 | Fast review, introductory surveys, executive briefings |
| **Standard** | 1,500 words | 6,000 | Undergraduate textbooks, foundational coursework |
| **Detailed** *(Default)* | 2,800 words | 10,000 | In-depth university reference, derivations, tables |
| **Deep Academic** | 4,200 words | 14,000 | Graduate monographs, exhaustive proofs, case studies |
| **Reference** | 5,500 words | 16,000 | Comprehensive handbook, industry standards, encyclopedic |

---

## 4. Editorial Review & Quality Scorecard

Every generated section is passed to the `ContentReviewAgent` which scores the material across 5 distinct axes (0–20 points each, 100 total):
- **Depth & Rigor (0–20):** Sufficient mathematical and conceptual density.
- **Pedagogical Value (0–20):** Clear examples, worked problems, exercise questions.
- **Zero Filler (0–20):** Absence of generic AI clichés and conversational fluff.
- **Technical Accuracy (0–20):** Correct formulas and coherent explanations.
- **Completeness (0–20):** All subtopic points addressed.

If a section scores below **75**, the rewrite loop triggers automatically with targeted correction guidance, up to `MAX_CONTENT_REVIEW_RETRIES` (default: 2).
