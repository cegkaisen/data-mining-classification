"""Validate evaluation and fairness helpers with small synthetic examples."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.evaluation import classification_metrics_table, overfitting_summary  # noqa: E402
from src.fairness import (  # noqa: E402
    fairness_gap_table,
    group_metrics,
    initial_target_distribution_by_group,
)


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    y_true = pd.Series(["high", "low", "high", "low"])
    y_pred = pd.Series(["high", "low", "low", "low"])
    y_proba = pd.Series([0.90, 0.20, 0.40, 0.10])
    groups = pd.Series(["Male", "Female", "Female", "Male"])

    metrics = classification_metrics_table(
        y_true,
        y_pred,
        y_proba,
        split_name="validation",
        model_name="Synthetic",
        variant="unit",
    )
    assert_true(metrics.loc[0, "accuracy"] == 0.75, "accuracy mismatch")
    assert_true(metrics.loc[0, "precision_high"] == 1.0, "precision_high mismatch")
    assert_true(metrics.loc[0, "recall_high"] == 0.5, "recall_high mismatch")
    assert_true(metrics.loc[0, "precision_low"] == 2 / 3, "precision_low mismatch")
    assert_true(metrics.loc[0, "recall_low"] == 1.0, "recall_low mismatch")
    print("classification metrics: ok")

    reversed_class_probabilities = pd.DataFrame(
        {
            "low": [0.10, 0.80, 0.60, 0.90],
            "high": [0.90, 0.20, 0.40, 0.10],
        }
    )
    class_order_metrics = classification_metrics_table(
        y_true,
        y_pred,
        reversed_class_probabilities,
        classes=["low", "high"],
    )
    assert_true(class_order_metrics.loc[0, "auc"] == metrics.loc[0, "auc"], "class order AUC mismatch")
    print("class-aware probability selection: ok")

    train_metrics = metrics.assign(split="train", accuracy=1.0, auc=1.0)
    validation_metrics = metrics.assign(split="validation", accuracy=0.75, auc=1.0)
    overfit = overfitting_summary(train_metrics, validation_metrics)
    assert_true(overfit.loc[0, "accuracy_gap"] == 0.25, "accuracy gap mismatch")
    print("overfitting summary: ok")

    group_table = group_metrics(y_true, y_pred, y_proba, groups)
    assert_true(set(group_table["group"]) == {"Female", "Male"}, "group metrics mismatch")
    group_table_2d = group_metrics(
        y_true,
        y_pred,
        reversed_class_probabilities,
        groups,
        classes=["low", "high"],
    )
    assert_true(
        group_table_2d["mean_positive_score"].equals(group_table["mean_positive_score"]),
        "group probability selection mismatch",
    )
    gaps = fairness_gap_table(group_table)
    assert_true("positive_prediction_rate" in set(gaps["metric"]), "gap metric missing")
    print("group fairness metrics: ok")

    data = pd.DataFrame({"sex": groups, "income": y_true})
    distribution = initial_target_distribution_by_group(data)
    assert_true({"sex", "income", "count", "rate"}.issubset(distribution.columns), "distribution schema mismatch")
    print("initial target distribution: ok")

    print("\nEvaluation check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
