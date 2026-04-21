"""
Unit tests for utility helpers: _pick, _is_parcel_complete, _csv_is_fresh,
_synthetic_history, and the cached decorator.
"""

import os
import time

import numpy as np
import pandas as pd
import pytest

import app as app_module
from app import (
    _csv_is_fresh,
    _is_parcel_complete,
    _pick,
    _synthetic_history,
    cached,
)


# ---------------------------------------------------------------------------
# _pick
# ---------------------------------------------------------------------------

class TestPick:
    def test_returns_first_non_empty_value(self):
        attrs = {"a": None, "b": "", "c": "found", "d": "ignored"}
        assert _pick(attrs, "a", "b", "c", "d") == "found"

    def test_skips_none(self):
        assert _pick({"a": None, "b": "x"}, "a", "b") == "x"

    def test_skips_empty_string(self):
        assert _pick({"a": "  ", "b": "x"}, "a", "b") == "x"

    def test_skips_string_none(self):
        assert _pick({"a": "None", "b": "x"}, "a", "b") == "x"

    def test_returns_none_when_all_empty(self):
        assert _pick({"a": None, "b": ""}, "a", "b") is None

    def test_returns_zero_as_valid_value(self):
        assert _pick({"a": None, "b": 0}, "a", "b") == 0

    def test_returns_none_for_missing_keys(self):
        assert _pick({}, "a", "b") is None

    def test_returns_none_with_no_keys(self):
        assert _pick({"a": "val"}) is None


# ---------------------------------------------------------------------------
# _is_parcel_complete
# ---------------------------------------------------------------------------

class TestIsParcelComplete:
    def test_non_king_county_is_always_complete(self):
        assert _is_parcel_complete({"in_king_county": False}) is True

    def test_king_county_with_address_is_complete(self):
        assert _is_parcel_complete({"in_king_county": True, "address": "123 Main St"}) is True

    def test_king_county_with_jurisdiction_is_complete(self):
        assert _is_parcel_complete({"in_king_county": True, "jurisdiction": "Seattle"}) is True

    def test_king_county_with_zoning_is_complete(self):
        assert _is_parcel_complete({"in_king_county": True, "zoning": "R-5"}) is True

    def test_king_county_with_year_built_is_complete(self):
        assert _is_parcel_complete({"in_king_county": True, "year_built": "1990"}) is True

    def test_king_county_with_no_enriched_fields_is_incomplete(self):
        assert _is_parcel_complete({"in_king_county": True}) is False

    def test_king_county_with_all_empty_enriched_fields_is_incomplete(self):
        assert _is_parcel_complete({
            "in_king_county": True,
            "address": None,
            "jurisdiction": None,
            "zoning": None,
            "year_built": None,
        }) is False


# ---------------------------------------------------------------------------
# _csv_is_fresh
# ---------------------------------------------------------------------------

class TestCsvIsFresh:
    def test_returns_false_when_file_missing(self, tmp_path, monkeypatch):
        monkeypatch.setattr(app_module, "CSV_PATH", str(tmp_path / "nope.csv"))
        assert _csv_is_fresh() is False

    def test_returns_true_when_file_is_recent(self, tmp_path, monkeypatch):
        p = tmp_path / "rates.csv"
        p.write_text("date,rate_30\n")
        monkeypatch.setattr(app_module, "CSV_PATH", str(p))
        assert _csv_is_fresh() is True

    def test_returns_false_when_file_is_stale(self, tmp_path, monkeypatch):
        p = tmp_path / "rates.csv"
        p.write_text("date,rate_30\n")
        stale_ts = time.time() - (40 * 3600)
        os.utime(str(p), (stale_ts, stale_ts))
        monkeypatch.setattr(app_module, "CSV_PATH", str(p))
        assert _csv_is_fresh() is False


# ---------------------------------------------------------------------------
# _synthetic_history
# ---------------------------------------------------------------------------

class TestSyntheticHistory:
    def setup_method(self):
        self.df = _synthetic_history()

    def test_returns_dataframe(self):
        assert isinstance(self.df, pd.DataFrame)

    def test_has_expected_columns(self):
        assert set(self.df.columns) == {"date", "rate_30", "rate_15", "rate_arm"}

    def test_has_approximately_20_years_of_weekly_data(self):
        assert len(self.df) >= 1000

    def test_rates_30yr_are_in_valid_range(self):
        assert self.df["rate_30"].between(2.0, 9.5).all()

    def test_rates_15yr_are_below_30yr(self):
        assert (self.df["rate_15"] < self.df["rate_30"]).all()

    def test_dates_are_monotonically_increasing(self):
        assert self.df["date"].is_monotonic_increasing

    def test_is_deterministic(self):
        df2 = _synthetic_history()
        pd.testing.assert_frame_equal(self.df.reset_index(drop=True),
                                      df2.reset_index(drop=True))


# ---------------------------------------------------------------------------
# cached decorator
# ---------------------------------------------------------------------------

class TestCached:
    def setup_method(self):
        app_module._cache.clear()

    def teardown_method(self):
        app_module._cache.clear()

    def test_returns_correct_value(self):
        @cached(ttl=60)
        def fn():
            return 42

        assert fn() == 42

    def test_calls_function_only_once_within_ttl(self):
        call_count = {"n": 0}

        @cached(ttl=60)
        def fn():
            call_count["n"] += 1
            return call_count["n"]

        fn()
        fn()
        assert call_count["n"] == 1

    def test_calls_function_again_after_ttl_expires(self):
        call_count = {"n": 0}

        @cached(ttl=60)
        def fn():
            call_count["n"] += 1
            return call_count["n"]

        fn()
        for key in list(app_module._cache.keys()):
            app_module._cache[key]["ts"] = time.time() - 120

        result = fn()
        assert call_count["n"] == 2
        assert result == 2

    def test_different_args_have_separate_cache_entries(self):
        call_count = {"n": 0}

        @cached(ttl=60)
        def fn(x):
            call_count["n"] += 1
            return x * 2

        assert fn(1) == 2
        assert fn(2) == 4
        assert call_count["n"] == 2
