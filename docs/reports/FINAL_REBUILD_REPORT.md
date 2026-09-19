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
claim is retracted as a result (not supported after FDR correction; it is not proof that no
disassortativity exists). The kinship network (G3) shows no detectable deviation from its null
model on any tested metric — reported rather than omitted; note that G3 is a forest (83 nodes,
61 edges, 22 components), so its clustering/transitivity are structurally zero and only its
assortativity and modularity tests are informative. →
`reports/07_null_models_report.md`.

## Sensitivity

Six paired network-construction choices tested by rank correlation. Actor-type inclusion
(person+group vs. person-only, ρ=0.887-0.926; groups included vs. excluded, ρ=0.896-0.957) and edge
weighting (ρ=0.849-1.000, PageRank most affected) change centrality rankings noticeably; person+group
vs. person-only has the lowest mean ρ (0.91) but weighting is lower for PageRank (0.85), and the
differences among these three are small and untested. Girizgah inclusion, core-social filtering and
relation-inference policy have negligible effect (ρ ≥ 0.97). Structural robustness (G0_full): the
network needs ~25% random node loss (78 of 311 nodes) before its largest component falls below half
of the original node count, but only ~2-4% (6-12 nodes; resolution is one 6-node step) under
degree- or betweenness-targeted attack — a classic robust-yet-fragile pattern, framed strictly as
graph connectivity, never narrative resilience. →
`reports/08_sensitivity_robustness_report.md`, `outputs/statistics/audit_top5_checks.json`.

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
   networks after Benjamini-Hochberg correction (α=0.05; z = 2.6-7.0, all positive; G3_kinship and
   G5 not significant). Audit check: the result also holds on the largest connected component of
   G0_full alone (observed 0.692 vs. null mean 0.615, z=9.9, p=0.001), so it is not an artifact of
   the 23-component fragmentation. Scope: this validates non-random modular organization, not
   independently discovered social communities (numeric labels only; whether communities align
   with story boundaries was not tested). Louvain, not Leiden, was used in the null ensemble.
   **Confirmatory.**
   (`reports/07_null_models_report.md` §2; `outputs/statistics/null_model_fdr_corrected.csv`;
   `outputs/statistics/audit_top5_checks.json` A)
2. **A prior descriptive finding did not survive statistical validation and is withdrawn.**
   All twelve network variants show negative degree assortativity (−0.11 to −0.33), but it is not
   statistically significant in any of the nine networks tested against a null model (lowest
   q=0.089, G0_full, nominal p=0.032). The observed values are negative, but not more extreme than
   degree-preserving random graphs produce (z of mixed sign). The "disassortative network" claim is
   withdrawn as unsupported; this is absence of evidence, not proof of no disassortativity.
   **Confirmatory (negative).** (`reports/07_null_models_report.md` §3.3;
   `outputs/statistics/null_model_fdr_corrected.csv`)
3. **Actor-type inclusion and edge weighting are the construction choices that most change
   centrality rankings; the others barely matter.** Of six paired modeling choices, person+group vs.
   person-only (ρ=0.887-0.926; mean ρ 0.91, lowest), groups included vs. excluded (ρ=0.896-0.957) and
   weighted vs. unweighted (ρ=0.849-1.000; lowest for PageRank, 0.85) change rankings noticeably,
   while relation-inference policy, core-social filtering and prologue (girizgah) inclusion have
   negligible effect (ρ ≥ 0.97). Rankings stay broadly stable overall (all ρ ≥ 0.85). The earlier
   phrasing "the single most consequential decision, by a wide margin" is **not** supported: the
   three larger-effect choices differ by only ~0.02 in mean ρ, node sets differ across pairs
   (n=154-311), and no test of differences between ρ values was run. **Descriptive/sensitivity
   result, not confirmatory.** (`reports/08_sensitivity_robustness_report.md` §2;
   `outputs/tables/sensitivity_rank_stability.csv`; `outputs/statistics/audit_top5_checks.json` C)
4. **The kinship sub-network shows no detectable deviation from its degree-preserving null.**
   All four tested metrics (clustering, transitivity, assortativity, modularity) have q ≥ 0.67. G3
   is a forest (83 nodes, 61 edges, 22 components, no triangles), so clustering and transitivity
   are structurally zero and those two tests are uninformative; the informative tests are
   assortativity (z≈0) and modularity (z=0.8, observed 0.871, itself high in the null because a
   sparse forest is naturally modular). Read as "no evidence of extra structure in a sparse, acyclic
   kinship coding", not as evidence that kinship ties are literarily unimportant. **Confirmatory
   (negative), low power.** (`reports/07_null_models_report.md` §3.4;
   `outputs/statistics/audit_top5_checks.json` B)
5. **The corpus network (G0_full) is robust to random disruption but fragile to targeted attack.**
   Its largest component falls below 50% of the original node count (311) after ~25% random removal
   (78 nodes; mean of 100 trials), versus ~2-4% (6-12 nodes) under degree- or betweenness-targeted
   removal. Caveats: the threshold is relative to all 311 nodes, not to the original 261-node giant
   component; targeted crossings are resolved only to one 6-node step; degree ranking is recomputed
   after every removal but betweenness only every 15 removals; only G0_full was tested. Consistent
   with (not proof of) the hub-dominated structure found elsewhere. **Descriptive (graph
   connectivity only).** (`reports/08_sensitivity_robustness_report.md` §3;
   `outputs/statistics/robustness_summary_G0_full.json`; F18; `outputs/statistics/audit_top5_checks.json` D)

Claim-to-evidence status after the DEC-015 audit: 5/5 verified against their output files, correct
network model, and effect direction; #3 and #4 and #2 reworded (scope and strength), #1 and #5 gained
explicit caveats. No claim above concerns literary or historical importance of any character — each
is a statement about structural properties of this specific encoded relational dataset.

---

## Post-Release Addendum: Story Similarity (RQ6) — Metric Suite Built, Then Audited

After the 21-phase delivery above, the user asked to continue with optional future work. The
story-similarity metric suite (previously this project's one open research question, RQ6) was
built: `src/story_similarity.py` computes actor Jaccard, weighted Jaccard, cosine, relation-
profile, and layer-composition similarity across all 91 story pairs, plus a Ward hierarchical
clustering on each story's relation-family/layer profile (`docs/decision_log.md` DEC-014).
Figures F10-F11 and the full T08 table were added. RQ6 was first recorded as "answered".

**Final academic audit (DEC-015) — RQ6 is PARTIALLY ANSWERED / EXPLORATORY.** Audit of the
existing artifacts, plus low-cost validity checks (`src/story_similarity_validity.py`), found:

- **Overlap is low.** Actor Jaccard median 0.030, max 0.153; 28 of 91 pairs share no actor. S03–S05
  (0.153) is the *relatively most overlapping* pair among the evaluated stories, not a strongly
  similar pair. It is top only on the two Jaccard measures (rank 6–7 of 91 on the three cosine
  measures, each with a different top pair).
- **Cosine values are high by construction.** Observed max relation-profile cosine 0.985 vs. a
  permutation-baseline 95th percentile of the pair maximum of 0.987.
- **Discrete clusters are not robustly supported.** Ward always yields a dendrogram. Silhouette
  0.37–0.56 (k=2–6; the k=2 split only isolates the 1-relation S01), bootstrap ARI 0.54–0.79,
  linkage methods disagree at k=4–5, Ward cophenetic r=0.73; no k passes the pre-set rule
  (silhouette > 0.50, ARI ≥ 0.75, permutation p < 0.05), with or without S01. Stories do differ
  more than sampling noise (silhouette > permutation baseline for k ≥ 3), which is equally
  consistent with a continuum.
- **Unsupported interpretation removed.** "Shared captivity theme" for S03/S05 was not a coded
  variable in the canonical dataset (no structured theme field; S03's free-text relation phrases
  contain none of esir/esaret/tutsak/kurtar/yağma, S05's contain them in 2 of 40 rows) and was
  removed as a finding (S12, not S03/S05, is the boy whose title names Kazan's captivity and Uruz's
  rescue).
- **Reproducibility defect fixed.** `run_pipeline.py --all` had no story-similarity stage, and
  `export_tables.py` would have overwritten the full T08 with the older partial projection; both
  fixed.

Accepted wording: "Story-level similarity can be quantified and visualized, but evidence for a
robust discrete clustering structure is limited." Paper, thesis, website, and reports use it
consistently. The four open release blockers (source edition, inter-annotator reliability,
merged-entity review, CITATION.cff metadata) are unchanged.
