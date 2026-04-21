"""
Tests for /api/news endpoint: response structure, signal distribution,
dominant sentiment detection, and fallback articles.
"""

import pytest

import app as app_module
from app import app as flask_app


@pytest.fixture()
def client():
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as c:
        yield c


def _articles(rate_down=0, rate_up=0, neutral=0):
    result = []
    for i in range(rate_down):
        result.append({
            "title": f"Rate Down {i}", "summary": "", "source": "Test",
            "published": "", "sentiment": "Rate Down", "category": "Rates", "url": "#",
        })
    for i in range(rate_up):
        result.append({
            "title": f"Rate Up {i}", "summary": "", "source": "Test",
            "published": "", "sentiment": "Rate Up", "category": "Economy", "url": "#",
        })
    for i in range(neutral):
        result.append({
            "title": f"Neutral {i}", "summary": "", "source": "Test",
            "published": "", "sentiment": "Neutral", "category": "Economy", "url": "#",
        })
    return result


# ---------------------------------------------------------------------------
# Response structure
# ---------------------------------------------------------------------------

class TestApiNewsStructure:
    def test_returns_200(self, client, monkeypatch):
        monkeypatch.setattr(app_module, "_fetch_news", lambda: _articles(3, 2, 5))
        assert client.get("/api/news").status_code == 200

    def test_has_articles_and_signal_keys(self, client, monkeypatch):
        monkeypatch.setattr(app_module, "_fetch_news", lambda: _articles(3, 2, 5))
        data = client.get("/api/news").get_json()
        assert "articles" in data
        assert "signal" in data

    def test_signal_has_required_keys(self, client, monkeypatch):
        monkeypatch.setattr(app_module, "_fetch_news", lambda: _articles(3, 2, 5))
        data = client.get("/api/news").get_json()
        for key in ("lower_pct", "neutral_pct", "higher_pct", "dominant"):
            assert key in data["signal"]

    def test_articles_list_matches_mocked_count(self, client, monkeypatch):
        monkeypatch.setattr(app_module, "_fetch_news", lambda: _articles(2, 3, 1))
        data = client.get("/api/news").get_json()
        assert len(data["articles"]) == 6


# ---------------------------------------------------------------------------
# Signal distribution
# ---------------------------------------------------------------------------

class TestApiNewsSignal:
    def test_percentages_sum_to_approximately_100(self, client, monkeypatch):
        monkeypatch.setattr(app_module, "_fetch_news", lambda: _articles(3, 2, 5))
        data = client.get("/api/news").get_json()
        s = data["signal"]
        total = s["lower_pct"] + s["neutral_pct"] + s["higher_pct"]
        # Integer rounding can cause ±1 deviation
        assert abs(total - 100) <= 1

    def test_dominant_rate_down_when_majority(self, client, monkeypatch):
        monkeypatch.setattr(app_module, "_fetch_news", lambda: _articles(7, 2, 1))
        data = client.get("/api/news").get_json()
        assert data["signal"]["dominant"] == "Rate Down"

    def test_dominant_rate_up_when_majority(self, client, monkeypatch):
        monkeypatch.setattr(app_module, "_fetch_news", lambda: _articles(1, 7, 2))
        data = client.get("/api/news").get_json()
        assert data["signal"]["dominant"] == "Rate Up"

    def test_dominant_neutral_when_neither_down_nor_up_leads(self, client, monkeypatch):
        # Equal Rate Down and Rate Up — neither dominates, Neutral wins
        monkeypatch.setattr(app_module, "_fetch_news", lambda: _articles(3, 3, 4))
        data = client.get("/api/news").get_json()
        assert data["signal"]["dominant"] == "Neutral"

    def test_lower_pct_reflects_rate_down_proportion(self, client, monkeypatch):
        # 5 Rate Down out of 10 total = 50%
        monkeypatch.setattr(app_module, "_fetch_news", lambda: _articles(5, 3, 2))
        data = client.get("/api/news").get_json()
        assert data["signal"]["lower_pct"] == 50


# ---------------------------------------------------------------------------
# Fallback behavior
# ---------------------------------------------------------------------------

class TestApiNewsFallback:
    def test_fallback_articles_returned_when_fetch_empty(self, client, monkeypatch):
        monkeypatch.setattr(app_module, "_fetch_news", lambda: [])
        data = client.get("/api/news").get_json()
        assert len(data["articles"]) >= 3

    def test_fallback_articles_have_required_fields(self, client, monkeypatch):
        monkeypatch.setattr(app_module, "_fetch_news", lambda: [])
        data = client.get("/api/news").get_json()
        for article in data["articles"]:
            for field in ("title", "sentiment", "category", "source"):
                assert field in article
