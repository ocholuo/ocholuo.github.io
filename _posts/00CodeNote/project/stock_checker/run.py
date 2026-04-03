#!/usr/bin/env python3
"""
Universal Stock Checker
────────────────────────────────────────────────────────────────────────────
Track items from any store. Each item lives in WATCHLIST as a config dict.
To add a new item, just append a new entry to WATCHLIST — no other code changes needed.

Run:   python3 stock_checker.py              # checks all active items
       python3 stock_checker.py --list       # show all tracked items
       python3 stock_checker.py --item 0     # check only item at index 0
"""

import argparse
import gzip as gzip_module
import json
import subprocess
import urllib.request
from datetime import datetime

LOG_FILE = "/tmp/stock_checker.log"

# ══════════════════════════════════════════════════════════════════════════════
#  WATCHLIST  — add / edit / disable items here
# ══════════════════════════════════════════════════════════════════════════════
WATCHLIST = [

    # ── Item 0: Costco — Kohler Rodean Faucet ────────────────────────────────
    {
        "active":    True,
        "name":      "Kohler Rodean Faucet (Stainless / Touchless)",
        "store":     "Costco",
        "url":       "https://www.costco.com/p/-/kohler-rodean-kitchen-sink-faucet/4000404952?langId=-1",
        "item_id":   "1000104",
        "model":     "R38473-RT2-LVS",

        # Variant selectors: text labels to click on the product page (in order).
        # Costco shows attribute buttons like "Stainless Steel" and "Touchless".
        "variant_selectors": ["Stainless Steel", "Touchless"],

        "store_profile": "costco",
        "use_selenium":  True,   # use headless Chrome — required for JS-rendered pages
        "open_on_stock": True,
    },

    # {
    #     "active":    True,                   # set False to pause without deleting
    #     "name":      "Kohler Rodean Faucet (Matte Black / Touchless)",
    #     "store":     "Costco",
    #     "url":       "https://www.costco.com/p/-/kohler-rodean-kitchen-sink-faucet/4000404952?langId=-1",
    #     "item_id":   "1000105",              # Costco item # (for your reference)
    #     "model":     "R38473-RT2-BL",       # model number (for your reference)

    #     # All these words must appear on the page to confirm it's the right variant.
    #     # Case-insensitive. Leave empty [] to skip variant check.
    #     "variant_keywords": ["matte black", "touchless"],

    #     # Store-specific in-stock / out-of-stock HTML signals.
    #     # Uses "costco" profile by default — see STORE_PROFILES below.
    #     "store_profile": "costco",

    #     # Open the URL in browser automatically when IN STOCK?
    #     "open_on_stock": True,
    # },

    # ── Add more items below this line ───────────────────────────────────────
    # Example (commented out — uncomment and fill in when ready):
    #
    # {
    #     "active":    True,
    #     "name":      "Lululemon Align Dress (size 6, Dark Olive)",
    #     "store":     "Lululemon",
    #     "url":       "https://www.lululemon.com/en-us/p/align-dress/...",
    #     "item_id":   "",
    #     "model":     "",
    #     "variant_keywords": ["dark olive", "size 6"],
    #     "store_profile": "lululemon",
    #     "open_on_stock": True,
    # },

]

# ══════════════════════════════════════════════════════════════════════════════
#  STORE PROFILES  — HTML signals per retailer
#  Add a new profile when you add a store for the first time.
# ══════════════════════════════════════════════════════════════════════════════
STORE_PROFILES = {

    "costco": {
        "referer": "https://www.costco.com/",
        # Use Costco's real-time inventory API instead of HTML scraping.
        # {item_id} is replaced with the item's item_id at runtime.
        "inventory_api": (
            "https://ecom-api.costco.com/ebusiness/inventory/v1"
            "/inventorylevels/availability/v2"
            "?orderItemId={item_id}&action=EDD"
        ),
        "inventory_api_headers": {
            "client_identifier": "481b1aec-aa3b-454b-b81b-48187e28f205",
            "costco-env":        "ECOM",
            "costco-service":    "restInventory",
            "Origin":            "https://www.costco.com",
        },
        # Fallback HTML signals — NOTE: isbuyable is catalog data, not live inventory.
        # These fire for ALL variants regardless of stock. Only used if API fails.
        # Set item_id_window=0 to disable HTML fallback for Costco (prefer unknown over wrong).
        "in_stock_signals":     [],
        "out_of_stock_signals": [],
        "item_id_window": 0,
    },

    "lululemon": {
        "referer": "https://www.lululemon.com/",
        "in_stock_signals": [
            'add to bag',
            '"availability":"instock"',
            '"instockstatus":true',
            '"isavailable":true',
        ],
        "out_of_stock_signals": [
            'notify me when available',
            'out of stock',
            'sold out',
            '"availability":"outofstock"',
            '"instockstatus":false',
        ],
    },

    # Generic fallback — works for many sites
    "generic": {
        "referer": "",
        "in_stock_signals": [
            '"availability":"instock"',
            'add to cart',
            'add to bag',
            '"instock":true',
            '"available":true',
        ],
        "out_of_stock_signals": [
            'out of stock',
            'sold out',
            'currently unavailable',
            '"availability":"outofstock"',
            '"instock":false',
            'notify me when available',
        ],
    },
}


# ══════════════════════════════════════════════════════════════════════════════
#  CORE UTILITIES
# ══════════════════════════════════════════════════════════════════════════════

def log(msg: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {msg}"
    print(line)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")


def send_notification(title: str, message: str, subtitle: str = ""):
    """Send a native macOS notification via osascript."""
    # Escape double quotes inside strings
    message  = message.replace('"', '\\"')
    subtitle = subtitle.replace('"', '\\"')
    title    = title.replace('"', '\\"')
    subtitle_part = f'subtitle "{subtitle}"' if subtitle else ""
    script = f'display notification "{message}" with title "{title}" {subtitle_part}'
    try:
        subprocess.run(["osascript", "-e", script], check=True)
    except subprocess.CalledProcessError as e:
        log(f"  ⚠ Notification failed: {e}")


def fetch_page(url: str, referer: str = "") -> str:
    """Fetch a URL with browser-like headers."""
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/123.0.0.0 Safari/537.36"
        ),
        "Accept":          "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip",          # only advertise what we can decompress
        "Connection":      "keep-alive",
    }
    if referer:
        headers["Referer"] = referer

    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=25) as resp:
        raw = resp.read()
        if resp.info().get("Content-Encoding") == "gzip":
            raw = gzip_module.decompress(raw)
        return raw.decode("utf-8", errors="replace")


def dump_page_html(url: str, out_path: str = "/tmp/costco_page.html"):
    """One-off helper: fetch and save raw HTML for inspection."""
    html = fetch_page(url, referer="https://www.costco.com/")
    with open(out_path, "w") as f:
        f.write(html)
    print(f"Saved {len(html)} chars to {out_path}")


def _parse_availability(data) -> bool | None:
    """
    Recursively search a Costco inventory API response for an availability signal.
    Returns True (in stock), False (out of stock), or None (can't determine).
    Handles string values ("true"/"false"), bool values, and status strings.
    """
    if isinstance(data, dict):
        # Direct boolean/string fields
        for key in ("available", "inStock", "isAvailable", "availableToOrder",
                    "isOrderable", "buyable", "isBuyable"):
            val = data.get(key)
            if val is True  or val == "true"  or val == "True":  return True
            if val is False or val == "false" or val == "False": return False
        # Status string fields
        for key in ("inventoryStatus", "onlineInventoryStatus", "availabilityStatus"):
            val = str(data.get(key, "")).lower()
            if val in ("available", "instock", "in_stock"):        return True
            if val in ("outofstock", "out_of_stock", "unavailable"): return False
        # availableQty > 0 means in stock
        qty = data.get("availableQty") or data.get("quantity") or data.get("qty")
        if qty is not None:
            try:
                return int(float(str(qty))) > 0
            except (ValueError, TypeError):
                pass
        # Recurse into nested dicts/lists
        for v in data.values():
            result = _parse_availability(v)
            if result is not None:
                return result
    elif isinstance(data, list):
        for item in data:
            result = _parse_availability(item)
            if result is not None:
                return result
    return None


def fetch_inventory_api(item: dict, profile: dict) -> dict | None:
    """
    Call a profile's inventory_api endpoint. Returns parsed JSON or None on error.
    The {item_id} placeholder in the URL is replaced with item["item_id"].
    """
    item_id = item.get("item_id", "")
    if not item_id:
        return None
    url = profile["inventory_api"].replace("{item_id}", item_id)
    base_headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
        ),
        "Accept": "application/json",
        "Referer": profile.get("referer", ""),
    }
    base_headers.update(profile.get("inventory_api_headers", {}))
    try:
        req = urllib.request.Request(url, headers=base_headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
            log(f"  [debug] inventory API response: {json.dumps(data)[:600]}")
            return data
    except Exception as e:
        log(f"  [debug] inventory API error: {e}")
        return None


def check_item_with_selenium(item: dict) -> dict:
    """
    Use headless Chrome to fully render the page, select variant attributes,
    then read the Add-to-Cart / Out-of-Stock button to determine availability.
    Requires: pip install selenium
    """
    try:
        import time

        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.support.ui import WebDriverWait
    except ImportError:
        log("  [error] selenium not installed — run: pip install selenium")
        return {"status": "error", "variant_found": False, "message": "selenium not installed"}

    opts = webdriver.ChromeOptions()
    opts.add_argument("--headless")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument(
        "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    )

    driver = webdriver.Chrome(options=opts)
    try:
        driver.get(item["url"])
        wait = WebDriverWait(driver, 15)

        # ── Select each variant attribute ─────────────────────────────────────
        variant_found = True
        for label in item.get("variant_selectors", []):
            xpath = (
                f'//*[normalize-space(text())="{label}" or '
                f'normalize-space(@aria-label)="{label}" or '
                f'normalize-space(@value)="{label}"]'
            )
            try:
                el = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
                driver.execute_script("arguments[0].scrollIntoView(true);", el)
                el.click()
                time.sleep(0.8)   # let the page update after each selection
                log(f"  [debug] clicked variant: '{label}'")
            except Exception as e:
                log(f"  [debug] could not select variant '{label}': {e}")
                variant_found = False

        # ── Read the Add-to-Cart button ───────────────────────────────────────
        try:
            btn = wait.until(EC.presence_of_element_located((By.ID, "add-to-cart-btn")))
            btn_html = btn.get_attribute("outerHTML").lower()
            btn_val  = btn.get_attribute("value") or ""
            log(f"  [debug] button value='{btn_val}'  html snippet: {repr(btn_html[:200])}")

            if "out of stock" in btn_html or "out of stock" in btn_val.lower():
                return {"status": "out_of_stock", "variant_found": variant_found, "message": "selenium"}
            if "add to cart" in btn_html or "add to cart" in btn_val.lower():
                return {"status": "in_stock",     "variant_found": variant_found, "message": "selenium"}

            # Button present but neither text matched — log full value for debugging
            log(f"  [debug] unrecognized button state; full html: {repr(btn_html[:400])}")
            return {"status": "unknown", "variant_found": variant_found, "message": "selenium: unrecognized button"}

        except Exception as e:
            log(f"  [debug] add-to-cart button not found: {e}")
            return {"status": "error", "variant_found": False, "message": f"button not found: {e}"}

    finally:
        driver.quit()


def check_item(item: dict) -> dict:
    """
    Check a single item. Returns a result dict:
      status: "in_stock" | "out_of_stock" | "unknown" | "error"
      variant_found: bool
      message: human-readable detail
    """
    # ── Selenium path — fully renders JS, clicks variant selectors ───────────
    if item.get("use_selenium"):
        return check_item_with_selenium(item)

    profile_key = item.get("store_profile", "generic")
    profile     = STORE_PROFILES.get(profile_key, STORE_PROFILES["generic"])

    # ── Inventory API path (e.g. Costco) ─────────────────────────────────────
    if "inventory_api" in profile and item.get("item_id"):
        data = fetch_inventory_api(item, profile)
        if data is not None:
            available = _parse_availability(data)
            if available is True:
                return {"status": "in_stock",     "variant_found": True, "message": "inventory API"}
            if available is False:
                return {"status": "out_of_stock", "variant_found": True, "message": "inventory API"}
            log(f"  [debug] inventory API: unrecognized response shape — falling back to HTML")

    # ── HTML scraping fallback ────────────────────────────────────────────────
    try:
        html = fetch_page(item["url"], referer=profile["referer"])
    except Exception as e:
        return {"status": "error", "variant_found": False, "message": str(e)}

    lower = html.lower()

    # Variant check
    variant_keywords = [kw.lower() for kw in item.get("variant_keywords", [])]
    if variant_keywords:
        variant_found = all(kw in lower for kw in variant_keywords)
    else:
        variant_found = True   # no keywords required → treat as found

    # Stock signals — prefer item_id-scoped window when available
    item_id = item.get("item_id", "").lower()
    window_size = profile.get("item_id_window", 0)
    if item_id and window_size:
        pos = lower.find(item_id)
        if pos >= 0:
            window = lower[max(0, pos - window_size // 2): pos + window_size]
            is_in  = any(sig in window for sig in profile["in_stock_signals"])
            is_out = any(sig in window for sig in profile["out_of_stock_signals"])
            log(f"  [debug] item_id '{item_id}' found at pos {pos}; window in={is_in} out={is_out}")
        else:
            log(f"  [debug] item_id '{item_id}' NOT found on page — falling back to full-page signals")
            is_in  = any(sig in lower for sig in profile["in_stock_signals"])
            is_out = any(sig in lower for sig in profile["out_of_stock_signals"])
    else:
        is_in  = any(sig in lower for sig in profile["in_stock_signals"])
        is_out = any(sig in lower for sig in profile["out_of_stock_signals"])

    if is_in and not is_out:
        status = "in_stock"
    elif is_out and not is_in:
        status = "out_of_stock"
    else:
        # Both or neither signal found — page likely shows multiple variants
        # with mixed availability. Can't determine status without per-variant parsing.
        status = "unknown"

    return {"status": status, "variant_found": variant_found, "message": ""}


def notify_result(item: dict, result: dict):
    """Send the right macOS notification based on the check result."""
    name  = item["name"]
    store = item["store"]
    url   = item["url"]

    status        = result["status"]
    variant_found = result["variant_found"]

    if status == "error":
        log(f"  ✗ Error fetching page: {result['message']}")
        send_notification(
            f"⚠️ Stock Checker Error — {store}",
            f"Could not reach page for: {name}",
            "Will retry next run"
        )

    elif status == "in_stock" and variant_found:
        log(f"  ✓ IN STOCK")
        send_notification(
            f"✅ IN STOCK — {store}",
            f"{name} is AVAILABLE! Tap to order.",
            store
        )
        if item.get("open_on_stock"):
            subprocess.run(["open", url])

    elif status == "out_of_stock" and variant_found:
        log(f"  ✗ Out of stock")
        send_notification(
            f"❌ Out of Stock — {store}",
            f"{name}: not available today.",
            "Will check again next run"
        )

    elif not variant_found:
        log(f"  ? Variant keywords not found on page")
        send_notification(
            f"⚠️ {store} — Check Manually",
            f"Could not confirm variant for: {name}",
            "Page content may have changed"
        )

    else:  # unknown
        log(f"  ? Stock status ambiguous — check manually")
        send_notification(
            f"⚠️ {store} — Status Unclear",
            f"Could not determine stock for: {name}",
            url
        )


# ══════════════════════════════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="Universal Stock Checker")
    parser.add_argument("--list", action="store_true",  help="List all tracked items and exit")
    parser.add_argument("--item", type=int, default=None, help="Check only item at this index")
    args = parser.parse_args()

    # ── --list mode ──────────────────────────────────────────────────────────
    if args.list:
        print("\nTracked items:")
        for i, item in enumerate(WATCHLIST):
            status = "✓ active" if item.get("active") else "✗ paused"
            print(f"  [{i}] {status}  {item['store']} — {item['name']}")
            if item.get("variant_keywords"):
                print(f"       keywords: {item['variant_keywords']}")
        print()
        return

    # ── Select items to check ────────────────────────────────────────────────
    if args.item is not None:
        items_to_check = [(args.item, WATCHLIST[args.item])]
    else:
        items_to_check = [(i, item) for i, item in enumerate(WATCHLIST) if item.get("active")]

    log(f"═══ Stock Checker — checking {len(items_to_check)} item(s) ═══")

    for idx, item in items_to_check:
        meta = ""
        if item.get("model"):
            meta += f" | Model: {item['model']}"
        if item.get("item_id"):
            meta += f" | SKU: {item['item_id']}"
        log(f"[{idx}] {item['store']} — {item['name']}{meta}")
        result = check_item(item)
        notify_result(item, result)

    log("═══ Done ═══\n")


if __name__ == "__main__":
    main()
