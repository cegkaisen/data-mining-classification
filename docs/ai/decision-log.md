# Karar Kaydi

Bu dosya kalici muhendislik kararlarini (engineering decisions) kaydeder.

## Format

```text
YYYY-MM-DD - Karar basligi
Baglam:
Karar:
Gerekce:
Sonuclar:
```

## Kararlar

2026-06-08 - Proje incelemesi oncesi AI workflow iskeleti kuruldu
Baglam:
Kullanici, proje dosyalari okunmadan once baglam yonetimi ve AI destekli muhendislik icin temel dosyalarin olusturulmasini istedi.

Karar:
Hafif Markdown workflow dosyalari ve `AGENTS.md` rehberi olusturuldu.

Gerekce:
Bu, sonraki calismalar icin ortak bir calisma modeli sagladi ve kullanicinin dosya okumama talimatina uydu.

Sonuclar:
Ilk dosyalar proje bilgisi icermiyordu; assignment PDF'i ve veri dosyalari incelendikten sonra Turkce ve projeye ozel hale getirildi.

2026-06-08 - Workflow dili Turkceye alindi
Baglam:
Kullanici, dosyalarin Ingilizce olmasinin ozel bir sebebi olup olmadigini sordu ve fark yoksa Turkce kullanilmasini istedi.

Karar:
AI workflow ve baglam dosyalari Turkce yazilacak; kod, dosya adlari ve standart teknik adlar Ingilizce kalabilecek.

Gerekce:
Bu proje icin Turkce yazmak dogruluk veya verimlilik acisindan belirgin bir dezavantaj yaratmiyor; kullanici ile calisma dilini tutarli hale getiriyor.

Sonuclar:
`AGENTS.md`, `docs/ai/context.md`, `docs/ai/workflow.md`, `docs/ai/decision-log.md` ve ilgili workflow dosyalari Turkceye cevrildi.

2026-06-08 - Git hygiene ve PRD taslagi eklendi
Baglam:
Kullanici repository icin Git baslatti ve Git ile kalan temel islerin yapilmasini, ardindan proje icerigi ve PRD taslagi hazirlanmasini istedi.

Karar:
Kaynak veri ve assignment PDF'i takip edilebilir birakildi; uretilmis ciktilar, cache dosyalari, sanal ortamlar ve model artifact dosyalari `.gitignore` ile dislandi. PRD taslagi `docs/prd.md` olarak eklendi.

Gerekce:
Assignment projesinde ham veri ve PDF kucuk ve calisma icin kaynak niteliginde; buna karsilik notebook checkpointleri, output dosyalari ve model artifactleri tekrar uretilebilir ve repository'yi kirletebilir.

Sonuclar:
Repository, analiz kodu ve rapor kaynaklarini takip etmeye hazir; PRD grill session icin ilk tartisma zemini olustu.

2026-06-08 - `sex` kolonu icin fairness ablation karari kabul edildi
Baglam:
Assignment gender fairness tartismasi istiyor ve train verisinde `high` orani cinsiyete gore belirgin fark gosteriyor.

Karar:
Ana modelde `sex` kolonu kullanilacak; ayrica `sex` olmadan ablation experiment calistirilacak ve performans/fairness farklari raporlanacak.

Gerekce:
`sex` kolonunu sadece cikarmak fairness'i garanti etmez; diger degiskenler proxy olabilir. Kullanim ve cikarma senaryolarini sayisal olarak karsilastirmak daha savunulabilir bir rapor argumani verir.

Sonuclar:
Modelleme workflow'u iki final aday varyantini degerlendirecek: `sex` dahil ve `sex` haric. Rapor fairness bolumunde bu karsilastirmayi kullanacak.

2026-06-08 - Yuksek eksikli kolonlar icin missing-category ve ablation karari kabul edildi
Baglam:
`ability to speak english` ve `gave birth this year` kolonlarinda eksik deger orani cok yuksek, ancak eksik olma durumu model icin sinyal tasiyor olabilir.

Karar:
Bu iki kolon ana preprocessing pipeline'inda missing-category imputation ile tutulacak; ayrica kolonlar cikarilarak ablation experiment calistirilacak.

Gerekce:
Kolonlari bastan drop etmek potansiyel sinyali kaybettirebilir. Tutup ablation ile karsilastirmak feature selection tartismasi icin sayisal kanit saglar.

Sonuclar:
Model deneyleri, yuksek eksikli kolonlar dahil ve haric olacak sekilde karsilastirma icerecek.

2026-06-08 - Notebook ve hafif `src/` modulleriyle ilerleme karari kabul edildi
Baglam:
Assignment hem deneysel analiz hem de okunabilir kod gerektiriyor.

Karar:
Analiz ve rapor gorselleri notebooklarda tutulacak; tekrar eden preprocessing, evaluation ve fairness kodlari `src/` modullerine ayrilacak.

Gerekce:
Notebooklar rapor iterasyonunu hizlandirir, `src/` modulleri kod kalitesini ve tekrar kullanimi iyilestirir.

Sonuclar:
Calisma yapisi notebook + modul hibriti olarak ilerleyecek.

2026-06-08 - Model aday seti kabul edildi
Baglam:
Assignment en az iki model ve en az bir ensemble model gerektiriyor.

Karar:
Logistic Regression baseline, Random Forest ensemble, Gradient Boosting veya HistGradientBoosting ek guclu aday olarak kullanilacak. XGBoost gibi ek dependency isteyen modeller varsayilan kapsam disinda kalacak.

Gerekce:
Bu set rubrik gereksinimini karsilar, tabular data icin makul performans verir ve gereksiz kurulum riski yaratmaz.

Sonuclar:
Model deneyleri bu aday seti etrafinda tasarlanacak.

2026-06-08 - Final model secim kriterleri kabul edildi
Baglam:
Train verisinde sinif dagilimi dengesiz sayilabilir ve assignment accuracy disinda AUC, precision ve recall istiyor.

Karar:
Validation AUC birincil secim kriteri olacak; precision/recall dengesi, overfitting gap ve fairness metrikleri ikincil kriterler olacak.

Gerekce:
AUC threshold'dan bagimsiz karsilastirma saglar; diger metrikler final secimin tek boyutlu olmasini engeller.

Sonuclar:
Accuracy raporlanacak ama tek basina final model secimini belirlemeyecek.

2026-06-08 - Explainability icin SHAP birincil, LIME fallback kabul edildi
Baglam:
Assignment final model icin SHAP veya LIME ve en az iki bireysel tahmin aciklamasi istiyor.

Karar:
Final model tree-based ise SHAP birincil explainability yontemi olacak; SHAP uyumluluk sorunu cikarsa LIME fallback olarak kullanilacak.

Gerekce:
SHAP global ve lokal aciklamayi ayni cercevede saglar. LIME, uyumluluk sorunlarinda assignment sartini karsilayan makul fallback'tir.

Sonuclar:
Explainability workflow'u once SHAP uzerinden planlanacak.

2026-06-08 - Rapor once Turkce taslak, sonra Ingilizce final olacak
Baglam:
Kullanici final raporun once basit ogrenci diliyle Turkce yazilmasini, teknik terimlerin Ingilizce parantezle verilmesini ve teslimden once Ingilizceye cevrilmesini istedi.

Karar:
Ilk rapor taslagi Turkce yazilacak; final teslim asamasinda Ingilizce rapora cevrilecek.

Gerekce:
Turkce taslak kullanicinin icerigi daha iyi kontrol etmesini saglar; Ingilizce final assignment metni ve rubrikle uyumlu olur.

Sonuclar:
Rapor workflow'u iki asamali olacak: Turkce taslak, Ingilizce final.

2026-06-08 - Technical Design dokumani olusturuldu
Baglam:
PRD asamasi tamamlandi ve kullanici implementation'a gecmeden technical design / architecture asamasina gecmek istedi.

Karar:
`docs/technical-design.md` olusturuldu. Dokuman veri sozlesmesi, preprocessing tasarimi, modul sinirlari, notebook akisi, deney matrisi, explainability, fairness, output sozlesmeleri ve dogrulama stratejisini tanimlar.

Gerekce:
Implementation'a gecmeden once mimari akisin, sorumluluklarin ve cikti sozlesmelerinin netlesmesi kodun daha odakli ve tekrar uretilebilir yazilmasini saglar.

Sonuclar:
Sonraki implementation asamasi `docs/technical-design.md` dosyasini kaynak alacak. Kalan acik teknik sorular rapor dosya formati ve notebook execution tercihidir.

2026-06-08 - Overfitting azaltma stratejisi kabul edildi
Baglam:
Assignment en az bir overfitting azaltma teknigi uygulanmasini ve etkisinin raporlanmasini istiyor.

Karar:
Tree/ensemble modellerde complexity controls (`max_depth`, `min_samples_leaf`, `max_features` vb.) kullanilacak. Logistic Regression icin regularization (`C`) tune edilecek.

Gerekce:
Bu stratejiler model bazinda dogrudan uygulanabilir, metriklerle kolay karsilastirilabilir ve raporda acikca savunulabilir.

Sonuclar:
Overfitting bolumu train-validation gap ve complexity/regularization deneyleriyle desteklenecek.

2026-06-08 - Rapor kaynak formati Markdown olarak kabul edildi
Baglam:
Kullanici raporun once Turkce, sonra Ingilizce hazirlanmasini; PDF'in sadece Blackboard'a yukleme asamasinda uretilmesini istedi.

Karar:
Turkce taslak `reports/report_draft_tr.md`, Ingilizce final `reports/report_final_en.md` olarak Markdown formatinda tutulacak. PDF export son teslim asamasinda yapilacak.

Gerekce:
Markdown Git icin temiz, diff-friendly ve hizli duzenlenebilir bir kaynak formattir. PDF'i sona birakmak iterasyonu hizlandirir.

Sonuclar:
Rapor workflow'u Markdown kaynak dosyalari uzerinden ilerleyecek.

2026-06-08 - Architecture grill karar paketi kabul edildi
Baglam:
Technical design asamasinda notebook sayisi, validation stratejisi, preprocessing yapisi, output takibi, prediction dosyasi konumu ve rapor figurleri tartisildi.

Karar:
Uc notebook akisi, holdout + cross-validation hybrid validation, ortak preprocessing pipeline, generated outputs'un varsayilan olarak Git disinda kalmasi, final prediction'in `outputs/predictions.csv` olarak uretilmesi ve raporda az sayida guclu figur kullanilmasi kabul edildi. Final GitHub halinde gerekli outputlarin bulundugundan son checklist ile emin olunacak.

Gerekce:
Bu kararlar implementation'i sade, tekrar uretilebilir ve assignment rubrigiyle uyumlu tutar. Generated output'lari varsayilan olarak ignore etmek repository hijyenini korur; final artefactleri son asamada bilincli dahil etmek teslim eksigi riskini azaltir.

Sonuclar:
Technical design final GitHub checklist'i ile guncellendi.

2026-06-08 - Karar siniflandirma protokolu kabul edildi
Baglam:
Kullanici bundan sonraki kararlarda risk ve geri donus maliyetinin acik siniflandirilmasini istedi.

Karar:
Kararlar `Reversible decision`, `Costly decision` veya `Dangerous decision` olarak etiketlenecek.

Gerekce:
Bu siniflandirma, dusuk riskli kararlarin hizli gecilmesini; data leakage, grading failure veya ciddi scope creep yaratabilecek kararlarin ise daha dikkatli tartisilmasini saglar.

Sonuclar:
PRD'ye karar siniflandirma protokolu eklendi. Bundan sonraki grill session kararlarinda bu etiketler kullanilacak.

2026-06-08 - Data leakage guardrails kabul edildi
Baglam:
Architecture grill session'da preprocessing fit noktasi, test seti kullanim siniri, threshold secimi ve final model selection leakage riski tartisildi.

Karar:
Tum preprocessing sadece training split/fold icinde fit edilecek; validation/test uzerinde transform uygulanacak. `income_test.csv` sadece final prediction icin kullanilacak. Final threshold varsayilan olarak `0.5` olacak; threshold tuning yapilirsa yalnizca validation uzerinde yapilacak. Final model secimi sadece validation/CV sonuclarina dayanacak.

Gerekce:
Bu kararlar data leakage, yanlis evaluation ve grading failure riskini azaltir.

Sonuclar:
Technical design'a leakage prevention guardrails bolumu eklendi ve dogrulama checklist'i guncellendi.

2026-06-08 - Feature selection ve deney kapsam kararlari kabul edildi
Baglam:
Architecture grill session'da feature selection yeri, hyperparameter search kapsami, class imbalance stratejisi, explainability instance secimi ve rapor kanit butcesi tartisildi.

Karar:
Feature selection pipeline/fold icinde yapilacak. Hyperparameter search kucuk ve savunulabilir gridlerle sinirli kalacak. Class imbalance icin `class_weight="balanced"` varyanti denenecek, SMOTE varsayilan kapsam disinda kalacak. Local explanation icin validation setinden dogru `high` ve dogru `low` ornekleri secilecek; yer kalirsa bir hatali tahmin eklenecek. Rapor kanit butcesi 3 tablo + 3 figur olacak.

Gerekce:
Feature selection'in pipeline disinda yapilmasi data leakage yaratabilir. Kucuk grid ve `class_weight` deneyleri assignment icin yeterli metodolojik kanit saglar. Validation ornekleri explainability yorumunu ground truth ile destekler. Sinirli tablo/figur butcesi 4 sayfa rapor sinirini korur.

Sonuclar:
Technical design deney matrisi, explainability tasarimi, rapor tasarimi ve dogrulama checklist'i guncellendi.

2026-06-08 - Reproducibility ve source-of-truth kararlari kabul edildi
Baglam:
Architecture grill session'da notebook execution stratejisi, deney metriklerinin kaynagi, randomness kontrolu, rapor sayilari ve dependency stratejisi tartisildi.

Karar:
Uc notebook bagimsiz calisabilir olacak. Deney metriklerinin source of truth'u `outputs/*.csv` tablolari olacak. Tum split/model/tuning adimlarinda `random_state=42` veya esdeger seed kullanilacak. Rapordaki metrikler final oncesi generated CSV'lerle kontrol edilecek. Implementation icin `.venv` + `requirements.txt` ve minimum dependency seti kullanilacak.

Gerekce:
Bu kararlar reproducibility, rapor tutarliligi ve dependency risklerini azaltir.

Sonuclar:
Technical design'a reproducibility guardrails ve dependency strategy bolumleri eklendi.

2026-06-08 - Final training, ham veri koruma ve rapor iddia politikalari kabul edildi
Baglam:
Architecture grill session'in son paketinde final training strategy, model artifact policy, ham veri mutability, report claim policy ve implementation entry point tartisildi.

Karar:
Final model secildikten sonra pipeline tum `income.csv` uzerinde yeniden fit edilecek ve `income_test.csv` tahminlenecek. Ham veri dosyalari overwrite edilmeyecek. Model artifact varsayilan olarak kaydedilmeyecek. Raporda test accuracy iddia edilmeyecek; performans tahmini validation/CV uzerinden anlatilacak. Implementation `src/` temel modulleri ve `01_eda.ipynb` ile baslayacak.

Gerekce:
Bu kararlar reproducibility, grading safety ve kod organizasyonunu korur.

Sonuclar:
Technical design implementation-ready olarak isaretlendi.

2026-06-08 - Task breakdown reviewer onerileriyle revize edildi
Baglam:
Kullanici task breakdown taslagini skeptical reviewer gibi grill etmemi ve kabul edilen onerilere gore revize etmemi istedi.

Karar:
Task breakdown'a EDA sonrasi preprocessing refinement, initial data fairness summary, T5 milestone ayrimi, T6/T7 sinir netligi, final model selection memo, SHAP timebox + LIME fallback trigger, strict template id equality validation, rolling report notes ve sertlestirilmis submission checklist eklendi.

Gerekce:
Bu revizyonlar rapor kanitlarinin dagilmasini, data leakage riskini, final prediction format hatasini ve submission artefact eksigini azaltir.

Sonuclar:
`docs/task-breakdown.md` implementation oncesi daha uygulanabilir ve grading risklerine karsi daha guvenli hale geldi.

2026-06-08 - Commit checkpoint ve otonom commit izni
Baglam:
Kullanici task breakdown revizyonundan sonra commit checkpoint alinmasini ve bundan sonra gerektiginde Codex'in kendi yargisiyla commit alabilmesini istedi.

Karar:
Bu noktada bir Git checkpoint commit alinacak. Bundan sonraki anlamli, dogrulanmis asama sonlarinda Codex kendi yargisiyla commit alabilir.

Gerekce:
Planlama, PRD, technical design ve task breakdown asamalari artik implementation oncesi stabil bir checkpoint olusturuyor.

Sonuclar:
Gelecekteki commitler anlamli is birimleri tamamlandiginda, alakasiz degisiklikleri karistirmadan alinacak.
