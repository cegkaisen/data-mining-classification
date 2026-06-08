# Data Mining Assignment 4 - Classification

This repository contains the code and final artefacts for the income classification assignment.

## Repository

GitHub: https://github.com/cegkaisen/data-mining-classification

## Data

- `income.csv`: training data with the `income` target column.
- `income_test.csv`: new instances for final prediction.
- `predictions_template.csv`: required submission format.

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe scripts\smoke_test.py
```

The project was prepared with Python 3.12.

## Main Files

- `notebooks/01_eda.ipynb`: data exploration.
- `notebooks/02_model_experiments.ipynb`: model comparison, tuning, ablation, and fairness analysis.
- `notebooks/03_explainability_and_predictions.ipynb`: SHAP explainability and final predictions.
- `src/`: reusable preprocessing, modeling, evaluation, and fairness helpers.
- `scripts/`: validation checks.
- `reports/report_final_en.md`: final report source.
- `outputs/predictions.csv`: final prediction file.

## Validation

```powershell
.\.venv\Scripts\python.exe scripts\check_preprocessing.py
.\.venv\Scripts\python.exe scripts\check_evaluation.py
.\.venv\Scripts\python.exe scripts\check_modeling.py
.\.venv\Scripts\python.exe scripts\check_predictions.py
```
