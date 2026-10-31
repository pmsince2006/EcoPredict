"""Feature Engineering Module for EcoPredict.

Constructs strictly backward-looking time-series features for AQI/PM2.5 forecasting,
ensuring zero future-information leakage:
- Autoregressive lag features (t-1, t-2, t-3, t-6, t-12, t-24).
- Rate of change (velocity) delta features.
- Trailing backward rolling statistics (3h, 6h, 24h trailing mean).
- Cyclical trigonometric temporal encodings (hour of day, day of week).
- Multi-horizon forward targets (e.g. +1h, +6h ahead).
"""

from typing import List, Optional, Tuple
import logging
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)

DEFAULT_LAGS = [1, 2, 3, 6, 12, 24]
DEFAULT_WINDOWS = [3, 6, 24]


class FeatureEngineer:
    """Extracts and transforms tabular time-series features for air quality forecasting."""

    def __init__(
        self,
        target_col: str = "pm25",
        horizon: int = 1,
        lag_hours: Optional[List[int]] = None,
        rolling_windows: Optional[List[int]] = None,
        add_cyclical_time: bool = True,
    ) -> None:
        """Initializes FeatureEngineer with target and lag configuration.

        Args:
            target_col: Name of the continuous target column (default: 'pm25').
            horizon: Forward prediction horizon in hours (h >= 1).
            lag_hours: List of backward lag hours to construct (e.g. [1, 2, 3, 6]).
            rolling_windows: List of backward rolling window sizes in hours (e.g. [3, 6]).
            add_cyclical_time: Whether to encode hour and day as sine/cosine cyclical features.
        """
        if horizon < 1:
            raise ValueError(f"Forecast horizon must be >= 1 hour. Received: {horizon}")

        self.target_col = target_col
        self.horizon = horizon
        self.lag_hours = sorted(lag_hours or DEFAULT_LAGS)
        self.rolling_windows = sorted(rolling_windows or DEFAULT_WINDOWS)
        self.add_cyclical_time = add_cyclical_time
        self.feature_names_: List[str] = []

    def create_features(
        self,
        df: pd.DataFrame,
        drop_na: bool = True,
    ) -> Tuple[pd.DataFrame, pd.Series]:
        """Constructs model features (X) and future target (y) from input time series.

        Zero Data Leakage Guarantees:
        - All rolling windows are strictly backward-looking (never centered).
        - Rolling means at time t use only observations up to time t.
        - Future target y at row t represents the true observation at row t + horizon.

        Args:
            df: Input DataFrame containing 'timestamp' and target_col, sorted chronologically.
            drop_na: If True, drops rows containing NaN caused by initial lags or terminal target shift.

        Returns:
            Tuple of (X, y) where:
            - X: DataFrame of engineered predictor features.
            - y: Series containing future target values y_{t + horizon}.
        """
        if self.target_col not in df.columns:
            raise ValueError(f"Target column '{self.target_col}' not found in DataFrame.")

        # Ensure sorted chronologically
        data = df.copy()
        if "timestamp" in data.columns:
            data = data.sort_values(by="timestamp").reset_index(drop=True)

        features = pd.DataFrame(index=data.index)

        # 1. Base observation at forecast origin t
        features[f"{self.target_col}_current"] = data[self.target_col]

        # 2. Autoregressive past lag features: y_{t-1}, y_{t-2}, ...
        for lag in self.lag_hours:
            col_name = f"{self.target_col}_lag_{lag}h"
            features[col_name] = data[self.target_col].shift(lag)

        # 3. Short-term rate of change (velocity: current - previous hour)
        features[f"{self.target_col}_diff_1h"] = (
            data[self.target_col] - data[self.target_col].shift(1)
        )

        # 4. Trailing rolling statistics (strictly backward-looking, NO centered windows)
        for w in self.rolling_windows:
            col_name = f"{self.target_col}_rolling_mean_{w}h"
            # rolling window of size w closed on the right (current time t)
            features[col_name] = data[self.target_col].rolling(window=w, min_periods=1).mean()

        # 5. Supporting pollutant and weather features at time t (if present)
        supplementary_cols = ["pm10", "no2", "so2", "co", "o3", "temperature", "relative_humidity", "wind_speed"]
        for supp in supplementary_cols:
            if supp in data.columns and supp != self.target_col:
                features[f"{supp}_current"] = data[supp]

        # 6. Cyclical temporal encodings (capturing diurnal and weekly cycles)
        if self.add_cyclical_time and "timestamp" in data.columns:
            dt = pd.to_datetime(data["timestamp"])
            
            # Diurnal 24-hour cycle
            features["hour_sin"] = np.sin(2 * np.pi * dt.dt.hour / 24.0)
            features["hour_cos"] = np.cos(2 * np.pi * dt.dt.hour / 24.0)
            
            # Weekly 7-day cycle
            dow = dt.dt.day_of_week if hasattr(dt.dt, "day_of_week") else dt.dt.dayofweek
            features["dayofweek_sin"] = np.sin(2 * np.pi * dow / 7.0)
            features["dayofweek_cos"] = np.cos(2 * np.pi * dow / 7.0)
            
            # Weekend indicator
            features["is_weekend"] = (dow >= 5).astype(float)

        # 7. Construct target variable at future horizon: y_{t + horizon}
        target = data[self.target_col].shift(-self.horizon)
        target.name = f"{self.target_col}_target_plus_{self.horizon}h"

        # 8. Clean null boundaries caused by shifting
        if drop_na:
            valid_mask = ~(features.isna().any(axis=1) | target.isna())
            features = features.loc[valid_mask].reset_index(drop=True)
            target = target.loc[valid_mask].reset_index(drop=True)

        self.feature_names_ = list(features.columns)
        logger.info(
            "Constructed %d features across %d samples for horizon +%dh.",
            len(self.feature_names_),
            len(features),
            self.horizon,
        )

        return features, target
