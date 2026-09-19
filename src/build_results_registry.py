"""Results registry (DEC-019): one machine-readable file holding every scientific
value that the website (and the consistency tests) quote, all read from the
pipeline's own outputs. The site generator loads values from here instead of
carrying hand-typed copies, so a number can no longer drift from the analysis.

Output: outputs/results_registry.json  (deterministic: no timestamps).
A value that cannot be derived is stored as null (and the site build refuses to
print a null scientific value) - it is never silently invented.

Pipeline position: after every analysis stage (needs their outputs)."""
import json
import subprocess
import sys
from pathlib import Path

import networkx as nx
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "results_registry.json"
sys.path.insert(0, str(ROOT))


def rd(rel):
    return pd.read_csv(ROOT / rel, encoding="utf-8-sig")


def js(rel):
    with open(ROOT / rel, encoding="utf-8") as f:
        return json.load(f)


def dataset_section():
    nodes = rd("data/processed/nodes.csv")
    rel = rd("data/processed/relations_event_level.csv")
    agg = rd("data/processed/relations_aggregated.csv")
    stories = rd("data/processed/stories.csv")
    tax = rd("data/processed/relation_taxonomy.csv")
    events = rd("data/final/dede_korkut_olaylar_temiz.csv")
    prov = rd("data/processed/provenance.csv")
    prov_counts = {k: int(v) for k, v in prov["source_row_status"].value_counts().items()}
    return {
        "provenance_status_counts": prov_counts,
        "provenance_gap_share": round(prov_counts.get("unmatched_provenance_gap", 0) / len(prov), 4),
        "n_canonical_nodes": int(len(nodes)),
        "node_type_counts": {k: int(v) for k, v in nodes["node_type"].value_counts().items()},
        "n_person_nodes": int((nodes["node_type"] == "kişi").sum()),
        "n_group_nodes": int((nodes["node_type"] == "grup").sum()),
        "n_other_type_nodes": int((~nodes["node_type"].isin(["kişi", "grup"])).sum()),
        "n_relations_event_level": int(len(rel)),
        "n_aggregated_pairs": int(len(agg)),
        "n_stories": int(len(stories)),
        "n_boy_stories": int((stories["section_type"] == "boy").sum()),
        "n_non_boy_sections": int((stories["section_type"] != "boy").sum()),
        "n_narrative_events": int(len(events)),
        "n_relation_layers": int(rel["layer"].nunique()),
        "n_relation_types": int(len(tax)),
        "n_relation_families_top": int(rel["relation_family_top"].nunique()),
        "share_uncertain_relations": round(float((rel["standard_relation"] == "belirsiz").mean()), 4),
        "n_inferred_relations": int((rel["extraction_method"] != "açık_ilişki").sum()),
    }


def networks_section():
    summ = js("outputs/networks/network_summary.json")
    g2 = summ["G2_core_social"]
    return {
        "n_models": int(len(summ)),
        "models": {k: {"n_nodes": v.get("n_nodes"), "n_edges": v.get("n_edges"),
                       "n_components": v.get("n_connected_components", v.get("n_weakly_connected_components")),
                       "largest_component_size": v.get("largest_component_size")} for k, v in summ.items()},
        "g2_core_social": {"n_components": g2.get("n_connected_components"),
                           "giant_component_size": g2.get("largest_component_size"),
                           "n_smaller_components": (g2.get("n_connected_components") - 1) if g2.get("n_connected_components") else None},
    }


def null_models_section():
    fdr = rd("outputs/statistics/null_model_fdr_corrected.csv")
    flag = [c for c in fdr.columns if c.startswith("significant_at_bh_fdr")][0]
    full = js("outputs/null_models/null_model_results_full.json")
    per_metric = {}
    for m, grp in fdr.groupby("metric"):
        per_metric[m] = {"n_tested": int(len(grp)), "n_significant": int(grp[flag].sum()),
                         "significant_networks": sorted(grp[grp[flag]]["network"].tolist())}
    mod = fdr[(fdr["metric"] == "modularity_louvain") & fdr[flag]]
    return {
        "mode": full["mode"], "n_random": full["n_random"], "seed": full["seed"],
        "randomization": "networkx.double_edge_swap on the simple (weight-stripped) graph, 10 x n_edges swap attempts",
        "n_tests": int(len(fdr)), "n_significant": int(fdr[flag].sum()), "fdr_method": "Benjamini-Hochberg", "alpha": 0.05,
        "n_networks_tested": int(fdr["network"].nunique()),
        "per_metric": per_metric,
        "modularity_z_range_significant": [round(float(mod["z_score"].min()), 2), round(float(mod["z_score"].max()), 2)] if len(mod) else None,
        "observed_modularity_procedure": "single Louvain partition (networkx louvain_communities, seed = config seed, weight=None); each randomized graph gets one Louvain run with seed+i",
        "independence_note": "the tested networks are related/nested specifications (e.g. G1 and G2 are subsets/variants of G0); significant results across them are not independent replications",
    }


def sensitivity_section():
    t = rd("outputs/tables/sensitivity_rank_stability.csv")
    pairs = {}
    for pair, grp in t.groupby("pair"):
        rho = {r.metric: float(r.spearman_rho) for r in grp.itertuples()}
        pairs[pair] = {"n_common_nodes": int(grp["n_common_nodes"].iloc[0]), "spearman_rho": rho,
                       "mean_rho": round(float(np.mean(list(rho.values()))), 4), "min_rho": round(float(min(rho.values())), 4),
                       "top10_overlap": {r.metric: float(r.top_10_overlap_fraction) for r in grp.itertuples()}}
    threshold = 0.95
    noticeable = sorted([p for p, v in pairs.items() if v["min_rho"] < threshold], key=lambda p: pairs[p]["mean_rho"])
    negligible = sorted([p for p in pairs if p not in noticeable], key=lambda p: pairs[p]["mean_rho"])
    all_rho = [x for p in pairs.values() for x in p["spearman_rho"].values()]
    lowest = {m: min(pairs, key=lambda p: pairs[p]["spearman_rho"][m]) for m in ("degree", "betweenness", "pagerank")}
    return {
        "betweenness_definition": "weighted betweenness uses distance = 1/tie strength (DEC-017); the 'unweighted' arm (G11) has all strengths 1, i.e. hop-count betweenness",
        "pairs": pairs, "n_pairs": len(pairs),
        "tier_rule": f"'noticeable' = at least one measure with Spearman rho < {threshold}; otherwise 'negligible'",
        "noticeable_pairs": noticeable, "negligible_pairs": negligible,
        "rho_range_noticeable": [round(min(x for p in noticeable for x in pairs[p]["spearman_rho"].values()), 3),
                                 round(max(x for p in noticeable for x in pairs[p]["spearman_rho"].values() if x < 0.9999), 3)] if noticeable else None,
        "min_rho_negligible": round(min(pairs[p]["min_rho"] for p in negligible), 3) if negligible else None,
        "min_rho_overall": round(min(all_rho), 3),
        "lowest_rho_pair_per_metric": lowest,
        "ordering_by_mean_rho_ascending": sorted(pairs, key=lambda p: pairs[p]["mean_rho"]),
        "max_mean_rho_gap_among_noticeable": round(max(pairs[p]["mean_rho"] for p in noticeable) - min(pairs[p]["mean_rho"] for p in noticeable), 4) if noticeable else None,
    }


def robustness_section():
    s = js("outputs/statistics/robustness_summary_G0_full.json")
    return {k: s[k] for k in ("n_nodes", "n_edges", "n_random_trials", "seed", "checkpoint_step_nodes", "denominators",
                              "fraction_removed_below_threshold_of_all_nodes",
                              "fraction_removed_below_threshold_of_initial_giant_component",
                              "degree_targeted_tie_break_sensitivity", "betweenness_targeted_exact_nodes_removed",
                              "betweenness_targeted_ranking")}


def similarity_section():
    t = rd("outputs/tables/publication/T08_story_similarity.csv")
    metrics = ["actor_jaccard", "actor_weighted_jaccard", "actor_cosine", "relation_profile_similarity", "layer_composition_similarity"]
    lead = t.sort_values("actor_jaccard", ascending=False).iloc[0]
    ranks = {m: int((t[m] > lead[m]).sum() + 1) for m in metrics}
    top_pair = {m: f"{t.sort_values(m, ascending=False).iloc[0].story_a}-{t.sort_values(m, ascending=False).iloc[0].story_b}" for m in metrics}
    v = js("outputs/statistics/story_similarity_cluster_validity.json")
    a14, nos1 = v["all_14_stories"], v["sensitivity_excluding_S01"]

    def sil(a):
        return [float(x) for x in a["observed"]["ward"]["silhouette_by_k"].values()]

    def boot(a):
        return [float(x["mean_ari"]) for x in a["bootstrap_stability_ward"]["by_k"].values()]

    disagree = sorted({int(k) for k, d in a14["cross_linkage_agreement_ari"].items() if min(d.values()) < 0.9999})
    return {
        "n_stories": int(pd.concat([t.story_a, t.story_b]).nunique()), "n_pairs": int(len(t)), "n_metrics": len(metrics),
        "actor_jaccard": {"median": round(float(t["actor_jaccard"].median()), 4), "max": round(float(t["actor_jaccard"].max()), 4),
                          "n_zero_pairs": int((t["actor_jaccard"] == 0).sum())},
        "leading_pair_by_actor_jaccard": f"{lead.story_a}-{lead.story_b}",
        "leading_pair_rank_per_metric": ranks, "top_pair_per_metric": top_pair,
        "cluster_validity": {
            "verdict_all_14": a14["verdict_discrete_clusters"], "verdict_excluding_S01": nos1["verdict_discrete_clusters"],
            "silhouette_range_all_k_both_analyses": [round(min(sil(a14) + sil(nos1)), 2), round(max(sil(a14) + sil(nos1)), 2)],
            "bootstrap_ari_range_both_analyses": [round(min(boot(a14) + boot(nos1)), 2), round(max(boot(a14) + boot(nos1)), 2)],
            "ward_cophenetic_correlation_all_14": a14["observed"]["ward"]["cophenetic_correlation"],
            "k_where_linkage_methods_disagree": disagree,
            "pre_set_rule": v["verdict_rule"],
        },
    }


def pipeline_section():
    import run_pipeline
    n_tests = None
    try:
        r = subprocess.run([sys.executable, "-m", "pytest", "--collect-only", "-q", "-p", "no:cacheprovider", "tests"],
                           cwd=str(ROOT), capture_output=True, text=True, timeout=180)
        n_tests = sum(1 for line in r.stdout.splitlines() if "::" in line) or None
    except Exception:
        n_tests = None
    return {"n_stages": len(run_pipeline.STAGES), "stage_names": run_pipeline.STAGE_NAMES,
            "n_tests_collected": n_tests,
            "test_count_note": "collected test functions; whether they pass is reported by pytest / CI, not by this registry"}


def main():
    reg = {
        "purpose": "Single source for scientific values quoted by the website and checked by tests (DEC-019). Generated; do not edit.",
        "dataset": dataset_section(),
        "networks": networks_section(),
        "null_models": null_models_section(),
        "sensitivity": sensitivity_section(),
        "robustness": robustness_section(),
        "story_similarity": similarity_section(),
        "composite_nodes": js("outputs/statistics/composite_node_summary.json"),
        "pipeline": pipeline_section(),
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(reg, f, ensure_ascii=False, indent=2)
    print(f"Wrote {OUT.relative_to(ROOT)}")
    print("dataset:", reg["dataset"]["n_canonical_nodes"], "nodes |", reg["null_models"]["n_significant"], "/", reg["null_models"]["n_tests"],
          "significant |", reg["pipeline"]["n_stages"], "stages |", reg["pipeline"]["n_tests_collected"], "tests collected")


if __name__ == "__main__":
    main()
