"""
Tests for /api/rates endpoint: rate extraction, change calculations,
TNX spread, stale flag, and error paths.
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


def _make_rate_df(n=70):
    """70 weeks of weekly mortgage data, rates declining 7.5 -> 6.5."""
    end = pd.Timestamp("2024-10-31")
    dates = pd.date_range(end=end, periods=n, freq="W-THU")
    r30 = np.round(np.linspace(7.5, 6.5, n), 2)
    return pd.DataFrame({
        "date": dates,
        "rate_30": r30,
        "rate_15": np.round(r30 - 0.65, 2),
        "rate_arm": np.round(r30 - 0.3, 2),
    })


def _make_tnx_df(n=350):
    """Daily treasury data, rates declining 4.5 -> 3.8."""
    end = pd.Timestamp("2024-10-31")
    dates = pd.date_range(end=end, periods=n, freq="B")
    return pd.DataFrame({
        "date": dates,
        "rate_tnx": np.round(np.linspace(4.5, 3.8, n), 3),
    })


# ---------------------------------------------------------------------------
# Response structure
# ---------------------------------------------------------------------------

class TestApiRatesStructure:
    def test_returns_200(self, client, monkeypatch):
        monkeypatch.setattr(app_module, "_load_or_refresh_csv", lambda: _make_rate_df())
        monkeypatch.setattr(app_module, "_load_tnx_data", lambda: _make_tnx_df())
        monkeypatch.setattr(app_module, "_csv_is_fresh", lambda: True)
        assert client.get("/api/rates").status_code == 200

    def test_has_required_top_level_keys(self, client, monkeypatch):
        monkeypatch.setattr(app_module, "_load_or_refresh_csv", lambda: _make_rate_df())
        monkeypatch.setattr(app_module, "_load_tnx_data", lambda: _make_tnx_df())
        monkeypatch.setattr(app_module, "_csv_is_fresh", lambda: True)
        data = client.get("/api/rates").get_json()
        for key in ("updated", "stale", "rates"):
            assert key in data

    def test_rates_has_expected_series_keys(self, client, monkeypatch):
        monkeypatch.setattr(app_module, "_load_or_refresh_csv", lambda: _make_rate_df())
        monkeypatch.setattr(app_module, "_load_tnx_data", lambda: _make_tnx_df())
        monkeypatch.setattr(app_module, "_csv_is_fresh", lambda: True)
        data = client.get("/api/rates").get_json()
        for key in ("30yr", "15yr", "arm", "tnx"):
            assert key in data["rates"]

    def test_503_when_df_empty(self, client, monkeypatch):
        monkeypatch.setattr(app_module, "_load_or_refresh_csv", lambda: pd.DataFrame())
        monkeypatch.setattr(app_module, "_load_tnx_data", lambda: _make_tnx_df())
        monkeypatch.setattr(app_module, "_csv_is_fresh", lambda: True)
        assert client.get("/api/rates").status_code == 503

    def test_updated_is_yyyy_mm_dd(self, client, monkeypatch):
        import re
        monkeypatch.setattr(app_module, "_load_or_refresh_csv", lambda: _make_rate_df())
        monkeypatch.setattr(app_module, "_load_tnx_data", lambda: _make_tnx_df())
        monkeypatch.setattr(app_module, "_csv_is_fresh", lambda: True)
        data = client.get("/api/rates").get_json()
        assert re.match(r"^\d{4}-\d{2}-\d{2}$", data["updated"])


# ---------------------------------------------------------------------------
# Rate values
# ---------------------------------------------------------------------------

class TestApiRatesValues:
    def test_current_rate_matches_latest_row(self, client, monkeypatch):
        df = _make_rate_df()
        monkeypatch.setattr(app_module, "_load_or_refresh_csv", lambda: df)
        monkeypatch.setattr(app_module, "_load_tnx_data", lambda: _make_tnx_df())
        monkeypatch.setattr(app_module, "_csv_is_fresh", lambda: True)
        data = client.get("/api/rates").get_json()
        assert data["rates"]["30yr"]["current"] == pytest.approx(float(df["rate_30"].iloc[-1]))

    def test_change_1wk_is_negative_for_declining_rates(self, client, monkeypatch):
        monkeypatch.setattr(app_module, "_load_or_refresh_csv", lambda: _make_rate_df())
        monkeypatch.setattr(app_module, "_load_tnx_data", lambda: _make_tnx_df())
        monkeypatch.setattr(app_module, "_csv_is_fresh", lambda: True)
        data = client.get("/api/rates").get_json()
        assert data["rates"]["30yr"]["change_1wk"] < 0

    def test_change_1yr_is_negative_for_declining_rates(self, client, monkeypatch):
        monkeypatch.setattr(app_module, "_load_or_refresh_csv", lambda: _make_rate_df())
        monkeypatch.setattr(app_module, "_load_tnx_data", lambda: _make_tnx_df())
        monkeypatch.setattr(app_module, "_csv_is_fresh", lambda: True)
        data = client.get("/api/rates").get_json()
        assert data["rates"]["30yr"]["change_1yr"] < 0

    def test_range_pos_is_50_when_all_rates_equal(self, client, monkeypatch):
        flat_df = pd.DataFrame({
            "date": pd.date_range("2024-01-01", periods=10, freq="W"),
            "rate_30": [6.5] * 10,
            "rate_15": [5.85] * 10,
            "rate_arm": [6.2] * 10,
        })
        monkeypatch.setattr(app_module, "_load_or_refresh_csv", lambda: flat_df)
        monkeypatch.setattr(app_module, "_load_tnx_data", lambda: pd.DataFrame())
        monkeypatch.setattr(app_module, "_csv_is_fresh", lambda: True)
        data = client.get("/api/rates").get_json()
        assert data["rates"]["30yr"]["range_pos"] == 50

    def test_range_pos_is_100_at_52wk_high(self, client, monkeypatch):
        # Latest rate is the max of the 52-week window
        n = 60
        dates = pd.date_range(end="2024-10-31", periods=n, freq="W-THU")
        r30 = np.round(np.linspace(6.0, 8.0, len(dates)), 2)  # rising: latest = max
        df = pd.DataFrame({
            "date": dates,
            "rate_30": r30,
            "rate_15": np.round(r30 - 0.65, 2),
            "rate_arm": np.round(r30 - 0.3, 2),
        })
        monkeypatch.setattr(app_module, "_load_or_refresh_csv", lambda: df)
        monkeypatch.setattr(app_module, "_load_tnx_data", lambda: pd.DataFrame())
        monkeypatch.setattr(app_module, "_csv_is_fresh", lambda: True)
        data = client.get("/api/rates").get_json()
        assert data["rates"]["30yr"]["range_pos"] == 100.0


# ---------------------------------------------------------------------------
# Stale flag
# ---------------------------------------------------------------------------

class TestApiRatesStaleFlag:
    def test_stale_true_when_csv_stale(self, client, monkeypatch):
        monkeypatch.setattr(app_module, "_load_or_refresh_csv", lambda: _make_rate_df())
        monkeypatch.setattr(app_module, "_load_tnx_data", lambda: _make_tnx_df())
        monkeypatch.setattr(app_module, "_csv_is_fresh", lambda: False)
        data = client.get("/api/rates").get_json()
        assert data["stale"] is True

    def test_stale_false_when_csv_fresh(self, client, monkeypatch):
        monkeypatch.setattr(app_module, "_load_or_refresh_csv", lambda: _make_rate_df())
        monkeypatch.setattr(app_module, "_load_tnx_data", lambda: _make_tnx_df())
        monkeypatch.setattr(app_module, "_csv_is_fresh", lambda: True)
        data = client.get("/api/rates").get_json()
        assert data["stale"] is False


# ---------------------------------------------------------------------------
# TNX / Treasury metrics
# ---------------------------------------------------------------------------

class TestApiRatesTnx:
    def test_tnx_metrics_absent_when_tnx_empty(self, client, monkeypatch):
        monkeypatch.setattr(app_module, "_load_or_refresh_csv", lambda: _make_rate_df())
        monkeypatch.setattr(app_module, "_load_tnx_data", lambda: pd.DataFrame())
        monkeypatch.setattr(app_module, "_csv_is_fresh", lambda: True)
        data = client.get("/api/rates").get_json()
        assert data["rates"]["tnx"] == {}

    def test_tnx_spread_equals_30yr_minus_treasury(self, client, monkeypatch):
        monkeypatch.setattr(app_module, "_load_or_refresh_csv", lambda: _make_rate_df())
        monkeypatch.setattr(app_module, "_load_tnx_data", lambda: _make_tnx_df())
        monkeypatch.setattr(app_module, "_csv_is_fresh", lambda: True)
        data = client.get("/api/rates").get_json()
        r30 = data["rates"]["30yr"]["current"]
        rtnx = data["rates"]["tnx"]["current"]
        spread = data["rates"]["tnx"]["spread_30yr"]
        assert spread == pytest.approx(r30 - rtnx, abs=0.01)

    def test_tnx_has_required_metric_keys(self, client, monkeypatch):
        monkeypatch.setattr(app_module, "_load_or_refresh_csv", lambda: _make_rate_df())
        monkeypatch.setattr(app_module, "_load_tnx_data", lambda: _make_tnx_df())
        monkeypatch.setattr(app_module, "_csv_is_fresh", lambda: True)
        data = client.get("/api/rates").get_json()
        tnx = data["rates"]["tnx"]
        for key in ("current", "change_1wk", "monthly_avg", "avg_52wk", "spread_30yr"):
            assert key in tnx
