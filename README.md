# Development Process

## 🎯 Problem Statement
Build an **AI-assisted news analysis pipeline** for **Indian political news** using a dual-LLM approach (Analyze + Validate) to ensure trustworthy results.

---

## 🏗️ Design Philosophy
- **Modular Pipeline:** Fetch → Analyze (LLM#1) → Validate (LLM#2) → Report.
- **Critical Review:** AI outputs are audited by a second model, not blindly trusted.
- **Stability:** Migrated from Gemini to **OpenRouter** (Qwen & Mistral) for reliable API uptime.

---

## 🛠️ Step-by-Step Implementation

### 1. News Fetching & Context
- **Source:** NewsAPI with India-specific political keyword filtering.
- **Refinement:** Skips empty/short content; combines Title + Description + Content.
- **Context Management:** Truncates combined text to **~500 words** for LLM input to balance context vs. token costs.

### 2. Primary Analysis (LLM#1: Qwen 2.5)
- **Role:** Extracts Gist, Sentiment, and Tone.
- **Strategy:** Uses strict output formatting and predefined sentiment boundaries to avoid hallucination.

### 3. Secondary Validation (LLM#2: Mistral 7B)
- **Role:** Independent auditor.
- **Logic:** Reads raw text and flags disagreements with LLM#1. Disagreements are **preserved** in the report for human review.

### 4. Reliability & Testing
- **Error Handling:** Pipeline logs and skips API failures without crashing.
- **Unit Testing:** Focuses on pipeline safety (e.g., rejecting invalid/empty articles).

---

## 📊 Outputs & Insights
- **Files:** `raw_articles.json`, `analysis_results.json`, and `final_report.md`.
- **Key Learning:** Dual-LLM validation is essential for handling the inherent ambiguity of political news.

---

## 🚀 Future Roadmap
- Implement full-text scraping for deeper analysis.
- Add AI confidence scoring and response caching to reduce costs.

**Final Note:** This project demonstrates an engineer-driven approach where AI accelerates the workflow while validation layers ensure system integrity.
