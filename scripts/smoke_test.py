"""Smoke test for the project environment.

The test checks imports and required input-file presence without mutating the
raw assignment data.
"""

from __future__ import annotations

import importlib
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


REQUIRED_MODULES = (
    "pandas",
    "numpy",
    "sklearn",
    "matplotlib",
    "seaborn",
    "nbformat",
    "nbconvert",
)

EXPLAINABILITY_MODULES = (
    "shap",
    "lime",
)


def import_module(name: str) -> tuple[bool, str]:
    try:
        importlib.import_module(name)
    except Exception as exc:  # pragma: no cover - smoke-test diagnostics only
        return False, f"{type(exc).__name__}: {exc}"
    return True, "ok"


def main() -> int:
    failures: list[str] = []

    src_ok, src_message = import_module("src")
    print(f"src: {src_message}")
    if not src_ok:
        failures.append(f"src import failed: {src_message}")

    for module_name in REQUIRED_MODULES:
        ok, message = import_module(module_name)
        print(f"{module_name}: {message}")
        if not ok:
            failures.append(f"{module_name} import failed: {message}")

    for module_name in EXPLAINABILITY_MODULES:
        ok, message = import_module(module_name)
        print(f"{module_name}: {message}")
        if not ok:
            failures.append(
                f"{module_name} import failed: {message}. "
                "Use the documented SHAP/LIME fallback strategy if needed."
            )

    from src.project_paths import missing_input_files

    missing_files = missing_input_files()
    if missing_files:
        for path in missing_files:
            failures.append(f"Missing required input file: {path}")
    else:
        print("required input files: ok")

    if failures:
        print("\nSmoke test failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("\nSmoke test passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

