# Contributing

This project's core scientific rule (see `CLAUDE_SESSION_HANDOFF.md` and `docs/decision_log.md`)
is: **never invent data.** Every contribution rule below exists to protect that.

## Adding a New Relation Annotation

If you are adding a new coded relation (a new row conceptually equivalent to a
`data/processed/relations_event_level.csv` row):

1. **Do not edit `data/final/` or `data/raw/` directly.** These are treated as immutable
   historical snapshots (legacy v3 and the original raw workbook, respectively).
2. Trace your new relation to specific `raw_evidence` — the actual narrative text supporting it.
   A relation without a quotable textual basis should not be added.
3. Classify it using the existing `standard_relation` taxonomy
   (`data/processed/relation_taxonomy.csv`, documented in `docs/relation_codebook.md`) where
   possible. If none fits, propose a new relation type explicitly, with its own family assignment
   and rationale — do not silently reuse `belirsiz` (uncertain) to avoid the decision, and do not
   silently force it into an ill-fitting existing category either.
4. Mark `extraction_method` honestly: `açık_ilişki` (explicit) only if the text directly states
   the relation; otherwise use or extend the `inferred`-style categories, and expect it to be
   included in the explicit-vs-inferred sensitivity comparison (`src/sensitivity.py`).
5. If you are uncertain about `polarity`, `directionality`, or `weight`, do not guess a value that
   looks reasonable — leave it for manual review (add a row to
   `validation/HUMAN_REVIEW_QUEUE.csv`) rather than filling in an unsupported value.
6. Re-run the pipeline after any data change: `python run_pipeline.py --all` (or at minimum
   `--stage validate` and `--stage build_canonical`) and `python -m pytest tests/`, so
   downstream networks/metrics/figures/tables/the website all reflect the change consistently.

## Adding Metadata (gender, faction, lineage, social status, narrative role, etc.)

These fields are deliberately **absent** from `data/processed/nodes.csv` because the current
dataset does not support them without inference. If you have genuine textual or scholarly
evidence for such an attribute:

1. Add it to `validation/manual_actor_metadata_template.csv` (create this file if it does not yet
   exist) rather than directly to `nodes.csv`.
2. Cite the specific evidence (a quote, a scholarly source) for each value.
3. Mark it `needs_manual_validation=1` until an independent reviewer confirms it.
4. Never derive such a field from an LLM's inference alone and present it as verified data.

## Proposing an Entity Merge

Entity resolution changes (merging two node IDs believed to represent the same actor) must:

1. Be proposed first in `validation/entity_resolution_candidates.csv` with `entity_a`, `entity_b`,
   `evidence`, `proposed_action`, and `confidence`.
2. Only be applied automatically (in `src/build_canonical.py`) if `confidence == "high"` and the
   evidence is unambiguous (e.g., identical canonical name and type). Anything else stays a
   proposal pending human review — see `docs/decision_log.md` DEC-002 for the one precedent case.

## Code Contributions

- Follow the existing pattern: one script per pipeline stage under `src/`, each independently
  runnable and also orchestrated by `run_pipeline.py`.
- Read parameters from `config/analysis.yaml` — do not hardcode seeds, thresholds, or iteration
  counts inline.
- If a new analysis cannot be run meaningfully on this data (too sparse, too few samples), have it
  report `not_applicable` with a stated reason rather than a forced or approximate result — see
  the precedents in `src/signed_and_directed.py` (structural balance) and `docs/decision_log.md`
  DEC-006, DEC-010.
- Add or update `tests/` coverage for any new canonical-data transformation.
- Never target `main` directly; work on a feature branch.

## Website Changes

Test any change to `docs/*.html` or `docs/assets/` against a real local HTTP server
(`python -m http.server` from inside `docs/`), never just by opening the file directly —
GitHub Pages only publishes the `docs/` subtree, and a `file://` preview will not reveal a link
that only works against a full repository checkout. Run `python src/validate_site.py` after any
change and confirm it reports 0 issues before committing.
