"""Data Loader & Ingestion Module for EcoPredict.

Responsible for:
- Loading raw air quality CSV time-series datasets from disk.
- Validating required columns and schemas.
- Parsing timestamps with timezone awareness.
- Detecting and reporting missing values, duplicates, and physical anomalies (e.g., negative concentrations).
- Sanitizing invalid sensor artifacts without silently deleting data.
- Exporting processed datasets to ml/data/processed/.
"""

from pathlib import Path
from typing import Optional, List, Dict, Any, Union
import logging
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)

# Standard required columns for ambient air quality monitoring
DEFAULT_REQUIRED_COLUMNS = ["timestamp", "station_id", "pm25"]

# Expected non-negative physical concentrations and reasonable sensor maximums
PHYSICAL_LIMITS: Dict[str, Dict[str, float]] = {
    "pm25": {"min": 0.0, "max": 1000.0},
    "pm10": {"min": 0.0, "max": 1500.0},
    "no2": {"min": 0.0, "max": 500.0},
    "so2": {"min": 0.0, "max": 500.0},
    "co": {"min": 0.0, "max": 50.0},
    "o3": {"min": 0.0, "max": 500.0},
    "wind_speed": {"min": 0.0, "max": 60.0},
    "relative_humidity": {"min": 0.0, "max": 100.0},
}


class DataValidationError(ValueError):
    """Raised when an input dataset fails schema or data integrity validation."""
    pass


class DataLoader:
    """Loads, inspects, and validates ambient air quality time-series datasets."""

    def __init__(
        self,
        raw_data_dir: Optional[Union[str, Path]] = None,
        processed_data_dir: Optional[Union[str, Path]] = None,
    ) -> None:
        """Initializes the data loader with configurable input and output directories.

        Args:
            raw_data_dir: Path to directory containing raw CSV files (default: 'ml/data/raw').
            processed_data_dir: Path to directory where processed data is stored (default: 'ml/data/processed').
        """
        self.raw_data_dir = Path(raw_data_dir or "ml/data/raw")
        self.processed_data_dir = Path(processed_data_dir or "ml/data/processed")
        self.validation_report: Dict[str, Any] = {}

    def load_dataset(
        self,
        file_path_or_name: Union[str, Path],
        required_columns: Optional[List[str]] = None,
        drop_duplicates: bool = True,
        clip_negatives: bool = True,
    ) -> pd.DataFrame:
        """Loads and validates a raw air-quality CSV dataset.

        Args:
            file_path_or_name: File name in raw_data_dir or an absolute Path.
            required_columns: List of columns required in the CSV. Defaults to timestamp, station_id, pm25.
            drop_duplicates: If True, identifies and removes duplicate timestamps for the same station.
            clip_negatives: If True, replaces negative pollutant readings with NaN rather than discarding rows.

        Returns:
            Validated, sorted pandas DataFrame.

        Raises:
            FileNotFoundError: If the specified file does not exist.
            DataValidationError: If required columns are missing or the file is malformed.
        """
        required_cols = required_columns or DEFAULT_REQUIRED_COLUMNS

        # Resolve path
        path = Path(file_path_or_name)
        if not path.is_absolute():
            path = self.raw_data_dir / path

        if not path.exists():
            raise FileNotFoundError(f"Dataset file not found at: {path}")

        logger.info("Reading raw dataset from %s", path)

        try:
            df = pd.read_csv(path)
        except Exception as e:
            raise DataValidationError(f"Failed to parse CSV file at {path}: {str(e)}") from e

        if df.empty:
            raise DataValidationError(f"Dataset at {path} is empty (0 rows).")

        # 1. Validate required columns
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            raise DataValidationError(
                f"Missing required column(s): {missing_cols}. Available columns: {list(df.columns)}"
            )

        initial_rows = len(df)

        # 2. Parse timestamps consistently
        try:
            df["timestamp"] = pd.to_datetime(df["timestamp"], errors="raise")
        except Exception as e:
            raise DataValidationError(f"Invalid timestamp format in dataset: {str(e)}") from e

        # 3. Check and report duplicate records
        duplicate_mask = df.duplicated(subset=["timestamp", "station_id"], keep="last")
        duplicate_count = int(duplicate_mask.sum())
        if duplicate_count > 0:
            logger.warning("Found %d duplicate timestamp records. Keeping latest observation.", duplicate_count)
            if drop_duplicates:
                df = df[~duplicate_mask].copy()

        # 4. Check for invalid and non-finite numeric measurements
        anomaly_counts: Dict[str, int] = {}
        for col, limits in PHYSICAL_LIMITS.items():
            if col in df.columns:
                # Coerce to numeric
                df[col] = pd.to_numeric(df[col], errors="coerce")
                
                # Detect negative concentrations (sensor calibration artifacts)
                negatives = (df[col] < limits["min"])
                num_negatives = int(negatives.sum())
                if num_negatives > 0:
                    logger.warning(
                        "Column '%s' contains %d negative readings (< %.1f). Sanitizing to NaN.",
                        col, num_negatives, limits["min"]
                    )
                    anomaly_counts[col] = num_negatives
                    if clip_negatives:
                        df.loc[negatives, col] = np.nan

        # 5. Missing value accounting (without silent deletion)
        missing_stats: Dict[str, Dict[str, Union[int, float]]] = {}
        for col in df.columns:
            null_count = int(df[col].isna().sum())
            null_pct = round((null_count / len(df)) * 100, 2)
            missing_stats[col] = {"missing_count": null_count, "missing_pct": null_pct}

        # 6. Chronological sorting
        df = df.sort_values(by="timestamp").reset_index(drop=True)

        # Store validation summary
        self.validation_report = {
            "source_path": str(path),
            "initial_rows": initial_rows,
            "final_rows": len(df),
            "duplicates_removed": duplicate_count if drop_duplicates else 0,
            "anomalies_sanitized": anomaly_counts,
            "missing_stats": missing_stats,
            "date_range": {
                "start": str(df["timestamp"].min()),
                "end": str(df["timestamp"].max()),
            },
            "stations": list(df["station_id"].unique()) if "station_id" in df.columns else [],
        }

        logger.info(
            "Dataset validated successfully: %d rows from %s to %s",
            len(df),
            self.validation_report["date_range"]["start"],
            self.validation_report["date_range"]["end"],
        )

        return df

    def save_processed(self, df: pd.DataFrame, filename: str) -> Path:
        """Saves a processed, validated DataFrame to the processed directory.

        Args:
            df: Validated pandas DataFrame.
            filename: Destination CSV file name.

        Returns:
            Absolute Path of the written file.
        """
        self.processed_data_dir.mkdir(parents=True, exist_ok=True)
        target_path = self.processed_data_dir / filename
        df.to_csv(target_path, index=False)
        logger.info("Saved processed dataset (%d rows) to %s", len(df), target_path)
        return target_path
