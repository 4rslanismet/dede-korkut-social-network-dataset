# CURRENT PROJECT STATUS

PHASES 1-7 COMPLETE AND COMMITTED.

NEXT:
PHASE 8 — SENSITIVITY / ROBUSTNESS ANALYSIS

## Start by reading (in this order)

1. `CLAUDE_SESSION_HANDOFF.md` — full state, verified numbers, what's done vs. not
2. `docs/MASTER_PROMPT.md` — the original 147-item project specification
3. `reports/07_null_models_report.md` — Phase 7 results, especially §3.3 (the assortativity
   finding was retracted after FDR correction — don't re-introduce it as fact)
4. `config/analysis.yaml` — `sensitivity.variants` (already listed) and `robustness` sections
5. `docs/network_models.md`, `docs/decision_log.md` (DEC-001 through DEC-008)

**Do not rebuild Phases 1-7.** The canonical dataset, G0-G11 networks, descriptive metrics,
community/signed/directed/multilayer/narrative-order analysis, and null-model validation are all
done and verified. Build on `outputs/tables/centrality_*.csv` and the G0-G11 graph objects
(`src/networks.py::build_all_networks()`) rather than recomputing them.

## First task — Phase 8: Sensitivity Analysis

Several of the required comparisons already exist as network variants — reuse them rather than
rebuilding:
- person+group vs person-only -> `G0_full` vs `G1_person_only` (already built)
- weighted vs unweighted -> `G10_weighted` vs `G11_unweighted` (already built, identical structure
  by construction - note in the report that this comparison is currently a no-op because both
  variants use the same edge set; if a genuinely different unweighted construction is wanted,
  that needs a new variant)
- all relations vs core-social -> `G0_full` vs `G2_core_social` (already built)
- group included vs excluded -> same as person-only vs person+group above

Still need to be built in `src/sensitivity.py`:
- explicit vs explicit+inferred: filter `relations_event_level.csv` by
  `extraction_method == 'açık_ilişki'` (596/628 rows) vs. all rows (628) — build two new graph
  variants for this filter, following the same pattern as `src/networks.py::NETWORK_DEFINITIONS`.
- girizgah included vs excluded: filter out `story_id == 'S01'` — check whether this changes
  anything (S01 has only 1 relation, so the practical effect may be negligible; still worth
  running to have a documented, N/A-if-trivial result rather than assuming).

For every pair of variants:
1. Compute centrality (degree, betweenness, pagerank at minimum — reuse `src/metrics.py`'s
   `centrality_profile()` function) on both.
2. Compare rankings: Spearman correlation, Kendall's tau, and top-k overlap (k=10 and k=20) on
   the actor set common to both variants.
3. Write `reports/08_sensitivity_robustness_report.md`: which centrality conclusions are stable
   across variants, which are not. Frame stable results as "robust to this modeling choice", not
   as newly "confirmed important."

## Then also this phase: Structural Robustness (sections 30-31)

Using `config/analysis.yaml::robustness` (removal_strategies: random/high_degree/high_betweenness,
n_random_trials=100): on `G0_full` (or `G2_core_social`), remove nodes incrementally under each
strategy and track largest-component size, number of components, and average path length (on the
giant component) as a function of fraction removed. Call this **structural robustness**, not
"narrative resilience" (explicit naming rule in the master prompt, section 31).

## Then continue in master-plan order

PHASE 9 (if not folded into 8) -> PHASE 10 motif/triad (only if methodologically sound, see
Phase 6/7's sparse-triad caveats) -> PHASE 11 figures -> PHASE 12 tables -> PHASE 13
inter-annotator infrastructure -> PHASE 14 reproducibility/pipeline -> PHASE 15 web portal ->
PHASE 16 website validation -> PHASE 17 documentation -> PHASE 18 paper package -> PHASE 19
thesis package -> PHASE 20 final validation/release -> PHASE 21 final reports.

Update `CLAUDE_SESSION_HANDOFF.md`, `NEXT_TASK.md`, `project_state.json`, and
`docs/decision_log.md` after each completed phase, then commit locally.

## Rules that must not be relaxed

- Never invent unsupported data, metadata, or academic findings.
- Centrality ≠ literary importance.
- If an analysis can't be meaningfully run (too sparse, too few cases), mark `not_applicable`
  with a stated reason.
- `data/raw/` and `data/final/` stay untouched.
- No merge/push to `main`. No force-push. Local commits on `claude-dk-rebuild` only.
- Degree assortativity is **not** a validated finding (Phase 7) — do not cite it as fact in new
  reports without re-deriving/re-checking.
