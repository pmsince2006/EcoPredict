"""Unit and pipeline integration tests for model training and evaluation."""

import sys
from pathlib import Path
import pandas as pd
import numpy as np
import pytest

ml_path = Path(__file__).parent.parent.parent / "ml"
sys.path.insert(0, str(ml_path))

from src.training.train import ModelTrainer, chronological_split
from src.evaluation.evaluate import ModelEvaluator


def test_chronological_split_ordering():
    """Verify strictly chronological non-overlapping partitions."""
    n_samples = 100
    features = pd.DataFrame({"feat1": range(n_samples), "pm25_current": range(n_samples)})
    target = pd.Series(range(1, n_samples + 1))

    X_train, y_train, X_val, y_val, X_test, y_test = chronological_split(
        features, target, train_ratio=0.70, val_ratio=0.15
    )

    # Size checks
    assert len(X_train) == 70
    assert len(X_val) == 15
    assert len(X_test) == 15

    # Strict chronological order check (no index overlap, no random shuffling)
    assert X_train.index.max() < X_val.index.min()
    assert X_val.index.max() < X_test.index.min()


def test_evaluator_known_metrics():
    """Test metric computations on known analytical vectors."""
    evaluator = ModelEvaluator()
    y_true = np.array([10.0, 20.0, 30.0])
    y_pred = np.array([12.0, 18.0, 32.0])  # Errors: -2.0, +2.0, -2.0

    metrics = evaluator.compute_metrics(y_true, y_pred, target_unit="µg/m³")
    assert np.isclose(metrics["mae"], 2.0)
    assert np.isclose(metrics["rmse"], 2.0)
    assert metrics["n_samples"] == 3
    assert metrics["unit"] == "µg/m³"


def test_evaluator_comparison_logic():
    """Test comparison against persistence baseline."""
    evaluator = ModelEvaluator()
    base_metrics = {"mae": 10.0, "rmse": 14.0}
    model_metrics = {"mae": 8.0, "rmse": 11.2}

    comp = evaluator.compare_against_baseline(base_metrics, model_metrics)
    assert comp["beats_baseline"] is True
    assert np.isclose(comp["mae_reduction_pct"], 20.0)
    assert np.isclose(comp["rmse_reduction_pct"], 20.0)


def test_trainer_end_to_end_on_fixture(tmp_path):
    """Integration test running full pipeline on software test fixture."""
    trainer = ModelTrainer(
        model_save_dir=tmp_path / "models",
        horizon=1,
        random_state=42,
    )
    results = trainer.run_pipeline("sample_delhi_cpcb_fixture.csv")

    assert "baseline" in results
    assert "model" in results
    assert results["baseline"]["mae"] > 0
    assert results["model"]["mae"] > 0
    assert results["target"] == "pm25"
    assert results["horizon_hours"] == 1

    # Check that artifact files were written
    model_file = tmp_path / "models" / "baseline_random_forest.pkl"
    metadata_file = tmp_path / "models" / "model_metadata.json"
    assert model_file.exists()
    assert metadata_file.exists()
