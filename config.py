import os
from dotenv import load_dotenv

load_dotenv()

NEWSAPI_API_KEY = os.getenv("NEWSAPI_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not NEWSAPI_API_KEY:
    raise RuntimeError("Missing NEWSAPI_API_KEY")

if not OPENROUTER_API_KEY:
    raise RuntimeError("Missing OPENROUTER_API_KEY")
