"""
Tests for /api/forecast endpoint: trend direction, RSI range,
projection CI ordering, and error paths.
"""

import numpy as np
import pandas as pd
import pytest

import app as app_module
from app import app as flask_app


@pytest.fixture()
def client():
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as c:
        yield c


@pytest.fixture(autouse=True)
def clear_cache():
    app_module._cache.clear()
    yield
    app_module._cache.clear()


def _make_standard_df(n=60):
    dates = pd.date_range(end="2024-10-31", periods=n, freq="W-THU")
    r30 = np.round(np.linspace(7.5, 6.5, n), 2)
    return pd.DataFrame({
        "date": dates,
        "rate_30": r30,
        "rate_15": np.round(r30 - 0.65, 2),
        "rate_arm": np.round(r30 - 0.3, 2),
    })


def _make_trending_up_df(n=60):
    """Last 7 rows spike by 1.0 — MA7 >> MA30 -> trend up."""
    rates = [6.5] * (n - 7) + [7.5] * 7
    dates = pd.date_range(end="2024-10-31", periods=n, freq="W-THU")
    return pd.DataFrame({
        "date": dates,
        "rate_30": rates,
        "rate_15": [v - 0.65 for v in rates],
        "rate_arm": [v - 0.3 for v in rates],
    })


def _make_trending_down_df(n=60):
    """Last 7 rows drop by 1.0 — MA7 << MA30 -> trend down."""
    rates = [6.5] * (n - 7) + [5.5] * 7
    dates = pd.date_range(end="2024-10-31", periods=n, freq="W-THU")
    return pd.DataFrame({
        "date": dates,
        "rate_30": rates,
        "rate_15": [v - 0.65 for v in rates],
        "rate_arm": [v - 0.3 for v in rates],
    })


def _make_flat_df(n=60):
    """All rates identical — MA7 == MA30 -> trend flat."""
    dates = pd.date_range(end="2024-10-31", periods=n, freq="W-THU")
    return pd.DataFrame({
        "date": dates,
        "rate_30": [6.5] * n,
        "rate_15": [5.85] * n,
        "rate_arm": [6.2] * n,
    })


# ---------------------------------------------------------------------------
# Response structure
# ---------------------------------------------------------------------------

class TestApiForecastStructure:
    def test_returns_200(self, client, monkeypatch):
        monkeypatch.setattr(app_module, "_load_or_refresh_csv", lambda: _make_standard_df())
        assert client.get("/api/forecast").status_code == 200

    def test_503_when_df_empty(self, client, monkeypatch):
        monkeypatch.setattr(app_module, "_load_or_refresh_csv", lambda: pd.DataFrame())
        assert client.get("/api/forecast").status_code == 503

    def test_has_required_top_level_keys(self, client, monkeypatch):
        monkeypatch.setattr(app_module, "_load_or_refresh_csv", lambda: _make_standard_df())
        data = client.get("/api/forecast").get_json()
        for key in ("trend", "trend_label", "ma7", "ma30", "rsi",
                    "analysis", "projection_30d", "projection_60d",
                    "percentile", "current"):
            assert key in data

    def test_projections_have_value_low_high(self, client, monkeypatch):
        monkeypatch.setattr(app_module, "_load_or_refresh_csv", lambda: _make_standard_df())
        data = client.get("/api/forecast").get_json()
        for proj_key in ("projection_30d", "projection_60d"):
            for subkey in ("value", "low", "high"):
                assert subkey in data[proj_key]


# ---------------------------------------------------------------------------
# Trend direction
# ---------------------------------------------------------------------------

class TestApiForecastTrend:
    def test_trend_up_when_recent_rates_spike(self, client, monkeypatch):
        monkeypatch.setattr(app_module, "_load_or_refresh_csv", lambda: _make_trending_up_df())
        data = client.get("/api/forecast").get_json()
        assert data["trend"] == "up"

    def test_trend_down_when_recent_rates_drop(self, client, monkeypatch):
        monkeypatch.setattr(app_module, "_load_or_refresh_csv", lambda: _make_trending_down_df())
        data = client.get("/api/forecast").get_json()
        assert data["trend"] == "down"

    def test_trend_flat_when_all_rates_equal(self, client, monkeypatch):
        monkeypatch.setattr(app_module, "_load_or_refresh_csv", lambda: _make_flat_df())
        data = client.get("/api/forecast").get_json()
        assert data["trend"] == "flat"

    def test_trend_label_contains_trend_direction(self, client, monkeypatch):
        monkeypatch.setattr(app_module, "_load_or_refresh_csv", lambda: _make_trending_up_df())
        data = client.get("/api/forecast").get_json()
        assert "up" in data["trend_label"].lower()


# ---------------------------------------------------------------------------
# Computed metrics
# ---------------------------------------------------------------------------

class TestApiForecastMetrics:
    def test_rsi_is_in_range_0_to_100(self, client, monkeypatch):
        monkeypatch.setattr(app_module, "_load_or_refresh_csv", lambda: _make_standard_df())
        data = client.get("/api/forecast").get_json()
        assert 0.0 <= data["rsi"] <= 100.0

    def test_projection_ci_low_lte_value_lte_high(self, client, monkeypatch):
        monkeypatch.setattr(app_module, "_load_or_refresh_csv", lambda: _make_standard_df())
        data = client.get("/api/forecast").get_json()
        for proj in (data["projection_30d"], data["projection_60d"]):
            assert proj["low"] <= proj["value"] <= proj["high"]

    def test_percentile_is_in_range_0_to_100(self, client, monkeypatch):
        monkeypatch.setattr(app_module, "_load_or_refresh_csv", lambda: _make_standard_df())
        data = client.get("/api/forecast").get_json()
        assert 0.0 <= data["percentile"] <= 100.0

    def test_ma7_and_ma30_are_floats(self, client, monkeypatch):
        monkeypatch.setattr(app_module, "_load_or_refresh_csv", lambda: _make_standard_df())
        data = client.get("/api/forecast").get_json()
        assert isinstance(data["ma7"], float)
        assert isinstance(data["ma30"], float)

    def test_current_matches_last_rate_in_df(self, client, monkeypatch):
        df = _make_standard_df()
        monkeypatch.setattr(app_module, "_load_or_refresh_csv", lambda: df)
        data = client.get("/api/forecast").get_json()
        assert data["current"] == pytest.approx(float(df["rate_30"].iloc[-1]))

    def test_analysis_is_nonempty_string(self, client, monkeypatch):
        monkeypatch.setattr(app_module, "_load_or_refresh_csv", lambda: _make_standard_df())
        data = client.get("/api/forecast").get_json()
        assert isinstance(data["analysis"], str)
        assert len(data["analysis"]) > 0
