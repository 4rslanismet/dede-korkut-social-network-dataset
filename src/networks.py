"""Reusable network-construction library.

All G0-G11 variants (section 14 of the project brief) are built from the
same source: data/processed/relations_event_level.csv + nodes.csv. Each
variant is defined as an explicit row-filter predicate over the event-level
table, so the definition is auditable in one place (NETWORK_DEFINITIONS)
rather than scattered across scripts.

Two representations are built per variant:
  - a simple weighted undirected nx.Graph (edges aggregated across the
    unordered actor pair, weight = sum of `agirlik` for edges matching the
    filter) — used for the great majority of structural metrics.
  - for G9 only, an nx.DiGraph built from the subset of relations marked
    `directionality == 'yönlü'` (undirected relations are out of scope for
    a directed-network variant by definition, not merged in as reciprocal
    edges — this is a modeling choice, documented in docs/network_models.md).
"""
from pathlib import Path
from typing import Callable

import networkx as nx
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"


def load_processed():
    nodes = pd.read_csv(PROCESSED / "nodes.csv", encoding="utf-8-sig")
    rel = pd.read_csv(PROCESSED / "relations_event_level.csv", encoding="utf-8-sig")
    return nodes, rel


def strength_to_distance(strength) -> float:
    """Convert a tie STRENGTH into a shortest-path DISTANCE: distance = 1 / strength.

    The edge attribute `weight` in every graph built here is tie strength
    (sum of the coded 1-5 `agirlik` values over an actor pair): larger = a
    stronger tie. NetworkX shortest-path functions (weighted betweenness,
    closeness, ...) interpret their `weight=` argument as DISTANCE/COST
    (smaller = shorter), so passing strength directly makes strong ties count
    as LONG paths. Shortest-path-based metrics must therefore use this derived
    distance (edge attribute "distance"), never `weight` (DEC-017).

    Raises ValueError for strength <= 0 or NaN instead of returning an
    arbitrary value."""
    try:
        s = float(strength)
    except (TypeError, ValueError):
        raise ValueError(f"tie strength must be numeric, got {strength!r}")
    if not (s > 0) or s != s:  # rejects <= 0 and NaN
        raise ValueError(f"tie strength must be > 0 to derive a distance, got {strength!r}")
    return 1.0 / s


def with_distance(g):
    """Return a copy of `g` whose every edge carries distance = 1/weight (see
    strength_to_distance). `weight` (strength) is left untouched; the input
    graph is not modified and exported graph files do not gain the attribute."""
    h = g.copy()
    for _, _, data in h.edges(data=True):
        data["distance"] = strength_to_distance(data.get("weight", 1.0))
    return h


def _semantic_family(rel: pd.DataFrame) -> pd.Series:
    return rel["relation_family_top"] == "SEMANTIC"


NETWORK_DEFINITIONS: dict[str, dict] = {
    "G0_full": {
        "description": "All nodes and all relations, no filtering.",
        "filter": lambda rel, nodes: pd.Series(True, index=rel.index),
        "directed": False,
    },
    "G1_person_only": {
        "description": "Only actors of node_type == 'kişi' on both endpoints.",
        "filter": lambda rel, nodes: rel["source_type"].eq("kişi") & rel["target_type"].eq("kişi"),
        "directed": False,
    },
    "G2_core_social": {
        "description": "All relations except the SEMANTIC family (identity/title/epithet) — "
                        "'gerçek sosyal etkileşimler' per project brief section 14.",
        "filter": lambda rel, nodes: ~_semantic_family(rel),
        "directed": False,
    },
    "G3_kinship": {
        "description": "relation_family_top == KINSHIP.",
        "filter": lambda rel, nodes: rel["relation_family_top"].eq("KINSHIP"),
        "directed": False,
    },
    "G4_communication": {
        "description": "relation_family == communication (diyalog_nötr/olumlu/olumsuz).",
        "filter": lambda rel, nodes: rel["relation_family"].eq("communication"),
        "directed": False,
    },
    "G5_cooperation_support": {
        "description": "relation_family in {cooperation, support}.",
        "filter": lambda rel, nodes: rel["relation_family"].isin(["cooperation", "support"]),
        "directed": False,
    },
    "G6_conflict": {
        "description": "relation_family == conflict (çatışma, gerilim).",
        "filter": lambda rel, nodes: rel["relation_family"].eq("conflict"),
        "directed": False,
    },
    "G7_positive": {
        "description": "polarity == pozitif.",
        "filter": lambda rel, nodes: rel["polarity"].eq("pozitif"),
        "directed": False,
    },
    "G8_negative": {
        "description": "polarity == negatif.",
        "filter": lambda rel, nodes: rel["polarity"].eq("negatif"),
        "directed": False,
    },
    "G9_directed": {
        "description": "Only relations coded directionality == 'yönlü', kept as a directed graph. "
                        "'yönsüz' relations are excluded from this variant by definition, not "
                        "folded in as reciprocal edges.",
        "filter": lambda rel, nodes: rel["directionality"].eq("yönlü"),
        "directed": True,
    },
    "G10_weighted": {
        "description": "Same edge set as G0, weights preserved (agirlik 1-5). Used as the "
                        "'weighted' arm of the weighted-vs-unweighted sensitivity comparison.",
        "filter": lambda rel, nodes: pd.Series(True, index=rel.index),
        "directed": False,
    },
    "G11_unweighted": {
        "description": "Same edge set as G0, all weights forced to 1 (binary presence). Used as "
                        "the 'unweighted' arm of the sensitivity comparison.",
        "filter": lambda rel, nodes: pd.Series(True, index=rel.index),
        "directed": False,
        "force_unweight": True,
    },
}


def _aggregate_undirected(rel_subset: pd.DataFrame) -> pd.DataFrame:
    pair = rel_subset.apply(lambda r: tuple(sorted([str(r["source_id"]), str(r["target_id"])])), axis=1)
    tmp = rel_subset.copy()
    tmp["_a"] = pair.map(lambda p: p[0])
    tmp["_b"] = pair.map(lambda p: p[1])
    w = pd.to_numeric(tmp["weight"], errors="coerce").fillna(0)
    tmp["_w"] = w
    grouped = tmp.groupby(["_a", "_b"]).agg(
        weight=("_w", "sum"),
        interaction_count=("_w", "size"),
    ).reset_index()
    return grouped.rename(columns={"_a": "source", "_b": "target"})


def build_graph(name: str, nodes: pd.DataFrame, rel: pd.DataFrame) -> "nx.Graph | nx.DiGraph":
    spec = NETWORK_DEFINITIONS[name]
    mask = spec["filter"](rel, nodes)
    subset = rel[mask].copy()
    subset = subset.dropna(subset=["source_id", "target_id"])

    if spec.get("directed"):
        g = nx.DiGraph(name=name)
        g.add_nodes_from(nodes["node_id"])
        for _, r in subset.iterrows():
            w = 1.0 if spec.get("force_unweight") else float(r["weight"]) if pd.notna(r["weight"]) else 1.0
            if g.has_edge(r["source_id"], r["target_id"]):
                g[r["source_id"]][r["target_id"]]["weight"] += w
                g[r["source_id"]][r["target_id"]]["interaction_count"] += 1
            else:
                g.add_edge(r["source_id"], r["target_id"], weight=w, interaction_count=1)
    else:
        agg = _aggregate_undirected(subset)
        g = nx.Graph(name=name)
        g.add_nodes_from(nodes["node_id"])
        for _, r in agg.iterrows():
            w = 1.0 if spec.get("force_unweight") else float(r["weight"])
            g.add_edge(r["source"], r["target"], weight=w, interaction_count=int(r["interaction_count"]))

    node_attr_cols = ["canonical_name", "node_type", "story_count"]
    attrs = nodes.set_index("node_id")[node_attr_cols].to_dict("index")
    nx.set_node_attributes(g, attrs)

    g.remove_nodes_from(list(nx.isolates(g)))
    return g


def build_all_networks() -> dict:
    nodes, rel = load_processed()
    return {name: build_graph(name, nodes, rel) for name in NETWORK_DEFINITIONS}


def build_story_graph(nodes: pd.DataFrame, rel: pd.DataFrame, story_id: str) -> nx.Graph:
    subset = rel[rel["story_id"] == story_id].dropna(subset=["source_id", "target_id"])
    agg = _aggregate_undirected(subset)
    g = nx.Graph(name=story_id)
    for _, r in agg.iterrows():
        g.add_edge(r["source"], r["target"], weight=float(r["weight"]), interaction_count=int(r["interaction_count"]))
    return g
