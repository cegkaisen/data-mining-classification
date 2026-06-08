# Data Mining Assignment 4 - Classification

Bu proje gelir tahmini (income prediction) icin ikili siniflandirma (binary classification) assignment calismasidir.

## Veri Dosyalari

- `income.csv`: egitim verisi ve `income` hedef kolonu.
- `income_test.csv`: tahmin uretilecek test verisi.
- `predictions_template.csv`: teslim tahmin dosyasi formati.
- `Data Mining Assignment 4 - Classification.pdf`: assignment aciklamasi.

## Calisma Yapisi

- `docs/ai/`: AI destekli muhendislik (AI-assisted engineering) baglam ve workflow dosyalari.
- `notebooks/`: kesifsel analiz (EDA), model deneyleri ve rapora girecek analizler.
- `src/`: tekrar kullanilabilir Python kodu.
- `outputs/`: uretilen metrikler, tahminler ve ara ciktilar.
- `outputs/figures/`: raporda kullanilacak gorseller.
- `reports/`: final rapor taslaklari ve PDF ciktisi.

## Ana Workflow

1. Veriyi incele ve preprocessing pipeline'i kur.
2. En az iki model egit; en az biri ensemble model olsun.
3. Overfitting, feature selection ve hyperparameter deneylerini kaydet.
4. Final modeli sec ve SHAP/LIME ile acikla.
5. `income_test.csv` icin prediction CSV uret.
6. Fairness analizini ve maksimum 4 sayfalik raporu tamamla.

Detayli AI workflow'u icin `docs/ai/workflow.md` dosyasina bak.
