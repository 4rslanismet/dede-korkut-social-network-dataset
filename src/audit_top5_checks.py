"""Final-academic-audit checks behind the FINAL_REBUILD_REPORT "Top 5 findings" (DEC-015).

Nothing here changes any earlier result; it re-reads existing outputs and adds
three cheap verifications so each headline claim can be tied to evidence:

A. Modularity finding (#1): 23 connected components could inflate observed
   Louvain modularity relative to a degree-preserving null that reconnects
   components. Re-run the same null (double_edge_swap, 10 x edges swaps, 1000
   randomizations, Louvain, seed 42, same procedure as null_models.py) on the
   largest connected component of G0_full only.
B. Kinship null (#4): check whether G3_kinship is acyclic (a forest), which
   would make clustering/transitivity structurally zero and those two tests
   uninformative.
C. Sensitivity (#3): per-pair mean/min/ranking of Spearman rho from the
   existing sensitivity table, so "most consequential" is stated against the
   actual numbers.
D. Robustness (#5): the reference size and absolute node counts behind the
   removal thresholds.

Output: outputs/statistics/audit_top5_checks.json
"""
import json
from pathlib import Path

import networkx as nx
import numpy as np
import pandas as pd
import yaml

from networks import build_all_networks
from null_models import modularity_for_graph, randomized_copy, z_and_percentile

ROOT = Path(__file__).resolve().parents[1]
OUT_STATS = ROOT / "outputs" / "statistics"

with open(ROOT / "config" / "analysis.yaml", encoding="utf-8") as f:
    CONFIG = yaml.safe_load(f)
SEED = CONFIG["seed"]
N_RANDOM = CONFIG["null_models"]["n_random"]


def check_modularity_giant_component(graphs: dict) -> dict:
    g = graphs["G0_full"]
    giant_nodes = max(nx.connected_components(g), key=len)
    giant = g.subgraph(giant_nodes).copy()
    obs = modularity_for_graph(giant, seed=SEED)
    rng = np.random.default_rng(SEED)
    vals = []
    for i in range(N_RANDOM):
        h = randomized_copy(giant, rng)
        vals.append(modularity_for_graph(h, seed=SEED + i))
    vals = np.array(vals)
    stats = z_and_percentile(obs, vals)
    return {
        "network": "G0_full, largest connected component only",
        "n_nodes": giant.number_of_nodes(), "n_edges": giant.number_of_edges(),
        "n_random": N_RANDOM, "seed": SEED,
        "observed_louvain_modularity": obs,
        "random_mean": stats["random_mean"], "random_std": stats["random_std"],
        "z_score": stats["z_score"], "empirical_p_two_sided": stats["empirical_p"],
        "observed_exceeds_all_randomizations": bool((vals < obs).all()),
        "reading": "supports the whole-network finding if z is clearly positive and p small",
    }


def check_kinship_forest(graphs: dict) -> dict:
    g = graphs["G3_kinship"]
    n, m = g.number_of_nodes(), g.number_of_edges()
    c = nx.number_connected_components(g)
    cycles = m - (n - c)  # 0 iff the graph is a forest
    return {
        "network": "G3_kinship", "n_nodes": n, "n_edges": m, "n_components": c,
        "cyclomatic_number": cycles, "is_forest": bool(cycles == 0),
        "n_triangles": int(sum(nx.triangles(g).values()) // 3),
        "reading": "if is_forest, clustering and transitivity are structurally 0 in the observed network, so those two tests carry little information; only assortativity and modularity are informative",
    }


def check_sensitivity_pairs() -> dict:
    t = pd.read_csv(ROOT / "outputs" / "tables" / "sensitivity_rank_stability.csv", encoding="utf-8-sig")
    rows = []
    for pair, grp in t.groupby("pair"):
        by_metric = grp.set_index("metric")
        rows.append({
            "pair": pair,
            "n_common_nodes": int(grp["n_common_nodes"].iloc[0]),
            "spearman_rho_mean": round(float(grp["spearman_rho"].mean()), 4),
            "spearman_rho_min": round(float(grp["spearman_rho"].min()), 4),
            "spearman_rho_by_metric": {k: round(float(v), 4) for k, v in by_metric["spearman_rho"].items()},
            "top10_overlap_by_metric": {k: float(v) for k, v in by_metric["top_10_overlap_fraction"].items()},
        })
    rows.sort(key=lambda r: r["spearman_rho_mean"])
    lowest_by_metric = {}
    for metric in ["degree", "betweenness", "pagerank"]:
        lowest_by_metric[metric] = min(rows, key=lambda r: r["spearman_rho_by_metric"][metric])["pair"]
    return {
        "pairs_ranked_by_mean_rho_ascending": rows,
        "pair_with_lowest_rho_per_metric": lowest_by_metric,
        "reading": "'most consequential' depends on the metric; compare pairs only with the caveat that n_common_nodes differs across pairs and no test of differences between rho values was run",
    }


def check_robustness_reference() -> dict:
    with open(OUT_STATS / "robustness_summary_G0_full.json", encoding="utf-8") as f:
        s = json.load(f)
    n0 = s["n_nodes"]
    graphs = build_all_networks()
    giant0 = len(max(nx.connected_components(graphs["G0_full"]), key=len))
    step = max(1, int(round(n0 * s["step_fraction"])))
    out = {"n_nodes": n0, "initial_giant_component_size": giant0,
           "initial_giant_fraction_of_nodes": round(giant0 / n0, 4),
           "removal_step_nodes": step, "thresholds": {}}
    for key, label in [("fraction_removed_to_drop_giant_below_50pct", "50pct_of_original_node_count"),
                       ("fraction_removed_to_drop_giant_below_10pct", "10pct_of_original_node_count")]:
        out["thresholds"][label] = {k: {"fraction_removed": round(v, 4), "nodes_removed": int(round(v * n0))}
                                    for k, v in s[key].items()}
    out["reading"] = ("thresholds are relative to the ORIGINAL NODE COUNT (311), not to the original giant component "
                      "(261 = 83.9% of nodes); targeted-removal crossings are resolved only to one removal step of "
                      f"{step} nodes ({step / n0:.1%}); betweenness ranking is recomputed every "
                      f"{max(1, n0 // 20)} removals, not after each removal")
    return out


def main():
    graphs = build_all_networks()
    result = {
        "A_modularity_giant_component_null": check_modularity_giant_component(graphs),
        "B_kinship_forest_check": check_kinship_forest(graphs),
        "C_sensitivity_pair_ranking": check_sensitivity_pairs(),
        "D_robustness_reference": check_robustness_reference(),
    }
    with open(OUT_STATS / "audit_top5_checks.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2, default=str)
    a = result["A_modularity_giant_component_null"]
    print("A giant-component modularity: obs=%.4f null_mean=%.4f z=%.2f p=%.4f exceeds_all=%s" % (
        a["observed_louvain_modularity"], a["random_mean"], a["z_score"], a["empirical_p_two_sided"], a["observed_exceeds_all_randomizations"]))
    print("B kinship:", result["B_kinship_forest_check"])
    for r in result["C_sensitivity_pair_ranking"]["pairs_ranked_by_mean_rho_ascending"]:
        print("C", r["pair"], r["n_common_nodes"], r["spearman_rho_mean"], r["spearman_rho_min"])
    print("C lowest per metric:", result["C_sensitivity_pair_ranking"]["pair_with_lowest_rho_per_metric"])
    print("D", json.dumps(result["D_robustness_reference"], indent=1))


if __name__ == "__main__":
    main()
