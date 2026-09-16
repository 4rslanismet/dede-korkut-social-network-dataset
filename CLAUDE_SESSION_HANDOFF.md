# CLAUDE SESSION HANDOFF

**Bu dosya, önceki konuşmaya erişimi olmayan yeni bir Claude Code oturumunun bu projeye kaldığı yerden devam edebilmesi için yazılmıştır.** Tüm sayılar bu checkpoint anında repository'deki gerçek dosyalardan programatik olarak doğrulanmıştır (aşağıda her sayının kaynağı gösterilmiştir). Yeni oturum, bu dosyayı okuduktan sonra kendi çalışmasına başlamadan önce aynı doğrulamayı (dosyaları açıp gerçek satır/değer saymayı) tekrar yapmalıdır — burada yazılanlar "doğrulanmış" olsa da, zamanla dosyalar değişmiş olabilir.

**Checkpoint zamanı:** bu commit'in oluşturulduğu an (bkz. `project_state.json` → `last_updated`).

---

## PROJECT IDENTITY

**Proje adı:** Dede Korkut Digital Humanities & Network Science Project (çalışma adı: *Dede Korkut Narrative Network Project — DKNN*, henüz repository adı değiştirilmedi).

**Kaynak talimat:** [`docs/MASTER_PROMPT.md`](docs/MASTER_PROMPT.md) — kullanıcının verdiği 147 maddelik tam "Complete Project Rebuild Master Prompt" bu dosyaya birebir kopyalanmıştır. **Bu proje hiçbir zaman "degree centrality hesaplama" ölçeğinde bir çalışma değildir.**

**Ana hedef:** Dede Korkut anlatılarındaki aktörler ve ilişkiler üzerinden akademik olarak savunulabilir, yeniden üretilebilir, çok katmanlı bir araştırma altyapısı üretmek:

- reproducible canonical dataset (`data/processed/`)
- social network analysis + complex network analysis
- multilayer/multiplex network analysis
- story-level network analysis (14 boy)
- actor–story bipartite analysis
- story similarity (henüz yapılmadı)
- community detection (Leiden/Louvain — **yapıldı**, bkz. aşağı)
- signed/directed network analysis (**yapıldı**)
- multilayer/versatility analysis (**yapıldı**)
- narrative-order + dynamic centrality analysis (**yapıldı**)
- null models (**Faz 7, şimdi başlıyor**), sensitivity analysis, structural robustness (**yapılmadı**)
- academic figures/tables (**yapılmadı**)
- interactive GitHub Pages portal (**yapılmadı**)
- reproducibility/evidence package (kısmen: `reports/`, `validation/`)
- article/thesis package (**yapılmadı**)

Repository, GitHub'da `4rslanismet/dede-korkut-social-network-dataset` — klonlandı, `main` dokunulmadı, tüm çalışma `claude-dk-rebuild` branch'inde.

---

## MASTER SCIENTIFIC RULES

Bu kurallar her yeni analiz adımında geçerlidir; hiçbiri şu ana kadar ihlal edilmedi, yeni oturum da bunlara uymalı:

1. Repository veya güvenilir mevcut veri tarafından desteklenmeyen bilgi **uydurulmayacak**.
2. LLM tahminiyle gender/faction/lineage/social status/narrative role/kinship/hostility/chronology gibi metadata üretilip ground truth gibi kullanılmayacak (bu yüzden `data/processed/nodes.csv`'de bu alanlar yok — veri desteklemiyor).
3. `data/raw/` immutable — hiç değiştirilmedi.
4. `data/final/` (legacy v3) sessizce overwrite edilmeyecek — tüm yeni veri `data/processed/` altında ayrı üretildi, `data/final/` dokunulmadı.
5. Entity merge yalnızca açık kanıt ve yüksek güvenle yapılır — şu ana kadar tam olarak **1 tane** otomatik merge yapıldı (aşağıda DEC-002).
6. Network centrality ≠ edebi önem. Bu ayrım her raporda açıkça belirtildi ve belirtilmeye devam edecek.
7. Community'lere keyfi kültürel/sosyolojik isim verilmedi — sayısal ID kullanılıyor (`leiden_community`, `louvain_community` sütunlarında tam sayı).
8. `narrative_order` (= `satir_no`) hiçbir yerde historical time olarak yorumlanmadı; kod ve dokümanlarda açıkça "narrative order within a story" olarak etiketlendi.
9-11. Person+group vs person-only, weighted vs unweighted, explicit vs inferred, all-relations vs core-social karşılaştırmaları **henüz yapılmadı** (Faz 8 — Sensitivity Analysis). `config/analysis.yaml` içinde bu varyantlar zaten listelenmiş durumda (`sensitivity.variants`), ama kod tarafı henüz yazılmadı.
12. Null-model/sensitivity tamamlanmadan güçlü bilimsel sonuç yazılmadı — tüm raporlarda "preliminary" / "pending sensitivity and statistical validation" ifadesi kullanıldı.
13. Negative/null sonuçlar gizlenmedi — örnek: signed structural balance analizi "not_applicable" olarak işaretlendi (13 üçgen < 15 eşik), zorla bir sonuç üretilmedi.
14. Metodolojik olarak uygulanamayan analiz "not applicable" olarak işaretlendi, sahte çıktı üretilmedi (yukarıdaki örnek + S01/Girizgah için degree centralization = `NaN`, n<3).

---

## EXECUTION ENVIRONMENT

Bu bilgiler checkpoint anında gerçek komutlarla doğrulanmıştır:

- **OS:** Windows 11 Pro N (win32), PowerShell 5.1
- **Repository absolute path:** `F:\Recovered_D2\v4gus\Computer Since Master\Articles\dede korkut ai`
- **Git:** repository var, aktif branch = `claude-dk-rebuild`, `main` branch'e hiç yazılmadı, hiçbir zaman push denenmedi (remote auth hazır değil / istenmedi)
- **Son commit (checkpoint öncesi):** `3840993` — "Add Phase 5 corpus-level metrics and centrality profiles; combined Phase 4-5 report"
- **Python:** 3.12.10, sanal ortam `.\.venv\` (repo kökünde, **git'e commit edilmedi**, `.gitignore`'da hariç tutuluyor)
- **Ortamı aktive etme:** Bu Windows makinesinde `git`/`python` PATH'e winget kurulumu sonrası düzgün yansımıyor olabilir; en güvenilir yöntem **doğrudan `.venv` içindeki python'u çağırmak**:
  ```powershell
  .\.venv\Scripts\python.exe src\<script>.py
  ```
  Eğer `git`/`python` komutları "tanınmıyor" hatası verirse, PATH'i şu şekilde tazele:
  ```powershell
  $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
  ```
  (Bu PowerShell tool çağrıları arasında kalıcı olmuyor, her komut bloğunun başında tekrar gerekebilir.)
- **Kurulu ana paketler (checkpoint anında doğrulandı, `pip list`):** pandas 3.0.5, numpy 2.5.3, networkx 3.6.1, python-igraph 1.0.0, leidenalg 0.12.0, scipy 1.18.1, matplotlib 3.11.2, plotly 7.1.0, scikit-learn 1.9.1, statsmodels 0.15.0, pyyaml 6.0.3, pytest 9.1.1, openpyxl 3.1.5, pyarrow 25.0.1 — hepsi `requirements.txt`'te.
- **Config dosyası:** [`config/analysis.yaml`](config/analysis.yaml) — seed=42, community algorithm/resolution/seed sayısı, null model n_random=1000, sensitivity varyant listesi, robustness stratejileri, node2vec parametreleri, multiple-testing yöntemi hepsi burada. **Yeni kod bu dosyadan okumalı, sayı hardcode etmemeli.**
- **`tests/` dizini henüz oluşturulmadı.** `requirements.txt`'te pytest var ama hiç test yazılmadı — bu açık bir eksik (Faz 14'te ele alınacak).

---

## COMPLETED PHASES

### PHASE 1 — Repository Audit ✅

**Amaç:** Repository'yi klonlayıp mevcut veriyi kör güvenmeden denetlemek.
**Script:** [`src/audit.py`](src/audit.py) → [`reports/audit_data.json`](reports/audit_data.json) → [`reports/01_repository_audit.md`](reports/01_repository_audit.md)

**Doğrulanan sonuçlar** (checkpoint anında `reports/audit_data.json`'dan yeniden okundu):
- README iddiası: 14 stories / 333 nodes / 628 edges / 85 narrative events → **hepsi programatik olarak doğrulandı, tutarlı**.
- **KRİTİK bulgu 1:** `data/story_level/` (toplam 633 satır) ile `data/final/` (edges+events toplam 713 satır) arasında **+80 satırlık belgelenmemiş fark**. 11/14 boy'da fark var. Dönüşüm mantığı hiçbir README'de yok.
- **KRİTİK bulgu 2:** `data/raw/dede korkut karakterler.xlsx` (13 sheet, `Source/Target/Weight/Type` şeması), `story_level`/`final` verisinin **doğrudan ham kaynağı değil** — satır sayıları ve şema uyuşmuyor. Gerçek ham kodlama kaynağı (hangi Dede Korkut edisyonu okunarak kodlandığı) repo'da yok → `validation/source_edition_metadata_required.md`.
- `iliski_turu`'nün %29.6'sı (`186/628`) "belirsiz".
- 1 node-adı → 2 farklı ID çakışması (`Begil'in Adamları`), 1 beklenmeyen self-loop, `boy` alanında yazım/büyük-küçük harf tutarsızlıkları (kozmetik).
- Node/edge/event bütünlüğü sağlam: 0 orphan, 0 missing endpoint, 0 duplicate node ID.

### PHASE 2 — Validation Framework ✅

**Scriptler:** [`src/validate.py`](src/validate.py), [`src/entity_resolution.py`](src/entity_resolution.py) → [`outputs/validation/*.csv`](outputs/validation/) (26 dosya + `summary.json`) → [`reports/02_data_quality_report.md`](reports/02_data_quality_report.md)

**Doğrulanan `outputs/validation/summary.json` (checkpoint anında yeniden okundu):**
```json
node:  duplicate_node_id=0, same_name_multiple_ids=2, capitalization_variants=0,
       empty_or_blank_node_name=0, whitespace_in_node_name=0, invalid_id_format=0
edge:  missing_source=0, missing_target=0, orphan_source_endpoint=0, orphan_target_endpoint=0,
       observed_relation_types=17, invalid_layer=0, invalid_polarity=0, invalid_weight=0,
       invalid_directionality=0, unexpected_self_loop=1, exact_duplicate_relationship_same_line=2,
       repeated_actor_pair_relation_pattern=114, duplicate_kayit_id=0
event: missing_actor=0, orphan_actor=0, unsupported_target=0, duplicate_kayit_id=0,
       duplicate_event_pattern=11
alias: duplicate_original_alias=248, alias_maps_to_multiple_targets=17,
       alias_target_not_in_node_table=73
```
- "exact_duplicate_relationship_same_line" (2 satır) incelendi → **gerçek hata değil**, kasıtlı olarak eklenmiş iki ayrı coğrafi-epitet kaydı (`DKR0814`/`DKR0815`), sadece ikisinin de `satir_no` boş olması nedeniyle testte yan yana düştü.
- "repeated_actor_pair_relation_pattern" (114 satır) → çoğunlukla meşru narratif tekrar (farklı `satir_no`), event-level/aggregated ayrımı tam bunun için var.
- `validation/entity_resolution_candidates.csv`: **18 satır** (1 yüksek-güven node çakışması + 17 düşük-güven alias çakışması).
- `validation/HUMAN_REVIEW_QUEUE.csv`: **75 madde** (entity_resolution:18, stale_alias_target:45, provenance_gap:11, unexpected_self_loop:1).

### PHASE 3 — Canonical Dataset ✅

**Script:** [`src/build_canonical.py`](src/build_canonical.py) → `data/processed/*.csv` → [`reports/03_canonical_dataset_report.md`](reports/03_canonical_dataset_report.md)

**Doğrulanan dosya/satır sayıları (checkpoint anında yeniden `pd.read_csv` ile sayıldı):**

| Dosya | Satır |
|---|---:|
| `data/processed/nodes.csv` | **332** (333 legacy − 1 merge) |
| `data/processed/aliases.csv` | 525 |
| `data/processed/stories.csv` | 14 |
| `data/processed/relations_event_level.csv` | **628** (hiç kayıp yok) |
| `data/processed/relations_aggregated.csv` | **376** (benzersiz yönsüz aktör çifti) |
| `data/processed/relation_taxonomy.csv` | 17 |
| `data/processed/provenance.csv` | 628 |
| `data/processed/validation_status.csv` | 27 |

**Metodolojik kararlar (bkz. `docs/decision_log.md`):**
- Tek merge: `begil_in_adamlari` → `begilin_adamlari` (DEC-002).
- Aggregation kuralı: **yönsüz** aktör çifti (DEC-003).
- Relation taxonomy: 17 `iliski_turu` → SOCIAL/KINSHIP/AUTHORITY/SEMANTIC/OTHER/UNCERTAIN (DEC-004) — bu **yorumlayıcı bir kategorileştirme**, ham veri gerçeği değil.
- Provenance eşleme: 571 `matched_unique` (%90.9), 53 `unmatched_provenance_gap` (%8.4, Faz 1'deki +80 satır farkının somut karşılığı), 4 `matched_ambiguous`.

### PHASE 4 — Network Construction ✅

**Scriptler:** [`src/networks.py`](src/networks.py), [`src/build_networks.py`](src/build_networks.py), [`src/story_networks.py`](src/story_networks.py) → [`docs/network_models.md`](docs/network_models.md), `outputs/networks/`, `outputs/matrices/`

G0–G11 (12 varyant) tanımlandı ve inşa edildi — tam tanımlar `docs/network_models.md`'de, kod `src/networks.py::NETWORK_DEFINITIONS`. Ayrıca:
- 14 story-level network (`outputs/networks/stories/S01.graphml`…`S14.graphml`, metrikler `data/derived/story_level_metrics.csv`)
- Actor×story bipartite (311 aktör × 14 boy, 399 incidence) + iki projeksiyon (`outputs/matrices/actor_projection_cooccurrence.csv`, `story_projection_shared_actors.csv`) — **degree inflation uyarısı `docs/network_models.md`'de açıkça yazılı**, bu projeksiyonlar centrality iddiası için kullanılmıyor.

### PHASE 5 — Descriptive Analysis ✅

**Script:** [`src/metrics.py`](src/metrics.py) → `outputs/statistics/corpus_network_metrics.csv`, `outputs/tables/centrality_*.csv`

**Doğrulanan G0/G9 satırları (checkpoint anında `outputs/statistics/corpus_network_metrics.csv`'den okundu):**

| network | n_nodes | n_edges | density | components | largest_component | reciprocity |
|---|---:|---:|---:|---:|---:|---:|
| G0_full | 311 | 376 | 0.0078 | 23 | 261 | — |
| G9_directed | 221 | 324 | 0.0067 | 13 (weak) | 194 | **0.358** |

(311 ≠ 332 canonical node sayısı çünkü 21 node yalnızca event tablosunda geçiyor, hiçbir edge'de yok — bu node'lar edge-tabanlı G0 grafiğinde izole kaldığı için graf nesnesinden çıkarılıyor, `data/processed/nodes.csv`'den değil.)

**Centrality bulgusu (ÖNEMLİ — nasıl yazılacağı):** G0/G1/G2/G9 varyantlarının hepsinde Salur Kazan ve Bamsı Beyrek en yüksek degree/betweenness/PageRank değerlerine sahip. **Bu "en önemli karakterler" olarak sunulmadı ve sunulmamalı.** Doğru çerçeveleme: *"Preliminary descriptive centrality result; pending sensitivity and statistical validation (Phase 7-8)."* Tüm mevcut raporlarda bu ihtiyat zaten uygulandı.

---

## PHASE 6 — ADVANCED NETWORK ANALYSIS ✅ TAMAMLANDI

**Rapor:** [`reports/06_advanced_network_analysis_report.md`](reports/06_advanced_network_analysis_report.md)

### Tamamlanan ve gerçek sonuçlarla doğrulanan alt-adımlar:

**1. Community Detection ✅** — [`src/communities.py`](src/communities.py), ağ: `G2_core_social` (309 node, 374 edge)
- Leiden (resolution=1.0, seed=42): **modularity=0.6950, 33 community**
- Louvain (seed=42): **modularity=0.7114, 34 community**
- Leiden vs Louvain ARI: **0.899** (yüksek uyum)
- 10 seed'lik stabilite testi: modularity_mean=0.6981 (std=0.0028), **mean pairwise ARI=0.908** (yüksek kararlılık)
- Resolution sensitivity (0.5–1.5): community sayısı 30→36, modularity 0.646→0.710 (monoton artış)
- **Uyarı:** graf 23 bileşenli (bağlantısız) olduğu için 33 community'nin önemli bir kısmı trivial olarak izole bileşenlerden oluşuyor; asıl anlamlı community yapısı 261-node'luk dev bileşen içinde aranmalı — bu nüans henüz hiçbir raporda yazılı değil, **yeni oturum bunu Faz 6 raporuna eklemeli**.
- Community bridge (participation coefficient, within-module degree): `outputs/tables/community_bridge_metrics_G2_core_social.csv`. En yüksek participation coefficient: **Aruz (0.778, 8 inter-community edge)** — İç Oğuz'a Dış Oğuz boyundaki "hain" figürü, makul bir bulgu ama henüz raporlanmadı.

**2. Signed Network Analysis ✅** — [`src/signed_and_directed.py`](src/signed_and_directed.py)
- `outputs/tables/signed_network_profile.csv`: pozitif/negatif degree, strength, oran. Salur Kazan: +59/−19 (oran 3.11).
- **Structural balance: "not_applicable"** — sadece 13 tanımlı-işaretli üçgen var (eşik: 15). Bu dürüstçe "not applicable" olarak işaretlendi, zorla sonuç üretilmedi (`outputs/statistics/signed_structural_balance.json`).

**3. Directed Network Analysis (kısmen) ✅** — aynı script
- Triadic census hesaplandı (`outputs/statistics/directed_triad_census_G9.json`, 16 triad tipi). HITS henüz ayrı raporlanmadı (kod `src/metrics.py`'de zaten var, `centrality_G9_directed.csv` içinde `hits_hub`/`hits_authority` sütunları mevcut).

**4. Multilayer Analysis ✅** — [`src/multilayer.py`](src/multilayer.py) → `outputs/tables/multilayer_profile.csv`
- 7 gözlenen layer: akrabalık, iletişim, kimlik, mekân, olay, otorite, çatışma.
- En çok layer'da aktif: **Salur Kazan (7/7 layer, participation coefficient 0.766)**, sonra Dede Korkut (6), Aruz/Uruz/Bayındır Han/vb. (5).

**5. Narrative-Order Analysis ✅** — [`src/narrative_order.py`](src/narrative_order.py) çalıştırıldı ve doğrulandı
- S01 (Girizgah) `not_applicable` (1 kayıt, eşik: 6); diğer 13 boy için early/middle/late pencere üretildi (`outputs/tables/narrative_order_windows.csv`).
- İç tutarlılık kontrolü: 12/13 boyda `cumulative_distinct_nodes`, Faz 4'ün bağımsız story-level node sayılarıyla birebir eşleşti; S03'te küçük bir sapma (47 vs 48) 2 eksik `satir_no` kaydıyla açıklandı.
- Çoğu boyda çatışma yoğunluğu early→late arttı (istatistiksel test yok, yalnızca betimleyici).

**6. Dynamic Centrality (exploratory) ✅** — aynı script, `outputs/tables/dynamic_centrality_trajectory.csv`
- Top-6 karakterin corpus-order'a göre kümülatif ilişki-örneği sayısı. Salur Kazan (156, çok-boylu) ve Bamsı Beyrek (64) corpus-çapında tekrar ederken, Tepegöz (28) ve Basat (27) neredeyse tamamen tek boyda (S09) yoğunlaşmış — "yüksek toplam derece" ile "corpus-çapında yaygınlık" arasındaki farkın somut kanıtı.

**Faz 6 özet raporu tamamlandı:** [`reports/06_advanced_network_analysis_report.md`](reports/06_advanced_network_analysis_report.md) — yukarıdaki tüm alt-adımları, 23-bileşen/trivial-community uyarısını (§1.4), HITS sonuçlarını ve descriptive-vs-exploratory sınıflandırma tablosunu (§7) içeriyor.

---

## KNOWN DATA / PROVENANCE LIMITATIONS (henüz çözülmedi, "çözülmüş" gibi gösterilmiyor)

1. **Raw source lineage eksik** — hangi Dede Korkut edisyonunun/transkripsiyonunun kodlandığı belli değil (`validation/source_edition_metadata_required.md`).
2. **story_level → final dönüşümü tam olarak yeniden üretilebilir değil** — +80 satırlık belgelenmemiş fark (Faz 1).
3. **53 final kaydı (`relations_event_level.csv`'nin %8.4'ü) provenance_gap** — `story_level`'daki orijinal satıra eşlenemedi (`data/processed/provenance.csv` → `source_row_status`).
4. **Relation taxonomy'de %29.6 "belirsiz"** — herhangi bir katman/relation-family analizinde kapsam sınırlaması olarak açıkça belirtilmeli.
5. **Collective/group aktörlerin (125/332 node) network metrikleri üzerindeki etkisi henüz test edilmedi** — Faz 8 (person-only vs person+group sensitivity) bekliyor.
6. **Inferred ilişkilerin (cikarma_yontemi≠açık_ilişki, 32/628 satır) etkisi henüz test edilmedi** — Faz 8 bekliyor.
7. **17 alias çakışması ve 73 "stale alias target" kaydı çözülmedi** — `needs_manual_validation` olarak açık bırakıldı, `validation/HUMAN_REVIEW_QUEUE.csv`'de.
8. Community partition'ın **anlamlı** kısmı yalnızca 261-node'luk dev bileşen içindir; 23 bileşenli graf otomatik olarak trivial "tek-node community"lere yol açar — **bu artık `reports/06_advanced_network_analysis_report.md` §1.4'te açıkça belgelendi**, ama community sonuçları kullanılan her yeni yerde (Faz 11 figürleri, web portal) bu uyarı tekrarlanmalı.
9. Signed structural balance analizi veri yetersizliği (13 üçgen < 15 eşik) nedeniyle "not_applicable" — ek relation kodlaması gelmeden tekrar denenmemeli.
10. Directed triadic census, ağın seyrekliği nedeniyle ezici çoğunlukla "003" (bağlantısız) tipte — null model karşılaştırması (Faz 7) olmadan motif-tipi yorum yapılmamalı.

---

## CURRENT EXACT POSITION

```text
CURRENT STATUS:
PHASES 1-6 COMPLETE

NEXT PHASE:
PHASE 7 — NULL MODELS / STATISTICAL VALIDATION

PHASES 1-6 ARE COMPLETE. DO NOT RESTART THEM UNLESS VALIDATION REVEALS A REAL ERROR.
```

---

## PHASE 7 — NEXT WORK

1. `src/null_models.py` yaz: `config/analysis.yaml` → `null_models.n_random` (1000) ve `null_models.model` (`configuration_model`) kullanarak degree-preserving randomizasyon.
2. Uygun network'lerde (öncelik: `G0_full`, `G1_person_only`, `G2_core_social`; anlamlıysa `G9_directed`) clustering, transitivity, degree assortativity, modularity (Leiden, resolution=1.0) için observed vs random ensemble karşılaştırması: `random_mean`, `random_std`, `z_score`, `percentile`, `empirical_p`.
3. Motif/triad enrichment yalnızca örneklem yeterliyse (bkz. Faz 6 §3.1 uyarısı — G9 triadic census'ta çoğu kategori çok düşük sayıda, dikkatli olunmalı).
4. FAST mode (`n_random` küçük, örn. 100) geliştirme sırasında, FULL mode (`n_random=1000`, config'teki değer) final sonuçlar için.
5. Seed `config/analysis.yaml::seed` (42) + her random deneme için türetilmiş alt-seed'ler kaydedilsin, raporlanabilir olsun.
6. Uygun olmayan kombinasyon varsa (örn. çok küçük/seyrek bir alt-ağda anlamlı z-score üretilemiyorsa) `not_applicable` olarak işaretle.

---

## REMAINING MASTER PLAN AFTER PHASE 6

Tam liste `docs/MASTER_PROMPT.md`'de; öncelik sırası (proje sahibinin verdiği faz numaralandırmasıyla, kendi phase raporu numaralandırmamızdan farklı olabilir — önemli olan iş sırası):

- **PHASE 7 — Null Models / Statistical Validation:** `config/analysis.yaml`'daki `null_models.n_random=1000`, `configuration_model` randomizasyonu; clustering/transitivity/assortativity/modularity/motif için observed vs random_mean/std/z-score/percentile/empirical-p. Henüz `src/null_models.py` yok.
- **PHASE 8 — Sensitivity / Robustness:** person+group vs person-only, weighted vs unweighted, all vs core-social, explicit vs explicit+inferred, group included/excluded, girizgah included/excluded; centrality stability (Spearman, Kendall tau, top-k overlap). `config/analysis.yaml` → `sensitivity.variants` zaten tanımlı. Henüz `src/sensitivity.py` yok.
- **PHASE 9 — Structural Robustness:** random/degree/betweenness-targeted node removal, giant component/connectivity eğrileri. `config/analysis.yaml` → `robustness` zaten tanımlı. Henüz `src/robustness.py` yok.
- **PHASE 10 — Motif/Triad (yalnızca uygunsa):** null modellerle motif enrichment.
- **PHASE 11 — Publication Figures (F01-F18 hedefi, master prompt madde 48):** henüz `src/visualization.py` yok, `outputs/figures/` boş.
- **PHASE 12 — Publication Tables (T01-T11, madde 49):** CSV + LaTeX. Henüz yok.
- **PHASE 13 — Inter-Annotator Infrastructure:** `validation/inter_annotator_sample.csv`, `docs/inter_annotator_protocol.md` — gerçek ikinci coder olmadan agreement değeri **üretilmeyecek**, sadece altyapı hazırlanacak.
- **PHASE 14 — Reproducibility/Pipeline:** `run_pipeline.py` (henüz yok), `tests/` (henüz yok), hash manifest (`outputs/manifest_sha256.csv`, henüz yok), `requirements-lock.txt` (henüz yok).
- **PHASE 15 — Web Portal:** `docs/` altında GitHub Pages sitesi (Home/Dataset/Methodology/Network Explorer/Stories/Characters/Layers/Communities/Similarity/Analysis/Evidence/Downloads/Reproduce/About). Henüz hiç başlanmadı — `docs/` şu an sadece `network_models.md`, `README_v2.md`, `README_v3.md`, `MASTER_PROMPT.md` içeriyor.
- **PHASE 16 — Website Validation:** henüz N/A (site yok).
- **PHASE 17 — Documentation:** `docs/data_dictionary.md`, `docs/relation_codebook.md`, `docs/methodology.md`, `docs/limitations.md` — **hiçbiri henüz yazılmadı** (network_models.md hariç). `DATASET_CARD.md`, `CITATION.cff`, `CHANGELOG.md`, `CONTRIBUTING.md` — **hiçbiri henüz yok**.
- **PHASE 18 — Paper Package:** `paper/` dizini **henüz yok**.
- **PHASE 19 — Thesis Package:** `thesis/` dizini **henüz yok**.
- **PHASE 20 — Final Validation/Release:** tüm sayıların (README, paper, thesis, canonical data) tutarlılığı henüz kontrol edilmedi (bu sistematik kontrol henüz yapılmadı çünkü paper/thesis/website henüz yok).
- **PHASE 21 — Final Reports:** `reports/FINAL_REBUILD_REPORT.md`, `reports/EXECUTIVE_SUMMARY.md`, `reports/RELEASE_CHECKLIST.md` — **hiçbiri henüz yok**.

---

## IMPORTANT FILES TO READ ON RESUME

Gerçek dosya adlarıyla, okuma sırasına göre:

1. `CLAUDE_SESSION_HANDOFF.md` (bu dosya)
2. `NEXT_TASK.md`
3. `docs/MASTER_PROMPT.md` (orijinal 147 maddelik tam talimat)
4. `config/analysis.yaml`
5. `reports/01_repository_audit.md`
6. `reports/02_data_quality_report.md`
7. `reports/03_canonical_dataset_report.md`
8. `reports/04_05_network_construction_and_descriptive_report.md`
9. `reports/06_advanced_network_analysis_report.md`
10. `docs/network_models.md`
11. `docs/decision_log.md`
12. `data/processed/*.csv` (canonical dataset — özellikle `nodes.csv`, `relations_event_level.csv`, `relations_aggregated.csv`, `relation_taxonomy.csv`)
13. `src/networks.py` (network tanımlarının tek kaynağı — `NETWORK_DEFINITIONS`)
14. `src/communities.py`, `src/signed_and_directed.py`, `src/multilayer.py`, `src/narrative_order.py` (Faz 6 kodu, referans için)
15. `project_state.json` (makine-okunabilir özet)

---

## IMPORTANT DECISIONS

Bkz. [`docs/decision_log.md`](docs/decision_log.md) — DEC-001'den başlayarak tüm metodolojik kararlar orada.

---

## SESSION CONTINUITY RULE

Bundan sonra her büyük faz tamamlandığında `CLAUDE_SESSION_HANDOFF.md`, `NEXT_TASK.md`, `project_state.json` güncellenecek. Bu üç dosya + `docs/decision_log.md`, projenin kalıcı session-memory/checkpoint sistemidir.
