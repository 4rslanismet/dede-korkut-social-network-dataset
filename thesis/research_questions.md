# Research Questions

The seven research questions below are from the governing project brief (`docs/MASTER_PROMPT.md`
section 43). Each is assessed here for whether this rebuild's data and analysis can actually
answer it — per that brief's own instruction ("Eğer veri bir soruyu cevaplamaya yetmiyorsa bunu
çıkar" / "if the data cannot answer a question, remove it").

## RQ1 — How is the actor network in the Dede Korkut narratives structurally organized?

**Answerable: yes, fully.** Addressed by descriptive corpus-level metrics (density, degree
distribution, hub structure) and by null-model-validated community structure.
→ `reports/04_05_network_construction_and_descriptive_report.md`, `reports/06_advanced_network_analysis_report.md` §1, `reports/07_null_models_report.md` §3.1.

## RQ2 — Which actors serve as bridges between narratives and relation layers?

**Answerable: partially.** Cross-*layer* bridging is addressed (layer participation coefficient,
Salur Kazan active in all 7 layers) and cross-*community* bridging within one partition is
addressed (participation coefficient identifies Aruz as the strongest candidate bridge). Cross-
*narrative* (cross-story) bridging is only addressed via the actor-story bipartite projection,
which carries an explicit, disclosed degree-inflation caveat and was not used for a rigorous
"bridge" claim.
→ `reports/06_advanced_network_analysis_report.md` §1.5 (community bridges), §4 (multilayer);
`docs/network_models.md` (bipartite caveat).

## RQ3 — Do kinship, communication, cooperation, and conflict networks assign different structural roles to characters?

**Answerable: yes.** G3 (kinship), G4 (communication), G5 (cooperation/support), and G6 (conflict)
were each constructed and independently analyzed, including null-model testing. Notably, the
kinship network (G3) showed no detectable deviation from a degree-preserving random network on any
tested metric (clustering, transitivity, assortativity, modularity) — a negative result, reported
rather than hidden, but a low-information one: G3 is a forest (83 nodes, 61 edges, 22 components),
so clustering and transitivity are structurally zero.
→ `reports/07_null_models_report.md` §3.4 (G3_kinship null result), `docs/network_models.md`.

## RQ4 — Does the corpus network differ significantly from null networks with similar degree structure?

**Answerable: yes — this rebuild's central confirmatory finding.** Modularity is significantly
higher than a degree-preserving null model in 7/9 tested networks after FDR correction; clustering
is significant in 4/9; degree assortativity is significant in **none** (a retraction of an earlier
descriptive claim).
→ `reports/07_null_models_report.md` (entire report is the answer to this RQ).

## RQ5 — How stable are the main network findings against different network-construction choices?

**Answerable: yes (descriptive sensitivity analysis).** Six paired construction choices tested by
rank correlation (weighted betweenness uses distance = 1/strength, DEC-017); actor-type inclusion
(person+group vs. person-only), edge weighting and, more weakly, groups included vs. excluded change
centrality rankings noticeably (at least one ρ < 0.95; ρ 0.85-0.96), while girizgah, core-social
filtering and relation-inference policy are negligible (ρ ≥ 0.98). Person+group vs. person-only and
weighted vs. unweighted are numerically tied (mean ρ 0.911 vs. 0.912) and are not ranked against each
other (differences untested).
→ `reports/08_sensitivity_robustness_report.md` §2.

## RQ6 — What clusterings do the Dede Korkut boy show in terms of character composition and relation profiles?

**Status: PARTIALLY ANSWERED / EXPLORATORY (DEC-014, narrowed by the DEC-015 audit).** The full
similarity metric suite (actor Jaccard, weighted Jaccard, actor cosine, relation-profile
similarity, layer-composition similarity, hierarchical clustering — section 17) is built in
`src/story_similarity.py`, so story-level similarity *can be quantified and visualized*. The
"clusterings" part of the question is **not** established: evidence for a robust discrete
clustering structure is limited.

**Pairwise similarity (answered descriptively):** actor overlap between stories is low (Jaccard
median 0.030, maximum 0.153; 28 of 91 pairs share no actor). S03 ("Salur Kazan'ın Evinin
Yağmalandığı") and S05 ("Kazan Bey Oğlu Uruz Bey'in Tutsak Olduğu Boy") are the *relatively most
overlapping* pair among the evaluated stories (Jaccard = 0.153, 11 shared actors including Salur
Kazan and Uruz), followed by S08–S10 (0.133). They are the top pair on the two Jaccard measures
only (rank 6–7 of 91 on actor cosine, relation-profile and layer-composition cosine, each of which
has a different top pair). Relation-profile and layer-composition cosines are high by construction
(counts over few categories); the maximum observed value (0.985) is close to what a permutation
baseline produces (95th percentile of the pair maximum: 0.987), so they are not read as evidence of
specific affinity. A shared narrative theme (e.g. captivity) is **not** a coded variable in the
canonical dataset (no structured theme field; the free-text relation phrases of S03 contain none of
esir/esaret/tutsak/kurtar/yağma, S05's contain them in 2 of 40 rows) and is therefore not a finding
of this analysis; any thematic reading of a similar
pair is qualitative interpretation for the literary analysis chapters, not a network-analysis result.

**Discrete clustering (not robustly supported):** Ward linkage always returns a dendrogram; that is
not evidence of clusters. Validity checks on the 14 stories (`story_similarity_cluster_validity.json`):
silhouette 0.37–0.56 (k=2–6; the k=2 split only isolates S01, a 1-relation story, and scores below
its permutation baseline), bootstrap ARI 0.746 without S01 at k=2 falling to ~0.54 at k≥4, linkage
methods disagree at k=4–5, Ward cophenetic correlation 0.73. No k passes the pre-set support rule
(silhouette > 0.50, bootstrap ARI ≥ 0.75, permutation p < 0.05). Stories do differ in relational
profile more than sampling noise alone would produce (silhouette exceeds the permutation baseline
for k ≥ 3), which is consistent with a continuum as much as with discrete groups. The leaf order
`[S01, S04, S02, S06, S14, S03, S05, S11, S13, S07, S08, S09, S10, S12]` is a visualization order, not
a cluster assignment.

→ `outputs/matrices/story_similarity_*.csv` (5 matrices), `outputs/statistics/story_similarity_clustering.json`,
`outputs/statistics/story_similarity_cluster_validity.json`,
`outputs/tables/publication/T08_story_similarity.csv` (full 91-pair table), Figures F10-F11,
`docs/decision_log.md` DEC-014 and DEC-015.

## RQ7 — How does character centrality and relational intensity change over the course of the narrative?

**Answerable: partially, exploratory only.** Narrative-order windowing (early/middle/late
tertiles) and a corpus-order dynamic-centrality trajectory for the top 6 actors were computed for
13/14 stories (girizgah excluded, insufficient data). This is explicitly **descriptive/exploratory**
— no statistical trend test was applied, and the corpus-order trajectory tracks *presentation
order*, never historical or narrative chronology across stories (an explicit naming/framing rule
enforced throughout this project). A rigorous confirmatory answer to this RQ (e.g., a formal trend
test) has not been attempted.
→ `reports/06_advanced_network_analysis_report.md` §5-6.

---

## Summary Table

| RQ | Status | Confidence |
|---|---|---|
| RQ1 (structure) | Fully answered | Confirmatory (null-model validated) |
| RQ2 (bridges) | Partially answered | Exploratory (community/layer only, not cross-story) |
| RQ3 (relation-specific roles) | Fully answered | Confirmatory (incl. one low-information null result, G3 — a forest) |
| RQ4 (null-model comparison) | Fully answered | Confirmatory — this project's central finding |
| RQ5 (construction sensitivity) | Fully answered | Descriptive sensitivity analysis (no test of differences between correlations) |
| RQ6 (story clustering) | Partially answered / exploratory (DEC-014, audited in DEC-015) | Pairwise similarity quantified descriptively; evidence for discrete clusters limited (fails pre-set validity rule) |
| RQ7 (temporal/narrative-order evolution) | Partially answered | Exploratory only |
