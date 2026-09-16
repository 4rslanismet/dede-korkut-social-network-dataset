# Results

Every number below is sourced from a specific pipeline output, cited inline. Results are labeled
**[descriptive]**, **[exploratory]**, or **[confirmatory]** throughout, per this project's
exploratory/confirmatory discipline (section 44/110 of the governing project brief).

## 1. Corpus Structure [descriptive]

The full corpus network (G0) comprises 311 connected actors (of 332 canonical actors; the
remaining 21 appear only in non-relational narrative events) and 376 aggregated relations, with
density 0.0078 and 23 connected components, the largest containing 261 actors
(`outputs/statistics/corpus_network_metrics.csv`). Across the full, person-only, and core-social
specifications alike, Salur Kazan and Bamsı Beyrek exhibit the highest degree, betweenness, and
PageRank (e.g., under G0_full: Salur Kazan degree=72, strength=436, betweenness=0.388,
PageRank=0.092; `outputs/tables/centrality_G0_full.csv`). **We do not interpret this as evidence
that these are the "most important" characters in a literary sense** — only that they occupy the
most structurally central positions in this specific encoded relational network.

Under the directed specification (G9, 221 nodes, 324 edges), Salur Kazan's HITS hub score
(0.425) far exceeds its authority score (0.016), and out-degree (53) exceeds in-degree (30),
indicating this actor is coded predominantly as the initiator rather than recipient of directed
relations. Reciprocity in G9 is 0.358.

## 2. Community Structure [confirmatory, null-model validated]

Leiden community detection (resolution 1.0) on the core-social network (G2, 309 nodes, 374 edges)
identifies 33 communities at modularity 0.695; Louvain identifies 34 communities at modularity
0.711 (Adjusted Rand Index between the two partitions: 0.899). Across ten random seeds, the Leiden
partition is highly stable (mean modularity 0.698, SD 0.003; mean pairwise Adjusted Rand Index
0.908). **Because the core-social network contains 23 connected components, and modularity-
maximizing algorithms trivially assign each disconnected component its own community, a
substantial share of the raw community count of 33 reflects graph fragmentation rather than
socially meaningful clustering; only structure within the 261-node giant component is interpreted
as such** (`reports/06_advanced_network_analysis_report.md` §1.4).

Against a null model of 1,000 degree-preserving randomizations, Louvain modularity is
significantly higher than expectation by chance in 7 of 9 tested networks after Benjamini-Hochberg
correction (α=0.05): G0_full (q=0.012), G2_core_social (q=0.012), G1_person_only (q=0.022),
G6_conflict (q=0.027), G7_positive (q=0.032), G8_negative (q=0.036), G4_communication (q=0.036)
(`outputs/statistics/null_model_fdr_corrected.csv`). **This is the strongest confirmatory finding
in this study: the community structure detected in this corpus is not an artifact of the degree
sequence alone.**

## 3. Retraction of an Earlier Descriptive Finding [confirmatory, negative result]

All twelve network variants exhibit negative degree assortativity (range −0.11 to −0.33),
consistent with a hub-and-spoke structure. **However, after null-model testing and
Benjamini-Hochberg correction, degree assortativity is not statistically significant in any of the
nine networks tested** (smallest q-value: G0_full, q=0.089, above the α=0.05 threshold)
(`reports/07_null_models_report.md` §3.3). We therefore retract the earlier descriptive
characterization of this corpus's networks as "disassortative" as a validated structural claim;
the observed negative values most likely follow mechanically from the underlying degree
distribution rather than reflecting an additional structural preference against hub-hub
connections. **We report this retraction as a substantive methodological finding in its own
right**: a network statistic that appears meaningful on inspection can fail basic null-model
validation, and we recommend this check as standard practice for literary/narrative network
studies making descriptive claims of this kind.

Clustering coefficient, by contrast, is validated as significantly elevated above the null
expectation in four networks (G0_full, G1_person_only, G2_core_social, G4_communication;
q≤0.048), and transitivity in one (G1_person_only, q=0.027). The kinship network (G3) is
indistinguishable from its null model on all four tested metrics (p≥0.45) — a genuine null result
consistent with a sparse, tree-like kinship structure, reported rather than omitted.

## 4. Sensitivity to Network-Construction Choices [confirmatory]

Of six paired network-construction choices tested by rank correlation, two show negligible effect
on centrality rankings — prologue inclusion/exclusion and core-social filtering, both Spearman
ρ=1.000 on degree and betweenness — while **person-plus-group versus person-only actor inclusion
produces the largest disagreement** of any comparison tested (ρ=0.887-0.926 across degree,
betweenness, and PageRank; `outputs/tables/sensitivity_rank_stability.csv`). The choice of edge
weighting affects PageRank more than any other metric tested (ρ=0.849 between weighted and
unweighted variants), consistent with this dataset's edge-weight field having undocumented
semantics (`docs/limitations.md` item 7). We conclude that any centrality-based claim drawn from
this corpus should specify which actor-inclusion and weighting decisions were made, since these
are shown here to materially change which actors rank highest.

## 5. Structural Robustness [descriptive]

The full network (G0) requires random removal of approximately 25.1% of nodes to reduce the
largest connected component below 50% of its original size, but only 3.9% (degree-targeted) or
1.9% (betweenness-targeted) of nodes under adaptive targeted removal
(`outputs/statistics/robustness_summary_G0_full.json`). This robust-to-random/fragile-to-targeted
pattern is consistent with the hub-dominated degree distribution reported in §1, and describes
graph connectivity only — we make no claim about narrative resilience or any property of the
underlying story.

## 6. Multilayer and Signed Structure [exploratory]

Across seven observed relation layers (kinship, communication, conflict, authority, identity,
place, event), Salur Kazan is the only actor active in all seven, with a layer participation
coefficient of 0.766 — the corpus's most versatile actor by this measure. Signed-network structural
balance was not assessed: only 13 triangles among positively/negatively signed edges meet a
documented minimum-sample threshold of 15, below which we judged a balance statistic unreliable
for a corpus this sparse. Motif/triad enrichment on the directed network was likewise not
attempted: only 44 of 1,774,630 triads in the directed triadic census fall into a closed category,
an insufficient sample for per-category null comparison, and no directed degree-preserving null
model was available in the software version used.
