# 📈 Mortgage Rate Tracker – Setup Guide

Tracks the **10-Year US Treasury Yield** daily, estimates your 30-yr mortgage rate, sends desktop notifications, and keeps a running trend chart.

---

## 1. Requirements

- Python 3.9+ (comes pre-installed on macOS/most Linux; download at python.org for Windows)
- Internet connection

All Python packages (`requests`, `matplotlib`, `numpy`) are **auto-installed** on first run.

---

## 2. (Optional) Free FRED API Key — more reliable data source

Yahoo Finance is used by default (no key needed). For a more stable data source:

1. Go to https://fred.stlouisfed.org/docs/api/api_key.html
2. Sign up for a free account and request an API key
3. Create a `config.json` file next to `rate_tracker.py`:

```json
{
  "fred_api_key": "your_key_here"
}
```

---

## 3. Run manually (test it works)

```bash
python rate_tracker.py
```

It will:
- Fetch today's 10-yr Treasury yield
- Append it to `rate_history.csv`
- Save/update `rate_trend.png`
- Send a desktop notification

---

## 4. Schedule to run every day automatically

### macOS – launchd (recommended)

1. Edit the plist below to match your paths, then save as
   `~/Library/LaunchAgents/com.user.ratetracker.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>            <string>com.user.ratetracker</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/Users/YOUR_USERNAME/rate_tracker/rate_tracker.py</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>    <integer>9</integer>
        <key>Minute</key>  <integer>0</integer>
    </dict>
    <key>StandardOutPath</key>  <string>/tmp/ratetracker.log</string>
    <key>StandardErrorPath</key><string>/tmp/ratetracker.err</string>
</dict>
</plist>
```

2. Load it:

```bash
# Load the job
launchctl load ~/Library/LaunchAgents/com.graceluo.rate_tracker.plist

# Confirm it's registered (should print a line with the label)
launchctl list | grep rate_tracker

# To test it fires right now without waiting for 9am:
launchctl start com.graceluo.rate_tracker

# Then watch the output
tail -f /tmp/rate_tracker.log
# And errors if any
tail -f /tmp/rate_tracker.err

# Disable (won't run tomorrow)
launchctl unload ~/Library/LaunchAgents/com.graceluo.rate_tracker.plist

# Re-enable
launchctl load ~/Library/LaunchAgents/com.graceluo.rate_tracker.plist

# Check last exit code (0 = success, anything else = error)
launchctl list | grep rate_tracker

# The output of launchctl list shows <PID> <last-exit-code> <label> — if the middle column is 0 after a run, it succeeded.
```

---

### Windows – Task Scheduler

1. Open **Task Scheduler** → "Create Basic Task"
2. Name: `Mortgage Rate Tracker`
3. Trigger: **Daily** at 9:00 AM
4. Action: **Start a program**
   - Program: `C:\Python312\python.exe`  (adjust to your Python path)
   - Arguments: `C:\Users\YOU\rate_tracker\rate_tracker.py`
5. Finish

---

### Linux – cron

```bash
crontab -e
```

Add this line (runs at 9 AM every weekday):

```bash
0 9 * * 1-5 /usr/bin/python3 /Users/graceluo/Documents/github-geren/ocholuo.github.io/_posts/00CodeNote/project/rate_tracker/rate_tracker.py >> /tmp/ratetracker.log 2>&1
```

---

## 5. Output files

| File | Description |
|------|-------------|
| `rate_history.csv` | All logged rates with dates |
| `rate_trend.png` | Updated chart image (open in any image viewer) |
| `config.json` | Optional FRED API key |

---

## 6. Customise

In `rate_tracker.py` you can tweak:

```python
MORTGAGE_SPREAD = 1.75   # Adjust the treasury→mortgage spread (pp)
ALERT_THRESHOLD = 0.10   # Minimum move (%) to trigger an alert notification
```

---

## 7. Viewing the chart

Simply open `rate_trend.png` with any image viewer.
It auto-updates every time the script runs, so you can set it as a pinned image in your file explorer.
