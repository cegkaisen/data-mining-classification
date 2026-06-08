# Technical Design - Income Classification Assignment

## 1. Amac

Bu dokuman, PRD'de tanimlanan assignment hedeflerini uygulanabilir bir teknik tasarima (technical design) cevirir. Bu asamada implementation yapilmaz; veri akisi, modul sinirlari, deney tasarimi, cikti sozlesmeleri ve dogrulama stratejisi netlestirilir.

## 2. Mimari Ozeti

Calisma notebook + hafif `src/` modulleri uzerine kurulacak.

```text
income.csv
  -> EDA
  -> preprocessing pipeline
  -> model experiments
  -> evaluation + overfitting analysis
  -> feature selection / ablation experiments
  -> final model selection
  -> explainability
  -> income_test.csv predictions
  -> Turkish report draft
  -> English final report
```

Ana dizin sorumluluklari:

- `notebooks/`: analiz akisi, deney sonuclari, rapora girecek grafikler.
- `src/`: tekrar kullanilabilir preprocessing, modeling, evaluation ve fairness fonksiyonlari.
- `outputs/`: uretilen metrikler, prediction dosyalari ve ara tablolar.
- `outputs/figures/`: rapor gorselleri.
- `reports/`: Turkce taslak ve final Ingilizce rapor.
- `docs/`: PRD, teknik tasarim ve AI workflow notlari.

## 3. Veri Sozlesmesi

Architecture decision:

- Decision class: Dangerous decision.
- Accepted: `income.csv`, `income_test.csv` ve `predictions_template.csv` asla overwrite edilmeyecek.
- Rationale: Ham veri kaynak gerceklik (source of truth) olarak korunmali.
- Risk: Orijinal veri degistirilirse reproducibility bozulur, teslim formati zarar gorebilir ve grading riski olusur.

### 3.1 Input Dosyalari

`income.csv`

- Egitim verisi.
- Hedef kolon: `income`.
- Beklenen hedef degerler: `high`, `low`.
- Beklenen satir sayisi: 9000.

`income_test.csv`

- Final tahmin verisi.
- Hedef kolon yok.
- Beklenen satir sayisi: 2000.

`predictions_template.csv`

- Final prediction format referansi.
- Beklenen kolonlar: `id`, `income`.
- Beklenen satir sayisi: 2000.

### 3.2 Kolon Gruplari

Sayisal ozellikler (numeric features):

- `age`
- `education`
- `workinghours`

Kategorik ozellikler (categorical features):

- `workclass`
- `marital status`
- `occupation`
- `sex`
- `ability to speak english`
- `gave birth this year`

Hedef (target):

- `income`

### 3.3 Data Validation Kurallari

Baslangic kontrolleri:

- Train setinde `income` kolonu olmali.
- Test setinde `income` kolonu olmamali.
- Train ve test feature kolonlari ayni olmali.
- `predictions_template.csv` kolonlari `id,income` olmali.
- Test satir sayisi prediction template satir sayisiyla ayni olmali.
- Final prediction degerleri yalnizca `high` veya `low` olmali.

## 4. Preprocessing Tasarimi

Preprocessing `sklearn` pipeline yapisi uzerine kurulacak.

### 4.1 Sayisal Pipeline

Recommended default:

- Missing value stratejisi: median imputation.
- Scaling: Logistic Regression icin `StandardScaler`; tree-based modeller icin zaruri degil ama ortak pipeline sadeligi icin uygulanabilir.

Risk:

- Scaling tree modellerine genelde zarar vermez ama gereksizdir.
- Ortak preprocessing pipeline'i model karsilastirmasini daha temiz hale getirir.

### 4.2 Kategorik Pipeline

Recommended default:

- Missing value stratejisi: `missing` kategorisiyle imputation.
- Encoding: `OneHotEncoder(handle_unknown="ignore")`.

Risk:

- Yuksek missing orani olan kolonlarda `missing` kategorisi baskin gelebilir.
- `handle_unknown="ignore"` test setindeki yeni kategorilerde hata riskini azaltir.

### 4.3 Ozel Kolon Kararlari

`ability to speak english` ve `gave birth this year`

- Ana pipeline'da missing-category imputation ile tutulacak.
- Ablation experiment'te iki kolon birlikte cikarilacak.

`sex`

- Ana modelde kullanilacak.
- Fairness ablation experiment'te cikarilacak.

## 5. Modul Tasarimi

### 5.1 `src/preprocessing.py`

Sorumluluk:

- Kolon gruplarini tanimlamak.
- Feature set varyantlarini uretmek.
- `ColumnTransformer` ve model pipeline icin preprocessing bileseni olusturmak.

Planlanan fonksiyonlar:

- `get_feature_groups(include_sex=True, include_high_missing=True)`
- `build_preprocessor(numeric_features, categorical_features, scale_numeric=True)`
- `split_features_target(df, target_col="income")`

### 5.2 `src/modeling.py`

Sorumluluk:

- Model adaylarini ve hyperparameter gridlerini tanimlamak.
- Pipeline olusturmak.
- Cross-validation veya holdout deneylerini calistirmaya yardimci olmak.

Planlanan fonksiyonlar:

- `get_model_specs(random_state=42)`
- `build_pipeline(preprocessor, model)`
- `get_param_grids()`

### 5.3 `src/evaluation.py`

Sorumluluk:

- Accuracy, AUC, precision, recall metriklerini hesaplamak.
- Train/validation farklarini overfitting analizi icin kaydetmek.
- Model karsilastirma tablolari uretmek.

Planlanan fonksiyonlar:

- `evaluate_classifier(model, X, y, split_name)`
- `classification_metrics_table(y_true, y_pred, y_proba)`
- `overfitting_summary(train_metrics, validation_metrics)`

### 5.4 `src/fairness.py`

Sorumluluk:

- `sex` gruplarina gore performans metrikleri hesaplamak.
- Positive prediction rate ve hata oranlarini karsilastirmak.
- `sex` dahil/haric ablation sonuclarini raporlamak.

Planlanan fonksiyonlar:

- `group_metrics(y_true, y_pred, y_proba, group_values)`
- `fairness_gap_table(group_metric_table)`

### 5.5 `src/reporting.py` Opsiyonel

Sorumluluk:

- Metrik tablolarini ve prediction ozetlerini kaydetmek.
- Rapor icin tekrar kullanilabilir tablo/grafik ciktilari uretmek.

Bu modul implementation sirasinda ihtiyac dogarsa eklenecek.

## 6. Notebook Tasarimi

Architecture decision:

- Decision class: Costly decision.
- Accepted: Uc notebook akisi kullanilacak.
- Rationale: Assignment task'lari EDA, modelleme ve final explainability/prediction adimlarina dogal bolunuyor.
- Risk: Yanlis bolunurse notebook state'i dagilabilir; `src/` modulleri ve net output sozlesmeleriyle azaltilecek.

Architecture decision:

- Decision class: Costly decision.
- Accepted: Uc notebook bagimsiz calisabilir olacak; ortak kod `src/` icinde tutulacak ve notebooklar birbirinin memory state'ine bagli olmayacak.
- Rationale: Bagimsiz notebooklar daha guvenilir ve tekrar calistirilabilir olur.
- Risk: State zinciri kurulursa notebooklar sira disi calistiginda kirilir ve reproducibility riski artar.

### 6.1 `notebooks/01_eda.ipynb`

Amac:

- Veriyi anlamak.
- Sinif dagilimi, eksik degerler, feature dagilimlari ve fairness sinyalini incelemek.

Beklenen ciktilar:

- Class distribution tablosu/grafigi.
- Missingness tablosu.
- `sex` bazli income dagilimi.
- Train/test kolon uyumu kontrolu.

### 6.2 `notebooks/02_model_experiments.ipynb`

Amac:

- Model adaylarini egitmek.
- Hyperparameter tuning yapmak.
- Overfitting ve feature selection/ablation deneylerini calistirmak.

Beklenen ciktilar:

- Model comparison table.
- Train vs validation metrics.
- Overfitting reduction table.
- High-missing-column ablation table.
- `sex` ablation table.

### 6.3 `notebooks/03_explainability_and_predictions.ipynb`

Amac:

- Final modeli secmek.
- SHAP veya LIME explainability calistirmak.
- Final test predictions uretmek.
- Fairness ozetini rapora hazirlamak.

Beklenen ciktilar:

- Global feature importance.
- En az iki local explanation.
- Final prediction CSV.
- Test setinde `high` tahmin sayisi ve orani.
- Fairness metrics table.

## 7. Deney Tasarimi

## 7.0 Leakage Prevention Guardrails

Architecture decisions:

- Decision class: Dangerous decision.
- Accepted: Tum preprocessing adimlari sadece training split/fold icinde fit edilecek; validation/test uzerinde sadece transform uygulanacak.
- Rationale: `SimpleImputer`, `OneHotEncoder`, scaler ve feature selection gibi adimlar validation/test bilgisini gorurse data leakage olusur.
- Risk: Yanlis uygulanirsa validation skorlari yapay olarak iyilesir ve rapor metodolojik olarak hatali olur.

- Decision class: Dangerous decision.
- Accepted: `income_test.csv` sadece final prediction icin kullanilacak; model secimi, tuning, threshold secimi veya feature selection icin kullanilmayacak.
- Rationale: Test seti yeni instance mantigini temsil eder; label olmasa bile test dagilimina gore karar almak metodolojik savunmayi zayiflatir.
- Risk: Test bilgisinin karar surecine sizmasi grading failure riski yaratabilir.

- Decision class: Costly decision.
- Accepted: Final class prediction icin varsayilan threshold `0.5` olacak. Threshold tuning yapilirse yalnizca validation uzerinde yapilacak ve raporda acikca belirtilecek.
- Rationale: Assignment label prediction istiyor; default threshold basit ve savunulabilir. Threshold tuning ekstra aciklama yuku getirir.
- Risk: Yanlis threshold secimi precision/recall/fairness dengesini bozabilir.

- Decision class: Dangerous decision.
- Accepted: Final model secimi yalnizca validation/CV sonuclarina gore yapilacak; `income_test.csv` prediction dagilimi final model secimini degistirmeyecek.
- Rationale: Test output dagilimina gore model secmek, label olmasa bile new data mantigini bozar.
- Risk: Rapor savunmasi zayiflar ve metodolojik hata olusur.

- Decision class: Dangerous decision.
- Accepted: Feature selection, preprocessing ve model ile ayni `Pipeline` icinde yapilacak; CV/validation fold disinda fit edilmeyecek.
- Rationale: Feature selection hedef (`income`) bilgisini kullanabilir. Split disinda yapilirsa validation bilgisi karar surecine sizabilir.
- Risk: Data leakage olur; feature selection sonuclari ve model skorlari yapay iyilesebilir.

### 7.1 Validation Stratejisi

Architecture decision:

- Decision class: Dangerous decision.
- Accepted: Hizli deneyler icin stratified %80/%20 holdout, hyperparameter tuning icin `StratifiedKFold`.
- Rationale: Holdout hizli iterasyon, cross-validation ise daha stabil tuning kararlari saglar.
- Risk: Yanlis validation tasarimi data leakage veya yaniltici model secimi yaratabilir. Preprocessing sadece training fold/split icinde fit edilecek.

Recommended default:

- Ilk deneyler icin stratified holdout split.
- Hyperparameter tuning icin `StratifiedKFold`.

Varsayilan:

- `random_state = 42`
- Validation split: %20
- Scoring: AUC birincil, accuracy ve class-level precision/recall rapor metrikleri.

Why:

- Holdout hizli iterasyon saglar.
- Stratified split sinif dagilimini korur.
- Cross-validation tuning kararlarini daha stabil yapar.

Risk:

- Sadece tek holdout split kararlar icin oynak olabilir.
- Cross-validation tum deneylerde kullanilirsa sure uzayabilir.

### 7.2 Model Deney Matrisi

Architecture decision:

- Decision class: Costly decision.
- Accepted: Hyperparameter search scope kucuk ve savunulabilir gridlerle sinirli tutulacak.
- Rationale: Assignment icin amac maksimum leaderboard skoru degil; metodolojik, okunabilir ve raporlanabilir deneydir.
- Risk: Cok genis search zaman ve rapor karmasasi yaratir; cok dar search tuning'i zayif gosterebilir.

Baseline:

- Logistic Regression.

Ensemble:

- Random Forest.
- Gradient Boosting veya HistGradientBoosting.

Overfitting azaltma:

- Random Forest icin `max_depth`, `min_samples_leaf`, `max_features`.
- Gradient/HistGradientBoosting icin `max_iter`, `learning_rate`, `max_leaf_nodes` veya benzeri complexity controls.
- Logistic Regression icin regularization (`C`).

Feature/ablation deneyleri:

- Full feature set.
- High-missing columns removed.
- `sex` removed.

Class imbalance deneyleri:

- Once class imbalance metriklerle izlenecek.
- Logistic Regression ve Random Forest icin `class_weight="balanced"` varyanti deney olarak eklenecek.
- SMOTE/resampling varsayilan kapsam disinda kalacak.

Architecture decision:

- Decision class: Costly decision.
- Accepted: Class imbalance icin `class_weight="balanced"` varyanti denenecek; SMOTE kullanilmayacak.
- Rationale: Veri dagilimi dengesiz ama asiri degil; `class_weight` dusuk maliyetli ve raporlanabilir bir deneydir. SMOTE ekstra karmasiklik ve leakage riski yaratir.
- Risk: `class_weight` precision'i dusurebilir; hic denenmezse `high` recall zayif kalabilir.

### 7.3 Final Model Secimi

Secim sirasi:

1. Validation AUC.
2. `high` ve `low` icin precision/recall dengesi.
3. Train-validation gap.
4. Fairness gap.
5. Explainability uygunlugu.

Final karar raporda sayisal tabloyla gerekcelendirilecek.

### 7.4 Final Training Strategy

Architecture decision:

- Decision class: Dangerous decision.
- Accepted: Final model secildikten sonra ayni preprocessing/model pipeline tum `income.csv` uzerinde yeniden fit edilecek; sonra `income_test.csv` tahminlenecek.
- Rationale: Final prediction icin tum labeled data'dan yararlanmak mantiklidir. Performans tahmini validation/CV metriklerinden gelmelidir.
- Risk: Validation metrikleri yerine test accuracy iddia etmek grading riski yaratir; validation'da fit edilmis modeli kullanmak egitim verisinin bir kismini bosa birakir.

## 8. Explainability Tasarimi

Primary:

- Final model tree-based ise SHAP.

Fallback:

- SHAP uyumluluk sorunu olursa LIME.

Global explanation:

- En onemli feature'lar siralanacak.
- Gerekirse encoded feature isimleri insan-okur hale getirilecek.

Local explanation:

- En az iki test veya validation instance secilecek.
- Tercihen biri `high`, biri `low` tahmininden secilecek.
- Aciklamalar basit rapor diliyle yorumlanacak.

Architecture decision:

- Decision class: Reversible decision.
- Accepted: Local explanation icin validation setinden biri dogru `high`, biri dogru `low` prediction secilecek; yer kalirsa bir hatali tahmin ornegi eklenecek.
- Rationale: Validation setinde ground truth oldugu icin aciklamalar dogru/yanlis baglaminda yorumlanabilir.
- Risk: Test instance aciklamak mumkun ama ground truth olmadigi icin rapor yorumu daha zayif olur.

Risk:

- One-hot encoded feature isimleri raporda fazla teknik gorunebilir.
- SHAP output formatlari model tipine gore degisebilir.

Mitigation:

- Feature names temizleme yardimci fonksiyonu kullan.
- SHAP sorununda LIME fallback calistir.

## 9. Fairness Tasarimi

Protected attribute:

- `sex`

Grup bazli metrikler:

- Accuracy.
- Precision.
- Recall.
- Positive prediction rate.
- False positive rate veya false negative rate, uygulanabilirse.

Karsilastirmalar:

- Ana model: `sex` dahil.
- Ablation model: `sex` haric.

Rapor yorumu:

- Fairness'in sadece `sex` kolonunu cikarmakla garanti olmadigi belirtilecek.
- Performans/fairness trade-off sayisal olarak tartisilacak.

## 10. Output Sozlesmeleri

Architecture decision:

- Decision class: Reversible decision.
- Accepted: Generated outputs varsayilan olarak Git disinda kalacak; final GitHub halinde gerekli outputlar bilincli olarak dahil edilecek.
- Rationale: Ara ciktilar repository'yi kirletmemeli, ancak final submission/reproducibility icin gerekli prediction/report artefactleri eksik kalmamali.
- Risk: Finalde gerekli outputlar eklenmezse GitHub teslimi eksik gorunebilir. Son teslim checklist'i bunu kontrol edecek.

Architecture decision:

- Decision class: Costly decision.
- Accepted: Deney metriklerinin source of truth'u notebook output'u degil, `outputs/*.csv` tablolari olacak.
- Rationale: CSV tablolar tekrar kullanilabilir, rapora aktarilabilir ve final checklist ile dogrulanabilir.
- Risk: Metrikler sadece notebook hucrelerinde kalirsa stale output veya manuel kopyalama hatasi riski artar.

### 10.1 Metrics Outputs

Onerilen dosyalar:

- `outputs/model_comparison.csv`
- `outputs/overfitting_summary.csv`
- `outputs/ablation_summary.csv`
- `outputs/fairness_metrics.csv`

Varsayilan olarak `.gitignore` nedeniyle generated outputs Git'e alinmaz. Final GitHub halinde gerekli outputlar, ozellikle final prediction ve rapor artefactleri, son teslim checklist'iyle bilincli olarak eklenecek.

### 10.2 Prediction Output

Onerilen dosya:

- `outputs/predictions.csv`

Architecture decision:

- Decision class: Reversible decision.
- Accepted: Final prediction dosyasi `outputs/predictions.csv` olarak uretilecek.
- Rationale: Prediction dosyasi generated artifact oldugu icin `outputs/` altinda tutulmasi daha temizdir.
- Risk: Teslim sirasinda dosya yolu karisabilir; README ve final checklist'te dosya yolu acik yazilacak.

Sozlesme:

- Kolonlar: `id`, `income`
- Satir sayisi: 2000
- `id`: `predictions_template.csv` ile ayni
- `income`: sadece `high` veya `low`

### 10.3 Figures

Onerilen dosyalar:

- `outputs/figures/class_distribution.png`
- `outputs/figures/missing_values.png`
- `outputs/figures/model_comparison.png`
- `outputs/figures/feature_importance.png`
- `outputs/figures/fairness_comparison.png`

Architecture decision:

- Decision class: Reversible decision.
- Accepted: Rapor icin az sayida guclu figur kullanilacak: class distribution, missing values, model comparison, feature importance, fairness comparison.
- Rationale: 4 sayfa sinirinda her figur dogrudan kanit degeri tasimali.
- Risk: Fazla figur raporu sisirir; az figur analiz zayif gorunebilir.

### 10.4 Model Artifact Policy

Architecture decision:

- Decision class: Reversible decision.
- Accepted: Model artifact (`.joblib`, `.pkl`) varsayilan olarak kaydedilmeyecek; prediction ve metrikler koddan yeniden uretilebilir olacak.
- Rationale: Assignment model artifact istemiyor; binary artifact yonetimi gereksiz karmasiklik yaratir.
- Risk: Artifact yoksa tekrar prediction uretmek biraz daha uzun surer; artifact varsa gereksiz binary dosya yonetimi dogar.

## 11. Rapor Tasarimi

Iki asamali rapor workflow'u:

1. Turkce taslak:
   - Basit ogrenci dili.
   - Teknik terimler parantez icinde Ingilizce.
   - Bulgular ve kararlar once Turkce netlestirilir.
   - Kaynak dosya: `reports/report_draft_tr.md`.
2. Ingilizce final:
   - Teslimden once Turkce taslak Ingilizceye cevrilir.
   - Assignment rubrigiyle uyum kontrolu yapilir.
   - Kaynak dosya: `reports/report_final_en.md`.
3. Blackboard teslim:
   - Final Markdown rapor PDF'e cevrilir.
   - PDF export son asamada yapilir.

Maksimum 4 sayfa icin onerilen bolumler:

- Problem and data.
- Methods and experimental setup.
- Results, overfitting, and feature selection.
- Explainability, test predictions, and fairness.

Evidence budget:

- En fazla 3 tablo.
- En fazla 3 figur.
- Fazla detay notebooklarda kalacak.

Architecture decision:

- Decision class: Reversible decision.
- Accepted: Rapor icin hedef kanit butcesi 3 tablo + 3 figur olacak.
- Rationale: 4 sayfa sinirinda her tablo/figur dogrudan argumana hizmet etmeli.
- Risk: Fazla kanit raporu sisirir; az kanit analiz zayif gorunebilir.

### 11.1 Report Claim Policy

Architecture decision:

- Decision class: Dangerous decision.
- Accepted: Raporda test accuracy iddia edilmeyecek; "estimated performance based on validation/CV" dili kullanilacak. Test seti icin yalnizca predicted `high` count/rate raporlanacak.
- Rationale: `income_test.csv` label icermiyor. Performans tahmini validation/CV ve veri dagilimi incelemesine dayanmalidir.
- Risk: Label olmayan test seti icin kesin accuracy iddia etmek metodolojik hata ve grading riski yaratir.

## 12. Dogrulama Stratejisi

Implementation sonrasi calistirilacak kontroller:

- Import smoke test.
- Notebook execution veya script-level end-to-end run.
- Leakage guardrail review.
- Prediction CSV schema validation.
- Metrics output validation.
- Report page count validation.
- Randomness/seed check.
- Report numbers vs generated CSV consistency check.

Minimum acceptance checks:

- Prediction CSV 2000 satir.
- Prediction CSV kolonlari `id,income`.
- Prediction degerleri `high` veya `low`.
- En az iki model sonucu kayitli.
- En az bir ensemble model sonucu kayitli.
- Fairness metrics uretildi.
- Explainability output uretildi veya fallback gerekcesi kayitli.
- Final GitHub halinde gerekli outputlar ve rapor kaynaklari bulunuyor.
- Preprocessing ve feature selection pipeline icinde fit ediliyor; validation/test bilgisini onceden gormuyor.
- `income_test.csv` model secimi veya tuning icin kullanilmadi.
- Feature selection varsa pipeline/fold icinde uygulandi.
- Tum split/model/tuning adimlarinda `random_state=42` veya esdeger seed kullanildi.
- Rapordaki metrikler generated CSV source of truth ile uyumlu.

## 12.1 Final GitHub Checklist

Final GitHub halinde bulunmasi gerekenler:

- Source code ve notebooks.
- `reports/report_draft_tr.md`.
- `reports/report_final_en.md`.
- Final prediction CSV: `outputs/predictions.csv` veya teslim icin yeniden adlandirilmis final dosya.
- Rapor PDF'i, eger GitHub linki teslim aninda final artefact gostermeli ise.
- README'de calistirma ve final output yolu.

Not:

- `.gitignore` generated outputs'u varsayilan olarak dislar. Final artefactler gerekiyorsa son asamada bilincli `git add -f` veya `.gitignore` istisnasi ile eklenir.

## 12.2 Reproducibility Guardrails

Architecture decisions:

- Decision class: Dangerous decision.
- Accepted: Tum split, model ve tuning adimlarinda `random_state=42` kullanilacak; `numpy` veya Python `random` kullanilirsa seed sabitlenecek.
- Rationale: Assignment metrikleri ve final prediction tekrar uretilebilir olmali.
- Risk: Seed sabitlenmezse rapordaki sayilar ve final prediction yeniden calistirmada degisebilir.

- Decision class: Dangerous decision.
- Accepted: Rapordaki tum metrikler generated CSV source of truth'tan alinacak; final oncesi rapor sayilari CSV ile kontrol edilecek.
- Rationale: Manuel kopyalama hatalari rapor ve output metrikleri arasinda celiski yaratabilir.
- Risk: Rapor sayilari ile deney ciktilari celisirse grading sirasinda guven kaybi olusur.

## 12.3 Dependency Strategy

Architecture decision:

- Decision class: Costly decision.
- Accepted: Implementation icin `.venv` + `requirements.txt` kullanilacak; minimum dependency setiyle ilerlenecek. SHAP sorun cikarirsa LIME fallback kullanilacak. XGBoost varsayilan kapsama alinmayacak.
- Rationale: Izole ortam dependency ve surum riskini azaltir. Minimum dependency seti kurulumu daha basit ve savunulabilir tutar.
- Risk: Global Python kullanilirsa "bende calisiyor" problemi dogabilir; fazla dependency uyumluluk ve kurulum riskini artirir.

## 12.4 Implementation Entry Point

Architecture decision:

- Decision class: Costly decision.
- Accepted: Implementation'a once `src/` temel modulleri ve `notebooks/01_eda.ipynb` ile baslanacak; sonra `notebooks/02_model_experiments.ipynb`, en son `notebooks/03_explainability_and_predictions.ipynb`.
- Rationale: Once modul iskeleti ve EDA kurmak preprocessing, metrik ve rapor akisini temiz tutar.
- Risk: Direkt model notebookuna atlanirsa preprocessing ve evaluation kodu dagilabilir.

## 13. Teknik Riskler

Risk: `scikit-learn` sistem ortaminda mevcut olmayabilir.

- Mitigation: `.venv` kur ve `requirements.txt` kullan. Kurulum icin kullanici onayi gerekebilir.

Risk: SHAP kurulum veya uyumluluk problemi.

- Mitigation: LIME fallback.

Risk: Notebooklar daginiklasabilir.

- Mitigation: Tekrar eden kodu `src/` modullerine cikar.

Risk: 4 sayfa rapor siniri asilir.

- Mitigation: Tablolari ozetle, sadece en kanitlayici figurleri kullan.

Risk: Fairness tartismasi fazla yuzeysel kalir.

- Mitigation: `sex` dahil/haric ablation ve grup metriklerini rapora koy.

## 14. Acik Teknik Sorular

- Su an architecture seviyesinde acik teknik soru yok.

## 15. Implementation Readiness

Status:

- Ready for implementation.

Implementation baslamadan once kaynak alinacak dosyalar:

- `docs/prd.md`
- `docs/technical-design.md`
- `docs/ai/context.md`
- `docs/ai/workflow.md`

Ilk implementation hedefi:

- `.venv` hazirligi.
- `src/` temel modulleri.
- `notebooks/01_eda.ipynb`.
