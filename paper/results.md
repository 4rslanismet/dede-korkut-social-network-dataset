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
(`outputs/statistics/null_model_fdr_corrected.csv`; z = 2.6–7.0, all positive; G3_kinship and
G5_cooperation_support not significant). As a robustness check on the component-fragmentation
caveat above, the same null (1,000 degree-preserving randomizations) applied to the 261-node giant
component of G0_full alone gives observed Louvain modularity 0.692 against a null mean of 0.615
(z = 9.9, p = 0.001; `outputs/statistics/audit_top5_checks.json`). **This is the strongest
confirmatory finding in this study: the community structure detected in this corpus is not an
artifact of the degree sequence alone.** It establishes non-random modular organization; it does not
establish that the communities are socially meaningful units (labels are numeric only, alignment
with story boundaries was not tested, and the null ensemble used Louvain rather than Leiden).

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
q≤0.048), and transitivity in one (G1_person_only, q=0.027). The kinship network (G3) shows no
detectable deviation from its null model on any of the four tested metrics (q≥0.67; p≥0.45),
reported rather than omitted. This is a low-information null: G3 is a forest (83 nodes, 61 edges,
22 components, no triangles), so its clustering and transitivity are structurally zero and only the
assortativity and modularity tests are informative (`outputs/statistics/audit_top5_checks.json`).
It is consistent with a sparse, acyclic kinship coding and is not evidence about the literary
importance of kinship.

## 4. Sensitivity to Network-Construction Choices [descriptive sensitivity analysis]

Of six paired network-construction choices tested by rank correlation, three show negligible effect
on centrality rankings — prologue inclusion/exclusion, core-social filtering and (nearly)
explicit-only versus explicit-plus-inferred relations (Spearman ρ ≥ 0.97 on all three centralities).
Actor-type inclusion and edge weighting change rankings noticeably: person-plus-group versus
person-only (ρ=0.887-0.926 across degree, betweenness and PageRank), groups included versus excluded
(ρ=0.896-0.957) and weighted versus unweighted (ρ=0.849 for PageRank, 0.930 for betweenness; degree
identical by construction; `outputs/tables/sensitivity_rank_stability.csv`). Person-plus-group versus
person-only has the lowest mean ρ (0.91), but weighting has the lowest PageRank ρ, the three means
lie within 0.03 of one another, the comparisons use different node sets (n=154 to 311), and the
differences between correlations were not tested, so we do not rank these three choices. All
correlations remain ≥ 0.85. The weighting effect on PageRank is consistent with this dataset's
edge-weight field having undocumented semantics (`docs/limitations.md` item 7). We conclude that any
centrality-based claim drawn from this corpus should specify which actor-inclusion and weighting
decisions were made, since these measurably change which actors rank highest.

## 5. Structural Robustness [descriptive]

The full network (G0, 311 nodes) requires random removal of approximately 25.1% of nodes (78 nodes;
mean of 100 trials) to reduce the largest connected component below 50% of the original node count,
but only 3.9% (12 nodes, degree-targeted) or 1.9% (6 nodes, betweenness-targeted) under targeted
removal (`outputs/statistics/robustness_summary_G0_full.json`). The reference is the original 311
nodes, not the 261-node initial giant component; targeted crossings are resolved only to one 6-node
removal step; degree ranking is recomputed after every removal, betweenness ranking every 15
removals; and only G0 was tested. This robust-to-random/fragile-to-targeted pattern is consistent
with the hub-dominated degree distribution reported in §1, and describes graph connectivity only —
we make no claim about narrative resilience or any property of the underlying story.

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

## 7. Story Similarity [descriptive / exploratory — RQ6 partially answered]

*(Added after initial completion of this study, when the story-similarity metric suite originally
scoped for this project — actor Jaccard, weighted Jaccard, cosine similarity, relation-profile
similarity, layer-composition similarity, and hierarchical clustering — was built; see
`docs/decision_log.md` DEC-014, and DEC-015 for the audit that narrowed the claims below.)*

**Actor overlap between stories is low.** Across all 91 story pairs the actor-set Jaccard index has
a median of 0.030 and a maximum of 0.153; 28 of 91 pairs share no actor at all. The pair with the
highest overlap, S03 ("Salur Kazan'ın Evinin Yağmalandığı") and S05 ("Kazan Bey Oğlu Uruz Bey'in
Tutsak Olduğu Boy"), is the relatively most overlapping pair among the evaluated stories (Jaccard =
0.153, weighted Jaccard = 0.222; 11 shared actors, including Salur Kazan and Uruz). It is the top
pair on the two Jaccard-type measures only: on actor cosine (0.676), relation-profile cosine (0.941)
and layer-composition cosine (0.965) it ranks 6th, 6th and 7th of 91, and each of those three
measures has a different top pair (S12–S14, S11–S13 and S11–S13 respectively). S08–S10 (Jaccard =
0.133) is the next most overlapping pair. Because even the maximum overlap is low, these results
identify the *relatively* most overlapping pairs; they do not show that any two stories are highly
similar.

**Cosine values are high by construction.** Relation-profile and layer-composition cosine
similarities are computed on non-negative counts over a few categories dominated by conflict and
uncertain relations, so values in the 0.9 range arise readily. Under a permutation baseline
(relations reassigned across stories, story sizes preserved; 1,000 permutations) the largest
pairwise relation-profile cosine reaches 0.987 at the 95th percentile, close to the observed
maximum of 0.985. The top relation-profile and layer-composition similarities are therefore not
distinguishable from what chance reassignment produces at the top of the distribution and should not
be read as evidence of specific affinity between stories.

**Evidence for discrete clusters is limited.** Ward hierarchical clustering on each story's
relation-family and layer proportions always yields a dendrogram; its existence is not evidence of
clusters. A validity audit (`outputs/statistics/story_similarity_cluster_validity.json`, DEC-015)
found: silhouette widths of 0.37–0.56 for k = 2–6, in the weak-to-moderate range; the k = 2 split
isolates a single story (S01, one coded relation) and its silhouette is below the permutation
baseline; without S01 the best silhouette is 0.487 at k = 2, with a bootstrap adjusted Rand index
of 0.746 that falls to about 0.54–0.55 for k ≥ 4 (below the pre-set 0.75 support threshold at every k); different linkage methods disagree at k = 4 and k = 5;
and Ward's cophenetic correlation is 0.73. Silhouette values exceed the permutation baseline for
k ≥ 3 (all 14 stories) and for every k tested (without S01), which shows that stories differ in
relational profile more than sampling noise would produce, but is equally consistent with a
continuum of differences as with discrete groups. Story-level similarity can therefore be quantified
and visualized, but evidence for a robust discrete clustering structure is limited; no cluster
solution is offered as a finding. Narrative interpretation of any similar pair (for example a shared
theme) is qualitative and is not a result of the network analysis: thematic content such as captivity
is not a coded variable in the canonical dataset (no structured theme field exists, and the free-text
relation phrases of S03 contain none of the terms esir/esaret/tutsak/kurtar/yağma, while S05's
contain them in 2 of 40 rows). This section is descriptive and exploratory; no
significance test was applied to the similarity values themselves.
