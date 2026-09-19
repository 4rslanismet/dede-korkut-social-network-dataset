# Methods

*(Paper-register condensation of `docs/methodology.md`. Every number below was verified against
the pipeline outputs at the time of writing; re-verify against `reports/*.md` before submission if
significant time has passed.)*

## Data

We use a manually coded dataset of characters and relations from the Book of Dede Korkut,
originating from a single coder's three-round standardization process (v1→v2→v3, pre-dating this
study). We rebuilt a canonical version of this dataset (`data/processed/`) with explicit
provenance tracking, after auditing the original repository and re-deriving every headline
statistic from source files rather than trusting prior documentation. The rebuilt dataset
comprises 332 actors, 628 event-level relations, and 85 non-relational narrative events across 14
narrative units (13 *boy* and one *girizgah* prologue). One high-confidence entity merge was
applied (two node identifiers referring to the same named collective actor); seventeen
lower-confidence alias ambiguities were left for manual review rather than resolved
algorithmically.

## Network Construction

We define twelve network variants from the same underlying relation table, each by a single,
auditable filter predicate (implemented once in `src/networks.py`): a full network (G0), a
person-only network restricting to individual (non-collective) actors (G1), a "core social"
network excluding purely identity/title relations (G2), four relation-family-restricted networks
(kinship, communication, cooperation/support, conflict; G3-G6), polarity-restricted positive and
negative networks (G7-G8), a directed network restricted to explicitly directional relations (G9),
and weighted/unweighted variants of the full network (G10-G11). Undirected variants aggregate
repeated interactions between the same unordered actor pair into a single weighted edge; isolated
nodes are removed from each variant's graph object.

## Descriptive Network Analysis

For each applicable variant we compute standard descriptive statistics (density, average
clustering, transitivity, degree assortativity, diameter and average shortest path on the giant
component, k-core structure) and centrality measures (degree, strength, betweenness, harmonic
centrality — used in preference to closeness given the graph's disconnection — PageRank, and, for
the directed variant, in/out-degree and HITS hub/authority scores).

## Community Detection

We apply both the Leiden algorithm (RBConfiguration objective, resolution 1.0) and the Louvain
algorithm to the core-social network (G2), each with a fixed random seed. We assess partition
stability across ten random seeds via the mean pairwise Adjusted Rand Index, and resolution
sensitivity across five resolution values (0.5-1.5). We note explicitly that the core-social
network contains 23 connected components; because modularity-maximizing algorithms assign each
disconnected component its own community by construction, we restrict substantive interpretation
of community structure to the largest (261-node) connected component.

## Statistical Validation via Null Models

To test whether descriptive structural findings reflect genuine higher-order structure rather than
an artifact of the degree distribution alone, we compare each of nine network variants against an
ensemble of 1,000 degree-preserving randomizations (double-edge-swap, ten swaps per edge) on four
metrics: clustering coefficient, transitivity, degree assortativity, and Louvain modularity. For
each network-metric pair we report the observed value, the randomized ensemble's mean and standard
deviation, a z-score, a percentile, and an empirical p-value, and we correct for multiple testing
(36 tests total) using the Benjamini-Hochberg false discovery rate procedure at α=0.05.

## Sensitivity Analysis

We assess the robustness of centrality rankings to six network-construction decisions: including
versus excluding collective actors, weighted versus unweighted edges, all relations versus
core-social relations only, explicitly-coded versus explicitly-plus-inferred relations, group
actors included versus excluded, and the prologue included versus excluded. For each pair we
compute Spearman's ρ, Kendall's τ, and top-k rank overlap (k=10, 20) for degree, betweenness, and
PageRank over the actor set common to both variants.

## Structural Robustness

We simulate node removal under three strategies — uniform random removal (averaged over 100
trials), and adaptive targeted removal ordered by highest current degree (recomputed after every
removal) or highest current betweenness (recomputed every 15 removals, i.e. about 20 times, for
cost) — and track the size of the largest connected component, relative to the original node count,
as a function of the fraction of nodes removed (checkpoints every 2% = 6 nodes; G0_full only).

## Implementation and Reproducibility

All analyses were implemented in Python (NetworkX, python-igraph/leidenalg, SciPy,
scikit-learn/statsmodels) with a single global random seed (42) governing every stochastic
procedure. The full pipeline (eighteen automated stages) is orchestrated by a single script
(`run_pipeline.py`) and covered by eighteen automated tests verifying schema integrity,
aggregation correctness, and the determinism of every stochastic step given a fixed seed.
