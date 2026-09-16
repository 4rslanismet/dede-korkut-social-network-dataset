# CURRENT PROJECT STATUS

PHASES 1-17 COMPLETE AND COMMITTED (repository audit through full documentation set; Phase 9-10
motif/triad explicitly skipped with documented rationale, DEC-010).

NEXT:
PHASE 18 — PAPER PACKAGE, THEN PHASE 19 — THESIS PACKAGE

## Start by reading

1. `CLAUDE_SESSION_HANDOFF.md` — full state, "PHASE 18-19 — NEXT WORK" section has the detailed
   task breakdown
2. `docs/MASTER_PROMPT.md` sections 43 (research questions), 91-96 (paper), 95 (thesis)
3. `docs/methodology.md`, `docs/limitations.md` — reusable content for the paper's methods and
   limitations sections
4. Every `reports/*.md` file (01 through 17) — this is where every citable finding already lives

**Do not rebuild Phases 1-17.** This is a writing/assembly task from existing findings.

## Critical rule for this phase (section 94)

Write every result as a **measured, hedged statement** tied to a specific network specification,
never as an unhedged literary claim. Correct: "Salur Kazan exhibited the highest betweenness
centrality (0.388) under the person-only core-social network specification (G1_person_only),
though this is a preliminary descriptive result." Incorrect: "Salur Kazan is the most important
character." This rule was already followed throughout `reports/*.md` — the paper/thesis text
should inherit that discipline exactly, not loosen it for readability.

## Task: Phase 18 — Paper Package (`paper/`)

1. `paper/manuscript_outline.md` (structure: Introduction, Related Work, Materials and Data,
   Methods, Results, Discussion, Limitations, Conclusion, Data/Code Availability — section 93).
   The three most defensible headline findings to build the paper around: (a) community modularity
   is validated as a real signal beyond the degree sequence in 7/9 tested networks (Phase 7), (b)
   the earlier "disassortative network" claim did NOT survive null-model testing and was retracted
   (Phase 7) - itself a notable methodological result about the risk of unvalidated descriptive
   network statistics, (c) person+group vs. person-only is the single most consequential network-
   construction choice tested (Phase 8).
2. `paper/methods.md` (adapt from `docs/methodology.md`).
3. `paper/results.md` (pull from `reports/04_05`, `06`, `07`, `08` - every number traceable to a
   specific `outputs/` file; separate exploratory vs. confirmatory findings per section 44/110;
   report effect sizes/z-scores/q-values, not just significance, per section 111).
4. `paper/figures/`, `paper/tables/` (copy from `outputs/figures/`, `outputs/tables/publication/`).
5. `paper/supplementary_material.md` (full metric tables, null model details, coding protocol,
   taxonomy, validation results - section 96).

## Task: Phase 19 — Thesis Package (`thesis/`)

1. `thesis/proposed_structure.md`, `thesis/research_questions.md` - map to RQ1-RQ7 (master prompt
   section 43); explicitly mark which RQs this dataset can only partially answer given the
   limitations already catalogued in `docs/limitations.md` (e.g., RQ4's null-model question is
   answerable; a hypothetical RQ about "which character is most important" is explicitly NOT
   answerable given this project's own rules).
2. `thesis/methodology_mapping.md`, `thesis/results_mapping.md` - map each RQ to the specific
   report/script/output addressing it.
3. `thesis/figure_inventory.md`, `thesis/table_inventory.md`.

## Then continue in master-plan order

PHASE 20 final validation/release (cross-check every number across README/paper/thesis/canonical
data/website for consistency - a good candidate for a small `src/validate_release_consistency.py`
script rather than manual checking) -> PHASE 21 final reports (`reports/FINAL_REBUILD_REPORT.md`,
`reports/EXECUTIVE_SUMMARY.md`, `reports/RELEASE_CHECKLIST.md`).

## Known gaps carried forward

- Story similarity (section 17) still not fully computed - if the paper/thesis wants to discuss
  story-level clustering, either compute the full metric suite first or scope the claim to what
  the raw shared-actor projection actually supports.
- 5 concatenated-multi-actor nodes discovered in Phase 15, unresolved (DEC-013) - mention as a
  data-quality limitation if the paper discusses entity resolution.
- G9_directed has no null-model comparison; degree assortativity is NOT validated (retracted,
  Phase 7) - do not cite it as fact in the paper/thesis.
- Site not yet deployed to actual GitHub Pages (tested locally only).
- CITATION.cff has TODO placeholders for author name and date - resolve with the repository owner
  before any real publication, don't fill in guessed values.

## Rules that must not be relaxed

- Never invent unsupported data, metadata, academic findings, citation/DOI info, or author names.
- Centrality ≠ literary importance - the paper/thesis must preserve this discipline.
- Mark `not_applicable` rather than forcing a result on insufficient data.
- `data/raw/` and `data/final/` stay untouched.
- No merge/push to `main`. No force-push. Local commits on `claude-dk-rebuild` only.
- Git commits via PowerShell: avoid embedded double quotes in `-m`, use `git commit -F <tempfile>`.
  Avoid PowerShell `-replace`/`Get-Content | Set-Content` on UTF-8 files with non-ASCII characters
  (corrupted em-dashes/Turkish characters once this session) - use the Edit tool or a small Python
  script instead.
