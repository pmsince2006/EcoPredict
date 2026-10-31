"""Smoke tests for backend services and configuration."""

import sys
from pathlib import Path

# Add backend directory to path
backend_path = Path(__file__).parent.parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from app.core.config import settings
from app.services.aqi_service import AQIService


def test_settings_initialization():
    """Verify that settings are configured with default properties."""
    assert settings.PROJECT_NAME == "EcoPredict API"
    assert settings.API_V1_PREFIX == "/api"
    assert "http://localhost:5173" in settings.CORS_ORIGINS


def test_aqi_service_severity_categories():
    """Test standard AQI category threshold mapping."""
    assert AQIService.get_severity_category(40)["category"] == "Good"
    assert AQIService.get_severity_category(85)["category"] == "Moderate"
    assert AQIService.get_severity_category(150)["category"] == "Poor"
    assert AQIService.get_severity_category(280)["category"] == "Very Poor"
    assert AQIService.get_severity_category(350)["category"] == "Severe"
    assert AQIService.get_severity_category(450)["category"] == "Hazardous"


def test_aqi_demo_summary():
    """Ensure demo summary payload returns required fields and is marked as demo."""
    summary = AQIService.get_demo_summary("Delhi NCR")
    assert summary["is_demo_data"] is True
    assert summary["aqi"] == 234
    assert "pm25" in summary["pollutants"]
