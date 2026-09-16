"""Phase 7: null models / statistical validation (section 28).

Degree-preserving randomization (double-edge-swap configuration-model
style) is applied to each primary network variant. For each network we
compare the OBSERVED value of a structural statistic against the
distribution of that statistic across the random ensemble: random_mean,
random_std, z_score, percentile, empirical_p.

DEC-008 (recorded in docs/decision_log.md): randomization method is
networkx's `double_edge_swap` applied to a simple (weight-stripped) copy of
each undirected graph, run for `n_swaps = 10 * n_edges` per randomization
(a common rule-of-thumb for adequate mixing), independently for each of the
`n_random` ensemble members. This preserves the exact degree sequence
(configuration-model equivalent for simple graphs) without the
self-loop/multi-edge bookkeeping networkx's `configuration_model` needs for
projection back to a simple graph.

FAST mode (env var NULL_MODEL_FAST=1, or --fast CLI flag) uses a small
n_random for iteration; FULL mode uses config/analysis.yaml's
null_models.n_random (1000) for the numbers that go into the report.
"""
import argparse
import json
from pathlib import Path

import networkx as nx
import numpy as np
import pandas as pd
import yaml

from networks import build_all_networks

ROOT = Path(__file__).resolve().parents[1]
OUT_STATS = ROOT / "outputs" / "statistics"
OUT_NULL = ROOT / "outputs" / "null_models"

with open(ROOT / "config" / "analysis.yaml", encoding="utf-8") as f:
    CONFIG = yaml.safe_load(f)

SEED = CONFIG["seed"]
N_RANDOM_FULL = CONFIG["null_models"]["n_random"]

# Networks small/sparse enough that a null-model comparison is judged
# unreliable are explicitly excluded with a stated reason, rather than
# forcing a z-score out of a degenerate distribution (see also Phase 6's
# precedent with the 13-triangle signed-balance case).
MIN_EDGES_FOR_NULL_COMPARISON = 20

TARGET_NETWORKS = ["G0_full", "G1_person_only", "G2_core_social", "G3_kinship",
                   "G4_communication", "G5_cooperation_support", "G6_conflict",
                   "G7_positive", "G8_negative"]


def randomized_copy(g: nx.Graph, rng: np.random.Generator) -> nx.Graph:
    h = nx.Graph()
    h.add_nodes_from(g.nodes())
    h.add_edges_from(g.edges())
    m = h.number_of_edges()
    if m < 2:
        return h
    n_swaps = max(1, 10 * m)
    seed_int = int(rng.integers(0, 2**31 - 1))
    try:
        nx.double_edge_swap(h, nswap=n_swaps, max_tries=n_swaps * 20, seed=seed_int)
    except nx.NetworkXAlgorithmError:
        pass  # graph too constrained to complete all swaps; keep partial result, still degree-preserving attempts
    return h


def observed_stats(g: nx.Graph) -> dict:
    n = g.number_of_nodes()
    stats = {
        "clustering": nx.average_clustering(g) if n > 2 else None,
        "transitivity": nx.transitivity(g),
    }
    try:
        stats["degree_assortativity"] = nx.degree_assortativity_coefficient(g)
    except Exception:
        stats["degree_assortativity"] = None
    return stats


def modularity_for_graph(g: nx.Graph, seed: int) -> float:
    communities = nx.algorithms.community.louvain_communities(g, weight=None, seed=seed)
    return nx.algorithms.community.modularity(g, communities, weight=None)


def z_and_percentile(observed: float, random_values: np.ndarray) -> dict:
    random_values = random_values[~np.isnan(random_values)]
    if len(random_values) == 0:
        return {"random_mean": None, "random_std": None, "z_score": None, "percentile": None, "empirical_p": None}
    mean = float(np.mean(random_values))
    std = float(np.std(random_values))
    z = (observed - mean) / std if std > 0 else None
    percentile = float((random_values < observed).mean() * 100)
    n = len(random_values)
    n_as_extreme = int(np.sum(np.abs(random_values - mean) >= abs(observed - mean)))
    empirical_p = (n_as_extreme + 1) / (n + 1)  # add-one smoothing, standard for permutation p-values
    return {"random_mean": mean, "random_std": std, "z_score": z, "percentile": percentile, "empirical_p": empirical_p}


def run_null_model_for_network(name: str, g: nx.Graph, n_random: int, seed: int) -> dict:
    m = g.number_of_edges()
    if m < MIN_EDGES_FOR_NULL_COMPARISON:
        return {
            "network": name, "n_nodes": g.number_of_nodes(), "n_edges": m,
            "status": "not_applicable",
            "reason": f"only {m} edges (< {MIN_EDGES_FOR_NULL_COMPARISON}) - a randomized ensemble "
                      f"this small would not support a meaningful null distribution",
        }

    obs = observed_stats(g)
    obs_modularity = modularity_for_graph(g, seed=seed)

    rng = np.random.default_rng(seed)
    random_clustering, random_transitivity, random_assort, random_modularity = [], [], [], []
    for i in range(n_random):
        h = randomized_copy(g, rng)
        s = observed_stats(h)
        random_clustering.append(s["clustering"] if s["clustering"] is not None else np.nan)
        random_transitivity.append(s["transitivity"] if s["transitivity"] is not None else np.nan)
        random_assort.append(s["degree_assortativity"] if s["degree_assortativity"] is not None else np.nan)
        random_modularity.append(modularity_for_graph(h, seed=seed + i))

    result = {
        "network": name, "n_nodes": g.number_of_nodes(), "n_edges": m,
        "status": "computed", "n_random": n_random, "seed": seed,
        "metrics": {
            "clustering": {"observed": obs["clustering"], **z_and_percentile(obs["clustering"], np.array(random_clustering))},
            "transitivity": {"observed": obs["transitivity"], **z_and_percentile(obs["transitivity"], np.array(random_transitivity))},
            "degree_assortativity": {"observed": obs["degree_assortativity"], **z_and_percentile(obs["degree_assortativity"], np.array(random_assort))},
            "modularity_louvain": {"observed": obs_modularity, **z_and_percentile(obs_modularity, np.array(random_modularity))},
        },
    }
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--fast", action="store_true", help="use a small n_random for development")
    parser.add_argument("--n-random", type=int, default=None, help="override n_random explicitly")
    args = parser.parse_args()

    if args.n_random is not None:
        n_random = args.n_random
        mode = f"custom(n_random={n_random})"
    elif args.fast:
        n_random = 100
        mode = "fast"
    else:
        n_random = N_RANDOM_FULL
        mode = "full"

    OUT_STATS.mkdir(parents=True, exist_ok=True)
    OUT_NULL.mkdir(parents=True, exist_ok=True)

    graphs = build_all_networks()
    results = {}
    for name in TARGET_NETWORKS:
        print(f"Running null model for {name} (n_random={n_random})...")
        res = run_null_model_for_network(name, graphs[name], n_random=n_random, seed=SEED)
        results[name] = res
        if res["status"] == "computed":
            for metric, vals in res["metrics"].items():
                print(f"  {metric}: observed={vals['observed']}, z={vals['z_score']}, p={vals['empirical_p']}")
        else:
            print(f"  {res['status']}: {res['reason']}")

    out_path = OUT_NULL / f"null_model_results_{mode}.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({"mode": mode, "n_random": n_random, "seed": SEED, "results": results}, f, ensure_ascii=False, indent=2, default=str)
    print(f"\nWrote {out_path}")

    if mode == "full":
        with open(OUT_STATS / "null_model_summary.json", "w", encoding="utf-8") as f:
            json.dump({"mode": mode, "n_random": n_random, "seed": SEED, "results": results}, f, ensure_ascii=False, indent=2, default=str)


if __name__ == "__main__":
    main()
