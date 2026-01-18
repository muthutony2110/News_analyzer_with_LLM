# Development Process

## Problem Statement

The goal of this take-home assignment is to build an **AI-assisted news analysis pipeline** focused on **Indian political news**, where:

- News articles are fetched from a real-world API (NewsAPI)
- A primary LLM analyzes each article for:
  - **Gist** (1–2 sentence summary)
  - **Sentiment** (positive / negative / neutral)
  - **Tone** (analytical / urgent / balanced / satirical)
- A secondary LLM validates the primary analysis
- Outputs are saved as structured JSON and a human-readable Markdown report

This mirrors a **real-world fact-checking pipeline**, where AI-generated insights are reviewed instead of blindly trusted.

---

## Overall Design Philosophy

I followed Celltron Intelligence’s **AI-assisted development philosophy**:

- Think first, code second
- Break the problem into small, testable steps
- Use AI as an assistant, not a black box
- Iterate when outputs are weak or inconsistent
- Make design trade-offs explicit and explainable

The pipeline was deliberately broken down into:

**Fetch News → Analyze (LLM#1) → Validate (LLM#2) → Save Results → Generate Report**

Each stage was implemented and refined independently.

---

## Step 1: News Fetching (Data Source)

### Initial Approach
- Used **NewsAPI** as the data source
- Started with broad queries such as `"India politics"`

### Problems Identified
- Foreign news articles mentioning India were included
- Some articles had missing or extremely short content
- NewsAPI does **not provide full article text**, only partial content

### Final Design & Fixes
- Used **India-focused queries** related to politics, government, elections, parliament, and state affairs
- Added strict filtering to:
  - Skip articles with missing or removed content
  - Skip articles that were too short to analyze reliably
- **Important clarification**:
  - The pipeline fetches **all available article content from NewsAPI**
  - **Only the text passed to the LLM is trimmed**, not the fetched data itself

### Context Management (500-word Handling)
- After fetching each article, the following fields are combined:
  - **Title + description + content**
- This combined text is then **truncated to approximately 500 words before being sent to the LLM**
- This ensures:
  - Enough political context for accurate analysis
  - No token overload or unnecessary cost for LLM calls

This reflects a realistic production constraint when working with LLMs.

---

## Step 2: Primary Analysis (LLM#1)

### Model Used
- **I initially attempted Gemini but faced API availability and quota issues, so I migrated to OpenRouter for stability while preserving the dual-LLM validation design.**
- **OpenRouter – Qwen 2.5 Instruct**

### Why This Model
- Stable free-tier access
- Consistent structured outputs
- Performs well on factual and political analysis tasks

### Prompt Design
The prompt enforces a **strict output format**:

- `Gist:` 1–2 sentence summary
- `Sentiment:` positive | negative | neutral
- `Tone:` analytical | urgent | balanced | satirical

### Iterations & Improvements
- Enforced minimum article length before analysis
- Added retry and failure handling
- Refined sentiment definitions:
  - **Positive** → beneficial development or progress
  - **Negative** → criticism, harm, injustice, conflict, failure
  - **Neutral** → factual or informational reporting

The analyzer reasons **only from article content**, not assumptions.

---

## Step 3: Secondary Validation (LLM#2)

### Model Used
- **OpenRouter – Mistral 7B Instruct**

### Purpose
The validator independently:
- Reads the original article text
- Reviews LLM#1’s gist, sentiment, and tone
- Confirms correctness or flags disagreement

### Validation Strategy
- Does not blindly agree with LLM#1
- Can explicitly disagree with sentiment or gist
- Provides short justification when disagreement occurs

This demonstrates **critical review**, not blind trust in AI output.

---

## Step 4: Handling LLM Disagreements

### Observations
- Some political articles are inherently ambiguous
- LLM#1 and LLM#2 occasionally disagreed on sentiment

### Design Decision
- Disagreements are **preserved and shown** in the final report
- No forced reconciliation or override
- Transparency is preferred over artificial consistency

This directly aligns with the idea of **dual LLM validation**.

---

## Step 5: Error Handling & Reliability

Robust error handling was implemented across the pipeline:

- NewsAPI timeouts and request failures
- Empty or insufficient article content
- LLM API failures or rate limits

Failures:
- Do **not crash** the pipeline
- Are logged and skipped safely
- Appear clearly in the output where applicable

---

## Step 6: Testing Strategy

### Tests Implemented
Unit tests focus on **pipeline safety**, not model intelligence:

- Reject empty article content
- Reject very short articles
- Accept valid articles for analysis

### Why Tests Matter
These tests ensure:
- Predictable behavior
- Stability under bad input
- Production-readiness of the pipeline

---

## Step 7: Output & Reporting

### Generated Outputs
- `raw_articles.json` → fetched article data
- `analysis_results.json` → analysis + validation results
- `final_report.md` → human-readable report

### Report Format
The final report strictly follows the required structure:

- Date
- Articles analyzed
- Sentiment summary
- Per-article breakdown:
  - Source
  - Gist
  - LLM#1 sentiment
  - LLM#2 validation
  - Tone

---

## Key Learnings

- Real-world APIs impose unavoidable constraints
- LLM disagreement is expected and valuable
- Prompt discipline greatly improves output quality
- Validation layers are essential for trustworthy AI systems

---

## Future Improvements

- Use a full-text news source or scraper
- Add confidence scores to sentiment
- Introduce scoring metrics between LLM outputs
- Cache LLM responses to reduce API usage

---

## Final Notes

This project demonstrates **disciplined AI-assisted development**.  
AI was used to accelerate execution, but **all design decisions, validations, and trade-offs were engineer-driven**, with transparency and reliability prioritized throughout the pipeline.
