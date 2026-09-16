# CURRENT PROJECT STATUS

PHASES 1-16 COMPLETE AND COMMITTED (repository audit through web portal + website validation;
Phase 9-10 motif/triad explicitly skipped with documented rationale, DEC-010).

NEXT:
PHASE 17 — DOCUMENTATION

## Start by reading

1. `CLAUDE_SESSION_HANDOFF.md` — full state
2. `docs/MASTER_PROMPT.md` sections 83-90, 100-101 (documentation requirements)
3. `reports/15_16_web_portal_report.md` — most recent work, including two new findings:
   a GitHub-Pages path bug (DEC-012) and 5 newly-discovered concatenated-multi-actor nodes
   (DEC-013, `validation/HUMAN_REVIEW_QUEUE.csv` HR0076-HR0080)
4. `docs/decision_log.md` (DEC-001 through DEC-013)

**Do not rebuild Phases 1-16.** This phase is mostly synthesis/writing from data that already
exists — schemas in `data/processed/*.csv`, relation types in `relation_taxonomy.csv`, every
methodological decision in `docs/decision_log.md`, and limitations already scattered across every
`reports/*.md` file and this handoff.

## Task: Phase 17 — Documentation

1. `docs/data_dictionary.md` (section 83): every column of every file in `data/processed/`
   (nodes.csv, aliases.csv, stories.csv, relations_event_level.csv, relations_aggregated.csv,
   relation_taxonomy.csv, provenance.csv, validation_status.csv) — field, type, meaning, allowed
   values, nullability, source.
2. `docs/relation_codebook.md` (section 84): one entry per relation type in
   `data/processed/relation_taxonomy.csv` (17 types) — definition, parent family, directionality
   expectation, polarity expectation, and 1-2 real examples pulled from
   `relations_event_level.csv` (use `raw_evidence`).
3. `docs/methodology.md` (section 85): expand well beyond `docs/methodology.html`'s summary — this
   needs to be detailed enough to serve as a thesis/paper methods section source. Cite every
   DEC-XXX decision by number with its rationale.
4. `docs/limitations.md` (section 86): consolidate everything already known - source edition gap
   (`validation/source_edition_metadata_required.md`), single coder, the 80-row story_level/final
   provenance gap, 53 unmatched provenance relations, 29.6% "belirsiz" relations, group actor
   effects (Phase 8 sensitivity results), inferred relation effects, edge weight semantics
   (agirlik), narrative-order ≠ chronology, the 23-connected-component community artifact, the 5
   concatenated-multi-actor nodes (new, Phase 15), entity resolution uncertainty (17 open alias
   conflicts), retracted assortativity finding (Phase 7).
5. `DATASET_CARD.md` (section 87), `CITATION.cff` (section 88 — use TODO/placeholder for missing
   author/publication metadata, never invent), `CHANGELOG.md` (section 89 — legacy v3 to this
   rebuild), `CONTRIBUTING.md` (section 90 — rules for adding new relation annotations).
6. Architecture diagram (section 101) as SVG/PNG - the data-flow diagram already sketched in
   `methodology.html` can be the basis.
7. Root `README.md` redesign (section 100) - project overview, key features, dataset snapshot
   (real numbers), repository structure, methodology summary, reproducibility, website link,
   citation, license. This is the actual repository README, not a site page.

## Then continue in master-plan order

PHASE 18 paper package (`paper/`: manuscript outline, methods, results, figures, tables,
supplementary material - section 91-94, use ONLY real computed findings, hedge appropriately per
section 94's example phrasing) -> PHASE 19 thesis package (`thesis/`: proposed structure, research
questions, methodology mapping, results mapping, figure/table inventory) -> PHASE 20 final
validation/release (cross-check every number across README/paper/thesis/canonical
data/website for consistency) -> PHASE 21 final reports (FINAL_REBUILD_REPORT.md,
EXECUTIVE_SUMMARY.md, RELEASE_CHECKLIST.md).

## Known gaps carried forward

- Story similarity (section 17) still not fully computed.
- 5 concatenated-multi-actor nodes discovered in Phase 15, unresolved (DEC-013).
- G9_directed has no null-model comparison; degree assortativity is NOT validated (retracted,
  Phase 7) - do not cite it as fact in new documentation.
- `run_pipeline.py --all` (full mode) not tested end-to-end.
- Site not yet deployed to actual GitHub Pages (only tested locally via `python -m http.server`).

## Rules that must not be relaxed

- Never invent unsupported data, metadata, academic findings, citation/DOI info, or author names.
- Centrality ≠ literary importance.
- Mark `not_applicable` rather than forcing a result on insufficient data.
- `data/raw/` and `data/final/` stay untouched.
- No merge/push to `main`. No force-push. Local commits on `claude-dk-rebuild` only.
- When testing the website, always use a real local HTTP server (`python -m http.server` from
  `docs/`), never just open the HTML file directly - `file://` previews hide real path bugs
  (see DEC-012, caught a GitHub-Pages-breaking bug that a file:// preview missed entirely).
- When writing git commit messages via PowerShell, avoid embedded double quotes in `-m` — use
  `git commit -F <tempfile>`. Also avoid piping file content through PowerShell `-replace` /
  `Get-Content | Set-Content` for files with non-ASCII characters - it can corrupt UTF-8 (this
  happened once this session, see DEC-012's note and the fix in `src/build_site.py`'s git
  history); prefer the Edit tool or a small Python script for text replacement instead.
