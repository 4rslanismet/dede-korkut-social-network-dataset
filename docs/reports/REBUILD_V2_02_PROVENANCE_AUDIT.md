# Rebuild V2 — 02 Provenance Audit

## 1. Data Flow

```
data/raw/dede korkut karakterler.xlsx
    ↓ (unknown transformation — NOT documented)
data/story_level/*.csv (14 files, 633 rows)
    ↓ (cleaning, splitting edges from events, entity normalization)
data/final/ (dugumler, kenarlar, olaylar, alias_sozlugu, boy_index)
    ↓ (src/build_canonical.py: column rename, taxonomy mapping, entity merge, provenance attach)
data/processed/ (canonical dataset: nodes, relations, stories, aliases, provenance, taxonomy)
    ↓ (src/build_networks.py et al.)
outputs/ (networks, metrics, figures, tables)
```

## 2. Raw → Story-Level

**STATUS: UNRESOLVED**

The raw XLSX workbook (`data/raw/dede korkut karakterler.xlsx`) has a
4-column schema (`Source, Target, Weight, Type`) that does NOT correspond to
the 21-column `story_level` schema. This means:

- The XLSX is likely an earlier, coarser network-export format
- The actual line-by-line coding from the literary source is NOT present in the repository
- The source edition (which printed text of Dede Korkut was read) is UNKNOWN

**Conclusion**: The raw → story_level transformation is NOT reproducible
from repository data alone. This is a documented limitation, not a defect
introduced by the rebuild.

See: `validation/source_edition_metadata_required.md`

## 3. Story-Level → Final

633 story-level rows produced:
- 628 edge records in `kenarlar_temiz.csv`
- 85 event records in `olaylar_temiz.csv`
- 5 story-level rows NOT in final: DKR0122, DKR0167, DKR0252, DKR0345, DKR0708

The 5 missing rows were dropped during the cleaning/splitting process.
Their disposition is not documented in the repository. This is a provenance
gap requiring human clarification.

Story-level → final transformation also involved:
- Entity normalization (alias resolution via `dede_korkut_alias_sozlugu.csv`)
- Change tracking via `dede_korkut_degisim_logu.csv` and `_v3_only.csv`
- Column schema changes (21 columns → standardized naming)

## 4. Final → Processed (Canonical)

This transformation IS fully reproducible via `src/build_canonical.py`:

1. **Entity resolution**: single merge (begil_in_adamlari → begilin_adamlari),
   reducing 333 legacy nodes to 332 canonical nodes
2. **Column renaming**: Turkish → English column names
3. **Taxonomy mapping**: 17 raw relation types → 6 interpretive families
4. **Aggregation**: event-level → unordered-pair aggregation (376 pairs)
5. **Provenance attachment**: best-effort matching back to story-level rows

### Provenance Match Rates

| Status | Count | % |
|---|---|---|
| matched_unique | 571 | 90.9% |
| unmatched_provenance_gap | 53 | 8.4% |
| matched_ambiguous | 4 | 0.6% |

The 53 provenance gaps and 4 ambiguous matches are expected given the
non-trivial cleaning transformations between story-level and final.

## 5. Source Edition Provenance

**CLASSIFICATION: UNRESOLVED**

Missing information:
- Which printed edition of Dede Korkut was used
- Edition year and publisher
- Whether `satir_no` refers to a specific edition's numbering
- Relationship between XLSX and story-level files
- Whether pre-story-level raw coding notes exist

This information can only come from the original researcher/annotator.

## 6. Reproducibility Assessment

| Stage | Reproducible? |
|---|---|
| Raw → Story-Level | NO (source edition unknown, transformation undocumented) |
| Story-Level → Final | PARTIALLY (change logs exist but 5 row dispositions unclear) |
| Final → Processed | YES (deterministic script: src/build_canonical.py) |
| Processed → Analysis | YES (deterministic pipeline: run_pipeline.py) |

## 7. Summary

The canonical dataset (`data/processed/`) is fully reproducible from
`data/final/` via deterministic scripts. The upstream provenance (raw →
story-level → final) has documented gaps that require human researcher input.
This is honestly disclosed and does not affect the technical validity of the
computational pipeline, but it does affect the academic completeness of the
research package.
