# AI Baglam

Bu dosya AI destekli muhendislik (AI-assisted engineering) icin projenin calisan hafizasidir.

## Proje Ozeti

- Proje: Data Mining Assignment 4 - Classification.
- Problem: Demografik ve sosyoekonomik ozelliklerden yillik gelirin `high` veya `low` olarak tahmini.
- Gorev tipi: Ikili siniflandirma (binary classification).
- Egitim verisi: `income.csv`, 9000 satir ve 10 kolon.
- Test verisi: `income_test.csv`, 2000 satir ve 9 kolon.
- Teslim tahmin sablonu: `predictions_template.csv`, 2000 satir, `id` ve `income` kolonlari.
- Hedef kolon: `income`.
- Hedef siniflar: `low`, `high`.

## Assignment Gereksinimleri

- En az iki siniflandirma modeli denenmeli.
- En az bir model ensemble model olmali.
- En az iki model icin asiri uyum (overfitting) acikca incelenmeli.
- En az bir overfitting azaltma teknigi uygulanmali ve etkisi raporlanmali.
- Ozellik secimi (feature selection) teknikleri denenmeli ve performans etkisi tartisilmali.
- Hyperparameter optimizasyonu yapilmali.
- Metrikler: accuracy, AUC, her iki sinif icin precision ve recall.
- Final model icin SHAP veya LIME ile aciklanabilirlik (explainability) yapilmali.
- En az iki bireysel tahmin aciklanmali.
- Test setinde kac kisinin `high` olacagi tahmin edilmeli.
- Modelin beklenen dogrulugu ve bu tahminin dayanaklari tartisilmali.
- Cinsiyet adaleti (gender fairness) degerlendirilmeli ve iyilestirme yollari kisaca tartisilmali.
- Rapor en fazla 4 sayfa olmali.

## Veri Ozeti

- `income.csv` sinif dagilimi:
  - `low`: 5921 satir, yaklasik %65.79.
  - `high`: 3079 satir, yaklasik %34.21.
- Eksik degerler:
  - `ability to speak english`: train %95.52, test %94.75 eksik.
  - `gave birth this year`: train %78.42, test %71.90 eksik.
  - Diger kolonlarda eksik deger gorulmedi.
- Kategorik kolonlar:
  - `workclass`, `marital status`, `occupation`, `sex`, `ability to speak english`, `gave birth this year`.
- Sayisal kolonlar:
  - `age`, `education`, `workinghours`.
- Ilk fairness sinyali:
  - Train setinde `high` orani Female icin yaklasik %20.4, Male icin yaklasik %41.1.
  - Bu fark model degerlendirmesinde cinsiyet bazli metriklere bakmayi gerekli kiliyor.

## Onerilen Teknik Yaklasim

- Tekrar uretilebilir bir Python pipeline kullan.
- Train/validation veya cross-validation ile deneyleri ayir.
- Preprocessing icin `ColumnTransformer`, `SimpleImputer`, `OneHotEncoder` ve gerekirse `StandardScaler` kullan.
- Baseline model olarak Logistic Regression veya Decision Tree dusun.
- Ensemble model olarak Random Forest, Gradient Boosting veya HistGradientBoosting dusun.
- Overfitting icin train/validation skorlarini karsilastir.
- Overfitting azaltma icin model karmasikligini sinirla, regularization kullan veya feature selection dene.
- Fairness icin cinsiyet gruplarina gore accuracy, precision, recall, positive prediction rate ve error rate hesapla.
- Ayrintili teknik tasarim icin `docs/technical-design.md` kaynak alinacak.
- Technical design asamasi implementation-ready olarak isaretlendi.

## Bilinen Ortam Durumu

- Sistem Python ortaminda `pandas` mevcut.
- Baslangicta sistem Python ortaminda `sklearn` gorulmedi.
- Bundled runtime icinde PDF okumak icin `pypdf` mevcut.
- Modelleme asamasinda `scikit-learn`, `matplotlib`, `seaborn` ve SHAP/LIME ihtiyaci tekrar kontrol edilmeli.

## Acik Sorular

- Rapor ve kod hangi isimle teslim edilecek?
- GitHub repository hazir mi, yoksa sonra mi olusturulacak?
- Final Blackboard PDF dosya adi icin ogrenci bilgileri gerekli.

## Guncelleme Kurallari

- Sadece sonraki calismayi kolaylastiracak kalici bilgi ekle.
- Dogrulanan varsayimlari guncelle.
- Deney komutlari ve final metrikleri burada kisa sekilde kaydedilebilir.
