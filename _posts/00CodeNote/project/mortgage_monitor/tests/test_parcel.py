"""
Tests for /api/parcel endpoint and parcel cache helpers.

Integration address used throughout:
  3234 78th Pl NE, Medina, WA 98039
  Coordinates: lat=47.6248, lon=-122.2258  (King County)
  Expected PIN: 2525069058 (from King County Parcel Viewer)
"""

import json

import pytest

import app as app_module
from app import _load_parcel_cache, _save_parcel_cache


# ---------------------------------------------------------------------------
# Parcel cache helpers
# ---------------------------------------------------------------------------

class TestParcelCache:
    def test_load_returns_empty_dict_when_missing(self, tmp_path, monkeypatch):
        monkeypatch.setattr(app_module, "PARCEL_CACHE_PATH", str(tmp_path / "nope.json"))
        assert _load_parcel_cache() == {}

    def test_load_returns_empty_dict_on_corrupt_file(self, tmp_path, monkeypatch):
        p = tmp_path / "cache.json"
        p.write_text("not valid json")
        monkeypatch.setattr(app_module, "PARCEL_CACHE_PATH", str(p))
        assert _load_parcel_cache() == {}

    def test_save_and_load_roundtrip(self, tmp_path, monkeypatch):
        p = str(tmp_path / "cache.json")
        monkeypatch.setattr(app_module, "PARCEL_CACHE_PATH", p)
        data = {"47.6248,-122.2258": {"in_king_county": True, "pin": "2525069058"}}
        _save_parcel_cache(data)
        assert _load_parcel_cache() == data

    def test_save_creates_data_dir(self, tmp_path, monkeypatch):
        nested = tmp_path / "data" / "sub" / "cache.json"
        monkeypatch.setattr(app_module, "PARCEL_CACHE_PATH", str(nested))
        _save_parcel_cache({"k": "v"})
        assert nested.exists()


# ---------------------------------------------------------------------------
# /api/parcel — input validation
# ---------------------------------------------------------------------------

class TestParcelInputValidation:
    def test_missing_lat_returns_400(self, client):
        r = client.get("/api/parcel?lon=-122.2258")
        assert r.status_code == 400
        assert "error" in r.get_json()

    def test_missing_lon_returns_400(self, client):
        r = client.get("/api/parcel?lat=47.6248")
        assert r.status_code == 400
        assert "error" in r.get_json()

    def test_missing_both_returns_400(self, client):
        r = client.get("/api/parcel")
        assert r.status_code == 400


# ---------------------------------------------------------------------------
# /api/parcel — cache hit (no network call)
# ---------------------------------------------------------------------------

MEDINA_CACHED = {
    "in_king_county": True,
    "pin": "2525069058",
    "address": "3234 78TH PL NE",
    "jurisdiction": "MEDINA",
    "zoning": "R-16",
    "lot_sqft": 16000,
    "appr_land": 1200000,
    "appr_improvement": 800000,
    "appr_total": 2000000,
    "erp_url": "https://blue.kingcounty.com/Assessor/eRealProperty/Dashboard.aspx?ParcelNbr=2525069058",
    "geometry": None,
    "year_built": "1965",
    "bedrooms": "4",
    "bathrooms": "3",
    "living_sqft": "2800",
    "stories": "2",
}


class TestParcelCacheHit:
    def test_cache_hit_returns_cached_data_without_network(self, client, tmp_cache, monkeypatch):
        monkeypatch.setitem(app_module._parcel_cache, "47.6248,-122.2258", MEDINA_CACHED)

        # If requests.get were called it would raise — proving we never reach the network
        import requests as req_mod
        monkeypatch.setattr(req_mod, "get", lambda *a, **kw: (_ for _ in ()).throw(AssertionError("network called")))

        r = client.get("/api/parcel?lat=47.6248&lon=-122.2258")
        assert r.status_code == 200
        data = r.get_json()
        assert data["pin"] == "2525069058"
        assert data["in_king_county"] is True

    def test_cache_key_uses_4_decimal_places(self, client, tmp_cache, monkeypatch):
        # lat=47.62481 rounds to 47.6248 — should still hit the cache
        monkeypatch.setitem(app_module._parcel_cache, "47.6248,-122.2258", MEDINA_CACHED)
        import requests as req_mod
        monkeypatch.setattr(req_mod, "get", lambda *a, **kw: (_ for _ in ()).throw(AssertionError("network called")))

        r = client.get("/api/parcel?lat=47.62481&lon=-122.22584")
        assert r.status_code == 200
        assert r.get_json()["pin"] == "2525069058"


# ---------------------------------------------------------------------------
# /api/parcel — live ArcGIS mock (Medina, King County success path)
# ---------------------------------------------------------------------------

def _make_arcgis_response(pin, addr, juris, zoning, lot_sqft, appr_land, appr_impr, appr_total):
    """Build a minimal ArcGIS query response for a single parcel feature."""
    return {
        "features": [
            {
                "attributes": {
                    "PIN": pin,
                    "ADDR_FULL": addr,
                    "JURIS": juris,
                    "CURRENT_ZONING": zoning,
                    "SQ_FT_LOT": lot_sqft,
                    "APPR_LAND": appr_land,
                    "APPR_IMPR": appr_impr,
                    "APPR_TOTAL": appr_total,
                },
                "geometry": {
                    "rings": [
                        [
                            [-122.226, 47.624],
                            [-122.225, 47.624],
                            [-122.225, 47.625],
                            [-122.226, 47.625],
                            [-122.226, 47.624],
                        ]
                    ]
                },
            }
        ]
    }


def _make_socrata_response(yrbuilt, bedrooms, baths, sqft, stories):
    return [
        {
            "yrbuilt": yrbuilt,
            "nbrbedrooms": bedrooms,
            "nbrbaths": baths,
            "sqfttotliving": sqft,
            "stories": stories,
        }
    ]


class FakeResponse:
    def __init__(self, payload, status_code=200):
        self._payload = payload
        self.status_code = status_code
        self.ok = status_code < 400

    def json(self):
        return self._payload

    def raise_for_status(self):
        if self.status_code >= 400:
            raise Exception(f"HTTP {self.status_code}")


class TestParcelMedinaKingCounty:
    """
    Unit test for 3234 78th Pl NE, Medina, WA 98039 (lat=47.6248, lon=-122.2258).
    ArcGIS and Socrata responses are mocked — no real network calls.
    """

    def _mock_requests_get(self, arcgis_pin="2525069058", socrata_yrbuilt="1965"):
        call_count = {"n": 0}

        def fake_get(url, **kwargs):
            call_count["n"] += 1
            if "gismaps.kingcounty.gov" in url:
                return FakeResponse(
                    _make_arcgis_response(
                        pin=arcgis_pin,
                        addr="3234 78TH PL NE",
                        juris="MEDINA",
                        zoning="R-16",
                        lot_sqft=16000,
                        appr_land=1200000,
                        appr_impr=800000,
                        appr_total=2000000,
                    )
                )
            if "data.kingcounty.gov" in url:
                return FakeResponse(
                    _make_socrata_response(
                        yrbuilt=socrata_yrbuilt,
                        bedrooms="4",
                        baths="3",
                        sqft="2800",
                        stories="2",
                    )
                )
            raise AssertionError(f"Unexpected URL: {url}")

        return fake_get, call_count

    def test_returns_200_with_king_county_true(self, client, tmp_cache, monkeypatch):
        fake_get, _ = self._mock_requests_get()
        import requests as req_mod
        monkeypatch.setattr(req_mod, "get", fake_get)

        r = client.get("/api/parcel?lat=47.6248&lon=-122.2258")
        assert r.status_code == 200
        data = r.get_json()
        assert data["in_king_county"] is True

    def test_pin_matches_expected(self, client, tmp_cache, monkeypatch):
        fake_get, _ = self._mock_requests_get()
        import requests as req_mod
        monkeypatch.setattr(req_mod, "get", fake_get)

        data = client.get("/api/parcel?lat=47.6248&lon=-122.2258").get_json()
        assert data["pin"] == "2525069058"

    def test_address_fields_present(self, client, tmp_cache, monkeypatch):
        fake_get, _ = self._mock_requests_get()
        import requests as req_mod
        monkeypatch.setattr(req_mod, "get", fake_get)

        data = client.get("/api/parcel?lat=47.6248&lon=-122.2258").get_json()
        assert data["address"] == "3234 78TH PL NE"
        assert data["jurisdiction"] == "MEDINA"
        assert data["zoning"] == "R-16"

    def test_financial_fields(self, client, tmp_cache, monkeypatch):
        fake_get, _ = self._mock_requests_get()
        import requests as req_mod
        monkeypatch.setattr(req_mod, "get", fake_get)

        data = client.get("/api/parcel?lat=47.6248&lon=-122.2258").get_json()
        assert data["lot_sqft"] == 16000
        assert data["appr_total"] == 2000000
        assert data["erp_url"].endswith("ParcelNbr=2525069058")

    def test_building_fields_from_socrata(self, client, tmp_cache, monkeypatch):
        fake_get, _ = self._mock_requests_get()
        import requests as req_mod
        monkeypatch.setattr(req_mod, "get", fake_get)

        data = client.get("/api/parcel?lat=47.6248&lon=-122.2258").get_json()
        assert data["year_built"] == "1965"
        assert data["bedrooms"] == "4"
        assert data["living_sqft"] == "2800"

    def test_geojson_geometry_present(self, client, tmp_cache, monkeypatch):
        fake_get, _ = self._mock_requests_get()
        import requests as req_mod
        monkeypatch.setattr(req_mod, "get", fake_get)

        data = client.get("/api/parcel?lat=47.6248&lon=-122.2258").get_json()
        assert data["geometry"]["type"] == "Polygon"
        assert len(data["geometry"]["coordinates"]) > 0

    def test_result_is_written_to_cache(self, client, tmp_cache, monkeypatch):
        fake_get, _ = self._mock_requests_get()
        import requests as req_mod
        monkeypatch.setattr(req_mod, "get", fake_get)

        client.get("/api/parcel?lat=47.6248&lon=-122.2258")
        assert "47.6248,-122.2258" in app_module._parcel_cache

    def test_second_request_uses_cache(self, client, tmp_cache, monkeypatch):
        fake_get, call_count = self._mock_requests_get()
        import requests as req_mod
        monkeypatch.setattr(req_mod, "get", fake_get)

        client.get("/api/parcel?lat=47.6248&lon=-122.2258")
        client.get("/api/parcel?lat=47.6248&lon=-122.2258")
        # ArcGIS should only have been called once
        assert call_count["n"] == 2  # 1 ArcGIS + 1 Socrata on first request; 0 on second


# ---------------------------------------------------------------------------
# /api/parcel — not in King County
# ---------------------------------------------------------------------------

class TestParcelOutsideKingCounty:
    def test_returns_in_king_county_false(self, client, tmp_cache, monkeypatch):
        import requests as req_mod
        monkeypatch.setattr(req_mod, "get", lambda *a, **kw: FakeResponse({"features": []}))

        r = client.get("/api/parcel?lat=45.5231&lon=-122.6765")  # Portland, OR
        assert r.status_code == 200
        assert r.get_json()["in_king_county"] is False

    def test_not_found_is_cached(self, client, tmp_cache, monkeypatch):
        import requests as req_mod
        monkeypatch.setattr(req_mod, "get", lambda *a, **kw: FakeResponse({"features": []}))

        client.get("/api/parcel?lat=45.5231&lon=-122.6765")
        assert "45.5231,-122.6765" in app_module._parcel_cache


# ---------------------------------------------------------------------------
# /api/parcel — ArcGIS error paths
# ---------------------------------------------------------------------------

class TestParcelArcGISErrors:
    def test_arcgis_error_json_returns_502(self, client, tmp_cache, monkeypatch):
        import requests as req_mod
        monkeypatch.setattr(
            req_mod, "get",
            lambda *a, **kw: FakeResponse({"error": {"code": 400, "message": "Failed to execute query.", "details": []}}),
        )
        r = client.get("/api/parcel?lat=47.6248&lon=-122.2258")
        assert r.status_code == 502
        assert r.get_json()["error"] == "ArcGIS error"

    def test_network_timeout_returns_502(self, client, tmp_cache, monkeypatch):
        import requests as req_mod
        import requests.exceptions

        def raise_timeout(*a, **kw):
            raise requests.exceptions.ReadTimeout("timed out")

        monkeypatch.setattr(req_mod, "get", raise_timeout)

        r = client.get("/api/parcel?lat=47.6248&lon=-122.2258")
        assert r.status_code == 502
        assert "error" in r.get_json()

    def test_network_error_does_not_cache(self, client, tmp_cache, monkeypatch):
        import requests as req_mod
        import requests.exceptions
        monkeypatch.setattr(req_mod, "get", lambda *a, **kw: (_ for _ in ()).throw(requests.exceptions.ConnectionError()))

        client.get("/api/parcel?lat=47.6248&lon=-122.2258")
        assert "47.6248,-122.2258" not in app_module._parcel_cache
