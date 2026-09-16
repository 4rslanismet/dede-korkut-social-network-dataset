# Dataset Card — Dede Korkut Narrative Network Dataset

## Motivation

This dataset encodes the actors, relations, and narrative events of the Book of Dede Korkut (14
narrative units: 13 boy + 1 girizgah prologue) for computational digital-humanities and network-
science research. It was created to support reproducible social/complex/multilayer network
analysis of a canonical Turkic epic corpus, rather than one-off, non-reproducible close-reading
notes.

## Composition

- **332 canonical actors** (`data/processed/nodes.csv`): 187 person (`kişi`), 125 group (`grup`),
  and 20 of other types (mythological/divine, animal, object/nature, place/geography).
- **628 event-level relations** (`data/processed/relations_event_level.csv`), aggregated into 376
  unique unordered actor pairs (`relations_aggregated.csv`).
- **85 narrative events** (non-relational; `data/final/dede_korkut_olaylar_temiz.csv`).
- **525 alias entries** documenting the standardization history from raw text forms to canonical
  names.
- 17 relation types, mapped to 6 interpretive families (`data/processed/relation_taxonomy.csv`,
  `docs/relation_codebook.md`).

Instances represent: an actor (node), a coded relation between two actors at a specific point in a
specific story (event-level edge), an aggregated actor-pair summary, or a narrative event without
a clear second party.

## Collection Process

The underlying coding (which actors, relations, and events appear, and how they are labeled) was
performed by the original repository author across three iterative rounds (v1→v2→v3, documented
in `docs/README_v2.md` and `docs/README_v3.md`), reading the Book of Dede Korkut and recording
observations line-by-line (`satir_no`/`narrative_order`). **The specific print edition read is not
recorded** (see `docs/limitations.md` §1) — this is disclosed as an open gap, not filled by
inference.

This rebuild (this repository's `claude-dk-rebuild` branch) does not re-collect or re-code any
narrative content. It audits, validates, restructures, analyzes, and publishes the existing v3
coding as a canonical dataset (`data/processed/`), preserving `data/raw/` and `data/final/`
unchanged.

## Preprocessing/Cleaning/Labeling

See `docs/methodology.md` for the full pipeline. Key steps: repository audit and README-claim
verification (Phase 1); structural validation (node/edge/event/alias integrity checks, Phase 2);
canonical schema construction with one high-confidence entity merge and an interpretive relation
taxonomy mapping (Phase 3); provenance linkage back to `data/story_level/` with explicit
match/no-match status per relation (no silent assumptions).

## Intended Uses

- Social network analysis and complex network research on a literary/narrative corpus.
- Digital humanities studies of Turkic epic narrative structure.
- Methodological research on constructing and validating literary networks from manually coded
  data (this dataset's provenance and validation trail is itself a usable case study).

## Limitations

See `docs/limitations.md` for the full, itemized list (17 items) — most importantly: unknown
source edition, single coder (no verified inter-annotator agreement), an undocumented
story_level→final row-count gap, 29.6% "belirsiz" (undetermined) relation coding, unresolved
entity-resolution ambiguity, and 5 discovered-but-unfixed concatenated-multi-actor nodes.

## Ethical Considerations

This dataset encodes structural relationships in a public-domain epic narrative tradition; it does
not involve human subjects, personal data, or any living individuals. No literary text is
redistributed in this repository — only structured coding annotations and short evidentiary quotes
(`raw_evidence` field) are stored (see `docs/methodology.md` and the project's copyright rule:
`data/raw/` is never supplemented with externally-sourced literary text).

## License

CC BY 4.0 (see `LICENSE`).

## Citation

See `CITATION.cff`. If author/publication metadata is incomplete there, that reflects genuinely
unavailable information at the time of this rebuild — it is marked `TODO`, not invented.
