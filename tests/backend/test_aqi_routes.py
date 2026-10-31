"""Integration and route tests for EcoPredict backend API endpoints.

Validates:
- GET /api/health with data provenance reporting
- GET /api/aqi/summary with demo data flags
- GET /api/aqi/stations with schema adherence
- GET /api/aqi/forecast with horizon validation, demo disclaimers, and allow_demo toggles
- Fallback handling when demo mode is disallowed or artifacts are missing
"""

import sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

backend_path = Path(__file__).resolve().parent.parent.parent / "backend"
if str(backend_path) not in sys.path:
    sys.path.insert(0, str(backend_path))

from app.main import app
from app.services.model_service import ModelService


@pytest.fixture
def client():
    """Create a FastAPI TestClient."""
    return TestClient(app)


def test_health_endpoint(client):
    """GET /api/health should return 200 and explicit provenance details."""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "healthy"
    assert "version" in data
    assert data["model_loaded"] is True
    # Crucial honest reporting: current model is trained on synthetic fixture
    assert data["data_status"] == "demo_preview"
    assert data["model_provenance"] == "synthetic_fixture"
    assert data["real_data_validated"] is False
    assert "disclaimer" in data
    assert "DEMO" in data["disclaimer"]


def test_aqi_summary_endpoint(client):
    """GET /api/aqi/summary should return 200 with honest demo annotations."""
    response = client.get("/api/aqi/summary?location=Delhi%20NCR")
    assert response.status_code == 200
    data = response.json()

    assert data["location_name"] == "Delhi NCR"
    assert "aqi" in data
    assert "category" in data
    assert "primary_pollutant" in data
    assert data["is_demo_data"] is True
    assert data["data_status"] == "demo_preview"
    assert "pollutants" in data
    assert "pm25" in data["pollutants"]


def test_aqi_stations_endpoint(client):
    """GET /api/aqi/stations should return 200 and valid station list."""
    response = client.get("/api/aqi/stations")
    assert response.status_code == 200
    data = response.json()

    assert "stations" in data
    assert "count" in data
    assert data["count"] > 0
    assert len(data["stations"]) == data["count"]
    assert data["is_demo_data"] is True

    # Validate first station schema
    station = data["stations"][0]
    assert "id" in station
    assert "name" in station
    assert "lat" in station
    assert "lng" in station
    assert "aqi" in station
    assert "category" in station


def test_forecast_demo_mode(client):
    """GET /api/aqi/forecast with allow_demo=true should return synthetic preview."""
    response = client.get("/api/aqi/forecast?location=Delhi%20NCR&horizon=24&allow_demo=true")
    assert response.status_code == 200
    data = response.json()

    assert data["location_name"] == "Delhi NCR"
    assert data["forecast_horizon_hours"] == 24
    assert data["is_demo_model"] is True
    assert data["real_data_validated"] is False
    assert data["data_status"] == "demo_preview"
    assert len(data["forecast_points"]) == 24
    assert "DEMO" in data["disclaimer"]

    # Verify forecast point properties
    point = data["forecast_points"][0]
    assert "time" in point
    assert "predicted_pm25" in point
    assert "predicted_aqi" in point
    assert "lower_bound_pm25" in point
    assert "upper_bound_pm25" in point
    assert "category" in point


def test_forecast_real_data_only_mode(client):
    """GET /api/aqi/forecast with allow_demo=false must return data_status='unavailable'."""
    response = client.get("/api/aqi/forecast?location=Delhi%20NCR&horizon=24&allow_demo=false")
    assert response.status_code == 200
    data = response.json()

    assert data["data_status"] == "unavailable"
    assert data["is_demo_model"] is True
    assert len(data["forecast_points"]) == 0
    assert "unavailable" in data["disclaimer"].lower()


def test_forecast_horizon_validation(client):
    """GET /api/aqi/forecast with out-of-range horizon must return 422 Unprocessable Entity."""
    # Horizon too low (< 1)
    res_low = client.get("/api/aqi/forecast?horizon=0")
    assert res_low.status_code == 422

    # Horizon too high (> 72)
    res_high = client.get("/api/aqi/forecast?horizon=100")
    assert res_high.status_code == 422


def test_forecast_fallback_on_unloaded_model(client, monkeypatch):
    """Verify endpoint gracefully falls back when model service fails to load."""
    service = ModelService.get_instance()
    # Temporarily monkeypatch is_loaded to False
    monkeypatch.setattr(service, "is_loaded", False)

    response = client.get("/api/aqi/forecast?horizon=12&allow_demo=true")
    assert response.status_code == 200
    data = response.json()
    assert data["data_status"] == "unavailable"
    assert len(data["forecast_points"]) == 0
    assert "unavailable" in data["disclaimer"].lower()
