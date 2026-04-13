# CLAUDE.md — Mortgage Monitor Project

> **This file governs all code changes to this project.**
> Before modifying any file, read and align with every section below.
> Never overwrite behavior that contradicts a documented requirement — raise the conflict to the user instead.

---

## Project Overview

**Mortgage Monitor** is a single-page Flask web app that tracks and displays daily US mortgage rates.

| Item | Value |
|------|-------|
| Framework | Flask + Gunicorn |
| Frontend | Vanilla JS + Chart.js 4.4 |
| Entry point | `app.py` |
| Template | `templates/index.html` (single file — all CSS, HTML, JS) |
| Run locally | `flask run` or `gunicorn app:app` |
| Deploy | Heroku-compatible (`Procfile` + `requirements.txt`) |

---

## Code Change Rules

1. **Read before editing** — always read the relevant section of `index.html` before writing.
2. **One file** — all CSS, HTML, JS lives in `templates/index.html`. Do not split without asking.
3. **No `!` in heredocs** — Zsh escapes `!` as `\!` in heredoc content. Always use the Write tool or Python scripts to write file content that contains `!` (e.g., `!important`, `<!DOCTYPE`). Never use `cat << EOF` or `echo` for this file.
4. **No JS logic changes** — do not modify data-fetching, calculation, or chart logic unless explicitly requested. CSS and HTML structure changes are safe.
5. **Preserve all IDs and event handlers** — JS depends on specific element IDs (`rtnx-big`, `r30-big`, etc.) and onclick handlers. Never rename them.
6. **Explain every change** — include a `/* WHY: ... */` comment for non-obvious CSS additions.
7. **Commit after changes** — always run `git commit` inside `SecurityKB/` first, then update the submodule pointer in the vault root. Two separate commits always required.

---

## Design System

### Color Tokens (CSS variables)

```css
--bg: #f1f5f9          /* page background */
--surface: #ffffff     /* card / modal background */
--border: #e2e8f0      /* card borders */
--accent: #2563eb      /* primary blue */
--accent-light: #eff6ff
--accent-dark: #1d4ed8
--nav-bg: #0f172a      /* sidebar dark navy */
--blue: #3b82f6        /* 30yr Fixed line + card accent */
--purple: #a78bfa      /* 15yr Fixed line + card accent */
--teal: #0891b2        /* 10yr Treasury line + card accent */
--text: #0f172a
--text-muted: #64748b
--text-light: #94a3b8
--radius: 8px
--radius-sm: 4px
```

### Themes (4 total)

| ID | Display | Description |
|----|---------|-------------|
| `parchment` | 🌿 | Default — slate/blue palette |
| `midnight` | 🌙 | Dark glassmorphism with purple accent |
| `terminal` | ☁ | Dark monospace, gold accent |
| `frost` | ❄ | Light indigo, navy sidebar |

Theme is applied via `html[data-theme="..."]` attribute. Each theme has CSS overrides for sidebar, table headers, and key components.

### Typography

- Page H1 (Dashboard title): `font-size: 1.55rem; font-weight: 800; letter-spacing: -0.03em`
- Tab page title (inline mode): `font-size: 1.55rem; font-weight: 800; letter-spacing: -0.03em`
- Card title: `font-size: .95rem; font-weight: 700`
- Section card title: `font-size: .7rem; font-weight: 700; text-transform: uppercase; letter-spacing: .1em`

---

## Layout Architecture

### Desktop (≥ 768px)

```
┌─────────────────────────────────────────────────────┐
│  Sidebar (220px fixed)  │  .app-main (margin-left:220px)  │
│  .sidebar               │  .container (padding: 20px 24px)│
│  - Logo + brand mark    │  [Dashboard content]             │
│  - Nav items            │  OR                              │
│  - Theme/lang controls  │  [Inline section content]        │
└─────────────────────────────────────────────────────┘
```

- Sidebar: `width: 220px; position: fixed; background: var(--nav-bg)`
- `.app-main`: `margin-left: 220px; min-width: 0; overflow-x: hidden`
- `.container`: `padding: 20px 24px 64px` (no `max-width` — fills available width)

### Mobile (< 768px)

```
┌──────────────────────────────────────────────┐
│  .mobile-tab-bar (sticky top, horizontal)    │
│  [Dashboard | Calc | Refi | History | News…] │
├──────────────────────────────────────────────┤
│  .app-main (full width, no left margin)      │
│  [Dashboard content]                         │
│  OR [Inline section content]                 │
└──────────────────────────────────────────────┘
```

- Sidebar hidden on mobile (`display: none` at < 768px)
- Mobile tab bar: `position: sticky; top: 0; z-index: 90; overflow-x: auto`
- `.app-main`: `margin-left: 0`

---

## Navigation

### Sidebar (Desktop)

```
Dashboard          → sidebarGoHome()
Payment Calculator → sidebarOpen(this, 'calc')
Refi Savings       → sidebarOpen(this, 'refi')
Rate History       → sidebarOpen(this, 'history')
Market News        → sidebarOpen(this, 'news')
──────────────────
Share Rate Card    → shareCard(); sidebarSetActive(this)
Rate Alert         → openModal('alert'); sidebarSetActive(this)
```

### Mobile Tab Bar

```
Dashboard  → mobileGoHome()
Calculator → mobileTabOpen(this, 'calc')
Refi       → mobileTabOpen(this, 'refi')
History    → mobileTabOpen(this, 'history')
News       → mobileTabOpen(this, 'news')
Alert      → mobileTabOpen(this, 'alert')
Share      → shareCard()
```

### Inline Section Mode

When a sidebar/mobile-tab item is clicked (except Share/Alert), `body[data-section]="<id>"` is set and the corresponding `.modal-overlay#modal-<id>` gets `.open`. CSS media queries render it inline (not as a popup):

- **Desktop**: `body[data-section] .modal-overlay.open { position: static; margin-left: 220px; padding: 20px 24px 60px; }`
- **Mobile**: `body[data-section] .modal-overlay.open { position: static; margin-left: 0; padding: 16px 16px 60px; }`
- In both cases, `.modal` becomes transparent (`background/border/shadow: none`) and each `.section-card` inside renders as a standalone card.

---

## Dashboard Sections (in order)

### 1. Header

```html
<div class="header">
  <h1 data-i18n="app.title">Daily Mortgage Rate Tracker</h1>
  <div class="header-sub">...</div>
  <div class="badges">Updated | Updated Daily | MND Rate Index</div>
</div>
```

### 2. Rate Cards (`div.rate-cards` — 3-column grid)

Three equal-width cards, each with:

- Colored `border-top: 3px solid` accent (teal / blue / purple)
- Big rate number (e.g., `6.37%`)
- Meta row: 1-Wk Change, 1-Yr Change, Monthly Avg, 52-Wk Avg
- 52-Week Range bar with thumb indicator

| Card | Color | Rate |
|------|-------|------|
| `rate-card.teal` | teal | 10-YR Treasury |
| `rate-card.blue` | blue | 30-YR Fixed |
| `rate-card.purple` | purple | 15-YR Fixed |

Responsive breakpoints:

- `> 900px`: 3 columns
- `681–900px`: 2 columns
- `≤ 680px`: 1 column

### 3. Daily Rate Chart (`div.chart-card`)

- Full-width card (`.dash-row` is single-column `grid-template-columns: 1fr`)
- Chart.js 4.4 line chart with 3 datasets: 30yr Fixed (blue), 15yr Fixed (purple), 10yr Treasury (teal)
- Time-range tabs: 2W / 3M (default) / 1Y / 20Y
- Chart wrapper: `height: 260px; overflow: hidden` — prevents canvas overflow on resize
- Canvas: `max-width: 100%`

### 4. Rate Forecast & Analysis (`div.forecast-card`)

- Full-width card (stacks below chart in the same `.dash-row`)
- Contains: trend badge, analysis text, MA 7d/30d badges, 30-day + 60-day projection boxes, historical percentile bar
- `word-break: break-word` on analysis text to prevent card overflow

### 5. Navigation Grid (Mobile only, `div.nav-grid`)

- Hidden on desktop (`@media (min-width: 768px) { display: none }`)
- 3-column grid of nav-cards, each `openModal()`
- Replaced by the mobile tab bar as primary navigation — nav-grid is secondary/redundant but kept

### 6. Footer (`div.footer`)

- Data sources: Mortgage News Daily, Bankrate/Freddie Mac, FRED
- Disclaimer text

---

## Tab Pages (Modal / Inline Sections)

All tab pages use this HTML skeleton:
```html
<div class="modal-overlay" id="modal-<id>" onclick="closeModalOutside(...)">
  <div class="modal">
    <div class="modal-header">
      <div class="modal-title">Title</div>
      <button class="modal-close" onclick="closeModal('<id>')">✕</button>
    </div>
    <!-- optional: <div class="live-badge">...</div> -->

    <div class="section-card">
      <div class="section-card-title">Section Name</div>
      <!-- content -->
    </div>
    <!-- more section-cards -->
  </div>
</div>
```

**In popup mode** (mobile without inline mode active): `.modal` is a centered card (`max-width: 580px`). `.section-card` has no visual styling (just `margin-bottom: 14px`).

**In inline mode** (desktop or mobile with `body[data-section]`): `.modal` becomes transparent, each `.section-card` is a full Dashboard-style card.

### Payment Calculator (`modal-calc`)

| Section Card | Contents |
|---|---|
| Loan Details | Preset chips + form inputs (price, down, term, rate slider) |
| Payment Summary | Results grid (monthly payment, total interest, total cost) + principal/interest bar |
| Amortization Schedule | Scrollable table (`max-height: 360px`) with sticky header |

### Refi Savings (`modal-refi`)

| Section Card | Contents |
|---|---|
| Potential Savings | Hero savings display (`hero-savings`) |
| Loan Details | Form inputs (balance, term, current rate, new rate, closing costs) |
| Rate Comparison | Comparison boxes (current vs new loan) + summary table |

### Rate History (`modal-history`)

| Section Card | Contents |
|---|---|
| Last 20 Trading Days | Scrollable rate history table (`#history-table-wrap`, `max-height: 400px`) |

Rate history table (`history-table`) requirements:

- Sticky header row: `position: sticky; top: 0; z-index: 2`
- Header background: `#dde3ec` with `box-shadow: 0 2px 4px rgba(0,0,0,0.08)` — must be visually distinct from data rows
- `today-row` highlighted with light blue background

### Market News (`modal-news`)

| Section Card | Contents |
|---|---|
| Rate Impact Signal | Signal bars + signal analysis text |
| Headlines | Filter chips (All / Mortgage / Fed Policy / Rate Up / Rate Down / Neutral) + news list |

### Rate Alert (`modal-alert`)

- Simple popup only (no inline section mode needed)
- Email input + rate threshold slider + submit button
- Prototype note: alerts are not actually sent

---

## Proportional Bar (Stacked Bar) — Color Requirements

Any part-to-whole bar that splits a value into a "good/neutral" segment vs. a "cost/warning" segment **must** use contrasting colors with clear semantic meaning. Same-family colors (e.g., two blues) are **not acceptable** — they fail to communicate the difference to the user.

### Principal vs. Interest bar (`.pi-bar`)

| Segment | Semantic meaning | Color rule | Default token |
|---------|-----------------|------------|---------------|
| **Principal** (`.pi-principal`) | Equity you own — calm, positive | Cool/soothing color | `var(--blue)` `#3b82f6` |
| **Interest** (`.pi-interest`) | Cost paid to lender — more = worse | Warm/attention-grabbing | `var(--gold)` `#f59e0b` |

**Rationale**: Blue is perceived as stable and trustworthy (your equity). Amber/gold is a universal "attention / cost / caution" signal — it scales naturally: a small gold segment feels fine, a large one communicates "this is expensive." The two colors must be visually distinct at a glance across all themes.

### Per-theme color assignments

| Theme | Principal | Interest |
|-------|-----------|----------|
| `parchment` (default) | `var(--blue)` #3b82f6 | `var(--gold)` #f59e0b |
| `midnight` | `var(--blue)` #3b82f6 | `var(--gold)` #f59e0b |
| `terminal` | `var(--teal)` #0891b2 | `var(--gold)` #f59e0b |
| `frost` | `var(--blue)` #3b82f6 | `var(--gold)` #f59e0b |

**Rule**: `--gold: #f59e0b` is already defined in `:root`. Always use this token for the "cost/warning" segment. Never use `var(--accent)` or any blue-family color for the interest segment — that creates the "bad example" of two near-identical colors.

### Legend dots
The legend dots next to "Principal" and "Interest" labels must match their respective bar segment colors exactly.

---

## Tables — Requirements

All data tables (`amort-table`, `history-table`) must follow:

- Sticky first header row: `position: sticky; top: 0; z-index: 2`
- Header background: `#dde3ec` (≠ data row bg `#f1f5f9`) — must have clear visual separation
- Header bottom shadow: `box-shadow: 0 2px 4px rgba(0,0,0,0.08)`
- Scroll container must have explicit `max-height` and `overflow-y: auto` for sticky to work

---

## i18n (Internationalization)

Three languages supported: `en` (English), `zh` (Chinese), `es` (Spanish).

- Translation strings in `const T = { en: {...}, zh: {...}, es: {...} }`
- Applied via `data-i18n="key"` attributes on elements
- `applyLang(lang)` function updates all `[data-i18n]` elements
- Language buttons in sidebar and on mobile fallback

**Rule**: when adding new UI text, always add keys to all three language objects (`T.en`, `T.zh`, `T.es`). If translation is unknown, use the English value as a placeholder.

---

## Chart.js Integration

- Version: 4.4.0 (CDN)
- Chart element: `<canvas id="rateChart">` inside `.chart-wrap`
- Datasets: 30yr Fixed, 15yr Fixed, 10yr Treasury (loaded from `/api/rates`)
- `responsive: true`, `maintainAspectRatio: false`
- Container `.chart-wrap { overflow: hidden }` prevents canvas bleed on resize
- Time range tabs (2W/3M/1Y/20Y) filter the chart data client-side

---

## API Endpoints (Flask `app.py`)

| Endpoint | Method | Returns |
|---|---|---|
| `/` | GET | Rendered `index.html` |
| `/api/rates` | GET | Current rates, history, forecast JSON |
| `/api/news` | GET | RSS-parsed news items JSON |
| `/api/history` | GET | Rate history table data JSON |

---

## Known Constraints / Do Not Break

- `<!DOCTYPE html>` — must NOT be written through a Zsh heredoc (becomes `<\!DOCTYPE html>`). Always use Python Write tool.
- `!important` in CSS — must NOT be written through a Zsh heredoc (becomes `\!important`). Always use Python scripts or the Write/Edit tool.
- `window.innerWidth` check in JS was removed — `sidebarOpen()` now always uses inline mode (CSS handles the difference between desktop and mobile margins).
- The `.container` has NO `max-width` by design — do not add one. Use `padding` for side spacing.
- `.app-main` must keep `overflow-x: hidden; min-width: 0` to prevent chart overflow.

---

## Changelog

| Date | Change |
|------|--------|
| 2026-04-13 | Initial design: cool slate/blue palette, 3-column rate cards, left sidebar |
| 2026-04-13 | Fixed top navbar → restored left sidebar; inline section mode added |
| 2026-04-13 | All tabs restructured to section-card layout; responsive content width |
| 2026-04-13 | Sticky table headers with distinct bg + shadow |
| 2026-04-13 | DOCTYPE fix; chart overflow fix; mobile top tab bar + inline mode |
