"""Model specifications and pipeline helpers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline


@dataclass(frozen=True)
class ModelSpec:
    """Named model candidate used in experiment notebooks."""

    name: str
    estimator: object


def get_model_specs(random_state: int = 42) -> tuple[ModelSpec, ...]:
    """Return initial model candidates for T5."""
    return (
        ModelSpec(
            name="Logistic Regression",
            estimator=LogisticRegression(
                max_iter=1000,
                random_state=random_state,
            ),
        ),
        ModelSpec(
            name="Random Forest",
            estimator=RandomForestClassifier(
                n_estimators=200,
                max_depth=None,
                min_samples_leaf=1,
                n_jobs=-1,
                random_state=random_state,
            ),
        ),
        ModelSpec(
            name="HistGradientBoosting",
            estimator=HistGradientBoostingClassifier(
                max_iter=150,
                learning_rate=0.08,
                random_state=random_state,
            ),
        ),
    )


def build_pipeline(preprocessor, model) -> Pipeline:
    """Combine preprocessing and estimator in one leakage-safe pipeline."""
    return Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", model),
        ]
    )


def get_tuning_grids() -> dict[str, dict[str, list[Any]]]:
    """Return small hyperparameter grids keyed by model name."""
    return {
        "Logistic Regression": {
            "model__C": [0.1, 1.0, 10.0],
        },
        "Random Forest": {
            "model__max_depth": [6, 10, None],
            "model__min_samples_leaf": [1, 5],
            "model__max_features": ["sqrt", None],
        },
        "HistGradientBoosting": {
            "model__max_iter": [100, 150],
            "model__learning_rate": [0.05, 0.08],
            "model__max_leaf_nodes": [15, 31],
        },
    }
