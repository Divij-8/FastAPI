from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"


def test_get_diagnostic_code_found():
    resp = client.get("/diagnostic-codes/P0300")
    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == "P0300"
    assert "troubleshooting_steps" in data


def test_get_diagnostic_code_not_found():
    resp = client.get("/diagnostic-codes/UNKNOWN")
    assert resp.status_code == 404


def test_get_vehicle_info_found():
    resp = client.get("/vehicle-info/Toyota/Camry/2018")
    assert resp.status_code == 200
    data = resp.json()
    assert data["make"] == "Toyota"
    assert data["year"] == 2018


def test_get_vehicle_info_not_found():
    resp = client.get("/vehicle-info/Honda/Civic/1999")
    assert resp.status_code == 404
