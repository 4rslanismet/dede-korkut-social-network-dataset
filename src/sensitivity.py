"""Phase 8: sensitivity analysis (sections 29-30, 34-36).

Six paired network-construction choices are compared (matching
config/analysis.yaml::sensitivity.variants, 12 entries = 6 pairs). Three
pairs reuse G0-G11 variants already built in src/networks.py; three are new
filters built here with the same aggregation logic. For each pair we compare
centrality rankings (degree, betweenness, pagerank) via Spearman rho,
Kendall's tau, and top-k overlap (k=10, k=20) on the actor set common to
both variants — this is the standard way to ask "how much does this
modeling choice change who looks central," not whether either variant is
'more correct'."""
import json
from pathlib import Path

import networkx as nx
import pandas as pd
from scipy.stats import kendalltau, spearmanr

from networks import build_all_networks, load_processed, _aggregate_undirected
from metrics import centrality_profile

ROOT = Path(__file__).resolve().parents[1]
OUT_STATS = ROOT / "outputs" / "statistics"
OUT_TABLES = ROOT / "outputs" / "tables"


def build_filtered_graph(rel_subset: pd.DataFrame, nodes: pd.DataFrame, name: str) -> nx.Graph:
    subset = rel_subset.dropna(subset=["source_id", "target_id"])
    agg = _aggregate_undirected(subset)
    g = nx.Graph(name=name)
    g.add_nodes_from(nodes["node_id"])
    for _, r in agg.iterrows():
        g.add_edge(r["source"], r["target"], weight=float(r["weight"]), interaction_count=int(r["interaction_count"]))
    attrs = nodes.set_index("node_id")[["canonical_name", "node_type", "story_count"]].to_dict("index")
    nx.set_node_attributes(g, attrs)
    g.remove_nodes_from(list(nx.isolates(g)))
    return g


def build_sensitivity_pairs(nodes: pd.DataFrame, rel: pd.DataFrame, base_graphs: dict) -> dict:
    explicit_only_rel = rel[rel["extraction_method"] == "açık_ilişki"]
    explicit_only_g = build_filtered_graph(explicit_only_rel, nodes, "explicit_only")

    groups_excluded_rel = rel[(rel["source_type"] != "grup") & (rel["target_type"] != "grup")]
    groups_excluded_g = build_filtered_graph(groups_excluded_rel, nodes, "groups_excluded")

    girizgah_excluded_rel = rel[rel["story_id"] != "S01"]
    girizgah_excluded_g = build_filtered_graph(girizgah_excluded_rel, nodes, "girizgah_excluded")

    return {
        "person_plus_group_vs_person_only": {
            "a_label": "person_plus_group", "a_graph": base_graphs["G0_full"],
            "b_label": "person_only", "b_graph": base_graphs["G1_person_only"],
            "description": "All actor types (G0_full) vs. kişi-only endpoints (G1_person_only).",
        },
        "weighted_vs_unweighted": {
            "a_label": "weighted", "a_graph": base_graphs["G10_weighted"],
            "b_label": "unweighted", "b_graph": base_graphs["G11_unweighted"],
            "description": "Same edge set; G10 uses agirlik (1-5) as weight, G11 forces weight=1. "
                            "Centrality measures that ignore weight (plain degree) are identical by "
                            "construction - only weighted measures (strength, weighted betweenness/"
                            "PageRank) can differ here.",
        },
        "all_relations_vs_core_social": {
            "a_label": "all_relations", "a_graph": base_graphs["G0_full"],
            "b_label": "core_social_only", "b_graph": base_graphs["G2_core_social"],
            "description": "All relations (G0_full) vs. SEMANTIC/identity relations excluded (G2_core_social).",
        },
        "explicit_only_vs_explicit_plus_inferred": {
            "a_label": "explicit_only", "a_graph": explicit_only_g,
            "b_label": "explicit_plus_inferred", "b_graph": base_graphs["G0_full"],
            "description": f"Only cikarma_yontemi=='açık_ilişki' rows ({len(explicit_only_rel)}/{len(rel)}) "
                            f"vs. all rows including inferred relations (G0_full).",
        },
        "groups_included_vs_excluded": {
            "a_label": "groups_included", "a_graph": base_graphs["G0_full"],
            "b_label": "groups_excluded", "b_graph": groups_excluded_g,
            "description": "G0_full vs. relations where neither endpoint is node_type=='grup' "
                            "(kişi + mitolojik/ilahi + hayvan + nesne/doğa + yer/coğrafya kept).",
        },
        "girizgah_included_vs_excluded": {
            "a_label": "girizgah_included", "a_graph": base_graphs["G0_full"],
            "b_label": "girizgah_excluded", "b_graph": girizgah_excluded_g,
            "description": "G0_full vs. story_id != 'S01' (girizgah has only 1 relation record; "
                            "practical effect on rankings expected to be minimal but tested, not assumed).",
        },
    }


def compare_pair(pair_name: str, spec: dict, nodes: pd.DataFrame) -> dict:
    prof_a = centrality_profile(spec["a_label"], spec["a_graph"], nodes).set_index("node_id")
    prof_b = centrality_profile(spec["b_label"], spec["b_graph"], nodes).set_index("node_id")

    common = prof_a.index.intersection(prof_b.index)
    result = {
        "pair": pair_name, "description": spec["description"],
        "n_nodes_a": len(prof_a), "n_nodes_b": len(prof_b), "n_common_nodes": len(common),
    }

    if len(common) < 5:
        result["status"] = "not_applicable"
        result["reason"] = f"only {len(common)} nodes in common - too few for a meaningful rank correlation"
        return result

    result["status"] = "computed"
    result["metrics"] = {}
    for metric in ["degree", "betweenness", "pagerank"]:
        a_vals = prof_a.loc[common, metric]
        b_vals = prof_b.loc[common, metric]
        rho, rho_p = spearmanr(a_vals, b_vals)
        tau, tau_p = kendalltau(a_vals, b_vals)

        overlaps = {}
        for k in (10, 20):
            k_eff = min(k, len(common))
            top_a = set(prof_a.loc[common, metric].sort_values(ascending=False).head(k_eff).index)
            top_b = set(prof_b.loc[common, metric].sort_values(ascending=False).head(k_eff).index)
            overlaps[f"top_{k}_overlap_fraction"] = len(top_a & top_b) / k_eff

        result["metrics"][metric] = {
            "spearman_rho": rho, "spearman_p": rho_p,
            "kendall_tau": tau, "kendall_p": tau_p,
            **overlaps,
        }
    return result


def main():
    OUT_STATS.mkdir(parents=True, exist_ok=True)
    OUT_TABLES.mkdir(parents=True, exist_ok=True)

    nodes, rel = load_processed()
    base_graphs = build_all_networks()
    pairs = build_sensitivity_pairs(nodes, rel, base_graphs)

    results = {}
    rows = []
    for pair_name, spec in pairs.items():
        res = compare_pair(pair_name, spec, nodes)
        results[pair_name] = res
        print(f"\n{pair_name}: {spec['description']}")
        if res["status"] == "not_applicable":
            print(f"  NOT_APPLICABLE: {res['reason']}")
            continue
        for metric, vals in res["metrics"].items():
            print(f"  {metric}: spearman={vals['spearman_rho']:.3f} kendall={vals['kendall_tau']:.3f} "
                  f"top10_overlap={vals['top_10_overlap_fraction']:.2f} top20_overlap={vals['top_20_overlap_fraction']:.2f}")
            rows.append({
                "pair": pair_name, "metric": metric, "n_common_nodes": res["n_common_nodes"],
                "spearman_rho": vals["spearman_rho"], "spearman_p": vals["spearman_p"],
                "kendall_tau": vals["kendall_tau"], "kendall_p": vals["kendall_p"],
                "top_10_overlap_fraction": vals["top_10_overlap_fraction"],
                "top_20_overlap_fraction": vals["top_20_overlap_fraction"],
            })

    with open(OUT_STATS / "sensitivity_analysis_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2, default=str)

    pd.DataFrame(rows).to_csv(OUT_TABLES / "sensitivity_rank_stability.csv", index=False, encoding="utf-8-sig")
    print("\nWrote outputs/statistics/sensitivity_analysis_results.json and outputs/tables/sensitivity_rank_stability.csv")


if __name__ == "__main__":
    main()
