# Motif Analysis Decision, Publication Figures & Tables — Faz 9-12

**Scriptler:** [`src/visualization.py`](../src/visualization.py), [`src/export_tables.py`](../src/export_tables.py)
**İlgili karar:** DEC-010 (`docs/decision_log.md`)

---

## 1. Faz 9-10 — Motif/Triad Ek Analizi: Atlandı (Gerekçeli)

G9_directed'in triadic census'u (Faz 6) incelendiğinde, kapalı triad kategorilerinin (030T+030C+120D+120U+120C+210+300) toplamı yalnızca **44** — 1.774.630 toplam triad'ın **%0.0025'i**. Bireysel kategoriler tek haneli (300: 1, 030C: 2, 120D: 3...). Ayrıca mevcut networkx sürümünde (3.6.1) yönlü ağlar için hazır bir degree-preserving randomizasyon yok.

**Karar (DEC-010):** Bu analiz atlandı. Madde 32'nin "küçük networklerde aşırı istatistiksel yorum yapma" kuralı ve Faz 6/7'nin kendi emsali (13 üçgen → not_applicable) ile tutarlı. Gelecekte elle yazılmış bir yönlü double-edge-swap eklenirse, yalnızca toplam kapalı-triad sayısı (44) tek bir null karşılaştırmasıyla test edilebilir.

---

## 2. Faz 11 — Publication Figures

8 öncelikli figür üretildi (`outputs/figures/`), madde 47 kurallarına uyularak (hairball yok, degree-bazlı node boyutu, ağırlık-bazlı edge opacity, seçici etiketleme — yalnızca top 6 node etiketlendi, çakışmayı önlemek için halka-desenli offset + lider çizgileri kullanıldı):

| Figür | Dosya | İçerik |
|---|---|---|
| F02 | `corpus/F02_corpus_full_network.png(.svg)` | G0_full (311 node, 376 edge) |
| F03 | `corpus/F03_person_only_network.png(.svg)` | G1_person_only (154 node) |
| F06 | `communities/F06_community_structure.png(.svg)` | G2_core_social, Leiden renklendirmesi — **23-bileşen uyarısı doğrudan figür altyazısında** |
| F07 | `corpus/F07_top_actors_centrality_comparison.png(.svg)` | Top 15 aktör, degree/betweenness/PageRank yan yana |
| F15 | `null_models/F15_null_model_distributions.png(.svg)` | FDR-anlamlı 12 testin tümü, random dağılım + gözlenen değer |
| F16 | `sensitivity/F16_sensitivity_correlation_matrix.png(.svg)` | 6 sensitivity çifti × 3 metrik Spearman ρ heatmap |
| F17 | `sensitivity/F17_centrality_rank_stability.png(.svg)` | Person+group vs person-only rank scatter |
| F18 | `robustness/F18_structural_robustness_curves.png(.svg)` | 3 kaldırma stratejisi, dev bileşen boyutu eğrisi |

**Üretilmeyen figürler (madde 48'in tam F01-F18 listesinden):** F01 (workflow diyagramı — Faz 17 mimari diyagramıyla birlikte yapılacak), F04 (core-social — F02'ye çok benzer, düşük öncelik), F05 (multilayer overview), F08 (story metrics karşılaştırması), F09 (bipartite), F10/F11 (story similarity — madde 17'nin tam benzerlik metrikleri henüz hesaplanmadı, yalnızca ham shared-actor projeksiyonu var), F12 (layer participation), F13 (positive/negative karşılaştırma), F14 (narrative-order evolution). Bunlar backlog'da, öncelik değeri düşük görüldüğü için bu turda atlandı.

---

## 3. Faz 12 — Publication Tables (T01-T11)

Tüm 11 tablo `outputs/tables/publication/` altında hem CSV hem LaTeX (`\begin{tabular}`) formatında üretildi:

| Tablo | İçerik | Satır |
|---|---|---:|
| T01 | Dataset overview | 8 |
| T02 | Relation taxonomy | 17 |
| T03 | Story-level statistics | 14 |
| T04 | Top 20 centrality (G0_full) | 20 |
| T05 | Community statistics | 9 |
| T06 | Top 15 layer participation | 15 |
| T07 | Top 15 actor-story participation | 15 |
| T08 | Story similarity (**kısmi** — bkz. aşağı) | 14 |
| T09 | Null model tests (36, FDR) | 36 |
| T10 | Sensitivity analysis | 18 |
| T11 | Robustness results | 6 |

**T08 önemli not:** Bu tablo şu anda yalnızca ham "shared-actor" bipartite projeksiyonunu (`outputs/matrices/story_projection_shared_actors.csv`) içeriyor — madde 17'nin istediği tam benzerlik metrik seti (actor Jaccard, weighted Jaccard, cosine, relation-profile similarity, layer-composition similarity, hierarchical clustering) **henüz hesaplanmadı**. Bu, `docs/MASTER_PROMPT.md` madde 17'nin tamamlanmamış bir parçası olarak kalıyor — gelecekteki bir iyileştirme.

---

## 4. Genel Değerlendirme

Bu üç fazın hiçbiri yeni bilimsel bulgu üretmedi — Faz 5-8'in sonuçlarını **yayın-hazır** formatlara (figür, tablo) dönüştürdüler. Motif analizi, veri yetersizliği nedeniyle dürüstçe atlandı.

## 5. Sıradaki Adım

Faz 13 (Inter-Annotator Infrastructure) → Faz 14 (Reproducibility/Pipeline: `run_pipeline.py`, `tests/`, hash manifest) → Faz 15 (Web Portal) → ... (bkz. `CLAUDE_SESSION_HANDOFF.md`).
