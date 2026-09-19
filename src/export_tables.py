"""Phase 12: publication tables T01-T11 (section 49), CSV + LaTeX.

Every table is assembled from already-computed outputs (data/processed,
outputs/statistics, outputs/tables) - nothing here recomputes analysis, it
only reformats for publication."""
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "tables" / "publication"


def write(df: pd.DataFrame, name: str, caption: str, float_format: str = "%.3f"):
    OUT.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT / f"{name}.csv", index=False, encoding="utf-8-sig")
    latex = df.to_latex(index=False, float_format=lambda x: float_format % x if isinstance(x, float) else str(x),
                         caption=caption, label=f"tab:{name.lower()}", longtable=False)
    with open(OUT / f"{name}.tex", "w", encoding="utf-8") as f:
        f.write(latex)
    print(f"Wrote {name}.csv / .tex ({len(df)} rows)")


def t01_dataset_overview():
    nodes = pd.read_csv(ROOT / "data" / "processed" / "nodes.csv", encoding="utf-8-sig")
    rel = pd.read_csv(ROOT / "data" / "processed" / "relations_event_level.csv", encoding="utf-8-sig")
    stories = pd.read_csv(ROOT / "data" / "processed" / "stories.csv", encoding="utf-8-sig")
    agg = pd.read_csv(ROOT / "data" / "processed" / "relations_aggregated.csv", encoding="utf-8-sig")
    events = pd.read_csv(ROOT / "data" / "final" / "dede_korkut_olaylar_temiz.csv", encoding="utf-8-sig")

    rows = [
        ("Stories (boy + girizgah)", len(stories)),
        ("Canonical actors (nodes)", len(nodes)),
        ("Event-level relations", len(rel)),
        ("Aggregated unique actor pairs", len(agg)),
        ("Narrative events (non-relational)", len(events)),
        ("Person-type actors (kişi)", int((nodes["node_type"] == "kişi").sum())),
        ("Group-type actors (grup)", int((nodes["node_type"] == "grup").sum())),
        ("Other actor types (mythological/animal/object/place)", int((~nodes["node_type"].isin(["kişi", "grup"])).sum())),
    ]
    df = pd.DataFrame(rows, columns=["Metric", "Value"])
    write(df, "T01_dataset_overview", "Dataset overview (canonical, Phase 3)", float_format="%d")


def t02_relation_taxonomy():
    df = pd.read_csv(ROOT / "data" / "processed" / "relation_taxonomy.csv", encoding="utf-8-sig")
    write(df, "T02_relation_taxonomy", "Relation taxonomy: 17 observed relation types mapped to interpretive families (Phase 3)")


def t03_story_level_statistics():
    df = pd.read_csv(ROOT / "data" / "derived" / "story_level_metrics.csv", encoding="utf-8-sig")
    stories = pd.read_csv(ROOT / "data" / "processed" / "stories.csv", encoding="utf-8-sig")
    # Two different "edge" counts exist and must not be conflated (review finding, DEC-019):
    #   n_relation_records    raw coded relation rows of the story (stories.csv n_edges)
    #   n_edges_aggregated    edges of the story's aggregated undirected graph (one per unordered actor pair);
    #                         density / average degree / clustering below are computed on THIS graph
    df = df.merge(stories[["story_id", "n_edges"]].rename(columns={"n_edges": "n_relation_records"}), on="story_id", how="left")
    df = df.rename(columns={"n_edges": "n_edges_aggregated"})
    cols = ["story_id", "boy_name_raw", "n_nodes", "n_relation_records", "n_edges_aggregated", "density", "average_degree",
            "average_clustering", "n_connected_components", "degree_centralization"]
    write(df[cols], "T03_story_level_statistics",
          "Story-level network statistics: raw relation records vs. edges of the aggregated story graph (density, degree and clustering use the aggregated graph)")


def t04_centrality_results():
    df = pd.read_csv(ROOT / "outputs" / "tables" / "centrality_G0_full.csv", encoding="utf-8-sig")
    top = df.sort_values("degree", ascending=False).head(20)
    cols = ["canonical_name", "node_type", "degree", "strength_weighted_degree", "betweenness",
            "harmonic_centrality", "pagerank", "story_count"]
    write(top[cols], "T04_centrality_results",
          "Top 20 actors by degree, G0\\_full (preliminary/descriptive). Betweenness uses shortest-path distance = 1/tie strength (DEC-017); "
          "unweighted hop-count betweenness is in the full centrality table")


def t05_community_statistics():
    with open(ROOT / "outputs" / "statistics" / "community_summary_G2_core_social.json", encoding="utf-8") as f:
        import json
        summary = json.load(f)
    with open(ROOT / "outputs" / "statistics" / "community_stability_G2_core_social.json", encoding="utf-8") as f:
        stability = json.load(f)
    with open(ROOT / "outputs" / "networks" / "network_summary.json", encoding="utf-8") as f:
        n_components = json.load(f)[summary["network"]]["n_connected_components"]
    rows = [
        ("Network", summary["network"]),
        ("Leiden modularity (res=1.0, seed=42)", round(summary["leiden_modularity_res1.0_seed42"], 4)),
        ("Leiden n communities", summary["leiden_n_communities_res1.0_seed42"]),
        ("Louvain modularity (seed=42)", round(summary["louvain_modularity_seed42"], 4)),
        ("Louvain n communities", summary["louvain_n_communities_seed42"]),
        ("ARI (Leiden vs Louvain)", round(summary["adjusted_rand_index_leiden_vs_louvain"], 4)),
        ("Stability: mean modularity (10 seeds)", round(stability["modularity_mean"], 4)),
        ("Stability: mean pairwise ARI (10 seeds)", round(stability["mean_pairwise_adjusted_rand_index"], 4)),
        ("Caveat", f"{n_components} connected components inflate raw community count with trivial isolates (see reports/06 sec 1.4)"),
    ]
    df = pd.DataFrame(rows, columns=["Metric", "Value"])
    write(df, "T05_community_statistics", "Community detection statistics, G2\\_core\\_social (Phase 6)", float_format="%s")


def t06_layer_specific_metrics():
    df = pd.read_csv(ROOT / "outputs" / "tables" / "multilayer_profile.csv", encoding="utf-8-sig")
    top = df.sort_values("n_active_layers", ascending=False).head(15)
    cols = ["canonical_name", "node_type", "n_active_layers", "layer_participation_coefficient",
            "cross_layer_entropy", "total_degree_across_layers"]
    write(top[cols], "T06_layer_specific_metrics", "Top 15 actors by number of active relation layers (Phase 6)")


def t07_actor_story_participation():
    nodes = pd.read_csv(ROOT / "data" / "processed" / "nodes.csv", encoding="utf-8-sig")
    top = nodes.sort_values("story_count", ascending=False).head(15)
    cols = ["canonical_name", "node_type", "story_count", "relation_count", "event_count", "first_story"]
    write(top[cols], "T07_actor_story_participation", "Top 15 actors by number of distinct stories (Phase 3-4)")


def t08_story_similarity():
    # story_similarity.py (RQ6, DEC-014) authors the full 91-pair, 5-metric T08.
    # Do not overwrite it with the older partial shared-actor projection.
    if (ROOT / "outputs" / "matrices" / "story_similarity_actor_jaccard.csv").exists():
        print("T08_story_similarity: authored by story_similarity.py (full 5-metric table) - left as is")
        return
    path = ROOT / "outputs" / "matrices" / "story_projection_shared_actors.csv"
    if not path.exists():
        df = pd.DataFrame([{"status": "not_applicable", "reason": "story similarity metrics (Jaccard/cosine/etc, section 17) not yet computed - only the raw shared-actor bipartite projection exists"}])
        write(df, "T08_story_similarity", "Story similarity (NOT YET COMPUTED - placeholder)", float_format="%s")
        return
    df = pd.read_csv(path, index_col=0, encoding="utf-8-sig")
    write(df.reset_index(), "T08_story_similarity", "Story x story shared-actor counts (bipartite projection; full similarity metrics pending)")


def t09_null_model_tests():
    df = pd.read_csv(ROOT / "outputs" / "statistics" / "null_model_fdr_corrected.csv", encoding="utf-8-sig")
    write(df, "T09_null_model_tests", "Null model tests, all 36, with Benjamini-Hochberg FDR correction (Phase 7)")


def t10_sensitivity_analysis():
    df = pd.read_csv(ROOT / "outputs" / "tables" / "sensitivity_rank_stability.csv", encoding="utf-8-sig")
    write(df, "T10_sensitivity_analysis", "Sensitivity analysis: rank stability across 6 network-construction variant pairs (Phase 8)")


def t11_robustness_results():
    import json
    with open(ROOT / "outputs" / "statistics" / "robustness_summary_G0_full.json", encoding="utf-8") as f:
        summary = json.load(f)
    n0 = summary["n_nodes"]
    bases = [("all_G0_nodes", "fraction_removed_below_threshold_of_all_nodes", summary["denominators"]["all_nodes"]),
             ("initial_giant_component", "fraction_removed_below_threshold_of_initial_giant_component", summary["denominators"]["initial_giant_component"])]
    rows = []
    exact_key = {"all_G0_nodes": "all_nodes", "initial_giant_component": "initial_giant_component"}
    for basis, key, denominator in bases:
        for threshold_label in ("50pct", "10pct"):
            for strategy, val in summary[key][threshold_label].items():
                # exact crossing, checked after EVERY removal (the checkpoint-grid value above can overshoot by up to one grid step)
                if strategy == "degree_targeted":
                    exact = summary["degree_targeted_tie_break_sensitivity"][exact_key[basis]][threshold_label]["nodes_removed_median"]
                elif strategy == "betweenness_targeted":
                    exact = summary["betweenness_targeted_exact_nodes_removed"][exact_key[basis]][threshold_label]
                else:
                    exact = None
                rows.append({"component_size_basis": basis, "basis_size_nodes": denominator,
                             "largest_component_below": threshold_label.replace("pct", "%") + " of basis",
                             "removal_strategy": strategy,
                             "fraction_of_G0_nodes_removed": round(val, 4) if val is not None else None,
                             "nodes_removed_on_checkpoint_grid": int(round(val * n0)) if val is not None else None,
                             "nodes_removed_exact": exact})
    df = pd.DataFrame(rows)
    write(df, "T11_robustness_results",
          f"Structural robustness of G0\\_full: share of the {n0} G0 nodes removed until the largest connected component falls below 50\\% / 10\\% of a stated basis "
          f"(all G0 nodes, or the initial giant component). Grid columns use checkpoints every {summary['checkpoint_step_nodes']} nodes; "
          "the exact columns check after every removal (degree-targeted: median over random tie-breaks; random: grid only). "
          "The grid-based degree- vs betweenness-targeted gap is a resolution/tie-break artifact, not a supported claim (DEC-019)")


def main():
    t01_dataset_overview()
    t02_relation_taxonomy()
    t03_story_level_statistics()
    t04_centrality_results()
    t05_community_statistics()
    t06_layer_specific_metrics()
    t07_actor_story_participation()
    t08_story_similarity()
    t09_null_model_tests()
    t10_sensitivity_analysis()
    t11_robustness_results()
    print(f"\nAll tables written to {OUT}")


if __name__ == "__main__":
    main()
