# Limitations

This document consolidates every methodological and data limitation identified across this
project's phases. It is written to stand alone — each item states what the limitation is, how it
was discovered, and how it affects interpretation, with a pointer to the fuller discussion.

---

## 1. Source Edition Unknown (critical)

The repository does not record which printed edition, transcription, or translation of the Book
of Dede Korkut was read to produce the original coding. `data/raw/*.xlsx` — the only file
resembling "raw" source material — was found not to correspond to `data/story_level/`/`data/final/`
in either schema or row counts, so it cannot answer this question either. Any claim about "the
text of Dede Korkut" in downstream academic outputs must note the specific edition is
**unspecified in the current repository metadata**.
→ `validation/source_edition_metadata_required.md`, `reports/01_repository_audit.md` §4.

## 2. Single Coder — No Verified Inter-Annotator Reliability

All coding was done by one person. No Cohen's kappa or Krippendorff's alpha has been computed, and
none should be reported until a real second coder completes
`validation/inter_annotator_sample.csv` (70 stratified rows) per `docs/inter_annotator_protocol.md`.
`src/inter_annotator_stats.py` is built and verified to refuse producing a number from placeholder
data.
→ `reports/13_14_reproducibility_report.md` §1.

## 3. story_level → final Transformation Not Fully Reproducible

`data/story_level/` (633 rows) and `data/final/` (713 rows in edges+events) differ by +80 rows
across 11 of 14 stories, with no documented rule for the transformation (possible row-splitting
during v2/v3 standardization). This was not assumed away — 53 of 628 final relations (8.4%) could
not be matched back to a specific `data/story_level/` row at all (`unmatched_provenance_gap` in
`data/processed/provenance.csv`).
→ `reports/01_repository_audit.md` §3, `reports/03_canonical_dataset_report.md` §3.

## 4. Relation Taxonomy Coverage Gap

29.6% of all relations (186/628) are coded `belirsiz` (undetermined) — the single largest
`standard_relation` category. Any relation-family-based analysis inherits this coverage
limitation; results should be reported both with and without the UNCERTAIN family where relevant.
→ `docs/relation_codebook.md`.

## 5. Collective/Group Actor Effects

124 of 332 canonical actors are `grup`-type (plus 21 more of other non-`kişi` types). Phase 8
sensitivity analysis (with weighted betweenness computed as distance = 1/strength, DEC-017) confirms
this is not a negligible modeling choice: person+group vs. person-only (Spearman ρ=0.892-0.926, mean
0.911) and groups included vs. excluded (ρ=0.949-0.957, mean 0.952) change centrality rankings
noticeably. Edge weighting is numerically tied with person+group vs. person-only (mean ρ 0.912; PageRank
ρ=0.849, betweenness ρ=0.886), so no single construction choice is identified as the most influential.
→ `reports/08_sensitivity_robustness_report.md` §2.4.

## 6. Inferred-Relation Effects (small but measured)

32/628 relations (5.1%) used a non-explicit extraction method (`çıkarımsal_akrabalık`,
`manuel_turkistan_ekleme`, `epitet_aktarım`). Excluding them changes centrality rankings only
slightly (ρ≥0.98 across degree/betweenness/PageRank) — measured, not assumed.
→ `reports/08_sensitivity_robustness_report.md` §2.2.

## 7. Edge Weight (`agirlik`) Semantics Undocumented

The 1-5 integer weight scale's exact meaning is not documented in the source repository. It
behaves like an ordinal intensity/importance coding, not a repeat-interaction count (which is
tracked separately via `interaction_count`). This matters in practice: PageRank (ρ=0.849) and
weighted betweenness (ρ=0.886) were the metrics most sensitive to the weighted-vs-unweighted modeling
choice in Phase 8. Because `weight` is treated as tie *strength*, shortest-path metrics use the
derived distance 1/strength (DEC-017); a different reading of the 1-5 scale would change them.
→ `docs/relation_codebook.md`, `reports/08_sensitivity_robustness_report.md` §2.3.

## 8. Narrative Order ≠ Historical Time

`narrative_order` (from `satir_no`) is a within-story sequence indicator only. It is never used as
a chronological or historical timeline anywhere in this project, per an explicit naming/framing
rule enforced throughout. `first_story` in `nodes.csv` similarly reflects **corpus presentation
order** (file order 01-14), not narrative or historical chronology.
→ `docs/methodology.md` §5, `reports/06_advanced_network_analysis_report.md` §5.

## 9. Network Projection Artifacts

The actor×story bipartite projection (actor-actor co-occurrence) inflates apparent connectivity
for actors with a high `story_count`, independent of any direct narrative interaction. It is used
descriptively only, never as an edge-weighted network for centrality claims.
→ `docs/network_models.md`.

## 10. Entity Resolution Uncertainty

Only one node merge was applied automatically (high confidence: identical name, identical type).
Seventeen lower-confidence alias conflicts (same raw text standardized to two different targets in
different contexts) remain open in `validation/HUMAN_REVIEW_QUEUE.csv`, as do 45 "stale alias
target" cases where the alias dictionary points to a name that no longer exists in the current
node table (a multi-hop v1→v2→v3 standardization chain the alias table doesn't fully capture).
→ `reports/02_data_quality_report.md` §4, `docs/decision_log.md` DEC-002.

## 11. Candidate Composite Actor Nodes (found late, Phase 15; scan extended in DEC-018)

Some canonical actor labels may denote several actors collapsed into one node (e.g. a single node
named "Beyrek, Yigenek, Kazan, Kara Budak, Deli Dündar, Uruz"). The first discovery (DEC-013) found five
such comma-joined nodes while generating character pages; a reproducible scan (`src/composite_nodes.py`)
now flags **46 of 332 canonical nodes as candidate composite nodes requiring manual review** (comma
lists, "X ve Y" constructions and sentence-like names). They touch 46 of 628 relations (7.3%) and 48 of
1,256 relation endpoints (3.8%). A candidate is not necessarily an error — many are legitimate
collective labels — and none has been split or merged, so every node-level statistic counts each such
label as one actor. This passed every structural validation check (it violates neither uniqueness nor
referential integrity). The scan is a heuristic and is under-inclusive by design: it does not flag "ile"
constructions, hyphen-joined names or phrases shorter than six words. For example "Egreke Yol Gösterdi"
(a possible sentence fragment) and "Kayın Ata - Kayın Anası" (possibly two kin terms in one node) are
canonical nodes it does not flag and that are not in the review queue, so the set of nodes worth
reviewing is larger than the flagged 46. Neither the scan nor this note splits, merges or recodes any
node. Resolving them requires manual entity review of the node list against the original text; this
remains a publication blocker.
→ `docs/decision_log.md` DEC-013 and DEC-018, `validation/composite_node_candidates.csv`,
`validation/HUMAN_REVIEW_QUEUE.csv` (HR0076-HR0080 hand-recorded; further items category
`composite_node_candidate`).

## 12. Retracted Finding: Degree Assortativity

Phase 5's descriptive observation that all network variants show negative degree assortativity
("disassortative," hub-and-spoke structure) was tested against a null model in Phase 7 and found
**not statistically significant** in any of the 9 networks tested, after Benjamini-Hochberg FDR
correction. This claim is retracted; negative values likely arise mechanically from the degree
distribution itself.
→ `reports/07_null_models_report.md` §3.3.

## 13. Community Count Partly a Connected-Component Artifact

`G2_core_social` has 23 connected components. Modularity-maximizing algorithms assign each
disconnected component its own community by construction, inflating the raw community count (33)
with trivial single/few-node partitions unrelated to social clustering. The overall
higher-than-random modularity signal *is* statistically validated (Phase 7), but the specific
count of 33 should never be quoted without this caveat. Only structure within the 261-node giant
component should be interpreted substantively.
→ `reports/06_advanced_network_analysis_report.md` §1.4.

## 14. Motif/Triad Analysis Not Attempted

G9_directed's triadic census is overwhelmingly dominated by disconnected triples (>99.99%); only
44 closed triads exist across all 7 non-trivial categories. No directed degree-preserving null
model was available in the networkx version used, and 44 samples across 7 categories would not
support a meaningful per-category enrichment test. Skipped, not forced.
→ `docs/decision_log.md` DEC-010.

## 15. Story Similarity — Built Post-Project, RQ6 Only Partially Answered (Update)

*Originally, only the raw actor×story bipartite shared-actor projection had been computed and
this item flagged RQ6 as unanswerable.* The full similarity metric suite (actor Jaccard, weighted
Jaccard, cosine similarity, relation-profile similarity, layer-composition similarity,
hierarchical clustering) was subsequently built (`src/story_similarity.py`, `docs/decision_log.md`
DEC-014). A final audit (DEC-015) narrowed what it supports:

- Actor overlap between stories is low (Jaccard median 0.030, max 0.153; 28 of 91 pairs share no
  actor). "Most similar pair" means relatively most overlapping among the evaluated stories, not
  strongly similar; the top pair differs by metric.
- Cosine similarities on the relation/layer profiles are high by construction (a permutation
  baseline reaches the same range at the top of the distribution).
- A Ward dendrogram always exists and is not evidence of clusters. Cluster-validity checks
  (silhouette, cophenetic correlation, linkage agreement, bootstrap, permutation baseline;
  `outputs/statistics/story_similarity_cluster_validity.json`) do not support a robust discrete
  clustering. Story-level similarity can be quantified and visualized, but evidence for a robust
  discrete clustering structure is limited.
- Narrative themes such as captivity are not coded variables in the canonical dataset; thematic
  readings of similar stories are qualitative interpretation, not network-analysis results.
- No significance test was applied to the similarity values themselves.

RQ6 status: **PARTIALLY ANSWERED / EXPLORATORY.**
→ `thesis/research_questions.md` RQ6, `outputs/statistics/story_similarity_clustering.json`,
`outputs/statistics/story_similarity_cluster_validity.json`.

## 16. Website Scope

The Network Explorer offers 3 of the 12 network variants (G0, G1, G2). Figures F01, F04-F05,
F08-F14 (of the F01-F18 target list) were not produced. TR/EN bilingual infrastructure was not
built (English only). Mobile responsiveness and keyboard accessibility were not systematically
tested beyond the CSS's built-in responsive rules. The site has been tested locally
(`python -m http.server`) but not yet deployed to a live GitHub Pages URL.

## 17. Interpretation Limits (general)

Every centrality, community, and versatility finding in this project describes **structural
position in an encoded relational dataset**, not literary importance, narrative centrality in a
critical sense, or historical fact about the Oghuz Turkic oral tradition. This distinction is
stated in a disclaimer on every relevant page of the website and should be preserved in any
academic use of this dataset.

## 18. Licensing: Dataset Licence Set, Source-Code Licence Unresolved

The dataset is licensed CC BY 4.0 (`LICENSE`). No separate licence has been chosen for the **source
code** (`src/`, `tests/`, `run_pipeline.py`); Creative Commons licences are not generally recommended
for software, so this is an open decision for the repository owner. Nothing in this repository selects
or implies a code licence on the owner's behalf.

## 19. Manuscript Package Is Not a Finished Paper

The `paper/` directory is a manuscript/research package: an outline, methods, results and supplementary
material. The Introduction, Discussion and References are not written and no literature review has been
performed (only a search plan, `reports/literature_search_plan.md`). Publication additionally depends on
the open external/manual items in `reports/RELEASE_CHECKLIST.md` (source-edition metadata, a second
annotator, manual entity review, `CITATION.cff` owner metadata, the code-licence decision).
