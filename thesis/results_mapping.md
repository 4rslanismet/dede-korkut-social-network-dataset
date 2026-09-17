# Results Mapping

Maps each research question to the specific finding(s) that answer it, with exact figures/tables
to cite. Cross-reference `paper/results.md` for full prose treatment.

## RQ1 — Structural organization

- **Finding:** G0_full: 311 connected actors, 376 edges, density 0.0078, 23 components, largest
  261 actors. Salur Kazan/Bamsı Beyrek dominate degree/betweenness/PageRank across G0/G1/G2/G9.
- **Cite:** Table T04, Figure F02/F03/F07, `outputs/statistics/corpus_network_metrics.csv`.
- **Confirmatory layer:** community modularity validated above null in 7/9 networks (see RQ4).

## RQ2 — Bridge actors

- **Finding:** Aruz has the highest community-participation coefficient (0.778, 8 inter-community
  edges) within one Leiden partition of G2_core_social — a bridge candidate, not a validated
  finding across partitions. Salur Kazan is the only actor active in all 7 relation layers
  (participation coefficient 0.766).
- **Cite:** `outputs/tables/community_bridge_metrics_G2_core_social.csv`, Table T06.
- **Caveat:** cross-*story* bridging (via the bipartite projection) was not used for this claim —
  degree-inflation caveat applies (`docs/network_models.md`).

## RQ3 — Relation-specific structural roles

- **Finding:** G3 (kinship) is statistically indistinguishable from its null model on all four
  tested metrics — a genuine negative result. G4 (communication) shows validated elevated
  clustering (q=0.048). G6 (conflict) shows validated elevated modularity (q=0.027).
- **Cite:** Table T09 (rows filtered by network), `reports/07_null_models_report.md` §3.4.

## RQ4 — Null-model comparison

- **Finding:** Modularity significant in 7/9 networks (Table T09); degree assortativity
  significant in 0/9 networks — retraction of the earlier "disassortative" claim.
- **Cite:** Table T09 in full, Figure F15 (null model distributions), `reports/07_null_models_report.md`.
- **This is the thesis's strongest confirmatory chapter-5 result.**

## RQ5 — Sensitivity to construction choices

- **Finding:** Person+group vs. person-only: ρ=0.887-0.926 (largest disagreement of 6 tested
  pairs). Girizgah/core-social filtering: ρ=1.000 (negligible). Weighted vs. unweighted: PageRank
  most sensitive (ρ=0.849). Structural robustness: 25.1% random vs. 1.9-3.9% targeted removal to
  halve the giant component.
- **Cite:** Table T10, T11, Figure F16, F17, F18.

## RQ6 — Story clustering (answered post-project, DEC-014)

- **Finding:** S03/S05 (Jaccard=0.153) and S08/S10 (Jaccard=0.133) are the most actor-similar
  story pairs, both also scoring highly on relation-profile and layer-composition similarity
  (0.94-0.97) — these pairs are alike both in who appears and in what kind of relations dominate.
  Ward hierarchical clustering on each story's relation-family/layer proportion profile shows no
  sharp genre-like partition — several tight pairs/triples embedded in a broader continuum.
- **Cite:** Table T08 (full 5-metric, 91-pair suite), Figure F10 (heatmap), Figure F11 (network,
  top 15 pairs), `outputs/statistics/story_similarity_clustering.json` (dendrogram/linkage).
- **Caveat for the thesis text:** descriptive only — no significance test was applied to the
  clustering or similarity values themselves (unlike RQ4's null-model-tested claims).

## RQ7 — Narrative-order evolution (exploratory only)

- **Finding:** 13/14 stories windowed into early/middle/late narrative-order tertiles; conflict
  intensity increases from early to late window in several (not all) stories, described
  descriptively, no formal trend test applied. Dynamic centrality trajectory: Salur Kazan and
  Bamsı Beyrek recur across multiple stories (corpus-wide centrality); Tepegöz and Basat
  concentrate almost entirely within one story each (locally high, not corpus-wide).
- **Cite:** `outputs/tables/narrative_order_windows.csv`, `outputs/tables/dynamic_centrality_trajectory.csv`,
  `reports/06_advanced_network_analysis_report.md` §5-6.
- **Caveat for the thesis text:** frame explicitly as exploratory; do not upgrade to a
  confirmatory claim without running an actual statistical trend test first.
