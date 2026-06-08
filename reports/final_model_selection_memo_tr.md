# Final Model Selection Memo - Turkish Draft

## Secilen aday

Final aday: **HistGradientBoosting / tuned_full**.

## Sayisal gerekce

- Birincil metrik (primary metric) validation AUC idi: 0.854.
- Accuracy: 0.784.
- High precision/recall: 0.709 / 0.628.
- Low precision/recall: 0.817 / 0.866.

## Overfitting ve feature selection yorumu

Tuning (hyperparameter tuning) sadece training split uzerinde cross-validation ile yapildi. Validation split model secimi icin ayrik tutuldu. Train-validation AUC gap ozeti: HistGradientBoosting: AUC gap 0.043; Logistic Regression: AUC gap 0.017; Random Forest: AUC gap 0.056. Feature ablation deneylerinde full, high-missing removed ve sex removed varyantlari karsilastirildi. Son secim validation AUC, precision/recall dengesi, train-validation gap ve fairness gap birlikte dusunulerek yapildi.

## Class imbalance yorumu

Class weight balanced varyantlarinda en iyi validation AUC Random Forest icin 0.851 oldu. Bu varyant high recall 0.791 ile final adaydan yuksek recall verdi, fakat precision ve AUC dengesi daha zayif kaldigi icin final secim yapilmadi.

## Fairness notu

Final aday icin sex bazli positive prediction rate gap 0.254. Final model ailesinde full gap 0.254, sex removed gap 0.228. Bu, fairness (adalet) acisindan fark oldugunu ve sadece `sex` kolonunu cikarmanin fairness'i garanti etmedigini gosterir.

## Guardrail

`income_test.csv` final model secimi, tuning veya threshold belirleme icin kullanilmadi. Test accuracy iddia edilmeyecek; performans yorumu validation/CV sonuclarina dayanacak.
