# AI Book Writer v3.0 — AI Pipeline & Multi-Agent Architecture

## 1. AI Provider Abstraction

All LLM and image calls are decoupled via the `AIProvider` base interface (`backend/app/services/ai/base.py`):

```python
class AIProvider(ABC):
    async def generate_text(prompt, system_instruction, temperature, max_output_tokens) -> str: ...
    async def generate_structured(prompt, system_instruction, temperature) -> Dict[str, Any]: ...
    async def generate_image(prompt, output_path) -> Dict[str, Any]: ...
```

### Supported Providers:
1. **Google Gemini (`GeminiProvider`):**
   - Utilizes Google GenAI SDK (`google-genai>=1.0.0`).
   - Primary Text Model: `gemini-2.5-flash` (balanced latency and academic depth).
   - High-Complexity Fallback: `gemini-2.5-pro` (used on proofs or difficult derivations).
   - Image Model: `imagen-3.0-generate-002` (generates 16:9 photorealistic scientific illustrations).
   - Exponential Backoff & Retry: Automatically retries on 429 rate limits or 503 server overloads.

2. **Deterministic Mock Provider (`MockProvider`):**
   - Fully offline provider generating compliant structured JSON, technical markdown, and PIL technical schematics.
   - Used for zero-cost automated tests (`pytest`) and local continuous integration.

---

## 2. Centralized Prompt Registry (`prompts/`)

Prompts are separated from application code into parameterized text files with strict anti-filler instructions:

| Template | Purpose | Key Constraints |
|---|---|---|
| `toc_planner.txt` | Table of contents structuring | Strictly academic, no introductory conversational fluff. |
| `chapter_planner.txt` | Chapter introductions & roadmaps | Prerequisites, learning outcomes, thematic breakdown. |
| `content_writer.txt` | Academic subsection text | Mandates mathematical formulations, tables, worked problems. Banned phrases: *"In today's fast-paced world"*, *"Delve"*, *"Tapestry"*. |
| `diagram_planner.txt` | Figure prompt design | Scientific precision, clean labels, choosing between Imagen or Matplotlib. |
| `reviewer.txt` | Editorial peer review | Rigorous grading 1–100 across 5 dimensions. |
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

## 4. Scientific Diagram Generation System

The `DiagramSystem` evaluates whether each subsection requires visual clarification:

1. **Photorealistic & Concept Schematics:**
   - Generated via Google Imagen 3 (`imagen-3.0-generate-002`).
   - Clean, publication-grade academic style with solid dark or white neutral backgrounds.

2. **Deterministic Scientific Plots (Matplotlib):**
   - System dynamics, phase portraits, statistical distributions, Bode plots, and polarization curves are rendered via headless `matplotlib.pyplot` scripts.
   - Rendered as high-DPI (300 DPI) figures.

---

## 5. Peer Review & Quality Scorecard

Every generated section is passed to the `ReviewAgent` which scores the material across 5 distinct axes (0–20 points each, 100 total):
- **Depth & Rigor (0–20):** Sufficient mathematical and conceptual density.
- **Pedagogical Value (0–20):** Clear examples, worked problems, exercise questions.
- **Zero Filler (0–20):** Absence of generic AI clichés and fluff.
- **Technical Accuracy (0–20):** Correct formulas and coherent explanations.
- **Completeness (0–20):** All subtopic points addressed.

If a section scores below 70, the rewrite loop triggers automatically with targeted correction guidance.
