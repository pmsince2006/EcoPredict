"""Unit tests for FeatureEngineer module and leakage prevention."""

import sys
from pathlib import Path
import pandas as pd
import numpy as np
import pytest

ml_path = Path(__file__).parent.parent.parent / "ml"
sys.path.insert(0, str(ml_path))

from src.features.engineer import FeatureEngineer


@pytest.fixture
def synthetic_time_series():
    """Generates 50 hours of synthetic continuous hourly PM2.5 readings."""
    dates = pd.date_range("2024-01-01 00:00:00", periods=50, freq="h")
    values = [100.0 + 10.0 * np.sin(i * np.pi / 12) for i in range(50)]
    return pd.DataFrame({
        "timestamp": dates,
        "station_id": "ST01",
        "pm25": values,
    })


def test_feature_engineer_dimensions(synthetic_time_series):
    """Test that feature extraction produces expected columns and rows."""
    engineer = FeatureEngineer(
        target_col="pm25",
        horizon=1,
        lag_hours=[1, 2, 3],
        rolling_windows=[3],
    )
    X, y = engineer.create_features(synthetic_time_series, drop_na=True)
    
    assert len(X) == len(y)
    assert len(X) < len(synthetic_time_series)  # Boundary drops
    assert "pm25_current" in X.columns
    assert "pm25_lag_1h" in X.columns
    assert "pm25_rolling_mean_3h" in X.columns
    assert "hour_sin" in X.columns
    assert "hour_cos" in X.columns


def test_target_horizon_alignment(synthetic_time_series):
    """Verify future target alignment y_t = x_{t + horizon}."""
    horizon = 2
    engineer = FeatureEngineer(
        target_col="pm25",
        horizon=horizon,
        lag_hours=[1],
        rolling_windows=[2],
    )
    X, y = engineer.create_features(synthetic_time_series, drop_na=False)
    
    # For any row t, target value should match raw pm25 at row t + horizon
    raw_pm25 = synthetic_time_series["pm25"]
    for t in range(len(X) - horizon):
        expected_future_val = raw_pm25.iloc[t + horizon]
        actual_target_val = y.iloc[t]
        assert np.isclose(expected_future_val, actual_target_val), f"Mismatch at row {t}"


def test_absence_of_future_data_leakage(synthetic_time_series):
    """CRITICAL TEST: Verify modifying future observations does not alter past/current features.

    If features at row t change when row t+1 or t+2 are modified, data leakage exists.
    """
    engineer = FeatureEngineer(
        target_col="pm25",
        horizon=1,
        lag_hours=[1, 2, 3],
        rolling_windows=[3, 6],
    )
    
    # Compute baseline features
    X_original, _ = engineer.create_features(synthetic_time_series, drop_na=False)
    
    # Create corrupted series where future values (after index 25) are modified
    corrupted_series = synthetic_time_series.copy()
    corrupted_series.loc[26:, "pm25"] = 9999.0  # Massive future spike
    
    X_corrupted, _ = engineer.create_features(corrupted_series, drop_na=False)
    
    # All features at row 25 and prior must be 100% IDENTICAL
    pd.testing.assert_frame_equal(
        X_original.iloc[:26],
        X_corrupted.iloc[:26],
        check_dtype=True,
        obj="Features prior to future modification must be strictly identical",
    )


def test_invalid_horizon_raises():
    """Verify that horizon < 1 raises ValueError."""
    with pytest.raises(ValueError, match="Forecast horizon must be >= 1"):
        FeatureEngineer(horizon=0)
