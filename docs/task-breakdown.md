# Task Breakdown - Income Classification Assignment

## Amac

Bu dokuman, PRD ve technical design kararlarini uygulanabilir tasklara cevirir. Implementation bu sirayi takip etmeli; ancak her task sonunda uretilen kanitlar ve riskler kontrol edilmelidir.

## Task Siniflari

- Foundation task: Sonraki islerin saglam ilerlemesi icin altyapi veya ortak kod.
- Evidence task: Assignment/report icin sayisal veya gorsel kanit uretir.
- Delivery task: Final submission artefactleri, rapor ve GitHub hazirligi.
- Guardrail task: Data leakage, evaluation hatasi veya grading failure riskini azaltir.

## T1. Environment ve Project Bootstrap

Type:

- Foundation task.
- Guardrail task.

Goal:

- `.venv` kurulumunu ve dependency stratejisini implementation'a hazir hale getirmek.
- Proje import yapisinin calistigini dogrulamak.

Scope:

- `.venv` olustur.
- `requirements.txt` minimum dependency setini kullan.
- `src/` package yapisini hazirla.
- Import smoke test icin hafif kontrol ekle.

Evidence/report impact:

- Dogrudan rapor kaniti uretmez.
- Kodun tekrar calistirilabilirligi (reproducibility) icin temel kanittir.

Done criteria:

- Dependency kurulumu tamam.
- `src` modulleri import edilebilir.
- Ham veri dosyalarina dokunulmadi.

Risk:

- Dependency kurulumu sorun cikarabilir; SHAP sorununda LIME fallback korunmali.

## T2. Core Data and Preprocessing Modules

Type:

- Foundation task.
- Guardrail task.

Goal:

- Veri sozlesmesini ve preprocessing pipeline'ini leakage-safe sekilde kurmak.

Scope:

- `src/preprocessing.py`.
- Feature group tanimlari.
- `get_feature_groups(include_sex=True, include_high_missing=True)`.
- `build_preprocessor(...)`.
- `split_features_target(...)`.
- EDA sonrasinda preprocessing refinement pass.
- Ham veri overwrite edilmesini onleyen calisma disiplini.

Evidence/report impact:

- Missing-category imputation, one-hot encoding ve numeric preprocessing metodoloji bolumunde anlatilacak.

Done criteria:

- Full feature set, high-missing removed ve sex removed feature varyantlari uretilebilir.
- Preprocessing `Pipeline`/`ColumnTransformer` icinde fit edilecek sekilde tasarlanir.
- Train/test kolon uyumu kontrol edilebilir.
- T4 EDA bulgularindan sonra preprocessing varsayimlari tekrar kontrol edildi.

Risk:

- Dangerous: Preprocessing split disinda fit edilirse data leakage olur.

## T3. Evaluation, Metrics, and Fairness Utilities

Type:

- Foundation task.
- Evidence task.
- Guardrail task.

Goal:

- Model sonuclarini tek formatta hesaplamak ve CSV source-of-truth'a hazirlamak.

Scope:

- `src/evaluation.py`.
- `src/fairness.py`.
- Accuracy, AUC, class-level precision/recall.
- Train-validation gap.
- Group metrics: accuracy, precision, recall, positive prediction rate, error-rate gap.
- Model olmadan initial data fairness summary: `sex` bazli target distribution.

Evidence/report impact:

- Model comparison table.
- Overfitting summary.
- Fairness metrics table.

Done criteria:

- Metrikler tutarli schema ile DataFrame olarak uretilebilir.
- `sex` gruplarina gore fairness metrikleri hesaplanabilir.
- Model oncesi `sex` bazli target distribution ozetlenebilir.
- Rapor sayilari icin CSV source-of-truth altyapisi hazirdir.

Risk:

- Dangerous: Metrik hesaplama pozitif sinif (`high`) varsayimini yanlis kurarsa rapor yanlis yorumlanir.

## T4. EDA Notebook

Type:

- Evidence task.

Goal:

- Veriyi anlamak ve rapora girecek temel veri kanitlarini uretmek.

Scope:

- `notebooks/01_eda.ipynb`.
- Train/test schema kontrolu.
- Class distribution.
- Missing values.
- Numeric/categorical ozetler.
- `sex` bazli income dagilimi.
- Ilk fairness sinyali.

Evidence/report impact:

- Class distribution figure/table.
- Missingness table/figure.
- Gender-income distribution bulgusu.

Done criteria:

- Notebook bagimsiz calisir.
- EDA bulgulari `outputs/` veya notebook icinde rapora aktarilabilir halde olur.
- Ham veri degistirilmez.

Risk:

- Reversible: Fazla EDA figur uretmek rapor butcesini sisirebilir; notebookta kalabilir.

## T5. Baseline and Initial Model Experiments

Type:

- Evidence task.
- Guardrail task.

Goal:

- Baseline ve ensemble modelleri leakage-safe validation ile karsilastirmaya baslamak.

Scope:

- `src/modeling.py`.
- Milestone A: Logistic Regression baseline + Random Forest ensemble.
- Milestone B: Gradient Boosting veya HistGradientBoosting ek aday.
- Stratified holdout split.
- `random_state=42`.
- Initial metrics CSV.

Evidence/report impact:

- En az iki model ve en az bir ensemble requirement'i icin ana kanit.
- Model comparison table'in ilk versiyonu.

Done criteria:

- Milestone A tamam: Logistic Regression ve Random Forest calisir.
- Milestone B tamam: Gradient Boosting veya HistGradientBoosting calisir.
- Accuracy, AUC, precision/recall raporlanir.
- Sonuclar `outputs/model_comparison.csv` olarak uretilebilir.

Risk:

- Dangerous: Validation split veya preprocessing yanlis baglanirsa evaluation gecersiz olur.

## T6. Hyperparameter Tuning and Overfitting Analysis

Type:

- Evidence task.
- Guardrail task.

Goal:

- Overfitting'i acikca gostermek ve azaltma tekniklerinin etkisini sayisal kanitla raporlamak.

Scope:

- Kucuk gridler.
- Logistic Regression `C`.
- Random Forest complexity controls.
- Gradient/HistGradientBoosting complexity controls.
- Train vs validation metrics.
- `StratifiedKFold` tuning.
- Bu task sadece model complexity / regularization tuning kapsar; feature set ablation T7'de kalir.

Evidence/report impact:

- Overfitting reduction table.
- Train-validation gap yorumu.
- Hyperparameter tuning metodoloji gerekcesi.
- Rapor dili: overfitting reduction, model complexity veya regularization uzerinden anlatilir.

Done criteria:

- En az iki model icin overfitting analizi var.
- En az bir overfitting azaltma teknigi once/sonra etkisiyle gosterildi.
- `outputs/overfitting_summary.csv` uretildi.

Risk:

- Costly: Grid fazla genis olursa zaman ve rapor karmasasi yaratir.
- Dangerous: Tuning test setine bakarak yapilirsa grading failure riski dogar.

## T7. Feature Selection and Ablation Experiments

Type:

- Evidence task.
- Guardrail task.

Goal:

- Feature selection etkisini assignment gereksinimine uygun sekilde gostermek.

Scope:

- Full feature set.
- High-missing columns removed.
- `sex` removed.
- Feature selection varsa pipeline/fold icinde uygulanir.
- Ablation sonuclari karsilastirilir.
- Bu task model complexity tuning degil, feature set varyantlari olarak anlatilir.

Evidence/report impact:

- Feature selection/ablation table.
- Yuksek eksikli kolonlar ve fairness icin sayisal tartisma.
- Rapor dili: feature selection/ablation etkisi overfitting tuning'den ayri tutulur.

Done criteria:

- `outputs/ablation_summary.csv` uretildi.
- High-missing removed etkisi yorumlanabilir.
- `sex` removed etkisi fairness ve performance acisindan yorumlanabilir.

Risk:

- Dangerous: Feature selection pipeline disinda fit edilirse data leakage olur.

## T8. Class Imbalance and Final Model Selection

Type:

- Evidence task.
- Guardrail task.

Goal:

- Final modeli AUC birincil, precision/recall, overfitting gap ve fairness ikincil kriterleriyle secmek.

Scope:

- `class_weight="balanced"` varyantlari.
- Final candidate comparison.
- Threshold default `0.5`.
- Test seti kullanmadan model secimi.
- Final model selection memo.

Evidence/report impact:

- Final model selection table.
- Estimated performance claim icin validation/CV kaniti.
- Final model selection memo raporun model secimi omurgasini olusturur.

Done criteria:

- Final model secimi sayisal gerekceyle yapildi.
- `reports/final_model_selection_memo_tr.md` veya esdeger not hazirlandi.
- Accuracy, AUC, precision/recall iki sinif icin hazir.
- Test accuracy iddia edilmez.

Risk:

- Dangerous: Test prediction dagilimina bakarak model secmek methodological leakage yaratir.

## T9. Explainability Analysis

Type:

- Evidence task.

Goal:

- Final model icin global ve local explainability kanitlarini uretmek.

Scope:

- SHAP primary.
- LIME fallback.
- SHAP timebox: makul entegrasyon suresinde calismazsa LIME fallback'e gec.
- Permutation importance destekleyici kanit olabilir, ancak SHAP/LIME yerine gecmez.
- Global feature importance.
- Validation setinden dogru `high` ve dogru `low` prediction explanation.
- Yer kalirsa bir hatali prediction explanation.

Evidence/report impact:

- Feature importance figure/table.
- En az iki local explanation.
- Modelin neden boyle davrandigina dair rapor yorumu.

Done criteria:

- SHAP veya LIME output uretildi.
- En az iki bireysel tahmin aciklandi.
- Encoded feature isimleri rapor icin okunabilir hale getirildi.
- SHAP kullanilmadiysa fallback gerekcesi not edildi.

Risk:

- Reversible: Hangi iki instance'in secildigi sonradan degistirilebilir.
- Costly: SHAP uyumluluk sorunlari zaman alabilir; LIME fallback hazir tutulmali.

## T10. Final Training and Prediction Generation

Type:

- Delivery task.
- Guardrail task.

Goal:

- Final pipeline'i tum `income.csv` uzerinde fit edip `income_test.csv` icin prediction uretmek.

Scope:

- Final pipeline refit.
- `outputs/predictions.csv`.
- Prediction schema validation.
- Strict template id equality validation.
- Predicted `high` count/rate.

Evidence/report impact:

- Task 3 prediction teslimi.
- Test setinde kac kisinin `high` tahmin edildigi.

Done criteria:

- Prediction CSV 2000 satir.
- Kolonlar `id,income`.
- `id` template ile ayni.
- `id` sirasi ve degerleri `predictions_template.csv` ile birebir ayni.
- `income` yalnizca `high` veya `low`.
- Test accuracy iddia edilmedi.

Risk:

- Dangerous: Template formatini bozmak grading failure yaratabilir.

## T11. Report Drafting in Turkish

Type:

- Delivery task.
- Evidence task.

Goal:

- Bulgulari maksimum 4 sayfalik rapor taslagina donusturmek.

Scope:

- `reports/report_draft_tr.md`.
- `reports/report_notes_tr.md` rolling report notes.
- Basit ogrenci dili.
- Teknik terimler Ingilizce parantezle.
- En fazla 3 tablo + 3 figur.
- Validation/CV temelli performance estimate.
- Fairness discussion.

Evidence/report impact:

- Assignment rubriginin yazili karsiligi.

Done criteria:

- Her evidence task sonunda `reports/report_notes_tr.md` icine aday tablo/figur ve 2-3 cumlelik yorum eklendi.
- Task 1, Task 2, Task 3 kapsaniyor.
- Rapor sayilari generated CSV'lerle uyumlu.
- Test accuracy iddia edilmiyor.
- Fairness iyilestirme onerisi var.

Risk:

- Costly: Raporu cok gec yazmak bulgu secimini zorlastirir; model deneylerinden hemen sonra taslak baslamali.

## T12. English Final Report and Submission Readiness

Type:

- Delivery task.
- Guardrail task.

Goal:

- Turkce taslagi Ingilizce final rapora cevirmek ve submission checklist'i tamamlamak.

Scope:

- `reports/report_final_en.md`.
- PDF export son asamada.
- README final output yollarinin guncellenmesi.
- GitHub final artefact kontrolu.
- Blackboard submission checklist.

Evidence/report impact:

- Final Blackboard/GitHub teslim hazirligi.

Done criteria:

- Ingilizce rapor assignment/rubric ile uyumlu.
- Final prediction ve gerekli artefactler GitHub halinde mevcut.
- Rapor maksimum 4 sayfa olacak sekilde PDF'e cevrilebilir.
- Final checklist tamam.
- README GitHub repo linkini ve final output yollarini icerir.
- Final prediction GitHub halinde bulunur veya bilincli olarak nasil uretilecegi net yazilir.
- Final English Markdown bulunur.
- PDF export uretildi.
- PDF maksimum 4 sayfa.
- PDF dosya adi assignment formatina uygundur: `Lastname_Firstname-studentNumber.pdf`.

Risk:

- Dangerous: Final GitHub veya Blackboard submission artefact eksigi grading failure yaratabilir.

## Rolling Report Notes Policy

Her evidence task sonunda rapor notu uretilecek:

- T4: EDA bulgulari ve aday veri figuru/tablosu.
- T5: Initial model comparison yorumu.
- T6: Overfitting ve tuning yorumu.
- T7: Feature selection/ablation yorumu.
- T8: Final model selection memo.
- T9: Explainability yorumu.
- T10: Predicted `high` count/rate ve performance estimate notu.

Bu notlar `reports/report_notes_tr.md` icinde tutulacak ve T11 Turkce rapor taslaginin hammaddesi olacak.

## Onerilen Uygulama Sirasi

1. T1 Environment ve Project Bootstrap.
2. T2 Core Data and Preprocessing Modules.
3. T3 Evaluation, Metrics, and Fairness Utilities.
4. T4 EDA Notebook.
5. T5 Baseline and Initial Model Experiments.
6. T6 Hyperparameter Tuning and Overfitting Analysis.
7. T7 Feature Selection and Ablation Experiments.
8. T8 Class Imbalance and Final Model Selection.
9. T9 Explainability Analysis.
10. T10 Final Training and Prediction Generation.
11. T11 Report Drafting in Turkish.
12. T12 English Final Report and Submission Readiness.

## Gerekce

Bu sira once leakage-safe altyapiyi kurar, sonra rapora kanit ureten deneyleri calistirir, en sonda final prediction ve rapor teslimine gecirir. EDA ve model deneyleri ayrilir; boylece veri bulgulari, model karsilastirmasi, overfitting, feature selection, explainability ve fairness bolumleri raporda birbirine karismadan kullanilabilir.

En kritik kanit ureten tasklar:

- T4: Veri, missingness ve fairness baslangic kaniti.
- T5: Model comparison ve ensemble requirement kaniti.
- T6: Overfitting ve hyperparameter tuning kaniti.
- T7: Feature selection/ablation kaniti.
- T8: Final model selection ve estimated performance kaniti.
- T9: Explainability kaniti.
- T10: Task 3 prediction ve predicted high count/rate kaniti.
- T11/T12: Kanitlarin rapor ve teslim formuna donusmesi.
