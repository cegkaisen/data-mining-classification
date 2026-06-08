"""Fairness-oriented summaries for the income assignment."""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score


def initial_target_distribution_by_group(
    df: pd.DataFrame,
    group_col: str = "sex",
    target_col: str = "income",
) -> pd.DataFrame:
    """Summarize target distribution by a protected/group column."""
    counts = (
        df.groupby([group_col, target_col], dropna=False)
        .size()
        .rename("count")
        .reset_index()
    )
    totals = counts.groupby(group_col, dropna=False)["count"].transform("sum")
    counts["rate"] = counts["count"] / totals
    return counts


def group_metrics(
    y_true,
    y_pred,
    y_proba,
    group_values,
    positive_label: str = "high",
    classes=None,
) -> pd.DataFrame:
    """Compute model metrics by group."""
    frame = pd.DataFrame(
        {
            "y_true": pd.Series(y_true).reset_index(drop=True),
            "y_pred": pd.Series(y_pred).reset_index(drop=True),
            "positive_score": _as_positive_scores(y_proba, classes, positive_label),
            "group": pd.Series(group_values).reset_index(drop=True),
        }
    )

    rows = []
    for group, group_df in frame.groupby("group", dropna=False):
        rows.append(
            {
                "group": group,
                "n": len(group_df),
                "accuracy": accuracy_score(group_df["y_true"], group_df["y_pred"]),
                f"precision_{positive_label}": precision_score(
                    group_df["y_true"],
                    group_df["y_pred"],
                    pos_label=positive_label,
                    zero_division=0,
                ),
                f"recall_{positive_label}": recall_score(
                    group_df["y_true"],
                    group_df["y_pred"],
                    pos_label=positive_label,
                    zero_division=0,
                ),
                "positive_prediction_rate": group_df["y_pred"].eq(positive_label).mean(),
                "mean_positive_score": group_df["positive_score"].mean(),
            }
        )
    return pd.DataFrame(rows)


def fairness_gap_table(group_metric_table: pd.DataFrame) -> pd.DataFrame:
    """Return max-min gaps for numeric group metrics."""
    numeric_columns = [
        column
        for column in group_metric_table.select_dtypes(include="number").columns
        if column != "n"
    ]
    rows = []
    for column in numeric_columns:
        rows.append(
            {
                "metric": column,
                "min": group_metric_table[column].min(),
                "max": group_metric_table[column].max(),
                "gap": group_metric_table[column].max() - group_metric_table[column].min(),
            }
        )
    return pd.DataFrame(rows)


def _as_positive_scores(y_proba, classes, positive_label: str) -> np.ndarray:
    scores = np.asarray(y_proba)
    if scores.ndim == 2:
        if classes is None:
            raise ValueError(
                "Two-dimensional probabilities require class labels. "
                "Pass positive-class scores as a one-dimensional array, "
                "or provide classes so the positive column can be selected safely."
            )
        classes_array = np.asarray(classes)
        if positive_label not in classes_array:
            raise ValueError(f"Positive label '{positive_label}' not found in classes.")
        positive_index = int(np.where(classes_array == positive_label)[0][0])
        return scores[:, positive_index]
    return scores
