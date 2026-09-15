"""Phase 5: corpus-level descriptive network metrics (section 18) and
centrality profiles (section 19-20).

Every metric is computed only where structurally meaningful for that graph
(e.g. reciprocity/in-out-degree only for the directed G9 variant; harmonic
centrality preferred over closeness on disconnected graphs, per section
19's explicit instruction) — nothing is force-computed everywhere."""
import json
from pathlib import Path

import networkx as nx
import pandas as pd

from networks import build_all_networks, load_processed

ROOT = Path(__file__).resolve().parents[1]
OUT_STATS = ROOT / "outputs" / "statistics"
OUT_TABLES = ROOT / "outputs" / "tables"


def corpus_level_metrics(graphs: dict) -> pd.DataFrame:
    rows = []
    for name, g in graphs.items():
        n, m = g.number_of_nodes(), g.number_of_edges()
        row = {"network": name, "n_nodes": n, "n_edges": m, "directed": g.is_directed()}
        if n == 0:
            rows.append(row)
            continue

        if g.is_directed():
            row["reciprocity"] = nx.reciprocity(g)
            row["n_weakly_connected_components"] = nx.number_weakly_connected_components(g)
            giant_nodes = max(nx.weakly_connected_components(g), key=len)
            giant = g.subgraph(giant_nodes)
            und_for_clustering = g.to_undirected()
        else:
            row["n_connected_components"] = nx.number_connected_components(g)
            giant_nodes = max(nx.connected_components(g), key=len)
            giant = g.subgraph(giant_nodes)
            und_for_clustering = g

        row["density"] = nx.density(g)
        row["average_clustering"] = nx.average_clustering(und_for_clustering) if n > 2 else None
        row["transitivity"] = nx.transitivity(und_for_clustering)

        try:
            row["degree_assortativity"] = nx.degree_assortativity_coefficient(g)
        except Exception:
            row["degree_assortativity"] = None

        if giant.number_of_nodes() > 1:
            giant_und = giant.to_undirected() if giant.is_directed() else giant
            try:
                row["diameter_giant_component"] = nx.diameter(giant_und)
                row["average_shortest_path_length_giant_component"] = nx.average_shortest_path_length(giant_und)
                ecc = nx.eccentricity(giant_und)
                row["average_eccentricity_giant_component"] = sum(ecc.values()) / len(ecc)
            except Exception:
                pass

        core_input = g.to_undirected() if g.is_directed() else g
        core_input = nx.Graph(core_input)
        core_input.remove_edges_from(nx.selfloop_edges(core_input))
        if core_input.number_of_nodes() > 0:
            coreness = nx.core_number(core_input)
            row["max_k_core"] = max(coreness.values()) if coreness else None

        rows.append(row)
    return pd.DataFrame(rows)


def _safe_eigenvector(g) -> dict:
    try:
        return nx.eigenvector_centrality(g, max_iter=2000, weight="weight")
    except Exception:
        return {n: float("nan") for n in g.nodes()}


def centrality_profile(name: str, g, nodes: pd.DataFrame) -> pd.DataFrame:
    n = g.number_of_nodes()
    if n == 0:
        return pd.DataFrame()

    degree = dict(g.degree())
    strength = dict(g.degree(weight="weight"))
    betweenness = nx.betweenness_centrality(g, weight="weight", normalized=True)
    harmonic = nx.harmonic_centrality(g, distance=None)
    pagerank = nx.pagerank(g, weight="weight")
    eigen = _safe_eigenvector(g)

    data = {
        "node_id": list(g.nodes()),
        "degree": [degree[x] for x in g.nodes()],
        "strength_weighted_degree": [strength[x] for x in g.nodes()],
        "betweenness": [betweenness[x] for x in g.nodes()],
        "harmonic_centrality": [harmonic[x] for x in g.nodes()],
        "pagerank": [pagerank[x] for x in g.nodes()],
        "eigenvector_centrality": [eigen.get(x, float("nan")) for x in g.nodes()],
    }

    if g.is_directed():
        in_deg = dict(g.in_degree())
        out_deg = dict(g.out_degree())
        in_deg_c = nx.in_degree_centrality(g)
        out_deg_c = nx.out_degree_centrality(g)
        data["in_degree"] = [in_deg[x] for x in g.nodes()]
        data["out_degree"] = [out_deg[x] for x in g.nodes()]
        data["in_degree_centrality"] = [in_deg_c[x] for x in g.nodes()]
        data["out_degree_centrality"] = [out_deg_c[x] for x in g.nodes()]
        try:
            hits_h, hits_a = nx.hits(g, max_iter=2000)
            data["hits_hub"] = [hits_h[x] for x in g.nodes()]
            data["hits_authority"] = [hits_a[x] for x in g.nodes()]
        except Exception:
            pass

    df = pd.DataFrame(data)
    name_map = nodes.set_index("node_id")[["canonical_name", "node_type", "story_count"]]
    df = df.merge(name_map, left_on="node_id", right_index=True, how="left")
    df.insert(0, "network", name)
    return df.sort_values("degree", ascending=False)


def main():
    OUT_STATS.mkdir(parents=True, exist_ok=True)
    OUT_TABLES.mkdir(parents=True, exist_ok=True)

    nodes, rel = load_processed()
    graphs = build_all_networks()

    corpus_df = corpus_level_metrics(graphs)
    corpus_df.to_csv(OUT_STATS / "corpus_network_metrics.csv", index=False, encoding="utf-8-sig")
    print(corpus_df.to_string(index=False))

    # Centrality profiles computed for the networks most relevant to the
    # character-importance question (section 19-20): full, person-only,
    # core-social, and the directed variant (in/out-degree, HITS).
    for name in ["G0_full", "G1_person_only", "G2_core_social", "G9_directed"]:
        prof = centrality_profile(name, graphs[name], nodes)
        prof.to_csv(OUT_TABLES / f"centrality_{name}.csv", index=False, encoding="utf-8-sig")
        print(f"\n{name} top 10 by degree:")
        print(prof[["canonical_name", "degree", "strength_weighted_degree", "betweenness", "pagerank"]].head(10).to_string(index=False))


if __name__ == "__main__":
    main()
