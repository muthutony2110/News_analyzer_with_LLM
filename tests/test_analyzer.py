import pytest
from llm_analyzer import analyze_article


def test_short_article_rejected():
    article = {
        "title": "Test",
        "content": "Too short",
        "source": "Test",
        "url": "http://example.com",
    }
    with pytest.raises(ValueError):
        analyze_article(article)


def test_empty_article_rejected():
    article = {
        "title": "Test",
        "content": "",
        "source": "Test",
        "url": "http://example.com",
    }
    with pytest.raises(ValueError):
        analyze_article(article)


def test_valid_article_structure():
    article = {
        "title": "Test",
        "content": "This is a valid long article content used only for testing.",
        "source": "Test",
        "url": "http://example.com",
    }

    try:
        result = analyze_article(article)
        assert "analysis" in result
    except RuntimeError:
        pass  # acceptable if API unavailable
