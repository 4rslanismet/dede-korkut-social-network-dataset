# CURRENT PROJECT STATUS

PHASES 1-6 COMPLETE AND COMMITTED.

NEXT:
PHASE 7 — NULL MODELS / STATISTICAL VALIDATION

## Start by reading (in this order)

1. `CLAUDE_SESSION_HANDOFF.md` — full state, verified numbers, what's done vs. not
2. `docs/MASTER_PROMPT.md` — the original 147-item project specification
3. `reports/06_advanced_network_analysis_report.md` — Phase 6 results (community detection,
   signed/directed, multilayer, narrative-order/dynamic centrality)
4. `config/analysis.yaml` — `null_models.n_random` (1000), `null_models.model`
   (`configuration_model`), `seed` (42)
5. `docs/network_models.md`, `docs/decision_log.md`

**Do not rebuild Phases 1-6.** Everything through Phase 6 (repository audit, validation,
canonical dataset, G0-G11 network construction, descriptive metrics, community detection,
signed/directed analysis, multilayer profile, narrative-order/dynamic centrality) is done and
verified — re-derive numbers from the actual files if you need to check something, but don't
re-run the pipeline from scratch.

## First task — Phase 7: Null Models / Statistical Validation

1. Create `src/null_models.py`. For the primary network variants (start with `G0_full`,
   `G1_person_only`, `G2_core_social`; add `G9_directed` if a directed-appropriate null model is
   used), generate a degree-preserving randomized ensemble (`networkx`'s configuration-model-style
   double-edge-swap on a copy of the graph, or `nx.random_reference`/`nx.expected_degree_graph`
   equivalent — pick one, document the choice as a new DEC-### entry in `docs/decision_log.md`).
2. For each network, compare **observed vs. random ensemble** on: clustering coefficient,
   transitivity, degree assortativity, modularity (Leiden, resolution=1.0, same seed as Phase 6).
   Report `observed`, `random_mean`, `random_std`, `z_score`, `percentile`, `empirical_p` for each.
3. Use `config/analysis.yaml::null_models.n_random` (1000) for the full run. Add a `--fast` mode
   (e.g. n_random=100 or a CLI/env override) for development so iteration doesn't require waiting
   on 1000 randomizations every time — document which mode produced which numbers in the report.
4. `config/analysis.yaml::seed` (42) must seed everything; record the seed in the output.
5. If a metric/network combination is not statistically meaningful (e.g. too few edges/triangles
   for a stable null distribution — see Phase 6's own precedent with the 13-triangle signed-balance
   case), mark it `not_applicable` with a stated reason. Do not force a z-score out of a
   degenerate distribution.
6. Write `reports/07_null_models_report.md` with the same rigor as Phase 6's report (observed
   numbers, what's descriptive vs. statistically validated, limitations).
7. Update `CLAUDE_SESSION_HANDOFF.md`, `NEXT_TASK.md`, `project_state.json`, and
   `docs/decision_log.md` (if new methodological decisions were made), then commit:
   `Complete Phase 7 null models and statistical validation`

## Then continue in master-plan order (see CLAUDE_SESSION_HANDOFF.md → "REMAINING MASTER PLAN")

PHASE 8 sensitivity -> PHASE 9 structural robustness -> PHASE 10 motif/triad (only if
methodologically sound) -> PHASE 11 figures -> PHASE 12 tables -> PHASE 13 inter-annotator
infrastructure -> PHASE 14 reproducibility/pipeline -> PHASE 15 web portal -> PHASE 16 website
validation -> PHASE 17 documentation -> PHASE 18 paper package -> PHASE 19 thesis package ->
PHASE 20 final validation/release -> PHASE 21 final reports.

Update the three checkpoint files + decision log after each completed phase and commit locally.

## Rules that must not be relaxed

- Never invent unsupported data, metadata, or academic findings.
- Centrality ≠ literary importance — always frame centrality/community/bridge results as
  preliminary/structural, pending the statistical validation this phase is building.
- If an analysis can't be meaningfully run on this data (too sparse, too few cases), mark it
  `not_applicable` with a stated reason — do not force a number out of it (Phase 6 already set
  this precedent with the signed-balance and multilayer analyses).
- `data/raw/` and `data/final/` stay untouched. All new work lives under `data/processed/`,
  `data/derived/`, `outputs/`, `docs/`, `reports/`.
- No merge/push to `main`. No force-push. Local commits on `claude-dk-rebuild` only.
