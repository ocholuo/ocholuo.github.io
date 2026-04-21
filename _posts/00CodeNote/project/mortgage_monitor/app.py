"""
Daily Mortgage Rate Tracker — Flask Backend
Fetches data from FRED CSV endpoint (no API key required),
caches in data/rate_history.csv, and exposes JSON endpoints.
"""

import os
import time
import math
import json
import datetime
import io
import logging
import threading
from functools import wraps

import requests
import pandas as pd
import numpy as np
import feedparser
from flask import Flask, jsonify, render_template, request

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
CSV_PATH = os.path.join(DATA_DIR, "rate_history.csv")
TNX_CSV_PATH = os.path.join(DATA_DIR, "tnx_history.csv")  # separate: DGS10 is daily vs weekly mortgage
PARCEL_CACHE_PATH = os.path.join(DATA_DIR, "parcel_cache.json")

FRED_BASE = "https://fred.stlouisfed.org/graph/fredgraph.csv"
FRED_SERIES = {
    "30yr": "MORTGAGE30US",
    "15yr": "MORTGAGE15US",
    "arm": "MORTGAGE5US",
}

CACHE_TTL_SECONDS = 300  # 5 minutes in-memory cache
CACHE_STALE_HOURS = 36   # CSV considered stale after 36 h (covers weekends)

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

app = Flask(__name__)

# ---------------------------------------------------------------------------
# Simple in-memory cache decorator
# ---------------------------------------------------------------------------
_cache: dict = {}

def cached(ttl=CACHE_TTL_SECONDS):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            key = fn.__name__ + str(args) + str(sorted(kwargs.items()))
            entry = _cache.get(key)
            if entry and (time.time() - entry["ts"]) < ttl:
                return entry["val"]
            val = fn(*args, **kwargs)
            _cache[key] = {"val": val, "ts": time.time()}
            return val
        return wrapper
    return decorator

# ---------------------------------------------------------------------------
# Parcel cache — file-backed, same pattern as rate_history.csv
# WHY: ArcGIS + Socrata round-trip is slow (~1-2 s); parcel attributes
# (PIN, zoning, assessed value) are reassessed annually at most, so a
# persistent on-disk cache is safe and avoids redundant network calls.
# Cache key: lat/lon rounded to 4 decimal places (~11 m precision).
# ---------------------------------------------------------------------------

def _load_parcel_cache() -> dict:
    if not os.path.exists(PARCEL_CACHE_PATH):
        return {}
    try:
        with open(PARCEL_CACHE_PATH) as f:
            return json.load(f)
    except Exception as exc:
        log.warning("Could not read parcel cache: %s", exc)
        return {}


def _save_parcel_cache(cache: dict) -> None:
    try:
        os.makedirs(os.path.dirname(PARCEL_CACHE_PATH), exist_ok=True)
        with open(PARCEL_CACHE_PATH, "w") as f:
            json.dump(cache, f)
    except Exception as exc:
        log.warning("Could not save parcel cache: %s", exc)


def _is_parcel_complete(entry: dict) -> bool:
    """Return False if a King County entry is missing all enriched fields, triggering a re-fetch."""
    if not entry.get("in_king_county"):
        return True
    return bool(
        entry.get("address")
        or entry.get("jurisdiction")
        or entry.get("zoning")
        or entry.get("year_built")
    )


def _pick(attrs: dict, *keys: str) -> object:
    """Return the first non-empty value found among the candidate field names."""
    for k in keys:
        v = attrs.get(k)
        if v is not None and str(v).strip() not in ("", "None"):
            return v
    return None


_parcel_cache: dict = _load_parcel_cache()

# ---------------------------------------------------------------------------
# FRED data fetching helpers
# ---------------------------------------------------------------------------

def _fetch_fred_series(series_id: str) -> pd.Series:
    """Download a FRED series as a pandas Series indexed by date."""
    url = f"{FRED_BASE}?id={series_id}"
    try:
        r = requests.get(url, timeout=15)
        r.raise_for_status()
        df = pd.read_csv(io.StringIO(r.text), parse_dates=[0], index_col=0)
        df.index.name = "date"
        s = df.iloc[:, 0].replace(".", np.nan).astype(float)
        s = s.dropna()
        return s
    except Exception as exc:
        log.warning("FRED fetch failed for %s: %s", series_id, exc)
        return pd.Series(dtype=float)


def _csv_is_fresh() -> bool:
    if not os.path.exists(CSV_PATH):
        return False
    age = time.time() - os.path.getmtime(CSV_PATH)
    return age < CACHE_STALE_HOURS * 3600


def _load_or_refresh_csv() -> pd.DataFrame:
    """Return a DataFrame with columns: date, rate_30, rate_15, rate_arm."""
    if _csv_is_fresh():
        try:
            df = pd.read_csv(CSV_PATH, parse_dates=["date"])
            df = df.sort_values("date").reset_index(drop=True)
            return df
        except Exception as exc:
            log.warning("Could not read CSV: %s", exc)

    log.info("Refreshing rate data from FRED …")
    s30 = _fetch_fred_series(FRED_SERIES["30yr"])
    s15 = _fetch_fred_series(FRED_SERIES["15yr"])
    sarm = _fetch_fred_series(FRED_SERIES["arm"])

    if s30.empty:
        log.warning("FRED returned empty data; using synthetic fallback.")
        return _synthetic_history()

    df = pd.DataFrame({"rate_30": s30, "rate_15": s15, "rate_arm": sarm})
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()
    df.index.name = "date"
    df = df.reset_index()

    # Forward-fill ARM which sometimes has gaps
    df["rate_arm"] = df["rate_arm"].ffill()
    df["rate_15"] = df["rate_15"].ffill()

    os.makedirs(DATA_DIR, exist_ok=True)
    df.to_csv(CSV_PATH, index=False)
    log.info("Saved %d rows to %s", len(df), CSV_PATH)
    return df


def _synthetic_history() -> pd.DataFrame:
    """Generate a plausible 20-year synthetic history when FRED is unreachable."""
    rng = np.random.default_rng(42)
    dates = pd.date_range(end=datetime.date.today(), periods=52 * 20, freq="W-THU")
    # Rough shape: high in 2006-2007, low in 2020-2021, rising since 2022
    n = len(dates)
    t = np.linspace(0, 1, n)
    base = (
        6.5
        - 1.5 * np.exp(-8 * (t - 0.15) ** 2)   # 2006 peak
        - 2.5 * np.exp(-8 * (t - 0.65) ** 2)   # 2020 low
        + 2.8 * np.maximum(0, t - 0.72)         # 2022 rise
        + rng.normal(0, 0.08, n)
    )
    base = np.clip(base, 2.5, 8.5)
    r30 = np.round(base, 2)
    r15 = np.round(base - 0.65 + rng.normal(0, 0.04, n), 2)
    rarm = np.round(base - 0.3 + rng.normal(0, 0.06, n), 2)
    return pd.DataFrame({"date": dates, "rate_30": r30, "rate_15": r15, "rate_arm": rarm})


def _load_tnx_data() -> pd.DataFrame:
    """
    WHY: 10Y Treasury (DGS10) is a daily FRED series, structurally different from
    the weekly mortgage CSV. Kept in a separate file to avoid date-alignment issues.
    Refreshes every 36h same as mortgage CSV.
    """
    stale = not (os.path.exists(TNX_CSV_PATH) and
                 (time.time() - os.path.getmtime(TNX_CSV_PATH)) < CACHE_STALE_HOURS * 3600)
    if not stale:
        try:
            df = pd.read_csv(TNX_CSV_PATH, parse_dates=["date"])
            return df.sort_values("date").reset_index(drop=True)
        except Exception:
            pass

    log.info("Refreshing 10Y Treasury data from FRED DGS10 …")
    s = _fetch_fred_series("DGS10")
    if s.empty:
        log.warning("DGS10 fetch failed; using synthetic TNX fallback.")
        rng = np.random.default_rng(99)
        dates = pd.date_range(end=datetime.date.today(), periods=252 * 20, freq="B")
        n = len(dates)
        t = np.linspace(0, 1, n)
        base = (4.5 - 1.5 * np.exp(-8*(t-0.15)**2) - 2.0 * np.exp(-8*(t-0.65)**2)
                + 2.5 * np.maximum(0, t - 0.72) + rng.normal(0, 0.06, n))
        s = pd.Series(np.round(np.clip(base, 0.5, 7.0), 3), index=dates)

    df = pd.DataFrame({"date": s.index, "rate_tnx": s.values})
    df["date"] = pd.to_datetime(df["date"])
    df = df.dropna().sort_values("date").reset_index(drop=True)
    os.makedirs(DATA_DIR, exist_ok=True)
    df.to_csv(TNX_CSV_PATH, index=False)
    log.info("Saved %d TNX rows to %s", len(df), TNX_CSV_PATH)
    return df


# ---------------------------------------------------------------------------
# Statistical helpers
# ---------------------------------------------------------------------------

def _rsi(series: pd.Series, period: int = 14) -> float:
    delta = series.diff().dropna()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(period).mean().iloc[-1]
    avg_loss = loss.rolling(period).mean().iloc[-1]
    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return round(100 - 100 / (1 + rs), 1)


def _linear_projection(series: pd.Series, days_back: int, days_forward: int):
    """Simple OLS projection with ±1 std CI."""
    tail = series.dropna().tail(days_back)
    if len(tail) < 4:
        last = float(series.dropna().iloc[-1])
        return last, last - 0.2, last + 0.2
    x = np.arange(len(tail))
    coeffs = np.polyfit(x, tail.values, 1)
    slope, intercept = coeffs
    proj = slope * (len(tail) + days_forward) + intercept
    residuals = tail.values - (slope * x + intercept)
    std = np.std(residuals) * math.sqrt(days_forward / len(tail) + 1)
    return round(proj, 2), round(proj - 1.96 * std, 2), round(proj + 1.96 * std, 2)


def _percentile_in_history(current: float, series: pd.Series) -> float:
    vals = series.dropna().values
    return round(float(np.sum(vals <= current) / len(vals) * 100), 1)

# ---------------------------------------------------------------------------
# News helpers
# ---------------------------------------------------------------------------

LOWER_KEYWORDS = ["cut", "drop", "fall", "fell", "decline", "dovish", "pause",
                  "inflation easing", "cool", "lower", "decrease", "below"]
HIGHER_KEYWORDS = ["hike", "rise", "surge", "hawkish", "hot cpi", "higher",
                   "increase", "above", "jump", "spike", "accelerat"]
MORTGAGE_KEYWORDS = ["mortgage", "home loan", "30-year", "15-year", "refinanc",
                     "homebuyer", "housing"]
FED_KEYWORDS = ["federal reserve", "fed ", " fed,", "fomc", "powell",
                "interest rate", "rate decision"]
ECONOMY_KEYWORDS = ["cpi", "inflation", "gdp", "unemployment", "jobs report",
                    "nonfarm", "recession", "economy"]

NEWS_FEEDS = [
    "https://news.google.com/rss/search?q=mortgage+rates&hl=en-US&gl=US&ceid=US:en",
    "https://news.google.com/rss/search?q=federal+reserve+interest+rates&hl=en-US&gl=US&ceid=US:en",
    "https://news.google.com/rss/search?q=CPI+inflation+economy&hl=en-US&gl=US&ceid=US:en",
]


def _classify_article(title: str, summary: str = "") -> dict:
    text = (title + " " + summary).lower()
    sentiment = "Neutral"
    for kw in LOWER_KEYWORDS:
        if kw in text:
            sentiment = "Rate Down"
            break
    if sentiment == "Neutral":
        for kw in HIGHER_KEYWORDS:
            if kw in text:
                sentiment = "Rate Up"
                break

    category = "Economy"
    for kw in MORTGAGE_KEYWORDS:
        if kw in text:
            category = "Rates"
            break
    if category == "Economy":
        for kw in FED_KEYWORDS:
            if kw in text:
                category = "Fed Policy"
                break

    return {"sentiment": sentiment, "category": category}


@cached(ttl=600)
def _fetch_news() -> list:
    articles = []
    for feed_url in NEWS_FEEDS:
        try:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries[:8]:
                title = entry.get("title", "")
                summary = entry.get("summary", "")
                # Strip HTML tags simply
                summary_clean = summary.replace("<b>", "").replace("</b>", "").replace("&amp;", "&")[:200]
                pub = entry.get("published", "")
                source = entry.get("source", {}).get("title", "Google News")
                info = _classify_article(title, summary)
                articles.append({
                    "title": title,
                    "summary": summary_clean,
                    "source": source,
                    "published": pub,
                    "sentiment": info["sentiment"],
                    "category": info["category"],
                    "url": entry.get("link", "#"),
                })
        except Exception as exc:
            log.warning("News feed error: %s", exc)

    # Deduplicate by title
    seen = set()
    unique = []
    for a in articles:
        if a["title"] not in seen:
            seen.add(a["title"])
            unique.append(a)
    return unique[:20]

# ---------------------------------------------------------------------------
# API endpoints
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/rates")
@cached()
def api_rates():
    df = _load_or_refresh_csv()
    if df.empty:
        return jsonify({"error": "No data available"}), 503

    latest = df.dropna(subset=["rate_30"]).iloc[-1]
    today_str = str(latest["date"])[:10]
    r30 = float(latest["rate_30"])
    r15 = float(latest["rate_15"]) if not pd.isna(latest.get("rate_15", np.nan)) else r30 - 0.65
    rarm = float(latest["rate_arm"]) if not pd.isna(latest.get("rate_arm", np.nan)) else r30 - 0.3

    def change_ago(col, weeks):
        target = latest["date"] - pd.Timedelta(weeks=weeks)
        past = df[df["date"] <= target]
        if past.empty:
            return None
        return round(float(latest[col]) - float(past.iloc[-1][col]), 2)

    def range_stats(col, weeks=52):
        cutoff = latest["date"] - pd.Timedelta(weeks=weeks)
        sub = df[df["date"] >= cutoff][col].dropna()
        if sub.empty:
            return None, None, None, None
        return round(sub.mean(), 2), round(sub.mean(), 2), round(sub.min(), 2), round(sub.max(), 2)

    # Position in 52-wk range (0–100)
    def range_pos(current, lo, hi):
        if hi == lo:
            return 50
        return round((current - lo) / (hi - lo) * 100, 1)

    avg30_monthly, _, _, _ = range_stats("rate_30", 4)
    avg30_52wk, _, min30, max30 = range_stats("rate_30", 52)
    avg15_monthly, _, _, _ = range_stats("rate_15", 4)
    avg15_52wk, _, min15, max15 = range_stats("rate_15", 52)

    # --- WHY: 10Y Treasury metrics via separate DGS10 dataset (daily vs weekly mortgage) ---
    tnx_df = _load_tnx_data()
    tnx_metrics = {}
    if not tnx_df.empty:
        tnx_latest = tnx_df.dropna(subset=["rate_tnx"]).iloc[-1]
        rtnx = float(tnx_latest["rate_tnx"])

        def tnx_change_ago(weeks):
            target = tnx_latest["date"] - pd.Timedelta(weeks=weeks)
            past = tnx_df[tnx_df["date"] <= target]
            return round(rtnx - float(past.iloc[-1]["rate_tnx"]), 2) if not past.empty else None

        cutoff4w = tnx_latest["date"] - pd.Timedelta(weeks=4)
        cutoff52w = tnx_latest["date"] - pd.Timedelta(weeks=52)
        sub4 = tnx_df[tnx_df["date"] >= cutoff4w]["rate_tnx"].dropna()
        sub52 = tnx_df[tnx_df["date"] >= cutoff52w]["rate_tnx"].dropna()
        tnx_mavg = round(sub4.mean(), 2) if not sub4.empty else None
        tnx_52avg = round(sub52.mean(), 2) if not sub52.empty else None
        tnx_min = round(sub52.min(), 2) if not sub52.empty else None
        tnx_max = round(sub52.max(), 2) if not sub52.empty else None

        tnx_metrics = {
            "current": rtnx,
            "change_1wk": tnx_change_ago(1),
            "change_1yr": tnx_change_ago(52),
            "monthly_avg": tnx_mavg,
            "avg_52wk": tnx_52avg,
            "min_52wk": tnx_min,
            "max_52wk": tnx_max,
            "range_pos": range_pos(rtnx, tnx_min, tnx_max) if tnx_min and tnx_max else 50,
            "spread_30yr": round(r30 - rtnx, 2),  # mortgage premium over treasury
        }

    stale = not _csv_is_fresh()

    return jsonify({
        "updated": today_str,
        "stale": stale,
        "rates": {
            "30yr": {
                "current": r30,
                "change_1wk": change_ago("rate_30", 1),
                "change_1yr": change_ago("rate_30", 52),
                "monthly_avg": avg30_monthly,
                "avg_52wk": avg30_52wk,
                "min_52wk": min30,
                "max_52wk": max30,
                "range_pos": range_pos(r30, min30, max30) if min30 and max30 else 50,
            },
            "15yr": {
                "current": r15,
                "change_1wk": change_ago("rate_15", 1),
                "change_1yr": change_ago("rate_15", 52),
                "monthly_avg": avg15_monthly,
                "avg_52wk": avg15_52wk,
                "min_52wk": min15,
                "max_52wk": max15,
                "range_pos": range_pos(r15, min15, max15) if min15 and max15 else 50,
            },
            "arm": {"current": rarm},
            "tnx": tnx_metrics,  # 10Y Treasury — full metrics with spread
        },
    })


@app.route("/api/history")
def api_history():
    range_param = request.args.get("range", "3M").upper()
    df = _load_or_refresh_csv()
    if df.empty:
        return jsonify({"labels": [], "data30": [], "data15": [], "data_tnx": []})

    df = df.sort_values("date")
    latest_date = df["date"].max()

    cutoffs = {
        "2W": latest_date - pd.Timedelta(weeks=2),
        "3M": latest_date - pd.Timedelta(days=91),
        "1Y": latest_date - pd.Timedelta(days=365),
        "20Y": latest_date - pd.Timedelta(days=365 * 20),
    }
    cutoff = cutoffs.get(range_param, cutoffs["3M"])

    # WHY: use daily TNX (DGS10) dates as the primary spine so the tooltip fires
    # on every individual day, not once per week (FRED mortgage data is weekly).
    # Weekly mortgage rates are forward-filled onto the daily date grid via merge_asof.
    try:
        tnx_df = _load_tnx_data()
        if not tnx_df.empty:
            tnx_sub = tnx_df[
                (tnx_df["date"] >= cutoff) & (tnx_df["date"] <= latest_date)
            ].copy()

            if not tnx_sub.empty:
                # Downsample 20Y to stay within ~300 points for payload size
                if range_param == "20Y" and len(tnx_sub) > 300:
                    step = max(1, len(tnx_sub) // 300)
                    tnx_sub = tnx_sub.iloc[::step].copy()

                # Forward-fill weekly mortgage rates onto each daily TNX date
                merged = pd.merge_asof(
                    tnx_sub.sort_values("date"),
                    df[["date", "rate_30", "rate_15"]].sort_values("date"),
                    on="date",
                    direction="backward",
                )
                labels  = [str(d)[:10] for d in merged["date"]]
                data30  = [round(float(v), 2) if not pd.isna(v) else None for v in merged["rate_30"]]
                data15  = [round(float(v), 2) if not pd.isna(v) else None for v in merged["rate_15"]]
                data_tnx = [round(float(v), 2) if not pd.isna(v) else None for v in merged["rate_tnx"]]
                return jsonify({"labels": labels, "data30": data30, "data15": data15, "data_tnx": data_tnx})
    except Exception as e:
        log.warning("Daily-spine merge failed, falling back to weekly: %s", e)

    # Fallback: original weekly mortgage spine (used if TNX data unavailable)
    sub = df[df["date"] >= cutoff].copy()
    if range_param == "20Y" and len(sub) > 300:
        step = max(1, len(sub) // 300)
        sub = sub.iloc[::step]
    labels  = [str(d)[:10] for d in sub["date"]]
    data30  = [round(float(v), 2) if not pd.isna(v) else None for v in sub["rate_30"]]
    data15  = [round(float(v), 2) if not pd.isna(v) else None for v in sub["rate_15"]]
    return jsonify({"labels": labels, "data30": data30, "data15": data15, "data_tnx": [None] * len(labels)})


@app.route("/api/forecast")
@cached()
def api_forecast():
    df = _load_or_refresh_csv()
    if df.empty:
        return jsonify({"error": "No data"}), 503

    s30 = df["rate_30"].dropna()
    current = float(s30.iloc[-1])

    ma7 = round(float(s30.tail(7).mean()), 2)
    ma30 = round(float(s30.tail(30).mean()), 2)
    rsi = _rsi(s30)

    # Trend: compare MA7 to MA30
    if ma7 < ma30 - 0.05:
        trend = "down"
        trend_label = "Rates trending down"
    elif ma7 > ma30 + 0.05:
        trend = "up"
        trend_label = "Rates trending up"
    else:
        trend = "flat"
        trend_label = "Rates holding steady"

    proj30_val, proj30_lo, proj30_hi = _linear_projection(s30, 30, 30)
    proj60_val, proj60_lo, proj60_hi = _linear_projection(s30, 60, 60)

    pct = _percentile_in_history(current, s30)
    hist_min = round(float(s30.min()), 2)
    hist_max = round(float(s30.max()), 2)

    # Build analysis text
    rsi_note = "neutral territory"
    if rsi > 70:
        rsi_note = "overbought (rates may ease)"
    elif rsi < 30:
        rsi_note = "oversold (rates may rise from here)"

    analysis = (
        f"The 7-day moving average ({ma7}%) is "
        f"{'below' if ma7 < ma30 else 'above'} the 30-day median ({ma30}%), "
        f"suggesting a {'downward' if trend == 'down' else 'upward' if trend == 'up' else 'sideways'} trend. "
        f"RSI(14) reads {rsi}, indicating {rsi_note}."
    )

    return jsonify({
        "trend": trend,
        "trend_label": trend_label,
        "ma7": ma7,
        "ma30": ma30,
        "rsi": rsi,
        "analysis": analysis,
        "projection_30d": {"value": proj30_val, "low": proj30_lo, "high": proj30_hi},
        "projection_60d": {"value": proj60_val, "low": proj60_lo, "high": proj60_hi},
        "percentile": pct,
        "hist_min": hist_min,
        "hist_max": hist_max,
        "current": current,
    })


@app.route("/api/news")
def api_news():
    articles = _fetch_news()
    if not articles:
        # Fallback static news
        articles = [
            {
                "title": "Federal Reserve Holds Rates Steady Amid Inflation Uncertainty",
                "summary": "The Fed kept its benchmark rate unchanged, citing mixed economic signals.",
                "source": "Reuters",
                "published": datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0000"),
                "sentiment": "Neutral",
                "category": "Fed Policy",
                "url": "#",
            },
            {
                "title": "Mortgage Rates Dip to 3-Month Low on Softer Jobs Report",
                "summary": "Average 30-year fixed mortgage rates fell following weaker-than-expected employment data.",
                "source": "Bloomberg",
                "published": datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0000"),
                "sentiment": "Rate Down",
                "category": "Rates",
                "url": "#",
            },
            {
                "title": "CPI Comes in Hotter Than Expected, Pushing Bond Yields Higher",
                "summary": "Consumer prices rose 3.5% year-over-year, above the 3.2% forecast.",
                "source": "WSJ",
                "published": datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0000"),
                "sentiment": "Rate Up",
                "category": "Economy",
                "url": "#",
            },
        ]

    # Compute signal distribution
    total = len(articles) or 1
    lower_count = sum(1 for a in articles if a["sentiment"] == "Rate Down")
    higher_count = sum(1 for a in articles if a["sentiment"] == "Rate Up")
    neutral_count = total - lower_count - higher_count

    signal = {
        "lower_pct": round(lower_count / total * 100),
        "neutral_pct": round(neutral_count / total * 100),
        "higher_pct": round(higher_count / total * 100),
        "dominant": (
            "Rate Down" if lower_count > higher_count and lower_count > neutral_count
            else "Rate Up" if higher_count > lower_count and higher_count > neutral_count
            else "Neutral"
        ),
    }

    return jsonify({"articles": articles, "signal": signal})


@app.route("/api/rate_history_table")
@cached()
def api_rate_history_table():
    df = _load_or_refresh_csv()
    if df.empty:
        return jsonify({"rows": []})

    # Get last 30 trading days (weekly data = last 30 rows covers ~7 months; use last 20)
    df = df.sort_values("date")
    recent = df.dropna(subset=["rate_30"]).tail(20).copy()

    rows = []
    prev_rate = None
    for _, row in recent.iterrows():
        r30 = float(row["rate_30"]) if not pd.isna(row["rate_30"]) else None
        r15 = float(row["rate_15"]) if not pd.isna(row["rate_15"]) else None
        rarm = float(row["rate_arm"]) if not pd.isna(row["rate_arm"]) else None

        change = None
        change_dir = "flat"
        if r30 is not None and prev_rate is not None:
            change = round(r30 - prev_rate, 2)
            change_dir = "up" if change > 0 else "down" if change < 0 else "flat"
        prev_rate = r30

        rows.append({
            "date": str(row["date"])[:10],
            "rate_30": r30,
            "rate_15": r15,
            "rate_arm": rarm,
            "change": change,
            "change_dir": change_dir,
            "note": "MND / FRED",
        })

    rows.reverse()  # Most recent first
    if rows:
        rows[0]["is_today"] = True
    return jsonify({"rows": rows})


# ---------------------------------------------------------------------------
# Startup: seed CSV if not present
# ---------------------------------------------------------------------------

_SCOUT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/javascript, */*",
    "Accept-Language": "en-US,en;q=0.9",
}

_STATE_ABBR = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR",
    "California": "CA", "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE",
    "Florida": "FL", "Georgia": "GA", "Hawaii": "HI", "Idaho": "ID",
    "Illinois": "IL", "Indiana": "IN", "Iowa": "IA", "Kansas": "KS",
    "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD",
    "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS",
    "Missouri": "MO", "Montana": "MT", "Nebraska": "NE", "Nevada": "NV",
    "New Hampshire": "NH", "New Jersey": "NJ", "New Mexico": "NM", "New York": "NY",
    "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK",
    "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC",
    "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX", "Utah": "UT",
    "Vermont": "VT", "Virginia": "VA", "Washington": "WA", "West Virginia": "WV",
    "Wisconsin": "WI", "Wyoming": "WY",
}


@app.route("/api/scout")
def api_scout():
    address = request.args.get("address", "").strip()
    lat = request.args.get("lat", type=float)
    lon = request.args.get("lon", type=float)

    if not address:
        return jsonify({"error": "address required"}), 400

    parts = [p.strip() for p in address.split(",")]
    street = parts[0] if parts else address
    city   = parts[1].strip() if len(parts) > 1 else ""
    state  = next((p.strip() for p in parts if p.strip() in _STATE_ABBR), "")
    state_abbr = _STATE_ABBR.get(state, "WA")
    zipcode = next(
        (w for p in parts for w in p.split() if w.isdigit() and len(w) == 5), ""
    )

    street_slug = street.replace(" ", "-")
    city_slug   = city.replace(" ", "-")

    result = {"zillow": {}, "redfin": {}, "realtor": {}}

    # Zillow — construct URL from address parts
    z_addr = f"{street_slug}-{city_slug}-{state_abbr}-{zipcode}".strip("-")
    result["zillow"] = {
        "url": f"https://www.zillow.com/homes/{z_addr}_rb/",
        "name": street,
    }

    # Realtor.com — city-state search
    r_city = city_slug or street_slug
    result["realtor"] = {
        "url": f"https://www.realtor.com/realestateandhomes-search/{r_city}_{state_abbr}/",
        "name": street,
    }

    # Redfin — use their location-autocomplete API to get a direct listing path
    try:
        resp = requests.get(
            "https://www.redfin.com/stingray/do/location-autocomplete",
            params={"location": address, "v": "2", "al": "1"},
            headers={**_SCOUT_HEADERS, "Referer": "https://www.redfin.com/"},
            timeout=8,
        )
        if resp.ok:
            # Redfin prepends {}&&  as a security prefix — strip it
            text = resp.text
            if text.startswith("{}&&"):
                text = text[4:]
            data = json.loads(text)
            for section in data.get("payload", {}).get("sections", []):
                for row in section.get("rows", []):
                    url_path = row.get("url", "")
                    if url_path and "/home/" in url_path:
                        result["redfin"] = {
                            "url": f"https://www.redfin.com{url_path}",
                            "name": row.get("name", street),
                        }
                        break
                if result["redfin"]:
                    break
    except Exception as exc:
        log.info(f"Redfin autocomplete failed: {exc}")

    # Fallback Redfin URL if autocomplete returned nothing
    if not result["redfin"]:
        rf_addr = f"{street_slug}-{zipcode}".strip("-")
        result["redfin"] = {
            "url": f"https://www.redfin.com/homes/{rf_addr}/",
            "name": street,
        }

    return jsonify(result)


@app.route("/api/parcel")
def api_parcel():
    lat = request.args.get("lat", type=float)
    lon = request.args.get("lon", type=float)
    pin_param = request.args.get("pin", "").strip()

    if not pin_param and (lat is None or lon is None):
        return jsonify({"error": "lat/lon or pin required"}), 400

    # WHY: PIN key is stable across re-geocodings; lat/lon key rounded to ~11 m.
    cache_key = pin_param if pin_param else f"{round(lat, 4)},{round(lon, 4)}"

    if cache_key in _parcel_cache:
        cached = _parcel_cache[cache_key]
        if _is_parcel_complete(cached):
            log.info("Parcel cache hit for %s — revalidating in background", cache_key)
            threading.Thread(
                target=_revalidate_parcel,
                args=(cache_key, cached, lat, lon, pin_param),
                daemon=True,
            ).start()
            return jsonify(cached)
        log.info("Parcel cache incomplete for %s, re-fetching now", cache_key)

    result = _fetch_parcel_data(lat, lon, pin_param)
    if result is None:
        return jsonify({"error": "parcel lookup failed"}), 502

    _parcel_cache[cache_key] = result
    _save_parcel_cache(_parcel_cache)
    log.info("Parcel cached for %s (PIN=%s)", cache_key, result.get("pin", "n/a"))
    return jsonify(result)


def _revalidate_parcel(
    cache_key: str,
    old: dict,
    lat: float | None,
    lon: float | None,
    pin_param: str,
) -> None:
    """Fetch fresh parcel data in the background and update cache if it differs."""
    try:
        fresh = _fetch_parcel_data(lat, lon, pin_param)
        if fresh and fresh != old:
            _parcel_cache[cache_key] = fresh
            _save_parcel_cache(_parcel_cache)
            log.info("Parcel cache refreshed (background) for %s", cache_key)
    except Exception as exc:
        log.info("Background parcel revalidation failed for %s: %s", cache_key, exc)


def _fetch_parcel_data(
    lat: float | None,
    lon: float | None,
    pin_param: str,
) -> dict | None:
    """Query ArcGIS + Socrata for parcel data. Returns result dict or None on hard failure."""
    arcgis_url = (
        "https://gismaps.kingcounty.gov/arcgis/rest/services"
        "/Property/KingCo_Parcels/MapServer/0/query"
    )

    if pin_param:
        # WHY: WHERE-clause query by PIN avoids spatial query entirely — more
        # reliable and faster. PIN format: 10 digits, no spaces.
        params = {
            "where": f"PIN='{pin_param}'",
            "outFields": "*",
            "returnGeometry": "true",
            "outSR": "4326",
            "f": "json",
        }
    else:
        # WHY: outFields=* avoids 400 errors from requesting field names that
        # don't exist in the parcel layer (e.g. APPR_LAND is in Socrata, not here).
        # inSR=4326 tells ArcGIS our geometry is WGS84 lat/lon, not State Plane.
        params = {
            "geometry": f"{lon},{lat}",
            "geometryType": "esriGeometryPoint",
            "spatialRel": "esriSpatialRelIntersects",
            "outFields": "*",
            "returnGeometry": "true",
            "inSR": "4326",
            "outSR": "4326",
            "f": "json",
        }

    try:
        # WHY: bypass any inherited https_proxy env var (e.g. Claude Code sandbox proxy)
        # that would intercept and drop the connection to gismaps.kingcounty.gov.
        resp = requests.get(
            arcgis_url, params=params, timeout=30, headers=_SCOUT_HEADERS,
            proxies={"http": None, "https": None},
        )
        resp.raise_for_status()
        data = resp.json()
    except Exception as exc:
        log.warning("ArcGIS parcel query failed: %s", exc)
        return None

    if data.get("error"):
        log.warning("ArcGIS returned error: %s", data["error"])
        return None

    features = data.get("features", [])
    if not features:
        log.info("ArcGIS returned no features (outside King County or invalid PIN)")
        return {"in_king_county": False}

    feat = features[0]
    attrs = feat.get("attributes", {})
    geo = feat.get("geometry", {})
    log.info("ArcGIS returned fields: %s", list(attrs.keys()))

    pin = str(attrs.get("PIN", "") or "").strip()

    geojson_geom = None
    if geo and geo.get("rings"):
        geojson_geom = {"type": "Polygon", "coordinates": geo["rings"]}

    erp_url = (
        f"https://blue.kingcounty.com/Assessor/eRealProperty/Dashboard.aspx?ParcelNbr={pin}"
        if pin else None
    )

    result: dict = {
        "in_king_county": True,
        "pin": pin,
        "erp_url": erp_url,
        "geometry": geojson_geom,
    }

    # WHY: ArcGIS MapServer/0 only carries PIN + geometry; eRealProperty has all
    # enriched attributes (address, zoning, building, assessed values).
    if pin:
        erp = _scrape_erp_details(pin)
        result.update(erp)

    result.setdefault("address", "")
    result.setdefault("jurisdiction", "")
    result.setdefault("zoning", "")
    result.setdefault("lot_sqft", None)

    return result


import re as _re
from html.parser import HTMLParser as _HTMLParser


class _TableParser(_HTMLParser):
    """Extract label->value pairs from consecutive <td> cells in each <tr>."""

    def __init__(self) -> None:
        super().__init__()
        self._in_td = False
        self._cell_buf: list[str] = []
        self._row_cells: list[str] = []
        self.pairs: dict[str, str] = {}
        # WHY: assessment history rows have format Year|Land|Improvement|Total;
        # captured separately because they have 3+ value cells, not a single label->value.
        self.year_rows: dict[str, list[str]] = {}

    def handle_starttag(self, tag: str, attrs: list) -> None:
        if tag == "tr":
            self._row_cells = []
        elif tag == "td":
            self._in_td = True
            self._cell_buf = []

    def handle_endtag(self, tag: str) -> None:
        if tag == "td":
            self._in_td = False
            self._row_cells.append(" ".join(self._cell_buf).strip())
        elif tag == "tr":
            cells = self._row_cells
            if len(cells) >= 2:
                label = cells[0].lower().rstrip(":").strip()
                value = cells[1].strip()
                if label and value:
                    self.pairs[label] = value
            if len(cells) >= 3 and _re.match(r"^\d{4}$", cells[0].strip()):
                self.year_rows[cells[0].strip()] = [c.strip() for c in cells[1:]]

    def handle_data(self, data: str) -> None:
        if self._in_td:
            stripped = data.strip()
            if stripped:
                self._cell_buf.append(stripped)


def _fetch_erp_page(url: str, pin: str, label: str) -> _TableParser | None:
    """Fetch one eRealProperty page and return a parsed _TableParser, or None on error."""
    try:
        resp = requests.get(url, timeout=20, headers=_SCOUT_HEADERS,
                            proxies={"http": None, "https": None})
        resp.raise_for_status()
    except Exception as exc:
        log.info("eRealProperty %s fetch failed for PIN=%s: %s", label, pin, exc)
        return None
    try:
        p = _TableParser()
        p.feed(resp.text)
        log.info("eRealProperty %s labels for PIN=%s: %s", label, pin, list(p.pairs.keys()))
        return p
    except Exception as exc:
        log.info("eRealProperty %s parse failed for PIN=%s: %s", label, pin, exc)
        return None


def _scrape_erp_details(pin: str) -> dict:
    """Scrape King County eRealProperty Dashboard + Detail pages for parcel attributes."""
    base = "https://blue.kingcounty.com/Assessor/eRealProperty"
    dashboard = _fetch_erp_page(f"{base}/Dashboard.aspx?ParcelNbr={pin}", pin, "Dashboard")
    detail    = _fetch_erp_page(f"{base}/Detail.aspx?ParcelNbr={pin}",    pin, "Detail")

    if dashboard is None and detail is None:
        return {}

    # Merge pairs: Dashboard takes priority; Detail fills in what Dashboard lacks.
    pairs: dict[str, str] = {}
    if detail:
        pairs.update(detail.pairs)
    if dashboard:
        pairs.update(dashboard.pairs)   # overwrites detail duplicates with dashboard values

    # Merge year_rows from both pages.
    year_rows: dict[str, list[str]] = {}
    if detail:
        year_rows.update(detail.year_rows)
    if dashboard:
        year_rows.update(dashboard.year_rows)

    def get(*labels: str) -> str | None:
        for lbl in labels:
            v = pairs.get(lbl.lower())
            if v and v not in ("-", "N/A", "n/a", ""):
                return v
        return None

    def to_int(raw: str | None) -> int | None:
        if raw is None:
            return None
        m = _re.search(r"[\d,]+", raw)
        return int(m.group().replace(",", "")) if m else None

    def strip_dollar(raw: str | None) -> str | None:
        if raw is None:
            return None
        return raw.replace("$", "").replace(",", "").strip() or None

    out: dict = {}
    out["name"]             = get("name")
    out["address"]          = get("site address", "property address", "address")
    out["jurisdiction"]     = get("jurisdiction", "city", "municipality")
    out["zoning"]           = get("zoning", "current zoning", "zone class", "zone")
    out["lot_sqft"]         = to_int(get("lot size", "lot area", "lot sq ft", "lot sq. ft."))
    out["year_built"]       = get("year built", "yr built")
    out["bedrooms"]         = get("number of bedrooms", "bedrooms", "nbr bedrooms", "bedroom count")
    out["bathrooms"]        = get("number of baths", "baths", "bathrooms", "nbr baths", "bath count")
    out["living_sqft"]      = get("total square footage", "sq ft tot living", "total living sq ft",
                                  "living space", "sq ft living", "square feet of living space")
    out["grade"]            = get("grade")
    out["condition"]        = get("condition")
    out["views"]            = get("views")
    out["appr_land"]        = strip_dollar(get("appraised land", "appraised land value", "land value"))
    out["appr_improvement"] = strip_dollar(get("appraised improvement", "appraised improvements",
                                               "improvement value"))
    out["appr_total"]       = strip_dollar(get("appraised total", "total appraised value", "total value"))

    # Detail-page fields.
    out["stories"]          = get("stories", "number of stories", "nbr stories")
    out["year_renovated"]   = get("year renovated", "yr renovated")
    out["heat_source"]      = get("heat source", "heating source")
    out["heat_system"]      = get("heat system", "heating system")
    out["basement_sqft"]    = to_int(get("total basement", "finished basement",
                                         "sq ft basement", "basement sqft"))
    out["garage_sqft"]      = to_int(get("attached garage", "basement garage",
                                         "garage sqft", "sq ft garage"))
    out["deck_sqft"]        = to_int(get("deck area sqft", "deck sqft"))
    out["present_use"]      = get("present use", "property type", "land type")
    out["land_sqft"]        = to_int(get("land sqft", "land sq ft", "sq ft land"))
    out["land_acres"]       = get("acres")
    out["sewer"]            = get("sewer/septic", "sewer", "sewage disposal")
    out["water"]            = get("water", "water source")

    # WHY: King County labels each fireplace type separately; sum them for a total count.
    fireplace_keys = [
        "fireplace single story", "fireplace muilti story",
        "fireplace free standing", "fireplace additional",
    ]
    fp_total = sum(
        int(m.group()) if (v := pairs.get(k)) and (m := _re.search(r"\d+", v)) else 0
        for k in fireplace_keys
    )
    if fp_total:
        out["fireplaces"] = str(fp_total)

    # WHY: assessment values live in multi-cell year rows, not label->value pairs.
    if year_rows:
        latest = max(year_rows.keys())
        vals = year_rows[latest]
        if len(vals) >= 1 and not out.get("appr_land"):
            out["appr_land"] = strip_dollar(vals[0])
        if len(vals) >= 2 and not out.get("appr_improvement"):
            out["appr_improvement"] = strip_dollar(vals[1])
        if len(vals) >= 3 and not out.get("appr_total"):
            out["appr_total"] = strip_dollar(vals[2])

    return {k: v for k, v in out.items() if v is not None}


@app.route("/api/parcel/debug")
def api_parcel_debug():
    """Return raw ArcGIS attrs + eRealProperty scrape for a PIN — diagnostic only."""
    pin = request.args.get("pin", "").strip()
    if not pin:
        return jsonify({"error": "pin required"}), 400

    arcgis_url = (
        "https://gismaps.kingcounty.gov/arcgis/rest/services"
        "/Property/KingCo_Parcels/MapServer/0/query"
    )
    try:
        ar = requests.get(arcgis_url,
                          params={"where": f"PIN='{pin}'", "outFields": "*",
                                  "returnGeometry": "false", "f": "json"},
                          timeout=30, headers=_SCOUT_HEADERS,
                          proxies={"http": None, "https": None})
        ar.raise_for_status()
        arcgis_raw = ar.json()
    except Exception as exc:
        arcgis_raw = {"error": str(exc)}

    features = arcgis_raw.get("features", [])
    attrs = features[0]["attributes"] if features else {}

    base = "https://blue.kingcounty.com/Assessor/eRealProperty"
    dashboard_parser = _fetch_erp_page(f"{base}/Dashboard.aspx?ParcelNbr={pin}", pin, "Dashboard")
    detail_parser    = _fetch_erp_page(f"{base}/Detail.aspx?ParcelNbr={pin}",    pin, "Detail")

    return jsonify({
        "arcgis_fields": list(attrs.keys()),
        "arcgis_attrs": attrs,
        "dashboard_labels": list(dashboard_parser.pairs.keys()) if dashboard_parser else [],
        "dashboard_pairs":  dashboard_parser.pairs if dashboard_parser else {},
        "detail_labels":    list(detail_parser.pairs.keys()) if detail_parser else [],
        "detail_pairs":     detail_parser.pairs if detail_parser else {},
        "erp_scraped":      _scrape_erp_details(pin),
    })


def _seed_on_startup():
    if not os.path.exists(CSV_PATH):
        log.info("No rate_history.csv found — seeding from FRED on startup …")
        _load_or_refresh_csv()


if __name__ == "__main__":
    _seed_on_startup()
    port = int(os.environ.get("PORT", 5050))
    app.run(debug=False, host="0.0.0.0", port=port)
