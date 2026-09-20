"""Phase 6 (cont.): signed network analysis (section 24) and directed
network analysis incl. triad census (section 25).

Signed structural-balance analysis requires triangles where all three edges
carry a definite sign. This corpus is sparse (density ~0.01); the script
checks the actual triangle count before attempting balance analysis and
reports 'not_applicable' with the reason if there are too few to support
any claim, rather than forcing a result."""
import json
from pathlib import Path

import networkx as nx
import pandas as pd

from networks import build_all_networks, load_processed

ROOT = Path(__file__).resolve().parents[1]
OUT_STATS = ROOT / "outputs" / "statistics"
OUT_TABLES = ROOT / "outputs" / "tables"

MIN_TRIANGLES_FOR_BALANCE_CLAIM = 15  # documented threshold, not derived from data


def signed_node_profile(rel: pd.DataFrame, nodes: pd.DataFrame) -> pd.DataFrame:
    pos = rel[rel["polarity"] == "pozitif"]
    neg = rel[rel["polarity"] == "negatif"]

    def degree_strength(df, id_cols):
        long = pd.concat([df[[c]].rename(columns={c: "node_id"}) for c in id_cols])
        long = long.dropna()
        deg = long.groupby("node_id").size()
        return deg

    def weighted(df, id_cols, weight_col="weight"):
        frames = []
        for c in id_cols:
            frames.append(df[[c, weight_col]].rename(columns={c: "node_id"}))
        long = pd.concat(frames).dropna(subset=["node_id"])
        return long.groupby("node_id")[weight_col].sum()

    pos_deg = degree_strength(pos, ["source_id", "target_id"])
    neg_deg = degree_strength(neg, ["source_id", "target_id"])
    pos_str = weighted(pos, ["source_id", "target_id"])
    neg_str = weighted(neg, ["source_id", "target_id"])

    df = pd.DataFrame({"node_id": nodes["node_id"]}).set_index("node_id")
    df["positive_degree"] = pos_deg
    df["negative_degree"] = neg_deg
    df["positive_strength"] = pos_str
    df["negative_strength"] = neg_str
    df = df.fillna(0)
    total_deg = df["positive_degree"] + df["negative_degree"]
    df["positive_negative_ratio"] = df.apply(
        lambda r: (r["positive_degree"] / r["negative_degree"]) if r["negative_degree"] > 0
        else (float("inf") if r["positive_degree"] > 0 else float("nan")),
        axis=1,
    )
    df = df[total_deg > 0].reset_index()
    df = df.merge(nodes.set_index("node_id")[["canonical_name", "node_type"]], left_on="node_id", right_index=True, how="left")
    return df.sort_values("positive_degree", ascending=False)


def structural_balance_check(g_full_signed: nx.Graph) -> dict:
    n_triangles = sum(nx.triangles(g_full_signed).values()) // 3
    result = {"n_triangles_in_signed_subgraph": n_triangles, "threshold_for_claim": MIN_TRIANGLES_FOR_BALANCE_CLAIM}
    if n_triangles < MIN_TRIANGLES_FOR_BALANCE_CLAIM:
        result["status"] = "not_applicable"
        result["reason"] = (
            f"Only {n_triangles} triangles exist among edges with a definite (pozitif/negatif) "
            f"polarity — below the documented threshold of {MIN_TRIANGLES_FOR_BALANCE_CLAIM} needed "
            "to say anything statistically meaningful about structural balance. Reporting a balance "
            "ratio on this few triangles would overstate what a sparse literary network supports."
        )
        return result

    balanced = 0
    unbalanced = 0
    for tri in nx.enumerate_all_cliques(g_full_signed):
        if len(tri) != 3:
            continue
        a, b, c = tri
        signs = []
        for u, v in [(a, b), (b, c), (a, c)]:
            signs.append(g_full_signed[u][v]["sign"])
        product = signs[0] * signs[1] * signs[2]
        if product > 0:
            balanced += 1
        else:
            unbalanced += 1
    result["status"] = "computed"
    result["balanced_triads"] = balanced
    result["unbalanced_triads"] = unbalanced
    result["balanced_fraction"] = balanced / (balanced + unbalanced) if (balanced + unbalanced) else None
    return result


def build_signed_simple_graph(rel: pd.DataFrame) -> nx.Graph:
    signed = rel[rel["polarity"].isin(["pozitif", "negatif"])].dropna(subset=["source_id", "target_id"])
    g = nx.Graph()
    for _, r in signed.iterrows():
        sign = 1 if r["polarity"] == "pozitif" else -1
        u, v = r["source_id"], r["target_id"]
        if g.has_edge(u, v):
            continue  # keep first sign seen; conflicting signs on same pair are rare, noted separately
        g.add_edge(u, v, sign=sign)
    return g


def directed_analysis(g9: nx.DiGraph, nodes: pd.DataFrame) -> dict:
    census = nx.triadic_census(g9)
    out = {"triadic_census": census}
    return out


def main():
    OUT_STATS.mkdir(parents=True, exist_ok=True)
    OUT_TABLES.mkdir(parents=True, exist_ok=True)

    nodes, rel = load_processed()
    graphs = build_all_networks()

    signed_profile = signed_node_profile(rel, nodes)
    signed_profile.to_csv(OUT_TABLES / "signed_network_profile.csv", index=False, encoding="utf-8-sig")
    print("Signed profile top 10 by positive_degree:")
    print(signed_profile[["canonical_name", "positive_degree", "negative_degree", "positive_negative_ratio"]].head(10).to_string(index=False))

    g_signed = build_signed_simple_graph(rel)
    balance = structural_balance_check(g_signed)
    with open(OUT_STATS / "signed_structural_balance.json", "w", encoding="utf-8") as f:
        json.dump(balance, f, ensure_ascii=False, indent=2)
    print("\nStructural balance check:", balance)

    g9 = graphs["G9_directed"]
    dir_result = directed_analysis(g9, nodes)
    with open(OUT_STATS / "directed_triad_census_G9.json", "w", encoding="utf-8") as f:
        json.dump(dir_result, f, ensure_ascii=False, indent=2)
    print("\nTriadic census (G9_directed):", dir_result["triadic_census"])


if __name__ == "__main__":
    main()
