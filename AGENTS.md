# Proje Ajan Rehberi

## Iletisim

- Kullanici ile Turkce konus.
- Standart dosya adlari, kod tanimlayicilari (identifiers), komutlar, paket adlari ve teknik API adlari Ingilizce kalabilir.
- Onemli teknik terimleri Turkce anlatirken ilk kullanimda Ingilizcesini parantez icinde ver: baglam yonetimi (context management), ozellik secimi (feature selection), asiri uyum (overfitting).

## Proje Amaci

Bu proje Data Mining Assignment 4 kapsaminda gelir tahmini (income prediction) icin ikili siniflandirma (binary classification) calismasidir.

Ana hedefler:

- `income.csv` ile modeller egitmek ve degerlendirmek.
- En az iki model denemek; bunlardan en az biri ensemble model olmali.
- En az iki model icin asiri uyum (overfitting) analizi yapmak.
- En az bir asiri uyum azaltma teknigi (regularization, pruning, cross-validation, early stopping, feature selection vb.) uygulamak.
- Accuracy, AUC, precision ve recall metriklerini iki sinif icin raporlamak.
- Final model icin SHAP veya LIME ile aciklanabilirlik (explainability) analizi yapmak.
- `income_test.csv` icin tahmin uretip `predictions_template.csv` formatinda teslim dosyasi hazirlamak.
- Cinsiyet adaleti (gender fairness) acisindan model performansini tartismak.

## Calisma Ilkeleri

- Once baglami oku, sonra kod veya analiz degisikligi yap.
- Kullanici degisikliklerini koru; alakasiz dosyalari geri alma.
- Degisiklikleri kucuk, odakli ve assignment hedeflerine bagli tut.
- Deneyleri tekrar uretilebilir (reproducible) yap: sabit `random_state`, net veri bolme stratejisi ve kayitli metrikler kullan.
- Sonuclari yalnizca tek bir skorla degil; overfitting, fairness ve aciklanabilirlik baglaminda yorumla.

## Baglam Yonetimi

- Her onemli goreve `docs/ai/context.md` dosyasini okuyarak basla.
- Assignment gereksinimleri icin `docs/ai/project-brief.md` dosyasini kaynak al.
- Kalici kararlar `docs/ai/decision-log.md` dosyasina eklenmeli.
- Cok adimli islerde `docs/ai/task-template.md` kullan.
- Yeni dogrulama komutlari veya proje bulgulari `docs/ai/context.md` dosyasina eklenmeli.

## Varsayilan Workflow

1. Gorevi netlestir.
2. Ilgili baglami ve veri yuzeyini incele.
3. Deney planini kisa yaz.
4. On isleme (preprocessing) pipeline'ini kur.
5. Modelleri egit ve dogrula.
6. Overfitting, feature selection ve hyperparameter sonuclarini karsilastir.
7. Final modeli sec.
8. SHAP veya LIME analizi yap.
9. Test tahminlerini ve rapor bulgularini uret.
10. Sonuclari dogrula ve kisa ozetle.

## Guvenlik Kurallari

- Kullanici istemedikce commit, push veya pull request acma.
- Yikici komutlari kullanma.
- Bagimlilik kurulumu (dependency install) gerekiyorsa once nedenini acikla ve onay iste.
