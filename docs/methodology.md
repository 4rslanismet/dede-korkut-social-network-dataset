# Methodology

This document is written to be detailed enough to serve as the technical source for a thesis or
paper methods section. Every claim below is traceable to a script under `src/`, a report under
`reports/`, or a decision in `docs/decision_log.md` (cited as DEC-XXX throughout).

---

## 1. Data Provenance and Starting Point

This rebuild starts from the legacy `data/final/` (v3) dataset already present in the repository
(documented in `docs/README_v2.md`, `docs/README_v3.md`): 333 nodes, 628 edges, 85 narrative
events across 14 stories (13 boy + 1 girizgah prologue). `data/raw/` (a single Excel workbook,
13 sheets, `Source/Target/Weight/Type` schema) was audited (`src/audit.py`,
`reports/01_repository_audit.md` §4) and found **not** to be the direct raw source of
`data/story_level/`/`data/final/` — its schema and row counts do not correspond. The actual raw
coding source (which printed edition of the Book of Dede Korkut, line-by-line coding notes) is
not present in the repository; this is flagged as a critical open metadata gap in
`validation/source_edition_metadata_required.md`, not guessed at.

`data/story_level/` (633 rows total) and `data/final/` (713 rows in edges+events) differ by +80
rows across 11/14 stories, with no documented transformation rule explaining the difference
(`reports/01_repository_audit.md` §3). This gap is preserved as a disclosed limitation
(`docs/limitations.md`), not resolved by inference.

**Immutability rule:** `data/raw/` and `data/final/` are never modified by this rebuild. All new
work lives under `data/processed/`, `data/derived/`, `outputs/`, and `docs/`.

## 2. Repository Audit and Validation (Phase 1-2)

`src/audit.py` re-derives every headline number the legacy README claims (stories, nodes, edges,
events) directly from `data/final/*.csv`, rather than trusting the README text
(`reports/01_repository_audit.md`). `src/validate.py` then runs a structural validation framework
over the legacy data: node ID uniqueness/format, edge endpoint referential integrity,
layer/polarity/weight/directionality domain checks, self-loop and duplicate-relationship
detection, and alias-dictionary consistency (`reports/02_data_quality_report.md`,
`outputs/validation/summary.json`). Every "duplicate" or "self-loop" flag was individually
inspected before being classified as a real issue or a false positive (e.g., two geographic
epithets sharing a null `satir_no` looked like duplicates but were confirmed as two distinct,
intentionally-added records).

## 3. Canonical Dataset Construction (Phase 3)

`src/build_canonical.py` builds `data/processed/` from `data/final/`:

- **Entity resolution:** exactly one automatic merge was applied
  (`begil_in_adamlari`→`begilin_adamlari`, DEC-002) — a single high-confidence case (identical
  `canonical_name`, identical `node_type`) from `validation/entity_resolution_candidates.csv`.
  Seventeen lower-confidence alias conflicts were left open for manual review
  (`validation/HUMAN_REVIEW_QUEUE.csv`).
- **Schema normalization:** legacy Turkish column names are renamed to the schema documented in
  `docs/data_dictionary.md` (e.g. `karakter_1_id`→`source_id`).
- **Relation taxonomy (DEC-004):** the 17 observed `standard_relation` values are mapped to a
  6-family scheme (SOCIAL, KINSHIP, AUTHORITY, SEMANTIC, OTHER, UNCERTAIN) — an interpretive
  construct, documented in full in `docs/relation_codebook.md`.
- **Aggregation rule (DEC-003):** `relations_aggregated.csv` groups by **unordered** actor pair;
  directionality is preserved via boolean flags rather than lost or arbitrarily assigned.
- **Provenance linkage:** each event-level relation is best-effort matched back to its
  `data/story_level/` source row by exact text match on (source name, target name, raw relation
  text). 90.9% matched uniquely, 8.4% could not be matched (the concrete manifestation of the
  Phase 1 +80-row gap), 0.6% matched ambiguously — all three outcomes are recorded explicitly in
  `provenance.csv`'s `source_row_status`, never silently assumed.

## 4. Network Construction (Phase 4)

Twelve network variants (G0-G11) are built from `data/processed/relations_event_level.csv` by a
single filter predicate per variant, defined once in `src/networks.py::NETWORK_DEFINITIONS` and
documented in `docs/network_models.md`:

| Variant | Definition |
|---|---|
| G0_full | All relations, no filtering |
| G1_person_only | Both endpoints `node_type=='kişi'` |
| G2_core_social | All relations except the SEMANTIC family |
| G3_kinship | `relation_family_top=='KINSHIP'` |
| G4_communication | `relation_family=='communication'` |
| G5_cooperation_support | `relation_family` in {cooperation, support} |
| G6_conflict | `relation_family=='conflict'` |
| G7_positive / G8_negative | `polarity=='pozitif'` / `'negatif'` |
| G9_directed | `directionality=='yönlü'` only, kept directed (DEC-005: undirected relations excluded entirely, never given an arbitrary direction) |
| G10_weighted / G11_unweighted | Same edge set as G0; G11 forces weight=1 |

Undirected variants aggregate multiple event-level relations between the same unordered pair into
one edge (`weight` = sum of `agirlik`). Isolated nodes (0 edges after filtering) are removed from
that variant's graph object only, not from `data/processed/nodes.csv`.

Story-level networks (one per `story_id`) and the actor×story bipartite network (with its
degree-inflation caveat for the co-occurrence projection) are built the same way
(`src/story_networks.py`, `docs/network_models.md`).

## 5. Descriptive and Advanced Analysis (Phase 5-6)

Corpus-level metrics (density, clustering, transitivity, degree assortativity, diameter,
k-core) and centrality (degree, strength, betweenness, harmonic centrality — preferred over
closeness on this disconnected graph — PageRank, eigenvector) are computed per applicable
network (`src/metrics.py`). Community detection uses Leiden (RBConfiguration, resolution=1.0) and
Louvain, both seeded (`config/analysis.yaml::seed=42`), on `G2_core_social` (DEC-007: SEMANTIC
relations excluded from the community substrate). **Critical caveat:** `G2_core_social` has 23
connected components, so a substantial share of the raw community count is a
graph-fragmentation artifact, not meaningful clustering — only structure within the 261-node giant
component is interpreted substantively (`reports/06_advanced_network_analysis_report.md` §1.4).

Signed network analysis (positive/negative degree and strength) and directed network analysis
(triadic census, reciprocity, HITS on G9) follow the same descriptive approach. Structural balance
was explicitly **not computed** — only 13 triangles have a definite sign, below a documented
threshold of 15 (DEC-006). Multilayer/versatility metrics (active layer count, layer participation
coefficient, cross-layer entropy) use the `layer` field. Narrative-order analysis treats
`narrative_order` (from `satir_no`) strictly as within-story sequence, never chronology; stories
with fewer than 6 usable rows are marked `not_applicable` rather than forced into windows.

## 6. Statistical Validation (Phase 7)

Every descriptive structural finding above was tested against a null model: degree-preserving
randomization (`networkx.double_edge_swap`, `n_swaps=10×n_edges`, DEC-008), 1000-member ensemble,
compared on clustering, transitivity, degree assortativity, and Louvain modularity via z-score,
percentile, and empirical p-value. Nine networks × four metrics = 36 tests, corrected with
Benjamini-Hochberg FDR (α=0.05). **Result:** community modularity is validated as a real signal
(not a degree-sequence artifact) in 7/9 networks; degree assortativity is validated in **none** —
the earlier descriptive "disassortative network" observation was retracted
(`reports/07_null_models_report.md` §3.3). This is the single most important correction this
rebuild made to its own earlier findings.

## 7. Sensitivity and Robustness (Phase 8)

Six paired network-construction choices (person+group vs. person-only, weighted vs. unweighted,
all-relations vs. core-social, explicit-only vs. explicit+inferred, groups included vs. excluded,
girizgah included vs. excluded — `config/analysis.yaml::sensitivity.variants`) are compared via
Spearman ρ, Kendall τ, and top-k rank overlap on degree/betweenness/PageRank. Actor-type inclusion
(person+group vs. person-only, ρ=0.887-0.926; groups included vs. excluded, ρ=0.896-0.957) and edge
weighting (PageRank ρ=0.849) changed rankings most; girizgah, core-social filtering and
relation-inference policy had essentially no effect (ρ ≥ 0.97). The three larger-effect choices
are close (mean ρ 0.91-0.93), were not tested against each other, and use different node sets, so
none is called "the most consequential". Structural robustness (random vs. degree-targeted vs.
betweenness-targeted node removal on G0_full, `config/analysis.yaml::robustness`; thresholds
relative to the original 311 nodes; betweenness ranking recomputed every 15 removals) showed the
network is robust to random failure but fragile to targeted attack — a pattern consistent with the
hub-dominated degree distribution found in Phase 5 (`reports/08...`).

## 8. Figures, Tables, and the Web Portal (Phase 11-16)

Publication figures (F02, F03, F06, F07, F15, F16, F17, F18) follow the no-hairball principles of
degree-scaled node size, weight-scaled edge opacity, and labels limited to the highest-degree
nodes with collision-avoiding offsets. Publication tables (T01-T11) are exported as CSV and LaTeX
from the same underlying data as every other output — no table is retyped by hand.

The GitHub Pages site (`docs/`) is generated entirely by `src/build_site_data.py` (JSON export)
and `src/build_site.py` (HTML generation) from these same pipeline outputs; `src/validate_site.py`
crawls every generated page to check for broken links and missing assets before each release
(363/363 pages passing at last check). Every file the site links to or embeds is copied into
`docs/` at build time (`copy_assets()`), because GitHub Pages, when configured to publish from
`/docs`, only serves that subtree — a repo-relative `../outputs/...` link resolves fine on a full
checkout but 404s on the deployed site (DEC-012).

## 9. Reproducibility

`run_pipeline.py --all` runs every stage above in order; `run_pipeline.py --stage <name>` runs one
stage. `tests/` (18 tests, pytest) checks schema integrity, aggregation correctness, network
construction invariants, and determinism (the same seed must reproduce the same Leiden partition
and the same randomized graph). `outputs/manifest_sha256.csv` hashes 192 files for drift detection.
`.github/workflows/validate.yml` runs the test suite and a validation-only pipeline pass on every
push; the heavy null-model/sensitivity/robustness stages are intentionally excluded from CI
(development/analysis stages, not a merge gate).

## 10. What This Project Does Not Claim

- Network centrality is never equated with literary importance.
- Community labels are numeric IDs only — never invented cultural or sociological names.
- `narrative_order` is never treated as historical chronology.
- No inter-annotator reliability statistic (Cohen's kappa, Krippendorff's alpha) is reported —
  this is a single-coder dataset; the infrastructure to compute one exists
  (`validation/inter_annotator_sample.csv`, `src/inter_annotator_stats.py`) and correctly refuses
  to produce a number until real second-coder data exists.
- Degree assortativity is not a validated finding (Phase 7 retraction).
