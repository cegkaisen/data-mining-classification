"""Evaluation helpers for classification experiments."""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score


def classification_metrics_table(
    y_true,
    y_pred,
    y_proba,
    positive_label: str = "high",
    split_name: str = "validation",
    model_name: str | None = None,
    variant: str | None = None,
    classes=None,
) -> pd.DataFrame:
    """Return a one-row classification metric table."""
    y_true_series = pd.Series(y_true)
    y_pred_series = pd.Series(y_pred)
    positive_scores = _as_positive_scores(y_proba, classes, positive_label)
    negative_label = _negative_label(y_true_series, positive_label)

    row = {
        "model": model_name,
        "variant": variant,
        "split": split_name,
        "accuracy": accuracy_score(y_true_series, y_pred_series),
        "auc": roc_auc_score(y_true_series.eq(positive_label).astype(int), positive_scores),
        f"precision_{positive_label}": precision_score(
            y_true_series,
            y_pred_series,
            pos_label=positive_label,
            zero_division=0,
        ),
        f"recall_{positive_label}": recall_score(
            y_true_series,
            y_pred_series,
            pos_label=positive_label,
            zero_division=0,
        ),
        f"precision_{negative_label}": precision_score(
            y_true_series,
            y_pred_series,
            pos_label=negative_label,
            zero_division=0,
        ),
        f"recall_{negative_label}": recall_score(
            y_true_series,
            y_pred_series,
            pos_label=negative_label,
            zero_division=0,
        ),
        "positive_prediction_rate": y_pred_series.eq(positive_label).mean(),
        "n": len(y_true_series),
    }
    return pd.DataFrame([row])


def evaluate_classifier(
    model,
    X,
    y,
    split_name: str,
    positive_label: str = "high",
    model_name: str | None = None,
    variant: str | None = None,
) -> pd.DataFrame:
    """Evaluate a fitted classifier on one split."""
    y_pred = model.predict(X)
    y_proba = model.predict_proba(X)
    inferred_model_name = model_name or model.__class__.__name__
    return classification_metrics_table(
        y,
        y_pred,
        y_proba,
        positive_label=positive_label,
        split_name=split_name,
        model_name=inferred_model_name,
        variant=variant,
        classes=model.classes_,
    )


def overfitting_summary(
    train_metrics: pd.DataFrame,
    validation_metrics: pd.DataFrame,
) -> pd.DataFrame:
    """Compare train and validation metrics by model and variant."""
    key_columns = ["model", "variant"]
    metric_columns = ["accuracy", "auc"]

    train = train_metrics[key_columns + metric_columns].rename(
        columns={metric: f"train_{metric}" for metric in metric_columns}
    )
    validation = validation_metrics[key_columns + metric_columns].rename(
        columns={metric: f"validation_{metric}" for metric in metric_columns}
    )

    summary = train.merge(validation, on=key_columns, how="inner")
    for metric in metric_columns:
        summary[f"{metric}_gap"] = summary[f"train_{metric}"] - summary[
            f"validation_{metric}"
        ]
    return summary


def _as_positive_scores(y_proba, classes, positive_label: str) -> np.ndarray:
    scores = np.asarray(y_proba)
    if scores.ndim == 2:
        if classes is None:
            raise ValueError(
                "Two-dimensional probabilities require class labels. "
                "Pass positive-class scores as a one-dimensional array, "
                "or provide classes so the positive column can be selected safely."
            )
        return _positive_scores_from_classes(scores, classes, positive_label)
    return scores


def _positive_scores_from_classes(y_proba, classes, positive_label: str) -> np.ndarray:
    classes_array = np.asarray(classes)
    if positive_label not in classes_array:
        raise ValueError(f"Positive label '{positive_label}' not found in model classes.")

    scores = np.asarray(y_proba)
    if scores.ndim == 1:
        return scores

    positive_index = int(np.where(classes_array == positive_label)[0][0])
    return scores[:, positive_index]


def _negative_label(y_true: pd.Series, positive_label: str) -> str:
    labels = [label for label in sorted(y_true.dropna().unique()) if label != positive_label]
    if len(labels) != 1:
        raise ValueError(
            "Expected exactly one negative label. "
            f"Found labels other than '{positive_label}': {labels}."
        )
    return str(labels[0])
