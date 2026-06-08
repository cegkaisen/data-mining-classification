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

