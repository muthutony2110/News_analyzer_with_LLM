import json
import time
import re
from pathlib import Path
from datetime import date

from news_fetcher import fetch_news
from llm_analyzer import analyze_article
from llm_validator import validate_analysis

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)


# ---------- HELPERS ----------

def normalize_sentiment(raw: str) -> str:
    """
    Normalize LLM sentiment output into:
    positive | negative | neutral
    """
    if not raw:
        return "neutral"

    text = raw.lower()

    if "positive" in text:
        return "positive"
    if "negative" in text:
        return "negative"
    if "neutral" in text:
        return "neutral"

    # fallback safety
    return "neutral"


def parse_llm_output(text: str) -> dict:
    """
    Extract gist, sentiment, tone from LLM output.
    """
    result = {
        "gist": "N/A",
        "sentiment": "neutral",
        "tone": "analytical",
    }

    for line in text.splitlines():
        lower = line.lower().strip()

        if lower.startswith("gist"):
            result["gist"] = line.split(":", 1)[1].strip()

        elif lower.startswith("sentiment"):
            raw = line.split(":", 1)[1].strip()
            result["sentiment"] = normalize_sentiment(raw)

        elif lower.startswith("tone"):
            result["tone"] = line.split(":", 1)[1].strip().lower()

    return result


# ---------- MAIN PIPELINE ----------

def main():
    print("\n[INFO] Fetching news articles from NewsAPI...\n")
    articles = fetch_news()
    print(f"[INFO] ✔ Fetched {len(articles)} articles\n")

    with open(OUTPUT_DIR / "raw_articles.json", "w", encoding="utf-8") as f:
        json.dump(articles, f, indent=2)

    results = []

    for idx, article in enumerate(articles, start=1):
        print(f"[{idx}/{len(articles)}] Processing article: {article['title']}")

        # ---------- LLM #1 ANALYSIS ----------
        print(f"[{idx}/{len(articles)}] → Running LLM#1 (Analyzer)")
        try:
            llm1_raw = analyze_article(article)["analysis"]
        except Exception as e:
            print(f"[ERROR] Analyzer failed: {e}\n")
            continue

        llm1 = parse_llm_output(llm1_raw)

        # ---------- LLM #2 VALIDATION ----------
        print(f"[{idx}/{len(articles)}] → Running LLM#2 (Validator)")
        try:
            llm2_raw = validate_analysis(article)["validation"]
        except Exception as e:
            print(f"[ERROR] Validator failed: {e}\n")
            continue

        llm2 = parse_llm_output(llm2_raw)

        # ---------- DECISION ----------
        if llm1["sentiment"] == llm2["sentiment"]:
            final_sentiment = llm1["sentiment"]
            validation_status = "✓ Agreed"
        else:
            final_sentiment = llm2["sentiment"]
            validation_status = "✗ Corrected by LLM#2"

        results.append({
            "title": article["title"],
            "url": article["url"],
            "llm1": llm1,
            "llm2": llm2,
            "final_sentiment": final_sentiment,
            "validation_status": validation_status,
        })

        time.sleep(2)  # polite rate limiting

    with open(OUTPUT_DIR / "analysis_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    generate_report(results)

    print("\n[INFO] Pipeline completed successfully.")
    print("[INFO] Output files generated in /output directory\n")


# ---------- REPORT GENERATION ----------

def generate_report(results):
    today = date.today().isoformat()

    sentiment_counts = {"positive": 0, "negative": 0, "neutral": 0}

    for item in results:
        sentiment_counts[item["final_sentiment"]] += 1

    lines = [
        "# News Analysis Report\n\n",
        f"**Date:** {today}\n",
        f"**Articles Analyzed:** {len(results)}\n",
        "**Source:** NewsAPI\n\n",
        "## Summary\n",
        f"- Positive: {sentiment_counts['positive']} articles\n",
        f"- Negative: {sentiment_counts['negative']} articles\n",
        f"- Neutral: {sentiment_counts['neutral']} articles\n\n",
        "## Detailed Analysis\n\n",
    ]

    for idx, item in enumerate(results, start=1):
        lines.extend([
            f"### Article {idx}: \"{item['title']}\"\n",
            f"- **Source:** {item['url']}\n",
            f"- **LLM#1 Gist:** {item['llm1']['gist']}\n",
            f"- **LLM#1 Sentiment:** {item['llm1']['sentiment'].capitalize()}\n\n",
            f"- **LLM#2 Gist:** {item['llm2']['gist']}\n",
            f"- **LLM#2 Sentiment:** {item['llm2']['sentiment'].capitalize()}\n",
            f"- **Validation:** {item['validation_status']}\n\n",
            f"- **Final Sentiment Used:** {item['final_sentiment'].capitalize()}\n",
            f"- **Tone:** {item['llm1']['tone'].capitalize()}\n\n",
        ])

    with open(OUTPUT_DIR / "final_report.md", "w", encoding="utf-8") as f:
        f.writelines(lines)


if __name__ == "__main__":
    main()
