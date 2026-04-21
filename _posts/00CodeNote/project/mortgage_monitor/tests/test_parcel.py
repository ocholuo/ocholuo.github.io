"""
Tests for /api/parcel endpoint and parcel cache helpers.

Integration address used throughout:
  3234 78th Pl NE, Medina, WA 98039
  Coordinates: lat=47.6248, lon=-122.2258  (King County)
  Parcel PIN:  7397300140  (King County Parcel Viewer)
  eRealProperty: https://blue.kingcounty.com/Assessor/eRealProperty/Dashboard.aspx?ParcelNbr=7397300140
"""

import json

import pytest

import app as app_module
from app import _load_parcel_cache, _save_parcel_cache, _is_parcel_complete, _pick


# ---------------------------------------------------------------------------
# _is_parcel_complete
# ---------------------------------------------------------------------------

class TestIsParcelComplete:
    def test_not_in_king_county_is_complete(self):
        assert _is_parcel_complete({"in_king_county": False}) is True

    def test_empty_fields_is_incomplete(self):
        entry = {"in_king_county": True, "pin": "1234567890",
                 "address": "", "jurisdiction": "", "zoning": "", "year_built": None}
        assert _is_parcel_complete(entry) is False

    def test_address_present_is_complete(self):
        entry = {"in_king_county": True, "address": "123 MAIN ST"}
        assert _is_parcel_complete(entry) is True

    def test_jurisdiction_present_is_complete(self):
        entry = {"in_king_county": True, "address": "", "jurisdiction": "MEDINA"}
        assert _is_parcel_complete(entry) is True

    def test_year_built_present_is_complete(self):
        entry = {"in_king_county": True, "address": "", "jurisdiction": "", "zoning": "",
                 "year_built": "1960"}
        assert _is_parcel_complete(entry) is True


# ---------------------------------------------------------------------------
# _pick
# ---------------------------------------------------------------------------

class TestPick:
    def test_returns_first_matching_key(self):
        assert _pick({"ADDR_FULL": "123 MAIN"}, "ADDR_FULL", "SITE_ADDR") == "123 MAIN"

    def test_skips_empty_string(self):
        assert _pick({"ADDR_FULL": "", "SITE_ADDR": "456 ELM"}, "ADDR_FULL", "SITE_ADDR") == "456 ELM"

    def test_skips_none(self):
        assert _pick({"A": None, "B": "val"}, "A", "B") == "val"

    def test_returns_none_when_all_missing(self):
        assert _pick({"X": ""}, "A", "B") is None


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
    "pin": "7397300140",
    "address": "3234 78TH PL NE",
    "jurisdiction": "MEDINA",
    "zoning": "R-16",
    "lot_sqft": 17120,
    "appr_land": "1800000",
    "appr_improvement": "600000",
    "appr_total": "2400000",
    "erp_url": "https://blue.kingcounty.com/Assessor/eRealProperty/Dashboard.aspx?ParcelNbr=7397300140",
    "geometry": None,
    "year_built": "1960",
    "bedrooms": "4",
    "bathrooms": "3",
    "living_sqft": "3200",
    "stories": "2",
}


class TestParcelCacheHit:
    def test_cache_hit_returns_cached_data_without_network(self, client, tmp_cache, monkeypatch):
        monkeypatch.setitem(app_module._parcel_cache, "47.6248,-122.2258", MEDINA_CACHED)
        monkeypatch.setattr(app_module.threading, "Thread", lambda *a, **kw: type("T", (), {"start": lambda self: None})())

        import requests as req_mod
        monkeypatch.setattr(req_mod, "get", lambda *a, **kw: (_ for _ in ()).throw(AssertionError("network called")))

        r = client.get("/api/parcel?lat=47.6248&lon=-122.2258")
        assert r.status_code == 200
        data = r.get_json()
        assert data["pin"] == "7397300140"
        assert data["in_king_county"] is True

    def test_cache_key_uses_4_decimal_places(self, client, tmp_cache, monkeypatch):
        # lat=47.62481 rounds to 47.6248 — should still hit the cache
        monkeypatch.setitem(app_module._parcel_cache, "47.6248,-122.2258", MEDINA_CACHED)
        monkeypatch.setattr(app_module.threading, "Thread", lambda *a, **kw: type("T", (), {"start": lambda self: None})())

        import requests as req_mod
        monkeypatch.setattr(req_mod, "get", lambda *a, **kw: (_ for _ in ()).throw(AssertionError("network called")))

        r = client.get("/api/parcel?lat=47.62481&lon=-122.22584")
        assert r.status_code == 200
        assert r.get_json()["pin"] == "7397300140"

    def test_incomplete_cache_entry_triggers_refetch(self, client, tmp_cache, monkeypatch):
        """An entry with all fields empty is treated as a cache miss and re-fetched."""
        incomplete = {"in_king_county": True, "pin": "7397300140",
                      "address": "", "jurisdiction": "", "zoning": ""}
        monkeypatch.setitem(app_module._parcel_cache, "47.6248,-122.2258", incomplete)

        import requests as req_mod
        monkeypatch.setattr(req_mod, "get",
                            lambda *a, **kw: FakeResponse(_make_arcgis_response("7397300140")))
        monkeypatch.setattr(app_module, "_scrape_erp_details",
                            lambda pin: _make_erp_details())

        data = client.get("/api/parcel?lat=47.6248&lon=-122.2258").get_json()
        assert data["address"] == "3234 78TH PL NE"


# ---------------------------------------------------------------------------
# /api/parcel — live ArcGIS mock (Medina, King County success path)
# ---------------------------------------------------------------------------

def _make_arcgis_response(pin):
    """Build a minimal ArcGIS query response — only fields that MapServer/0 actually returns."""
    return {
        "features": [
            {
                "attributes": {"PIN": pin},
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


def _make_erp_details(
    addr="3234 78TH PL NE",
    juris="MEDINA",
    zoning="R-16",
    lot_sqft=17120,
    year_built="1960",
    bedrooms="4",
    bathrooms="3",
    living_sqft="2800",
    appr_land="1800000",
    appr_impr="600000",
    appr_total="2400000",
) -> dict:
    """Return the dict that _scrape_erp_details would produce for a Medina property."""
    return {
        "address": addr,
        "jurisdiction": juris,
        "zoning": zoning,
        "lot_sqft": lot_sqft,
        "year_built": year_built,
        "bedrooms": bedrooms,
        "bathrooms": bathrooms,
        "living_sqft": living_sqft,
        "appr_land": appr_land,
        "appr_improvement": appr_impr,
        "appr_total": appr_total,
    }



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
    ArcGIS response (PIN + geometry) and _scrape_erp_details are both mocked.
    """

    def _mock_requests_get(self, arcgis_pin="7397300140"):
        call_count = {"n": 0}

        def fake_get(url, **kwargs):
            call_count["n"] += 1
            if "gismaps.kingcounty.gov" in url:
                return FakeResponse(_make_arcgis_response(pin=arcgis_pin))
            raise AssertionError(f"Unexpected URL: {url}")

        return fake_get, call_count

    def _patch(self, monkeypatch, arcgis_pin="7397300140"):
        fake_get, call_count = self._mock_requests_get(arcgis_pin)
        import requests as req_mod
        monkeypatch.setattr(req_mod, "get", fake_get)
        monkeypatch.setattr(app_module, "_scrape_erp_details",
                            lambda pin: _make_erp_details())
        return call_count

    def test_returns_200_with_king_county_true(self, client, tmp_cache, monkeypatch):
        self._patch(monkeypatch)
        r = client.get("/api/parcel?lat=47.6248&lon=-122.2258")
        assert r.status_code == 200
        assert r.get_json()["in_king_county"] is True

    def test_pin_matches_expected(self, client, tmp_cache, monkeypatch):
        self._patch(monkeypatch)
        data = client.get("/api/parcel?lat=47.6248&lon=-122.2258").get_json()
        assert data["pin"] == "7397300140"

    def test_address_fields_present(self, client, tmp_cache, monkeypatch):
        self._patch(monkeypatch)
        data = client.get("/api/parcel?lat=47.6248&lon=-122.2258").get_json()
        assert data["address"] == "3234 78TH PL NE"
        assert data["jurisdiction"] == "MEDINA"
        assert data["zoning"] == "R-16"

    def test_financial_fields(self, client, tmp_cache, monkeypatch):
        self._patch(monkeypatch)
        data = client.get("/api/parcel?lat=47.6248&lon=-122.2258").get_json()
        assert data["lot_sqft"] == 17120
        assert data["appr_total"] == "2400000"
        assert data["erp_url"].endswith("ParcelNbr=7397300140")

    def test_building_fields_from_erp(self, client, tmp_cache, monkeypatch):
        self._patch(monkeypatch)
        data = client.get("/api/parcel?lat=47.6248&lon=-122.2258").get_json()
        assert data["year_built"] == "1960"
        assert data["bedrooms"] == "4"
        assert data["living_sqft"] == "2800"

    def test_geojson_geometry_present(self, client, tmp_cache, monkeypatch):
        self._patch(monkeypatch)
        data = client.get("/api/parcel?lat=47.6248&lon=-122.2258").get_json()
        assert data["geometry"]["type"] == "Polygon"
        assert len(data["geometry"]["coordinates"]) > 0

    def test_result_is_written_to_cache(self, client, tmp_cache, monkeypatch):
        self._patch(monkeypatch)
        client.get("/api/parcel?lat=47.6248&lon=-122.2258")
        assert "47.6248,-122.2258" in app_module._parcel_cache

    def test_second_request_uses_cache(self, client, tmp_cache, monkeypatch):
        call_count = self._patch(monkeypatch)
        monkeypatch.setattr(app_module.threading, "Thread",
                            lambda *a, **kw: type("T", (), {"start": lambda self: None})())

        client.get("/api/parcel?lat=47.6248&lon=-122.2258")
        client.get("/api/parcel?lat=47.6248&lon=-122.2258")
        assert call_count["n"] == 1  # ArcGIS only on first request; cache hit on second


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
        assert "error" in r.get_json()

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


# ---------------------------------------------------------------------------
# /api/parcel — PIN-based lookup
#
# Address: 3234 78th Pl NE, Medina, WA 98039
# Parcel:  7397300140  (King County Parcel Viewer)
# eRealProperty URL:
#   https://blue.kingcounty.com/Assessor/eRealProperty/Dashboard.aspx?ParcelNbr=7397300140
# ---------------------------------------------------------------------------

MEDINA_PIN = "7397300140"
MEDINA_ERP_URL = (
    "https://blue.kingcounty.com/Assessor/eRealProperty/Dashboard.aspx"
    "?ParcelNbr=7397300140"
)


def _medina_arcgis_by_pin():
    """ArcGIS WHERE-clause response for PIN=7397300140 — only PIN + geometry."""
    return {
        "features": [
            {
                "attributes": {"PIN": MEDINA_PIN},
                "geometry": {
                    "rings": [
                        [
                            [-122.2262, 47.6245],
                            [-122.2255, 47.6245],
                            [-122.2255, 47.6252],
                            [-122.2262, 47.6252],
                            [-122.2262, 47.6245],
                        ]
                    ]
                },
            }
        ]
    }


class TestParcelPinLookup:
    """
    Tests for ?pin= query param — WHERE-clause ArcGIS lookup for
    3234 78th Pl NE, Medina, WA 98039 (PIN 7397300140).
    """

    def _patch(self, monkeypatch):
        import requests as req_mod
        monkeypatch.setattr(req_mod, "get",
                            lambda *a, **kw: FakeResponse(_medina_arcgis_by_pin()))
        monkeypatch.setattr(app_module, "_scrape_erp_details",
                            lambda pin: _make_erp_details(living_sqft="3200"))

    def test_pin_lookup_returns_200(self, client, tmp_cache, monkeypatch):
        self._patch(monkeypatch)
        r = client.get(f"/api/parcel?pin={MEDINA_PIN}")
        assert r.status_code == 200

    def test_pin_lookup_in_king_county_true(self, client, tmp_cache, monkeypatch):
        self._patch(monkeypatch)
        data = client.get(f"/api/parcel?pin={MEDINA_PIN}").get_json()
        assert data["in_king_county"] is True

    def test_pin_lookup_pin_field_matches(self, client, tmp_cache, monkeypatch):
        self._patch(monkeypatch)
        data = client.get(f"/api/parcel?pin={MEDINA_PIN}").get_json()
        assert data["pin"] == MEDINA_PIN

    def test_pin_lookup_erp_url_correct(self, client, tmp_cache, monkeypatch):
        self._patch(monkeypatch)
        data = client.get(f"/api/parcel?pin={MEDINA_PIN}").get_json()
        assert data["erp_url"] == MEDINA_ERP_URL

    def test_pin_lookup_address_and_zoning(self, client, tmp_cache, monkeypatch):
        self._patch(monkeypatch)
        data = client.get(f"/api/parcel?pin={MEDINA_PIN}").get_json()
        assert data["address"] == "3234 78TH PL NE"
        assert data["jurisdiction"] == "MEDINA"
        assert data["zoning"] == "R-16"
        assert data["lot_sqft"] == 17120

    def test_pin_lookup_building_fields_from_erp(self, client, tmp_cache, monkeypatch):
        self._patch(monkeypatch)
        data = client.get(f"/api/parcel?pin={MEDINA_PIN}").get_json()
        assert data["year_built"] == "1960"
        assert data["bedrooms"] == "4"
        assert data["living_sqft"] == "3200"

    def test_pin_lookup_assessed_values_from_erp(self, client, tmp_cache, monkeypatch):
        self._patch(monkeypatch)
        data = client.get(f"/api/parcel?pin={MEDINA_PIN}").get_json()
        assert data["appr_land"] == "1800000"
        assert data["appr_total"] == "2400000"

    def test_pin_lookup_geojson_geometry(self, client, tmp_cache, monkeypatch):
        self._patch(monkeypatch)
        data = client.get(f"/api/parcel?pin={MEDINA_PIN}").get_json()
        assert data["geometry"]["type"] == "Polygon"

    def test_pin_lookup_cached_under_pin_key(self, client, tmp_cache, monkeypatch):
        self._patch(monkeypatch)
        client.get(f"/api/parcel?pin={MEDINA_PIN}")
        assert MEDINA_PIN in app_module._parcel_cache

    def test_missing_both_lat_lon_and_pin_returns_400(self, client, tmp_cache):
        r = client.get("/api/parcel")
        assert r.status_code == 400


# ---------------------------------------------------------------------------
# eRealProperty URL format check (no network — just verifies URL construction)
# ---------------------------------------------------------------------------

class TestErpUrl:
    def test_erp_url_format_for_known_pin(self, client, tmp_cache, monkeypatch):
        """Verify the eRealProperty dashboard URL is constructed correctly."""
        import requests as req_mod

        monkeypatch.setattr(req_mod, "get",
                            lambda *a, **kw: FakeResponse(
                                {"features": [{"attributes": {"PIN": "5255400140"}, "geometry": {}}]}
                            ))
        monkeypatch.setattr(app_module, "_scrape_erp_details", lambda pin: {})

        data = client.get("/api/parcel?lat=47.7769&lon=-122.2069").get_json()
        expected = (
            "https://blue.kingcounty.com/Assessor/eRealProperty/Dashboard.aspx"
            "?ParcelNbr=5255400140"
        )
        assert data["erp_url"] == expected
