"""Validate modeling grids and high-positive scoring helpers."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.evaluation import high_positive_auc_scorer  # noqa: E402
from src.modeling import get_model_specs, get_tuning_grids  # noqa: E402


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


class ReversedClassEstimator:
    """Tiny estimator exposing classes in low/high order."""

    classes_ = np.array(["low", "high"])

    def predict_proba(self, X):
        return np.array(
            [
                [0.10, 0.90],
                [0.80, 0.20],
                [0.60, 0.40],
                [0.90, 0.10],
            ]
        )


def main() -> int:
    model_names = {spec.name for spec in get_model_specs()}
    grids = get_tuning_grids()
    assert_true(model_names == set(grids), "tuning grids must match model specs")

    expected_prefixes = {
        "Logistic Regression": {"model__C"},
        "Random Forest": {
            "model__max_depth",
            "model__min_samples_leaf",
            "model__max_features",
        },
        "HistGradientBoosting": {
            "model__max_iter",
            "model__learning_rate",
            "model__max_leaf_nodes",
        },
    }
    for model_name, expected_keys in expected_prefixes.items():
        assert_true(set(grids[model_name]) == expected_keys, f"{model_name} grid mismatch")
        for key, values in grids[model_name].items():
            assert_true(key.startswith("model__"), f"{key} must target the pipeline model step")
            assert_true(len(values) > 0, f"{key} must not be empty")
    print("tuning grids: ok")

    y_true = pd.Series(["high", "low", "high", "low"])
    score = high_positive_auc_scorer(ReversedClassEstimator(), None, y_true)
    assert_true(score == 1.0, "high-positive AUC scorer selected the wrong probability column")
    print("high-positive auc scorer: ok")

    print("\nModeling check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
