"""Model Evaluation Module for EcoPredict.

Computes regression metrics (MAE, RMSE, R2, MAPE), compares candidate models against
persistence baselines, and exports structured evaluation reports.
"""

from pathlib import Path
from typing import Dict, Any, Optional, Union
import json
import logging
import numpy as np

logger = logging.getLogger(__name__)


class ModelEvaluator:
    """Evaluates regression models for air quality forecasting."""

    def __init__(self, reports_dir: Optional[Union[str, Path]] = None) -> None:
        """Initializes evaluator with configurable reports output directory.

        Args:
            reports_dir: Directory where evaluation reports are stored (default: 'ml/reports').
        """
        self.reports_dir = Path(reports_dir or "ml/reports")

    def compute_metrics(
        self,
        y_true: Union[np.ndarray, list],
        y_pred: Union[np.ndarray, list],
        target_unit: str = "µg/m³",
    ) -> Dict[str, Any]:
        """Calculates standard regression benchmarks.

        Args:
            y_true: Ground truth target observations.
            y_pred: Model predicted values.
            target_unit: Physical unit of the target (e.g. 'µg/m³').

        Returns:
            Dictionary containing MAE, RMSE, R2, MAPE, sample count, and unit.
        """
        yt = np.asarray(y_true, dtype=float)
        yp = np.asarray(y_pred, dtype=float)

        if len(yt) != len(yp):
            raise ValueError(f"Length mismatch: y_true ({len(yt)}) != y_pred ({len(yp)})")

        if len(yt) == 0:
            raise ValueError("Cannot evaluate metrics on empty arrays.")

        errors = yt - yp
        mae = float(np.mean(np.abs(errors)))
        rmse = float(np.sqrt(np.mean(errors ** 2)))

        # R-squared (coefficient of determination)
        ss_res = np.sum(errors ** 2)
        ss_tot = np.sum((yt - np.mean(yt)) ** 2)
        r2 = float(1.0 - (ss_res / ss_tot)) if ss_tot > 0 else 0.0

        # Mean Absolute Percentage Error (MAPE) where y_true > 0
        valid_pct_mask = yt > 0
        if np.any(valid_pct_mask):
            mape = float(np.mean(np.abs(errors[valid_pct_mask] / yt[valid_pct_mask])) * 100.0)
        else:
            mape = float("nan")

        return {
            "mae": round(mae, 3),
            "rmse": round(rmse, 3),
            "r2": round(r2, 4),
            "mape_pct": round(mape, 2) if not np.isnan(mape) else None,
            "n_samples": int(len(yt)),
            "unit": target_unit,
        }

    def compare_against_baseline(
        self,
        baseline_metrics: Dict[str, Any],
        model_metrics: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Compares a candidate model side-by-side with the persistence baseline.

        Args:
            baseline_metrics: Metrics dictionary for the baseline.
            model_metrics: Metrics dictionary for the evaluated model.

        Returns:
            Structured comparison dictionary with delta improvements.
        """
        base_mae = baseline_metrics["mae"]
        model_mae = model_metrics["mae"]

        base_rmse = baseline_metrics["rmse"]
        model_rmse = model_metrics["rmse"]

        # Positive delta indicates improvement (error reduction)
        mae_improvement_pct = round(((base_mae - model_mae) / base_mae) * 100.0, 2) if base_mae > 0 else 0.0
        rmse_improvement_pct = round(((base_rmse - model_rmse) / base_rmse) * 100.0, 2) if base_rmse > 0 else 0.0

        beats_baseline = (model_mae < base_mae) and (model_rmse < base_rmse)

        return {
            "baseline": baseline_metrics,
            "model": model_metrics,
            "mae_reduction_pct": mae_improvement_pct,
            "rmse_reduction_pct": rmse_improvement_pct,
            "beats_baseline": beats_baseline,
            "conclusion": (
                f"Model beats baseline with {mae_improvement_pct}% MAE reduction."
                if beats_baseline
                else "Model does not beat persistence baseline. Further feature engineering or data tuning required."
            ),
        }

    def save_report(self, report_data: Dict[str, Any], filename: str = "evaluation_summary.json") -> Path:
        """Serializes the evaluation summary report to the reports directory.

        Args:
            report_data: Dictionary containing evaluation results.
            filename: JSON file name.

        Returns:
            Absolute path to saved JSON report.
        """
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        target_path = self.reports_dir / filename
        with open(target_path, "w", encoding="utf-8") as f:
            json.dump(report_data, f, indent=2)
        logger.info("Evaluation report saved to %s", target_path)
        return target_path
