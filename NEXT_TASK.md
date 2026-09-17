# CURRENT PROJECT STATUS

**ALL 21 PHASES OF THE GOVERNING MASTER PROMPT ARE COMPLETE**, plus one post-release addendum:
**the story-similarity metric suite (RQ6) has also been completed**, so all seven original
research questions now have an answer (RQ6 descriptively; RQ4/RQ5 confirmatory/null-model
validated; see `thesis/research_questions.md`).

## Start by reading (in this order)

1. `CLAUDE_SESSION_HANDOFF.md` — full state, see the "POST-RELEASE ADDENDUM" section for the most
   recent work
2. `reports/EXECUTIVE_SUMMARY.md` (~4 min read)
3. `reports/FINAL_REBUILD_REPORT.md` (see its own "Post-Release Addendum" section at the end)
4. `reports/RELEASE_CHECKLIST.md`
5. `thesis/research_questions.md` — RQ6 is now "answered"

## There is no next mandatory task

Do not invent new phases. If resumed without a specific new instruction, summarize the above for
the user rather than starting new work.

## If the user asks you to continue, remaining optional items (from FINAL_REBUILD_REPORT.md)

All items below require external input this session cannot provide autonomously (a second coder,
the repo owner's confirmation, or explicit push/deploy permission) — that's why they weren't
picked up when the user last asked to continue, and the story-similarity suite was completed
instead as the one fully self-contained option.

1. Get a real second coder and compute genuine inter-annotator reliability
   (`docs/inter_annotator_protocol.md`, `src/inter_annotator_stats.py` ready and waiting).
2. Resolve the 5 concatenated-multi-actor nodes (`docs/decision_log.md` DEC-013) — requires
   returning to the original narrative text, which is not available in this repository.
3. Confirm the source edition/transcription metadata
   (`validation/source_edition_metadata_required.md`) — requires the repo owner.
4. Extend the Network Explorer to all 12 network variants; build remaining figures
   (F01, F04-F05, F08-F09, F12-F14).
5. **Only on explicit user request:** push `claude-dk-rebuild` to the remote, deploy the site to a
   live GitHub Pages URL, or open a PR to `main`. Nothing has been pushed anywhere yet.
6. Fill in `CITATION.cff` TODO fields once the repository owner confirms their details.

## Known environment quirk (not a real blocker)

On this machine, some scipy submodules (`scipy.cluster.hierarchy` → `scipy.spatial`/`scipy.sparse`)
can take 120s+ on their *first* import in a session (an Application Control Policy / antivirus DLL
scan), sometimes timing out. Retrying the same command (with a longer timeout, e.g. 150000ms)
resolves it — this happened once and was not a real code or dependency problem.

## Rules that must not be relaxed, ever

- Never invent unsupported data, metadata, academic findings, citation/DOI info, or author names.
- Centrality ≠ literary importance.
- Mark `not_applicable` rather than forcing a result on insufficient data.
- `data/raw/` and `data/final/` stay untouched.
- No merge/push to `main`, no push to remote at all without explicit user request.
- Git commits via PowerShell: avoid embedded double quotes in `-m`, use `git commit -F <tempfile>`.
  Avoid PowerShell `-replace`/`Get-Content | Set-Content` on UTF-8 files with non-ASCII characters
  - use the Edit tool or a small Python script instead.
- Test any website change against a real local HTTP server (`python -m http.server` from `docs/`),
  never just a `file://` preview.
