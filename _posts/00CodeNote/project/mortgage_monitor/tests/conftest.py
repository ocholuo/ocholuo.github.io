"""
Shared fixtures for mortgage monitor tests.
"""

import json
import os
import tempfile

import pandas as pd
import pytest

import app as app_module
from app import app as flask_app


@pytest.fixture()
def client():
    """Flask test client with testing mode on."""
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as c:
        yield c


@pytest.fixture()
def rate_df():
    """Minimal rate DataFrame matching the CSV schema."""
    return pd.DataFrame(
        {
            "date": pd.to_datetime(
                [f"2024-0{i}-01" for i in range(1, 9)]
                + ["2024-09-01", "2024-10-01"]
            ),
            "rate_30": [7.5, 7.4, 7.3, 7.2, 7.1, 7.0, 6.9, 6.8, 6.7, 6.6],
            "rate_15": [6.9, 6.8, 6.7, 6.6, 6.5, 6.4, 6.3, 6.2, 6.1, 6.0],
            "rate_arm": [6.5, 6.4, 6.3, 6.2, 6.1, 6.0, 5.9, 5.8, 5.7, 5.6],
        }
    )


@pytest.fixture()
def tmp_cache(tmp_path, monkeypatch):
    """Redirect parcel cache to a temp file and start each test with an empty cache."""
    cache_path = str(tmp_path / "parcel_cache.json")
    monkeypatch.setattr(app_module, "PARCEL_CACHE_PATH", cache_path)
    monkeypatch.setattr(app_module, "_parcel_cache", {})
    return cache_path
