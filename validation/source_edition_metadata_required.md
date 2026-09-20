# Source Edition Metadata — REQUIRED

## Problem

`data/raw/dede korkut karakterler.xlsx` does not correspond, row-for-row or
column-for-column, to `data/story_level/*.csv` or `data/final/*.csv` (see
`reports/01_repository_audit.md`, section 4). Its schema (`Source, Target,
Weight, Type`) is a different, coarser network-export format than the
21-column `story_level` schema.

This means the actual raw coding source used to produce `story_level` (i.e.,
which printed edition, transcription, or translation of the Book of Dede
Korkut was read line-by-line to produce `satir_no`-referenced records) is
**not present in this repository** and is **not documented** in
`README.md`, `docs/README_v2.md`, or `docs/README_v3.md`.

Per the project's provenance rule, this is treated as a critical missing
metadata item, not guessed at.

## Information needed from the original researcher/annotator

- [ ] Which printed edition / critical text of Dede Korkut was used as the
      reading source (e.g. Ergin, Gökyay, Tezcan-Boeschoten, or another)?
- [ ] Edition year and publisher.
- [ ] Whether `satir_no` refers to a specific edition's line numbering, a
      manuscript's, or an internal working transcription.
- [ ] Whether `data/raw/dede korkut karakterler.xlsx` was an earlier,
      abandoned coding pass, or a separate exercise unrelated to
      `story_level`/`final`.
- [ ] Whether original line-by-line raw coding notes (pre-story_level) exist
      anywhere outside this repository and could be added under
      `data/raw/` without violating copyright (see project rule 99 — do not
      redistribute copyrighted source text; only structured coding
      annotations, not the literary text itself, should be added).

## Until this is filled in

- `data/raw/` is left untouched.
- Any academic output (paper/thesis package) referencing "the text of Dede
  Korkut" must say the specific edition is **unspecified in the current
  repository metadata**, not assume a specific one.
