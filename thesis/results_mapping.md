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

- **Finding:** G3 (kinship) shows no detectable deviation from its null model on any of four
  tested metrics — a negative, low-information result (G3 is a forest: 83 nodes, 61 edges, 22
  components, so clustering/transitivity are structurally zero; only assortativity and modularity
  are informative). G4 (communication) shows validated elevated
  clustering (q=0.048). G6 (conflict) shows validated elevated modularity (q=0.027).
- **Cite:** Table T09 (rows filtered by network), `reports/07_null_models_report.md` §3.4.

## RQ4 — Null-model comparison

- **Finding:** Modularity significant in 7/9 networks (Table T09); degree assortativity
  significant in 0/9 networks — retraction of the earlier "disassortative" claim.
- **Cite:** Table T09 in full, Figure F15 (null model distributions), `reports/07_null_models_report.md`.
- **This is the thesis's strongest confirmatory chapter-5 result.**

## RQ5 — Sensitivity to construction choices

- **Finding:** Actor-type inclusion and edge weighting change centrality rankings most: person+group
  vs. person-only ρ=0.887-0.926 (lowest mean ρ, 0.91), groups included vs. excluded ρ=0.896-0.957,
  weighted vs. unweighted PageRank ρ=0.849 (lowest single value). Girizgah/core-social filtering and
  relation-inference policy: ρ ≥ 0.97 (negligible). Do not call any one of the three larger-effect
  choices "the single most consequential" (means 0.91-0.93, untested differences, different node
  sets). Structural robustness (G0_full): 25.1% random (78 nodes) vs. 1.9-3.9% targeted (6-12
  nodes) removal before the largest component falls below half of the original 311 nodes.
- **Cite:** Table T10, T11, Figure F16, F17, F18.

## RQ6 — Story similarity / clustering (PARTIALLY ANSWERED / EXPLORATORY; DEC-014, DEC-015)

- **Finding (pairwise, descriptive):** actor overlap between stories is low (Jaccard median 0.030,
  max 0.153; 28 of 91 pairs share no actor). S03/S05 (0.153) and S08/S10 (0.133) are the
  *relatively most overlapping* pairs among the evaluated stories, not strongly similar ones. S03/S05
  is the top pair on the two Jaccard measures only (rank 6–7 of 91 on the three cosine measures).
  Cosine values of 0.9+ are high by construction and are matched by a permutation baseline at the
  top of the distribution, so they carry no claim of specific affinity.
- **Finding (clustering):** Ward always yields a dendrogram; validity checks (silhouette 0.37–0.56,
  bootstrap ARI 0.54–0.79, linkage disagreement at k=4–5, permutation baseline) do not support a
  robust discrete cluster structure. Write: "Story-level similarity can be quantified and visualized,
  but evidence for a robust discrete clustering structure is limited." Do **not** write "story
  clusters", "genres" or "highly similar stories".
- **Interpretation rule:** captivity or any other narrative theme is not a coded variable in the
  canonical dataset; thematic readings of similar pairs belong in the qualitative literary chapters,
  labelled as interpretation, never as a network-analysis result.
- **Cite:** Table T08 (full 5-metric, 91-pair suite), Figure F10 (heatmap), Figure F11 (actor-overlap
  network, top 15 pairs), `outputs/statistics/story_similarity_clustering.json`,
  `outputs/statistics/story_similarity_cluster_validity.json`.
- **Caveat for the thesis text:** descriptive/exploratory — no significance test was applied to the
  similarity values themselves (unlike RQ4's null-model-tested claims).

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
