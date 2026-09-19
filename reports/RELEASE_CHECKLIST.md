# Release Checklist

Per master prompt section 123 (release preparation) and section 142 (final quality gate). Checked
at Phase 20, after re-running every automated validation layer this project has built.

| # | Item | Status | Evidence |
|---|---|---|---|
| 1 | Raw data preserved | ✅ PASS | `data/raw/`, `data/final/` untouched since clone; never written to by any `src/*.py` script |
| 2 | Canonical data produced | ✅ PASS | `data/processed/` — 8 files, 332 nodes, 628 relations (`reports/03_canonical_dataset_report.md`) |
| 3 | Provenance preserved | ⚠️ PASS WITH DISCLOSED GAPS | `data/processed/provenance.csv` — 90.9% matched uniquely, 8.4% disclosed as `unmatched_provenance_gap`, 0.6% `matched_ambiguous`; the +80-row story_level→final gap is documented, not hidden (`docs/limitations.md` item 3) |
| 4 | Validation tests passed | ✅ PASS | `outputs/validation/summary.json` — 0 FAIL-level issues; 18/18 `pytest` tests passing (just re-verified) |
| 5 | Network definitions documented | ✅ PASS | `docs/network_models.md` — all 12 variants (G0-G11), one filter rule each in `src/networks.py` |
| 6 | Analyses reproducible | ✅ PASS | Full end-to-end `python run_pipeline.py --all` (FULL mode, n_random=1000) run twice on 2026-09-19: 23/23 stages PASS each time; scientific outputs reproduced exactly (see "Full End-to-End Pipeline Run" below). The first run exposed two idempotency defects, fixed before the second run (DEC-016) |
| 7 | Figures regenerated | ⚠️ PARTIAL, DISCLOSED | 10/18 target figures produced (F02,F03,F06,F07,F10,F11,F15-F18); F01,F04-F05,F08-F09,F12-F14 not built (`docs/limitations.md` item 16) |
| 8 | Tables regenerated | ✅ PASS | T01-T11 all produced and complete (`outputs/tables/publication/`); T08 (story similarity) now the full 5-metric, 91-pair table (post-release addendum, DEC-014; exploratory content, see DEC-015) |
| 9 | Sensitivity analysis complete | ✅ PASS | 6/6 planned construction-choice pairs tested (`reports/08_sensitivity_robustness_report.md`) |
| 10 | Web portal built | ✅ PASS | 363 HTML pages, all 14 navbar sections, Cytoscape.js explorer (`reports/15_16_web_portal_report.md`) |
| 11 | Broken links cleaned | ✅ PASS | `src/validate_site.py` just re-run: 363/363 files, 0 issues |
| 12 | README correct | ✅ PASS | Cross-checked against source data by `src/validate_release_consistency.py`: PASS |
| 13 | Paper package produced | ✅ PASS | `paper/` — outline, methods, results, supplementary material, 8 figures, 22 table files |
| 14 | Thesis package produced | ✅ PASS | `thesis/` — structure, RQ assessment (RQ6 originally marked not-yet-answerable; now PARTIALLY ANSWERED / EXPLORATORY after DEC-014/DEC-015), mappings, inventories |
| 15 | Final report produced | ✅ PASS | `reports/FINAL_REBUILD_REPORT.md` and `reports/EXECUTIVE_SUMMARY.md` |

## Known, Disclosed Incompletions (not blockers — each has a stated reason and owner document)

- 5 concatenated-multi-actor nodes found, not fixed — `docs/decision_log.md` DEC-013, `validation/HUMAN_REVIEW_QUEUE.csv` HR0076-HR0080.
- No verified inter-annotator reliability statistic — single coder; infrastructure ready but correctly refuses to fabricate a value (`docs/limitations.md` item 2).
- Motif/triad null-model enrichment skipped — insufficient sample, no directed null model available (`docs/decision_log.md` DEC-010).
- Site not yet deployed to a live GitHub Pages URL — tested locally only.
- Repository never pushed to remote — all work is local commits on `claude-dk-rebuild`.
- `CITATION.cff` has `TODO` placeholders for author name and release date.

## Post-Release Addendum

After this checklist was first completed (all 21 phases), the user asked to continue with
optional future work. The single highest-value, fully self-contained item was picked: **the story
similarity metric suite (RQ6)**, previously the project's one open research question. It is now
built (`src/story_similarity.py`, `docs/decision_log.md` DEC-014) — all 91 story pairs, 5
metrics, hierarchical clustering, and figures F10-F11. It was first recorded as "answered"; a
**final academic audit before release (DEC-015)** found that overclaim was not supported: actor
overlap is low (max Jaccard 0.153), the top pair differs by metric, and cluster-validity checks
(`outputs/statistics/story_similarity_cluster_validity.json`) do not support a robust discrete
clustering. `thesis/research_questions.md` RQ6 is therefore **PARTIALLY ANSWERED / EXPLORATORY**;
an uncoded "captivity theme" interpretation was removed; and the pipeline now runs
`story_similarity`, `story_similarity_validity` and `audit_top5_checks` stages (previously
`export_tables` would have overwritten the full T08 on a rerun). The Top-5 findings in
`reports/FINAL_REBUILD_REPORT.md` were verified 5/5 against their output files and reworded where
the evidence was narrower than the claim (notably #3, sensitivity ranking; see DEC-015).
Validation layers re-run after the audit, all PASS: `pytest` 18/18;
`run_pipeline.py --all --validate-only`; `src/validate_site.py` 363/363 files, 0 issues;
`src/validate_release_consistency.py`.

### Open release blockers — unchanged by the DEC-015 audit

These remain open, deferred, manual/external items; the audit did not alter their status:

1. Source edition/transcription verification — external input from the repository owner
   (`validation/source_edition_metadata_required.md`).
2. Inter-annotator reliability — needs a real second coder (`docs/inter_annotator_protocol.md`).
3. Unresolved merged/concatenated entity cases (HR0076–HR0080 and other `HUMAN_REVIEW_QUEUE.csv`
   items) — need review against the original narrative text.
4. `CITATION.cff` personal/bibliographic metadata — needs the repository owner.

## Full End-to-End Pipeline Run (2026-09-19)

**Full end-to-end pipeline run: PASS**

- **Command / mode:** `python run_pipeline.py --all` — FULL mode (no `--fast`; `config/analysis.yaml`
  `null_models.n_random: 1000`, `robustness.n_random_trials: 100`, `seed: 42`). This is the mode the
  reported numbers come from (`reports/07_null_models_report.md`); there is no separate `--full`
  flag. Starting point: clean tree at `2e08975`; `data/raw/` and `data/final/` verified byte-identical
  before and after (hash comparison).
- **Run 1 (code as committed at `2e08975`):** 23/23 stages PASS, 7 min 11 s. It exposed two
  idempotency defects: a fresh run deleted (a) the five hand-appended review items HR0076-HR0080
  from `validation/HUMAN_REVIEW_QUEUE.csv` and (b) the story-level/bipartite sections of
  `docs/network_models.md`. No scientific output was affected.
- **Fix (DEC-016):** `validation/manual_review_items.csv` + `entity_resolution.py` append; the
  `story_networks.py` stage rewrites the doc sections (counts computed, not typed);
  bipartite `.graphml` edges written in sorted order. Both files now regenerate byte-identical to
  their committed versions, also on repeated runs.
- **Run 2 (fixed code):** 23/23 stages PASS, 7 min 18 s: audit, validate, entity_resolution,
  build_canonical, build_networks, story_networks, metrics, communities, signed_and_directed,
  multilayer, narrative_order, story_similarity, story_similarity_validity, null_models,
  null_models_fdr, sensitivity, robustness, audit_top5_checks, visualization, export_tables,
  build_inter_annotator_sample, inter_annotator_stats, hash_manifest.
- **Not orchestrator stages:** the website build (`src/build_site.py`), site validation
  (`src/validate_site.py`), `pytest` and `src/validate_release_consistency.py` are not in
  `run_pipeline.py`'s `STAGES`; they were run separately, in that order, after the pipeline.
- **Post-run validation:** `pytest` 18/18 PASS; `run_pipeline.py --all --validate-only` PASS;
  `validate_site.py` 363/363 files, 0 issues; `validate_release_consistency.py` PASS; the built site
  was also served over real HTTP (`python -m http.server`) and its key pages, figures and download
  files returned 200.
- **Scientific outputs vs. the committed versions:** no change. Byte-identical: all of
  `outputs/statistics/` (null-model FDR table, sensitivity, robustness, story-similarity clustering,
  cluster-validity, Top-5 checks), `outputs/matrices/`, `outputs/null_models/`, `outputs/validation/`,
  `data/processed/`, all publication tables incl. the full 91-pair T08, all PNG figures, and every
  paper/thesis/site page (RQ6 wording unchanged: PARTIALLY ANSWERED / EXPLORATORY).
- **Expected non-scientific differences when re-running (verified, and why they are not committed
  churn):** `.gexf` `lastmodifieddate` (one line per file, the only `.gexf` change committed);
  `.svg` `dc:date` and matplotlib's random element ids (embedded rasters pixel-identical);
  floating-point summation noise <= 1.1e-13 in `centrality_*.csv` / T04 (identifiers and row order
  identical). `outputs/manifest_sha256.csv` hashes update accordingly. `core.autocrlf=true` on
  Windows checks text files out with CRLF, so the manifest hashes of LF-written files (e.g. `.gexf`)
  match only files as the pipeline writes them, not a fresh CRLF checkout.
- **Recommendation (not done, changes the pipeline contract):** add `build_site` and `validate_site`
  to `run_pipeline.py` `STAGES` so that one command is end-to-end.

## Overall Status

**15/15 items PASS or PASS-WITH-DISCLOSED-GAPS.** No item is silently marked PASS while actually
incomplete — every partial/gap above is cross-referenced to the document that discloses it in
full. Phases 1-21 of the governing master prompt are complete, with Phase 9-10 (motif analysis)
explicitly and deliberately skipped (DEC-010) rather than forced.
