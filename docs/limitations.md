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

125 of 332 canonical actors are `grup`-type (plus 21 more of other non-`kişi` types). Phase 8
sensitivity analysis confirms this is not a negligible modeling choice: person+group vs.
person-only produced the largest rank disagreement (Spearman ρ=0.887-0.926) of the six
sensitivity comparisons tested — the single most consequential network-construction decision in
this project.
→ `reports/08_sensitivity_robustness_report.md` §2.4.

## 6. Inferred-Relation Effects (small but measured)

32/628 relations (5.1%) used a non-explicit extraction method (`çıkarımsal_akrabalık`,
`manuel_turkistan_ekleme`, `epitet_aktarım`). Excluding them changes centrality rankings only
slightly (ρ≥0.97 across degree/betweenness/PageRank) — measured, not assumed.
→ `reports/08_sensitivity_robustness_report.md` §2.2.

## 7. Edge Weight (`agirlik`) Semantics Undocumented

The 1-5 integer weight scale's exact meaning is not documented in the source repository. It
behaves like an ordinal intensity/importance coding, not a repeat-interaction count (which is
tracked separately via `interaction_count`). This matters in practice: PageRank was the metric
most sensitive to the weighted-vs-unweighted modeling choice in Phase 8 (ρ=0.849, the lowest of
all sensitivity comparisons).
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

## 11. Concatenated Multi-Actor Nodes (found late, Phase 15)

Five nodes have a `canonical_name` that is a comma-joined list of multiple distinct named
characters/groups collapsed into one node (e.g. a single node named "Beyrek, Yigenek, Kazan, Kara
Budak, Deli Dündar, Uruz"). This passed every Phase 2 structural validation check (it doesn't
violate uniqueness or referential integrity) and was only noticed while generating character
pages for the website. Not fixed — would require re-deriving relations from the original text.
All five have very low `relation_count` (0-1), so the likely impact on network-level findings is
small but **not verified**.
→ `docs/decision_log.md` DEC-013, `validation/HUMAN_REVIEW_QUEUE.csv` (HR0076-HR0080).

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

## 15. Story Similarity Incomplete

Only the raw actor×story bipartite shared-actor projection has been computed. The full similarity
metric suite (actor Jaccard, weighted Jaccard, cosine similarity, relation-profile similarity,
layer-composition similarity, hierarchical clustering) described in the original project brief has
not yet been built. The website's Similarity page and table T08 are explicitly marked partial.

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
