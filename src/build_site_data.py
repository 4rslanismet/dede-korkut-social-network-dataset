"""Phase 15: export machine-readable JSON for the GitHub Pages site
(section 68, 108-109). Every number the site displays must trace back to
this script reading real output files (above all outputs/results_registry.json)
- nothing scientific is hardcoded here or in the site's HTML/JS (DEC-019).
A value the registry cannot supply makes this script fail rather than guess.
"""
import json
from pathlib import Path

import networkx as nx
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DOCS_DATA = ROOT / "docs" / "data"


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def build_project_summary():
    nodes = pd.read_csv(ROOT / "data" / "processed" / "nodes.csv", encoding="utf-8-sig")
    rel = pd.read_csv(ROOT / "data" / "processed" / "relations_event_level.csv", encoding="utf-8-sig")
    stories = pd.read_csv(ROOT / "data" / "processed" / "stories.csv", encoding="utf-8-sig")
    events = pd.read_csv(ROOT / "data" / "final" / "dede_korkut_olaylar_temiz.csv", encoding="utf-8-sig")
    val_summary = load_json(ROOT / "outputs" / "validation" / "summary.json")
    corpus_metrics = pd.read_csv(ROOT / "outputs" / "statistics" / "corpus_network_metrics.csv", encoding="utf-8-sig")
    community_summary = load_json(ROOT / "outputs" / "statistics" / "community_summary_G2_core_social.json")

    n_layers = rel["layer"].nunique()

    # PASS/WARNING/FAIL rubric consistent with reports/02_data_quality_report.md:
    # FAIL-level checks are integrity violations (missing/orphan/invalid/duplicate);
    # everything else flagged (self-loops, alias conflicts, etc.) is WARNING-level.
    fail_level_keys = {"missing_source", "missing_target", "orphan_source_endpoint", "orphan_target_endpoint",
                        "invalid_layer", "invalid_polarity", "invalid_weight", "invalid_directionality",
                        "duplicate_node_id", "duplicate_kayit_id", "missing_actor", "orphan_actor",
                        "unsupported_target", "empty_or_blank_node_name", "invalid_id_format"}
    n_fail = sum(v for cat in val_summary.values() for k, v in cat.items() if k in fail_level_keys)
    n_warning = sum(v for cat in val_summary.values() for k, v in cat.items()
                     if k not in fail_level_keys and not k.startswith("_") and isinstance(v, int))
    validation_status = "FAIL" if n_fail > 0 else ("WARNING" if n_warning > 0 else "PASS")

    g0 = corpus_metrics[corpus_metrics["network"] == "G0_full"].iloc[0]

    registry_path = ROOT / "outputs" / "results_registry.json"
    if not registry_path.exists():
        raise SystemExit("outputs/results_registry.json is missing - run `python run_pipeline.py --stage results_registry` first")
    reg = load_json(registry_path)
    pipe = reg["pipeline"]
    g2 = reg["networks"]["g2_core_social"]
    for name, val in (("pipeline.n_stages", pipe["n_stages"]), ("networks.n_models", reg["networks"]["n_models"]),
                      ("networks.g2_core_social.n_components", g2["n_components"])):
        if val is None:
            raise SystemExit(f"required registry value '{name}' is null/unavailable")

    return {
        "generated_from": "src/build_site_data.py (Phase 15)",
        "dataset": {
            "stories": int(len(stories)),
            "actors": int(len(nodes)),
            "relations_event_level": int(len(rel)),
            "narrative_events": int(len(events)),
            "relation_layers": int(n_layers),
        },
        "validation_status": {
            "status": validation_status,
            "fail_level_issue_count": int(n_fail),
            "warning_level_issue_count": int(n_warning),
            "detail_source": "outputs/validation/summary.json",
        },
        "corpus_network_g0": {
            "nodes": int(g0["n_nodes"]), "edges": int(g0["n_edges"]),
            "density": round(float(g0["density"]), 4),
            "connected_components": int(g0["n_connected_components"]),
        },
        "community_detection": {
            "network": community_summary["network"],
            "leiden_modularity": round(community_summary["leiden_modularity_res1.0_seed42"], 4),
            "leiden_n_communities": community_summary["leiden_n_communities_res1.0_seed42"],
            "caveat": f"G2_core_social has {g2['n_components']} connected components; the raw community count is "
                      "partly inflated by trivial isolated-component partitions - see Methodology.",
        },
        "pipeline": {
            "n_stages": pipe["n_stages"],
            "n_network_models": reg["networks"]["n_models"],
            "n_tests_collected": pipe["n_tests_collected"],
        },
    }


def build_actor_metrics():
    nodes = pd.read_csv(ROOT / "data" / "processed" / "nodes.csv", encoding="utf-8-sig")
    cent = pd.read_csv(ROOT / "outputs" / "tables" / "centrality_G0_full.csv", encoding="utf-8-sig")
    ml = pd.read_csv(ROOT / "outputs" / "tables" / "multilayer_profile.csv", encoding="utf-8-sig")
    comm = pd.read_csv(ROOT / "outputs" / "tables" / "community_membership_G2_core_social.csv", encoding="utf-8-sig")

    df = nodes.merge(cent[["node_id", "degree", "strength_weighted_degree", "betweenness", "pagerank"]],
                      on="node_id", how="left")
    df = df.merge(ml[["node_id", "n_active_layers", "layer_participation_coefficient"]], on="node_id", how="left")
    df = df.merge(comm[["node_id", "leiden_community"]], on="node_id", how="left")
    df = df.where(pd.notna(df), None)

    records = df.to_dict("records")
    return {r["node_id"]: r for r in records}


def build_story_metrics():
    # Two different "edge" counts must stay distinguishable (DEC-019): stories.csv counts raw relation
    # RECORDS; story_level_metrics.csv counts edges of the AGGREGATED story graph, and its density /
    # average degree / centralization are computed on that graph.
    stories = pd.read_csv(ROOT / "data" / "processed" / "stories.csv", encoding="utf-8-sig").rename(columns={"n_edges": "n_relation_records"})
    metrics = pd.read_csv(ROOT / "data" / "derived" / "story_level_metrics.csv", encoding="utf-8-sig").rename(columns={"n_edges": "n_edges_aggregated"})
    df = stories.merge(metrics.drop(columns=["boy_name_raw"], errors="ignore"), on=["story_id", "source_file"], how="left", validate="one_to_one")
    df = df.where(pd.notna(df), None)
    return {r["story_id"]: r for r in df.to_dict("records")}


def build_network_summary():
    return load_json(ROOT / "outputs" / "networks" / "network_summary.json")


def build_cytoscape_json(network_name: str):
    edges = pd.read_csv(ROOT / "outputs" / "networks" / f"{network_name}_edges.csv", encoding="utf-8-sig")
    nodes_df = pd.read_csv(ROOT / "outputs" / "networks" / f"{network_name}_nodes.csv", encoding="utf-8-sig")

    elements = []
    for _, r in nodes_df.iterrows():
        elements.append({"data": {
            "id": str(r["node_id"]),
            "label": r.get("canonical_name", r["node_id"]),
            "node_type": r.get("node_type"),
            "story_count": r.get("story_count"),
        }})
    for _, r in edges.iterrows():
        elements.append({"data": {
            "source": str(r["source"]), "target": str(r["target"]),
            "weight": float(r["weight"]), "interaction_count": int(r["interaction_count"]),
        }})
    return {"elements": elements}


def main():
    DOCS_DATA.mkdir(parents=True, exist_ok=True)

    def write(name, obj):
        path = DOCS_DATA / name
        with open(path, "w", encoding="utf-8") as f:
            json.dump(obj, f, ensure_ascii=False, indent=2, default=str)
        print(f"Wrote {path} ({path.stat().st_size} bytes)")

    write("project_summary.json", build_project_summary())
    write("actor_metrics.json", build_actor_metrics())
    write("story_metrics.json", build_story_metrics())
    write("network_summary.json", build_network_summary())

    (DOCS_DATA / "networks").mkdir(parents=True, exist_ok=True)
    for net in ["G0_full", "G1_person_only", "G2_core_social"]:
        with open(DOCS_DATA / "networks" / f"{net}.json", "w", encoding="utf-8") as f:
            json.dump(build_cytoscape_json(net), f, ensure_ascii=False, default=str)
        print(f"Wrote docs/data/networks/{net}.json")


if __name__ == "__main__":
    main()
