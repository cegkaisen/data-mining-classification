# Data Mining Assignment 4 - Classification

**Student:** Niyazi Cenk Genek - 20259604

**GitHub repository:** https://github.com/cegkaisen/data-mining-classification

---

## 1. Introduction

In this project, I built a binary classification model for the `income.csv` dataset. The goal is to predict whether a person belongs to the `high` or `low` income class based on demographic and socioeconomic attributes.

This problem is not only about getting a good score. Income prediction can be used in decision-making contexts, so the model should also be checked for overfitting, interpretability, and gender fairness. For that reason, I did not select the final model only by accuracy. I compared several metrics and also looked at SHAP explanations and group-level fairness results.

The code is split into reusable Python modules in `src/` and analysis notebooks in `notebooks/`. The final prediction file is produced as `outputs/predictions.csv`.

---

## 2. Data Exploration

The training dataset contains **9000 rows**. The test dataset, `income_test.csv`, contains **2000 rows** and does not include the target label. The target distribution is somewhat imbalanced: `low` appears in 5921 rows, or **0.658**, while `high` appears in 3079 rows, or **0.342**.

This imbalance matters because a model can get a reasonable accuracy by doing well on the larger `low` class while still missing many `high` cases. I therefore used AUC, precision, and recall together with accuracy.

During EDA, two columns had a high amount of missing values:

- `ability to speak english`
- `gave birth this year`

I did not remove them immediately. Missingness can sometimes be informative, so I kept them in the main feature set and tested their impact later with an ablation experiment.

![Class distribution](../outputs/figures/class_distribution.png)

---

## 3. Preprocessing

The preprocessing pipeline was built with `sklearn` so that every transformation is fitted only on the training split or training fold.

The main preprocessing steps were:

1. Numeric missing values were filled with median imputation.
2. Numeric features were standardized.
3. Categorical missing values were replaced with a `missing` category.
4. Categorical variables were encoded using one-hot encoding.
5. Unknown categories in validation or test data were ignored safely.

I used this pipeline structure to avoid data leakage. If the imputer, scaler, or encoder were fitted before splitting the data, information from validation data could leak into training. That would make the validation score too optimistic.

---

## 4. Classification Methods

For Task 1, I trained three classification models:

1. **Logistic Regression**
2. **Random Forest**
3. **HistGradientBoosting**

Random Forest and HistGradientBoosting are ensemble models, so the assignment requirement of using at least one ensemble model is satisfied.

I first ran a baseline comparison. After that, I tuned hyperparameters using 3-fold StratifiedKFold on the training split only. The validation split was kept separate and was used for the final comparison. I did not use `income_test.csv` for model selection, threshold tuning, or feature selection.

The primary selection metric was validation AUC. I also reported accuracy, precision, and recall for both classes, because AUC alone does not show how the model behaves at the final threshold.

---

## 5. Model Results

The best final candidate was **HistGradientBoosting / tuned_full**.

| Model / variant | Accuracy | AUC | Precision high | Recall high | Precision low | Recall low |
|---|---:|---:|---:|---:|---:|---:|
| HistGradientBoosting / tuned_full | 0.784 | 0.854 | 0.709 | 0.628 | 0.817 | 0.866 |
| Random Forest / sex_removed | 0.777 | 0.853 | 0.722 | 0.568 | 0.798 | 0.886 |
| Random Forest / high_missing_removed | 0.779 | 0.853 | 0.728 | 0.565 | 0.797 | 0.890 |

The Random Forest variants came very close in AUC. Still, HistGradientBoosting had the highest AUC and better recall for the `high` class than those Random Forest alternatives. That made it the strongest overall choice.

The final model used:

- `learning_rate = 0.08`
- `max_iter = 100`
- `max_leaf_nodes = 15`

---

## 6. Overfitting and Hyperparameter Tuning

To investigate overfitting, I compared train AUC and validation AUC after tuning. The gaps were:

| Model | Train AUC | Validation AUC | AUC gap |
|---|---:|---:|---:|
| Logistic Regression | 0.860 | 0.843 | 0.017 |
| Random Forest | 0.909 | 0.853 | 0.056 |
| HistGradientBoosting | 0.897 | 0.854 | 0.043 |

Logistic Regression had the smallest gap, but its validation AUC was lower. Random Forest showed the largest gap, which suggests more overfitting. HistGradientBoosting was in the middle. It still had some gap, but it also gave the best validation AUC.

The overfitting reduction technique I used was hyperparameter tuning. For the tree-based models, I controlled model complexity with parameters such as depth, leaf size, number of iterations, learning rate, and leaf nodes. This reduced the extreme overfitting seen in the initial Random Forest, whose untuned train AUC was almost perfect.

---

## 7. Feature Selection and Class Imbalance

I used ablation experiments as a simple and explainable feature selection approach. I compared:

- the full feature set
- removing the high-missing columns
- removing `sex`

The results were close. Removing the high-missing columns gave a best AUC of **0.853**, very similar to the full model. Removing `sex` also gave a best AUC of **0.853**. So these features were not the only reason the model performed well.

I also tested `class_weight="balanced"` for Logistic Regression and Random Forest. The balanced Random Forest increased `high` recall to **0.791**, which is useful if the main goal is to catch more `high` cases. However, its precision and AUC balance became weaker. I selected the HistGradientBoosting model because it had a better overall validation profile.

---

## 8. Explainability

For Task 2, I used **SHAP** to explain the final model. The most important global features were:

`age`, `workinghours`, `education`, `marital status_Husband`, and `sex_Female`.

These features are plausible for income prediction. Age, education, and working hours can be directly related to income. Marital status and gender-related features may capture social or demographic patterns in the data, although they also raise fairness concerns.

![Feature importance](../outputs/figures/feature_importance.png)

I also generated two local explanations:

- one correct `high` prediction from the validation set
- one correct `low` prediction from the validation set

I used validation examples because they have true labels. I did not use test examples for local explanations, since the test labels are unknown.

---

## 9. Final Prediction Output

For Task 3, I refit the final pipeline on all of `income.csv` and applied it to `income_test.csv`. The prediction output was written to `outputs/predictions.csv`.

Verification checks:

- The file contains exactly **2000 rows**.
- The columns are exactly `id,income`.
- The `id` order matches `predictions_template.csv`.
- The predicted labels are only `high` or `low`.
- There is no extra unnamed index column.

Prediction summary: the model predicted **1028** people as `high`, which is a rate of **0.514**. The remaining **972** people were predicted as `low`, with a rate of **0.486**.

Since `income_test.csv` has no labels, I cannot measure the real score on that file. My estimated performance is based on validation and cross-validation results. The final model reached validation AUC **0.854** and validation accuracy **0.784**, with usable precision and recall for both classes.

---

## 10. Gender Fairness

I evaluated gender fairness using the `sex` column on the validation set. The final model predicted `high` much more often for the male group than for the female group. Female positive prediction rate was **0.132**, while Male positive prediction rate was **0.386**. The positive prediction rate gap was **0.254**. I also tested a model variant without `sex`. That reduced the gap to **0.228**, but it did not remove the difference.

This is an important result. Fairness is not guaranteed just by removing the protected attribute. Other variables can act as proxies. To improve fairness, I would compare candidate models using fairness metrics during selection, inspect proxy variables more carefully, and test threshold adjustments on validation data. I did not tune group-specific thresholds in this assignment because I wanted the final prediction rule to stay simple and reproducible.

---

## 11. Conclusion

The final model for this assignment is HistGradientBoosting. It performed best overall with validation AUC **0.854**, while still keeping precision and recall at a reasonable level for both income classes. Hyperparameter tuning helped control overfitting, and the ablation experiments showed that removing high-missing columns or `sex` did not strongly change AUC.

SHAP showed that age, working hours, education, marital status, and gender-related features were important for the model. The final prediction file was generated successfully for all 2000 new people in `income_test.csv`.

The model is useful, but it is not perfectly fair. The positive prediction rate differs strongly between Female and Male groups. Removing `sex` helped slightly, but not enough. A better fairness-aware workflow would need to include fairness metrics directly during model selection or threshold selection.
