# Network Construction (Faz 4) & Descriptive Analysis (Faz 5)

**Scriptler:** [`src/networks.py`](../src/networks.py), [`src/build_networks.py`](../src/build_networks.py), [`src/story_networks.py`](../src/story_networks.py), [`src/metrics.py`](../src/metrics.py)
**Tanımlar:** [`docs/network_models.md`](../docs/network_models.md)

## Faz 4 — Network Construction

12 network varyantı (G0–G11), tek bir filtre fonksiyonu ile `relations_event_level.csv`'den inşa edildi (tanımlar `docs/network_models.md`'de). Özet:

| Model | Nodes | Edges | Density | Bileşen | Dev bileşen | Avg degree |
|---|---:|---:|---:|---:|---:|---:|
| G0_full | 311 | 376 | 0.0078 | 23 | 261 | 2.42 |
| G1_person_only | 154 | 182 | 0.0154 | 14 | 121 | 2.36 |
| G2_core_social | 309 | 374 | 0.0079 | 23 | 259 | 2.42 |
| G3_kinship | 83 | 61 | 0.0179 | 22 | 24 | 1.47 |
| G4_communication | 74 | 73 | 0.0270 | 11 | 43 | 1.97 |
| G5_cooperation_support | 73 | 65 | 0.0247 | 12 | 45 | 1.78 |
| G6_conflict | 114 | 92 | 0.0143 | 23 | 43 | 1.61 |
| G7_positive | 127 | 116 | 0.0145 | 18 | 82 | 1.83 |
| G8_negative | 126 | 102 | 0.0130 | 25 | 57 | 1.62 |
| G9_directed | 221 | 324 | 0.0067 | 13 (weak) | 194 | 2.93 |
| G10_weighted / G11_unweighted | 311 | 376 | (G0 ile aynı yapı) | | | |

**Not:** `G0_full`, 332 canonical node'dan 311'ini içeriyor — kalan 21 node yalnızca `dede_korkut_olaylar_temiz.csv` (event) tablosunda geçiyor, hiçbir edge'de yer almıyor; bu yüzden edge-tabanlı network'te izole kalıp kaldırılıyorlar (node listesinden değil, sadece o network'ün graf nesnesinden). `G9_directed`, yalnızca `yönlü` ilişkileri kullandığı için 111 node'u izole bırakıyor (yönsüz ilişkilerle bağlı olanlar).

Story-level networkler (14 boy) ve actor×story bipartite network (311 aktör × 14 boy, 399 incidence) inşa edildi; detaylar ve **degree inflation uyarısı** `docs/network_models.md`'de.

## Faz 5 — Descriptive Analysis

`outputs/statistics/corpus_network_metrics.csv`: her network için density, clustering, transitivity, degree assortativity, diameter/avg-shortest-path/eccentricity (dev bileşen üzerinde), max k-core, (G9 için) reciprocity hesaplandı.

**Öne çıkan bulgular:**
- Tüm varyantlarda **degree assortativity negatif** (-0.11 ile -0.33 arası) → betimleyici olarak hub-and-spoke yapıya işaret ediyor (yüksek dereceli aktörler düşük dereceli aktörlere bağlanma eğiliminde).
  > **DÜZELTME (Faz 7, bkz. [`reports/07_null_models_report.md`](07_null_models_report.md) §3.3):** Null-model karşılaştırması bu gözlemin **istatistiksel olarak sağlam olmadığını** gösterdi — 9 ağın hiçbirinde degree assortativity, Benjamini-Hochberg FDR düzeltmesinden sonra rastgele (degree-preserving) ağdan anlamlı şekilde farklı değil. "Disassortative" ifadesi geri çekilmiştir; negatif değerler büyük ölçüde derece dağılımının kendisinden kaynaklanıyor olabilir, ek bir yapısal sinyal olarak kullanılmamalıdır.
- `G9_directed` reciprocity = **0.358** — yönlü ilişkilerin yaklaşık üçte biri karşılıklı.
- Max k-core tüm ana varyantlarda düşük (1–3) → yoğun, sıkı-bağlı bir çekirdek yerine dallanan/ağaç-benzeri bir yapı.

**Centrality profilleri** (`outputs/tables/centrality_{G0_full,G1_person_only,G2_core_social,G9_directed}.csv`): degree, strength, betweenness, harmonic centrality, PageRank, eigenvector centrality (ve G9 için in/out-degree + HITS) hesaplandı.

**G1 (person-only) top 5 by degree:** Salur Kazan (35), Bamsı Beyrek (21), Segrek (12), Bayındır Han (11), Kara Budak (8). Bu sıralama G0/G2'de de büyük ölçüde tutarlı (Salur Kazan ve Bamsı Beyrek her varyantta ilk iki sırada) — ancak bu sonucun network-tanım kararlarına ne kadar duyarlı olduğu Faz 8'de (sensitivity) sistematik olarak test edilecek, burada **tek bir merkezi metrikle "en önemli karakter" iddiası yapılmıyor**.

Tam çok-boyutlu karakter profili (madde 20: degree+strength+betweenness+pagerank+story_count+layer_count+coreness+community_bridge_score) multilayer (Faz 6) ve community detection (Faz 6) tamamlandıktan sonra birleştirilecek — bu rapor yalnızca ara/kısmi profildir.

## Sıradaki Adım

Faz 6 (Advanced Network Analysis): community detection (Leiden/Louvain, çoklu seed, resolution sensitivity), community bridge/participation coefficient, multilayer versatility, signed network (positive/negative degree + structural balance), directed triad census, narrative-order evolution.
