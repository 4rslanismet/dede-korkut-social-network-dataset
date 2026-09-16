# Proposed Thesis Structure

Intended for integration into a master's/graduate thesis. Chapter numbering is a suggestion, not
a requirement — adapt to the target program's conventions.

## Chapter 1 — Introduction

- The Book of Dede Korkut as a research corpus; motivation for a network-science reading.
- Research questions (→ `thesis/research_questions.md`).
- Roadmap of the thesis and a preview of the central methodological finding (the null-model
  retraction of the "disassortative network" claim — see `thesis/results_mapping.md`).

## Chapter 2 — Related Work

- Literary/narrative network analysis; multilayer literary networks; digital humanities network
  methodology; null-model validation practice in network science.
- **Not yet written** — see `reports/literature_search_plan.md` for the search queries a
  literature review chapter should be built from; no citations have been assembled in this
  pipeline session.

## Chapter 3 — Data and Provenance

- The legacy v1/v2/v3 coding history and this rebuild's canonical dataset
  (`data/processed/`).
- Repository audit findings: the +80-row story_level→final gap, the raw-Excel provenance
  mismatch, the unknown source edition — presented as a case study in data-provenance auditing for
  inherited humanities datasets, not just a limitations footnote.
- → Source material: `reports/01_repository_audit.md`, `reports/03_canonical_dataset_report.md`,
  `docs/data_dictionary.md`.

## Chapter 4 — Methodology

- Network construction (12 variants), descriptive metrics, community detection.
- Statistical validation: null models and multiple-testing correction.
- Sensitivity and robustness testing.
- → Source material: `docs/methodology.md`, `paper/methods.md` (can be reused near-verbatim).

## Chapter 5 — Results I: Descriptive and Confirmatory Network Structure

- Corpus structure, centrality, community detection (with the connected-component caveat as a
  worked example of a common network-science pitfall).
- Null-model validation results, including the assortativity retraction as a central result.
- → `thesis/results_mapping.md` RQ1, RQ3, RQ4.

## Chapter 6 — Results II: Sensitivity, Robustness, and What the Findings Depend On

- Which centrality/community conclusions are stable across modeling choices, and which are not.
- Structural robustness under random and targeted node removal.
- → `thesis/results_mapping.md` RQ5.

## Chapter 7 — Results III: Exploratory Structure (Multilayer, Signed, Narrative-Order)

- Explicitly framed as exploratory, not confirmatory — layer participation, signed profile,
  narrative-order windowing and dynamic centrality.
- Honest treatment of what could **not** be answered (RQ6, story-level clustering; the directed
  motif/triad analysis skip).
- → `thesis/results_mapping.md` RQ2, RQ6, RQ7.

## Chapter 8 — Discussion

- What this study demonstrates about the specific corpus, and, separately, what it demonstrates
  methodologically (the null-model-retraction result generalizes beyond this corpus).
- Explicit boundary: structural centrality vs. literary/critical importance.

## Chapter 9 — Limitations and Future Work

- → `docs/limitations.md` (17 items) as the primary source; future work should prioritize: a real
  second coder for inter-annotator reliability, resolving the 5 concatenated-multi-actor nodes,
  completing the story-similarity metric suite (RQ6), and obtaining the source edition metadata.

## Chapter 10 — Conclusion

## Appendices

- Appendix A: Full data dictionary (`docs/data_dictionary.md`).
- Appendix B: Relation codebook (`docs/relation_codebook.md`).
- Appendix C: Decision log (`docs/decision_log.md`, DEC-001 through DEC-013).
- Appendix D: Full supplementary tables and figures (`paper/supplementary_material.md`).
