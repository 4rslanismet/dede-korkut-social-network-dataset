# CURRENT PROJECT STATUS

**ALL 21 PHASES OF THE GOVERNING MASTER PROMPT ARE COMPLETE**, plus a post-release addendum
(story-similarity metric suite, RQ6) and a **final academic audit before release (DEC-015)**.

**Full end-to-end reproducibility is verified (DEC-016):** `python run_pipeline.py --all` (FULL
mode, n_random=1000) was run twice, 23/23 stages PASS each time (~7 min); scientific outputs
reproduced exactly; the pipeline is now idempotent (the first run exposed and the fix removed two
cases where a fresh run deleted hand-added review items / doc sections). `pytest` 18/18,
`--validate-only`, site validation (363/363) and release consistency all PASS afterwards. The site
build/validation scripts are run separately (they are not in the orchestrator's `STAGES`).

After the audit, the seven original research questions stand as: RQ1, RQ3, RQ4, RQ5 answered
(RQ4 confirmatory; RQ5 a descriptive sensitivity analysis); RQ2, RQ7 partially answered
(exploratory); **RQ6 PARTIALLY ANSWERED / EXPLORATORY** — story-level similarity can be quantified
and visualized, but evidence for a robust discrete clustering structure is limited (see
`thesis/research_questions.md`, `outputs/statistics/story_similarity_cluster_validity.json`).

## Start by reading (in this order)

1. `CLAUDE_SESSION_HANDOFF.md` — full state; see the "FINAL ACADEMIC AUDIT" section for the latest work
2. `reports/EXECUTIVE_SUMMARY.md` (~4 min read)
3. `reports/FINAL_REBUILD_REPORT.md` (see the Post-Release Addendum and the audited "Top 5" section)
4. `reports/RELEASE_CHECKLIST.md` (see "Open release blockers")
5. `thesis/research_questions.md` — RQ6 is "partially answered / exploratory"
6. `docs/decision_log.md` DEC-014 (revised), DEC-015 and DEC-016 (full-pipeline verification)

## There is no next mandatory task

Do not invent new phases. If resumed without a specific new instruction, summarize the above for
the user rather than starting new work. Recommended next step (only on the user's request):
push `claude-dk-rebuild` to the remote for independent review.

## Open release blockers (deferred / manual / external — the audit did NOT change their status)

1. **Source edition/transcription verification** — needs the repo owner
   (`validation/source_edition_metadata_required.md`).
2. **Inter-annotator reliability** — needs a real second coder (`docs/inter_annotator_protocol.md`,
   `src/inter_annotator_stats.py` ready and waiting).
3. **Unresolved merged/concatenated entity cases** (DEC-013, HR0076–HR0080 and other
   `validation/HUMAN_REVIEW_QUEUE.csv` items) — needs review against the original narrative text,
   which is not in this repository.
4. **`CITATION.cff` personal/bibliographic metadata** — needs the repo owner's details.

## Other optional items (only on explicit user request)

- Add `build_site` and `validate_site` to `run_pipeline.py` `STAGES` so one command is end-to-end
  (not done: it changes the pipeline contract).
- Extend the Network Explorer to all 12 network variants; build the remaining figures (F01, F04-F05,
  F08-F09, F12-F14).
- Push `claude-dk-rebuild`, deploy the site to a live GitHub Pages URL, or open a PR to `main`.
  Nothing has been pushed anywhere yet.
- For RQ6 specifically: a robust discrete story grouping, if one exists, would need richer
  story-level features than the current relation-type/layer profile (e.g. coded thematic
  variables); none exist in the canonical dataset today.

## Known environment quirk (not a real blocker)

On this machine, some scipy submodules (`scipy.cluster.hierarchy` → `scipy.spatial`/`scipy.sparse`)
can take 120s+ on their *first* import in a session (an Application Control Policy / antivirus DLL
scan), sometimes timing out. Retrying the same command (with a longer timeout, e.g. 150000ms)
resolves it — this happened once and was not a real code or dependency problem.

## Rules that must not be relaxed, ever

- Never invent unsupported data, metadata, academic findings, citation/DOI info, or author names.
- Never write an LLM inference (e.g. a narrative theme that is not a coded variable) as a
  quantitative/network-analysis finding.
- "Most similar pair" means relatively most overlapping among the evaluated stories — never write
  "highly similar", "strong similarity", "clear clusters" for RQ6.
- Centrality ≠ literary importance.
- Mark `not_applicable` rather than forcing a result on insufficient data.
- `data/raw/` and `data/final/` stay untouched.
- No merge/push to `main`, no push to remote at all without explicit user request.
- Git commits via PowerShell: avoid embedded double quotes in `-m`, use `git commit -F <tempfile>`.
  Avoid PowerShell `-replace`/`Get-Content | Set-Content` on UTF-8 files with non-ASCII characters
  - use the Edit tool or a small Python script instead.
- Test any website change against a real local HTTP server (`python -m http.server` from `docs/`),
  never just a `file://` preview.
