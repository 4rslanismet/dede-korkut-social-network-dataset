# Inter-Annotator Reliability Protocol

## Purpose

This project currently has **one coder** (the original repository author). No
inter-annotator reliability statistic (Cohen's kappa, Krippendorff's alpha)
has been computed, because computing one without a genuine second coder
would mean fabricating agreement data — explicitly prohibited by this
project's rules (`docs/decision_log.md`, `CLAUDE_SESSION_HANDOFF.md` §
Master Scientific Rules #12-14).

This document describes how a second coder should annotate the sample in
[`validation/inter_annotator_sample.csv`](../validation/inter_annotator_sample.csv)
so that a real reliability statistic can eventually be computed by
[`src/inter_annotator_stats.py`](../src/inter_annotator_stats.py).

## Sample construction

`validation/inter_annotator_sample.csv` (70 rows) was built by
[`src/build_inter_annotator_sample.py`](../src/build_inter_annotator_sample.py)
from `data/processed/relations_event_level.csv`, stratified by
(`relation_family_top`, `extraction_method`) so that:

- All 14 stories are represented.
- Both common relation types (akrabalık, belirsiz, otorite/emir, çatışma)
  and rare ones (evlilik/bağlaşıklık, duygusal_tepki, gerilim) appear.
- Both `açık_ilişki` (explicit, the vast majority of the corpus) and every
  inferred/manual extraction method (`çıkarımsal_akrabalık`,
  `manuel_turkistan_ekleme`, `epitet_aktarım`) are represented, not just the
  dominant category.

Random seed: `config/analysis.yaml::seed` (42) — the sample is fully
reproducible by re-running the build script.

## What the second coder sees

Each row gives: `actor_1`, `actor_2`, `raw_evidence` (the original textual
justification recorded by coder 1), and `story_name`/`story_id` for
context. **The second coder does NOT see `coder1_relation`,
`coder1_layer`, or `coder1_polarity`** when annotating — those columns
exist in the CSV for later comparison, but should be hidden (e.g. copy the
file, delete those three columns, hand the second coder only the blinded
version) before handing off the sheet, to avoid anchoring bias.

## What the second coder fills in

For each row, using only `actor_1`, `actor_2`, and `raw_evidence`:

- `coder2_relation`: one of the 17 relation types documented in
  `data/processed/relation_taxonomy.csv` (or `belirsiz` if genuinely
  unclear from the evidence given).
- `coder2_layer`: one of the 7 layers observed in the corpus (`akrabalık`,
  `iletişim`, `çatışma`, `otorite`, `kimlik`, `mekân`, `olay`).
- `coder2_polarity`: one of `pozitif`, `negatif`, `nötr`, `karışık`.
- `agreement`: leave blank — this is computed automatically by
  `src/inter_annotator_stats.py` once both coders' columns are filled in.
- `notes`: free text, optional — record anything ambiguous about the
  `raw_evidence` given.

## After the second coder finishes

1. Merge the second coder's filled-in `coder2_relation`/`coder2_layer`/
   `coder2_polarity` back into `validation/inter_annotator_sample.csv`
   (matching on `relation_id`).
2. Run `python src/inter_annotator_stats.py`. It will compute Cohen's kappa
   (per field: relation, layer, polarity) and Krippendorff's alpha, and
   write `outputs/statistics/inter_annotator_agreement.json`.
3. **Do not report a kappa/alpha value anywhere in this project's reports
   or documentation until this step has actually been run with real
   second-coder data.** Until then, any inter-annotator reliability claim
   must say "not yet assessed — single-coder dataset."

## Known limitation

With only 70/628 event-level relations (11.1%) sampled, any resulting
kappa/alpha will have a specific, statable confidence interval (computed by
the stats script) — it should not be presented as characterizing the
reliability of the full 628-relation dataset without that caveat.
