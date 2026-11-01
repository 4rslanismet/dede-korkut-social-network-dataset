# Rebuild V2 — 01 Repository Audit

Independent audit performed from `main` commit `149df2a`, 2026-11-01.

All counts recomputed directly from data files — no prior audit reports consulted.

## 1. Repository Structure

| Category | Count |
|---|---|
| Total tracked files | 781 |
| Source modules (`src/`) | 32 |
| Test modules (`tests/`) | 9 |
| Output files (`outputs/`) | 177 |
| Network files (`outputs/networks/`) | 64 |
| Figures | 14 (7 SVG + 7 PNG pairs) |
| Character pages (`docs/characters/`) | 332 |
| Story pages (`docs/stories/`) | 14 |
| Reports (`reports/`) | 17 |
| Validation files (`validation/`) | 7 |

## 2. Data Files

### 2.1 Protected Source Data

| Directory | Files | Status |
|---|---|---|
| `data/raw/` | 1 (XLSX workbook) | Immutable, hashed |
| `data/final/` | 7 data + 1 .gitkeep | Immutable, hashed |
| `data/story_level/` | 14 per-story CSVs | Immutable, hashed |

All hashes recorded in `validation/source_baseline_hashes.csv`.

### 2.2 Canonical Dataset (`data/processed/`)

| File | Records |
|---|---|
| `nodes.csv` | 332 |
| `relations_event_level.csv` | 628 |
| `relations_aggregated.csv` | 376 |
| `stories.csv` | 14 |
| `aliases.csv` | 525 |
| `provenance.csv` | 628 |
| `relation_taxonomy.csv` | 17 |
| `validation_status.csv` | 25 checks |

### 2.3 Legacy Source Counts

| File | Records |
|---|---|
| `dede_korkut_dugumler_temiz.csv` | 333 nodes |
| `dede_korkut_kenarlar_temiz.csv` | 628 edges |
| `dede_korkut_olaylar_temiz.csv` | 85 events |
| `dede_korkut_alias_sozlugu.csv` | 525 aliases |
| `00_boy_dataset_indeksi_temiz.csv` | 14 stories |
| Story-level CSVs (total rows) | 633 |

### 2.4 Story-Level vs Final Reconciliation

Story-level CSVs contain 633 rows; `kenarlar_temiz` contains 628. The 5 extra
story-level rows (DKR0122, DKR0167, DKR0252, DKR0345, DKR0708) exist in
story-level files but were not carried into the final edge table. These correspond
to records that were separated during the cleaning process — their disposition
should be verified in the provenance audit.

## 3. Core Counts

| Metric | Value |
|---|---|
| Narrative units | 14 |
| Boy stories | 13 |
| Non-boy sections (girizgah) | 1 |
| Legacy nodes | 333 |
| Canonical nodes | 332 (333 − 1 entity merge) |
| Event-level relations | 628 |
| Aggregated relations (unique pairs) | 376 |
| Narrative events | 85 |
| Node types | 6 |
| Relation types | 17 |
| Relation family_top categories | 6 |
| Relation layers | 7 |
| Source files (story-level) | 14 |

## 4. Node Types

| Type | Count |
|---|---|
| kişi (person) | 187 |
| grup (group) | 124 |
| mitolojik/ilahi (mythological/divine) | 8 |
| hayvan (animal) | 6 |
| nesne/doğa (object/nature) | 6 |
| yer/coğrafya (place/geography) | 1 |

## 5. Relation Types (17)

| Type | Count | Family | Top |
|---|---|---|---|
| belirsiz (uncertain) | 186 | uncertain | UNCERTAIN |
| çatışma (conflict) | 102 | conflict | SOCIAL |
| akrabalık (kinship) | 68 | kinship | KINSHIP |
| otorite/emir (authority/command) | 57 | authority | AUTHORITY |
| diyalog_nötr (neutral dialogue) | 54 | communication | SOCIAL |
| ikna/müzakere (persuasion/negotiation) | 42 | cooperation | SOCIAL |
| diyalog_olumlu (positive dialogue) | 29 | communication | SOCIAL |
| destek/yardım (support/aid) | 27 | support | SOCIAL |
| diyalog_olumsuz (negative dialogue) | 12 | communication | SOCIAL |
| evlilik/bağlaşıklık (marriage/alliance) | 10 | marriage_alliance | KINSHIP |
| ödül/değişim (reward/exchange) | 9 | cooperation | SOCIAL |
| hareket/eylem (action/movement) | 9 | other | OTHER |
| gerilim (tension) | 7 | conflict | SOCIAL |
| tören/ritüel (ceremony/ritual) | 7 | other | OTHER |
| duygusal_tepki (emotional reaction) | 4 | other | OTHER |
| coğrafi_epitet (geographic epithet) | 3 | identity_title | SEMANTIC |
| kimlik/unvan (identity/title) | 2 | identity_title | SEMANTIC |

## 6. Relation Family Distribution

| Family Top | Count | % |
|---|---|---|
| SOCIAL | 282 | 44.9% |
| UNCERTAIN | 186 | 29.6% |
| KINSHIP | 78 | 12.4% |
| AUTHORITY | 57 | 9.1% |
| OTHER | 20 | 3.2% |
| SEMANTIC | 5 | 0.8% |

## 7. Layers (7)

| Layer | Count |
|---|---|
| olay (event) | 230 |
| iletişim (communication) | 140 |
| çatışma (conflict) | 109 |
| akrabalık (kinship) | 78 |
| otorite (authority) | 66 |
| mekân (spatial) | 3 |
| kimlik (identity) | 2 |

## 8. Polarity Distribution

| Polarity | Count |
|---|---|
| nötr (neutral) | 315 |
| pozitif (positive) | 166 |
| negatif (negative) | 119 |
| karışık (mixed) | 28 |

## 9. Directionality

| Directionality | Count |
|---|---|
| yönlü (directed) | 441 |
| yönsüz (undirected) | 187 |

## 10. Extraction Method

| Method | Count |
|---|---|
| açık_ilişki (explicit relation) | 596 |
| çıkarımsal_akrabalık (inferred kinship) | 29 |
| manuel_turkistan_ekleme (manual Turkistan addition) | 2 |
| epitet_aktarım (epithet transfer) | 1 |

## 11. Data Integrity Checks

| Check | Result |
|---|---|
| Duplicate node IDs | 0 — PASS |
| Duplicate relation IDs | 0 — PASS |
| Orphan source endpoints | 0 — PASS |
| Orphan target endpoints | 0 — PASS |
| Self-loops | 1 (DKR0220: bamsi_beyrek → bamsi_beyrek) |
| same_name_multiple_ids | 2 |
| invalid_id_format | 0 — PASS |
| invalid_layer | 0 — PASS |
| invalid_polarity | 0 — PASS |
| invalid_weight | 0 — PASS |
| invalid_directionality | 0 — PASS |
| exact_duplicate_relationship | 2 |
| repeated_actor_pair_pattern | 114 |

### Self-loop note
DKR0220 (bamsi_beyrek → bamsi_beyrek) is a documented self-loop. It appears
to represent a reflexive relation in the source coding. Flagged but not an error
per se — requires human judgment on whether to keep or remove.

### Same-name-multiple-IDs note
2 cases where the same canonical name maps to multiple node IDs. These may be
legitimate (different characters with the same name in different stories) or
may warrant entity-resolution review.

## 12. Per-Story Relation Counts

All 14 stories have actual event-level relation counts matching their declared
`n_edges` in `stories.csv` — PASS.

| Story | Relations | Events | Nodes Declared |
|---|---|---|---|
| S01 (Girizgah) | 1 | 0 | 2 |
| S02 | 23 | 3 | 15 |
| S03 | 51 | 0 | 48 |
| S04 | 107 | 21 | 76 |
| S05 | 40 | 6 | 39 |
| S06 | 22 | 2 | 13 |
| S07 | 40 | 12 | 26 |
| S08 | 24 | 4 | 19 |
| S09 | 65 | 9 | 43 |
| S10 | 59 | 6 | 35 |
| S11 | 54 | 7 | 32 |
| S12 | 67 | 13 | 34 |
| S13 | 39 | 2 | 22 |
| S14 | 36 | 0 | 20 |

## 13. Provenance Status

| Status | Count |
|---|---|
| matched_unique | 571 |
| unmatched_provenance_gap | 53 |
| matched_ambiguous | 4 |

53 provenance gaps (8.4%) — these are relations in the final dataset where the
exact source row in story-level files could not be unambiguously matched. This
is documented and expected given the cleaning transformations.

## 14. Alias Coverage

| Check | Count |
|---|---|
| Total alias entries | 525 |
| Aliases resolving to current node | verified via validation_status |
| alias_maps_to_multiple_targets | 17 |
| alias_target_not_in_node_table | 73 |

73 alias targets not in the node table — these appear to be aliases referencing
legacy names that were merged or renamed during entity resolution. Flagged for
human review.

## 15. Network Models

12 network model variants (G0–G11) present in `outputs/networks/`:

| Model | Files |
|---|---|
| G0 full | GEXF + GraphML + nodes CSV + edges CSV |
| G1 person-only | GEXF + GraphML + nodes CSV + edges CSV |
| G2 core-social | GEXF + GraphML + nodes CSV + edges CSV |
| G3 kinship | GEXF + GraphML + nodes CSV + edges CSV |
| G4 communication | GEXF + GraphML + nodes CSV + edges CSV |
| G5 cooperation/support | GEXF + GraphML + nodes CSV + edges CSV |
| G6 conflict | GEXF + GraphML + nodes CSV + edges CSV |
| G7 positive | GEXF + GraphML + nodes CSV + edges CSV |
| G8 negative | GEXF + GraphML + nodes CSV + edges CSV |
| G9 directed | GEXF + GraphML + nodes CSV + edges CSV |
| G10 weighted | GEXF + GraphML + nodes CSV + edges CSV |
| G11 unweighted | GEXF + GraphML + nodes CSV + edges CSV |

Story-level network files: 14 per-story networks present.

## 16. Output Artifacts

| Category | Files |
|---|---|
| Figures (SVG+PNG) | 14 |
| Tables | present in `outputs/tables/` |
| Statistics/JSON | 18 |
| Network files | 64 |
| Matrices | 8 |
| Manifest | `outputs/manifest_sha256.csv` |
| Results registry | `outputs/results_registry.json` |

## 17. Website

| Check | Status |
|---|---|
| Character pages | 332 (matches canonical nodes) |
| Story pages | 14 (matches narrative units) |
| Static pages | Home, Dataset, Methodology, Analysis, etc. |
| CSS/JS assets | Present |
| Network explorer | `docs/assets/explorer.js` present |

## 18. Documentation & Academic Packages

| Item | Status |
|---|---|
| CLAUDE.md | Present (created in this rebuild) |
| AI_ASSISTANCE.md | Present (created in this rebuild) |
| README.md | Updated with AI disclosure |
| CITATION.cff | Present, author metadata marked TODO |
| paper/ | Present (incomplete) |
| thesis/ | Present (incomplete) |
| Inter-annotator protocol | Present |
| Literature search plan | Present |

## 19. Validation Infrastructure

| Item | Status |
|---|---|
| CI workflow | `.github/workflows/validate.yml` |
| Source baseline hashes | `validation/source_baseline_hashes.csv` |
| Composite node candidates | `validation/composite_node_candidates.csv` |
| Entity resolution candidates | `validation/entity_resolution_candidates.csv` |
| Human review queue | `validation/HUMAN_REVIEW_QUEUE.csv` |
| Inter-annotator sample | `validation/inter_annotator_sample.csv` |
| Source edition metadata required | `validation/source_edition_metadata_required.md` |

## 20. Summary

The repository is structurally sound and comprehensive. Key findings:

1. **All core counts verified independently**: 332 nodes, 628 event-level relations,
   376 aggregated edges, 14 narrative units, 85 events, 17 relation types, 7 layers.
2. **No referential integrity violations**: zero orphan endpoints, zero duplicate IDs.
3. **1 self-loop** (DKR0220) — documented, requires human judgment.
4. **5 story-level rows** not in final edges — disposition to be verified in provenance audit.
5. **53 provenance gaps** (8.4%) — documented and expected.
6. **73 alias targets** not in node table — legacy artifacts, flagged for review.
7. **All 12 network models** built and exported.
8. **Website coverage**: 332 character pages + 14 story pages (exact match).
9. **Publication blockers** remain: source edition, second annotator, citation metadata,
   code license, incomplete paper/thesis.
