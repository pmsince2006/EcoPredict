"""Model Training Module for EcoPredict.

Orchestrates:
1. Strict chronological train / validation / test partitioning.
2. Persistence baseline forecasting (y_{t+h} = y_t).
3. Supervised regression model training (Random Forest Regressor).
4. Out-of-sample evaluation on held-out test data.
5. Serialization of model artifacts and metadata with explicit data provenance.
"""

import sys
from pathlib import Path

# Ensure ml directory is on sys.path for direct execution and module import
ml_root = Path(__file__).resolve().parent.parent
project_root = ml_root.parent
for p in [str(ml_root), str(project_root)]:
    if p not in sys.path:
        sys.path.insert(0, p)

from typing import Dict, Any, Optional, Tuple, Union
import json
import logging
import pickle
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor

try:
    from src.data.loader import DataLoader
    from src.features.engineer import FeatureEngineer
    from src.evaluation.evaluate import ModelEvaluator
except ImportError:
    from ml.src.data.loader import DataLoader
    from ml.src.features.engineer import FeatureEngineer
    from ml.src.evaluation.evaluate import ModelEvaluator

logger = logging.getLogger(__name__)


def chronological_split(
    features: pd.DataFrame,
    target: pd.Series,
    train_ratio: float = 0.70,
    val_ratio: float = 0.15,
) -> Tuple[pd.DataFrame, pd.Series, pd.DataFrame, pd.Series, pd.DataFrame, pd.Series]:
    """Splits time series features and targets strictly by chronological order.

    Timeline: [ Train ] -> [ Validation ] -> [ Test ]
    No future leakage, no shuffling.

    Args:
        features: Feature matrix X.
        target: Target vector y.
        train_ratio: Proportion of earliest records allocated to training (default: 0.70).
        val_ratio: Proportion of intermediate records allocated to validation (default: 0.15).

    Returns:
        (X_train, y_train, X_val, y_val, X_test, y_test)
    """
    n = len(features)
    train_end = int(n * train_ratio)
    val_end = int(n * (train_ratio + val_ratio))

    if train_end == 0 or val_end <= train_end or val_end >= n:
        raise ValueError(f"Insufficient samples ({n}) to partition into train/val/test splits.")

    X_train = features.iloc[:train_end].copy()
    y_train = target.iloc[:train_end].copy()

    X_val = features.iloc[train_end:val_end].copy()
    y_val = target.iloc[train_end:val_end].copy()

    X_test = features.iloc[val_end:].copy()
    y_test = target.iloc[val_end:].copy()

    return X_train, y_train, X_val, y_val, X_test, y_test


class ModelTrainer:
    """Trains and serializes baseline and machine learning forecasting models."""

    def __init__(
        self,
        model_save_dir: Optional[Union[str, Path]] = None,
        target_col: str = "pm25",
        horizon: int = 1,
        random_state: int = 42,
    ) -> None:
        """Initializes ModelTrainer.

        Args:
            model_save_dir: Directory where trained model artifacts are stored.
            target_col: Name of the continuous target pollutant (default: 'pm25').
            horizon: Forward prediction horizon in hours (default: 1).
            random_state: Deterministic random seed for reproducibility.
        """
        self.model_save_dir = Path(model_save_dir or "ml/models")
        self.target_col = target_col
        self.horizon = horizon
        self.random_state = random_state

        self.model: Optional[RandomForestRegressor] = None
        self.feature_names: list = []
        self.training_metadata: Dict[str, Any] = {}

    def run_persistence_baseline(
        self,
        X_test: pd.DataFrame,
    ) -> np.ndarray:
        """Computes the persistence baseline forecast.

        Persistence benchmark: y_{t+h} = y_t (the latest known target value at forecast origin).
        """
        current_col = f"{self.target_col}_current"
        if current_col not in X_test.columns:
            raise ValueError(f"Required current target feature '{current_col}' missing from X_test.")
        return X_test[current_col].to_numpy()

    def train_model(
        self,
        X_train: pd.DataFrame,
        y_train: pd.Series,
        n_estimators: int = 100,
        max_depth: int = 8,
    ) -> RandomForestRegressor:
        """Fits a Random Forest Regressor strictly on the training partition.

        Args:
            X_train: Predictor features for training.
            y_train: Target values for training.
            n_estimators: Number of trees in the forest.
            max_depth: Maximum tree depth to constrain overfitting.

        Returns:
            Fitted RandomForestRegressor.
        """
        self.feature_names = list(X_train.columns)
        self.model = RandomForestRegressor(
            n_estimators=n_estimators,
            max_depth=max_depth,
            random_state=self.random_state,
            n_jobs=-1,
        )
        self.model.fit(X_train, y_train)
        logger.info(
            "Fitted Random Forest on %d samples with %d features.",
            len(X_train),
            len(self.feature_names),
        )
        return self.model

    def evaluate_and_compare(
        self,
        X_test: pd.DataFrame,
        y_test: pd.Series,
        evaluator: Optional[ModelEvaluator] = None,
        test_period_info: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """Evaluates persistence baseline and trained model side-by-side on test data.

        Args:
            X_test: Test predictor features.
            y_test: Test ground truth target.
            evaluator: ModelEvaluator instance.
            test_period_info: Optional dictionary with start/end timestamp strings.

        Returns:
            Comparison dictionary with MAE, RMSE, and delta improvements.
        """
        if self.model is None:
            raise ValueError("Model has not been trained. Call train_model() first.")

        ev = evaluator or ModelEvaluator()

        # 1. Evaluate Persistence Baseline: y_hat = y_t
        baseline_preds = self.run_persistence_baseline(X_test)
        baseline_metrics = ev.compute_metrics(y_test, baseline_preds, target_unit="µg/m³")

        # 2. Evaluate Trained Random Forest Model
        model_preds = self.model.predict(X_test)
        model_metrics = ev.compute_metrics(y_test, model_preds, target_unit="µg/m³")

        # 3. Compare Side-by-Side
        comparison = ev.compare_against_baseline(baseline_metrics, model_metrics)
        comparison["target"] = self.target_col
        comparison["horizon_hours"] = self.horizon
        if test_period_info:
            comparison["evaluation_period"] = test_period_info

        return comparison

    def save_artifacts(
        self,
        comparison_results: Dict[str, Any],
        model_filename: str = "baseline_random_forest.pkl",
        metadata_filename: str = "model_metadata.json",
        dataset_source: str = "sample_delhi_cpcb_fixture.csv",
    ) -> Tuple[Path, Path]:
        """Serializes the trained model and its metadata to the models directory.

        Args:
            comparison_results: Metrics and evaluation comparison dictionary.
            model_filename: Pickle filename for model weights.
            metadata_filename: JSON filename for metadata.
            dataset_source: Name or path of source dataset used to fit the model.

        Returns:
            Tuple of (model_path, metadata_path).
        """
        if self.model is None:
            raise ValueError("No trained model to serialize.")

        self.model_save_dir.mkdir(parents=True, exist_ok=True)
        model_path = self.model_save_dir / model_filename
        metadata_path = self.model_save_dir / metadata_filename

        # Save model weights via pickle
        with open(model_path, "wb") as f:
            pickle.dump(self.model, f)

        # Explicit provenance labeling: distinguish synthetic test fixtures from verified real data
        is_synthetic = "fixture" in str(dataset_source).lower() or "synthetic" in str(dataset_source).lower()
        metadata = {
            "model_type": "RandomForestRegressor",
            "model_file": str(model_filename),
            "target_variable": self.target_col,
            "target_unit": "µg/m³",
            "horizon_hours": self.horizon,
            "feature_count": len(self.feature_names),
            "features": self.feature_names,
            "random_state": self.random_state,
            "training_data_provenance": "synthetic_fixture" if is_synthetic else "verified_real_data",
            "dataset_source": str(dataset_source),
            "is_demo_model": is_synthetic,
            "real_data_validated": not is_synthetic,
            "data_status": "demo_preview" if is_synthetic else "real_data_forecast",
            "warning": (
                "DEMO MODEL ONLY: Trained on a synthetic test fixture. Not validated against real atmospheric data."
                if is_synthetic
                else None
            ),
            "evaluation_metrics": comparison_results,
        }

        with open(metadata_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2)

        logger.info("Saved model artifact to %s and metadata to %s", model_path, metadata_path)
        return model_path, metadata_path

    def run_pipeline(
        self,
        dataset_path_or_name: Union[str, Path] = "sample_delhi_cpcb_fixture.csv",
    ) -> Dict[str, Any]:
        """Executes the full reproducible training and evaluation pipeline on a dataset.

        Args:
            dataset_path_or_name: CSV dataset filename or path.

        Returns:
            Summary dictionary with pipeline results.
        """
        loader = DataLoader()
        df = loader.load_dataset(dataset_path_or_name)

        # Feature engineering
        engineer = FeatureEngineer(
            target_col=self.target_col,
            horizon=self.horizon,
        )
        X, y = engineer.create_features(df, drop_na=True)

        # Chronological split (70% train, 15% val, 15% test)
        X_train, y_train, X_val, y_val, X_test, y_test = chronological_split(X, y)

        # Train Random Forest
        self.train_model(X_train, y_train)

        # Test period metadata
        period_info = {}
        if "timestamp" in df.columns:
            period_info = {
                "test_start_index": int(len(X_train) + len(X_val)),
                "test_samples": int(len(X_test)),
            }

        # Evaluate against persistence baseline
        results = self.evaluate_and_compare(X_test, y_test, test_period_info=period_info)

        # Save artifacts with explicit provenance
        self.save_artifacts(results, dataset_source=str(dataset_path_or_name))

        return results


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    trainer = ModelTrainer(horizon=1)
    results = trainer.run_pipeline()
    print("\n--- Pipeline Execution Results ---")
    print(json.dumps(results, indent=2))
