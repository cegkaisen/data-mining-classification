# Assignment Proje Ozeti

## Kaynak

- Assignment dosyasi: `Data Mining Assignment 4 - Classification.pdf`
- Egitim verisi: `income.csv`
- Test verisi: `income_test.csv`
- Tahmin sablonu: `predictions_template.csv`

## Problem

Amac, bireylerin demografik ve sosyoekonomik ozelliklerinden yillik gelir sinifini tahmin eden bir ikili siniflandirma (binary classification) modeli gelistirmektir.

Hedef degisken:

- `income = high`: yillik gelir 50.000 dolar ustu.
- `income = low`: yillik gelir 50.000 dolar alti veya esit.

## Task 1 - Modelleme ve Degerlendirme

Gerekenler:

- Veri on isleme (preprocessing): eksik degerler, kategorik degisken encoding, gerekirse sayisal normalizasyon.
- En az iki farkli model.
- En az bir ensemble model.
- En az iki model icin overfitting analizi.
- En az bir overfitting azaltma teknigi.
- Feature selection denemeleri ve etkilerinin tartisilmasi.
- Hyperparameter optimizasyonu.
- Metrikler:
  - accuracy
  - AUC
  - iki sinif icin precision
  - iki sinif icin recall

## Task 2 - Aciklanabilirlik

Final model icin SHAP veya LIME uygulanmali.

Raporlanacaklar:

- Genel olarak en onemli ozellikler.
- En az iki tahmin icin bireysel aciklama.
- Aciklanabilirlik sonuclarinin model hakkinda ne gosterdigi.

## Task 3 - Yeni Veriye Uygulama

Final model `income_test.csv` uzerine uygulanmali.

Raporlanacaklar:

- Her yeni kisi icin `high` veya `low` tahmini.
- Modelin beklenen dogrulugu icin guvenilir tahmin.
- Test setinde kac kisinin `high` tahmin edildigi.
- Bu tahminlerin hangi faktorlerle desteklendigi.
- Cinsiyet adaleti (gender fairness) acisindan performans.
- Fairness iyilestirme onerileri.

Teslim tahmin dosyasi:

- `id`
- `income`

## Teslim

- Maksimum 4 sayfalik PDF rapor.
- Raporda GitHub repository linki.
- PDF dosya adi formati assignment metninde `Lastname_Firstname-studentNumber.pdf` olarak belirtilmis.
- PDF metnindeki teslim tarihi `21/05/2026`; mevcut calisma tarihi `2026-06-08` oldugu icin bu tarih gecmis gorunuyor.

## Rubrikten Cikan Oncelikler

- Yazim net ve kisa olmali.
- Metodoloji secimleri gerekcelendirilmeli.
- Sonuc analizi metriklerle desteklenmeli.
- Task 1, Task 2 ve Task 3 eksiksiz tamamlanmali.
- Kod okunabilir, belgelenmis ve tekrar calistirilabilir olmali.
