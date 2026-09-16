# CURRENT PROJECT STATUS

PHASES 1-5 COMPLETE AND COMMITTED.
PHASE 6 (Advanced Network Analysis) IS PARTIALLY COMPLETE: community detection, signed network
analysis, directed triad census, and multilayer analysis have all been run with real, verified
results. Narrative-order analysis and the Phase 6 report are the only pieces left.

NEXT:
Finish PHASE 6 — ADVANCED NETWORK ANALYSIS

## Start by reading (in this order)

1. `CLAUDE_SESSION_HANDOFF.md` — full state, verified numbers, what's done vs. not
2. `docs/MASTER_PROMPT.md` — the original 147-item project specification
3. `reports/04_05_network_construction_and_descriptive_report.md`
4. `config/analysis.yaml`
5. `docs/network_models.md`
6. `docs/decision_log.md`

**Do not rebuild Phases 1-5 unless validation reveals a real error.** Do not re-run
`src/communities.py`, `src/signed_and_directed.py`, or `src/multilayer.py` blindly — their
outputs already exist under `outputs/statistics/` and `outputs/tables/` and are described with
exact numbers in `CLAUDE_SESSION_HANDOFF.md`. Re-run only if you have a specific reason to
believe they're stale or wrong.

## First task

1. Run `python src/narrative_order.py` (via `.\.venv\Scripts\python.exe src\narrative_order.py`
   from the repo root) — this script exists but has never been executed. Verify its output
   (`outputs/tables/narrative_order_windows.csv`, `outputs/tables/dynamic_centrality_trajectory.csv`)
   makes sense (check for `not_applicable` rows, sane cumulative-degree trajectories).
2. Write `reports/06_advanced_network_analysis_report.md` covering: community detection
   (Leiden/Louvain, stability, resolution sensitivity, bridge metrics), signed network analysis
   (including the `not_applicable` structural balance result and why), directed triad census,
   multilayer/versatility profile, and narrative-order/dynamic-centrality results. Use the exact
   numbers already recorded in `CLAUDE_SESSION_HANDOFF.md` — re-derive them from the actual output
   files rather than copying blindly, in case anything changed.
   **Explicitly note the 23-connected-component caveat**: the community count (33) is partly an
   artifact of graph fragmentation, not all of it reflects meaningful social clustering — this
   nuance has not yet been written into any report.
3. Commit Phase 6 with a message like:
   `Complete Phase 6 advanced network analysis (community detection, signed/directed/multilayer/narrative-order)`

## Then continue in this order (see CLAUDE_SESSION_HANDOFF.md → "REMAINING MASTER PLAN" for full detail)

- PHASE 7 — Null models / statistical validation (`src/null_models.py`, does not exist yet)
- PHASE 8 — Sensitivity analysis (`src/sensitivity.py`, does not exist yet; variants already
  listed in `config/analysis.yaml`)
- PHASE 9 — Structural robustness (`src/robustness.py`, does not exist yet)
- PHASE 10 — Figures and tables
- PHASE 11 — Web portal (`docs/` GitHub Pages site)
- PHASE 12 — Documentation (data dictionary, relation codebook, methodology, limitations)
- PHASE 13 — Paper/thesis packages
- PHASE 14 — Final validation and release report

## Rules that must not be relaxed

- Never invent unsupported data, metadata, or academic findings.
- Centrality ≠ literary importance — always frame centrality results as preliminary/structural.
- If an analysis can't be meaningfully run on this data (too sparse, too few cases), mark it
  `not_applicable` with a stated reason — do not force a number out of it.
- `data/raw/` and `data/final/` stay untouched. All new work lives under `data/processed/`,
  `data/derived/`, `outputs/`, `docs/`, `reports/`.
- Update `CLAUDE_SESSION_HANDOFF.md`, `NEXT_TASK.md`, and `project_state.json` after each
  completed phase.
