# Rolling Report Notes

## T4 - EDA bulgulari

- Train verisi 9000 satir ve 10 kolondan olusuyor; test verisi 2000 satir ve 9 kolondan olusuyor.
- Hedef sinif dagilimi: low 0.658, high 0.342.
- En yuksek eksik deger oranlari `ability to speak english` ve `gave birth this year` kolonlarinda goruldu; bu T7 ablation deneyi icin kanit saglar.
- `sex` bazinda high income orani Female icin 0.204, Male icin 0.411; bu fairness (gender fairness) tartismasi icin baslangic sinyalidir.

## T5 - Initial model comparison

- Initial model deneylerinde Logistic Regression, Random Forest ve HistGradientBoosting modelleri ayni full feature set ile karsilastirildi.
- Birincil metrik AUC olarak tutuldu; en yuksek validation AUC HistGradientBoosting modelinde 0.846 olarak goruldu.
- Bu sonuclar final model secimi degildir; T6-T8 tuning, ablation ve fairness analizleri sonrasi karar verilecektir.
- `income_test.csv` bu asamada model secimi veya threshold belirlemek icin kullanilmadi.

## T6 - Hyperparameter tuning ve overfitting

- Tuning (hyperparameter tuning) sadece training split uzerinde 3-fold StratifiedKFold ile yapildi; validation split final karsilastirma icin ayrik tutuldu.
- En iyi validation AUC HistGradientBoosting / tuned_full icin 0.854 olarak goruldu.
- AUC train-validation gap ozeti: HistGradientBoosting: AUC gap 0.043; Logistic Regression: AUC gap 0.017; Random Forest: AUC gap 0.056.

## T7 - Feature ablation

- High-missing kolonlari cikarilan en iyi varyant Random Forest ile validation AUC 0.853 verdi.
- `sex` cikarilan en iyi varyant Random Forest ile validation AUC 0.853 verdi.
- Final model ailesinde positive prediction rate gap full icin 0.254, sex removed icin 0.228; bu fairness karsilastirmasi icin ayrica saklandi.
- Bu sonuclar feature selection (ozellik secimi) ve fairness tartismasi icin kanit olarak saklandi.

## T8 - Class imbalance ve final model selection

- Class weight balanced varyantlarinda en iyi validation AUC Random Forest icin 0.851 oldu.
- Balanced varyant Random Forest high recall 0.791 ile daha yuksek recall verdi, ancak final aday AUC dengesinde daha iyi kaldi.
- Final aday HistGradientBoosting / tuned_full olarak secildi; validation AUC 0.854, high recall 0.628.
- Final aday icin validation setinde sex bazli positive prediction rate gap 0.254; fairness (adalet) tartismasinda bu sayi kullanilacak.
- `income_test.csv` model secimi, tuning veya threshold belirleme icin kullanilmadi.

## T9 - Explainability

- Final model icin explainability (aciklanabilirlik) validation seti uzerinde uretildi; `income_test.csv` aciklama veya model secimi icin kullanilmadi.
- SHAP kullanildi.
- Global feature importance `outputs/explainability_global_importance.csv` ve `outputs/figures/feature_importance.png` olarak uretildi.
- Local explanation dosyalari dogru high ve dogru low validation prediction icin uretildi.

## T10 - Final prediction

- Final pipeline tum `income.csv` uzerinde refit edildi ve `income_test.csv` icin `outputs/predictions.csv` uretildi.
- Predicted high count/rate: 1028 / 0.514; predicted low count: 972.
- Test accuracy iddia edilmedi; test setinde label olmadigi icin performans yorumu validation/CV sonuclarina dayaniyor.
