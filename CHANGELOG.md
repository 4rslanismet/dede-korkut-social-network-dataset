# Changelog

Format loosely follows [Keep a Changelog](https://keepachangelog.com/). This project's dataset
versions before this rebuild (v1, v2, v3) are documented in `docs/README_v2.md` and
`docs/README_v3.md` — they are not repeated here.

## [processed-v4-rebuild, post-review] — claude-dk-fixpass branch (2026-09)

Corrections after two independent reviews of the rebuild below. No canonical data, raw data or headline
finding changed; current counts live in `outputs/results_registry.json`, `outputs/manifest_sha256.csv` and
`outputs/validation/site_validation_report.json`, not in this file. Details: `reports/FIX_PASS_REPORT.md`.

### Fixed

- Weighted betweenness now uses shortest-path distance = 1 / tie strength (DEC-017); hop-count betweenness
  is kept as a separate measure. Affected rankings, the sensitivity analysis and their tables were
  regenerated; the claim that two actors lead betweenness in every specification was withdrawn.
- Composite-node disclosure replaced by a reproducible scan (`src/composite_nodes.py`, DEC-018); the review
  queue was expanded and nothing was split or merged. The scan is a heuristic and under-inclusive.
- Website: generated character/story page sets derived from the data, stale pages removed, story pages
  separate raw relation records from aggregated edges, all scientific numbers loaded from the results
  registry (DEC-019); the pipeline now also builds and validates the site.
- Release-consistency validator derives its counts instead of carrying typed constants; stale status text,
  pre-correction sensitivity values, machine-specific paths and an unlabelled pre-fix betweenness value
  were corrected.

### Superseded

- The test count, page count and composite-node count quoted in the entry below describe the initial
  rebuild only.

## [processed-v4-rebuild] — claude-dk-rebuild branch (2026-09)

Full, from-scratch rebuild of the analysis and publication layer on top of the existing v3
dataset. `data/raw/` and `data/final/` (v3) are untouched; everything below is new. (Counts in this
entry are as of the initial rebuild; see the post-review entry above for what changed.)

### Added

- **Repository audit** (`src/audit.py`, `reports/01_repository_audit.md`): re-derived every
  README headline number from source files; found and documented a +80-row undocumented gap
  between `data/story_level/` and `data/final/`, and confirmed `data/raw/*.xlsx` is not the direct
  raw source of the processed data.
- **Validation framework** (`src/validate.py`, `src/entity_resolution.py`,
  `reports/02_data_quality_report.md`): 26 structural checks across node/edge/event/alias tables;
  entity-resolution candidate list and a 75-item (later 80-item) human review queue.
- **Canonical dataset** (`data/processed/`, `src/build_canonical.py`,
  `reports/03_canonical_dataset_report.md`): normalized schema, one entity merge, an interpretive
  relation taxonomy, unordered-pair aggregation, and per-relation provenance linkage.
- **Network models** (`src/networks.py`, `src/build_networks.py`, `src/story_networks.py`,
  `docs/network_models.md`): 12 network variants (G0-G11), 14 story-level networks, and the
  actor×story bipartite network with its two projections.
- **Descriptive and advanced analysis** (`src/metrics.py`, `src/communities.py`,
  `src/signed_and_directed.py`, `src/multilayer.py`, `src/narrative_order.py`): centrality,
  community detection (Leiden/Louvain), signed/directed analysis, multilayer versatility,
  narrative-order windowing, dynamic centrality.
- **Statistical validation** (`src/null_models.py`, `src/null_models_fdr.py`,
  `reports/07_null_models_report.md`): degree-preserving null models with Benjamini-Hochberg FDR
  correction across 36 tests; retracted the earlier "disassortative network" descriptive claim
  after it failed null-model validation.
- **Sensitivity and robustness** (`src/sensitivity.py`, `src/robustness.py`,
  `reports/08_sensitivity_robustness_report.md`): rank-stability testing across 6
  network-construction choices; structural robustness curves under random/targeted node removal.
- **Publication figures and tables** (`src/visualization.py`, `src/export_tables.py`,
  `outputs/figures/`, `outputs/tables/publication/`): 8 figures, 11 tables (CSV + LaTeX).
- **Inter-annotator infrastructure** (`validation/inter_annotator_sample.csv`,
  `docs/inter_annotator_protocol.md`, `src/inter_annotator_stats.py`): stratified sample and
  agreement-statistic tooling, correctly refusing to report a value without real second-coder
  data.
- **Reproducibility pipeline** (`run_pipeline.py`, `tests/`, `outputs/manifest_sha256.csv`,
  `requirements-lock.txt`, `.github/workflows/validate.yml`): 18 automated tests, SHA-256 hash
  manifest, CI validation gate.
- **Web portal** (`docs/`): full GitHub Pages site — 363 pages, an interactive Cytoscape.js
  network explorer, and per-actor/per-story profile pages, all generated from pipeline outputs.
- **Documentation**: `docs/data_dictionary.md`, `docs/relation_codebook.md`, expanded
  `docs/methodology.md`, `docs/limitations.md`, `DATASET_CARD.md`, `CITATION.cff`, this
  `CHANGELOG.md`, `CONTRIBUTING.md`.
- `docs/decision_log.md`: 13 documented methodological decisions (DEC-001 through DEC-013).

### Fixed

- Merged one high-confidence duplicate node (`begil_in_adamlari`→`begilin_adamlari`).
- Corrected two site-generation bugs found while building the web portal: repo-relative links that
  would 404 on a real GitHub Pages deployment (fixed by copying required assets into `docs/`), and
  a 239-character node ID that exceeded the filesystem path limit (fixed with a deterministic
  filename-truncation scheme that does not alter the underlying data).

### Discovered, not fixed (see `docs/limitations.md` and `validation/HUMAN_REVIEW_QUEUE.csv`)

- 5 nodes whose `canonical_name` is a comma-joined list of multiple distinct characters collapsed
  into one node (found while generating website character pages).
- 17 lower-confidence alias conflicts and 45 "stale alias target" cases (alias dictionary entries
  pointing to intermediate v1/v2 names no longer present in the v3 node table).
- 1 unexpected self-loop (`DKR0220`, Bamsı Beyrek).

### Known incomplete

- Story similarity (Jaccard/cosine/relation-profile/layer-composition metrics) — only the raw
  shared-actor bipartite projection has been computed.
- Motif/triad null-model enrichment for the directed network — skipped, insufficient sample
  (44 closed triads) and no directed degree-preserving null model available.
- Figures F01, F04-F05, F08-F14 of the F01-F18 target list.
