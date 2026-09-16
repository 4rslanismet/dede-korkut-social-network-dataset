# CURRENT PROJECT STATUS

PHASES 1-12 COMPLETE AND COMMITTED (repository audit through publication figures/tables;
Phase 9-10 motif/triad analysis explicitly skipped with documented rationale, DEC-010).

NEXT:
PHASE 13 — INTER-ANNOTATOR INFRASTRUCTURE, THEN PHASE 14 — REPRODUCIBILITY/PIPELINE

## Start by reading

1. `CLAUDE_SESSION_HANDOFF.md` — full state
2. `docs/MASTER_PROMPT.md` sections 37-38 (inter-annotator), 73-81 (pipeline/tests/hash manifest)
3. `docs/decision_log.md` (DEC-001 through DEC-010)
4. `reports/09_12_figures_tables_report.md` — most recent work

**Do not rebuild Phases 1-12.**

## Task A — Phase 13: Inter-Annotator Infrastructure

1. Build a stratified sample from `data/processed/relations_event_level.csv`: vary across
   story_id, standard_relation, layer, and extraction_method (explicit vs inferred). ~50-80 rows
   is reasonable. Write `validation/inter_annotator_sample.csv` with columns: relation_id, actor_1,
   actor_2, raw_evidence, coder1_relation, coder2_relation, coder1_layer, coder2_layer,
   coder1_polarity, coder2_polarity, agreement, notes (coder1_* pre-filled from the existing data,
   coder2_* and agreement left blank for a human to fill in).
2. Write `docs/inter_annotator_protocol.md` describing how a second coder should use the sample.
3. Write `src/inter_annotator_stats.py` with Cohen's kappa and Krippendorff's alpha computation
   ready to run once real second-coder data exists — but do NOT invent or simulate second-coder
   data, and do NOT report a kappa/alpha value now. The script should refuse to run meaningfully
   until `coder2_*` columns are actually filled in.

## Task B — Phase 14: Reproducibility / Pipeline

1. `run_pipeline.py` at repo root, orchestrating the 14 steps already implemented across
   `src/*.py` in order (audit -> validate -> entity_resolution -> build_canonical ->
   build_networks -> story_networks -> metrics -> communities -> signed_and_directed ->
   multilayer -> narrative_order -> null_models -> null_models_fdr -> sensitivity -> robustness
   -> visualization -> export_tables). Support `--stage <name>` and `--all` per section 119.
2. `tests/` directory with pytest tests covering: canonical schema (node_id uniqueness, edge
   endpoint referential integrity), deterministic outputs (same seed -> same result for at least
   one stochastic step, e.g. community detection), and aggregation correctness (relations_aggregated
   row count matches expectations from relations_event_level).
3. Hash manifest: `outputs/manifest_sha256.csv` listing SHA-256 of every file under `data/final/`,
   `data/processed/`, and key `outputs/` files.
4. `requirements-lock.txt`: exact pinned versions (`pip freeze` from `.venv`).
5. Update `CLAUDE_SESSION_HANDOFF.md`, `NEXT_TASK.md`, `project_state.json`,
   `docs/decision_log.md`, commit: `Complete phase 13-14 inter-annotator infrastructure and reproducibility pipeline`

## Then continue in master-plan order

PHASE 15 web portal (large - `docs/` GitHub Pages site, Cytoscape.js network explorer, per-story
and per-character pages, all navbar sections from master prompt section 52) -> PHASE 16 website
validation -> PHASE 17 documentation (data dictionary, relation codebook, methodology,
limitations, architecture diagram) -> PHASE 18 paper package -> PHASE 19 thesis package ->
PHASE 20 final validation/release -> PHASE 21 final reports (FINAL_REBUILD_REPORT,
EXECUTIVE_SUMMARY, RELEASE_CHECKLIST).

## Known gaps carried forward (do not silently "fix" without re-reading the relevant report)

- Story similarity (section 17: Jaccard/cosine/etc.) not yet computed - only raw shared-actor
  bipartite projection exists. Needed before F10/F11 figures and a complete T08 table.
- Figures F01, F04-F05, F08-F14 not yet produced (low priority backlog).
- G9_directed has no null-model comparison (double_edge_swap is undirected-only).
- Degree assortativity is NOT a validated finding (Phase 7 retraction) - don't cite as fact.
- Any community-structure figure/table for G2_core_social must carry the 23-connected-component
  caveat.
- When writing git commit messages with PowerShell, avoid embedded double quotes in `-m`
  arguments (native command-line quoting can mis-split them) - write the message to a temp file
  and use `git commit -F <file>` instead.

## Rules that must not be relaxed

- Never invent unsupported data, metadata, academic findings, or second-annotator agreement
  statistics.
- Centrality ≠ literary importance.
- Mark `not_applicable` rather than forcing a result on insufficient data.
- `data/raw/` and `data/final/` stay untouched.
- No merge/push to `main`. No force-push. Local commits on `claude-dk-rebuild` only.
