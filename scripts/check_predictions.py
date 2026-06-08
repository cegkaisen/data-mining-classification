"""Validate final prediction output against the assignment template."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.project_paths import INCOME_TEST_CSV, OUTPUTS_DIR, PREDICTIONS_TEMPLATE_CSV  # noqa: E402


PREDICTIONS_CSV = OUTPUTS_DIR / "predictions.csv"
VALID_LABELS = {"high", "low"}


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    assert_true(PREDICTIONS_CSV.is_file(), f"Missing predictions file: {PREDICTIONS_CSV}")

    predictions = pd.read_csv(PREDICTIONS_CSV)
    template = pd.read_csv(PREDICTIONS_TEMPLATE_CSV)
    test_df = pd.read_csv(INCOME_TEST_CSV)

    assert_true(list(predictions.columns) == ["id", "income"], "predictions columns must be id,income")
    assert_true(len(predictions) == len(template) == len(test_df), "prediction/template/test row counts mismatch")
    assert_true(predictions["id"].equals(template["id"]), "prediction ids must exactly match template ids")
    assert_true(set(predictions["income"].dropna()).issubset(VALID_LABELS), "predictions contain invalid labels")
    assert_true(not predictions["income"].isna().any(), "predictions contain missing labels")

    print("prediction schema: ok")
    print("template id equality: ok")
    print("prediction labels: ok")
    print("\nPrediction check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
