# CURRENT PROJECT STATUS

PHASES 1-8 COMPLETE AND COMMITTED (repository audit, validation, canonical dataset, G0-G11
networks, descriptive metrics, community/signed/directed/multilayer/narrative-order analysis,
null-model statistical validation, sensitivity analysis, structural robustness).

NEXT:
PHASE 9/10 (motif/triad, only if methodologically sound) THEN PHASE 11 — PUBLICATION FIGURES

## Start by reading (in this order)

1. `CLAUDE_SESSION_HANDOFF.md` — full state, verified numbers
2. `docs/MASTER_PROMPT.md` — original spec (section 48 for figure list F01-F18, section 47 for
   visualization principles)
3. `reports/08_sensitivity_robustness_report.md` — most recent results
4. `docs/decision_log.md` (DEC-001 through DEC-009)

**Do not rebuild Phases 1-8.** Reuse existing outputs: `src/networks.py::build_all_networks()`
for graphs, `outputs/tables/centrality_*.csv`, `outputs/statistics/*.json`,
`outputs/tables/community_membership_G2_core_social.csv`,
`outputs/statistics/null_model_fdr_corrected.csv`,
`outputs/tables/sensitivity_rank_stability.csv`,
`outputs/statistics/robustness_*_G0_full.csv`.

## Task A — Motif/Triad (Phase 9-10, only if sound)

G9_directed's triadic census already exists (`outputs/statistics/directed_triad_census_G9.json`,
Phase 6) but has no null-model comparison. Given the network's sparsity (the "003" disconnected
category dominates: 1,719,566 of ~1.77M triads), a naive per-category z-test would be unstable.
If you attempt this, aggregate the closed-triad categories (030T, 030C, 120D, 120U, 120C, 210,
300 — 43 triads total) into one count and compare that single count against a
`double_edge_swap`-based directed null ensemble (networkx doesn't have a built-in directed
double-edge-swap that preserves both in- and out-degree sequences exactly — check
`nx.directed_configuration_model` or implement a directed double-edge-swap; document the choice
as DEC-010). If the sample is still too thin to support a meaningful comparison, mark it
`not_applicable` with the reason — don't force a result.

## Task B — Publication Figures (Phase 11, master prompt section 48)

Create `src/visualization.py`. Follow section 47's rules: no hairballs, weighted edge opacity,
degree/centrality-based node size, community-based layout where relevant, selective labeling
(don't try to label every node). Output PNG at minimum (SVG/PDF if straightforward with
matplotlib). Priority order (these already have all the underlying data computed):

- F02 corpus full network (G0_full, sized/colored by degree, sparse labels)
- F03 person-only network (G1_person_only)
- F06 community structure (G2_core_social, colored by Leiden community — **must include the
  23-connected-component caveat in the caption/methodology note**, don't let the figure imply
  33 meaningful communities without that caveat)
- F07 top actors centrality comparison (bar/dot plot across degree/betweenness/pagerank from
  `outputs/tables/centrality_G0_full.csv`)
- F15 null-model distributions (histogram of random ensemble vs observed value, for the 12
  FDR-significant tests at minimum — `outputs/null_models/null_model_results_full.json`)
- F16 sensitivity correlation matrix (heatmap of Spearman rho across the 6 sensitivity pairs x
  3 metrics — `outputs/tables/sensitivity_rank_stability.csv`)
- F18 structural robustness curves (largest-component-fraction vs fraction-removed, 3 strategies
  overlaid — `outputs/statistics/robustness_*_G0_full.csv`)

Then remaining figures as time allows: F04 (core social), F05 (multilayer overview), F08 (story
metrics comparison), F09 (bipartite), F10/F11 (story similarity — not yet computed, may need to
build first), F12 (layer participation), F13 (positive/negative comparison), F14 (narrative-order
evolution), F17 (centrality rank stability, related to F16).

## Task C — Publication Tables (Phase 12, master prompt section 49, T01-T11)

Most of the underlying data already exists as CSV. Write a script that assembles the specific
T01-T11 tables (dataset overview, relation taxonomy, story-level statistics, centrality results,
community statistics, layer-specific metrics, actor-story participation, story similarity, null
model tests, sensitivity analysis, robustness results) and exports both CSV and LaTeX
(`\begin{tabular}`) versions under `outputs/tables/publication/`.

## Then continue in master-plan order

PHASE 13 inter-annotator infrastructure -> PHASE 14 reproducibility/pipeline (run_pipeline.py,
tests/, hash manifest) -> PHASE 15 web portal -> PHASE 16 website validation -> PHASE 17
documentation -> PHASE 18 paper package -> PHASE 19 thesis package -> PHASE 20 final
validation/release -> PHASE 21 final reports.

Update `CLAUDE_SESSION_HANDOFF.md`, `NEXT_TASK.md`, `project_state.json`, and
`docs/decision_log.md` after each completed phase, then commit locally.

## Rules that must not be relaxed

- Never invent unsupported data, metadata, or academic findings.
- Centrality ≠ literary importance.
- Mark `not_applicable` rather than forcing a result on insufficient data.
- `data/raw/` and `data/final/` stay untouched.
- No merge/push to `main`. No force-push. Local commits on `claude-dk-rebuild` only.
- Degree assortativity is not a validated finding (Phase 7) - don't cite it as fact.
- Any figure/table showing G2_core_social community structure must carry the 23-connected-
  component caveat (Phase 6 section 1.4).
- When writing git commit messages with PowerShell here-strings, avoid embedded double quotes
  (they can cause the native command line to be mis-split) — prefer plain text or write the
  message to a temp file and use `git commit -F <file>`.
