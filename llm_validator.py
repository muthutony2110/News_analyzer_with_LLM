import requests
from typing import Dict
from config import OPENROUTER_API_KEY


def validate_analysis(article: Dict) -> Dict:
    text = article.get("content")

    prompt = f"""
You are independently analyzing the SAME Indian political article.

Use EXACT same sentiment rules:

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
            "model": "mistralai/mistral-7b-instruct",
            "temperature": 0.2,
            "messages": [{"role": "user", "content": prompt}],
        },
        timeout=30,
    )

    if response.status_code != 200:
        raise RuntimeError("LLM#2 validation failed")

    return {
        "validation": response.json()["choices"][0]["message"]["content"].strip()
    }
