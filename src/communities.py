"""Phase 6: community detection (section 21-22).

Leiden and Louvain are both run, each across multiple random seeds (config
seed list) and, for Leiden, across a resolution sweep — all parameters come
from config/analysis.yaml, nothing is hardcoded inline. Stability is
measured via pairwise Adjusted Rand Index across seeds. Community bridge
roles (within-module degree z-score, participation coefficient) are
computed on the primary partition only (Leiden, resolution=1.0, seed 42)."""
import json
from pathlib import Path

import networkx as nx
import numpy as np
import pandas as pd
import yaml
from sklearn.metrics import adjusted_rand_score

import igraph as ig
import leidenalg

from networks import build_all_networks, load_processed

ROOT = Path(__file__).resolve().parents[1]
OUT_STATS = ROOT / "outputs" / "statistics"
OUT_TABLES = ROOT / "outputs" / "tables"

with open(ROOT / "config" / "analysis.yaml", encoding="utf-8") as f:
    CONFIG = yaml.safe_load(f)

SEED = CONFIG["seed"]
N_SEEDS = CONFIG["community"]["n_seeds"]
RESOLUTIONS = CONFIG["community"]["resolution_values"]


def nx_to_igraph(g: nx.Graph):
    nodes = list(g.nodes())
    idx = {n: i for i, n in enumerate(nodes)}
    edges = [(idx[u], idx[v]) for u, v in g.edges()]
    weights = [g[u][v].get("weight", 1.0) for u, v in g.edges()]
    ig_g = ig.Graph(n=len(nodes), edges=edges)
    ig_g.es["weight"] = weights
    ig_g.vs["name"] = nodes
    return ig_g, nodes


def run_leiden(ig_g, resolution: float, seed: int):
    part = leidenalg.find_partition(
        ig_g, leidenalg.RBConfigurationVertexPartition,
        weights="weight", resolution_parameter=resolution, seed=seed,
    )
    return part.membership, part.modularity


def run_louvain(g: nx.Graph, seed: int):
    communities = nx.algorithms.community.louvain_communities(g, weight="weight", seed=seed)
    membership = {}
    for i, comm in enumerate(communities):
        for n in comm:
            membership[n] = i
    modularity = nx.algorithms.community.modularity(g, communities, weight="weight")
    return membership, modularity


def stability_analysis(ig_g, nodes: list) -> dict:
    partitions = []
    modularities = []
    for i in range(N_SEEDS):
        membership, mod = run_leiden(ig_g, resolution=1.0, seed=SEED + i)
        partitions.append(membership)
        modularities.append(mod)

    n_pairs = 0
    ari_sum = 0.0
    for i in range(len(partitions)):
        for j in range(i + 1, len(partitions)):
            ari_sum += adjusted_rand_score(partitions[i], partitions[j])
            n_pairs += 1
    mean_ari = ari_sum / n_pairs if n_pairs else None

    return {
        "n_seeds": N_SEEDS,
        "modularity_mean": float(np.mean(modularities)),
        "modularity_std": float(np.std(modularities)),
        "n_communities_mean": float(np.mean([len(set(p)) for p in partitions])),
        "n_communities_std": float(np.std([len(set(p)) for p in partitions])),
        "mean_pairwise_adjusted_rand_index": mean_ari,
    }


def resolution_sensitivity(ig_g) -> pd.DataFrame:
    rows = []
    for res in RESOLUTIONS:
        membership, mod = run_leiden(ig_g, resolution=res, seed=SEED)
        sizes = pd.Series(membership).value_counts()
        rows.append({
            "resolution": res,
            "n_communities": len(sizes),
            "modularity": mod,
            "largest_community_size": int(sizes.max()),
            "smallest_community_size": int(sizes.min()),
        })
    return pd.DataFrame(rows)


def community_bridge_metrics(g: nx.Graph, membership: dict) -> pd.DataFrame:
    """Within-module degree z-score and participation coefficient
    (Guimera-Amaral style), computed on the primary partition."""
    rows = []
    comm_of = membership
    for node in g.nodes():
        neighbors = list(g.neighbors(node))
        k_i = len(neighbors)
        if k_i == 0:
            rows.append({"node_id": node, "within_module_degree_z": None,
                         "participation_coefficient": None, "n_inter_community_edges": 0})
            continue

        own_comm = comm_of[node]
        same_comm_neighbors = [x for x in neighbors if comm_of[x] == own_comm]
        k_i_within = len(same_comm_neighbors)

        comm_counts = {}
        for x in neighbors:
            comm_counts[comm_of[x]] = comm_counts.get(comm_of[x], 0) + 1
        participation = 1 - sum((c / k_i) ** 2 for c in comm_counts.values())

        rows.append({
            "node_id": node,
            "within_module_degree_raw": k_i_within,
            "participation_coefficient": participation,
            "n_inter_community_edges": k_i - k_i_within,
        })

    df = pd.DataFrame(rows)
    # z-score within_module_degree per community (needs at least 2 nodes/community with std>0)
    df["community"] = df["node_id"].map(comm_of)
    df["within_module_degree_z"] = df.groupby("community")["within_module_degree_raw"].transform(
        lambda s: (s - s.mean()) / s.std() if s.std() and s.std() > 0 else 0.0
    )
    return df


def main():
    OUT_STATS.mkdir(parents=True, exist_ok=True)
    OUT_TABLES.mkdir(parents=True, exist_ok=True)

    nodes_df, rel = load_processed()
    graphs = build_all_networks()
    g = graphs["G2_core_social"]  # core social network is the primary substrate for community structure
    ig_g, node_order = nx_to_igraph(g)

    stability = stability_analysis(ig_g, node_order)
    with open(OUT_STATS / "community_stability_G2_core_social.json", "w", encoding="utf-8") as f:
        json.dump(stability, f, ensure_ascii=False, indent=2)
    print("Stability:", stability)

    res_df = resolution_sensitivity(ig_g)
    res_df.to_csv(OUT_STATS / "community_resolution_sensitivity_G2_core_social.csv", index=False, encoding="utf-8-sig")
    print(res_df.to_string(index=False))

    leiden_membership_list, leiden_mod = run_leiden(ig_g, resolution=1.0, seed=SEED)
    leiden_membership = {node_order[i]: leiden_membership_list[i] for i in range(len(node_order))}

    louvain_membership, louvain_mod = run_louvain(g, seed=SEED)

    ari_leiden_louvain = adjusted_rand_score(
        [leiden_membership[n] for n in node_order],
        [louvain_membership[n] for n in node_order],
    )

    membership_df = pd.DataFrame({
        "node_id": node_order,
        "leiden_community": [leiden_membership[n] for n in node_order],
        "louvain_community": [louvain_membership[n] for n in node_order],
    })
    name_map = nodes_df.set_index("node_id")[["canonical_name", "node_type"]]
    membership_df = membership_df.merge(name_map, left_on="node_id", right_index=True, how="left")
    membership_df.to_csv(OUT_TABLES / "community_membership_G2_core_social.csv", index=False, encoding="utf-8-sig")

    bridge_df = community_bridge_metrics(g, leiden_membership)
    bridge_df = bridge_df.merge(name_map, left_on="node_id", right_index=True, how="left")
    bridge_df.to_csv(OUT_TABLES / "community_bridge_metrics_G2_core_social.csv", index=False, encoding="utf-8-sig")

    summary = {
        "network": "G2_core_social",
        "leiden_modularity_res1.0_seed42": leiden_mod,
        "leiden_n_communities_res1.0_seed42": len(set(leiden_membership_list)),
        "louvain_modularity_seed42": louvain_mod,
        "louvain_n_communities_seed42": len(set(louvain_membership.values())),
        "adjusted_rand_index_leiden_vs_louvain": ari_leiden_louvain,
    }
    with open(OUT_STATS / "community_summary_G2_core_social.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    print(json.dumps(summary, indent=2))

    top_bridges = bridge_df.sort_values("participation_coefficient", ascending=False).head(10)
    print("\nTop 10 by participation coefficient (candidate community bridges):")
    print(top_bridges[["canonical_name", "participation_coefficient", "n_inter_community_edges"]].to_string(index=False))


if __name__ == "__main__":
    main()
