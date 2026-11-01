"""Phase 6 (cont.): multilayer/multiplex analysis (section 23).

Layers are the observed `katman` values (olay, iletişim, çatışma, akrabalık,
otorite, mekân, kimlik) from relations_event_level.csv. For each node:
degree and strength per layer, number of active layers, a participation
coefficient across layers (same formula family as the community
participation coefficient), and a Shannon-entropy-based cross-layer
diversity score (0 = all activity in one layer, higher = spread evenly
across layers)."""
import math
from pathlib import Path

import pandas as pd

from networks import load_processed

ROOT = Path(__file__).resolve().parents[1]
OUT_TABLES = ROOT / "outputs" / "tables"


def per_node_layer_degree(rel: pd.DataFrame) -> pd.DataFrame:
    long = pd.concat([
        rel[["source_id", "layer", "weight"]].rename(columns={"source_id": "node_id"}),
        rel[["target_id", "layer", "weight"]].rename(columns={"target_id": "node_id"}),
    ]).dropna(subset=["node_id", "layer"])

    degree = long.groupby(["node_id", "layer"]).size().unstack(fill_value=0)
    degree.columns = [f"degree__{c}" for c in degree.columns]

    w = long.copy()
    w["weight"] = pd.to_numeric(w["weight"], errors="coerce").fillna(0)
    strength = w.groupby(["node_id", "layer"])["weight"].sum().unstack(fill_value=0)
    strength.columns = [f"strength__{c}" for c in strength.columns]

    return degree.join(strength, how="outer").fillna(0)


def layer_participation_and_versatility(degree_wide: pd.DataFrame, layer_names: list) -> pd.DataFrame:
    deg_cols = [f"degree__{layer}" for layer in layer_names if f"degree__{layer}" in degree_wide.columns]
    sub = degree_wide[deg_cols]
    total = sub.sum(axis=1)

    n_active_layers = (sub > 0).sum(axis=1)

    def participation(row):
        t = row.sum()
        if t == 0:
            return None
        return 1 - sum((v / t) ** 2 for v in row)

    def entropy(row):
        t = row.sum()
        if t == 0:
            return None
        probs = [v / t for v in row if v > 0]
        return -sum(p * math.log(p) for p in probs)

    result = pd.DataFrame({
        "total_degree_across_layers": total,
        "n_active_layers": n_active_layers,
        "layer_participation_coefficient": sub.apply(participation, axis=1),
        "cross_layer_entropy": sub.apply(entropy, axis=1),
    })
    return result


def main():
    OUT_TABLES.mkdir(parents=True, exist_ok=True)
    nodes, rel = load_processed()

    layer_names = sorted(rel["layer"].dropna().unique())
    print("Observed layers:", layer_names)

    degree_wide = per_node_layer_degree(rel)
    versatility = layer_participation_and_versatility(degree_wide, layer_names)

    out = degree_wide.join(versatility, how="outer")
    out = out.merge(nodes.set_index("node_id")[["canonical_name", "node_type", "story_count"]],
                     left_index=True, right_index=True, how="left")
    out = out.reset_index().rename(columns={"index": "node_id"})
    out.to_csv(OUT_TABLES / "multilayer_profile.csv", index=False, encoding="utf-8-sig")

    print(f"\n{len(out)} nodes with at least one layer-tagged relation")
    top_versatile = out.sort_values("n_active_layers", ascending=False).head(10)
    print("\nTop 10 by number of active layers:")
    print(top_versatile[["canonical_name", "n_active_layers", "layer_participation_coefficient", "total_degree_across_layers"]].to_string(index=False))


if __name__ == "__main__":
    main()
