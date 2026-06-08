# AI Destekli Muhendislik Workflow'u

## 1. Gorev Alimi

- Gorevin assignment'in hangi parcasina denk geldigini belirle: Task 1, Task 2, Task 3, rapor veya teslim hazirligi.
- Beklenen ciktiyi netlestir: notebook, script, grafik, metrik tablosu, PDF rapor veya prediction CSV.
- Riskli bir varsayim yoksa dogrudan ilerle.

## 2. Baglam Toplama

- Once `docs/ai/context.md` oku.
- Assignment ozeti icin `docs/ai/project-brief.md` oku.
- Teknik tasarim kararlari icin `docs/technical-design.md` oku.
- Sadece ilgili dosyalari incele.
- Veriyle ilgili degisikliklerde once kolonlar, eksikler, sinif dagilimi ve train/test farklarini kontrol et.

## 3. Deney Tasarimi

- Sabit `random_state` kullan.
- Validation stratejisini acik yaz: holdout, stratified split veya cross-validation.
- Baseline model ve ensemble model sec.
- Metrik setini sabitle: accuracy, AUC, precision, recall.
- Fairness metriklerini cinsiyet gruplarina gore planla.

## 4. Uygulama

- Preprocessing'i modelden ayri ve tekrar kullanilabilir pipeline olarak kur.
- Kategorik kolonlar icin encoding, sayisal kolonlar icin uygun scaling/imputation uygula.
- Deney sonuclarini tablo veya CSV olarak kaydet.
- Kod okunabilir, bolumlere ayrilmis ve tek satir degisikligiyle calistirilabilir olmali.

## 5. Overfitting ve Feature Selection

- En az iki model icin train ve validation performansini karsilastir.
- Overfitting azaltma teknigini uygulamadan once ve sonra metrikleri kaydet.
- Feature selection etkisini performans ve yorumlanabilirlik acisindan tartis.

## 6. Aciklanabilirlik

- Final modeli secmeden SHAP/LIME'a gecme.
- Global feature importance raporla.
- En az iki bireysel tahmini acikla.
- Aciklamalari model davranisi, veri ozetleri ve fairness bulgulariyla iliskilendir.

## 7. Test Tahminleri

- Final pipeline'i tum egitim verisiyle yeniden egit.
- `income_test.csv` icin tahmin uret.
- `predictions_template.csv` ile ayni `id`, `income` formatinda cikti kaydet.
- `high` tahmin sayisini ve oranini raporla.

## 8. Raporlama

- Rapor maksimum 4 sayfa olmali.
- Sekil ve tablolar az ama kanitlayici olmali.
- Her major karar sayisal sonuc veya ikna edici gerekceyle desteklenmeli.
- Rapor, GitHub repository linkini icermeli.

## 9. Dogrulama

- Kodun bastan sona calistigini dogrula.
- Prediction CSV satir sayisi 2000 olmali.
- Prediction CSV kolonlari `id,income` olmali.
- `income` degerleri yalnizca `high` veya `low` olmali.
- Raporun sayfa siniri kontrol edilmeli.

## Varsayilan Dongu

```text
Baglami oku -> Veriyi incele -> Deneyi tasarla -> Kodu yaz -> Metrikleri dogrula -> Bulgulari kaydet -> Raporla
```
