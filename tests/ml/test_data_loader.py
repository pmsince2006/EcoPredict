"""Unit and integration tests for DataLoader module."""

import sys
from pathlib import Path
import tempfile
import pandas as pd
import pytest

# Ensure ml package is resolvable
ml_path = Path(__file__).parent.parent.parent / "ml"
sys.path.insert(0, str(ml_path))

from src.data.loader import DataLoader, DataValidationError


@pytest.fixture
def valid_csv_file(tmp_path):
    """Creates a temporary valid CSV fixture."""
    file_path = tmp_path / "valid_sensor_data.csv"
    content = (
        "timestamp,station_id,pm25,pm10\n"
        "2024-01-01 00:00:00,ST01,85.5,140.0\n"
        "2024-01-01 01:00:00,ST01,92.0,155.0\n"
        "2024-01-01 02:00:00,ST01,88.4,148.0\n"
    )
    file_path.write_text(content, encoding="utf-8")
    return file_path


def test_loader_initialization():
    """Verify default paths and custom directory support."""
    loader = DataLoader(raw_data_dir="custom/raw", processed_data_dir="custom/proc")
    assert loader.raw_data_dir == Path("custom/raw")
    assert loader.processed_data_dir == Path("custom/proc")


def test_load_valid_csv(valid_csv_file):
    """Test loading a clean CSV returns expected DataFrame and date types."""
    loader = DataLoader()
    df = loader.load_dataset(valid_csv_file)
    assert len(df) == 3
    assert "timestamp" in df.columns
    assert pd.api.types.is_datetime64_any_dtype(df["timestamp"])
    assert df["pm25"].iloc[0] == 85.5


def test_missing_file_raises_not_found():
    """Test that a non-existent file raises FileNotFoundError with clear message."""
    loader = DataLoader()
    with pytest.raises(FileNotFoundError, match="Dataset file not found"):
        loader.load_dataset("definitely_non_existent_file.csv")


def test_missing_required_columns(tmp_path):
    """Test that CSV missing required columns raises DataValidationError."""
    file_path = tmp_path / "incomplete.csv"
    file_path.write_text("timestamp,pm25\n2024-01-01 00:00:00,50.0\n", encoding="utf-8")
    
    loader = DataLoader()
    with pytest.raises(DataValidationError, match="Missing required column"):
        loader.load_dataset(file_path, required_columns=["timestamp", "station_id", "pm25"])


def test_invalid_timestamp_raises_error(tmp_path):
    """Test that unparseable timestamps raise DataValidationError."""
    file_path = tmp_path / "bad_timestamp.csv"
    file_path.write_text(
        "timestamp,station_id,pm25\nnot-a-valid-date,ST01,50.0\n", encoding="utf-8"
    )
    
    loader = DataLoader()
    with pytest.raises(DataValidationError, match="Invalid timestamp format"):
        loader.load_dataset(file_path)


def test_duplicate_records_deduplication(tmp_path):
    """Test that duplicate timestamps for the same station are deduplicated."""
    file_path = tmp_path / "duplicates.csv"
    file_path.write_text(
        "timestamp,station_id,pm25\n"
        "2024-01-01 00:00:00,ST01,80.0\n"
        "2024-01-01 00:00:00,ST01,85.0\n"  # Duplicate timestamp
        "2024-01-01 01:00:00,ST01,90.0\n",
        encoding="utf-8",
    )
    
    loader = DataLoader()
    df = loader.load_dataset(file_path, drop_duplicates=True)
    assert len(df) == 2
    # Verify latest record is kept
    assert df[df["timestamp"] == "2024-01-01 00:00:00"]["pm25"].iloc[0] == 85.0
    assert loader.validation_report["duplicates_removed"] == 1


def test_negative_readings_sanitized(tmp_path):
    """Test that negative sensor artifacts are sanitized to NaN without deleting rows."""
    file_path = tmp_path / "negatives.csv"
    file_path.write_text(
        "timestamp,station_id,pm25\n"
        "2024-01-01 00:00:00,ST01,80.0\n"
        "2024-01-01 01:00:00,ST01,-5.5\n"  # Sensor calibration artifact
        "2024-01-01 02:00:00,ST01,90.0\n",
        encoding="utf-8",
    )
    
    loader = DataLoader()
    df = loader.load_dataset(file_path, clip_negatives=True)
    assert len(df) == 3  # Row is preserved
    assert pd.isna(df.loc[df["timestamp"] == "2024-01-01 01:00:00", "pm25"].iloc[0])
    assert loader.validation_report["anomalies_sanitized"]["pm25"] == 1


def test_sample_delhi_fixture_load():
    """Integration test verifying the provided Delhi CPCB software test fixture."""
    loader = DataLoader()
    fixture_path = "sample_delhi_cpcb_fixture.csv"
    df = loader.load_dataset(fixture_path)
    assert len(df) >= 165
    assert "pm25" in df.columns
    assert "pm10" in df.columns
    assert loader.validation_report["duplicates_removed"] >= 1
    assert loader.validation_report["anomalies_sanitized"].get("pm25", 0) >= 1
