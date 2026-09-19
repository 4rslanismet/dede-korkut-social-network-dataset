"""Phase 11: publication figures (section 46-48).

Follows section 47's rules: no hairballs (weighted edge opacity,
degree-based node size, selective labels only for the highest-degree
nodes), consistent readable font sizes, PNG + SVG export.

Figure numbering follows the project brief's F01-F18 list (section 48).
Not every figure is produced in this pass — see docs/decision_log.md /
CLAUDE_SESSION_HANDOFF.md for what remains (story similarity F10/F11 needs
Phase-unbuilt similarity metrics; several others are lower priority).
"""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx
import numpy as np
import pandas as pd

from networks import build_all_networks, load_processed

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "outputs" / "figures"

plt.rcParams.update({
    "font.size": 10,
    "axes.titlesize": 12,
    "axes.labelsize": 10,
    "figure.dpi": 150,
    "savefig.dpi": 300,
})


def save(fig, subdir: str, name: str):
    d = FIG / subdir
    d.mkdir(parents=True, exist_ok=True)
    fig.savefig(d / f"{name}.png", bbox_inches="tight")
    fig.savefig(d / f"{name}.svg", bbox_inches="tight")
    plt.close(fig)
    print(f"Saved {subdir}/{name}.png (+.svg)")


def draw_network(g: nx.Graph, title: str, subtitle: str, label_top_n: int = 6, seed: int = 42,
                  node_color_map: dict | None = None, legend_handles: list | None = None):
    pos = nx.spring_layout(g, weight="weight", seed=seed, k=6.0 / np.sqrt(max(g.number_of_nodes(), 1)), iterations=300)
    degrees = dict(g.degree())
    max_deg = max(degrees.values()) if degrees else 1

    fig, ax = plt.subplots(figsize=(12, 10))

    weights = np.array([g[u][v].get("weight", 1.0) for u, v in g.edges()])
    if len(weights):
        w_norm = 0.15 + 0.55 * (weights - weights.min()) / (weights.max() - weights.min() + 1e-9)
    else:
        w_norm = []
    for (u, v), alpha in zip(g.edges(), w_norm):
        ax.plot([pos[u][0], pos[v][0]], [pos[u][1], pos[v][1]], color="#999999", alpha=alpha, linewidth=0.8, zorder=1)

    node_sizes = [30 + 400 * (degrees[n] / max_deg) for n in g.nodes()]
    if node_color_map is not None:
        colors = [node_color_map.get(n, "#888888") for n in g.nodes()]
    else:
        colors = "#3b6fa0"
    ax.scatter([pos[n][0] for n in g.nodes()], [pos[n][1] for n in g.nodes()],
               s=node_sizes, c=colors, edgecolors="white", linewidths=0.5, zorder=2)

    # Stagger label offsets in a ring pattern so labels for nearby high-degree
    # nodes don't stack directly on top of one another; leader line connects
    # label to node when the offset is non-trivial.
    top_nodes = sorted(degrees, key=degrees.get, reverse=True)[:label_top_n]
    offset_ring = [(0, 20), (0, -24), (42, 10), (-42, 10), (42, -20), (-42, -20), (0, 34), (0, -38)]
    for i, n in enumerate(top_nodes):
        label = g.nodes[n].get("canonical_name", n)
        dx, dy = offset_ring[i % len(offset_ring)]
        ax.annotate(
            label, pos[n], fontsize=8.5, fontweight="bold", ha="center", va="center",
            xytext=(dx, dy), textcoords="offset points", zorder=4,
            bbox=dict(boxstyle="round,pad=0.15", facecolor="white", edgecolor="none", alpha=0.85),
            arrowprops=dict(arrowstyle="-", color="#555555", linewidth=0.6, shrinkA=0, shrinkB=4),
        )

    ax.set_title(title, fontsize=13, fontweight="bold")
    ax.text(0.5, -0.04, subtitle, transform=ax.transAxes, ha="center", va="top", fontsize=8.5, color="#444444", wrap=True)
    ax.axis("off")
    if legend_handles:
        ax.legend(handles=legend_handles, loc="lower left", fontsize=8, frameon=True)
    return fig


def figure_F02_corpus_full(graphs):
    g = graphs["G0_full"]
    label_n = 6
    fig = draw_network(
        g, "F02 — Corpus Full Network (G0_full)",
        f"{g.number_of_nodes()} nodes, {g.number_of_edges()} edges. Node size = degree. "
        f"Edge opacity = relation weight (agirlik). Labels: top {label_n} by degree only.",
        label_top_n=label_n,
    )
    save(fig, "corpus", "F02_corpus_full_network")


def figure_F03_person_only(graphs):
    g = graphs["G1_person_only"]
    label_n = 6
    fig = draw_network(
        g, "F03 — Person-Only Network (G1_person_only)",
        f"{g.number_of_nodes()} nodes (kişi type only), {g.number_of_edges()} edges. Node size = degree. "
        f"Labels: top {label_n} by degree only.",
        label_top_n=label_n,
    )
    save(fig, "corpus", "F03_person_only_network")


def figure_F06_communities(graphs):
    membership = pd.read_csv(ROOT / "outputs" / "tables" / "community_membership_G2_core_social.csv", encoding="utf-8-sig")
    g = graphs["G2_core_social"]
    comm_of = dict(zip(membership["node_id"], membership["leiden_community"]))

    giant_nodes = max(nx.connected_components(g), key=len)
    cmap = plt.get_cmap("tab20")
    comm_ids = sorted(set(comm_of.get(n, -1) for n in giant_nodes))
    color_map_giant = {cid: cmap(i % 20) for i, cid in enumerate(comm_ids)}
    node_color_map = {n: (color_map_giant[comm_of[n]] if n in giant_nodes else "#d9d9d9") for n in g.nodes()}

    fig = draw_network(
        g, "F06 — Community Structure (G2_core_social, Leiden, resolution=1.0, seed=42)",
        "Colors = community membership WITHIN the 261-node giant component only. Grey nodes = the "
        "22 smaller connected components, each trivially its own 'community' by construction - "
        "NOT meaningful social clustering (see reports/06_advanced_network_analysis_report.md §1.4). "
        f"Giant component modularity context: overall Leiden modularity = 0.695, 33 communities total.",
        node_color_map=node_color_map,
    )
    save(fig, "communities", "F06_community_structure")


def figure_F07_centrality_comparison(nodes):
    df = pd.read_csv(ROOT / "outputs" / "tables" / "centrality_G0_full.csv", encoding="utf-8-sig")
    top = df.sort_values("degree", ascending=False).head(15).iloc[::-1]

    fig, axes = plt.subplots(1, 3, figsize=(13, 6), sharey=True)
    metrics = [("degree", "Degree"), ("betweenness", "Betweenness"), ("pagerank", "PageRank")]
    for ax, (col, label) in zip(axes, metrics):
        ax.barh(top["canonical_name"], top[col], color="#3b6fa0")
        ax.set_title(label)
        ax.tick_params(axis="y", labelsize=8)
    fig.suptitle("F07 — Top 15 Actors by Degree, with Betweenness/PageRank (G0_full)", fontsize=13, fontweight="bold")
    fig.text(0.5, -0.02, "Preliminary descriptive centrality result (Phase 5); community/null-model context in "
                          "reports/06 and reports/07. Not a literary-importance ranking.", ha="center", fontsize=8.5, color="#444444")
    fig.tight_layout()
    save(fig, "corpus", "F07_top_actors_centrality_comparison")


def figure_F15_null_model_distributions():
    with open(ROOT / "outputs" / "null_models" / "null_model_results_full.json", encoding="utf-8") as f:
        data = json.load(f)
    fdr = pd.read_csv(ROOT / "outputs" / "statistics" / "null_model_fdr_corrected.csv", encoding="utf-8-sig")
    sig = fdr[fdr["significant_at_bh_fdr_0.05"]].sort_values(["metric", "network"])

    # We only stored ensemble summary stats (mean/std), not the raw ensemble arrays, in the JSON
    # results; rebuild an approximate normal distribution from mean/std for illustration, and mark
    # the observed value clearly. This is a visualization aid, not a re-derivation of the raw data.
    n_plots = len(sig)
    ncols = 4
    nrows = int(np.ceil(n_plots / ncols))
    fig, axes = plt.subplots(nrows, ncols, figsize=(4 * ncols, 3 * nrows))
    axes = np.array(axes).reshape(-1)

    for ax, (_, row) in zip(axes, sig.iterrows()):
        net_result = data["results"][row["network"]]["metrics"][row["metric"]]
        mean, std = net_result["random_mean"], net_result["random_std"]
        if std and std > 0:
            x = np.linspace(mean - 4 * std, mean + 4 * std, 200)
            y = np.exp(-0.5 * ((x - mean) / std) ** 2) / (std * np.sqrt(2 * np.pi))
            ax.plot(x, y, color="#999999")
            ax.fill_between(x, y, color="#cccccc", alpha=0.5)
        ax.axvline(row["observed"], color="#c0392b", linewidth=2)
        ax.set_title(f"{row['network']}\n{row['metric']}", fontsize=8.5)
        ax.set_yticks([])
        ax.tick_params(axis="x", labelsize=7)

    for ax in axes[n_plots:]:
        ax.axis("off")

    fig.suptitle("F15 — Null Model Distributions (random ensemble, n=1000) vs Observed (red line)\n"
                  "Only the 12/36 tests significant after Benjamini-Hochberg FDR correction (α=0.05) shown",
                  fontsize=11, fontweight="bold")
    fig.tight_layout(rect=[0, 0, 1, 0.92])
    save(fig, "null_models", "F15_null_model_distributions")


def figure_F16_sensitivity_matrix():
    df = pd.read_csv(ROOT / "outputs" / "tables" / "sensitivity_rank_stability.csv", encoding="utf-8-sig")
    pivot = df.pivot(index="pair", columns="metric", values="spearman_rho")
    pivot = pivot[["degree", "betweenness", "pagerank"]]

    fig, ax = plt.subplots(figsize=(7, 5))
    im = ax.imshow(pivot.values, cmap="RdYlGn", vmin=0.7, vmax=1.0, aspect="auto")
    ax.set_xticks(range(len(pivot.columns)))
    ax.set_xticklabels(pivot.columns)
    ax.set_yticks(range(len(pivot.index)))
    ax.set_yticklabels(pivot.index, fontsize=8.5)
    for i in range(pivot.shape[0]):
        for j in range(pivot.shape[1]):
            ax.text(j, i, f"{pivot.values[i, j]:.3f}", ha="center", va="center", fontsize=8.5)
    fig.colorbar(im, ax=ax, label="Spearman ρ")
    ax.set_title("F16 — Sensitivity: Rank Correlation Across Network-Construction Choices", fontsize=11, fontweight="bold")
    fig.tight_layout()
    save(fig, "sensitivity", "F16_sensitivity_correlation_matrix")


def figure_F17_rank_stability_scatter():
    g0 = pd.read_csv(ROOT / "outputs" / "tables" / "centrality_G0_full.csv", encoding="utf-8-sig").set_index("node_id")
    g1 = pd.read_csv(ROOT / "outputs" / "tables" / "centrality_G1_person_only.csv", encoding="utf-8-sig").set_index("node_id")
    common = g0.index.intersection(g1.index)

    rank_a = g0.loc[common, "degree"].rank(ascending=False)
    rank_b = g1.loc[common, "degree"].rank(ascending=False)

    fig, ax = plt.subplots(figsize=(6.5, 6.5))
    ax.scatter(rank_a, rank_b, alpha=0.6, color="#3b6fa0", s=25)
    lims = [0, max(rank_a.max(), rank_b.max()) + 1]
    ax.plot(lims, lims, color="#c0392b", linestyle="--", linewidth=1, label="perfect agreement")
    ax.set_xlabel("Degree rank in G0_full (person+group)")
    ax.set_ylabel("Degree rank in G1_person_only")
    ax.set_title("F17 — Centrality Rank Stability: Person+Group vs Person-Only", fontsize=11, fontweight="bold")
    ax.legend(fontsize=8)
    fig.tight_layout()
    save(fig, "sensitivity", "F17_centrality_rank_stability")


def figure_F18_robustness_curves():
    random_df = pd.read_csv(ROOT / "outputs" / "statistics" / "robustness_random_removal_G0_full.csv", encoding="utf-8-sig")
    degree_df = pd.read_csv(ROOT / "outputs" / "statistics" / "robustness_degree_targeted_removal_G0_full.csv", encoding="utf-8-sig")
    betweenness_df = pd.read_csv(ROOT / "outputs" / "statistics" / "robustness_betweenness_targeted_removal_G0_full.csv", encoding="utf-8-sig")

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(random_df["fraction_removed"], random_df["largest_component_fraction_mean"],
            label="Random removal (mean of 100 trials)", color="#2c7fb8", linewidth=2)
    ax.fill_between(random_df["fraction_removed"],
                     random_df["largest_component_fraction_mean"] - random_df["largest_component_size_std"] / random_df["largest_component_size_mean"].max(),
                     random_df["largest_component_fraction_mean"] + random_df["largest_component_size_std"] / random_df["largest_component_size_mean"].max(),
                     color="#2c7fb8", alpha=0.15)
    ax.plot(degree_df["fraction_removed"], degree_df["largest_component_fraction"],
            label="Degree-targeted removal", color="#d95f0e", linewidth=2)
    ax.plot(betweenness_df["fraction_removed"], betweenness_df["largest_component_fraction"],
            label="Betweenness-targeted removal", color="#c0392b", linewidth=2)
    ax.set_xlabel("Fraction of nodes removed")
    ax.set_ylabel("Largest component size / original network size")
    ax.set_title("F18 — Structural Robustness Curves (G0_full)", fontsize=12, fontweight="bold")
    ax.legend(fontsize=9)
    ax.grid(alpha=0.3)
    fig.text(0.5, -0.02, "Structural robustness only - not a claim about narrative resilience.",
              ha="center", fontsize=8.5, color="#444444")
    fig.tight_layout()
    save(fig, "robustness", "F18_structural_robustness_curves")


def figure_F10_story_similarity_heatmap():
    mat = pd.read_csv(ROOT / "outputs" / "matrices" / "story_similarity_actor_jaccard.csv", index_col=0, encoding="utf-8-sig")
    off_diag_max = mat.values[~np.eye(len(mat), dtype=bool)].max()

    masked = mat.values.copy()
    np.fill_diagonal(masked, np.nan)

    cmap = plt.get_cmap("YlOrBr").copy()
    cmap.set_bad("#e8e4da")  # diagonal (self-similarity, trivially 1.0) shown as neutral grey, not competing with real pairs

    fig, ax = plt.subplots(figsize=(8, 7))
    im = ax.imshow(masked, cmap=cmap, vmin=0, vmax=off_diag_max)
    ax.set_xticks(range(len(mat.columns)))
    ax.set_xticklabels(mat.columns, rotation=90, fontsize=8)
    ax.set_yticks(range(len(mat.index)))
    ax.set_yticklabels(mat.index, fontsize=8)
    fig.colorbar(im, ax=ax, label="Actor Jaccard similarity")
    ax.set_title("F10 — Story Similarity Heatmap (Actor Jaccard)", fontsize=12, fontweight="bold")
    fig.text(0.5, -0.02, f"Grey diagonal = self-similarity (trivially 1.0, excluded from color scale). Colour scale ends at the maximum off-diagonal value ({off_diag_max:.2f}): overlap is low throughout.\n"
                         "See outputs/matrices/ for the other 4 similarity metrics.",
              ha="center", fontsize=8, color="#444444")
    fig.tight_layout()
    save(fig, "similarity", "F10_story_similarity_heatmap")


def figure_F11_story_similarity_network():
    mat = pd.read_csv(ROOT / "outputs" / "matrices" / "story_similarity_actor_jaccard.csv", index_col=0, encoding="utf-8-sig")
    stories = pd.read_csv(ROOT / "data" / "processed" / "stories.csv", encoding="utf-8-sig").set_index("story_id")

    # Keep only the relatively most-overlapping pairs (top 15 of 91) so the
    # figure stays legible. Absolute overlap is low (max Jaccard ~0.15), so
    # these edges mark the relatively most overlapping pairs, not strong similarity.
    pairs = []
    for i, a in enumerate(mat.index):
        for b in mat.columns[i + 1:]:
            pairs.append((a, b, mat.loc[a, b]))
    pairs.sort(key=lambda x: x[2], reverse=True)
    top_pairs = [p for p in pairs if p[2] > 0][:15]
    threshold = top_pairs[-1][2] if top_pairs else 0

    g = nx.Graph()
    g.add_nodes_from(mat.index)
    for a, b, w in top_pairs:
        g.add_edge(a, b, weight=w)
    g.remove_nodes_from(list(nx.isolates(g)))

    pos = nx.spring_layout(g, weight="weight", seed=42, k=1.6)
    fig, ax = plt.subplots(figsize=(9, 8))
    weights = np.array([g[u][v]["weight"] for u, v in g.edges()])
    for (u, v), w in zip(g.edges(), weights):
        alpha = 0.25 + 0.65 * (w - threshold) / (weights.max() - threshold + 1e-9)
        lw = 1.0 + 3.0 * (w - threshold) / (weights.max() - threshold + 1e-9)
        ax.plot([pos[u][0], pos[v][0]], [pos[u][1], pos[v][1]], color="#7a4b2a", alpha=alpha, linewidth=lw, zorder=1)
    ax.scatter([pos[n][0] for n in g.nodes()], [pos[n][1] for n in g.nodes()], s=420, c="#3b6fa0", edgecolors="white", linewidths=1.5, zorder=2)
    for n in g.nodes():
        ax.annotate(n, pos[n], fontsize=9, ha="center", va="center", color="white", fontweight="bold", zorder=3)
        boy_name = stories.loc[n, "boy_name_raw"] if n in stories.index else n
        ax.annotate(boy_name[:22], pos[n], fontsize=7, ha="center", va="top",
                    xytext=(0, -16), textcoords="offset points", color="#2a2622", zorder=3)
    ax.set_title(f"F11 — Story Actor-Overlap Network (top {len(top_pairs)} of 91 pairs by Actor Jaccard)", fontsize=12, fontweight="bold")
    ax.axis("off")
    fig.text(0.5, 0.01, f"Exploratory/descriptive. Absolute overlap is low (max Jaccard = {weights.max():.2f}; {sum(1 for p in pairs if p[2] == 0)} of 91 pairs share no actor): "
                        "edges show the relatively most-overlapping pairs, not strong similarity or clusters.",
             ha="center", fontsize=8, color="#444444", wrap=True)
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    save(fig, "similarity", "F11_story_similarity_network")


def main():
    nodes, rel = load_processed()
    graphs = build_all_networks()

    figure_F02_corpus_full(graphs)
    figure_F03_person_only(graphs)
    figure_F06_communities(graphs)
    figure_F07_centrality_comparison(nodes)
    figure_F15_null_model_distributions()
    figure_F16_sensitivity_matrix()
    figure_F17_rank_stability_scatter()
    figure_F18_robustness_curves()
    figure_F10_story_similarity_heatmap()
    figure_F11_story_similarity_network()

    print("\nAll priority figures generated under outputs/figures/")


if __name__ == "__main__":
    main()
