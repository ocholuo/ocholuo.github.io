"""
Tests for /api/rate_history_table endpoint: row ordering, change direction,
is_today flag, row count cap, and empty data path.
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


def _make_declining_df(n=25):
    dates = pd.date_range(end="2024-10-31", periods=n, freq="W-THU")
    r30 = np.round(np.linspace(7.0, 6.5, n), 2)
    return pd.DataFrame({
        "date": dates,
        "rate_30": r30,
        "rate_15": np.round(r30 - 0.65, 2),
        "rate_arm": np.round(r30 - 0.3, 2),
    })


def _make_rising_df(n=25):
    dates = pd.date_range(end="2024-10-31", periods=n, freq="W-THU")
    r30 = np.round(np.linspace(6.0, 7.0, n), 2)
    return pd.DataFrame({
        "date": dates,
        "rate_30": r30,
        "rate_15": np.round(r30 - 0.65, 2),
        "rate_arm": np.round(r30 - 0.3, 2),
    })


# ---------------------------------------------------------------------------
# Response structure
# ---------------------------------------------------------------------------

class TestApiRateHistoryTableStructure:
    def test_returns_200(self, client, monkeypatch):
        monkeypatch.setattr(app_module, "_load_or_refresh_csv", lambda: _make_declining_df())
        assert client.get("/api/rate_history_table").status_code == 200

    def test_has_rows_key(self, client, monkeypatch):
        monkeypatch.setattr(app_module, "_load_or_refresh_csv", lambda: _make_declining_df())
        data = client.get("/api/rate_history_table").get_json()
        assert "rows" in data

    def test_empty_df_returns_empty_rows(self, client, monkeypatch):
        monkeypatch.setattr(app_module, "_load_or_refresh_csv", lambda: pd.DataFrame())
        data = client.get("/api/rate_history_table").get_json()
        assert data["rows"] == []

    def test_row_has_expected_keys(self, client, monkeypatch):
        monkeypatch.setattr(app_module, "_load_or_refresh_csv", lambda: _make_declining_df())
        data = client.get("/api/rate_history_table").get_json()
        row = data["rows"][0]
        for key in ("date", "rate_30", "rate_15", "rate_arm", "change", "change_dir"):
            assert key in row

    def test_max_20_rows_returned(self, client, monkeypatch):
        monkeypatch.setattr(app_module, "_load_or_refresh_csv", lambda: _make_declining_df(30))
        data = client.get("/api/rate_history_table").get_json()
        assert len(data["rows"]) <= 20


# ---------------------------------------------------------------------------
# Row ordering and flags
# ---------------------------------------------------------------------------

class TestApiRateHistoryTableOrder:
    def test_rows_are_most_recent_first(self, client, monkeypatch):
        monkeypatch.setattr(app_module, "_load_or_refresh_csv", lambda: _make_declining_df())
        data = client.get("/api/rate_history_table").get_json()
        dates = [r["date"] for r in data["rows"]]
        assert dates == sorted(dates, reverse=True)

    def test_is_today_set_on_first_row_only(self, client, monkeypatch):
        monkeypatch.setattr(app_module, "_load_or_refresh_csv", lambda: _make_declining_df())
        data = client.get("/api/rate_history_table").get_json()
        assert data["rows"][0].get("is_today") is True
        for row in data["rows"][1:]:
            assert row.get("is_today") is None


# ---------------------------------------------------------------------------
# Change direction
# ---------------------------------------------------------------------------

class TestApiRateHistoryTableChangeDir:
    def test_change_dir_down_on_most_recent_row_for_declining_rates(self, client, monkeypatch):
        monkeypatch.setattr(app_module, "_load_or_refresh_csv", lambda: _make_declining_df())
        data = client.get("/api/rate_history_table").get_json()
        assert data["rows"][0]["change_dir"] == "down"

    def test_change_dir_up_on_most_recent_row_for_rising_rates(self, client, monkeypatch):
        monkeypatch.setattr(app_module, "_load_or_refresh_csv", lambda: _make_rising_df())
        data = client.get("/api/rate_history_table").get_json()
        assert data["rows"][0]["change_dir"] == "up"

    def test_oldest_row_has_null_change(self, client, monkeypatch):
        monkeypatch.setattr(app_module, "_load_or_refresh_csv", lambda: _make_declining_df())
        data = client.get("/api/rate_history_table").get_json()
        assert data["rows"][-1]["change"] is None

    def test_change_value_is_correct_for_known_rates(self, client, monkeypatch):
        # Two-row df: rates go from 7.0 to 6.8 — change for latest row = -0.20
        df = pd.DataFrame({
            "date": pd.to_datetime(["2024-10-17", "2024-10-24"]),
            "rate_30": [7.0, 6.8],
            "rate_15": [6.35, 6.15],
            "rate_arm": [6.7, 6.5],
        })
        monkeypatch.setattr(app_module, "_load_or_refresh_csv", lambda: df)
        data = client.get("/api/rate_history_table").get_json()
        # rows[0] = most recent (2024-10-24), change = 6.8 - 7.0 = -0.20
        assert data["rows"][0]["change"] == pytest.approx(-0.20, abs=1e-9)
