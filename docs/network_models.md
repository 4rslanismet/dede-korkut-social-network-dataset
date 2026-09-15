# Network Models (G0-G11)

Every variant is built from `data/processed/relations_event_level.csv` by the single filter predicate shown, defined in `src/networks.py::NETWORK_DEFINITIONS`. No variant involves manual/ad-hoc edge selection; each is reproducible by re-running `python src/build_networks.py`.

Undirected variants aggregate multiple event-level interactions between the same unordered actor pair into one edge (`weight` = sum of `agirlik`, `interaction_count` = number of underlying event-level relations). Isolated nodes (0 edges after filtering) are removed from the graph object for that variant, but remain listed in `data/processed/nodes.csv`.

| Model | Directed | Nodes | Edges | Density | Components | Largest component | Avg degree | Description |
|---|---|---:|---:|---:|---:|---:|---:|---|
| `G0_full` | False | 311 | 376 | 0.0078 | 23 | 261 | 2.42 | All nodes and all relations, no filtering. |
| `G1_person_only` | False | 154 | 182 | 0.0154 | 14 | 121 | 2.36 | Only actors of node_type == 'kişi' on both endpoints. |
| `G2_core_social` | False | 309 | 374 | 0.0079 | 23 | 259 | 2.42 | All relations except the SEMANTIC family (identity/title/epithet) — 'gerçek sosyal etkileşimler' per project brief section 14. |
| `G3_kinship` | False | 83 | 61 | 0.0179 | 22 | 24 | 1.47 | relation_family_top == KINSHIP. |
| `G4_communication` | False | 74 | 73 | 0.0270 | 11 | 43 | 1.97 | relation_family == communication (diyalog_nötr/olumlu/olumsuz). |
| `G5_cooperation_support` | False | 73 | 65 | 0.0247 | 12 | 45 | 1.78 | relation_family in {cooperation, support}. |
| `G6_conflict` | False | 114 | 92 | 0.0143 | 23 | 43 | 1.61 | relation_family == conflict (çatışma, gerilim). |
| `G7_positive` | False | 127 | 116 | 0.0145 | 18 | 82 | 1.83 | polarity == pozitif. |
| `G8_negative` | False | 126 | 102 | 0.0130 | 25 | 57 | 1.62 | polarity == negatif. |
| `G9_directed` | True | 221 | 324 | 0.0067 | 13 | 194 | 2.93 | Only relations coded directionality == 'yönlü', kept as a directed graph. 'yönsüz' relations are excluded from this variant by definition, not folded in as reciprocal edges. |
| `G10_weighted` | False | 311 | 376 | 0.0078 | 23 | 261 | 2.42 | Same edge set as G0, weights preserved (agirlik 1-5). Used as the 'weighted' arm of the weighted-vs-unweighted sensitivity comparison. |
| `G11_unweighted` | False | 311 | 376 | 0.0078 | 23 | 261 | 2.42 | Same edge set as G0, all weights forced to 1 (binary presence). Used as the 'unweighted' arm of the sensitivity comparison. |

## Full per-model statistics

See [`outputs/networks/network_summary.json`](../outputs/networks/network_summary.json) for the complete machine-readable record (includes clustering, transitivity where applicable).

## Exports

Each model is exported to `outputs/networks/<model>.graphml`, `.gexf`, `_edges.csv`, and `_nodes.csv`.

## Story-level networks

Built by [`src/story_networks.py`](../src/story_networks.py): one undirected weighted graph per
`story_id` (S01-S14), built the same way as the aggregated corpus graphs (unordered actor pairs,
`weight` = sum of `agirlik`). Per-story metrics (nodes, edges, density, average degree, clustering,
transitivity, connected components, average shortest path on the giant component, Freeman degree
centralization per section 115) are written to `data/derived/story_level_metrics.csv`. GraphML
exports live in `outputs/networks/stories/<story_id>.graphml`.

`S01` (Girizgah, the prologue) has only 2 nodes/1 edge — degree centralization is undefined (n<3)
and this story is flagged for the girizgah-included-vs-excluded sensitivity arm (section 15, 29).

## Actor x story bipartite network

Built by the same script. An actor is incident to a story if it appears as source or target of at
least one event-level relation in that story (`data/processed/relations_event_level.csv`). Outputs:

- `outputs/matrices/actor_story_incidence.csv` — 311 actors x 14 stories, 399 incidences
- `outputs/networks/bipartite_actor_story.graphml`
- `outputs/matrices/actor_projection_cooccurrence.csv` — actor x actor co-occurrence counts (shared stories)
- `outputs/matrices/story_projection_shared_actors.csv` — story x story shared-actor counts

**Degree inflation warning (required by section 16):** the actor projection is a simple
co-occurrence count, not a weighted/normalized projection. Actors with a high `story_count` (see
`data/processed/nodes.csv`) will show inflated projected-degree purely as a function of appearing
in many stories, independent of any direct narrative interaction. This projection should be treated
as descriptive only; it is not used as an edge-weighted "social" network for centrality claims
elsewhere in this project.
