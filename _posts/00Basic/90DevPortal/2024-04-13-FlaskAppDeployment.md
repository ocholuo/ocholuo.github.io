---
title: DevPortal - Deploy a Flask Demo App to the Web
date: 2024-04-13 11:11:11 -0400
categories: [90DevPortal]
tags: [Flask, Python, Deployment, Railway, Render, Gunicorn, DevOps]
toc: true
image:
---

# Deploy a Flask Demo App to the Web

- [Deploy a Flask Demo App to the Web](#deploy-a-flask-demo-app-to-the-web)
  - [Overview](#overview)
  - [Pre-deployment — required code changes](#pre-deployment--required-code-changes)
    - [1. Fix app.run()](#1-fix-apprun)
    - [2. Add gunicorn to requirements.txt](#2-add-gunicorn-to-requirementstxt)
    - [3. Create a Procfile](#3-create-a-procfile)
  - [Option 1 — Railway (recommended)](#option-1--railway-recommended)
    - [Steps](#steps)
    - [Environment variables (if needed)](#environment-variables-if-needed)
    - [Redeploy on push](#redeploy-on-push)
  - [Option 2 — Render](#option-2--render)
    - [Steps](#steps-1)
  - [Option 3 — VPS (DigitalOcean / Hetzner)](#option-3--vps-digitalocean--hetzner)
    - [Server setup](#server-setup)
    - [Nginx reverse proxy config](#nginx-reverse-proxy-config)
    - [Run as a systemd service (survives reboots)](#run-as-a-systemd-service-survives-reboots)
  - [Local dev vs. production comparison](#local-dev-vs-production-comparison)
  - [Debugger PIN and debug mode](#debugger-pin-and-debug-mode)
  - [Ephemeral filesystem — cache consideration](#ephemeral-filesystem--cache-consideration)
  - [Custom domain (optional)](#custom-domain-optional)

ref:
- https://flask.palletsprojects.com/en/3.0.x/deploying/
- https://gunicorn.org/
- https://railway.app/
- https://render.com/

---

## Overview

This guide covers deploying a Flask app (single `app.py` + `templates/`) to a public URL. The example is the **mortgage-monitor** demo but the steps apply to any small Flask project.

Project structure assumed:

```bash
mortgage_monitor/
├── app.py
├── requirements.txt
├── Procfile          # created in this guide
├── templates/
│   └── index.html
└── data/             # runtime cache (ephemeral on cloud)
```

Three deployment targets are covered, ordered by setup effort:

| Platform | Free tier | Cold start | Filesystem | Effort |
|---|---|---|---|---|
| Railway | 500 hrs/mo | None | Ephemeral | Low |
| Render | Yes (sleeps) | ~30 s after idle | Ephemeral | Low |
| VPS | No (~$5/mo) | None | Persistent | Medium |

---

## Pre-deployment — required code changes

Three changes are required before any deployment target will work correctly.

### 1. Fix app.run()

Flask's built-in dev server is not suitable for production. Cloud platforms inject the port via the `$PORT` environment variable and expect the app to bind to `0.0.0.0`.

Change the last block in `app.py` from:

```python
if __name__ == "__main__":
    app.run(debug=True, port=5050)
```

To:

```python
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5050))
    app.run(debug=False, host="0.0.0.0", port=port)
```

Key differences:
- `debug=False` — disables the Werkzeug debugger and Debugger PIN in production
- `host="0.0.0.0"` — binds to all network interfaces, not just localhost
- `PORT` from env — Railway, Render, and Heroku all set this automatically

### 2. Add gunicorn to requirements.txt

Gunicorn is a production-grade WSGI server. Flask's built-in server handles one request at a time and is not designed for concurrent traffic.

```text
flask
requests
pandas
numpy
feedparser
gunicorn
```

### 3. Create a Procfile

The `Procfile` tells the platform which command to run to start the web process. Place it in the same directory as `app.py`:

```bash
web: gunicorn app:app
```

- `app:app` — first `app` is the Python module (`app.py`), second is the Flask instance variable inside it
- For multiple workers: `web: gunicorn -w 2 app:app`

---

## Option 1 — Railway (recommended)

**Best for:** personal tools, demos, no-configuration deploys.

**Free tier:** 500 hours/month (enough for a low-traffic personal app), no credit card required.

### Steps

1. Push the project to a GitHub repository.

```bash
cd mortgage_monitor/
git init
git add .
git commit -m "initial commit"
gh repo create mortgage-monitor --public --push
```

2. Go to [railway.app](https://railway.app) and sign in with GitHub.

3. Click **New Project** → **Deploy from GitHub repo** → select the repository.

4. Railway auto-detects Python, installs `requirements.txt`, and reads the `Procfile`.

5. Click **Deploy**. Within ~2 minutes a public URL is assigned:
   `https://mortgage-monitor-production.up.railway.app`

### Environment variables (if needed)

Set them in Railway dashboard → **Variables** tab:

```bash
FLASK_ENV=production
```

### Redeploy on push

Every `git push` to the connected branch triggers an automatic redeploy.

---

## Option 2 — Render

**Best for:** always-on hobby projects (paid tier) or demos that tolerate a cold start.

**Free tier:** sleeps after 15 minutes of inactivity — the first request after idle takes ~30 seconds to wake the container.

### Steps

1. Push to GitHub (same as Railway).

2. Go to [render.com](https://render.com) → **New** → **Web Service**.

3. Connect the GitHub repo.

4. Set:
   - **Build command:** `pip install -r requirements.txt`
   - **Start command:** `gunicorn app:app`
   - **Root directory:** `mortgage_monitor` (if the repo root is a parent folder)

5. Click **Create Web Service**. URL format: `https://mortgage-monitor.onrender.com`

---

## Option 3 — VPS (DigitalOcean / Hetzner)

**Best for:** always-on, persistent filesystem (cache survives restarts), custom domain, full control.

**Cost:** ~$5–6/month (Hetzner CX22 or DigitalOcean Basic Droplet).

### Server setup

```bash
# On the VPS (Ubuntu 22.04)
sudo apt update && sudo apt install python3-pip nginx -y

git clone https://github.com/yourname/mortgage-monitor.git
cd mortgage-monitor/mortgage_monitor
pip3 install -r requirements.txt

# Run gunicorn as a background service
gunicorn -w 2 -b 127.0.0.1:8000 app:app &
```

### Nginx reverse proxy config

Create `/etc/nginx/sites-available/mortgage`:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/mortgage /etc/nginx/sites-enabled/
sudo systemctl reload nginx
```

### Run as a systemd service (survives reboots)

Create `/etc/systemd/system/mortgage.service`:

```ini
[Unit]
Description=Mortgage Monitor Flask App
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/mortgage-monitor/mortgage_monitor
ExecStart=/usr/local/bin/gunicorn -w 2 -b 127.0.0.1:8000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable mortgage
sudo systemctl start mortgage
```

---

## Local dev vs. production comparison

| Setting | Local dev | Production |
|---|---|---|
| `debug=True` | Yes — hot reload, traceback | **No** — never |
| Debugger PIN | Shown in terminal | Not present |
| Server | Flask built-in (single thread) | Gunicorn (multi-worker) |
| Port | 5050 (hardcoded) | `$PORT` from environment |
| `host` | `127.0.0.1` (localhost only) | `0.0.0.0` (all interfaces) |

---

## Debugger PIN and debug mode

When running `debug=True`, Werkzeug starts an interactive in-browser Python console. The **Debugger PIN** is a one-time code that protects it from unauthorized access.

- Anyone with the PIN can execute arbitrary Python code inside the server process
- It only exists because `debug=True` is active
- Set `debug=False` in production — the PIN disappears entirely

```python
# Safe production start
app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 5050)))
```

---

## Ephemeral filesystem — cache consideration

Railway and Render use **ephemeral containers** — any file written to disk (e.g. `data/rate_history.csv`) is lost when the container restarts or redeploys.

Impact on mortgage-monitor:
- The FRED CSV cache (`data/rate_history.csv`) is deleted on each deploy
- The app re-fetches from FRED API on the first request after restart
- For a personal tool this is acceptable — cold fetch takes a few seconds

If cache persistence is required:
- Store the CSV in an external object store (S3, Cloudflare R2)
- Or use a managed database (PostgreSQL on Railway/Render is free up to 1 GB)

---

## Custom domain (optional)

Both Railway and Render support custom domains on free/paid plans.

1. Buy a domain (Namecheap, Cloudflare Registrar, etc.)
2. In Railway/Render dashboard → **Settings** → **Custom Domain** → enter domain
3. Add a `CNAME` record at your DNS provider pointing to the platform's hostname
4. HTTPS is provisioned automatically via Let's Encrypt

```bash
# Verify DNS propagation
dig CNAME yourdomain.com
```
