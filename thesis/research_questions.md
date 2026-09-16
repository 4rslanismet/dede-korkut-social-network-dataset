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
kinship network (G3) was found statistically indistinguishable from a degree-preserving random
network on every tested metric (clustering, transitivity, assortativity, modularity) — a genuine
negative result, reported rather than hidden.
→ `reports/07_null_models_report.md` §3.4 (G3_kinship null result), `docs/network_models.md`.

## RQ4 — Does the corpus network differ significantly from null networks with similar degree structure?

**Answerable: yes — this rebuild's central confirmatory finding.** Modularity is significantly
higher than a degree-preserving null model in 7/9 tested networks after FDR correction; clustering
is significant in 4/9; degree assortativity is significant in **none** (a retraction of an earlier
descriptive claim).
→ `reports/07_null_models_report.md` (entire report is the answer to this RQ).

## RQ5 — How stable are the main network findings against different network-construction choices?

**Answerable: yes.** Six paired construction choices tested by rank correlation; person+group vs.
person-only identified as the single most consequential choice, girizgah/core-social filtering as
negligible.
→ `reports/08_sensitivity_robustness_report.md` §2.

## RQ6 — What clusterings do the Dede Korkut boy show in terms of character composition and relation profiles?

**Answerable: NOT YET — data/analysis incomplete.** Only the raw actor×story shared-actor
bipartite projection has been computed (`outputs/matrices/story_projection_shared_actors.csv`).
The full similarity metric suite the project brief specifies for this question (actor Jaccard,
weighted Jaccard, cosine similarity, relation-profile similarity, layer-composition similarity,
hierarchical clustering — section 17) has not been built. **Per the brief's own instruction, this
question should be either deferred (with the gap disclosed, as done here) or scoped down to only
what the raw projection supports** — it should not be answered from the incomplete data as if it
were complete.
→ `docs/limitations.md` item 15; `outputs/tables/publication/T08_story_similarity.csv` (marked
partial).

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
| RQ3 (relation-specific roles) | Fully answered | Confirmatory (incl. one genuine null result, G3) |
| RQ4 (null-model comparison) | Fully answered | Confirmatory — this project's central finding |
| RQ5 (construction sensitivity) | Fully answered | Confirmatory |
| RQ6 (story clustering) | **Not answerable with current data** | N/A — flagged, not forced |
| RQ7 (temporal/narrative-order evolution) | Partially answered | Exploratory only |
