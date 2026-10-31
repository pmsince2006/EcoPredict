"""Smoke tests for ML pipeline scaffolding."""

import sys
from pathlib import Path

# Add ML directory to path
ml_path = Path(__file__).parent.parent.parent / "ml"
sys.path.insert(0, str(ml_path))

from src.data.loader import DataLoader
from src.features.engineer import FeatureEngineer
from src.training.train import ModelTrainer
from src.evaluation.evaluate import ModelEvaluator


def test_data_loader_initialization():
    """Verify DataLoader initial state."""
    loader = DataLoader()
    assert loader.raw_data_dir == Path("ml/data/raw")
    # Missing file returns None gracefully
    result = loader.load_dataset("non_existent_dataset.csv")
    assert result is None


def test_feature_engineer_transform():
    """Verify FeatureEngineer returns expected dictionary format."""
    engineer = FeatureEngineer(lag_hours=12)
    result = engineer.transform({"pm25": 100.0, "pm10": 200.0})
    assert result["lag_hours"] == 12
    assert result["status"] == "ready_for_pipeline"


def test_model_trainer_pipeline():
    """Verify trainer scaffold returns planned status."""
    trainer = ModelTrainer()
    output = trainer.run_training_pipeline()
    assert output["status"] == "planned"


def test_model_evaluator():
    """Verify evaluator returns dictionary with basic metrics."""
    evaluator = ModelEvaluator()
    metrics = evaluator.evaluate([100], [105])
    assert "mae" in metrics
    assert "rmse" in metrics
