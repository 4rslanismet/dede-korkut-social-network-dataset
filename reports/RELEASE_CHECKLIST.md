# Release Checklist

Per master prompt section 123 (release preparation) and section 142 (final quality gate). First checked at
Phase 20; updated after the story-similarity addendum (DEC-014), the final academic audit (DEC-015), the full
end-to-end pipeline verification (DEC-016) and the independent-review fix pass (DEC-017/018/019).

**Status: TECHNICALLY VALIDATED — READY FOR PR / TECHNICAL MERGE REVIEW. PUBLICATION BLOCKERS REMAIN.** The
pipeline, tests and site validation pass and the scientific core was independently reviewed twice (the second,
independent re-review of `claude-dk-fixpass` at `e5989c3` found 0 critical and 0 major issues and verified the
Top-5 findings 5/5), but the open owner/manual items below must be closed before anything is published or
presented as final. The project is **not** publication-ready. Current counts
(pipeline stages, tests, manifest entries, composite candidates) are generated into `outputs/results_registry.json`,
`outputs/manifest_sha256.csv` and `outputs/validation/site_validation_report.json`, not typed here.

| # | Item | Status | Evidence |
|---|---|---|---|
| 1 | Raw data preserved | ✅ PASS | `data/raw/`, `data/final/`, `data/story_level/` byte-identical to `main`; never written to by any `src/*.py` script (verified by hash comparison before/after full runs) |
| 2 | Canonical data produced | ✅ PASS | `data/processed/` — 332 nodes, 628 relations; 333→332 merge and 628/376 counts re-derived independently from `data/final/` (`reports/03_canonical_dataset_report.md`) |
| 3 | Provenance preserved | ⚠️ PASS WITH DISCLOSED GAPS | `data/processed/provenance.csv` — 90.9% matched uniquely, 8.4% disclosed as `unmatched_provenance_gap`, 0.6% `matched_ambiguous`; the +80-row story_level→final gap is documented (`docs/limitations.md` item 3) |
| 4 | Validation tests passed | ✅ PASS | `outputs/validation/summary.json` — 0 FAIL-level issues; full `pytest` suite passes (schema, aggregation, networks, distance semantics, site consistency, text consistency, determinism) and CI passed on the pushed reviewed state |
| 5 | Network definitions documented | ✅ PASS | `docs/network_models.md` (generated) — all 12 variants (G0-G11), one filter rule each in `src/networks.py`; all rebuilt independently by the reviewer; tie strength vs. path distance documented (DEC-017) |
| 6 | Analyses reproducible | ✅ PASS | `python run_pipeline.py --all` (FULL mode, n_random=1000) runs analysis → figures/tables → manifest → website build → website validation; run on the reviewed state and again after the fix pass; scientific outputs reproduce exactly; the manifest's SHA-256 hashes were independently re-verified |
| 7 | Figures regenerated | ⚠️ PARTIAL, DISCLOSED | 10/18 target figures produced; F01, F04-F05, F08-F09, F12-F14 not built (`docs/limitations.md` item 16) |
| 8 | Tables regenerated | ✅ PASS | T01-T11 produced from pipeline outputs; T03 separates raw relation records from aggregated edges; T04/T10 regenerated with corrected betweenness (DEC-017); T11 reports both component-size denominators |
| 9 | Sensitivity analysis complete | ✅ PASS | 6/6 planned construction-choice pairs, recomputed with weighted betweenness distance = 1/strength; person+group vs person-only and weighted vs unweighted numerically tied (`reports/08_sensitivity_robustness_report.md`) |
| 10 | Web portal built | ✅ PASS | Every actor and story has a generated page, all reachable from the Characters/Stories indexes; scientific numbers loaded from the results registry; Cytoscape.js explorer for 3 of 12 variants |
| 11 | Broken links / stale pages cleaned | ✅ PASS | `src/validate_site.py`: links, assets, JSON, expected-vs-generated page sets (no missing/orphan pages), index reachability — 0 issues; also served over real HTTP in earlier verification |
| 12 | README correct | ✅ PASS | Cross-checked against source data by `src/validate_release_consistency.py`; stale counts removed and enforced by `tests/test_text_consistency.py` |
| 13 | Paper package produced | ⚠️ PASS AS A PACKAGE, NOT A MANUSCRIPT | `paper/` — outline, methods, results, supplementary material, figures and tables. **Not a finished paper:** no Introduction, Discussion or References; no literature review performed |
| 14 | Thesis package produced | ✅ PASS | `thesis/` — structure, RQ assessment (RQ6 PARTIALLY ANSWERED / EXPLORATORY), mappings, inventories |
| 15 | Final report produced | ✅ PASS | `reports/FINAL_REBUILD_REPORT.md`, `reports/EXECUTIVE_SUMMARY.md`, `reports/FIX_PASS_REPORT.md` |

## Open blockers — classification

None of these can be closed by the pipeline; each needs the repository owner, a second human, or the original text.
"Release blocker" = must be settled before tagging/merging a citable release or deploying the site as final;
"publication blocker" = must be settled before a paper/thesis is submitted or the results are presented as final.

| Item | Severity | Blocks | Needs |
|---|---|---|---|
| Source edition/transcription metadata (`validation/source_edition_metadata_required.md`) | MAJOR | publication | repository owner |
| Second annotator / inter-annotator reliability (`docs/inter_annotator_protocol.md`) | MAJOR | publication | a real second coder |
| Manual review of unresolved entity items — 18 alias/entity conflicts, stale alias targets, provenance-gap files, the self-loop, and the candidate composite nodes (`validation/HUMAN_REVIEW_QUEUE.csv`, `validation/composite_node_candidates.csv`) | MAJOR | publication | review against the original text |
| `CITATION.cff` author / release-date metadata (`TODO` placeholders) | MINOR | release (tag/DOI) and publication | repository owner |
| Source-code licence (dataset is CC BY 4.0; no code licence chosen) | MINOR | release | repository owner |
| Paper Introduction / Discussion / References; literature review | MAJOR (for a paper) | publication | authors |
| Network Explorer covers 3 of 12 variants; 8 of 18 target figures not built | MINOR | nice-to-have | optional work |

## Known, disclosed incompletions (not blockers on their own — each has a stated reason and owner document)

- Candidate composite actor nodes are flagged, not resolved; no node has been split or merged (`docs/decision_log.md` DEC-013, DEC-018).
- No verified inter-annotator reliability statistic — single coder; infrastructure ready but correctly refuses to fabricate a value (`docs/limitations.md` item 2).
- Motif/triad null-model enrichment skipped — insufficient sample, no directed null model available (`docs/decision_log.md` DEC-010).
- The nine null-model networks are related, partly nested specifications, so "7 of 9" is not seven independent replications; observed modularity is a single Louvain partition.
- Site not deployed to a live GitHub Pages URL. `claude-dk-rebuild` and `claude-dk-fixpass` are on the remote
  (the latter independently re-reviewed at `e5989c3`); `main` is untouched, no tag or release exists.
- The composite-node scan is a heuristic and under-inclusive by design: it does not flag " ile " constructions,
  hyphen-joined names or phrases shorter than six words (e.g. "Egreke Yol Gösterdi", "Kayın Ata - Kayın Anası").
  Manual review therefore has to cover the whole node list (`docs/limitations.md` §11).

## History

- **Post-release addendum (RQ6, DEC-014) and final academic audit (DEC-015).** The story-similarity suite was built,
  first recorded as "answered", then corrected: actor overlap is low, the top pair differs by metric, and cluster
  validity does not support a robust discrete clustering, so RQ6 is **PARTIALLY ANSWERED / EXPLORATORY**; an uncoded
  "captivity theme" interpretation was removed; the Top-5 findings were re-verified against their outputs.
- **Full end-to-end pipeline verification (DEC-016).** A first full run exposed two idempotency defects (a fresh run
  deleted hand-appended review items and generated documentation sections); both were fixed at their generators and a
  second full run reproduced the scientific outputs exactly.
- **Independent review of the reviewed state and the fix pass (DEC-017, DEC-018, DEC-019).** The review passed the
  scientific core and found: weighted betweenness had used tie strength as path distance (**fixed**, rankings and
  sensitivity regenerated; no headline finding reversed, but the claim that two actors lead betweenness in every
  specification was withdrawn); an under-inclusive composite-node disclosure (**reproducible scan, review queue
  expanded, disclosures corrected; manual review still open**); stale generated pages, story-page edge labelling,
  hand-typed site numbers, ambiguous robustness wording and stale counts (**fixed at the generators and enforced by
  tests**). Details and per-issue status: `reports/FIX_PASS_REPORT.md`.

## Overall Status

**15/15 items PASS or PASS-WITH-DISCLOSED-GAPS.** No item is silently marked PASS while actually incomplete — every
partial/gap above is cross-referenced to the document that discloses it in full. The project is a validated research
repository, not a finished publication: the blockers above remain open. Phases 1-21 of the governing master prompt
are complete, with Phase 9-10 (motif analysis) explicitly and deliberately skipped (DEC-010) rather than forced.
