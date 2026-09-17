# Supplementary Material

Companion to `paper/manuscript_outline.md`, `paper/methods.md`, `paper/results.md`. Every item
below points to the actual repository artifact — this document is an index, not a duplicate.

## S1. Full Metric Tables

- **T01 Dataset overview** — `paper/tables/T01_dataset_overview.csv`
- **T02 Relation taxonomy** (17 types, families, occurrence counts) — `paper/tables/T02_relation_taxonomy.csv`
- **T03 Story-level statistics** (14 stories: nodes, edges, density, clustering, centralization) — `paper/tables/T03_story_level_statistics.csv`
- **T04 Centrality results** (top 20 actors, G0_full) — `paper/tables/T04_centrality_results.csv`
- **T05 Community statistics** — `paper/tables/T05_community_statistics.csv`
- **T06 Layer-specific metrics** (top 15 actors by layer participation) — `paper/tables/T06_layer_specific_metrics.csv`
- **T07 Actor-story participation** (top 15 by story count) — `paper/tables/T07_actor_story_participation.csv`
- **T08 Story similarity** (complete, post-project — 5 metrics × 91 pairs; DEC-014) — `paper/tables/T08_story_similarity.csv`
- **T09 Null model tests** (all 36 tests, observed/z/p/q) — `paper/tables/T09_null_model_tests.csv`
- **T10 Sensitivity analysis** (all 6 pairs × 3 metrics) — `paper/tables/T10_sensitivity_analysis.csv`
- **T11 Robustness results** — `paper/tables/T11_robustness_results.csv`

Figures F10 (`paper/figures/F10_story_similarity_heatmap.png`) and F11
(`paper/figures/F11_story_similarity_network.png`) accompany T08.

LaTeX versions of every table above (`.tex`) are in the same directory for direct manuscript
inclusion.

## S2. Null Model Details

- Method: `networkx.double_edge_swap`, 10 swaps per edge, 1000-member ensemble, seed 42
  (`config/analysis.yaml`).
- Full per-test results (observed, random mean/SD, z-score, percentile, empirical p, BH q-value):
  `outputs/statistics/null_model_fdr_corrected.csv`.
- Raw ensemble summary per network/metric: `outputs/null_models/null_model_results_full.json`.
- FAST-mode (n=100) cross-check, confirming direction/significance agreement with the full run:
  `outputs/null_models/null_model_results_fast.json`.

## S3. Coding Protocol and Taxonomy

- Relation taxonomy with definitions and real examples: `docs/relation_codebook.md`.
- Full column-by-column schema of the canonical dataset: `docs/data_dictionary.md`.
- Inter-annotator protocol (for a future second coder — not yet executed):
  `docs/inter_annotator_protocol.md`, stratified sample at
  `validation/inter_annotator_sample.csv` (70 rows).

## S4. Validation Results

- Structural validation summary (node/edge/event/alias integrity): `outputs/validation/summary.json`.
- Entity resolution candidates (1 applied, 17 open): `validation/entity_resolution_candidates.csv`.
- Full human review queue (80 open items across 4 categories — entity resolution, stale alias
  targets, provenance gaps, and the concatenated-multi-actor nodes found while building the
  website): `validation/HUMAN_REVIEW_QUEUE.csv`.
- Website link/asset validation (363 pages, 0 issues at last check): `outputs/validation/site_validation_report.json`.
- SHA-256 hash manifest of every key data/output file (192 files): `outputs/manifest_sha256.csv`.

## S5. Every Documented Methodological Decision

Thirteen decisions (DEC-001 through DEC-013), each with the question, the decision made, the
rationale, and current status: `docs/decision_log.md`. These cover entity merging, relation-family
mapping, directed-network construction, structural-balance and motif-analysis thresholds,
null-model method choice, sensitivity-pair construction, and the two website-build bugs found and
fixed while generating this project's companion portal.

## S6. Sensitivity Analysis — Full Detail

Six network-construction variant pairs, three centrality metrics each (18 rows):
`paper/tables/T10_sensitivity_analysis.csv`, visualized in `paper/figures/F16_sensitivity_correlation_matrix.png`
and `paper/figures/F17_centrality_rank_stability.png`.

## S7. Known Incomplete Analyses

- Directed-network null model — no degree-preserving randomization for directed graphs was
  available in the software version used; only 44/1,774,630 triads are closed, an insufficient
  sample for enrichment testing regardless.
- Publication figures F01, F04-F05, F08-F09, F12-F14 (of the F01-F18 target set) were not
  produced. (F10-F11, story similarity heatmap/network, were completed post-project — see S1.)
- 5 concatenated-multi-actor nodes discovered while building the companion website remain
  unresolved (`docs/decision_log.md` DEC-013).

## S8. Interactive Companion

All results in this supplement are also browsable interactively at the project's GitHub Pages
site (`docs/`), including a Cytoscape.js network explorer and a profile page for every one of the
332 canonical actors.
