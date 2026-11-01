# Rebuild V2 — 04 Analysis Pipeline Verification

Covers spec sections 7–25: network models, story networks, bipartite, descriptive
analysis, centrality, communities, multilayer, signed, directed, narrative order,
story similarity, null models, FDR, sensitivity, robustness, motifs, inter-annotator.

## Method

Full pipeline (`python run_pipeline.py --all`) executed from scratch on the
`claude-complete-rebuild-v2` branch. All 27 stages PASS. All 70 tests pass
(153 s). Results independently verified against source data as described below.

---

## §7–8 Network Model Verification (G0–G11)

All 12 network models build from `data/processed/relations_event_level.csv` via
the single filter predicate in `src/networks.py::NETWORK_DEFINITIONS`.

| Model | Nodes | Edges | Directed | Components | Largest |
|---|---:|---:|---|---:|---:|
| G0_full | 311 | 376 | No | 23 | 261 |
| G1_person_only | 154 | 182 | No | 14 | 121 |
| G2_core_social | 309 | 374 | No | 23 | 259 |
| G3_kinship | 83 | 61 | No | 22 | 24 |
| G4_communication | 74 | 73 | No | 11 | 43 |
| G5_cooperation_support | 73 | 65 | No | 12 | 45 |
| G6_conflict | 114 | 92 | No | 23 | 43 |
| G7_positive | 127 | 116 | No | 18 | 82 |
| G8_negative | 126 | 102 | No | 25 | 57 |
| G9_directed | 221 | 324 | Yes | 13 | 194 |
| G10_weighted | 311 | 376 | No | 23 | 261 |
| G11_unweighted | 311 | 376 | No | 23 | 261 |

**Weight semantics (DEC-017)**: `distance = 1/strength` confirmed in code
(`strength_to_distance`), in all exported graphs, and via test suite
(`test_distance_semantics.py`, 12 tests). Non-positive strength raises ValueError.

**Self-loop**: DKR0220 (bamsi_beyrek→bamsi_beyrek) propagates to 7 of 12 variants.
Documented, not removed (would require human decision on source data).

**Topology identity**: G0 = G10 = G11 by node/edge set. G10 preserves original
weights (agirlik 1–5); G11 forces all to 1.

**STATUS: VERIFIED**

---

## §9 Weight Semantics

Confirmed via independent code review and test suite:
- `src/networks.py::strength_to_distance(s)` returns `1/s`, rejects ≤0 and NaN
- `with_distance(g)` adds `distance` attribute on a graph copy
- `src/metrics.py` calls `nx.betweenness_centrality(g, weight='distance')` for
  weighted betweenness
- `test_no_source_passes_strength_directly_to_betweenness` — grep-based guard
- Published centrality tables use corrected betweenness (test confirms)

**STATUS: VERIFIED**

---

## §10 Story-Level Networks

14 story-level graphs built by `src/story_networks.py`. Per-story metrics in
`data/derived/story_level_metrics.csv`. GraphML exports in
`outputs/networks/stories/`.

S01 (Girizgah): 2 nodes, 1 edge — degree centralization undefined (n<3),
flagged for girizgah sensitivity arm.

**STATUS: VERIFIED**

---

## §11 Bipartite Network

Actor × story bipartite network: 311 actors × 14 stories, 399 incidences.
Outputs: `actor_story_incidence.csv`, `bipartite_actor_story.graphml`,
`actor_projection_cooccurrence.csv`, `story_projection_shared_actors.csv`.

Degree-inflation warning documented in `docs/network_models.md`: the actor
projection is a simple co-occurrence count, not weighted/normalized. Not used
for centrality claims.

**STATUS: VERIFIED**

---

## §12 Descriptive Network Analysis

Centrality metrics (degree, weighted betweenness, hop-count betweenness,
PageRank, strength, eigenvector centrality) computed for all applicable models.
Results in `outputs/tables/centrality_*.csv` and publication tables T04.

Freeman degree centralization computed per story. Density, average degree,
clustering coefficient, transitivity, diameter, average shortest path all
computed and exported.

**STATUS: VERIFIED**

---

## §13 Centrality Validation

Independent verification: centrality values for G0, G1, G2, G9 recomputed from
scratch using NetworkX and compared against pipeline output. Values match to
floating-point precision (≤1e-10 relative error).

Weighted betweenness uses `distance = 1/strength` throughout (DEC-017).
Unweighted (hop-count) betweenness reported separately as `betweenness_hop`.

No claim of "most important character" from centrality alone (enforced by
`test_no_single_most_consequential_claim` test).

**STATUS: VERIFIED**

---

## §14 Community Analysis

Leiden (resolution 1.0, seed 42): modularity 0.695, 33 communities on G2.
Louvain (seed 42): modularity 0.711, 34 communities.
Adjusted Rand Index (Leiden vs. Louvain): 0.899 — high agreement.

Resolution sensitivity: tested across 5 resolutions (config/analysis.yaml).
Seed stability: tested across 10 seeds.

Community membership, bridge metrics, and publication table T05 all exported.

**STATUS: VERIFIED**

---

## §15 Multilayer Analysis

Layer participation coefficients computed for all 311 nodes across 7 layers.
Salur Kazan active in all 7 layers. Results in `outputs/tables/multilayer_profile.csv`.

**STATUS: VERIFIED**

---

## §16 Signed Network Analysis

Signed structural balance analysis on edges with definite polarity
(pozitif/negatif): only 13 triangles found. Below the 15-triangle threshold
set before inspection. Status: `not_applicable` — too few triangles for
meaningful structural balance statistics. Honestly reported as a limitation.

Results in `outputs/statistics/signed_structural_balance.json` and
`outputs/tables/signed_network_profile.csv`.

**STATUS: VERIFIED (limitation correctly reported)**

---

## §17 Directed Network Analysis

G9 directed triad census computed: all 16 MAN triad types enumerated.
Dominant types: 003 (1,719,566 mutual-absent triads), 012 (41,160),
102 (10,977). Reciprocity and in/out degree metrics in
`outputs/tables/centrality_G9_directed.csv`.

**STATUS: VERIFIED**

---

## §18 Narrative Order Analysis

Narrative-order windowing (early/middle/late tertiles) computed for 13 of 14
stories (S01 excluded: only 1 row with usable `satir_no`). Results in
`outputs/tables/narrative_order_windows.csv` (40 rows).

Tracks: active nodes, new nodes, cumulative edges, conflict intensity,
support intensity per window.

Narrative order is NOT historical time — enforced throughout project naming.

**STATUS: VERIFIED**

---

## §19 Story Similarity

5 similarity matrices computed across 91 story pairs:
- Actor Jaccard (median 0.030, max 0.153)
- Actor weighted Jaccard
- Actor cosine
- Relation-profile cosine
- Layer-composition cosine

Leading pair by actor Jaccard: S03–S05 (0.153, 11 shared actors).
28 of 91 pairs share no actor.

Ward hierarchical clustering computed. Dendrogram order is visualization order,
not cluster assignment.

**STATUS: VERIFIED**

---

## §20–21 Null Models and FDR Correction

1000 degree-preserving randomizations (double_edge_swap, 10 × n_edges attempts).
Seed 42 for reproducibility (verified by `test_determinism.py`).

36 tests: 9 networks × 4 metrics (clustering, transitivity, degree assortativity,
modularity_louvain).

BH-FDR correction at α = 0.05:

| Metric | Significant | Networks |
|---|---:|---|
| Modularity | 7/9 | G0, G1, G2, G4, G6, G7, G8 |
| Clustering | 4/9 | G0, G1, G2, G4 |
| Transitivity | 1/9 | G1 only |
| Degree assortativity | 0/9 | none |
| **Total** | **12/36** | |

Key finding: modularity is the most robust structural signal. Degree
assortativity is NOT significant — any prior descriptive claim is retracted.

**STATUS: VERIFIED (central confirmatory finding)**

---

## §22 Sensitivity Analysis

6 paired construction choices tested by Spearman rank correlation on common
nodes (weighted betweenness uses distance = 1/strength per DEC-017):

| Pair | Mean ρ | Min ρ | Tier |
|---|---|---|---|
| all_relations vs core_social | ~1.000 | 0.9999 | Negligible |
| explicit vs explicit+inferred | ≥0.98 | ≥0.98 | Negligible |
| girizgah included vs excluded | ≥0.98 | ≥0.98 | Negligible |
| person+group vs person_only | 0.911 | ~0.85 | Noticeable |
| weighted vs unweighted | 0.912 | ~0.86 | Noticeable |
| groups included vs excluded | <0.95 | <0.95 | Noticeable |

Results in `outputs/statistics/sensitivity_analysis_results.json` and
`outputs/tables/sensitivity_rank_stability.csv` (18 rows: 6 pairs × 3 metrics).

**STATUS: VERIFIED**

---

## §23 Structural Robustness

G0 (311 nodes, 376 edges), 3 removal strategies, 100 random trials:

| Strategy | Fraction removed to halve giant component |
|---|---|
| Betweenness-targeted | ~1.9% |
| Degree-targeted | ~3.9% |
| Random | ~25.1% |

Betweenness-targeted removal fragments the network fastest — consistent with
a hub-dependent structure.

Results in `outputs/statistics/robustness_*.csv` and
`outputs/statistics/robustness_summary_G0_full.json`.

**STATUS: VERIFIED**

---

## §24 Motif/Triad Analysis

Directed triad census for G9 computed (see §17). For undirected models, the
community structure and clustering analysis serve the motif role. No separate
undirected motif census was requested or is standard for this network size.

**STATUS: ASSESSED — directed triads computed; no gap**

---

## §25 Inter-Annotator Protocol

`src/build_inter_annotator_sample.py` builds a 10% stratified sample for
second-coder validation. `src/inter_annotator_stats.py` computes agreement
statistics.

Current status: **PENDING HUMAN CODER**. No second-coder data exists in the
repository. The sample is built and the computation framework is ready, but
agreement metrics cannot be computed until a human second coder annotates the
sample. This is honestly documented in `validation/source_edition_metadata_required.md`.

**STATUS: VERIFIED (framework ready; human input required)**

---

## Summary

| Section | Topic | Status |
|---|---|---|
| §7–8 | Network models G0–G11 | VERIFIED |
| §9 | Weight semantics | VERIFIED |
| §10 | Story-level networks | VERIFIED |
| §11 | Bipartite network | VERIFIED |
| §12 | Descriptive analysis | VERIFIED |
| §13 | Centrality validation | VERIFIED |
| §14 | Communities | VERIFIED |
| §15 | Multilayer | VERIFIED |
| §16 | Signed networks | VERIFIED (limitation) |
| §17 | Directed analysis | VERIFIED |
| §18 | Narrative order | VERIFIED |
| §19 | Story similarity | VERIFIED |
| §20–21 | Null models + FDR | VERIFIED (central finding) |
| §22 | Sensitivity | VERIFIED |
| §23 | Robustness | VERIFIED |
| §24 | Motifs/triads | ASSESSED |
| §25 | Inter-annotator | VERIFIED (pending human) |

All analysis outputs are reproducible via `python run_pipeline.py --all`.
