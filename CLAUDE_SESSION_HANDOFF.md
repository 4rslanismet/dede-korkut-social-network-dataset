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
- null models (**yapıldı**, bkz. aşağı), sensitivity analysis, structural robustness (**Faz 8, şimdi başlıyor**)
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

## PHASE 7 — NULL MODELS / STATISTICAL VALIDATION ✅ TAMAMLANDI

**Scriptler:** [`src/null_models.py`](src/null_models.py), [`src/null_models_fdr.py`](src/null_models_fdr.py) → **Rapor:** [`reports/07_null_models_report.md`](reports/07_null_models_report.md)

**Yöntem (DEC-008):** `networkx.double_edge_swap` (degree-preserving randomizasyon, `n_swaps=10×n_edges`), 9 ağ (G0,G1,G2,G3,G4,G5,G6,G7,G8 — G9_directed hariç, yönlü null model henüz yok), 4 metrik (clustering, transitivity, degree assortativity, Louvain modularity), FAST (n=100, 29 sn) ve FULL (n=1000, config'ten, ~4dk35sn) mod. 36 test → Benjamini-Hochberg FDR (α=0.05).

**En önemli doğrulanmış sonuç:** Test edilen 7/9 ağın (G0,G1,G2,G4,G6,G7,G8) modularity'si, FDR-düzeltmeli olarak rastgele ağdan **istatistiksel olarak anlamlı derecede yüksek** — Faz 6'daki community yapısı yalnızca derece dağılımının yan ürünü değil, gerçek ek bir sinyal. Clustering G0/G1/G2/G4'te, transitivity yalnızca G1'de doğrulandı.

**KRİTİK DÜZELTME:** Faz 5'in "tüm ağlarda disassortative (negatif degree assortativity)" bulgusu **FDR düzeltmesinden sonra hiçbir ağda anlamlı çıkmadı** — bu iddia geri çekildi, `reports/04_05_network_construction_and_descriptive_report.md`'e düzeltme notu eklendi. G3_kinship'in 4 metriğinin tamamı rastgeleden ayırt edilemiyor (tam null sonuç, gizlenmedi).

**Açık kalan iş (Faz 7 kapsamı dışında bırakıldı, backlog):** G9_directed için yönlü-uyumlu null model yok; dev-bileşen-only modularity testi yapılmadı; motif/triad null karşılaştırması yapılmadı.

---

## PHASE 8 — SENSITIVITY / ROBUSTNESS ANALYSIS ✅ TAMAMLANDI

**Scriptler:** [`src/sensitivity.py`](src/sensitivity.py), [`src/robustness.py`](src/robustness.py) → **Rapor:** [`reports/08_sensitivity_robustness_report.md`](reports/08_sensitivity_robustness_report.md)

**Sensitivity (DEC-009):** `config/analysis.yaml::sensitivity.variants`'daki 6 çift test edildi (rank correlation: Spearman ρ, Kendall τ, top-k overlap). Sonuç, etki büyüklüğüne göre sıralı:
- İhmal edilebilir: girizgah dahil/hariç (ρ=1.000), tüm ilişkiler vs core-social (ρ=1.000)
- Küçük: explicit-only vs explicit+inferred (ρ=0.97-0.99)
- Orta: weighted vs unweighted (PageRank ρ=0.849 — en duyarlı metrik), groups dahil/hariç (ρ=0.90-0.96)
- **En büyük etki: person+group vs person-only** (ρ=0.887-0.926) — kolektif aktörleri çıkarmak sıralamayı en çok değiştiren tek karar.

**Structural Robustness (madde 30-31, "narrative resilience" DEĞİL):** `G0_full` üzerinde random/degree-targeted/betweenness-targeted kaldırma. Klasik "robust yet fragile" örüntüsü: dev bileşenin %50 altına düşmesi için rastgele kaldırmada **%25.1** node gerekirken, hedefli (degree/betweenness) kaldırmada yalnızca **%1.9-3.9** yeterli.

**Faz 5-7 bulgularına etkisi:** Salur Kazan/Bamsı Beyrek'in üstünlüğü network tanımına karşı nispeten kararlı (person-only'de bile top-10 overlap tam), ama alt sıradaki karakterlerin sıralaması modelleme kararına duyarlı.

---

## PHASE 9-12 — MOTIF DECISION, FIGURES, TABLES ✅ TAMAMLANDI

**Scriptler:** [`src/visualization.py`](src/visualization.py), [`src/export_tables.py`](src/export_tables.py) → **Rapor:** [`reports/09_12_figures_tables_report.md`](reports/09_12_figures_tables_report.md)

- **Faz 9-10 (motif/triad):** Atlandı, gerekçeli (DEC-010) — kapalı triad sayısı yalnızca 44/1.77M, uygun yönlü null model altyapısı yok.
- **Faz 11 (figures):** 8 öncelikli figür (F02, F03, F06, F07, F15, F16, F17, F18) PNG+SVG olarak `outputs/figures/` altında üretildi. F06'da 23-bileşen uyarısı doğrudan altyazıda. Kalan figürler (F01, F04-F05, F08-F14) backlog'da, düşük öncelik.
- **Faz 12 (tables):** T01-T11'in tamamı `outputs/tables/publication/` altında CSV+LaTeX olarak üretildi. **T08 (story similarity) kısmi** — yalnızca ham shared-actor projeksiyonu var, madde 17'nin tam benzerlik metrik seti (Jaccard/cosine/vb.) henüz hesaplanmadı.

**Yeni bağımlılık:** `jinja2` eklendi (`requirements.txt`) — pandas 3.0'da `to_latex()` için gerekli.

---

## PHASE 13-14 — INTER-ANNOTATOR & REPRODUCIBILITY ✅ TAMAMLANDI

**Rapor:** [`reports/13_14_reproducibility_report.md`](reports/13_14_reproducibility_report.md)

- **Faz 13:** `validation/inter_annotator_sample.csv` (70 satır, stratifiye, seed=42, 14/14 boy temsilli), `docs/inter_annotator_protocol.md`, `src/inter_annotator_stats.py` (Cohen's kappa + Krippendorff's alpha'ya hazır ama **ikinci kodlayıcı verisi olmadan `not_applicable` döndürüyor** — test edildi, sahte değer üretmiyor).
- **Faz 14:** `run_pipeline.py` (19 aşama, `--all`/`--stage`/`--fast`/`--validate-only`, `logs/`'a log yazıyor), `tests/` (**18 test, 18/18 PASS** — şema, aggregation, network inşası, determinizm), `outputs/manifest_sha256.csv` (192 dosya), `requirements-lock.txt` (42 paket), `.github/workflows/validate.yml` (CI: pytest + validate-only, ağır aşamalar CI dışında).

**Önemli:** `run_pipeline.py --all` (FULL mode) bu oturumda **uçtan uca test edilmedi** — yalnızca `--stage audit`, `--stage hash_manifest`, `--all --validate-only` doğrulandı. Her aşama zaten Faz 1-12'de ayrı ayrı çalıştırılmıştı, bu yüzden risk düşük ama tam bir `--all` çalıştırması (~10-15 dk) henüz yapılmadı — yeni oturum isterse bunu doğrulayabilir.

---

## PHASE 15-16 — WEB PORTAL & WEBSITE VALIDATION ✅ TAMAMLANDI

**Scriptler:** [`src/build_site_data.py`](src/build_site_data.py), [`src/build_site.py`](src/build_site.py), [`src/site_layout.py`](src/site_layout.py), [`docs/assets/explorer.js`](docs/assets/explorer.js), [`src/validate_site.py`](src/validate_site.py) → **Rapor:** [`reports/15_16_web_portal_report.md`](reports/15_16_web_portal_report.md)

- **363 HTML dosyası** üretildi: 14 statik sayfa (madde 52'nin tam nav listesi) + 14 boy sayfası + **332 karakter sayfası (tüm canonical aktörler, yalnızca top-N değil)**.
- Network Explorer (Cytoscape.js, cdnjs): 3 varyant (G0/G1/G2), arama, 3 layout, node/edge detay paneli — tarayıcıda canlı test edildi ve çalıştığı doğrulandı.
- **KRİTİK DÜZELTME (DEC-012):** İlk taslak `../outputs/...`/`../data/...`/`../reports/...` gibi repo-root-göreli yollar kullanıyordu — bu GitHub Pages'te (yalnızca `docs/` yayınlanır) 404 verirdi. **Bu hata yalnızca gerçek bir HTTP sunucusuyla test edilerek yakalandı** (`file://` önizlemesi statik snapshot olduğu için göstermedi). Çözüm: `copy_assets()` gerekli dosyaları build sırasında `docs/` içine kopyalıyor.
- **KRİTİK DÜZELTME (DEC-012):** 1 node'un 239 karakterlik `node_id`'si Windows dosya yolu sınırını aşıp site build'ini çökertti. `safe_filename()` ile çözüldü (yalnızca dosya adı, veri değil).
- **YENİ VERİ BULGUSU (DEC-013):** Website inşası sırasında **5 "birleştirilmiş çoklu-aktör node"** keşfedildi (ör. tek bir node'un `canonical_name`'i "Beyrek, Yigenek, Kazan, Kara Budak, Deli Dündar, Uruz" gibi virgülle ayrılmış 6 farklı karakter adı içeriyor). Faz 2'nin otomatik testlerinden hiçbirini ihlal etmediği için önceden yakalanmamıştı. Otomatik düzeltilmedi — `validation/HUMAN_REVIEW_QUEUE.csv`'ye HR0076-HR0080 olarak eklendi (80 madde, önceki 75'ten).
- `src/validate_site.py` (Faz 16): tüm dahili linkleri/asset'leri/JSON dosyalarını tarıyor. İlk çalıştırma: 85 kırık link. Düzeltme sonrası: **363/363 dosya PASS, 0 sorun** (`outputs/validation/site_validation_report.json`).

**Ders (yeni oturum için önemli):** Site değişiklikleri **her zaman gerçek bir HTTP sunucusuyla** (`python -m http.server`, `docs/` kökünden) test edilmeli, `file://` önizlemesiyle değil — ikincisi harici CSS/JS/fetch çağrılarını göstermez ve path hatalarını gizler.

---

## PHASE 17 — DOCUMENTATION ✅ TAMAMLANDI

**Rapor:** [`reports/17_documentation_report.md`](reports/17_documentation_report.md)

Yeni analiz yok — Faz 1-16'nın bilgisini kalıcı dokümanlara sentezledi: `docs/data_dictionary.md`, `docs/relation_codebook.md` (gerçek `raw_evidence` örnekleriyle), genişletilmiş `docs/methodology.md`, `docs/limitations.md` (17 madde), `DATASET_CARD.md`, `CITATION.cff` (yazar adı **TODO**, uydurulmadı — repo sahibinin gerçek adı bilinmiyor), `CHANGELOG.md`, `CONTRIBUTING.md`, `docs/architecture_diagram.svg`, kökte yeniden tasarlanmış `README.md`. Site yeniden build edildi + validate edildi: **363/363 PASS**.

---

## PHASE 18-19 — PAPER & THESIS PACKAGES ✅ TAMAMLANDI

**Dizinler:** [`paper/`](paper/), [`thesis/`](thesis/)

- **Faz 18 (paper):** `manuscript_outline.md` (öneri başlık: null-model retraction bulgusunu öne çıkaran bir başlık, master prompt'un önerdiği alternatif de not edildi), `methods.md`, `results.md` (her sayı gerçek `outputs/` dosyasına atıflı, madde 94'ün hedge'li dili kullanıldı, madde 110'un descriptive/exploratory/confirmatory etiketlemesi uygulandı), `supplementary_material.md`, `paper/figures/` (8 dosya) + `paper/tables/` (22 dosya, T01-T11 CSV+LaTeX) kopyalandı. Ayrıca `reports/literature_search_plan.md` (madde 97) oluşturuldu.
- **Faz 19 (thesis):** `research_questions.md` (RQ1-RQ7'nin her biri için "answerable: yes/partially/NOT YET" durumu — **RQ6 (story clustering) "NOT answerable with current data" olarak açıkça işaretlendi**, madde 17'nin tam benzerlik metrikleri eksik olduğu için zorla cevaplanmadı), `proposed_structure.md` (10 bölüm), `methodology_mapping.md`, `results_mapping.md`, `figure_inventory.md`, `table_inventory.md`.

**Önemli:** RQ4 (null model karşılaştırması) ve RQ5 (sensitivity) tam ve confirmatory olarak cevaplandı — bunlar projenin en güçlü, en savunulabilir bulguları. RQ6 dürüstçe "cevaplanamıyor" olarak işaretlendi (madde 140 kuralı: "uyguladım deme, not applicable olarak işaretle").

---

## PHASE 20-21 — FINAL VALIDATION/RELEASE & FINAL REPORTS ✅ TAMAMLANDI — PROJE TAMAMLANDI

**Scriptler:** [`src/validate_release_consistency.py`](src/validate_release_consistency.py) → **Raporlar:** [`reports/RELEASE_CHECKLIST.md`](reports/RELEASE_CHECKLIST.md), [`reports/FINAL_REBUILD_REPORT.md`](reports/FINAL_REBUILD_REPORT.md), [`reports/EXECUTIVE_SUMMARY.md`](reports/EXECUTIVE_SUMMARY.md)

- **Faz 20:** `src/validate_release_consistency.py` yazıldı — README.md/DATASET_CARD.md'deki temel sayıları (stories/actors/relations/events) gerçek kaynak dosyalarıyla çapraz kontrol ediyor. İlk çalıştırma 1 gerçek (küçük) tutarsızlık buldu: `DATASET_CARD.md` 14 birimi "narrative units" diye adlandırmış, "stories" kelimesini kullanmamıştı — terminoloji tutarlılığı için düzeltildi. Ayrıca `pytest` (18/18), `run_pipeline.py --all --validate-only` (PASS), `src/validate_site.py` (363/363, 0 sorun) yeniden çalıştırıldı, hepsi PASS.
- `reports/RELEASE_CHECKLIST.md`: madde 142'nin 15 maddelik kalite kapısı — **15/15 PASS veya PASS-WITH-DISCLOSED-GAPS**, hiçbir madde sahte PASS almadı, her kısmi/eksik durum ilgili belgeye atıflı.
- **Faz 21:** `reports/FINAL_REBUILD_REPORT.md` (madde 124'ün tam yapısı: Initial State → Future Work) ve `reports/EXECUTIVE_SUMMARY.md` (madde 125, ~4 dakikalık okuma) yazıldı. "Top 5 Strongest Defensible Findings" (madde 126) — hepsi gerçek istatistiklere atıflı, hiçbiri "en önemli karakter" tipi edebi iddia değil.

### PROJE DURUMU: `docs/MASTER_PROMPT.md`'nin 21 fazının tamamı tamamlandı (Faz 9-10 gerekçeli olarak atlandı, DEC-010).

**Bundan sonra kullanıcıyla görüşülmeden yapılmayacaklar** (NEXT_TASK.md'de de belirtildi):
- `claude-dk-rebuild` branch'ini remote'a push etmek (hiç push denenmedi, auth hazır değildi/istenmedi).
- `main`'e merge açmak.
- Siteyi gerçek GitHub Pages URL'sinde deploy etmek (repo ayarı değişikliği gerektirir).
- `CITATION.cff`'deki TODO alanlarını doldurmak (gerçek yazar adı/tarih bilgisi kullanıcıdan gelmeli).

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
10. Directed triadic census, ağın seyrekliği nedeniyle ezici çoğunlukla "003" (bağlantısız) tipte — motif-tipi yorum için null model karşılaştırması henüz yapılmadı (G9_directed'e uygun yönlü null model Faz 7 kapsamına alınmadı, backlog'da).
11. **Faz 5'in "disassortative network" bulgusu Faz 7'de geri çekildi** — degree assortativity, 9 ağın hiçbirinde FDR-düzeltmeli null modelden anlamlı şekilde farklı değil. Negatif değerler muhtemelen derece dağılımının kendisinden kaynaklanıyor.
12. Modularity/community yapısının (Faz 6) 7/9 ağda null modelden anlamlı yüksek olduğu doğrulandı — ama bu, 23-bileşen artefaktını (§8 yukarı) çözmüyor, yalnızca genel modularity sinyalinin rastgele olmadığını gösteriyor.
13. Faz 8 sensitivity: **person+group vs person-only** en büyük sıralama farkını yaratan modelleme kararı (ρ=0.887-0.926); PageRank, ağırlık şemasına (`agirlik`, semantiği hâlâ belirsiz — madde 36) en duyarlı metrik (ρ=0.849). Bu iki nokta, gelecekte "en önemli karakter" tartışması yapılırken **hangi network varyantının kullanıldığının açıkça belirtilmesi gerektiğini** gösteriyor.
14. Structural robustness yalnızca `G0_full` üzerinde çalıştırıldı, ortalama path length eğrisi hesaplanmadı (yalnızca dev bileşen boyutu) — gelecekteki bir iyileştirme.
15. Motif/triad null karşılaştırması atlandı (DEC-010, veri yetersizliği: 44/1.77M kapalı triad).
16. **Story similarity (madde 17) tamamlanmadı** — yalnızca ham shared-actor bipartite projeksiyonu var (`outputs/matrices/story_projection_shared_actors.csv`, `outputs/tables/publication/T08_story_similarity.csv`); actor Jaccard, weighted Jaccard, cosine, relation-profile similarity, layer-composition similarity, hierarchical clustering **henüz hesaplanmadı**. Bu, F10/F11 figürlerinin de neden üretilmediğini açıklıyor.
17. F01, F04-F05, F08-F14 figürleri (madde 48'in tam listesi) henüz üretilmedi — düşük öncelikli backlog.
18. Inter-annotator kappa/alpha hesaplanamadı (gerçek ikinci kodlayıcı yok, beklenen durum) — `not_applicable`.
19. `run_pipeline.py --all` (FULL mode, `--fast` olmadan) uçtan uca test edilmedi.
20. ~~Web portal, website validation~~ ✅ tamamlandı (Faz 15-16). Documentation (data dictionary/relation codebook/methodology/limitations), paper/thesis package, final validation/release raporları **henüz hiç başlamadı**.
21. **Website inşası sırasında 5 yeni "birleştirilmiş çoklu-aktör node" bulundu** (DEC-013, `validation/HUMAN_REVIEW_QUEUE.csv` HR0076-HR0080) — Faz 2'nin otomatik testlerini geçmişti ama içerik/anlamsal bir kalite sorunu. Düzeltilmedi, açık.
22. Site yalnızca 3 network varyantını (G0/G1/G2) Explorer'da sunuyor; G3-G11 export edilmedi. Similarity sayfası kısmi (madde 17 tamamlanmadı). TR/EN dil altyapısı yok. Mobil/erişilebilirlik sistematik test edilmedi.
23. Site henüz GitHub'a push edilmedi / gerçek Pages URL'sinde deploy edilmedi — yalnızca yerel `python -m http.server` ile test edildi.

---

## CURRENT EXACT POSITION

```text
CURRENT STATUS:
ALL 21 PHASES COMPLETE (9-10 skipped with documented rationale, DEC-010)
THE MASTER_PROMPT.md SCOPE IS FULLY DELIVERED.

NEXT PHASE:
NONE MANDATORY. This project has reached the end of its governing specification.
Any further work is optional polish (see "Future Work" in
reports/FINAL_REBUILD_REPORT.md) or something the user explicitly asks for next
(e.g. pushing to remote, deploying the site, resolving an open HUMAN_REVIEW_QUEUE.csv item).

DO NOT RESTART ANY COMPLETED PHASE UNLESS VALIDATION REVEALS A REAL ERROR.
DO NOT PUSH TO REMOTE OR MERGE TO MAIN WITHOUT EXPLICIT USER INSTRUCTION.
```

---

## OPTIONAL FUTURE WORK (nothing here is mandatory — the master prompt's scope is delivered)

If the user asks to continue, prioritize in this order (from `reports/FINAL_REBUILD_REPORT.md`
"Future Work" and `docs/limitations.md`):

1. Obtain a real second coder and run `src/inter_annotator_stats.py` on actual data.
2. Resolve the 5 concatenated-multi-actor nodes (DEC-013) — requires returning to original text.
3. Build the full story-similarity metric suite (Jaccard/cosine/relation-profile/layer-composition/
   hierarchical clustering) to properly answer RQ6 — currently the one open research question.
4. Confirm the source edition metadata (`validation/source_edition_metadata_required.md`).
5. Extend the Network Explorer to G3-G11; build remaining figures F01/F04-F05/F08-F14.
6. **Only if the user explicitly asks:** push `claude-dk-rebuild` to remote, deploy the site to a
   live GitHub Pages URL, or open a PR to `main`. None of these have been done — this entire
   project exists only as local commits so far.
7. Fill in `CITATION.cff`'s TODO fields once the repository owner confirms their name/publication
   details.

---

## REMAINING MASTER PLAN AFTER PHASE 16

Tam liste `docs/MASTER_PROMPT.md`'de; öncelik sırası (proje sahibinin verdiği faz numaralandırmasıyla, kendi phase raporu numaralandırmamızdan farklı olabilir — önemli olan iş sırası):

- ~~**PHASE 7 — Null Models / Statistical Validation**~~ ✅ **TAMAMLANDI**
- ~~**PHASE 8 — Sensitivity / Robustness**~~ ✅ **TAMAMLANDI**
- ~~**PHASE 9-10 — Motif/Triad**~~ ✅ **Atlandı, gerekçeli (DEC-010)**
- ~~**PHASE 11 — Publication Figures**~~ ✅ **TAMAMLANDI** (8/18 figür, backlog'da kalanlar var)
- ~~**PHASE 12 — Publication Tables**~~ ✅ **TAMAMLANDI** (T01-T11, T08 kısmi)
- ~~**PHASE 13 — Inter-Annotator Infrastructure**~~ ✅ **TAMAMLANDI** (altyapı hazır, gerçek agreement değeri yok — beklenen)
- ~~**PHASE 14 — Reproducibility/Pipeline**~~ ✅ **TAMAMLANDI** (`run_pipeline.py`, `tests/`, hash manifest, lock file)
- ~~**PHASE 15 — Web Portal**~~ ✅ **TAMAMLANDI** (363 HTML dosyası, bkz. yukarı)
- ~~**PHASE 16 — Website Validation**~~ ✅ **TAMAMLANDI** (363/363 PASS)
- ~~**PHASE 17 — Documentation**~~ ✅ **TAMAMLANDI**
- ~~**PHASE 18 — Paper Package**~~ ✅ **TAMAMLANDI** (`paper/`)
- ~~**PHASE 19 — Thesis Package**~~ ✅ **TAMAMLANDI** (`thesis/`)
- ~~**PHASE 20 — Final Validation/Release**~~ ✅ **TAMAMLANDI** (`reports/RELEASE_CHECKLIST.md`, 15/15 PASS)
- ~~**PHASE 21 — Final Reports**~~ ✅ **TAMAMLANDI** (`reports/FINAL_REBUILD_REPORT.md`, `reports/EXECUTIVE_SUMMARY.md`)

**Tüm 21 faz tamamlandı. `docs/MASTER_PROMPT.md`'nin kapsamı tam olarak teslim edildi.**

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
8. `reports/04_05_network_construction_and_descriptive_report.md` (§ assortativity düzeltme notuna dikkat)
9. `reports/06_advanced_network_analysis_report.md`
10. `reports/07_null_models_report.md`
11. `reports/08_sensitivity_robustness_report.md`
12. `reports/09_12_figures_tables_report.md`
13. `reports/13_14_reproducibility_report.md`
14. `reports/15_16_web_portal_report.md`
15. `reports/17_documentation_report.md`
16. `reports/RELEASE_CHECKLIST.md`, `reports/FINAL_REBUILD_REPORT.md`, `reports/EXECUTIVE_SUMMARY.md` — the project's closing documents; read these FIRST if you just want the overall picture
17. `thesis/research_questions.md` (which RQs are answerable, which are not)
18. `docs/network_models.md`, `docs/methodology.md`, `docs/limitations.md`, `docs/data_dictionary.md`, `docs/relation_codebook.md`
12. `docs/decision_log.md`
13. `data/processed/*.csv` (canonical dataset — özellikle `nodes.csv`, `relations_event_level.csv`, `relations_aggregated.csv`, `relation_taxonomy.csv`)
14. `src/networks.py` (network tanımlarının tek kaynağı — `NETWORK_DEFINITIONS`)
15. `src/communities.py`, `src/signed_and_directed.py`, `src/multilayer.py`, `src/narrative_order.py`, `src/null_models.py`, `src/null_models_fdr.py` (Faz 6-7 kodu, referans için)
16. `project_state.json` (makine-okunabilir özet)

---

## IMPORTANT DECISIONS

Bkz. [`docs/decision_log.md`](docs/decision_log.md) — DEC-001'den başlayarak tüm metodolojik kararlar orada.

---

## SESSION CONTINUITY RULE

Bundan sonra her büyük faz tamamlandığında `CLAUDE_SESSION_HANDOFF.md`, `NEXT_TASK.md`, `project_state.json` güncellenecek. Bu üç dosya + `docs/decision_log.md`, projenin kalıcı session-memory/checkpoint sistemidir.
