"""Validate preprocessing helpers against the assignment data."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.preprocessing import (  # noqa: E402
    HIGH_MISSING_FEATURES,
    build_preprocessor,
    get_feature_groups,
    split_features_target,
    validate_test_data,
    validate_train_test_compatibility,
    validate_training_data,
)
from src.project_paths import INCOME_CSV, INCOME_TEST_CSV  # noqa: E402


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    train_df = pd.read_csv(INCOME_CSV)
    test_df = pd.read_csv(INCOME_TEST_CSV)

    validate_training_data(train_df)
    validate_test_data(test_df)
    validate_train_test_compatibility(train_df, test_df)
    print("schema validation: ok")

    full = get_feature_groups()
    no_sex = get_feature_groups(include_sex=False)
    no_high_missing = get_feature_groups(include_high_missing=False)

    assert_true("sex" in full.categorical, "full feature set should include sex")
    assert_true("sex" not in no_sex.categorical, "no_sex variant should remove sex")
    for feature in HIGH_MISSING_FEATURES:
        assert_true(
            feature not in no_high_missing.categorical,
            f"no_high_missing variant should remove {feature}",
        )
    print("feature group variants: ok")

    X_train, y_train = split_features_target(train_df)
    assert_true("income" not in X_train.columns, "target leaked into X_train")
    assert_true(len(y_train) == len(train_df), "target row count mismatch")
    print("feature/target split: ok")

    preprocessor = build_preprocessor(full.numeric, full.categorical)
    selected_features = list(full.all_features)
    transformed_train = preprocessor.fit_transform(X_train[selected_features])
    transformed_test = preprocessor.transform(test_df[selected_features])

    assert_true(
        transformed_train.shape[0] == len(train_df),
        "transformed train row count changed",
    )
    assert_true(
        transformed_test.shape[0] == len(test_df),
        "transformed test row count changed",
    )
    assert_true(
        transformed_train.shape[1] == transformed_test.shape[1],
        "train/test transformed feature counts differ",
    )
    print("preprocessor fit/transform: ok")

    print("\nPreprocessing check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
