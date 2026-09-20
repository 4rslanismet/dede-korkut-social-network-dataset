# Figure Inventory

All figures follow the no-hairball design rules in `docs/methodology.md` §8. Located under
`outputs/figures/` (source) and mirrored in `paper/figures/` (paper package copy) and
`docs/figures/` (website copy).

| ID | Title | File | Used for RQ | Notes |
|---|---|---|---|---|
| F02 | Corpus full network (G0_full) | `corpus/F02_corpus_full_network.png` | RQ1 | 311 nodes, degree-scaled, top-6 labeled |
| F03 | Person-only network (G1_person_only) | `corpus/F03_person_only_network.png` | RQ1, RQ5 | 154 nodes |
| F06 | Community structure (G2_core_social) | `communities/F06_community_structure.png` | RQ1, RQ4 | Giant component only colored; grey = 22 trivial components — caption states the caveat directly |
| F07 | Top actors centrality comparison | `corpus/F07_top_actors_centrality_comparison.png` | RQ1 | Degree/betweenness/PageRank side by side, top 15 |
| F15 | Null model distributions | `null_models/F15_null_model_distributions.png` | RQ4 | All 12 FDR-significant tests, random ensemble vs. observed |
| F16 | Sensitivity correlation matrix | `sensitivity/F16_sensitivity_correlation_matrix.png` | RQ5 | 6 pairs × 3 metrics, Spearman ρ heatmap |
| F17 | Centrality rank stability scatter | `sensitivity/F17_centrality_rank_stability.png` | RQ5 | Person+group vs. person-only degree rank |
| F18 | Structural robustness curves | `robustness/F18_structural_robustness_curves.png` | RQ5 | Random vs. degree- vs. betweenness-targeted removal (y-axis: largest component / original network size, i.e. all G0 nodes) |
| F10 | Story similarity heatmap | `similarity/F10_story_similarity_heatmap.png` | RQ6 | Actor Jaccard, 14×14, diagonal masked grey; colour scale ends at max off-diagonal 0.15 (low overlap throughout). Exploratory (post-project, DEC-014/015) |
| F11 | Story actor-overlap network | `similarity/F11_story_similarity_network.png` | RQ6 | Top 15 of 91 pairs by actor Jaccard, edge weight = line darkness/thickness; relatively most-overlapping pairs, not strong similarity or clusters (figure carries this caveat) |

## Not Yet Produced (from the F01-F18 target list, master prompt section 48)

F01 (dataset construction workflow — `docs/architecture_diagram.svg` covers this need already,
consider renaming/promoting it to F01), F04 (core-social network — near-duplicate of F02, low
priority), F05 (multilayer overview), F08 (story-level metric comparison), F09 (actor×story
bipartite), F12 (layer participation — data exists in `outputs/tables/multilayer_profile.csv`,
chart not built), F13 (positive/negative network comparison), F14 (narrative-order evolution —
data exists in `outputs/tables/narrative_order_windows.csv`, chart not built).
