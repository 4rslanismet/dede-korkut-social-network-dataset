# Manuscript Outline

**Working title:** *Structure, Not Sentiment: A Reproducible Multilayer Network Analysis of the
Book of Dede Korkut, With Null-Model Validation of Its Own Descriptive Claims*

*(Alternative, simpler title if the above reads as too pointed for the target venue: "Mapping
Narrative Structure in the Book of Dede Korkut: A Reproducible Multilayer Network Analysis" —
the master prompt's own suggested title, section 92. The working title above was chosen instead
because this project's single most citable methodological contribution is the null-model
retraction in §7 below, and a title that foregrounds it is more accurate to what the paper
actually demonstrates.)*

Structure follows section 93 of the project brief.

---

## 1. Introduction

- Motivate literary network analysis as a digital-humanities method; situate the Book of Dede
  Korkut as a corpus with rich, already-hand-coded relational structure (14 narrative units, one
  coder, three prior standardization rounds — v1/v2/v3).
- State the paper's actual contribution precisely: not a new literary claim about the epic, but
  (a) a reproducible pipeline that rebuilds a canonical dataset from an existing hand-coded corpus
  with full provenance tracking, and (b) a demonstration that a plausible-looking descriptive
  network finding (negative degree assortativity) does not survive null-model validation —
  a methodological cautionary result relevant beyond this corpus.
- State up front, in the introduction, the discipline this paper follows throughout: centrality is
  never presented as literary importance (see `docs/limitations.md` item 17).

## 2. Related Work

*(Not researched in this Colab/local session per the project brief's own scope limit — section
97. This section should cite:)*
- Literary/narrative social network analysis (general).
- Multilayer literary networks.
- Digital humanities network analysis methodology papers.
- Null-model/statistical validation practice in network science (relevant given §7's finding).
- See `reports/literature_search_plan.md` *(not yet created — see Task list)* for suggested search
  queries.

## 3. Materials and Data

- Corpus: 14 narrative units (13 boy + 1 girizgah), legacy v3 coding (`data/final/`), rebuilt into
  a canonical dataset (`data/processed/`) with 332 actors, 628 event-level relations, 85
  non-relational narrative events.
- **State the source-edition gap explicitly and early**: the specific print edition read during
  original coding is not recorded in the repository (`docs/limitations.md` item 1). This paper
  cannot claim to represent "the" authoritative text of Dede Korkut, only this specific coded
  dataset.
- Single coder; no verified inter-annotator reliability statistic exists yet (item 2). State this
  as a limitation of the underlying data, not something this paper's analysis can correct.
- Describe the +80-row undocumented story_level→final transformation gap (item 3) as an inherited,
  disclosed data-provenance limitation.

## 4. Methods

Summarize `docs/methodology.md` at paper length:
- Twelve network model variants (G0-G11), one filter rule each (`src/networks.py`).
- Centrality measures used, with the disconnected-graph caveat (harmonic centrality preferred over
  closeness).
- Community detection: Leiden + Louvain, seeded, with the 23-connected-component caveat stated as
  part of the method, not buried in results.
- Null model method: degree-preserving randomization (`double_edge_swap`), 1000-member ensemble,
  Benjamini-Hochberg FDR correction across 36 tests (9 networks × 4 metrics).
- Sensitivity method: 6 paired network-construction choices, rank-correlation comparison.
- Robustness method: random/degree/betweenness-targeted node removal.

## 5. Results

Pull directly from `reports/04_05_network_construction_and_descriptive_report.md`,
`reports/06_advanced_network_analysis_report.md`, `reports/07_null_models_report.md`,
`reports/08_sensitivity_robustness_report.md`. Structure results into clearly labeled
subsections, each explicitly tagged **descriptive**, **exploratory**, or **confirmatory**
(section 44/110):

### 5.1 Descriptive corpus structure
Density, clustering, degree distribution, hub structure (Salur Kazan and Bamsı Beyrek dominate
degree/betweenness/PageRank across G0/G1/G2/G9 — framed exactly as in `reports/04_05...`, never as
"most important character").

### 5.2 Confirmatory: null-model validation (the paper's central methodological result)
Community modularity is significantly higher than a degree-preserving null model in 7/9 tested
networks (Benjamini-Hochberg FDR, α=0.05) — real structural signal, not a degree-sequence artifact.
**Degree assortativity is not significant in any of the 9 networks tested** — the earlier
descriptive "disassortative network" observation is retracted. Report full statistics: observed
value, z-score, empirical p, BH q-value for every one of the 36 tests (Table T09).

### 5.3 Confirmatory: sensitivity to network-construction choices
Person+group vs. person-only produces the largest rank disagreement (Spearman ρ=0.887-0.926) of
six tested modeling choices; girizgah inclusion/exclusion and core-social filtering have
negligible effect (ρ=1.000). Report as an explicit ranking of "how much does this decision matter"
(Table T10), not as validation/invalidation of any specific centrality finding.

### 5.4 Exploratory: multilayer, signed, and directed structure
Layer participation, signed degree profile, directed hub/authority asymmetry (Salur Kazan's HITS
hub score far exceeds its authority score) — labeled exploratory throughout, no null-model
validation was performed for these (motif/triad analysis was explicitly skipped, DEC-010).

### 5.5 Structural robustness
Classic robust-random/fragile-targeted pattern (Table T11) — framed strictly as graph
connectivity, never as "narrative resilience" (master prompt's own naming rule, section 31).

## 6. Discussion

- The null-model retraction (§5.2) as the paper's main methodological point: a network that
  "looks" structurally interesting under simple descriptive statistics can fail basic statistical
  validation, and researchers working with literary/narrative networks should treat descriptive
  findings (especially assortativity-type measures) as provisional until tested.
- The person-only sensitivity result (§5.3) as a caution for any literary-network study that
  silently excludes collective/group actors without testing the effect of that choice.
- Discuss the hub structure (Salur Kazan, Bamsı Beyrek) in terms of what it can and cannot support:
  it is consistent with these being recurring, well-connected figures across the corpus as coded;
  it is not, by itself, evidence about the epic's literary or cultural valuation of these figures.

## 7. Limitations

Reference `docs/limitations.md` in full; do not re-litigate items already stated there, but ensure
the paper's own text does not silently overstate anything the limitations document already
qualifies (source edition, single coder, provenance gap, taxonomy coverage, group-actor effects,
weight semantics, community-count artifact, the 5 concatenated-node data-quality issue, motif
analysis skip, incomplete story similarity).

## 8. Conclusion

Restate the two contributions (reproducible pipeline + null-model retraction finding) without
overclaiming literary insight.

## 9. Data and Code Availability

Repository URL, branch (`claude-dk-rebuild`), license (CC BY 4.0), and the reproduction command
(`python run_pipeline.py --all`). Point to the website (`docs/`) as the interactive companion to
the paper.

---

## Outstanding Tasks for Whoever Finalizes This Manuscript

- [ ] Write `reports/literature_search_plan.md` (section 97) and integrate real citations into §2.
- [ ] Decide on final title (working title above vs. the master-prompt-suggested alternative).
- [ ] Fill in `CITATION.cff` author metadata (currently TODO) before submission.
- [ ] Confirm target venue and adjust length/register accordingly — this outline assumes a
      full research paper, not a short paper or poster abstract.
