# Mortgage Monitor

- [Mortgage Monitor](#mortgage-monitor)
  - [Setup](#setup)
    - [1. Fix PATH (if `python` resolves to the wrong interpreter)](#1-fix-path-if-python-resolves-to-the-wrong-interpreter)
    - [2. Create and activate a virtualenv](#2-create-and-activate-a-virtualenv)
    - [3. Install dependencies](#3-install-dependencies)
  - [Run](#run)
  - [Deploy (Heroku)](#deploy-heroku)
  - [API Endpoints](#api-endpoints)
  - [Data](#data)
  - [Home Scout Feature](#home-scout-feature)
    - [Current Implementation Status](#current-implementation-status)
    - [External Listing Links — Options and Limitations](#external-listing-links--options-and-limitations)
    - [TODO — Home Scout](#todo--home-scout)
  - [Property Parcel Data — Options](#property-parcel-data--options)
    - [Option 1 — King County ArcGIS REST API (Free, King County only)](#option-1--king-county-arcgis-rest-api-free-king-county-only)
    - [Option 2 — WA State / Per-County GIS Portals (Free, all WA counties)](#option-2--wa-state--per-county-gis-portals-free-all-wa-counties)
    - [Option 3 — Regrid API (Free tier, national, standardized)](#option-3--regrid-api-free-tier-national-standardized)
    - [Option 4 — ATTOM Data (Paid, most comprehensive)](#option-4--attom-data-paid-most-comprehensive)
    - [Recommendation](#recommendation)

A single-page Flask web app that tracks and displays daily US mortgage rates (30-yr Fixed, 15-yr Fixed, 10-yr Treasury). Data is pulled from FRED with no API key required.

## Setup

### 1. Fix PATH (if `python` resolves to the wrong interpreter)

If you see `ModuleNotFoundError` despite having a pyenv virtualenv active in your prompt, your shell is picking up a different Python (e.g. uv's `~/.local/bin/python`) before pyenv shims. Fix it by adding this to your `~/.zshrc`:

```bash
export PATH="$(pyenv root)/shims:$PATH"
```

Then reload:

```bash
source ~/.zshrc
```

### 2. Create and activate a virtualenv

```bash
pyenv virtualenv 3.11.4 mortgage
pyenv shell 3.11.4/envs/mortgage
```

Or use an existing virtualenv:

```bash
pyenv shell 3.11.4/envs/ocho
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Run

```bash
python app.py
```

Or with Flask's dev server (auto-reload):

```bash
flask run
```

Then open `http://127.0.0.1:5000` in your browser.

## Deploy (Heroku)

```bash
heroku create
git push heroku main
```

The `Procfile` uses `gunicorn app:app`.

## API Endpoints

| Endpoint | Returns |
|---|---|
| `GET /` | Dashboard HTML |
| `GET /api/rates` | Current rates, history, forecast |
| `GET /api/news` | RSS-parsed mortgage news |
| `GET /api/history` | Rate history table data |
| `GET /api/scout?address=&lat=&lon=` | Resolved property links (Zillow, Redfin, Realtor.com) |

## Data

Rate history is cached locally in `data/rate_history.csv` (30/15-yr Fixed from FRED) and `data/tnx_history.csv` (10-yr Treasury). The app refreshes from FRED on startup if the cached data is stale.

---

## Home Scout Feature

### Current Implementation Status

| Capability | Status | Notes |
|---|---|---|
| US map with WA highlight | Done | D3 + us-atlas TopoJSON, free |
| Address autocomplete | Done | Nominatim (OSM), free, no key |
| Property map (zoom 18) | Done | Leaflet + CartoDB Positron tiles, free |
| Layer toggle (Clean / Standard) | Done | Built-in Leaflet control |
| Aerial satellite thumbnail | Done | ESRI World Imagery export, free, no key |
| Direct Redfin listing URL | Done | Via Redfin autocomplete API (semi-public) |
| Direct Zillow listing URL | Partial | URL constructed from address; accuracy varies |
| Direct Realtor.com listing URL | Partial | City-level search link only |

### External Listing Links — Options and Limitations

| Approach | Property Photo | Direct Listing Link | Cost | Reliability |
|---|---|---|---|---|
| Current (aerial + constructed URL) | ESRI satellite view | Approximate | Free | Good |
| Zillow Bridge API | Yes (listing photos) | Exact | Requires partnership | High |
| Redfin unofficial API | No | Exact (via autocomplete) | Free | Medium — may break |
| Realtor.com API | Yes | Exact | Requires approval | High |
| Google Custom Search API | og:image from result | Exact (first result) | 100 req/day free | High |
| Page scraping (server-side) | og:image | Exact | Free | Low (Cloudflare blocks) |

### TODO — Home Scout

- [ ] Improve Zillow direct link accuracy (currently address-slug construction, not verified against zpid)
- [ ] Improve Realtor.com to property-level link (currently city search)
- [ ] Add parcel / assessor data panel (see section below)
- [ ] Show lot boundary overlay on Leaflet map (requires Regrid or county GIS parcel API)

---

## Property Parcel Data — Options

When a user enters a WA address, the following sources can return structured assessor data
(zoning, year built, lot size, assessed value, owner, parcel number, etc.).

### Option 1 — King County ArcGIS REST API (Free, King County only)

King County publishes all parcel and assessor data through a public ArcGIS server.
No API key required. Covers all of King County (Seattle, Bellevue, Bothell, Redmond, etc.).

**Step 1 — Geocode address to get coordinates (already done via Nominatim)**

**Step 2 — Query parcel at lat/lon:**
```
GET https://gismaps.kingcounty.gov/arcgis/rest/services/Property/KingCo_Parcels/MapServer/0/query
  ?geometry={lon},{lat}
  &geometryType=esriGeometryPoint
  &spatialRel=esriSpatialRelIntersects
  &outFields=PIN,ADDR_FULL,PROP_NAME,JURIS,CURRENT_ZONING
  &f=json
```

**Step 3 — Fetch assessor detail by PIN:**
```
GET https://blue.kingcounty.com/Assessor/eRealProperty/Dashboard.aspx?ParcelNbr={PIN}
```
(Web page only — no JSON API for assessment detail)

**Step 4 — King County Open Data (Socrata REST API, machine-readable):**
```
GET https://data.kingcounty.gov/resource/4znr-bewt.json
  ?$where=parcel_number='{PIN}'
```
Returns: year built, bedrooms, bathrooms, lot sqft, building sqft, assessed land value, assessed improvement value, tax year.

**Pros:** Free, official, accurate, machine-readable via Socrata.
**Cons:** King County only. Other WA counties need their own GIS endpoints.

---

### Option 2 — WA State / Per-County GIS Portals (Free, all WA counties)

Every WA county has a GIS portal, but each has a different URL and schema.

| County | GIS Portal | Parcel API |
|---|---|---|
| King | gismaps.kingcounty.gov | ArcGIS REST (above) |
| Snohomish | snohomishcountywa.gov/gis | ArcGIS REST |
| Pierce | gis.co.pierce.wa.us | ArcGIS REST |
| Spokane | spokanecounty.org/gis | ArcGIS REST |

**Pros:** Free, official data.
**Cons:** Must implement per-county routing logic. Schemas differ per county.

---

### Option 3 — Regrid API (Free tier, national, standardized)

Regrid (regrid.com) aggregates parcel data from all US counties into a single normalized API.

```
GET https://app.regrid.com/api/v2/parcels/point?lat={lat}&lon={lon}&token={token}
```

Returns: parcel number, owner, address, zoning, year built, lot size, building sqft, assessed value — all in one JSON response, same schema for every county.

**Free tier:** 1,000 API calls/month, parcel geometry included.
**Paid tier:** from $99/month for higher volume.

**Pros:** One API call, national coverage, normalized schema, includes lot boundary GeoJSON (can draw on Leaflet map).
**Cons:** Requires account + free token. 1K/month limit on free tier.

---

### Option 4 — ATTOM Data (Paid, most comprehensive)

ATTOM is the commercial-grade property data standard used by Zillow, Redfin, and banks.

```
GET https://api.attomdata.com/propertyapi/v1.0.0/property/detail?address1={street}&address2={city_state_zip}
Authorization: apikey {key}
```

Returns: everything — assessor data, deed history, mortgage history, foreclosure status, school district, flood zone, permits, comparable sales.

**Cost:** starts ~$299/month.
**Pros:** Most complete data available. Same data Zillow uses.
**Cons:** Expensive. Overkill for personal use.

---

### Recommendation

For personal/WA-focused use: **start with King County ArcGIS + Socrata** (free, no key, returns the exact data you described — zoning, year built, assessed value). Add a county-routing layer later if you want broader WA coverage. Use **Regrid free tier** if you want lot boundary drawing on the map without county-specific code.
