"""Phase 8 (cont.): structural robustness (sections 30-31).

Explicitly named 'structural robustness', never 'narrative resilience' (the
project brief's own naming rule, section 31) - these curves describe graph
connectivity under node removal, not a claim about the narrative's
resilience to anything.

Three removal strategies on G0_full: random (averaged over
config::robustness.n_random_trials independent runs), highest-degree-first,
highest-betweenness-first. Degree ranking is recomputed after every removal
(adaptive, not a static one-shot ranking); betweenness ranking is recomputed
only every n/20 removals (~15 for G0_full) for cost. Curves report the
largest component relative to the ORIGINAL NODE COUNT (not the original giant
component), at checkpoints of 2% of nodes (6 for G0_full)."""
import json
from pathlib import Path

import networkx as nx
import numpy as np
import pandas as pd
import yaml

from networks import build_all_networks

ROOT = Path(__file__).resolve().parents[1]
OUT_STATS = ROOT / "outputs" / "statistics"

with open(ROOT / "config" / "analysis.yaml", encoding="utf-8") as f:
    CONFIG = yaml.safe_load(f)

SEED = CONFIG["seed"]
N_RANDOM_TRIALS = CONFIG["robustness"]["n_random_trials"]
STEP_FRACTION = 0.02  # remove 2% of original nodes per step


def curve_for_order(g: nx.Graph, removal_order: list) -> list[dict]:
    h = g.copy()
    n0 = h.number_of_nodes()
    step = max(1, int(round(n0 * STEP_FRACTION)))
    rows = []

    def snapshot(n_removed):
        if h.number_of_nodes() == 0:
            rows.append({"n_removed": n_removed, "fraction_removed": n_removed / n0,
                         "largest_component_size": 0, "n_components": 0, "largest_component_fraction": 0.0})
            return
        comps = list(nx.connected_components(h))
        largest = max(len(c) for c in comps)
        rows.append({
            "n_removed": n_removed, "fraction_removed": n_removed / n0,
            "largest_component_size": largest, "n_components": len(comps),
            "largest_component_fraction": largest / n0,
        })

    snapshot(0)
    removed = 0
    for node in removal_order:
        if node not in h:
            continue
        h.remove_node(node)
        removed += 1
        if removed % step == 0:
            snapshot(removed)
    if removed % step != 0:
        snapshot(removed)
    return rows


def random_removal_curve(g: nx.Graph, seed: int) -> pd.DataFrame:
    n0 = g.number_of_nodes()
    step = max(1, int(round(n0 * STEP_FRACTION)))
    checkpoints = list(range(0, n0 + 1, step))
    if checkpoints[-1] != n0:
        checkpoints.append(n0)

    all_trials = np.zeros((N_RANDOM_TRIALS, len(checkpoints)))
    rng = np.random.default_rng(seed)
    nodes_list = list(g.nodes())

    for trial in range(N_RANDOM_TRIALS):
        order = rng.permutation(nodes_list).tolist()
        h = g.copy()
        cp_idx = 0
        largest = n0
        for i, cp in enumerate(checkpoints):
            while h.number_of_nodes() > n0 - cp:
                node = order.pop()
                h.remove_node(node)
            largest = max((len(c) for c in nx.connected_components(h)), default=0)
            all_trials[trial, i] = largest

    mean_largest = all_trials.mean(axis=0)
    std_largest = all_trials.std(axis=0)
    return pd.DataFrame({
        "n_removed": checkpoints,
        "fraction_removed": [c / n0 for c in checkpoints],
        "largest_component_size_mean": mean_largest,
        "largest_component_size_std": std_largest,
        "largest_component_fraction_mean": mean_largest / n0,
    })


def degree_targeted_order(g: nx.Graph) -> list:
    h = g.copy()
    order = []
    while h.number_of_nodes() > 0:
        node = max(h.degree(), key=lambda x: x[1])[0]
        order.append(node)
        h.remove_node(node)
    return order


def betweenness_targeted_order(g: nx.Graph) -> list:
    h = g.copy()
    order = []
    recompute_every = max(1, h.number_of_nodes() // 20)  # recompute betweenness ~20 times, not every single step (cost)
    bc = nx.betweenness_centrality(h)
    count = 0
    while h.number_of_nodes() > 0:
        node = max(bc, key=bc.get)
        order.append(node)
        h.remove_node(node)
        del bc[node]
        count += 1
        if h.number_of_nodes() > 0 and count % recompute_every == 0:
            bc = nx.betweenness_centrality(h)
    return order


def main():
    OUT_STATS.mkdir(parents=True, exist_ok=True)
    graphs = build_all_networks()
    g = graphs["G0_full"]
    print(f"Structural robustness on G0_full: {g.number_of_nodes()} nodes, {g.number_of_edges()} edges")

    print(f"Random removal ({N_RANDOM_TRIALS} trials, seed={SEED})...")
    random_df = random_removal_curve(g, seed=SEED)

    print("Degree-targeted removal (recomputed after each removal)...")
    degree_order = degree_targeted_order(g)
    degree_rows = curve_for_order(g, degree_order)
    degree_df = pd.DataFrame(degree_rows)

    print("Betweenness-targeted removal (unweighted hop-count betweenness, recomputed periodically)...")
    betweenness_order = betweenness_targeted_order(g)
    betweenness_rows = curve_for_order(g, betweenness_order)
    betweenness_df = pd.DataFrame(betweenness_rows)

    random_df.to_csv(OUT_STATS / "robustness_random_removal_G0_full.csv", index=False, encoding="utf-8-sig")
    degree_df.to_csv(OUT_STATS / "robustness_degree_targeted_removal_G0_full.csv", index=False, encoding="utf-8-sig")
    betweenness_df.to_csv(OUT_STATS / "robustness_betweenness_targeted_removal_G0_full.csv", index=False, encoding="utf-8-sig")

    # The largest connected component (LCC) can be compared with TWO different
    # denominators, and they answer different questions - they are reported
    # separately and labelled, never mixed (review finding, DEC-019):
    #   all_nodes              LCC size < X% of ALL G0 nodes (n0)
    #   initial_giant_component LCC size < X% of the INITIAL giant component (size at 0 removed)
    n0 = g.number_of_nodes()
    giant0 = int(degree_df["largest_component_size"].iloc[0])

    def fraction_below(df, size_col, denominator, threshold):
        below = df[df[size_col] < threshold * denominator]
        return float(below["fraction_removed"].iloc[0]) if len(below) else None

    def thresholds_for(denominator):
        out = {}
        for label, thr in (("50pct", 0.5), ("10pct", 0.1)):
            out[label] = {
                "random": fraction_below(random_df, "largest_component_size_mean", denominator, thr),
                "degree_targeted": fraction_below(degree_df, "largest_component_size", denominator, thr),
                "betweenness_targeted": fraction_below(betweenness_df, "largest_component_size", denominator, thr),
            }
        return out

    # Tie-break sensitivity of degree-targeted removal: many nodes share the same
    # degree, so "highest degree first" is not uniquely defined. Re-run the adaptive
    # attack with random tie-break orders (seeded) and record how many removals are
    # needed to cross each threshold (exact, checked after every single removal).
    def degree_attack_crossings(rng_):
        rank = {n: i for i, n in enumerate(rng_.permutation(list(g.nodes())))}
        h = g.copy()
        crossed = {}
        removed = 0
        targets = {("all_nodes", "50pct"): 0.5 * n0, ("all_nodes", "10pct"): 0.1 * n0,
                   ("initial_giant_component", "50pct"): 0.5 * giant0, ("initial_giant_component", "10pct"): 0.1 * giant0}
        while h.number_of_nodes() > 0 and len(crossed) < len(targets):
            v = max(h.degree(), key=lambda x: (x[1], -rank[x[0]]))[0]
            h.remove_node(v)
            removed += 1
            size = max((len(c) for c in nx.connected_components(h)), default=0)
            for key, lim in targets.items():
                if key not in crossed and size < lim:
                    crossed[key] = removed
        return crossed

    tb_rng = np.random.default_rng(SEED + 1)
    tb_trials = [degree_attack_crossings(tb_rng) for _ in range(200)]
    tie_break = {"n_trials": 200, "seed": SEED + 1,
                 "description": "adaptive degree-targeted removal with random tie-breaks among equal-degree nodes; nodes removed (checked after every removal) until the largest component falls below the threshold"}
    for (basis, thr) in tb_trials[0]:
        vals = [t[(basis, thr)] for t in tb_trials]
        tie_break.setdefault(basis, {})[thr] = {"nodes_removed_min": int(min(vals)), "nodes_removed_median": float(np.median(vals)),
                                                "nodes_removed_max": int(max(vals))}
    # betweenness-targeted crossing, exact (the recorded order is a single deterministic sequence)
    def order_crossing(order, denominator, threshold):
        h = g.copy()
        for i, v in enumerate(order, start=1):
            h.remove_node(v)
            if max((len(c) for c in nx.connected_components(h)), default=0) < threshold * denominator:
                return i
        return None
    betw_exact = {basis: {thr_label: order_crossing(betweenness_order, den, thr)
                          for thr_label, thr in (("50pct", 0.5), ("10pct", 0.1))}
                  for basis, den in (("all_nodes", n0), ("initial_giant_component", giant0))}

    summary = {
        "n_nodes": g.number_of_nodes(), "n_edges": g.number_of_edges(),
        "n_random_trials": N_RANDOM_TRIALS, "seed": SEED, "step_fraction": STEP_FRACTION,
        "checkpoint_step_nodes": max(1, int(round(n0 * STEP_FRACTION))),
        "betweenness_targeted_ranking": "unweighted hop-count betweenness, recomputed every n/20 removals (category A: intentionally NOT strength-derived)",
        "denominators": {"all_nodes": n0, "initial_giant_component": giant0},
        "fraction_removed_below_threshold_of_all_nodes": thresholds_for(n0),
        "fraction_removed_below_threshold_of_initial_giant_component": thresholds_for(giant0),
        "degree_targeted_tie_break_sensitivity": tie_break,
        "betweenness_targeted_exact_nodes_removed": betw_exact,
    }
    with open(OUT_STATS / "robustness_summary_G0_full.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
