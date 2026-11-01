# Data Dictionary

Every column of every file in `data/processed/` (the canonical rebuild, Phase 3). Non-null counts,
distinct-value counts, and sample values below were computed directly from the files at the time
this document was written (`src/build_canonical.py` output) — re-run the pipeline and re-inspect
the files if you suspect drift.

Legacy `data/final/` (v3) files are documented separately in `docs/README_v3.md` and are not
re-described here; they are inputs to, not outputs of, this rebuild.

---

## `nodes.csv` (332 rows)

| Field | Type | Non-null | Meaning | Allowed values | Source |
|---|---|---|---|---|---|
| `node_id` | string | 332/332 | Unique slug identifier for the actor | `^[a-z0-9_]+$`, unique | Derived from `data/final/dede_korkut_dugumler_temiz.csv`'s `dugum_id`, with the single `begil_in_adamlari`→`begilin_adamlari` merge applied (DEC-002) |
| `canonical_name` | string | 332/332 | Display name of the actor | Free text (Turkish) | `dugum_adi` |
| `node_type` | string | 332/332 | Actor category | `kişi`, `grup`, `mitolojik/ilahi`, `hayvan`, `nesne/doğa`, `yer/coğrafya` (6 observed values) | `dugum_tipi` |
| `aliases` | string | 302/332 | `;`-joined list of raw forms that map directly (single-hop) to this `canonical_name` in `dede_korkut_alias_sozlugu.csv` | Free text or empty | Derived; **known limitation**: only single-hop matches, see `aliases.csv` below and `validation/HUMAN_REVIEW_QUEUE.csv` |
| `first_story` | string | 332/332 | `story_id` of the earliest story (by **corpus order**, not chronology) in which this actor is referenced | `S01`-`S14` | Derived from `relations_event_level.csv` + `relations_...`/events |
| `story_count` | int | 332/332 | Number of distinct stories this actor appears in (edges or events) | ≥1 | Derived |
| `relation_count` | int | 332/332 | Number of event-level relations (edges) this actor is source or target of | ≥0 (0 = event-only actor) | Derived |
| `event_count` | int | 332/332 | Number of narrative events (non-relational, `dede_korkut_olaylar_temiz.csv`) this actor is actor/target of | ≥0 | Derived |
| `validation_status` | string | 332/332 | `ok` or `needs_manual_validation` | 2 values | Set by `src/build_canonical.py` for the 2 merged node rows |
| `source` | string | 332/332 | Which legacy file (+ merge note) this row derives from | 2 distinct strings | Set by pipeline |
| `notes` | string | 1/332 | Free-text note (currently only populated for the merged Begil'in Adamları node) | Free text or empty | Set by pipeline |

**Not present, intentionally:** `gender`, `faction`, `lineage`, `social_status`, `narrative_role` — the source data does not support these without LLM inference, which this project's rules prohibit (Master Scientific Rule #2).

---

## `aliases.csv` (525 rows)

| Field | Type | Non-null | Meaning | Allowed values |
|---|---|---|---|---|
| `raw_form` | string | 525/525 | The original/raw expression as it appeared in coding | Free text, 389 distinct |
| `standard_form` | string | 525/525 | The standardized form it was mapped to | Free text, 347 distinct |
| `role_context` | string | 525/525 | Which coding role this alias entry was recorded under | `karakter_1`, `karakter_2`, `event_aktor`, `event_hedef`, and 2 others |
| `resolves_to_current_node` | bool | 525/525 | Whether `standard_form` matches a current `nodes.csv` `canonical_name` | `True`/`False` |
| `validation_status` | string | 525/525 | `ok` or `needs_manual_validation_stale_target` | 2 values |

**Known limitation:** this table is a **multi-hop standardization history** (v1→v2→v3), not a
single-hop lookup — 73 rows have `resolves_to_current_node=False` because `standard_form` is an
intermediate v1/v2 name later re-standardized again in v3. See `reports/02_data_quality_report.md`
§4 and `validation/HUMAN_REVIEW_QUEUE.csv` (category `stale_alias_target`, 45 items).

---

## `stories.csv` (14 rows)

| Field | Type | Non-null | Meaning | Allowed values |
|---|---|---|---|---|
| `story_id` | string | 14/14 | Canonical story identifier | `S01`-`S14` |
| `corpus_order` | int | 14/14 | Position in the corpus as presented (file-listing order 01-14) — **not** historical chronology | 1-14 |
| `source_file` | string | 14/14 | Legacy `data/story_level/` filename this story derives from | 14 distinct filenames |
| `boy_name_raw` | string | 14/14 | Display name of the story, exactly as it appears in `dede_korkut_kenarlar_temiz.csv`'s `boy` column | Free text (capitalization/punctuation inconsistent across rows — see `reports/01_repository_audit.md` §5.2) |
| `section_type` | string | 14/14 | `girizgah` (prologue, 1 story) or `boy` (13 stories) | 2 values |
| `n_edges` | int | 14/14 | Edge count for this story per `00_boy_dataset_indeksi_temiz.csv` | ≥1 |
| `n_events` | int | 14/14 | Event count for this story per the same index | ≥0 |
| `n_nodes_declared_in_index` | int | 14/14 | Node count as declared in the legacy index file (not independently recomputed here — see `data/derived/story_level_metrics.csv` for an independently-computed `n_nodes`) | ≥2 |

---

## `relations_event_level.csv` (628 rows) — the primary edge table

| Field | Type | Non-null | Meaning | Allowed values |
|---|---|---|---|---|
| `relation_id` | string | 628/628 | Unique ID, inherited from the legacy `kayit_id` | `DKR####`, unique |
| `story_id` / `story_name` | string | 628/628 | Which story this relation belongs to | `story_id`: S01-S14 |
| `section_type` | string | 628/628 | `boy` or `girizgah` | 2 values |
| `narrative_order` | float | 626/628 | **Narrative order within the story** (from legacy `satir_no`) — **never** historical/chronological time (Master Scientific Rule #8) | Numeric, 2 rows missing (both in story S03, a known limitation — see `reports/06...` §5.2) |
| `source_id` / `source_name` / `source_type` | string | 628/628 | The relation's source actor | `source_type`: 4 of the 6 `node_type` values appear as sources |
| `target_id` / `target_name` / `target_type` | string | 628/628 | The relation's target actor | `target_type`: all 6 `node_type` values appear as targets |
| `raw_relation` | string | 607/628 | The original/raw relation text (legacy `iliski_ham`) | Free text; 21 rows null |
| `standard_relation` | string | 628/628 | Standardized relation type | 17 distinct values, see `relation_taxonomy.csv` |
| `relation_family` / `relation_family_top` | string | 628/628 | Interpretive taxonomy mapping (DEC-004) — **not a raw-data fact** | `relation_family_top`: SOCIAL, KINSHIP, AUTHORITY, SEMANTIC, OTHER, UNCERTAIN |
| `layer` | string | 628/628 | Relation layer (distinct from `relation_family` — see `docs/methodology.md`) | akrabalık, iletişim, çatışma, otorite, kimlik, mekân, olay (7 values) |
| `weight` | int | 628/628 | Legacy `agirlik` — an ordinal 1-5 coding whose exact semantics are **not fully documented** (see `docs/limitations.md`) | 1-5 |
| `polarity` | string | 628/628 | Legacy `kutupluluk` | nötr, pozitif, negatif, karışık (4 values) |
| `directionality` | string | 628/628 | Legacy `yonluluk` | yönlü, yönsüz (2 values) |
| `extraction_method` | string | 628/628 | How this relation was coded | açık_ilişki (596), çıkarımsal_akrabalık, manuel_turkistan_ekleme, epitet_aktarım |
| `confidence` | float | **0/628** | Reserved field for a per-relation confidence score | **Not populated** — the source data has no such field at this granularity; deliberately left empty rather than invented (Master Scientific Rule #1) |
| `source_file` | string | 628/628 | Which `data/story_level/*.csv` file this relation's story derives from | 14 distinct filenames |
| `source_row` | float | 571/628 | Row index in the `data/story_level/` file this relation was matched to (best-effort, see `source_row_status`) | Numeric or empty |
| `raw_evidence` | string | 628/628 | The full original narrative line text this relation was coded from (legacy `ham_satir`) | Free text |
| `validation_status` | string | 628/628 | Always `ok` at event-relation granularity (issues are tracked in `outputs/validation/`, not per-row here) | 1 value |
| `notes` | string | 583/628 | Free-text annotator note (legacy `not`) | Free text or empty |
| `source_row_status` | string | 628/628 | Provenance match outcome | `matched_unique` (571, 90.9%), `unmatched_provenance_gap` (53, 8.4%), `matched_ambiguous` (4, 0.6%) |

---

## `relations_aggregated.csv` (376 rows) — unordered actor-pair aggregation

Aggregation rule: **unordered** actor pair (DEC-003) — `actor_a`/`actor_b` are alphabetically sorted, so directionality is not part of the grouping key (it's preserved via the `any_directed`/`any_undirected` flags instead).

| Field | Type | Meaning |
|---|---|---|
| `pair_id` | string | `P####`, unique per unordered actor pair |
| `actor_a`, `actor_b` | string | The two actors (`actor_a <= actor_b` alphabetically) |
| `interaction_count` | int | Number of underlying `relations_event_level.csv` rows for this pair |
| `total_weight` | int | Sum of `weight` across those rows |
| `positive_count`, `negative_count`, `neutral_count`, `mixed_count` | int | Count of underlying relations by `polarity` |
| `stories_shared` | int | Number of distinct stories this pair co-occurs in |
| `story_ids` | string | `;`-joined `story_id` list |
| `relation_types` | string | `;`-joined distinct `standard_relation` values for this pair |
| `relation_families` | string | `;`-joined distinct `relation_family` values |
| `layers` | string | `;`-joined distinct `layer` values |
| `any_directed`, `any_undirected` | bool | Whether at least one underlying relation was directed/undirected |

---

## `relation_taxonomy.csv` (17 rows)

| Field | Type | Meaning |
|---|---|---|
| `standard_relation` | string | One of the 17 observed relation types |
| `relation_family` | string | Interpretive sub-family (e.g. `communication`, `conflict`, `kinship`) |
| `relation_family_top` | string | Top-level family: SOCIAL, KINSHIP, AUTHORITY, SEMANTIC, OTHER, UNCERTAIN |
| `definition` | string | One-sentence definition/rationale for the mapping (DEC-004) |
| `n_occurrences` | int | Count in `relations_event_level.csv` |
| `share_of_all_edges_pct` | float | `n_occurrences` / 628 × 100 |

Full codebook with examples: `docs/relation_codebook.md`.

---

## `provenance.csv` (628 rows)

One row per `relations_event_level.csv` relation, recording its traceability back to
`data/story_level/`. See `reports/01_repository_audit.md` §3 for why `source_row_in_story_level`
is null for 57 rows (matched_ambiguous + unmatched_provenance_gap combined).

| Field | Type | Meaning |
|---|---|---|
| `relation_id` | string | Foreign key to `relations_event_level.csv` |
| `source_file_final` | string | Always `data/final/dede_korkut_kenarlar_temiz.csv` |
| `source_file_story_level` | string | The specific `data/story_level/*.csv` file |
| `source_row_in_story_level` | float | Row index if matched (see `source_row_status`) |
| `source_row_status` | string | `matched_unique` / `unmatched_provenance_gap` / `matched_ambiguous` |
| `transformation` | string | Fixed description of the column-rename + taxonomy-mapping transformation applied |
| `extraction_method` | string | Copied from `relations_event_level.csv` |
| `validation_status` | string | Always `ok` at this granularity |
| `annotator` | string | `"original repository coder (identity not recorded in source data)"` — deliberately not invented |
| `version` | string | Always `processed-v4-rebuild` |

---

## `validation_status.csv` (27 rows)

A flattened export of `outputs/validation/summary.json` (Phase 2): one row per
(`category`, `check`) pair with `n_flagged`. Categories: `node`, `edge`, `event`, `alias`. See
`reports/02_data_quality_report.md` for full interpretation of each check.
