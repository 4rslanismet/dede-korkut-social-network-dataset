# Final Rebuild Report

**Project:** Dede Korkut Narrative Network Project (DKNN) — working title
**Branch:** `claude-dk-rebuild` (never merged to `main`, never pushed to remote)
**Scope:** Full rebuild per `docs/MASTER_PROMPT.md` (147-item specification), Phases 1-21

This report synthesizes `reports/01` through `reports/17`, `paper/`, and `thesis/` into one
capstone document per master prompt section 124. It does not introduce new findings — every claim
below is cited to the report or output file that established it.

---

## Initial State

The repository, as cloned, contained a legacy v3 dataset (`data/final/`): 333 nodes, 628 edges, 85
narrative events across 14 stories, documented in `README.md`, `docs/README_v2.md`, and
`docs/README_v3.md`. A raw Excel workbook (`data/raw/`) and per-story coding files
(`data/story_level/`) were also present. No validation framework, network models, statistical
testing, sensitivity analysis, figures, tables, website, or academic output packages existed.

## Data Audit

`src/audit.py` re-derived every headline number the legacy README claimed, rather than trusting
it — all four (14/333/628/85) were confirmed accurate. Two critical provenance gaps were found and
documented rather than assumed away: (1) `data/story_level/` (633 rows) and `data/final/` (713
rows in edges+events) differ by +80 rows across 11/14 stories with no documented transformation
rule; (2) `data/raw/*.xlsx` does not correspond, in schema or row count, to the processed data —
the actual raw coding source (which print edition of the Book of Dede Korkut) is unrecorded.
→ `reports/01_repository_audit.md`.

## Data Corrections

A 26-check structural validation framework (`src/validate.py`) found 0 FAIL-level integrity
issues (no duplicate node IDs, no orphan edge endpoints, no missing endpoints) and several
WARNING-level issues, each individually inspected: one true entity duplication
(`begil_in_adamlari`/`begilin_adamlari`, merged — DEC-002), one unexpected self-loop (not
resolved, flagged), and two apparent "duplicate" relationship rows that on inspection were
confirmed as two distinct, intentionally-coded epithet records sharing a null narrative-order
field (not a bug). → `reports/02_data_quality_report.md`.

## Preserved Decisions

Thirteen methodological decisions are logged with rationale in `docs/decision_log.md`
(DEC-001–DEC-013), covering: which entity merge to apply and which to leave open (DEC-002),
the unordered-pair aggregation rule (DEC-003), the relation-family taxonomy mapping (DEC-004),
directed-network construction excluding undirected relations rather than assigning them an
arbitrary direction (DEC-005), the structural-balance and motif-analysis minimum-sample thresholds
(DEC-006, DEC-010), the community-detection substrate choice (DEC-007), the null-model method and
FDR correction (DEC-008), the sensitivity-pair construction (DEC-009), and two website-build fixes
found and resolved mid-project (DEC-012, DEC-013).

## Canonical Model

`data/processed/` (`src/build_canonical.py`): 332 actors (one merge applied), 628 event-level
relations (zero data loss from the legacy edge table), 376 aggregated unordered actor pairs, a
17-type relation taxonomy mapped to 6 interpretive families, and a per-relation provenance record
with an explicit match/no-match status (never silently assumed). Full schema:
`docs/data_dictionary.md`. → `reports/03_canonical_dataset_report.md`.

## Network Models

Twelve variants (G0-G11), each a single auditable filter predicate in `src/networks.py`: full,
person-only, core-social, four relation-family-restricted networks (kinship, communication,
cooperation/support, conflict), positive/negative polarity networks, a directed network, and
weighted/unweighted variants. Plus 14 story-level networks and an actor×story bipartite network
(with its degree-inflation caveat disclosed, never used for centrality claims). →
`docs/network_models.md`, `reports/04_05_network_construction_and_descriptive_report.md`.

## Analyses

Descriptive corpus/centrality metrics; Leiden and Louvain community detection (stable across
seeds, ARI=0.899 between algorithms) with an explicit caveat that 23 connected components inflate
the raw community count; signed-network profile (structural balance correctly judged
inapplicable — 13 triangles below a documented threshold of 15); directed-network analysis
(triadic census, reciprocity=0.358, HITS); multilayer versatility (Salur Kazan active in all 7
layers); narrative-order windowing (13/14 stories) and exploratory dynamic-centrality trajectories.
→ `reports/06_advanced_network_analysis_report.md`.

## Statistical Validation

The project's central methodological contribution. Nine networks × four metrics = 36 null-model
tests (degree-preserving randomization, 1000-member ensemble, Benjamini-Hochberg FDR α=0.05).
**Modularity validated as a real signal (not a degree-sequence artifact) in 7/9 networks.
Degree assortativity validated in 0/9 networks** — an earlier descriptive "disassortative network"
claim is retracted as a result. The kinship network (G3) is indistinguishable from its null model
on every tested metric, a genuine negative result reported rather than omitted. →
`reports/07_null_models_report.md`.

## Sensitivity

Six paired network-construction choices tested by rank correlation. Person+group vs. person-only
produces the largest disagreement of any pair tested (Spearman ρ=0.887-0.926) — the single most
consequential modeling decision. Girizgah inclusion and core-social filtering have negligible
effect (ρ=1.000). Structural robustness: the network tolerates ~25% random node loss before its
giant component halves, but only ~2-4% under targeted (degree/betweenness) attack — a classic
robust-yet-fragile pattern, framed strictly as graph connectivity, never narrative resilience. →
`reports/08_sensitivity_robustness_report.md`.

## Key Findings

See "Top 5 Strongest Defensible Findings" below.

## Limitations

Seventeen itemized limitations, consolidated in `docs/limitations.md`: unknown source edition,
single coder, the undocumented story-level/final transformation gap, 29.6% "belirsiz" relation
coverage, group-actor sensitivity effects, inferred-relation effects, undocumented edge-weight
semantics, narrative-order-is-not-chronology, bipartite projection artifacts, entity-resolution
uncertainty, the 5 concatenated-multi-actor nodes (found while building the website), the
retracted assortativity claim, the connected-component community-count artifact, the skipped
motif analysis, the incomplete story-similarity analysis, website scope limits, and the general
interpretation-limits disclaimer carried on every relevant page of the site.

## Website

A 363-page GitHub Pages site (`docs/`) — all 14 navbar sections from the project brief, a
Cytoscape.js network explorer (3 of 12 variants), and a generated profile page for every one of
the 332 canonical actors, not just a top-N subset. Built entirely from pipeline outputs
(`src/build_site_data.py`, `src/build_site.py`); validated with a custom link/asset crawler
(`src/validate_site.py`, 363/363 pages passing). Two significant bugs were found and fixed only by
testing against a real local HTTP server rather than a `file://` preview: relative links that
would 404 on an actual GitHub Pages deployment, and a 239-character node ID exceeding the
filesystem path limit. → `reports/15_16_web_portal_report.md`.

## Reproducibility

`run_pipeline.py` orchestrates all 19 implemented stages (`--all`/`--stage`/`--fast`/
`--validate-only`); 18 automated tests (schema, aggregation, network-construction invariants,
determinism) all pass; a 192-file SHA-256 hash manifest and a 42-package pinned lockfile support
drift detection; a GitHub Actions workflow runs the test suite and a validation-only pipeline pass
on every push (heavy null-model/sensitivity stages intentionally excluded from CI). →
`reports/13_14_reproducibility_report.md`.

## Academic Outputs

`paper/` (manuscript outline, methods, results, supplementary material, 8 figures, 22 table
files) and `thesis/` (proposed structure, a research-question-by-research-question honesty
assessment — RQ6 explicitly marked not-yet-answerable rather than force-answered — methodology and
results mappings, figure/table inventories). → `reports/17_documentation_report.md` and the
`paper/`/`thesis/` directories directly.

## Future Work

1. Obtain a real second coder and complete `validation/inter_annotator_sample.csv` to compute a
   genuine inter-annotator reliability statistic.
2. Resolve the 5 concatenated-multi-actor nodes (DEC-013) by returning to the original narrative
   text.
3. Build the full story-similarity metric suite (Jaccard, cosine, relation-profile,
   layer-composition, hierarchical clustering) to properly answer RQ6.
4. Confirm the source edition/transcription used for the original coding
   (`validation/source_edition_metadata_required.md`).
5. Extend the Network Explorer to all 12 network variants; build the remaining F01/F04-F05/F08-F14
   figures.
6. Deploy the site to a live GitHub Pages URL and, when the repository owner is ready, push
   `claude-dk-rebuild` to the remote and decide on a merge strategy with `main`.
7. Fill in `CITATION.cff`'s TODO fields once the repository owner's identity and any forthcoming
   publication details are confirmed.

---

## Top 5 Strongest Defensible Findings

Selected for defensibility, not novelty-for-its-own-sake (per the project's own discipline: "az
ama güvenilir sonuç" — few but reliable results).

1. **Community modularity is a validated structural signal, not a degree-sequence artifact.**
   Louvain modularity exceeds a 1000-member degree-preserving null ensemble in 7 of 9 tested
   networks after Benjamini-Hochberg correction (α=0.05). (`reports/07_null_models_report.md` §2)
2. **A prior descriptive finding did not survive statistical validation and is retracted.**
   All twelve network variants show negative degree assortativity, but this is not statistically
   significant in any of the nine networks tested against a null model — the "disassortative
   network" claim is withdrawn. (`reports/07_null_models_report.md` §3.3)
3. **Person+group vs. person-only actor inclusion is the single most consequential
   network-construction decision tested.** Of six paired modeling choices, this one produces the
   largest centrality-rank disagreement (Spearman ρ=0.887-0.926), while prologue inclusion and
   semantic-relation filtering have essentially no effect (ρ=1.000).
   (`reports/08_sensitivity_robustness_report.md` §2)
4. **The kinship sub-network is a genuine null result.** All four tested structural metrics
   (clustering, transitivity, assortativity, modularity) are statistically indistinguishable from
   a degree-preserving random network, consistent with a sparse, tree-like kinship coding.
   (`reports/07_null_models_report.md` §3.4)
5. **The corpus network is robust to random disruption but fragile to targeted attack.**
   Random removal of ~25% of nodes is needed to halve the giant component, versus only ~2-4% under
   adaptive degree- or betweenness-targeted removal — consistent with, and explaining, the
   hub-dominated structure found elsewhere in this study.
   (`reports/08_sensitivity_robustness_report.md` §3)

No claim above concerns literary or historical importance of any character — each is a
statement about structural properties of this specific encoded relational dataset.
