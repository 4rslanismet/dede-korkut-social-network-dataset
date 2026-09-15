"""Phase 4: construct the G0-G11 network variants, export them, and write
docs/network_models.md with explicit, auditable definitions."""
import json
from pathlib import Path

import networkx as nx
import pandas as pd

from networks import NETWORK_DEFINITIONS, build_all_networks, load_processed

ROOT = Path(__file__).resolve().parents[1]
OUT_NET = ROOT / "outputs" / "networks"
DOCS = ROOT / "docs"


def basic_stats(g) -> dict:
    n = g.number_of_nodes()
    m = g.number_of_edges()
    directed = g.is_directed()
    stats = {
        "n_nodes": n,
        "n_edges": m,
        "density": nx.density(g) if n > 1 else None,
        "is_directed": directed,
    }
    if n == 0:
        return stats
    if directed:
        stats["n_weakly_connected_components"] = nx.number_weakly_connected_components(g)
        largest_wcc = max(nx.weakly_connected_components(g), key=len)
        stats["largest_component_size"] = len(largest_wcc)
        degrees = [d for _, d in g.degree()]
    else:
        stats["n_connected_components"] = nx.number_connected_components(g)
        largest_cc = max(nx.connected_components(g), key=len)
        stats["largest_component_size"] = len(largest_cc)
        degrees = [d for _, d in g.degree()]
        stats["average_clustering"] = nx.average_clustering(g) if n > 2 else None
        stats["transitivity"] = nx.transitivity(g)
    stats["average_degree"] = sum(degrees) / n if n else None
    stats["n_isolates"] = 0  # isolates already stripped in build_graph
    return stats


def export_graph(name: str, g):
    OUT_NET.mkdir(parents=True, exist_ok=True)
    g_export = g.copy()
    # GraphML/GEXF require primitive attribute types; ensure that.
    for _, _, d in g_export.edges(data=True):
        d["weight"] = float(d.get("weight", 1.0))
        d["interaction_count"] = int(d.get("interaction_count", 1))
    nx.write_graphml(g_export, OUT_NET / f"{name}.graphml")
    nx.write_gexf(g_export, OUT_NET / f"{name}.gexf")

    edge_rows = [
        {"source": u, "target": v, "weight": d.get("weight"), "interaction_count": d.get("interaction_count")}
        for u, v, d in g.edges(data=True)
    ]
    pd.DataFrame(edge_rows).to_csv(OUT_NET / f"{name}_edges.csv", index=False, encoding="utf-8-sig")

    node_rows = [
        {"node_id": nid, **{k: v for k, v in attrs.items()}}
        for nid, attrs in g.nodes(data=True)
    ]
    pd.DataFrame(node_rows).to_csv(OUT_NET / f"{name}_nodes.csv", index=False, encoding="utf-8-sig")


def main():
    nodes, rel = load_processed()
    graphs = build_all_networks()

    all_stats = {}
    for name, g in graphs.items():
        stats = basic_stats(g)
        all_stats[name] = stats
        export_graph(name, g)
        print(name, stats)

    OUT_NET.mkdir(parents=True, exist_ok=True)
    with open(OUT_NET / "network_summary.json", "w", encoding="utf-8") as f:
        json.dump(all_stats, f, ensure_ascii=False, indent=2, default=str)

    # Build docs/network_models.md
    DOCS.mkdir(parents=True, exist_ok=True)
    md = []
    md.append("# Network Models (G0-G11)\n")
    md.append(
        "Every variant is built from `data/processed/relations_event_level.csv` by the single "
        "filter predicate shown, defined in `src/networks.py::NETWORK_DEFINITIONS`. No variant "
        "involves manual/ad-hoc edge selection; each is reproducible by re-running "
        "`python src/build_networks.py`.\n"
    )
    md.append(
        "Undirected variants aggregate multiple event-level interactions between the same "
        "unordered actor pair into one edge (`weight` = sum of `agirlik`, `interaction_count` = "
        "number of underlying event-level relations). Isolated nodes (0 edges after filtering) "
        "are removed from the graph object for that variant, but remain listed in "
        "`data/processed/nodes.csv`.\n"
    )
    md.append("| Model | Directed | Nodes | Edges | Density | Components | Largest component | Avg degree | Description |")
    md.append("|---|---|---:|---:|---:|---:|---:|---:|---|")
    for name, spec in NETWORK_DEFINITIONS.items():
        s = all_stats[name]
        comp = s.get("n_connected_components", s.get("n_weakly_connected_components", "N/A"))
        density_str = f"{s['density']:.4f}" if s.get("density") is not None else "N/A"
        avg_deg_str = f"{s['average_degree']:.2f}" if s.get("average_degree") is not None else "N/A"
        md.append(
            f"| `{name}` | {s['is_directed']} | {s['n_nodes']} | {s['n_edges']} | {density_str} | "
            f"{comp} | {s.get('largest_component_size', 'N/A')} | {avg_deg_str} | {spec['description']} |"
        )
    md.append("")
    md.append("## Full per-model statistics\n")
    md.append("See [`outputs/networks/network_summary.json`](../outputs/networks/network_summary.json) "
               "for the complete machine-readable record (includes clustering, transitivity where applicable).\n")
    md.append("## Exports\n")
    md.append("Each model is exported to `outputs/networks/<model>.graphml`, `.gexf`, `_edges.csv`, "
               "and `_nodes.csv`.\n")

    with open(DOCS / "network_models.md", "w", encoding="utf-8") as f:
        f.write("\n".join(md))

    print("\nWrote docs/network_models.md and outputs/networks/*")


if __name__ == "__main__":
    main()
