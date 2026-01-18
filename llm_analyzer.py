import requests
from typing import Dict
from config import OPENROUTER_API_KEY


def analyze_article(article: Dict) -> Dict:
    text = article.get("content")

    if not text or len(text) < 80:
        raise ValueError("Article text too short for analysis")

    prompt = f"""
You are analyzing an INDIAN POLITICAL NEWS ARTICLE.

Sentiment rules:
- Positive → clear benefit, progress, success, reform, improvement.
- Negative → harm, criticism, injustice, discrimination, unresolved or long-standing problem.
- Neutral → purely factual reporting with no value judgment.

Return STRICT format:

Gist: <6–7 sentence summary>
Sentiment: positive | negative | neutral
Tone: analytical | urgent | balanced | satirical

Article:
{text}
"""

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": "qwen/qwen-2.5-7b-instruct",
            "temperature": 0.2,
            "messages": [{"role": "user", "content": prompt}],
        },
        timeout=30,
    )

    if response.status_code != 200:
        raise RuntimeError("LLM#1 analysis failed")

    return {
        "analysis": response.json()["choices"][0]["message"]["content"].strip()
    }
