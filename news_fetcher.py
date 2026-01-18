import requests
from typing import List, Dict
from config import NEWSAPI_API_KEY

NEWS_API_URL = "https://newsapi.org/v2/everything"

INDIA_KEYWORDS = [
    "india", "indian", "parliament", "lok sabha", "rajya sabha",
    "election", "elections", "government", "prime minister",
    "chief minister", "state government", "assembly",
    "tamil nadu", "karnataka", "kerala", "maharashtra",
    "west bengal", "uttar pradesh", "delhi", "assam"
]


def limit_words(text: str, max_words: int = 500) -> str:
    return " ".join(text.split()[:max_words])


def india_keyword_score(text: str) -> int:
    text = text.lower()
    return sum(1 for kw in INDIA_KEYWORDS if kw in text)


def fetch_news(
    target_count: int = 10,
    max_pages: int = 8
) -> List[Dict]:

    collected: List[Dict] = []

    for page in range(1, max_pages + 1):

        if len(collected) >= target_count:
            break

        params = {
            "q": "India politics",
            "language": "en",
            "sortBy": "publishedAt",
            "pageSize": 20,
            "page": page,
            "apiKey": NEWSAPI_API_KEY,
        }

        try:
            response = requests.get(NEWS_API_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
        except requests.RequestException:
            continue

        for item in data.get("articles", []):

            if len(collected) >= target_count:
                break

            title = (item.get("title") or "").strip()
            description = (item.get("description") or "").strip()
            content = (item.get("content") or "").strip()

            if not title or not (content or description):
                continue

            full_text = " ".join(p for p in [title, description, content] if p)
            score = india_keyword_score(full_text)

            # ✅ India must dominate
            if score < 2:
                continue

            final_text = limit_words(full_text, 500)

            # ✅ NewsAPI reality: content is short
            if len(final_text.split()) < 70:
                continue

            collected.append({
                "title": title,
                "content": final_text,
                "source": item.get("source", {}).get("name"),
                "url": item.get("url"),
                "published_at": item.get("publishedAt"),
            })

    return collected
