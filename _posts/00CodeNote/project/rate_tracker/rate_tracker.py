#!/usr/bin/env python3
"""
Mortgage Rate Tracker
Fetches the 10-Year US Treasury yield daily, sends a desktop notification,
logs the rate to a CSV, and updates a trend chart image.

On the very first run it back-fills 90 days of history from Yahoo Finance
so the chart is always generated immediately.
"""

import csv
import datetime
import json
import platform
import subprocess
import sys
from pathlib import Path


# ── Dependencies (auto-install if missing) ──────────────────────────────────
def ensure(pkg, import_as=None):
    import importlib
    name = import_as or pkg
    try:
        importlib.import_module(name)
    except ImportError:
        print(f"[Setup] Installing {pkg}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg, "-q"])

ensure("requests")
ensure("matplotlib")
ensure("numpy")

import matplotlib
import matplotlib.ticker as ticker
import requests

matplotlib.use("Agg")          # headless – saves to file, no GUI window
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np

# ── Config ──────────────────────────────────────────────────────────────────
BASE_DIR    = Path(__file__).parent
CSV_FILE         = BASE_DIR / "rate_history.csv"
CHART_FILE_YTD   = BASE_DIR / f"rate_trend_{__import__('datetime').date.today().year}.png"
CHART_FILE_ALL   = BASE_DIR / "rate_trend_all_years.png"
CONFIG_FILE      = BASE_DIR / "config.json"

# Yahoo Finance endpoints
YAHOO_TODAY = (
    "https://query1.finance.yahoo.com/v8/finance/chart/%5ETNX"
    "?interval=1d&range=1d"
)
# period1=1577836800 is Unix timestamp for 2020-01-01 00:00:00 UTC
YAHOO_SINCE_2020 = (
    "https://query1.finance.yahoo.com/v8/finance/chart/%5ETNX"
    "?interval=1d&period1=1577836800&period2=9999999999"
)

# Rough mortgage spread over 10-yr treasury (historical avg ≈ 1.7–2.0 pp)
MORTGAGE_SPREAD = 1.23   # percentage points

# Alert when rate moves more than this since last check
ALERT_THRESHOLD = 0.10   # 10 basis points

# ── Refi target alerts ───────────────────────────────────────────────────────
# Notify once each time est. mortgage drops TO or BELOW one of these levels.
REFI_TARGETS = [5.2, 5.1, 4.0]

# Tracks which targets have already fired (prevents daily spam)
TARGETS_FILE = BASE_DIR / 'triggered_targets.json'


# ── Load / save config ──────────────────────────────────────────────────────
def load_config():
    if CONFIG_FILE.exists():
        return json.loads(CONFIG_FILE.read_text())
    return {}


# ── Fetch today's 10-yr yield ────────────────────────────────────────────────
def fetch_today_yield() -> float | None:
    try:
        r = requests.get(YAHOO_TODAY, timeout=10,
                         headers={"User-Agent": "Mozilla/5.0"})
        r.raise_for_status()
        price = r.json()["chart"]["result"][0]["meta"]["regularMarketPrice"]
        return round(float(price), 3)
    except Exception as e:
        print(f"[Fetch today failed] {e}")
        return None


# ── Back-fill history since Jan 1 2025 (first run only) ─────────────────────
def fetch_and_seed_history():
    """Downloads all daily closes since Jan 1 2020 and writes them to the CSV."""
    print("[Setup] First run – seeding all data since 2020-01-01 from Yahoo Finance...")
    try:
        r = requests.get(YAHOO_SINCE_2020, timeout=15,
                         headers={"User-Agent": "Mozilla/5.0"})
        r.raise_for_status()
        result = r.json()["chart"]["result"][0]
        timestamps = result["timestamp"]
        closes     = result["indicators"]["quote"][0]["close"]

        rows = []
        for ts, close in zip(timestamps, closes):
            if close is None:
                continue
            d = datetime.date.fromtimestamp(ts)
            rows.append((d.isoformat(), round(close, 3)))

        if not rows:
            print("[Setup] No historical rows returned – skipping seed.")
            return

        with open(CSV_FILE, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["date", "10yr_yield", "est_mortgage_rate"])
            for date_str, rate in rows:
                w.writerow([date_str, rate, round(rate + MORTGAGE_SPREAD, 3)])

        print(f"[Setup] Seeded {len(rows)} data points from 2020-01-01 to today.")
    except Exception as e:
        print(f"[Setup] Could not seed history: {e}")


# ── CSV helpers ──────────────────────────────────────────────────────────────
def append_to_csv(date_str: str, rate: float):
    with open(CSV_FILE, "a", newline="") as f:
        w = csv.writer(f)
        w.writerow([date_str, rate, round(rate + MORTGAGE_SPREAD, 3)])

def read_history() -> list[dict]:
    if not CSV_FILE.exists():
        return []
    with open(CSV_FILE, newline="") as f:
        return list(csv.DictReader(f))

def today_already_logged() -> bool:
    today = datetime.date.today().isoformat()
    return any(row["date"] == today for row in read_history())

def get_last_rate() -> float | None:
    history = read_history()
    # Last entry that is NOT today
    today = datetime.date.today().isoformat()
    past = [r for r in history if r["date"] != today]
    return float(past[-1]["10yr_yield"]) if past else None


# ── Refi target alert logic ──────────────────────────────────────────────────
def load_triggered() -> set:
    if TARGETS_FILE.exists():
        return set(json.loads(TARGETS_FILE.read_text()))
    return set()

def save_triggered(triggered: set):
    TARGETS_FILE.write_text(json.dumps(sorted(triggered)))

def check_refi_targets(est_mortgage: float):
    triggered = load_triggered()
    newly_hit = []
    for target in sorted(REFI_TARGETS):
        key = str(target)
        if key not in triggered and est_mortgage <= target:
            newly_hit.append(target)
            triggered.add(key)
        elif key in triggered and est_mortgage > target + 0.25:
            triggered.discard(key)
    save_triggered(triggered)
    for target in newly_hit:
        title = f'Refi Alert: Mortgage hit {target}%!'
        msg   = (f'Est. 30-yr mortgage is now {est_mortgage:.2f}% -- '
                 f'your target of {target}% has been reached. Time to call your lender!')
        print(f'[Refi Alert] {title}')
        notify(title, msg)
        try:
            subprocess.run(
                ['osascript', '-e',
                 f'display alert "{title}" message "{msg}" as warning'],
                timeout=10
            )
        except Exception:
            pass


# ── Shared chart theme ───────────────────────────────────────────────────────
BG       = "#111318"
CARD_BG  = "#1a1d26"
GRID     = "#2a2d3a"
YIELD_C  = "#4fc3f7"
MTG_C    = "#e07b39"
MA_C     = "#6b9e4e"
TEXT     = "#e0e6f0"
MUTED    = "#8a90a0"
POSITIVE = "#4caf82"
INFO_BG  = "#1a2a3a"
INFO_FG  = "#64b5f6"


def _draw_chart(dates, yields, mtg, title_str, out_path, show_cards=True, year_only_x=False):
    """Core chart renderer. Shared by all chart types."""
    import matplotlib.patches as mpatches

    all_vals = yields + mtg
    y_min    = min(all_vals) - 0.2
    y_max    = max(all_vals) + 0.3

    last_yield = yields[-1]
    last_mtg   = mtg[-1]
    prev_yield = yields[-2] if len(yields) >= 2 else last_yield
    delta      = round(last_yield - prev_yield, 3)
    arrow      = "\u25bc" if delta <= 0 else "\u25b2"
    delta_color = POSITIVE if delta <= 0 else MTG_C

    low_90_val  = min(yields[-90:])
    high_90_val = max(yields[-90:])
    low_90_idx  = yields[-90:].index(low_90_val)
    high_90_idx = yields[-90:].index(high_90_val)
    base        = max(0, len(dates) - 90)
    low_90_date  = dates[base + low_90_idx].strftime("%b %-d, %Y")
    high_90_date = dates[base + high_90_idx].strftime("%b %-d, %Y")

    fig_h = 7.8 if show_cards else 6.0
    fig = plt.figure(figsize=(14, fig_h), facecolor=BG)

    if show_cards:
        gs = fig.add_gridspec(2, 1, height_ratios=[1, 4], hspace=0.32)
        ax = fig.add_subplot(gs[1])
    else:
        ax = fig.add_subplot(1, 1, 1)

    # ── Title ────────────────────────────────────────────────────────────────
    title_y = 0.965 if show_cards else 0.97
    fig.text(0.5, title_y, title_str,
             ha="center", va="top", color=TEXT,
             fontsize=13, fontweight="bold", transform=fig.transFigure)

    # ── Metric cards ─────────────────────────────────────────────────────────
    if show_cards:
        cards = [
            ("10-yr Treasury",      f"{last_yield:.2f}%", f"{arrow} {abs(delta):.2f}% today", delta_color),
            ("Est. 30-yr Mortgage",  f"{last_mtg:.2f}%",  f"{arrow} {abs(delta):.2f}% today", delta_color),
            ("90-day low",           f"{low_90_val:.2f}%", low_90_date,  MUTED),
            ("90-day high",          f"{high_90_val:.2f}%",high_90_date, MUTED),
        ]
        card_w, card_h = 0.21, 0.095
        card_gap = 0.023
        start_x  = 0.03
        top_y    = 0.875
        for i, (label, value, sub, sub_color) in enumerate(cards):
            x = start_x + i * (card_w + card_gap)
            fig.add_artist(mpatches.FancyBboxPatch(
                (x, top_y - card_h), card_w, card_h,
                boxstyle="round,pad=0.01", linewidth=0,
                facecolor=CARD_BG, transform=fig.transFigure, clip_on=False
            ))
            fig.text(x + 0.01, top_y - 0.016, label,   fontsize=8,  color=MUTED, transform=fig.transFigure)
            fig.text(x + 0.01, top_y - 0.054, value,   fontsize=15, color=TEXT,  fontweight="bold", transform=fig.transFigure)
            fig.text(x + 0.01, top_y - 0.078, sub,     fontsize=8,  color=sub_color, transform=fig.transFigure)

    # ── Chart ────────────────────────────────────────────────────────────────
    ax.set_facecolor(BG)
    ax.fill_between(dates, yields, mtg, alpha=0.06, color=YIELD_C, zorder=1)
    ax.plot(dates, yields, color=YIELD_C, linewidth=1.8, label="10-yr Treasury", zorder=3)
    ax.scatter(dates[::3], yields[::3], color=YIELD_C, s=14, zorder=4, linewidths=0)
    ax.plot(dates, mtg, color=MTG_C, linewidth=1.8, linestyle="--", label="Est. mortgage", zorder=3)
    ax.scatter(dates[::3], mtg[::3], color=MTG_C, s=8, zorder=4, linewidths=0)

    if len(yields) >= 7:
        window    = min(30, len(yields))
        sma       = np.convolve(yields, np.ones(window) / window, mode="valid")
        sma_dates = dates[window - 1:]
        ax.plot(sma_dates, sma, color=MA_C, linewidth=1.5, label="30-day MA", zorder=3)

    # Refi target lines
    triggered = load_triggered()
    for target in REFI_TARGETS:
        hit   = str(target) in triggered
        color = "#4caf82" if hit else "#ffd54f"
        ax.axhline(y=target, color=color, linewidth=1.0,
                   linestyle=(0, (4, 4)), alpha=0.8, zorder=2)
        ax.text(dates[0], target + 0.04, f"Target {target}%" + (" (hit)" if hit else ""),
                color=color, fontsize=7.5, va="bottom")

    # End-labels
    ax.annotate(f"{last_yield:.2f}%", xy=(dates[-1], last_yield),
                xytext=(6, 0), textcoords="offset points",
                color=YIELD_C, fontsize=8.5, fontweight="bold", va="center")
    ax.annotate(f"{last_mtg:.2f}%", xy=(dates[-1], last_mtg),
                xytext=(6, 0), textcoords="offset points",
                color=MTG_C, fontsize=8.5, fontweight="bold", va="center")

    # Axes
    ax.set_ylim(y_min, y_max)
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda v, _: f"{v:.2f}%"))

    if year_only_x:
        ax.xaxis.set_major_locator(mdates.YearLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    else:
        def smart_month_fmt(x, pos):
            dt = mdates.num2date(x)
            return dt.strftime("%b %Y") if dt.month == 1 else dt.strftime("%b")

        ax.xaxis.set_major_formatter(ticker.FuncFormatter(smart_month_fmt))
        ax.xaxis.set_major_locator(mdates.MonthLocator())
    fig.autofmt_xdate(rotation=0, ha="center")

    for spine in ax.spines.values():
        spine.set_color(GRID)
    ax.tick_params(colors=MUTED, labelsize=8)
    ax.grid(color=GRID, linewidth=0.5, zorder=0, alpha=0.8)
    ax.legend(facecolor=CARD_BG, edgecolor=GRID, labelcolor=TEXT,
              fontsize=8.5, loc="upper left", handlelength=1.8,
              handleheight=0.8, framealpha=1, borderpad=0.6)

    # Bottom banner
    tip = ("Rates are currently trending down — worth monitoring for a refi window."
           if delta <= 0 else "Rates are rising — keep monitoring for a dip.")
    banner_y = 0.018
    fig.add_artist(mpatches.FancyBboxPatch(
        (0.03, banner_y - 0.005), 0.94, 0.042,
        boxstyle="round,pad=0.005", linewidth=0,
        facecolor=INFO_BG, transform=fig.transFigure, clip_on=False
    ))
    fig.text(0.5, banner_y + 0.010, tip,
             ha="center", color=INFO_FG, fontsize=8.5,
             style="italic", transform=fig.transFigure)

    top = 0.86 if show_cards else 0.93
    plt.tight_layout(rect=[0, 0.07, 1, top])
    fig.savefig(out_path, dpi=150, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print(f"[Chart] Saved → {out_path}")


# ── Build YTD chart for a specific year ──────────────────────────────────────
def build_year_chart(history: list[dict], year: int):
    rows = [r for r in history if r["date"].startswith(str(year))]
    if not rows:
        return
    dates  = [datetime.date.fromisoformat(r["date"]) for r in rows]
    yields = [float(r["10yr_yield"])        for r in rows]
    mtg    = [float(r["est_mortgage_rate"]) for r in rows]

    label    = "YTD" if year == datetime.date.today().year else "Full Year"
    today    = datetime.date.today().isoformat()
    updated  = today if year == datetime.date.today().year else rows[-1]["date"]
    title    = f"10-Yr Treasury & Mortgage Rate — {year} {label}  ·  Last updated {updated}"
    out_path = BASE_DIR / f"rate_trend_{year}.png"
    _draw_chart(dates, yields, mtg, title, out_path, show_cards=(year == datetime.date.today().year))
    return out_path


# ── Build overall all-years chart ────────────────────────────────────────────
def build_overall_chart(history: list[dict]):
    if not history:
        return
    dates  = [datetime.date.fromisoformat(r["date"]) for r in history]
    yields = [float(r["10yr_yield"])        for r in history]
    mtg    = [float(r["est_mortgage_rate"]) for r in history]
    start  = dates[0].strftime("%b %Y")
    end    = dates[-1].strftime("%b %Y")
    title  = f"10-Yr Treasury & Est. Mortgage Rate — Historic View ({start} to {end})"
    out_path = BASE_DIR / "rate_trend_all_years.png"
    _draw_chart(dates, yields, mtg, title, out_path, show_cards=False, year_only_x=True)
    return out_path


# ── Master chart builder — called every run ───────────────────────────────────
def build_all_charts():
    history = read_history()
    if not history:
        print("[Chart] No data – skipping.")
        return

    today_year = datetime.date.today().year

    # Years present in CSV
    years = sorted(set(int(r["date"][:4]) for r in history))

    for year in years:
        out_path = BASE_DIR / f"rate_trend_{year}.png"
        # Always regenerate current year; only create past years if missing
        if year == today_year or not out_path.exists():
            build_year_chart(history, year)

    # Always regenerate overall chart
    build_overall_chart(history)

# ── Desktop notifications ────────────────────────────────────────────────────
def notify(title: str, message: str):
    system = platform.system()
    try:
        if system == "Darwin":
            subprocess.run(
                ["osascript", "-e",
                 f'display notification "{message}" with title "{title}"'],
                check=True
            )
        elif system == "Windows":
            try:
                from win10toast import ToastNotifier
                ToastNotifier().show_toast(title, message, duration=10, threaded=True)
            except ImportError:
                ps = (
                    f"Add-Type -AssemblyName System.Windows.Forms;"
                    f"$n=New-Object System.Windows.Forms.NotifyIcon;"
                    f"$n.Icon=[System.Drawing.SystemIcons]::Information;"
                    f"$n.BalloonTipTitle='{title}';"
                    f"$n.BalloonTipText='{message}';"
                    f"$n.Visible=$True;$n.ShowBalloonTip(5000)"
                )
                subprocess.run(["powershell", "-Command", ps], check=True)
        elif system == "Linux":
            subprocess.run(["notify-send", title, message], check=True)
        print(f"[Notification] {title}: {message}")
    except Exception as e:
        print(f"[Notification fallback] {title}: {message}  ({e})")


# ── Main ─────────────────────────────────────────────────────────────────────
def main():
    print(f"\n{'='*55}")
    print(f"  Mortgage Rate Tracker  –  {datetime.datetime.now():%Y-%m-%d %H:%M}")
    print(f"{'='*55}")

    # ── --reseed flag: wipe CSV and re-download all data since 2025-01-01 ────
    if "--reseed" in sys.argv:
        print("[Reseed] Deleting existing CSV and re-fetching all data since 2025...")
        if CSV_FILE.exists():
            CSV_FILE.unlink()
        fetch_and_seed_history()
        build_all_charts()
        print(f"\n[Done] Reseed complete. Charts saved to {BASE_DIR}\n")
        return

    # ── First-run: seed historical data so chart works immediately ───────────
    if not CSV_FILE.exists():
        fetch_and_seed_history()

    # ── Already ran today? Just refresh the chart ────────────────────────────
    if today_already_logged():
        print("[Info] Rate already logged today. Refreshing chart.")
        build_all_charts()
        return

    # ── Fetch today's rate ───────────────────────────────────────────────────
    rate = fetch_today_yield()
    if rate is None:
        msg = "Could not fetch today's 10-yr Treasury yield. Check your connection."
        print(f"[Error] {msg}")
        notify("Mortgage Rate Tracker", msg)
        return

    today        = datetime.date.today().isoformat()
    est_mortgage = round(rate + MORTGAGE_SPREAD, 3)
    last_rate    = get_last_rate()

    append_to_csv(today, rate)
    print(f"[Logged] {today}  |  10-yr: {rate}%  |  Est. mortgage: {est_mortgage}%")

    # ── Check refi targets (fires urgent alert if any level crossed) ─────────
    check_refi_targets(est_mortgage)

    # ── Notification message ─────────────────────────────────────────────────
    change_str = ""
    if last_rate is not None:
        delta      = round(rate - last_rate, 3)
        arrow      = "Up" if delta > 0 else ("Down" if delta < 0 else "Unchanged")
        change_str = f"  {arrow} {delta:+.3f}% vs yesterday"

    msg = (
        f"10-Yr Treasury: {rate}%{change_str}\n"
        f"Est. 30-yr Mortgage: {est_mortgage}%\n"
        f"YTD chart: {CHART_FILE_YTD}"
    )

    if last_rate and abs(rate - last_rate) >= ALERT_THRESHOLD:
        notify("Mortgage Rate Alert!", msg)
    else:
        notify("Daily Mortgage Rate Update", msg)

    # ── Rebuild chart ────────────────────────────────────────────────────────
    build_all_charts()
    print(f"\n[Done] Charts saved to {BASE_DIR}\n")


if __name__ == "__main__":
    main()
