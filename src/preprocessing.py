"""Data contract and preprocessing helpers for the income assignment."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler


NUMERIC_FEATURES = ("age", "education", "workinghours")
CATEGORICAL_FEATURES = (
    "workclass",
    "marital status",
    "occupation",
    "sex",
    "ability to speak english",
    "gave birth this year",
)
HIGH_MISSING_FEATURES = ("ability to speak english", "gave birth this year")
TARGET_COLUMN = "income"
TARGET_LABELS = ("high", "low")


@dataclass(frozen=True)
class FeatureGroups:
    """Feature names grouped by preprocessing strategy."""

    numeric: tuple[str, ...]
    categorical: tuple[str, ...]

    @property
    def all_features(self) -> tuple[str, ...]:
        return self.numeric + self.categorical


def get_feature_groups(
    include_sex: bool = True,
    include_high_missing: bool = True,
) -> FeatureGroups:
    """Return feature groups for the requested feature-set variant."""
    categorical = list(CATEGORICAL_FEATURES)

    if not include_sex:
        categorical.remove("sex")

    if not include_high_missing:
        categorical = [
            feature
            for feature in categorical
            if feature not in HIGH_MISSING_FEATURES
        ]

    return FeatureGroups(
        numeric=NUMERIC_FEATURES,
        categorical=tuple(categorical),
    )


def split_features_target(
    df: pd.DataFrame,
    target_col: str = TARGET_COLUMN,
) -> tuple[pd.DataFrame, pd.Series]:
    """Split a training dataframe into features and target."""
    if target_col not in df.columns:
        raise ValueError(f"Expected target column '{target_col}' in dataframe.")
    return df.drop(columns=[target_col]), df[target_col]


def build_preprocessor(
    numeric_features: Iterable[str],
    categorical_features: Iterable[str],
    scale_numeric: bool = True,
) -> ColumnTransformer:
    """Build a leakage-safe preprocessing transformer.

    The returned transformer must be fit only on the training split/fold.
    """
    numeric_steps: list[tuple[str, object]] = [
        ("imputer", SimpleImputer(strategy="median")),
    ]
    if scale_numeric:
        numeric_steps.append(("scaler", StandardScaler()))

    numeric_pipeline = Pipeline(steps=numeric_steps)
    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="constant", fill_value="missing")),
            (
                "to_string",
                FunctionTransformer(
                    lambda values: values.astype(str),
                    feature_names_out="one-to-one",
                ),
            ),
            (
                "encoder",
                OneHotEncoder(handle_unknown="ignore", sparse_output=False),
            ),
        ]
    )

    return ColumnTransformer(
        transformers=[
            ("numeric", numeric_pipeline, list(numeric_features)),
            ("categorical", categorical_pipeline, list(categorical_features)),
        ],
        remainder="drop",
    )


def validate_training_data(df: pd.DataFrame) -> None:
    """Validate the training dataframe schema and target labels."""
    _require_columns(df, get_feature_groups().all_features, "training data")

    if TARGET_COLUMN not in df.columns:
        raise ValueError(f"Training data must include target column '{TARGET_COLUMN}'.")

    if df[TARGET_COLUMN].isna().any():
        raise ValueError(f"Training target column '{TARGET_COLUMN}' contains missing values.")

    unexpected_labels = sorted(set(df[TARGET_COLUMN].dropna()) - set(TARGET_LABELS))
    if unexpected_labels:
        raise ValueError(
            "Training target contains unexpected labels: "
            f"{unexpected_labels}. Expected only {list(TARGET_LABELS)}."
        )


def validate_test_data(df: pd.DataFrame) -> None:
    """Validate the test dataframe schema."""
    if TARGET_COLUMN in df.columns:
        raise ValueError(f"Test data must not include target column '{TARGET_COLUMN}'.")
    _require_columns(df, get_feature_groups().all_features, "test data")


def validate_train_test_compatibility(
    train_df: pd.DataFrame,
    test_df: pd.DataFrame,
) -> None:
    """Validate that train and test expose the same feature columns."""
    train_features = set(train_df.columns) - {TARGET_COLUMN}
    test_features = set(test_df.columns)

    missing_in_test = sorted(train_features - test_features)
    extra_in_test = sorted(test_features - train_features)

    if missing_in_test or extra_in_test:
        raise ValueError(
            "Train/test feature columns are incompatible. "
            f"Missing in test: {missing_in_test}. "
            f"Extra in test: {extra_in_test}."
        )


def _require_columns(
    df: pd.DataFrame,
    required_columns: Iterable[str],
    label: str,
) -> None:
    missing = [column for column in required_columns if column not in df.columns]
    if missing:
        raise ValueError(f"{label} is missing required columns: {missing}.")
