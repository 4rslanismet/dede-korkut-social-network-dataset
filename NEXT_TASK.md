# CURRENT PROJECT STATUS

**ALL 21 PHASES OF THE GOVERNING MASTER PROMPT ARE COMPLETE.** (Phase 9-10 motif/triad analysis
was explicitly and deliberately skipped, with documented rationale — DEC-010 — not silently
omitted.)

## Start by reading (in this order)

1. `CLAUDE_SESSION_HANDOFF.md` — full state
2. `reports/EXECUTIVE_SUMMARY.md` (~4 min read) — what was done, what was found, what's next
3. `reports/FINAL_REBUILD_REPORT.md` — the full capstone synthesis
4. `reports/RELEASE_CHECKLIST.md` — 15/15 PASS or PASS-with-disclosed-gaps

## There is no next mandatory task

This project has reached the end of `docs/MASTER_PROMPT.md`'s 147-item specification. Do not
invent new phases or restart completed ones. If you were resumed without a specific new
instruction from the user, the correct action is to summarize the above three documents for them,
not to start new work.

## If the user asks you to continue, prioritize (see "Future Work" in FINAL_REBUILD_REPORT.md)

1. Get a real second coder and compute genuine inter-annotator reliability
   (`docs/inter_annotator_protocol.md`, `src/inter_annotator_stats.py` are ready and waiting).
2. Resolve the 5 concatenated-multi-actor nodes (`docs/decision_log.md` DEC-013).
3. Build the full story-similarity metric suite to properly answer RQ6 (currently the project's
   one open research question — `thesis/research_questions.md`).
4. Confirm the source edition/transcription metadata
   (`validation/source_edition_metadata_required.md`).
5. Extend the Network Explorer to all 12 network variants; build remaining figures.
6. **Only on explicit user request:** push `claude-dk-rebuild` to the remote, deploy the site to a
   live GitHub Pages URL, or open a PR to `main`. Nothing has been pushed anywhere yet - this
   entire project exists only as local commits on `claude-dk-rebuild`.
7. Fill in `CITATION.cff` TODO fields once the repository owner confirms their details.

## Rules that must not be relaxed, ever, even after "completion"

- Never invent unsupported data, metadata, academic findings, citation/DOI info, or author names.
- Centrality ≠ literary importance.
- Mark `not_applicable` rather than forcing a result on insufficient data.
- `data/raw/` and `data/final/` stay untouched.
- No merge/push to `main`, no push to remote at all without explicit user request.
- Git commits via PowerShell: avoid embedded double quotes in `-m`, use `git commit -F <tempfile>`.
  Avoid PowerShell `-replace`/`Get-Content | Set-Content` on UTF-8 files with non-ASCII characters
  - use the Edit tool or a small Python script instead.
