# Inter-Annotator Infrastructure & Reproducibility Pipeline — Faz 13-14

**Scriptler:** [`src/build_inter_annotator_sample.py`](../src/build_inter_annotator_sample.py), [`src/inter_annotator_stats.py`](../src/inter_annotator_stats.py), [`run_pipeline.py`](../run_pipeline.py), [`src/build_hash_manifest.py`](../src/build_hash_manifest.py), `tests/`

---

## 1. Faz 13 — Inter-Annotator Infrastructure

- `validation/inter_annotator_sample.csv`: **70 satır**, `data/processed/relations_event_level.csv`'den `(relation_family_top, extraction_method)` üzerinden stratifiye edilmiş örneklem. 14 boyun tamamı temsil ediliyor; nadir `extraction_method` kategorileri (`çıkarımsal_akrabalık`, `manuel_turkistan_ekleme`, `epitet_aktarım`) de dahil edildi, yalnızca baskın `açık_ilişki` değil.
- `docs/inter_annotator_protocol.md`: ikinci kodlayıcının nasıl çalışacağını (kör değerlendirme — `coder1_*` sütunları gizlenmeli), hangi alanları dolduracağını, sonrasında ne yapılacağını tarif ediyor.
- `src/inter_annotator_stats.py`: Cohen's kappa + Krippendorff's alpha (nominal, 2-rater) hesaplamaya hazır, ama **çalıştırıldığında gerçek ikinci kodlayıcı verisi olmadığını tespit edip `not_applicable` döndürüyor** (test edildi, doğrulandı). Sahte/simüle edilmiş bir güvenilirlik değeri **hiçbir yerde üretilmedi**.

## 2. Faz 14 — Reproducibility / Pipeline

- **`run_pipeline.py`** (repo kökü): 19 aşamayı sırayla çalıştıran orkestratör. `--all`, `--stage <ad>`, `--fast` (null model FAST mode), `--validate-only` (CI için, yalnızca audit+validate) destekliyor. Her aşama `logs/`'a timestamp'li log yazıyor, ilk hatada durup PASS/FAIL özeti veriyor (madde 80, 120). Test edildi: `--stage audit`, `--stage hash_manifest`, `--all --validate-only` — hepsi PASS.
- **`tests/`** (18 test, `pytest`): şema/referential-integrity (`test_canonical_schema.py`, 7 test), aggregation doğruluğu (`test_aggregation.py`, 3 test), network inşası (`test_networks.py`, 5 test), determinizm (`test_determinism.py`, 2 test — aynı seed'in Leiden ve double-edge-swap'ta birebir aynı sonucu ürettiğini doğruluyor). **18/18 PASS.**
- **`outputs/manifest_sha256.csv`**: `data/{raw,story_level,final,processed,derived}` ve ana `outputs/` alt dizinlerindeki **192 dosyanın** SHA-256 hash'i.
- **`requirements-lock.txt`**: `.venv`'deki tam paket sürümlerinin (`pip freeze`) dökümü, 42 paket.
- **`.github/workflows/validate.yml`**: push/PR'da `pytest` + `run_pipeline.py --all --validate-only` çalıştıran CI. Ağır null-model/sensitivity/robustness aşamaları **bilinçli olarak CI dışında** bırakıldı (madde 103) — bunlar geliştirme/analiz aşamaları, merge gate değil.

## 3. Bilinen Sınırlamalar

- `run_pipeline.py --all` (tam, `--fast` olmadan) bu oturumda uçtan uca test edilmedi — her aşama ayrı ayrı zaten çalıştırılıp doğrulanmıştı (Faz 1-12); orkestratörün kendisi yalnızca tekil aşamalarla (`audit`, `hash_manifest`, `validate-only`) test edildi. Tam bir uçtan-uca `--all` çalıştırması (~10-15 dakika, çoğunlukla null_models FULL mode'dan) henüz yapılmadı. **[Güncelleme 2026-09-19: yapıldı — `python run_pipeline.py --all` FULL mode'da iki kez çalıştırıldı, her seferinde 23/23 aşama PASS (~7 dk); bilimsel çıktılar birebir yeniden üretildi. Bkz. `reports/RELEASE_CHECKLIST.md` "Full End-to-End Pipeline Run" ve `docs/decision_log.md` DEC-016.]**
- Inter-annotator kappa/alpha **hesaplanamadı** (beklenen, gerçek ikinci kodlayıcı yok) — bu proje "tek kodlayıcı" durumunu şeffafça koruyor.
- `tests/` kapsamı temel düzeyde (18 test) — ör. web portal, figür/tablo script'leri için test yok (görsel çıktı test edilmesi zor).

## 4. Sıradaki Adım

Faz 15 (Web Portal) — büyük bir iş. Ardından Faz 16-21 (website validation, documentation, paper/thesis package, final validation, final reports).
