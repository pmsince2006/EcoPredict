"""Unit tests for safe backend ModelService and inference logic."""

import sys
from pathlib import Path
import json
import pytest

backend_path = Path(__file__).resolve().parent.parent.parent / "backend"
if str(backend_path) not in sys.path:
    sys.path.insert(0, str(backend_path))

from app.services.model_service import (
    ModelService,
    MetadataValidationError,
)
from app.services.aqi_service import AQIService


def test_model_service_singleton():
    """Verify singleton pattern returns consistent instance."""
    s1 = ModelService.get_instance()
    s2 = ModelService.get_instance()
    assert s1 is s2


def test_model_service_loaded_attributes():
    """Verify that current model is explicitly identified as a demo model."""
    service = ModelService.get_instance()
    assert service.is_loaded is True
    # Crucial: Model was trained on synthetic fixture, so it MUST be flagged demo
    assert service.is_demo_model is True
    assert service.training_provenance == "synthetic_fixture"
    assert service.real_data_validated is False


def test_forecast_generation_structure():
    """Verify multi-horizon forecast structure and schema compliance."""
    service = ModelService.get_instance()
    fc = service.get_forecast(location="Delhi NCR", horizon_hours=12, allow_demo=True)

    assert fc.target_variable == "pm25"
    assert fc.target_unit == "µg/m³"
    assert fc.forecast_horizon_hours == 12
    assert fc.location_name == "Delhi NCR"
    assert fc.data_status == "demo_preview"
    assert fc.is_demo_model is True
    assert fc.real_data_validated is False
    assert len(fc.forecast_points) == 12
    assert "DEMO" in fc.disclaimer

    # Inspect first forecast point
    p1 = fc.forecast_points[0]
    assert p1.predicted_pm25 > 0
    assert p1.predicted_aqi > 0
    assert p1.lower_bound_pm25 <= p1.predicted_pm25
    assert p1.predicted_pm25 <= p1.upper_bound_pm25
    assert p1.category in ["Good", "Moderate", "Poor", "Very Poor", "Severe", "Hazardous"]


def test_real_data_only_mode_returns_unavailable():
    """Verify that when allow_demo=False, demo model returns data_status='unavailable'."""
    service = ModelService.get_instance()
    fc = service.get_forecast(location="Delhi NCR", horizon_hours=24, allow_demo=False)

    # Since current model is demo, real data forecast must be unavailable
    assert fc.data_status == "unavailable"
    assert len(fc.forecast_points) == 0
    assert "unavailable" in fc.disclaimer.lower()


def test_invalid_horizon_rejected():
    """Verify horizon out-of-range boundaries raise ValueError."""
    service = ModelService.get_instance()
    with pytest.raises(ValueError, match="Horizon hours must be between 1 and 72"):
        service.get_forecast(horizon_hours=0)

    with pytest.raises(ValueError, match="Horizon hours must be between 1 and 72"):
        service.get_forecast(horizon_hours=100)


def test_cpcb_aqi_sub_index_calculation():
    """Verify piecewise linear CPCB AQI calculation from PM2.5 concentrations."""
    # Breakpoint tests:
    # 0 - 30 -> 0 - 50
    assert AQIService.calculate_aqi_from_pm25(15.0) == 25
    assert AQIService.calculate_aqi_from_pm25(30.0) == 50
    # 31 - 60 -> 51 - 100
    assert AQIService.calculate_aqi_from_pm25(60.0) == 100
    # 61 - 90 -> 101 - 200
    assert AQIService.calculate_aqi_from_pm25(90.0) == 200
    # 91 - 120 -> 201 - 300
    assert AQIService.calculate_aqi_from_pm25(120.0) == 300
    # 121 - 250 -> 301 - 400
    assert AQIService.calculate_aqi_from_pm25(250.0) == 400
    # > 250 -> Severe/Hazardous
    assert AQIService.calculate_aqi_from_pm25(380.0) == 500


def test_missing_model_directory_handling(tmp_path):
    """Verify graceful handling when model artifact directory is missing."""
    empty_service = ModelService.__new__(ModelService)
    empty_service.artifacts_dir = tmp_path / "non_existent_dir"
    empty_service.model_filename = "missing.pkl"
    empty_service.metadata_filename = "missing.json"
    empty_service.model = None
    empty_service.is_loaded = False
    empty_service.is_demo_model = True
    empty_service.training_provenance = "unknown"
    empty_service.real_data_validated = False

    loaded = empty_service.load_model()
    assert loaded is False
    assert empty_service.is_loaded is False

    fc = empty_service.get_forecast(horizon_hours=6)
    assert fc.data_status == "unavailable"
    assert len(fc.forecast_points) == 0


def test_invalid_metadata_handling(tmp_path):
    """Verify MetadataValidationError when metadata JSON lacks required keys."""
    bad_meta_dir = tmp_path / "bad_meta"
    bad_meta_dir.mkdir()
    meta_file = bad_meta_dir / "model_metadata.json"
    meta_file.write_text(json.dumps({"invalid_key": "no_features"}), encoding="utf-8")

    test_service = ModelService.__new__(ModelService)
    test_service.artifacts_dir = bad_meta_dir
    test_service.model_filename = "dummy.pkl"
    test_service.metadata_filename = "model_metadata.json"
    test_service.is_loaded = False

    with pytest.raises(MetadataValidationError, match="missing required keys"):
        test_service.load_model()
