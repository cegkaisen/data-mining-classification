"""Project path helpers.

This module intentionally contains only lightweight path constants for T1.
Task-specific data loading and preprocessing logic belongs to later tasks.
"""

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

INCOME_CSV = PROJECT_ROOT / "income.csv"
INCOME_TEST_CSV = PROJECT_ROOT / "income_test.csv"
PREDICTIONS_TEMPLATE_CSV = PROJECT_ROOT / "predictions_template.csv"

DOCS_DIR = PROJECT_ROOT / "docs"
NOTEBOOKS_DIR = PROJECT_ROOT / "notebooks"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
REPORTS_DIR = PROJECT_ROOT / "reports"
FIGURES_DIR = OUTPUTS_DIR / "figures"

INPUT_FILES = (
    INCOME_CSV,
    INCOME_TEST_CSV,
    PREDICTIONS_TEMPLATE_CSV,
)


def missing_input_files() -> list[Path]:
    """Return required input files that are not present."""
    return [path for path in INPUT_FILES if not path.is_file()]

