# PRD Taslagi - Income Classification Assignment

## 1. Amac

Bu projenin amaci, `income.csv` verisini kullanarak bireylerin gelir sinifini (`high` veya `low`) tahmin eden, degerlendirilebilir, aciklanabilir ve raporlanabilir bir siniflandirma (classification) calismasi uretmektir.

Calismanin final ciktilari:

- Tekrar calistirilabilir analiz/modelleme kodu.
- En az iki modelin karsilastirmasi.
- Overfitting, feature selection ve hyperparameter tuning sonuclari.
- SHAP veya LIME ile explainability analizi.
- `income_test.csv` icin final prediction CSV.
- Maksimum 4 sayfalik final PDF rapor.

## 2. Kapsam

### Kapsamda

- Veri kesfi (EDA) ve veri kalitesi analizi.
- Eksik deger stratejisi.
- Kategorik degisken encoding.
- Sayisal degisken preprocessing.
- Baseline model.
- En az bir ensemble model.
- Overfitting analizi ve azaltma deneyi.
- Feature selection deneyi.
- Model secimi ve final model egitimi.
- Test seti tahmini.
- Gender fairness analizi.
- Rapor icin tablo ve grafik uretimi.

### Kapsam Disinda

- Production API veya web uygulamasi.
- Otomatik deployment.
- Gercek zamanli tahmin sistemi.
- Assignment gereksinimi olmayan ileri MLOps altyapisi.

## 3. Kullanici ve Degerlendiren

Birincil kullanici:

- Assignment'i tamamlayan ogrenci.

Degerlendiren:

- Data Mining dersi ogretim ekibi.

Degerlendirenin onem verdigi noktalar:

- Metodolojik gerekce.
- Metriklerle desteklenen sonuc analizi.
- Overfitting ve feature selection tartismasi.
- Explainability kalitesi.
- Fairness farkindaligi.
- Kodun okunabilir ve calistirilabilir olmasi.

## 4. Veri

Kaynak dosyalar:

- `income.csv`: 9000 satir, hedef kolon `income`.
- `income_test.csv`: 2000 satir, hedef kolon yok.
- `predictions_template.csv`: teslim formati.

Hedef siniflar:

- `high`
- `low`

Bilinen veri notlari:

- Train sinif dagilimi yaklasik %65.79 `low`, %34.21 `high`.
- `ability to speak english` ve `gave birth this year` kolonlarinda yuksek oranda eksik deger var.
- Gender fairness icin `sex` kolonu kritik bir analiz boyutu.

## 5. Fonksiyonel Gereksinimler

FR1. Sistem veriyi okuyabilmeli ve kolon tiplerini ayirmali.

FR2. Sistem eksik degerleri kontrollu bir preprocessing pipeline'i ile islemeli.

FR3. Sistem en az iki model egitmeli; modellerden en az biri ensemble model olmali.

FR4. Sistem her model icin accuracy, AUC, precision ve recall metriklerini uretmeli.

FR5. Sistem en az iki modelde train/validation farkina bakarak overfitting analizi yapmali.

FR6. Sistem en az bir overfitting azaltma teknigini denemeli ve etkisini kaydetmeli.

FR7. Sistem feature selection deneyi yapmali ve performans etkisini raporlamali.

FR8. Sistem final modeli secmeli ve secim gerekcesini metriklerle desteklemeli.

FR9. Sistem final model icin SHAP veya LIME explainability analizi uretmeli.

FR10. Sistem en az iki bireysel tahmin icin aciklama uretmeli.

FR11. Sistem `income_test.csv` icin `id,income` formatinda prediction CSV uretmeli.

FR12. Sistem test setindeki `high` tahmin sayisini ve oranini raporlamali.

FR13. Sistem gender fairness metriklerini hesaplamali ve yorumlamali.

FR14. Sistem rapora girecek tablo/grafikleri tekrar uretilebilir sekilde kaydetmeli.

## 6. Fonksiyonel Olmayan Gereksinimler

NFR1. Kod tekrar uretilebilir (reproducible) olmali; `random_state` sabitlenmeli.

NFR2. Kod okunabilir ve bolumlere ayrilmis olmali.

NFR3. Deney sonuclari raporda kullanilabilecek sekilde kaydedilmeli.

NFR4. Final prediction CSV assignment template'i ile uyumlu olmali.

NFR5. Rapor maksimum 4 sayfa olmali.

NFR6. Gereksiz buyuk ara dosyalar Git'e alinmamali.

## 7. Basari Kriterleri

- Kod bastan sona calisir.
- Prediction CSV 2000 satir icerir.
- Prediction CSV kolonlari tam olarak `id,income` olur.
- `income` degerleri sadece `high` veya `low` olur.
- En az iki model ve en az bir ensemble model raporlanir.
- Overfitting azaltma teknigi sayisal olarak tartisilir.
- Explainability bolumu global ve lokal aciklamalar icerir.
- Fairness bolumu cinsiyet bazli performans farklarini tartisir.
- Rapor 4 sayfayi asmaz.

## 8. Onerilen Teknik Tasarim

Notebook akisi:

1. `notebooks/01_eda.ipynb`
2. `notebooks/02_model_experiments.ipynb`
3. `notebooks/03_explainability_and_predictions.ipynb`

Modul akisi:

- `src/preprocessing.py`
- `src/modeling.py`
- `src/evaluation.py`
- `src/fairness.py`

Deney modeli adaylari:

- Logistic Regression veya Decision Tree baseline.
- Random Forest veya Gradient Boosting ensemble.
- Gerekirse HistGradientBoosting veya ExtraTrees.

## 9. Kritik Karar Matrisi

Bu bolum grill session icin baslangic pozisyonudur. Her karar icin bir varsayilan onerilir; tartisma bu varsayilanlari test etmelidir.

### K1. Calisma Formati

Status:

- Accepted.

Recommended default:

- Notebook + hafif `src/` modulleri. Analiz ve rapor gorselleri notebooklarda, tekrar kullanilan fonksiyonlar `src/` altinda.

Alternative option:

- Tamamen notebook agirlikli calisma.
- Tamamen script/pipeline agirlikli calisma.

Why:

- Assignment rapor odakli ve deneysel; notebooklar EDA, metrik tablolari ve grafikler icin hizli ilerletir.
- `src/` modulleri kod okunabilirligi rubrigini guclendirir ve tekrar eden preprocessing/evaluation kodunu temiz tutar.

Risk if wrong:

- Sadece notebook kullanirsak kod daginiklasabilir.
- Sadece script kullanirsak analiz ve rapor iterasyonu yavaslayabilir.

Accepted decision:

- Notebook + hafif `src/` modulleriyle ilerlenecek.
- Notebooklar analiz akisini ve rapor gorsellerini tasiyacak.
- Tekrar eden preprocessing, evaluation ve fairness kodlari `src/` altinda tutulacak.

### K2. Model Adaylari

Status:

- Accepted.

Recommended default:

- Logistic Regression baseline + Random Forest ensemble + Gradient Boosting/HistGradientBoosting ek aday.

Alternative option:

- Decision Tree baseline + Random Forest ensemble.
- ExtraTrees veya XGBoost benzeri daha ileri modeller.

Why:

- Logistic Regression yorumlanabilir ve iyi baseline verir.
- Random Forest ensemble gereksinimini karsilar ve non-linear iliskileri yakalar.
- Gradient boosting genellikle tabular classification icin guclu bir final adayidir.

Risk if wrong:

- Logistic Regression zayif kalirsa baseline fazla basit gorunebilir.
- Random Forest overfitting gosterebilir; tuning sart olur.
- XGBoost gibi ek bagimlilik isteyen modeller zaman ve kurulum riski yaratabilir.

Accepted decision:

- Logistic Regression baseline olarak kullanilacak.
- Random Forest ensemble model olarak kullanilacak.
- Gradient Boosting veya HistGradientBoosting guclu ek aday olarak denenecek.
- XGBoost gibi ek dependency isteyen modeller varsayilan kapsam disinda kalacak.

### K3. Final Model Secim Kriteri

Status:

- Accepted.

Recommended default:

- Birincil secim kriteri validation AUC; ikincil kriterler class-level recall/precision dengesi, overfitting gap ve fairness metrikleri.

Alternative option:

- Accuracy odakli secim.
- `high` sinifi recall odakli secim.
- Fairness-aware secim.

Why:

- Sinif dagilimi dengesiz sayilabilir; AUC threshold'dan bagimsiz daha saglam karsilastirma verir.
- Assignment precision/recall ve fairness istedigi icin tek metrikle secim yapmak zayif savunulur.

Risk if wrong:

- Sadece AUC'ye bakarsak belirli threshold'da `high` veya `low` sinif performansi kotu kalabilir.
- Sadece accuracy'ye bakarsak cogunluk sinifi avantajli olur ve rubrikte analiz zayif gorunur.

Accepted decision:

- Final model seciminde validation AUC birincil metrik olacak.
- Precision/recall dengesi, overfitting gap ve fairness metrikleri ikincil karar kriterleri olacak.
- Accuracy raporlanacak ama tek basina model secim kriteri olmayacak.

### K4. Eksikligi Yuksek Kolonlar

Status:

- Accepted.

Recommended default:

- `ability to speak english` ve `gave birth this year` kolonlarini once missing-category imputation ile tut; sonra ablation experiment ile bu kolonlari cikarmanin etkisini olc.

Alternative option:

- Kolonlari bastan drop etmek.
- Sadece impute edip ablation yapmamak.

Why:

- Eksiklik orani cok yuksek oldugu icin bu kolonlar riskli; ama eksik olma durumu kendisi sinyal tasiyor olabilir.
- Ablation, feature selection tartismasi icin sayisal kanit saglar.

Risk if wrong:

- Tutmak noise ve overfitting yaratabilir.
- Drop etmek faydali sinyali kaybettirebilir.
- Ablation yapmazsak rapordaki feature selection bolumu zayiflar.

Accepted decision:

- Iki kolon missing-category imputation ile ana pipeline'da tutulacak.
- Ayrica bu kolonlar cikarilarak ablation experiment calistirilacak.
- Sonuc feature selection ve overfitting tartismasinda kullanilacak.

### K5. `sex` Kolonunun Kullanimi

Status:

- Accepted.

Recommended default:

- `sex` kolonunu ana modelde kullan; ayrica `sex` olmadan bir fairness/ablation deneyi calistir ve farklari raporla.

Alternative option:

- `sex` kolonunu tamamen cikarmak.
- `sex` kolonunu kullanip sadece fairness metrikleriyle izlemek.

Why:

- Assignment gender fairness tartismasi istiyor; kolonu kullanmak ve kullanmamak arasindaki etkiyi olcmek daha guclu arguman verir.
- Sadece kolonu cikarmak fairness'i garanti etmez; diger degiskenler proxy olabilir.

Risk if wrong:

- `sex` kullanmak modelin disparate impact uretmesine katkida bulunabilir.
- `sex` cikarmak performansi dusurebilir ve fairness'i yine de iyilestirmeyebilir.
- Bu karari sayisal deney olmadan savunmak raporda zayif kalir.

Accepted decision:

- Ana modelde `sex` kolonu kullanilacak.
- Ayrica `sex` olmadan ablation experiment calistirilacak.
- Rapor, iki yaklasimin performans ve fairness etkisini karsilastiracak.

### K6. Overfitting Azaltma Stratejisi

Status:

- Accepted.

Recommended default:

- Tree/ensemble modellerde `max_depth`, `min_samples_leaf`, `max_features` gibi complexity controls kullan; Logistic Regression icin regularization gucunu tune et.

Alternative option:

- Feature selection ile overfitting azaltmaya odaklanmak.
- Cross-validation disinda ek azaltma teknigi yapmamak.

Why:

- Assignment en az bir overfitting azaltma teknigi istiyor; model complexity controls dogrudan ve kolay raporlanabilir.
- Feature selection ayrica denenmeli ama tek overfitting stratejisi olursa etkisi belirsiz olabilir.

Risk if wrong:

- Fazla sinirlama underfitting yaratabilir.
- Yetersiz sinirlama train skorunu sisirir ve validation performansini dusurur.

Accepted decision:

- Tree/ensemble modellerde complexity controls kullanilacak.
- Logistic Regression icin regularization (`C`) tune edilecek.
- Bu deneyler overfitting azaltma bolumunun ana kaniti olacak.

### K7. Explainability Yontemi

Status:

- Accepted.

Recommended default:

- Final model tree-based ise SHAP TreeExplainer/Explainer kullan; kurulum veya uyumluluk sorununda permutation importance + LIME fallback dusun.

Alternative option:

- LIME'i birincil yontem yapmak.
- Sadece model-native feature importance kullanmak.

Why:

- SHAP global ve lokal aciklamayi ayni cercevede verir; assignment'in iki prediction explanation istegine iyi uyar.
- LIME lokal aciklama icin kullanisli ama global feature importance hikayesi icin daha fazla is gerektirir.

Risk if wrong:

- SHAP kurulum/versiyon sorunlari zaman kaybettirebilir.
- LIME sonuc stabilitesi dusuk olabilir.
- Sadece feature importance kullanmak assignment'in SHAP/LIME sartini karsilamaz.

Accepted decision:

- Final model tree-based ise SHAP birincil explainability yontemi olacak.
- SHAP uyumluluk sorunu cikarsa LIME fallback olarak kullanilacak.
- Sadece model-native feature importance yeterli sayilmayacak.

### K8. Rapor Dili ve Hikayesi

Status:

- Revised and accepted.

Recommended default:

- Final rapor Ingilizce yazilsin. Ana hikaye: "accurate enough, checked for overfitting, interpretable, and fairness-aware".

Alternative option:

- Turkce rapor.
- Sadece model performansi odakli rapor.

Why:

- Assignment metni Ingilizce; rubrik ve teknik terimler Ingilizce raporda daha dogrudan karsilanir.
- Fairness ve explainability rubrikte ayri yer tuttugu icin sadece accuracy hikayesi yetersiz kalir.

Risk if wrong:

- Turkce rapor degerlendirme beklentisiyle uyumsuz olabilir.
- Sadece accuracy odakli rapor Task 2/Task 3 kalitesini zayif gosterir.

Accepted decision:

- Ilk rapor taslagi basit ogrenci diliyle Turkce yazilacak.
- Teknik terimler ilk kullanimda Ingilizce parantezle verilecek, ornegin aciklanabilirlik (explainability).
- Final teslimden once rapor Ingilizceye cevrilecek.
- Ana hikaye yine "accurate enough, checked for overfitting, interpretable, and fairness-aware" olacak.

### K9. Git'te Tutulacak Ciktilar

Status:

- Accepted.

Recommended default:

- Ham veri, assignment PDF'i, kod, notebooklar, PRD ve rapor kaynaklari Git'te tutulsun. Generated outputs ve model artifacts ignore edilsin; final prediction/report gerekirse son asamada bilincli eklenir.

Alternative option:

- Tum outputs dosyalarini Git'e almak.
- Ham veriyi Git'e almamak.

Why:

- Veri dosyalari kucuk ve assignment kaynagi; repository'yi calistirilabilir yapar.
- Generated outputs tekrar uretilebilir oldugu icin varsayilan olarak Git'i kirletmemeli.

Risk if wrong:

- Outputs takip edilirse repository hizla daginiklasir.
- Veri takip edilmezse baskasi repository'yi calistiramaz.

Accepted decision:

- Ham veri, assignment PDF'i, kod, notebooklar, PRD ve rapor Markdown kaynaklari Git'te tutulacak.
- Generated outputs, model artifacts ve ara rapor exportlari varsayilan olarak Git disinda kalacak.
- Final prediction/report dosyalari gerekiyorsa son asamada bilincli olarak eklenebilir.

## 10. Grill Session Baslangici

Grill session amaci, yukaridaki varsayilanlari savunmak veya degistirmek icin kararlari zorlamaktir.

## 11. Karar Siniflandirma Protokolu

Bundan sonraki teknik ve mimari kararlar uc siniftan biriyle etiketlenecek:

1. Reversible decisions:
   - Yanlis secilirse sonradan kolay degistirilebilir.
   - Ornek: output dosya adi, figur sayisi, rapor kaynak formatinin kucuk varyasyonlari.
2. Costly decisions:
   - Yanlis secilirse sonradan degistirmek zahmetlidir.
   - Ornek: notebook yapisi, modul sinirlari, model deney organizasyonu.
3. Dangerous decisions:
   - Yanlis secilirse data leakage, yanlis evaluation, security/privacy, grading failure veya ciddi scope creep yaratabilir.
   - Ornek: validation stratejisi, train/test karisimi, target leakage, final submission formatini bozma.

Dangerous kararlar kabul edilmeden once riskleri acikca yazilacak. Kullanici karari tam anlamazsa detayli aciklama istenmesi beklenir.

Ilk tartisma sirasi:

1. Final raporun hedef seviyesi: maksimum not mu, temiz yeterli teslim mi?
2. Eksik kolon karari: missing-category + ablation varsayilani yeterince guclu mu?
3. Final model seciminde AUC birincil metrik olmali mi?
4. SHAP'i birincil explainability yontemi yapma riskini kabul ediyor muyuz?
