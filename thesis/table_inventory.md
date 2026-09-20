# Table Inventory

All tables in `outputs/tables/publication/` (CSV + LaTeX), mirrored in `paper/tables/` and
`docs/downloads/outputs/tables/publication/`.

| ID | Title | Rows | Used for RQ | Notes |
|---|---|---:|---|---|
| T01 | Dataset overview | 8 | RQ1 | Actor/relation/event counts by type |
| T02 | Relation taxonomy | 17 | RQ3 | Family mapping + occurrence counts |
| T03 | Story-level statistics | 14 | RQ1, RQ7 | Per-story network metrics; raw relation records and aggregated-graph edges are separate columns (density/degree/clustering use the aggregated graph) |
| T04 | Centrality results | 20 | RQ1 | Top 20 actors, G0_full |
| T05 | Community statistics | 9 | RQ1, RQ4 | Leiden/Louvain comparison + stability |
| T06 | Layer-specific metrics | 15 | RQ2, RQ3 | Top actors per layer |
| T07 | Actor-story participation | 15 | RQ2 | Top actors by story count |
| T08 | Story similarity | 91 | RQ6 | **Complete table, exploratory content** (post-project, DEC-014/015) — all 5 metrics, all 91 story pairs; max actor Jaccard 0.153 (low overlap) |
| T09 | Null model tests | 36 | RQ4 | Every test, FDR-corrected |
| T10 | Sensitivity analysis | 18 | RQ5 | 6 pairs × 3 metrics |
| T11 | Robustness results | 12 | RQ5 | 3 strategies × 2 thresholds × 2 component-size denominators (all G0 nodes / initial giant component), grid and exact crossings |

## Additional Machine-Readable Outputs Not in the T01-T11 Set

- `data/processed/*.csv` (8 files) — the canonical dataset itself, referenced throughout.
- `outputs/statistics/corpus_network_metrics.csv` — full per-network descriptive statistics
  (source for T01/T03 and Figure F02/F03 captions).
- `outputs/tables/centrality_{G0_full,G1_person_only,G2_core_social,G9_directed}.csv` — full
  centrality profiles (T04 is a 20-row excerpt of `centrality_G0_full.csv`).
- `outputs/tables/multilayer_profile.csv` — full multilayer profile for all 311 actors (T06 is a
  15-row excerpt).
- `outputs/tables/narrative_order_windows.csv`, `dynamic_centrality_trajectory.csv` — RQ7 source
  data, not yet formatted as a numbered publication table.
- `outputs/matrices/story_projection_shared_actors.csv`, `actor_projection_cooccurrence.csv` —
  RQ2 raw projections underlying T07.
- `outputs/matrices/story_similarity_{actor_jaccard,actor_weighted_jaccard,actor_cosine,relation_profile,layer_composition}.csv` —
  the 5 full 14×14 similarity matrices underlying T08 (RQ6, completed post-project).
- `outputs/statistics/story_similarity_clustering.json` — Ward linkage matrix and dendrogram leaf
  order for the RQ6 hierarchical clustering (visualization order, not a validated cluster assignment).
- `outputs/statistics/story_similarity_cluster_validity.json` — cluster-validity audit (silhouette,
  cophenetic correlation, linkage agreement, bootstrap stability, permutation baseline; DEC-015).
