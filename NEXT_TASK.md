# CURRENT PROJECT STATUS

**VALIDATED RESEARCH REPOSITORY — PUBLICATION BLOCKERS REMAIN** (a technical release candidate; it is
**not** publication-ready).

Branches: `claude-dk-rebuild` is the independently reviewed state (pushed to the remote). The
post-review corrections live on the **local** branch `claude-dk-fixpass` (starting commit `4e89da5`);
it has not been pushed, merged or deployed. `main` is untouched.

All 21 phases of the governing master prompt are complete, plus: the story-similarity addendum (RQ6,
DEC-014), the final academic audit (DEC-015), full end-to-end pipeline verification (DEC-016), and the
independent-review fix pass (DEC-017 weighted-betweenness distance, DEC-018 composite-node review scan,
DEC-019 site/registry/wording consistency). See `reports/FIX_PASS_REPORT.md`.

Research questions: RQ1, RQ3, RQ4, RQ5 answered (RQ4 confirmatory; RQ5 a descriptive sensitivity
analysis); RQ2, RQ7 partially answered (exploratory); **RQ6 PARTIALLY ANSWERED / EXPLORATORY** — story-level
similarity can be quantified and visualized, but evidence for a robust discrete clustering structure is
limited (`thesis/research_questions.md`, `outputs/statistics/story_similarity_cluster_validity.json`).

## Start by reading (in this order)

1. `CLAUDE_SESSION_HANDOFF.md` — full state; see the "INDEPENDENT REVIEW FIX PASS" section for the latest work
2. `reports/FIX_PASS_REPORT.md` — per-issue status of the independent review's findings
3. `reports/EXECUTIVE_SUMMARY.md` (~4 min read) and `reports/FINAL_REBUILD_REPORT.md`
4. `reports/RELEASE_CHECKLIST.md` (open blockers, classified)
5. `docs/decision_log.md` DEC-014 … DEC-019
6. `outputs/results_registry.json` — the generated single source for the scientific numbers quoted by the
   site (stage/test counts, composite-candidate counts, sensitivity and robustness values live there,
   not in prose)

## There is no next mandatory task

Do not invent new phases. Recommended next step: an independent re-review of `claude-dk-fixpass`.
Push, merge to `main`, GitHub Pages deployment, tags and releases happen **only on the owner's explicit
authorization** (a push needs the GitHub login with `repo` and `workflow` scopes).

## Open publication blockers (external / manual — the fix pass did NOT change their status)

1. **Source edition/transcription verification** — needs the repository owner
   (`validation/source_edition_metadata_required.md`).
2. **Inter-annotator reliability** — needs a real second coder (`docs/inter_annotator_protocol.md`,
   `src/inter_annotator_stats.py` ready and waiting).
3. **Manual review of unresolved entity items** — `validation/HUMAN_REVIEW_QUEUE.csv`, including the candidate
   composite actor nodes (`validation/composite_node_candidates.csv`); needs the original narrative text,
   which is not in this repository. No node is split or merged automatically.
4. **`CITATION.cff` personal/bibliographic metadata** — needs the repository owner.
5. **Source-code licence** — the dataset is CC BY 4.0; no code licence has been chosen (owner decision;
   nothing in the repository implies one).
6. **Manuscript** — `paper/` is an outline + methods + results + supplement package; the Introduction,
   Discussion and References are unwritten and no literature review has been done.

## Other optional items (only on explicit user request)

- Extend the Network Explorer to all 12 network variants; build the remaining figures (F01, F04-F05,
  F08-F09, F12-F14).
- For RQ6: a robust discrete story grouping, if one exists, would need richer story-level features than the
  current relation-type/layer profile (e.g. coded thematic variables); none exist in the canonical dataset.

## Known environment quirks (not real blockers)

- Some scipy submodules (`scipy.cluster.hierarchy` → `scipy.spatial`/`scipy.sparse`) can take 120s+ on their
  *first* import in a session (an Application Control Policy / antivirus DLL scan); retrying resolves it.
- With `core.autocrlf=true` on Windows, `git checkout` writes CRLF into files the pipeline writes as LF (for
  example `.gexf`), so their manifest hashes match the files as the pipeline writes them, not a fresh CRLF
  checkout. Regenerate with the pipeline rather than restoring such files with `git checkout`.
- A command guard can false-positive on a bare `p:` token inside inline PowerShell here-strings; write
  scratch scripts to files instead.

## Rules that must not be relaxed, ever

- Never invent unsupported data, metadata, academic findings, citation/DOI info, or author names.
- Never write an LLM inference (e.g. a narrative theme that is not a coded variable) as a
  quantitative/network-analysis finding.
- `weight` is tie STRENGTH. Shortest-path metrics use `distance = 1 / strength`; never pass strength as a
  NetworkX distance (`tests/test_distance_semantics.py` enforces this).
- "Most similar pair" means relatively most overlapping among the evaluated stories — never write
  "highly similar", "strong similarity", "clear clusters" for RQ6.
- Do not merge or split composite/candidate actor nodes without a human review against the original text.
- Do not maintain the same scientific value in several handwritten places: quote it from
  `outputs/results_registry.json` or derive it.
- Centrality ≠ literary importance. Mark `not_applicable` rather than forcing a result on insufficient data.
- `data/raw/` and `data/final/` stay untouched.
- No merge/push to `main`, no push to any remote, no Pages deployment and no tag/release without explicit
  user authorization.
- Git commits via PowerShell: avoid embedded double quotes in `-m`, use `git commit -F <tempfile>`.
  Avoid PowerShell `-replace`/`Get-Content | Set-Content` on UTF-8 files with non-ASCII characters — use the
  Edit tool or a small Python script instead.
- Test any website change against a real local HTTP server (`python -m http.server` from `docs/`), never
  just a `file://` preview.
