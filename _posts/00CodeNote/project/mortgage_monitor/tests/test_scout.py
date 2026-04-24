"""
Tests for /api/scout — listing URL construction and Redfin fallback.
"""

import pytest

from app import app as flask_app


@pytest.fixture()
def client():
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as c:
        yield c


class TestScoutInputValidation:
    def test_missing_address_returns_400(self, client):
        r = client.get("/api/scout")
        assert r.status_code == 400
        assert "error" in r.get_json()

    def test_empty_address_returns_400(self, client):
        r = client.get("/api/scout?address=")
        assert r.status_code == 400


class TestScoutUrlConstruction:
    """Verify Zillow and Realtor.com URLs are built correctly from address parts."""

    MEDINA = "3234 78th Pl NE, Medina, WA 98039"

    def test_zillow_url_contains_street_slug(self, client, monkeypatch):
        import requests as req_mod
        # Redfin call will fail — that's fine, triggers the fallback
        monkeypatch.setattr(req_mod, "get", lambda *a, **kw: (_ for _ in ()).throw(Exception("offline")))

        data = client.get(f"/api/scout?address={self.MEDINA}").get_json()
        assert "3234-78th-Pl-NE" in data["zillow"]["url"]

    def test_zillow_url_contains_zipcode(self, client, monkeypatch):
        import requests as req_mod
        monkeypatch.setattr(req_mod, "get", lambda *a, **kw: (_ for _ in ()).throw(Exception("offline")))

        data = client.get(f"/api/scout?address={self.MEDINA}").get_json()
        assert "98039" in data["zillow"]["url"]

    def test_realtor_url_contains_city(self, client, monkeypatch):
        import requests as req_mod
        monkeypatch.setattr(req_mod, "get", lambda *a, **kw: (_ for _ in ()).throw(Exception("offline")))

        data = client.get(f"/api/scout?address={self.MEDINA}").get_json()
        assert "Medina" in data["realtor"]["url"]

    def test_realtor_url_contains_state(self, client, monkeypatch):
        import requests as req_mod
        monkeypatch.setattr(req_mod, "get", lambda *a, **kw: (_ for _ in ()).throw(Exception("offline")))

        data = client.get(f"/api/scout?address={self.MEDINA}").get_json()
        assert "WA" in data["realtor"]["url"]

    def test_response_has_all_three_sites(self, client, monkeypatch):
        import requests as req_mod
        monkeypatch.setattr(req_mod, "get", lambda *a, **kw: (_ for _ in ()).throw(Exception("offline")))

        data = client.get(f"/api/scout?address={self.MEDINA}").get_json()
        assert "zillow" in data
        assert "redfin" in data
        assert "realtor" in data


class TestScoutRedfinFallback:
    """When Redfin autocomplete fails, a fallback URL is returned (not an error)."""

    def test_redfin_fallback_url_is_set_on_network_error(self, client, monkeypatch):
        import requests as req_mod
        monkeypatch.setattr(req_mod, "get", lambda *a, **kw: (_ for _ in ()).throw(Exception("offline")))

        data = client.get("/api/scout?address=3234 78th Pl NE, Medina, WA 98039").get_json()
        assert data["redfin"]["url"].startswith("https://www.redfin.com/homes/")

    def test_redfin_direct_url_used_when_api_returns_home_path(self, client, monkeypatch):
        import requests as req_mod
        import json as _json

        class FakeRedfin:
            ok = True
            status_code = 200
            text = "{}&&" + _json.dumps({
                "payload": {
                    "sections": [
                        {
                            "rows": [
                                {"url": "/WA/Medina/3234-78th-Pl-NE-98039/home/12345678", "name": "3234 78th Pl NE"}
                            ]
                        }
                    ]
                }
            })

            def raise_for_status(self):
                pass

        monkeypatch.setattr(req_mod, "get", lambda *a, **kw: FakeRedfin())

        data = client.get("/api/scout?address=3234 78th Pl NE, Medina, WA 98039").get_json()
        assert "/home/" in data["redfin"]["url"]
        assert data["redfin"]["url"].startswith("https://www.redfin.com")
