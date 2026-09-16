# CURRENT PROJECT STATUS

PHASES 1-19 COMPLETE AND COMMITTED (repository audit through paper/thesis packages; Phase 9-10
motif/triad explicitly skipped with documented rationale, DEC-010).

NEXT:
PHASE 20 — FINAL VALIDATION/RELEASE, THEN PHASE 21 — FINAL REPORTS

## Start by reading

1. `CLAUDE_SESSION_HANDOFF.md` — "PHASE 20-21 — NEXT WORK" section has the full task breakdown
2. `thesis/research_questions.md` — which RQs are fully/partially/not answerable; the final report
   must not silently claim more than this document supports
3. Every `reports/*.md` file (01 through 17) plus `paper/` and `thesis/` — this phase synthesizes
   all of them, it does not add new findings

**This is the closing phase.** Do not run new analysis. If a consistency check finds a real
discrepancy, fix the specific stale number, don't re-derive analysis from scratch.

## Task: Phase 20 — Final Validation/Release

1. Cross-check headline numbers across README.md, DATASET_CARD.md, paper/results.md,
   thesis/research_questions.md, docs/data/project_summary.json, and project_state.json - they
   should all agree. A small script that re-derives each number from source and diffs against
   what's written would be more reliable than eyeballing.
2. Re-run `python -m pytest tests/`, `python run_pipeline.py --all --validate-only`, and
   `python src/validate_site.py` - confirm all still PASS.
3. Write `reports/RELEASE_CHECKLIST.md` (master prompt section 123/142's checklist) with an
   explicit PASS/FAIL per item. Known, disclosed incompletions (RQ6/story similarity, some
   figures, GitHub Pages not yet deployed) should show as explicitly acknowledged gaps, not
   silently marked PASS.

## Task: Phase 21 — Final Reports

1. `reports/FINAL_REBUILD_REPORT.md` (section 124's full outline - Initial State, Data Audit,
   Data Corrections, Preserved Decisions, Canonical Model, Network Models, Analyses, Statistical
   Validation, Sensitivity, Key Findings, Limitations, Website, Reproducibility, Academic Outputs,
   Future Work). Assemble by synthesizing `reports/01` through `reports/17` - this is the
   capstone document.
2. Within it, a "Top 5 strongest defensible findings" section (section 126) - candidates already
   identified in CLAUDE_SESSION_HANDOFF.md's Phase 21 section; don't pad to 5 if fewer are truly
   defensible (section 141).
3. Report negative/null results explicitly (section 127) - the G3_kinship null result, the
   assortativity retraction, and RQ6's "not answerable" status must all appear, not be dropped.
4. `reports/EXECUTIVE_SUMMARY.md` (section 125) - short, readable in 3-5 minutes by a
   non-specialist: what was done, what was found, the scientific contribution, what's next.

## After Phase 21: project is at v1 completion of the master prompt's scope

At that point, consider with the user (not unilaterally):
- Whether to push `claude-dk-rebuild` to the remote (this project has never pushed - no remote
  auth was set up, and pushing changes the shared repository, which needs explicit permission).
- Whether to open a PR to `main` or keep iterating on the branch.
- Whether to actually deploy the site to GitHub Pages (requires a repo setting change).

## Rules that must not be relaxed

- Never invent unsupported data, metadata, academic findings, citation/DOI info, or author names.
- Centrality ≠ literary importance.
- Mark `not_applicable` rather than forcing a result on insufficient data - RQ6 is the standing
  example; don't let a "final report" retroactively claim it was answered.
- `data/raw/` and `data/final/` stay untouched.
- No merge/push to `main`, no push to remote at all without explicit user request. Local commits
  on `claude-dk-rebuild` only, as has been the practice throughout.
- Git commits via PowerShell: avoid embedded double quotes in `-m`, use `git commit -F <tempfile>`.
  Avoid PowerShell `-replace`/`Get-Content | Set-Content` on UTF-8 files with non-ASCII characters
  - use the Edit tool or a small Python script instead.
