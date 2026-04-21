"""
Tests for /api/history endpoint: range parameters, TNX merge, downsampling,
and fallback behavior when TNX data is unavailable.
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


def _make_rate_df(n=200):
    """200 weeks of weekly mortgage data."""
    end = pd.Timestamp("2024-10-31")
    dates = pd.date_range(end=end, periods=n, freq="W-THU")
    r30 = np.round(np.linspace(7.5, 6.5, n), 2)
    return pd.DataFrame({
        "date": dates,
        "rate_30": r30,
        "rate_15": np.round(r30 - 0.65, 2),
        "rate_arm": np.round(r30 - 0.3, 2),
    })


def _make_tnx_df(n=1000):
    """Daily treasury data."""
    end = pd.Timestamp("2024-10-31")
    dates = pd.date_range(end=end, periods=n, freq="B")
    return pd.DataFrame({
        "date": dates,
        "rate_tnx": np.round(np.linspace(4.5, 3.8, n), 3),
    })


# ---------------------------------------------------------------------------
# Response structure
# ---------------------------------------------------------------------------

class TestApiHistoryStructure:
    def test_returns_200(self, client, monkeypatch):
        monkeypatch.setattr(app_module, "_load_or_refresh_csv", lambda: _make_rate_df())
        monkeypatch.setattr(app_module, "_load_tnx_data", lambda: _make_tnx_df())
        assert client.get("/api/history").status_code == 200

    def test_has_required_keys(self, client, monkeypatch):
        monkeypatch.setattr(app_module, "_load_or_refresh_csv", lambda: _make_rate_df())
        monkeypatch.setattr(app_module, "_load_tnx_data", lambda: _make_tnx_df())
        data = client.get("/api/history").get_json()
        for key in ("labels", "data30", "data15", "data_tnx"):
            assert key in data

    def test_empty_df_returns_empty_arrays(self, client, monkeypatch):
        monkeypatch.setattr(app_module, "_load_or_refresh_csv", lambda: pd.DataFrame())
        monkeypatch.setattr(app_module, "_load_tnx_data", lambda: _make_tnx_df())
        data = client.get("/api/history").get_json()
        assert data["labels"] == []
        assert data["data30"] == []
        assert data["data15"] == []

    def test_all_arrays_have_same_length(self, client, monkeypatch):
        monkeypatch.setattr(app_module, "_load_or_refresh_csv", lambda: _make_rate_df())
        monkeypatch.setattr(app_module, "_load_tnx_data", lambda: _make_tnx_df())
        data = client.get("/api/history").get_json()
        n = len(data["labels"])
        assert len(data["data30"]) == n
        assert len(data["data15"]) == n
        assert len(data["data_tnx"]) == n

    def test_labels_are_iso_date_strings(self, client, monkeypatch):
        import re
        monkeypatch.setattr(app_module, "_load_or_refresh_csv", lambda: _make_rate_df())
        monkeypatch.setattr(app_module, "_load_tnx_data", lambda: _make_tnx_df())
        data = client.get("/api/history?range=2W").get_json()
        for label in data["labels"]:
            assert re.match(r"^\d{4}-\d{2}-\d{2}$", label)


# ---------------------------------------------------------------------------
# Range filtering
# ---------------------------------------------------------------------------

class TestApiHistoryRangeFilter:
    def test_2w_returns_fewer_points_than_1y(self, client, monkeypatch):
        monkeypatch.setattr(app_module, "_load_or_refresh_csv", lambda: _make_rate_df())
        monkeypatch.setattr(app_module, "_load_tnx_data", lambda: _make_tnx_df())
        n_2w = len(client.get("/api/history?range=2W").get_json()["labels"])
        n_1y = len(client.get("/api/history?range=1Y").get_json()["labels"])
        assert n_2w < n_1y

    def test_invalid_range_falls_back_to_3m(self, client, monkeypatch):
        monkeypatch.setattr(app_module, "_load_or_refresh_csv", lambda: _make_rate_df())
        monkeypatch.setattr(app_module, "_load_tnx_data", lambda: _make_tnx_df())
        n_bogus = len(client.get("/api/history?range=BOGUS").get_json()["labels"])
        n_3m = len(client.get("/api/history?range=3M").get_json()["labels"])
        assert n_bogus == n_3m

    def test_20y_range_downsamples_large_tnx(self, client, monkeypatch):
        big_tnx = pd.DataFrame({
            "date": pd.date_range(end="2024-10-31", periods=5200, freq="B"),
            "rate_tnx": np.round(np.linspace(4.5, 3.8, 5200), 3),
        })
        big_rates = pd.DataFrame({
            "date": pd.date_range(end="2024-10-31", periods=1040, freq="W-THU"),
            "rate_30": np.round(np.linspace(7.5, 6.5, 1040), 2),
            "rate_15": np.round(np.linspace(6.85, 5.85, 1040), 2),
            "rate_arm": np.round(np.linspace(7.2, 6.2, 1040), 2),
        })
        monkeypatch.setattr(app_module, "_load_or_refresh_csv", lambda: big_rates)
        monkeypatch.setattr(app_module, "_load_tnx_data", lambda: big_tnx)
        data = client.get("/api/history?range=20Y").get_json()
        assert len(data["labels"]) <= 350


# ---------------------------------------------------------------------------
# TNX fallback
# ---------------------------------------------------------------------------

class TestApiHistoryTnxFallback:
    def test_falls_back_to_weekly_spine_when_tnx_empty(self, client, monkeypatch):
        monkeypatch.setattr(app_module, "_load_or_refresh_csv", lambda: _make_rate_df())
        monkeypatch.setattr(app_module, "_load_tnx_data", lambda: pd.DataFrame())
        data = client.get("/api/history?range=3M").get_json()
        assert len(data["labels"]) > 0

    def test_tnx_values_are_none_when_tnx_data_unavailable(self, client, monkeypatch):
        monkeypatch.setattr(app_module, "_load_or_refresh_csv", lambda: _make_rate_df())
        monkeypatch.setattr(app_module, "_load_tnx_data", lambda: pd.DataFrame())
        data = client.get("/api/history?range=3M").get_json()
        assert all(v is None for v in data["data_tnx"])
