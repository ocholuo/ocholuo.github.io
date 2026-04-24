"""
Unit tests for pure statistical and classification helpers in app.py.
No network calls, no Flask client — fast by design.
"""

import math

import numpy as np
import pandas as pd
import pytest

from app import (
    _classify_article,
    _linear_projection,
    _percentile_in_history,
    _rsi,
)


# ---------------------------------------------------------------------------
# _rsi
# ---------------------------------------------------------------------------

class TestRsi:
    def test_all_gains_returns_100(self):
        s = pd.Series([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0,
                        11.0, 12.0, 13.0, 14.0, 15.0, 16.0])
        assert _rsi(s) == 100.0

    def test_all_losses_returns_0(self):
        s = pd.Series([16.0, 15.0, 14.0, 13.0, 12.0, 11.0, 10.0, 9.0, 8.0,
                        7.0, 6.0, 5.0, 4.0, 3.0, 2.0, 1.0])
        assert _rsi(s) == 0.0

    def test_flat_series_returns_0(self):
        # No gains, no losses -> avg_loss == 0 guard -> expect 0 not 100
        s = pd.Series([5.0] * 20)
        # All deltas are 0 -> avg_gain=0, avg_loss=0 -> returns 100 by guard
        assert _rsi(s) == 100.0

    def test_typical_mixed_series(self):
        # Alternating up/down of equal size -> RSI near 50
        vals = []
        v = 7.0
        for i in range(30):
            v += 0.1 if i % 2 == 0 else -0.1
            vals.append(v)
        result = _rsi(pd.Series(vals))
        assert 40.0 <= result <= 60.0

    def test_returns_float(self):
        s = pd.Series(np.random.default_rng(0).normal(7.0, 0.1, 30))
        assert isinstance(_rsi(s), float)


# ---------------------------------------------------------------------------
# _linear_projection
# ---------------------------------------------------------------------------

class TestLinearProjection:
    def test_returns_three_values(self):
        s = pd.Series([7.0, 7.1, 7.2, 7.3, 7.4])
        result = _linear_projection(s, days_back=5, days_forward=30)
        assert len(result) == 3

    def test_upward_trend_projects_higher(self):
        s = pd.Series(np.linspace(6.0, 7.0, 20))
        proj, lo, hi = _linear_projection(s, days_back=20, days_forward=10)
        assert proj > 7.0

    def test_ci_ordering(self):
        s = pd.Series(np.linspace(6.0, 7.0, 20))
        proj, lo, hi = _linear_projection(s, days_back=20, days_forward=10)
        assert lo <= proj <= hi

    def test_short_series_fallback(self):
        # Fewer than 4 non-NaN values -> fallback returns last value +/- 0.2
        s = pd.Series([7.5, 7.4, 7.3])
        proj, lo, hi = _linear_projection(s, days_back=10, days_forward=30)
        assert proj == 7.3
        assert lo == pytest.approx(7.1, abs=1e-9)
        assert hi == pytest.approx(7.5, abs=1e-9)

    def test_output_are_floats(self):
        s = pd.Series(np.linspace(6.5, 7.0, 15))
        for v in _linear_projection(s, 15, 30):
            assert isinstance(v, float)


# ---------------------------------------------------------------------------
# _percentile_in_history
# ---------------------------------------------------------------------------

class TestPercentileInHistory:
    def test_min_value_is_zero_percent(self):
        s = pd.Series([1.0, 2.0, 3.0, 4.0, 5.0])
        assert _percentile_in_history(1.0, s) == 20.0  # 1 of 5 values <= 1.0

    def test_max_value_is_100_percent(self):
        s = pd.Series([1.0, 2.0, 3.0, 4.0, 5.0])
        assert _percentile_in_history(5.0, s) == 100.0

    def test_midpoint(self):
        s = pd.Series([2.0, 4.0, 6.0, 8.0, 10.0])
        # 6.0: 3 of 5 values <= 6.0 -> 60%
        assert _percentile_in_history(6.0, s) == 60.0

    def test_above_max_is_100_percent(self):
        s = pd.Series([1.0, 2.0, 3.0])
        assert _percentile_in_history(99.0, s) == 100.0


# ---------------------------------------------------------------------------
# _classify_article
# ---------------------------------------------------------------------------

class TestClassifyArticle:
    def test_rate_down_sentiment(self):
        result = _classify_article("Fed signals rate cut amid inflation cooling")
        assert result["sentiment"] == "Rate Down"

    def test_rate_up_sentiment(self):
        result = _classify_article("CPI surges, hawkish Fed signals rate hike")
        assert result["sentiment"] == "Rate Up"

    def test_neutral_sentiment(self):
        result = _classify_article("Housing market shows mixed signals this quarter")
        assert result["sentiment"] == "Neutral"

    def test_mortgage_category(self):
        result = _classify_article("30-year mortgage rates edge higher this week")
        assert result["category"] == "Rates"

    def test_fed_policy_category(self):
        result = _classify_article("FOMC meeting concludes with no rate change")
        assert result["category"] == "Fed Policy"

    def test_economy_category(self):
        result = _classify_article("GDP growth slows in Q3 amid consumer headwinds")
        assert result["category"] == "Economy"

    def test_returns_both_keys(self):
        result = _classify_article("Some headline")
        assert "sentiment" in result and "category" in result

    def test_summary_influences_sentiment(self):
        result = _classify_article("Fed meeting update", "Inflation easing faster than expected")
        assert result["sentiment"] == "Rate Down"

    def test_rate_down_takes_priority_in_mixed(self):
        # Both "cut" and "hike" present — first keyword match wins (Rate Down)
        result = _classify_article("Fed may cut rates; analysts warn of future hike")
        assert result["sentiment"] == "Rate Down"
