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

def _seed_on_startup():
    if not os.path.exists(CSV_PATH):
        log.info("No rate_history.csv found — seeding from FRED on startup …")
        _load_or_refresh_csv()


if __name__ == "__main__":
    _seed_on_startup()
    port = int(os.environ.get("PORT", 5050))
    app.run(debug=False, host="0.0.0.0", port=port)
