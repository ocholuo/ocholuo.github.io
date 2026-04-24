# Oh My House — Modular Refactor Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Split the single-file monolith (`app.py` + `index.html`) into a clean module structure without changing any behavior.

**Architecture:** Extract config, services (data/business logic), and route handlers from `app.py` into separate files connected via Flask Blueprints. Extract CSS and JS from `index.html` into `static/` files, leaving `index.html` as a pure HTML skeleton.

**Tech Stack:** Flask, Blueprints, Python 3.11, vanilla JS, Chart.js 4.4, Gunicorn

---

## Before You Start

Verify the app runs and key endpoints respond:

```bash
cd _posts/00CodeNote/project/mortgage_monitor
flask run --port 5050
# In another terminal:
curl http://localhost:5050/api/rates | python3 -m json.tool | head -20
curl http://localhost:5050/api/news  | python3 -m json.tool | head -5
```

Keep a note of what the JSON looks like — this is your regression baseline. The refactor must not change any API response shape.

---

## File Map: Before vs After

### Before
```
mortgage_monitor/
├── app.py           # 895 lines: config + cache + services + routes all mixed
├── templates/
│   └── index.html   # 3500+ lines: CSS + HTML + JS all mixed
```

### After
```
mortgage_monitor/
├── app.py                     # ~30 lines: Flask init + blueprint registration + startup
├── config.py                  # All constants (paths, URLs, TTLs)
├── services/
│   ├── __init__.py            # empty
│   ├── cache.py               # @cached decorator
│   ├── rates.py               # FRED fetch, CSV load/refresh, TNX data
│   ├── forecast.py            # RSI, linear projection, percentile
│   ├── news.py                # RSS fetch, article classification, keyword lists
│   └── parcel.py              # ArcGIS + Socrata parcel lookups, file-backed cache
├── routes/
│   ├── __init__.py            # register_blueprints(app) helper
│   ├── pages.py               # GET / -> render_template
│   ├── rates.py               # /api/rates, /api/history, /api/rate_history_table
│   ├── forecast.py            # /api/forecast
│   ├── news.py                # /api/news
│   └── scout.py               # /api/scout, /api/parcel
├── static/
│   ├── css/
│   │   └── style.css          # All CSS from <style> block in index.html
│   └── js/
│       └── app.js             # All JS from <script> block in index.html
└── templates/
    └── index.html             # HTML skeleton only (<link> + <script> + structure)
```

---

## Task 1: Extract config.py

**Files:**
- Create: `config.py`
- Modify: `app.py` (remove constants, import from config)

Extract all constants from the top of `app.py` into a single config module.

- [ ] **Step 1: Create `config.py`**

```python
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
CSV_PATH = os.path.join(DATA_DIR, "rate_history.csv")
TNX_CSV_PATH = os.path.join(DATA_DIR, "tnx_history.csv")
PARCEL_CACHE_PATH = os.path.join(DATA_DIR, "parcel_cache.json")

FRED_BASE = "https://fred.stlouisfed.org/graph/fredgraph.csv"
FRED_SERIES = {
    "30yr": "MORTGAGE30US",
    "15yr": "MORTGAGE15US",
    "arm":  "MORTGAGE5US",
}

CACHE_TTL_SECONDS = 300
CACHE_STALE_HOURS = 36
```

- [ ] **Step 2: In `app.py`, replace the constants block with an import**

```python
from config import (
    BASE_DIR, DATA_DIR, CSV_PATH, TNX_CSV_PATH, PARCEL_CACHE_PATH,
    FRED_BASE, FRED_SERIES, CACHE_TTL_SECONDS, CACHE_STALE_HOURS,
)
```

- [ ] **Step 3: Verify app still starts**

```bash
flask run --port 5050
# Expected: no ImportError, app starts normally
```

- [ ] **Step 4: Commit**

```bash
git add config.py app.py
git commit -m "refactor: extract config constants to config.py"
```

---

## Task 2: Extract services/cache.py

**Files:**
- Create: `services/__init__.py` (empty)
- Create: `services/cache.py`
- Modify: `app.py`

- [ ] **Step 1: Create `services/__init__.py`**

```python
```
(empty file)

- [ ] **Step 2: Create `services/cache.py`**

```python
import time
from functools import wraps
from config import CACHE_TTL_SECONDS

_cache: dict = {}


def cached(ttl: int = CACHE_TTL_SECONDS):
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
```

- [ ] **Step 3: In `app.py`, replace cache block with import**

```python
from services.cache import cached
```

Remove the `_cache` dict and `cached` function definition from `app.py`.

- [ ] **Step 4: Verify**

```bash
flask run --port 5050
curl http://localhost:5050/api/rates | python3 -m json.tool | head -5
# Expected: same JSON as baseline
```

- [ ] **Step 5: Commit**

```bash
git add services/__init__.py services/cache.py app.py
git commit -m "refactor: extract cache decorator to services/cache.py"
```

---

## Task 3: Extract services/rates.py

**Files:**
- Create: `services/rates.py`
- Modify: `app.py`

Move the FRED fetching and CSV management functions.

- [ ] **Step 1: Create `services/rates.py`**

```python
import os
import io
import time
import logging

import numpy as np
import pandas as pd
import requests
import datetime

from config import (
    CSV_PATH, TNX_CSV_PATH, DATA_DIR,
    FRED_BASE, FRED_SERIES, CACHE_STALE_HOURS,
)

log = logging.getLogger(__name__)


def fetch_fred_series(series_id: str) -> pd.Series:
    url = f"{FRED_BASE}?id={series_id}"
    try:
        r = requests.get(url, timeout=15)
        r.raise_for_status()
        df = pd.read_csv(io.StringIO(r.text), parse_dates=[0], index_col=0)
        df.index.name = "date"
        s = df.iloc[:, 0].replace(".", np.nan).astype(float)
        return s.dropna()
    except Exception as exc:
        log.warning("FRED fetch failed for %s: %s", series_id, exc)
        return pd.Series(dtype=float)


def csv_is_fresh() -> bool:
    if not os.path.exists(CSV_PATH):
        return False
    return (time.time() - os.path.getmtime(CSV_PATH)) < CACHE_STALE_HOURS * 3600


def load_or_refresh_csv() -> pd.DataFrame:
    """Return DataFrame with columns: date, rate_30, rate_15, rate_arm."""
    if csv_is_fresh():
        try:
            df = pd.read_csv(CSV_PATH, parse_dates=["date"])
            return df.sort_values("date").reset_index(drop=True)
        except Exception as exc:
            log.warning("Could not read CSV: %s", exc)

    log.info("Refreshing rate data from FRED ...")
    s30  = fetch_fred_series(FRED_SERIES["30yr"])
    s15  = fetch_fred_series(FRED_SERIES["15yr"])
    sarm = fetch_fred_series(FRED_SERIES["arm"])

    if s30.empty:
        log.warning("FRED returned empty data; using synthetic fallback.")
        return synthetic_history()

    df = pd.DataFrame({"rate_30": s30, "rate_15": s15, "rate_arm": sarm})
    df.index = pd.to_datetime(df.index)
    df = df.sort_index().reset_index()
    df.index.name = None
    df.rename(columns={"index": "date"}, inplace=True, errors="ignore")
    df["rate_arm"] = df["rate_arm"].ffill()
    df["rate_15"]  = df["rate_15"].ffill()

    os.makedirs(DATA_DIR, exist_ok=True)
    df.to_csv(CSV_PATH, index=False)
    log.info("Saved %d rows to %s", len(df), CSV_PATH)
    return df


def synthetic_history() -> pd.DataFrame:
    rng = np.random.default_rng(42)
    dates = pd.date_range(end=datetime.date.today(), periods=52 * 20, freq="W-THU")
    n = len(dates)
    t = np.linspace(0, 1, n)
    base = (
        6.5
        - 1.5 * np.exp(-8 * (t - 0.15) ** 2)
        - 2.5 * np.exp(-8 * (t - 0.65) ** 2)
        + 2.8 * np.maximum(0, t - 0.72)
        + rng.normal(0, 0.08, n)
    )
    base = np.clip(base, 2.5, 8.5)
    r30  = np.round(base, 2)
    r15  = np.round(base - 0.65 + rng.normal(0, 0.04, n), 2)
    rarm = np.round(base - 0.3  + rng.normal(0, 0.06, n), 2)
    return pd.DataFrame({"date": dates, "rate_30": r30, "rate_15": r15, "rate_arm": rarm})


def load_tnx_data() -> pd.DataFrame:
    """
    WHY: DGS10 is daily (vs weekly mortgage). Kept in a separate file to avoid
    date-alignment issues. Refreshes every 36h same as mortgage CSV.
    """
    stale = not (
        os.path.exists(TNX_CSV_PATH) and
        (time.time() - os.path.getmtime(TNX_CSV_PATH)) < CACHE_STALE_HOURS * 3600
    )
    if not stale:
        try:
            df = pd.read_csv(TNX_CSV_PATH, parse_dates=["date"])
            return df.sort_values("date").reset_index(drop=True)
        except Exception:
            pass

    log.info("Refreshing 10Y Treasury data from FRED DGS10 ...")
    s = fetch_fred_series("DGS10")
    if s.empty:
        log.warning("DGS10 fetch failed; using synthetic TNX fallback.")
        rng = np.random.default_rng(99)
        dates = pd.date_range(end=datetime.date.today(), periods=252 * 20, freq="B")
        n = len(dates)
        t = np.linspace(0, 1, n)
        base = (
            4.5 - 1.5 * np.exp(-8*(t-0.15)**2)
            - 2.0 * np.exp(-8*(t-0.65)**2)
            + 2.5 * np.maximum(0, t - 0.72)
            + rng.normal(0, 0.06, n)
        )
        s = pd.Series(np.round(np.clip(base, 0.5, 7.0), 3), index=dates)

    df = pd.DataFrame({"date": s.index, "rate_tnx": s.values})
    df["date"] = pd.to_datetime(df["date"])
    df = df.dropna().sort_values("date").reset_index(drop=True)
    os.makedirs(DATA_DIR, exist_ok=True)
    df.to_csv(TNX_CSV_PATH, index=False)
    log.info("Saved %d TNX rows to %s", len(df), TNX_CSV_PATH)
    return df
```

- [ ] **Step 2: In `app.py`, replace the rates service functions with imports**

```python
from services.rates import (
    load_or_refresh_csv, load_tnx_data, csv_is_fresh,
)
```

Remove `_fetch_fred_series`, `_csv_is_fresh`, `_load_or_refresh_csv`, `_synthetic_history`, `_load_tnx_data` from `app.py`. Update all call sites: `_load_or_refresh_csv()` → `load_or_refresh_csv()`, `_csv_is_fresh()` → `csv_is_fresh()`, `_load_tnx_data()` → `load_tnx_data()`.

- [ ] **Step 3: Verify**

```bash
flask run --port 5050
curl http://localhost:5050/api/rates | python3 -m json.tool | head -10
# Expected: same JSON structure as baseline
```

- [ ] **Step 4: Commit**

```bash
git add services/rates.py app.py
git commit -m "refactor: extract FRED data service to services/rates.py"
```

---

## Task 4: Extract services/forecast.py

**Files:**
- Create: `services/forecast.py`
- Modify: `app.py`

- [ ] **Step 1: Create `services/forecast.py`**

```python
import math
import numpy as np
import pandas as pd


def rsi(series: pd.Series, period: int = 14) -> float:
    delta = series.diff().dropna()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(period).mean().iloc[-1]
    avg_loss = loss.rolling(period).mean().iloc[-1]
    if avg_loss == 0:
        return 100.0
    return round(100 - 100 / (1 + avg_gain / avg_loss), 1)


def linear_projection(series: pd.Series, days_back: int, days_forward: int):
    """OLS projection returning (value, low_ci, high_ci)."""
    tail = series.dropna().tail(days_back)
    if len(tail) < 4:
        last = float(series.dropna().iloc[-1])
        return last, last - 0.2, last + 0.2
    x = np.arange(len(tail))
    slope, intercept = np.polyfit(x, tail.values, 1)
    proj = slope * (len(tail) + days_forward) + intercept
    residuals = tail.values - (slope * x + intercept)
    std = np.std(residuals) * math.sqrt(days_forward / len(tail) + 1)
    return round(proj, 2), round(proj - 1.96 * std, 2), round(proj + 1.96 * std, 2)


def percentile_in_history(current: float, series: pd.Series) -> float:
    vals = series.dropna().values
    return round(float(np.sum(vals <= current) / len(vals) * 100), 1)
```

- [ ] **Step 2: In `app.py`, replace with imports**

```python
from services.forecast import rsi, linear_projection, percentile_in_history
```

Remove `_rsi`, `_linear_projection`, `_percentile_in_history` from `app.py`. Update call sites (drop the `_` prefix).

- [ ] **Step 3: Verify**

```bash
curl http://localhost:5050/api/forecast | python3 -m json.tool
# Expected: trend, ma7, ma30, rsi, analysis, projection_30d, projection_60d all present
```

- [ ] **Step 4: Commit**

```bash
git add services/forecast.py app.py
git commit -m "refactor: extract forecast calculations to services/forecast.py"
```

---

## Task 5: Extract services/news.py

**Files:**
- Create: `services/news.py`
- Modify: `app.py`

- [ ] **Step 1: Create `services/news.py`**

```python
import logging
import feedparser
from services.cache import cached

log = logging.getLogger(__name__)

LOWER_KEYWORDS   = ["cut", "drop", "fall", "fell", "decline", "dovish", "pause",
                    "inflation easing", "cool", "lower", "decrease", "below"]
HIGHER_KEYWORDS  = ["hike", "rise", "surge", "hawkish", "hot cpi", "higher",
                    "increase", "above", "jump", "spike", "accelerat"]
MORTGAGE_KEYWORDS = ["mortgage", "home loan", "30-year", "15-year", "refinanc",
                     "homebuyer", "housing"]
FED_KEYWORDS     = ["federal reserve", "fed ", " fed,", "fomc", "powell",
                    "interest rate", "rate decision"]
# defined but not yet used in classify_article — kept for future filter extension
ECONOMY_KEYWORDS = ["cpi", "inflation", "gdp", "unemployment", "jobs report",
                    "nonfarm", "recession", "economy"]

NEWS_FEEDS = [
    "https://news.google.com/rss/search?q=mortgage+rates&hl=en-US&gl=US&ceid=US:en",
    "https://news.google.com/rss/search?q=federal+reserve+interest+rates&hl=en-US&gl=US&ceid=US:en",
    "https://news.google.com/rss/search?q=CPI+inflation+economy&hl=en-US&gl=US&ceid=US:en",
]


def classify_article(title: str, summary: str = "") -> dict:
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
def fetch_news() -> list:
    articles = []
    for feed_url in NEWS_FEEDS:
        try:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries[:8]:
                title   = entry.get("title", "")
                summary = entry.get("summary", "")
                summary_clean = (
                    summary.replace("<b>", "").replace("</b>", "")
                    .replace("&amp;", "&")[:200]
                )
                info = classify_article(title, summary)
                articles.append({
                    "title":     title,
                    "summary":   summary_clean,
                    "source":    entry.get("source", {}).get("title", "Google News"),
                    "published": entry.get("published", ""),
                    "sentiment": info["sentiment"],
                    "category":  info["category"],
                    "url":       entry.get("link", "#"),
                })
        except Exception as exc:
            log.warning("News feed error: %s", exc)

    seen, unique = set(), []
    for a in articles:
        if a["title"] not in seen:
            seen.add(a["title"])
            unique.append(a)
    return unique[:20]
```

- [ ] **Step 2: In `app.py`, replace with imports**

```python
from services.news import fetch_news
```

Remove `LOWER_KEYWORDS`, `HIGHER_KEYWORDS`, `MORTGAGE_KEYWORDS`, `FED_KEYWORDS`, `NEWS_FEEDS`, `_classify_article`, `_fetch_news` from `app.py`. Update call sites: `_fetch_news()` → `fetch_news()`.

- [ ] **Step 3: Verify**

```bash
curl http://localhost:5050/api/news | python3 -m json.tool | head -10
# Expected: articles list + signal dict
```

- [ ] **Step 4: Commit**

```bash
git add services/news.py app.py
git commit -m "refactor: extract news service to services/news.py"
```

---

## Task 6: Extract services/parcel.py

**Files:**
- Create: `services/parcel.py`
- Modify: `app.py`

Move the parcel cache, ArcGIS, and Socrata logic.

- [ ] **Step 1: Create `services/parcel.py`**

```python
import json
import os
import logging

from config import DATA_DIR, PARCEL_CACHE_PATH

log = logging.getLogger(__name__)

SCOUT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/javascript, */*",
    "Accept-Language": "en-US,en;q=0.9",
}

STATE_ABBR = {
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


def load_parcel_cache() -> dict:
    if not os.path.exists(PARCEL_CACHE_PATH):
        return {}
    try:
        with open(PARCEL_CACHE_PATH) as f:
            return json.load(f)
    except Exception as exc:
        log.warning("Could not read parcel cache: %s", exc)
        return {}


def save_parcel_cache(cache: dict) -> None:
    try:
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(PARCEL_CACHE_PATH, "w") as f:
            json.dump(cache, f)
    except Exception as exc:
        log.warning("Could not save parcel cache: %s", exc)
```

- [ ] **Step 2: In `app.py`, replace with imports**

```python
from services.parcel import SCOUT_HEADERS, STATE_ABBR, load_parcel_cache, save_parcel_cache
```

Remove `_load_parcel_cache`, `_save_parcel_cache`, `_parcel_cache`, `_SCOUT_HEADERS`, `_STATE_ABBR` from `app.py`.
The `_parcel_cache` global and all ArcGIS/Socrata query logic stays in-situ inside `api_parcel` — it moves to `routes/scout.py` in Task 7e.

- [ ] **Step 3: Verify**

```bash
flask run --port 5050
curl "http://localhost:5050/api/parcel?lat=47.6062&lon=-122.3321" | python3 -m json.tool
```

- [ ] **Step 4: Commit**

```bash
git add services/parcel.py app.py
git commit -m "refactor: extract parcel service to services/parcel.py"
```

---

## Task 7: Extract routes/ using Flask Blueprints

**Files:**
- Create: `routes/__init__.py`
- Create: `routes/pages.py`
- Create: `routes/rates.py`
- Create: `routes/forecast.py`
- Create: `routes/news.py`
- Create: `routes/scout.py`
- Modify: `app.py`

### Step 7a — routes/pages.py

- [ ] **Create `routes/__init__.py`**

```python
from routes.pages    import pages_bp
from routes.rates    import rates_bp
from routes.forecast import forecast_bp
from routes.news     import news_bp
from routes.scout    import scout_bp


def register_blueprints(app):
    app.register_blueprint(pages_bp)
    app.register_blueprint(rates_bp)
    app.register_blueprint(forecast_bp)
    app.register_blueprint(news_bp)
    app.register_blueprint(scout_bp)
```

- [ ] **Create `routes/pages.py`**

```python
from flask import Blueprint, render_template

pages_bp = Blueprint("pages", __name__)


@pages_bp.route("/")
def index():
    return render_template("index.html")
```

### Step 7b — routes/rates.py

- [ ] **Create `routes/rates.py`**

Move `api_rates`, `api_history`, `api_rate_history_table` from `app.py`:

```python
import numpy as np
import pandas as pd
from flask import Blueprint, jsonify, request

from services.cache import cached
from services.rates import load_or_refresh_csv, load_tnx_data, csv_is_fresh

rates_bp = Blueprint("rates", __name__)


@rates_bp.route("/api/rates")
@cached()
def api_rates():
    # ... paste the full function body from app.py, unchanged ...
    # NOTE: rename _load_or_refresh_csv → load_or_refresh_csv, _load_tnx_data → load_tnx_data


@rates_bp.route("/api/history")
def api_history():
    # ... paste the full function body from app.py, unchanged ...
    # NOTE: rename _load_or_refresh_csv → load_or_refresh_csv, _load_tnx_data → load_tnx_data


@rates_bp.route("/api/rate_history_table")
@cached()
def api_rate_history_table():
    # ... paste the full function body from app.py, unchanged ...
    # NOTE: rename _load_or_refresh_csv → load_or_refresh_csv
```

> **Important:** paste the exact existing function bodies — do not rewrite logic.

### Step 7c — routes/forecast.py

- [ ] **Create `routes/forecast.py`**

```python
from flask import Blueprint, jsonify

from services.cache import cached
from services.rates import load_or_refresh_csv
from services.forecast import rsi, linear_projection, percentile_in_history

forecast_bp = Blueprint("forecast", __name__)


@forecast_bp.route("/api/forecast")
@cached()
def api_forecast():
    # ... paste the full function body from app.py, unchanged ...
    # NOTE: rename _rsi → rsi, _linear_projection → linear_projection,
    #       _percentile_in_history → percentile_in_history,
    #       _load_or_refresh_csv → load_or_refresh_csv
```

### Step 7d — routes/news.py

- [ ] **Create `routes/news.py`**

```python
import datetime
from flask import Blueprint, jsonify
from services.news import fetch_news

news_bp = Blueprint("news", __name__)


@news_bp.route("/api/news")
def api_news():
    # ... paste the full function body from app.py, unchanged ...
    # NOTE: rename _fetch_news → fetch_news
```

### Step 7e — routes/scout.py

- [ ] **Create `routes/scout.py`**

```python
import logging
from flask import Blueprint, jsonify, request
import requests

from services.parcel import SCOUT_HEADERS, STATE_ABBR, load_parcel_cache, save_parcel_cache

log = logging.getLogger(__name__)
scout_bp = Blueprint("scout", __name__)

# WHY: loaded eagerly at module scope to match app.py behavior where
# _parcel_cache was populated at import time (line 93 of original app.py).
_parcel_cache: dict = load_parcel_cache()


@scout_bp.route("/api/scout")
def api_scout():
    # ... paste the full function body from app.py, unchanged ...
    # NOTE: _SCOUT_HEADERS → SCOUT_HEADERS, _STATE_ABBR → STATE_ABBR
    # NOTE: log.info(f"Redfin autocomplete failed: {exc}")
    #     → log.info("Redfin autocomplete failed: %s", exc)


@scout_bp.route("/api/parcel")
def api_parcel():
    # ... paste the full function body from app.py (lines 768-892) ...
    # NOTE: 3 targeted symbol replacements only:
    #   _save_parcel_cache(_parcel_cache) → save_parcel_cache(_parcel_cache)
    #   _SCOUT_HEADERS → SCOUT_HEADERS
    #   _load_parcel_cache()  (only in the scout module-level line above, not inside api_parcel)
    # Do NOT change any logic, params, field names, or error handling paths.
```

### Step 7f — Slim app.py

- [ ] **Replace `app.py` with the slim version**

```python
"""
Oh My House — Flask entry point.
Routes are defined in routes/. Business logic lives in services/.
"""
import logging
import os

from flask import Flask

from routes import register_blueprints
from services.rates import load_or_refresh_csv

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

app = Flask(__name__)
register_blueprints(app)


def _seed_on_startup() -> None:
    data_csv = os.path.join(os.path.dirname(__file__), "data", "rate_history.csv")
    if not os.path.exists(data_csv):
        logging.getLogger(__name__).info("Seeding rate data from FRED on startup ...")
        load_or_refresh_csv()


if __name__ == "__main__":
    _seed_on_startup()
    port = int(os.environ.get("PORT", 5050))
    app.run(debug=False, host="0.0.0.0", port=port)
```

- [ ] **Verify all endpoints**

```bash
flask run --port 5050
curl http://localhost:5050/             # -> 200 HTML
curl http://localhost:5050/api/rates    # -> JSON with rates.30yr.current
curl http://localhost:5050/api/history?range=3M  # -> JSON with labels array
curl http://localhost:5050/api/forecast # -> JSON with trend, ma7, rsi
curl http://localhost:5050/api/news     # -> JSON with articles array
curl http://localhost:5050/api/rate_history_table  # -> JSON with rows array
```

- [ ] **Commit**

```bash
git add routes/ app.py
git commit -m "refactor: extract all routes to Flask Blueprints in routes/"
```

---

## Task 8: Extract CSS to static/css/style.css

**Files:**
- Create: `static/css/style.css`
- Modify: `templates/index.html`

**Scope:** everything between `<style>` and `</style>` in `index.html` — approximately lines 1–1100.

- [ ] **Step 1: Create `static/css/style.css`**

Open `index.html`, select the entire content of the `<style>` block (everything between `<style>` and `</style>`), paste into `static/css/style.css`.

- [ ] **Step 2: Replace the `<style>` block in `index.html` with a `<link>` tag**

```html
<link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
```

- [ ] **Step 3: Verify the page looks identical**

```bash
flask run --port 5050
# Open http://localhost:5050 in browser
# All styles should be identical — check sidebar, rate cards, chart, dark themes
```

- [ ] **Step 4: Commit**

```bash
git add static/css/style.css templates/index.html
git commit -m "refactor: extract CSS to static/css/style.css"
```

---

## Task 9: Extract JS to static/js/app.js

**Files:**
- Create: `static/js/app.js`
- Modify: `templates/index.html`

**Scope:** everything between `<script>` and `</script>` at the bottom of `index.html` (the large inline script — not the CDN `<script src="...">` tags, leave those in place).

- [ ] **Step 1: Create `static/js/app.js`**

Copy the content of the inline `<script>` block (everything between the last `<script>` and `</script>` tags) into `static/js/app.js`.

- [ ] **Step 2: Replace the inline `<script>` block in `index.html`**

```html
<script src="{{ url_for('static', filename='js/app.js') }}"></script>
```

This must go after all CDN script tags (Chart.js etc.) but before `</body>`.

- [ ] **Step 3: Verify full app functionality**

```bash
flask run --port 5050
# Open http://localhost:5050 in browser and test:
# - Dashboard loads with rate cards and chart
# - Refi Savings calculator computes correctly
# - Payment calculator works
# - Rate history table loads
# - News tab loads
# - Language switcher (EN / ZH / ES) works
# - Theme switcher works
```

- [ ] **Step 4: Commit**

```bash
git add static/js/app.js templates/index.html
git commit -m "refactor: extract JS to static/js/app.js"
```

---

## Final State Check

After all tasks are complete:

```bash
# Count lines to confirm the split worked
wc -l app.py templates/index.html static/css/style.css static/js/app.js \
   services/*.py routes/*.py config.py
```

Expected result:
- `app.py` < 40 lines
- `templates/index.html` < 100 lines (HTML skeleton only)
- All services < 200 lines each
- All routes < 150 lines each

Then commit the plan doc and do the two-commit submodule update:

```bash
# Inside SecurityKB/:
git add docs/
git commit -m "docs: add modular refactor implementation plan"

# In vault root:
git add wiki/reference/SecurityKB
git commit -m "chore(submodule): update SecurityKB pointer after modular refactor"
```
