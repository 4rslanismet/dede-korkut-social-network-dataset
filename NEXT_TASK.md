# CURRENT PROJECT STATUS

PHASES 1-14 COMPLETE AND COMMITTED (repository audit through reproducibility pipeline; Phase
9-10 motif/triad analysis explicitly skipped with documented rationale, DEC-010).

NEXT:
PHASE 15 — WEB PORTAL (large; may warrant a dedicated session)

## Start by reading

1. `CLAUDE_SESSION_HANDOFF.md` — full state, especially the "PHASE 15 — NEXT WORK" section
2. `docs/MASTER_PROMPT.md` sections 50-72 (web portal requirements in full)
3. `docs/network_models.md`, `docs/decision_log.md` (DEC-001 through DEC-011)
4. `reports/13_14_reproducibility_report.md`

**Do not rebuild Phases 1-14.** All analysis is done; this phase is about presenting it.

## Task: Build the GitHub Pages site under docs/

1. **Data export layer first**: `src/build_site_data.py` producing `docs/data/*.json` from
   existing outputs (never hardcode a number the site displays - pull from
   `data/processed/nodes.csv`, `outputs/statistics/corpus_network_metrics.csv`,
   `outputs/validation/summary.json`, `project_state.json`, etc.).
2. **Home page**: title "Dede Korkut Narrative Networks", metric cards from the JSON (stories,
   actors, relations, narrative events, relation layers), reproducibility status panel (section
   129), required disclaimer (section 134: network metrics are structural, not literary
   judgments).
3. **Navbar** (section 52, exact list): Home, Dataset, Methodology, Network Explorer, Stories,
   Characters, Layers, Communities, Similarity, Analysis, Evidence, Downloads, Reproduce, About.
4. **Network Explorer**: Cytoscape.js (via cdnjs), fed by `outputs/networks/G0_full_edges.csv` /
   `_nodes.csv` (and other variants) converted to Cytoscape JSON by the data-export script. Filters
   per section 56. Node/edge detail panels show only real computed fields (section 57-58) - no
   placeholder text.
5. **Community page**: numeric community labels only (`Community 1`, `Community 2`, ...) - never
   invent cultural names. Must state the 23-connected-component caveat.
6. **Per-story and per-character pages**: generate from templates + JSON, not hand-authored per
   page. Start with the actors already in `outputs/tables/publication/T04_centrality_results.csv`.
7. **Downloads page**: link to the real files under `data/processed/`, `outputs/networks/`,
   `outputs/tables/publication/`.
8. **Reproduce page**: real commands (`git clone ...`, `pip install -r requirements.txt`,
   `python run_pipeline.py --all`).
9. Site must use relative paths only (section 104) - test by opening `docs/index.html` directly
   from the filesystem, not just via a server.

## Then Phase 16: Website Validation

Check for broken links, missing JSON/images, invalid generated pages, JS/data loading errors
(open in the built-in browser and check the console).

## Then continue in master-plan order

PHASE 17 documentation (data dictionary, relation codebook, methodology.md, limitations.md,
architecture diagram) -> PHASE 18 paper package -> PHASE 19 thesis package -> PHASE 20 final
validation/release (cross-check README/paper/thesis/canonical numbers for consistency) -> PHASE 21
final reports (FINAL_REBUILD_REPORT.md, EXECUTIVE_SUMMARY.md, RELEASE_CHECKLIST.md).

## Known gaps carried forward

- Story similarity (section 17) not fully computed - blocks a complete Similarity page; either
  compute it first or clearly mark that page as partial.
- Figures F01, F04-F05, F08-F14 not yet produced.
- Degree assortativity is NOT a validated finding (Phase 7 retraction).
- Any community-structure content must carry the 23-connected-component caveat.
- No `docs/methodology.md`, `docs/limitations.md`, `docs/data_dictionary.md`,
  `docs/relation_codebook.md` yet - the Methodology/Evidence pages will need this content, so
  consider whether to pull Phase 17 documentation forward if the web portal needs it as source
  text.
- When writing git commit messages with PowerShell, avoid embedded double quotes in `-m`
  arguments - use `git commit -F <tempfile>` instead.

## Rules that must not be relaxed

- Never invent unsupported data, metadata, academic findings, or agreement statistics.
- Centrality ≠ literary importance.
- Mark `not_applicable` rather than forcing a result on insufficient data.
- `data/raw/` and `data/final/` stay untouched.
- No merge/push to `main`. No force-push. Local commits on `claude-dk-rebuild` only.
