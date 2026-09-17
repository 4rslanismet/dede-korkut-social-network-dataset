"""Post-completion optional work: full story-similarity metric suite
(master prompt section 17), completing RQ6 (thesis/research_questions.md).

Five similarity measures are computed for every pair of the 14 stories:

1. actor_jaccard          - binary set overlap of which actors appear
2. actor_weighted_jaccard - weighted Jaccard using per-story actor
                            interaction counts as weights
3. actor_cosine           - cosine similarity of per-story actor weight
                            vectors (same weights as #2)
4. relation_profile_similarity - cosine similarity of each story's
                            distribution over the 17 standard_relation types
5. layer_composition_similarity - cosine similarity of each story's
                            distribution over the 7 relation layers

DEC-014 (see docs/decision_log.md): hierarchical clustering is run on the
relation-family-top + layer composition profile (a fixed, directly
comparable 13-dimensional feature vector across all 14 stories), not on
raw actor identity (332-dimensional, extremely sparse, and not what
"narrative-relational profile similarity" is meant to capture). The
actor-based measures (1-3) are reported as their own similarity matrices
and used for the story-similarity *network* (which stories share
characters), a deliberately different question from what the clustering
answers (which stories emphasize similar relation types/layers).
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import linkage, dendrogram
from scipy.spatial.distance import squareform

ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
OUT_MATRICES = ROOT / "outputs" / "matrices"
OUT_STATS = ROOT / "outputs" / "statistics"
OUT_TABLES = ROOT / "outputs" / "tables" / "publication"


def load():
    rel = pd.read_csv(PROCESSED / "relations_event_level.csv", encoding="utf-8-sig")
    stories = pd.read_csv(PROCESSED / "stories.csv", encoding="utf-8-sig")
    return rel, stories


def actor_weight_matrix(rel: pd.DataFrame, story_ids: list) -> pd.DataFrame:
    """actor x story matrix, weight = number of relations that actor
    participates in (as source or target) within that story."""
    long = pd.concat([
        rel[["source_id", "story_id"]].rename(columns={"source_id": "actor_id"}),
        rel[["target_id", "story_id"]].rename(columns={"target_id": "actor_id"}),
    ]).dropna()
    counts = long.groupby(["actor_id", "story_id"]).size().unstack(fill_value=0)
    counts = counts.reindex(columns=story_ids, fill_value=0)
    return counts


def cosine_sim(a: np.ndarray, b: np.ndarray) -> float:
    na, nb = np.linalg.norm(a), np.linalg.norm(b)
    if na == 0 or nb == 0:
        return float("nan")
    return float(np.dot(a, b) / (na * nb))


def jaccard_binary(a: np.ndarray, b: np.ndarray) -> float:
    a_bin, b_bin = a > 0, b > 0
    union = np.logical_or(a_bin, b_bin).sum()
    if union == 0:
        return float("nan")
    inter = np.logical_and(a_bin, b_bin).sum()
    return float(inter / union)


def jaccard_weighted(a: np.ndarray, b: np.ndarray) -> float:
    denom = np.sum(np.maximum(a, b))
    if denom == 0:
        return float("nan")
    return float(np.sum(np.minimum(a, b)) / denom)


def pairwise_matrix(feature_df: pd.DataFrame, metric_fn) -> pd.DataFrame:
    cols = list(feature_df.columns)
    n = len(cols)
    mat = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            mat[i, j] = metric_fn(feature_df.iloc[:, i].values, feature_df.iloc[:, j].values)
    return pd.DataFrame(mat, index=cols, columns=cols)


def profile_matrix(rel: pd.DataFrame, story_ids: list, group_col: str) -> pd.DataFrame:
    """story x category count matrix (categories = distinct values of
    group_col, e.g. standard_relation or layer), used to build the
    relation-profile and layer-composition similarity measures."""
    counts = rel.groupby(["story_id", group_col]).size().unstack(fill_value=0)
    counts = counts.reindex(index=story_ids, fill_value=0)
    return counts


def main():
    rel, stories = load()
    story_ids = stories.sort_values("corpus_order")["story_id"].tolist()

    # --- Actor-based measures (1-3) ---
    actor_weights = actor_weight_matrix(rel, story_ids)  # actors x stories
    actor_jaccard = pairwise_matrix(actor_weights, jaccard_binary)
    actor_weighted_jaccard = pairwise_matrix(actor_weights, jaccard_weighted)
    actor_cosine = pairwise_matrix(actor_weights, cosine_sim)

    # --- Content-profile measures (4-5) ---
    relation_profile = profile_matrix(rel, story_ids, "standard_relation")  # stories x 17
    layer_profile = profile_matrix(rel, story_ids, "layer")  # stories x 7
    relation_profile_sim = pairwise_matrix(relation_profile.T, cosine_sim)
    layer_composition_sim = pairwise_matrix(layer_profile.T, cosine_sim)

    OUT_MATRICES.mkdir(parents=True, exist_ok=True)
    actor_jaccard.to_csv(OUT_MATRICES / "story_similarity_actor_jaccard.csv", encoding="utf-8-sig")
    actor_weighted_jaccard.to_csv(OUT_MATRICES / "story_similarity_actor_weighted_jaccard.csv", encoding="utf-8-sig")
    actor_cosine.to_csv(OUT_MATRICES / "story_similarity_actor_cosine.csv", encoding="utf-8-sig")
    relation_profile_sim.to_csv(OUT_MATRICES / "story_similarity_relation_profile.csv", encoding="utf-8-sig")
    layer_composition_sim.to_csv(OUT_MATRICES / "story_similarity_layer_composition.csv", encoding="utf-8-sig")

    print("Actor Jaccard (first 3x3):")
    print(actor_jaccard.iloc[:3, :3].round(3))
    print("\nRelation-profile cosine similarity (first 3x3):")
    print(relation_profile_sim.iloc[:3, :3].round(3))

    # --- Hierarchical clustering (DEC-014): relation-family-top + layer profile ---
    family_profile = profile_matrix(rel, story_ids, "relation_family_top")  # stories x 6
    # normalize each story's profile to proportions so story size doesn't dominate
    family_prop = family_profile.div(family_profile.sum(axis=1), axis=0).fillna(0)
    layer_prop = layer_profile.div(layer_profile.sum(axis=1), axis=0).fillna(0)
    combined_features = pd.concat([family_prop, layer_prop], axis=1)
    combined_features.index = story_ids

    Z = linkage(combined_features.values, method="ward")
    dendro = dendrogram(Z, labels=story_ids, no_plot=True)
    cluster_order = dendro["ivl"]

    with open(OUT_STATS / "story_similarity_clustering.json", "w", encoding="utf-8") as f:
        json.dump({
            "feature_space": "relation_family_top proportions (6-dim) + layer proportions (7-dim), z-normalized to proportions per story",
            "linkage_method": "ward",
            "dendrogram_leaf_order": cluster_order,
            "linkage_matrix": Z.tolist(),
        }, f, ensure_ascii=False, indent=2)

    # --- T08 table: now the full suite, no longer "partial" ---
    rows = []
    for i, a in enumerate(story_ids):
        for j, b in enumerate(story_ids):
            if j <= i:
                continue
            rows.append({
                "story_a": a, "story_b": b,
                "actor_jaccard": round(actor_jaccard.loc[a, b], 4),
                "actor_weighted_jaccard": round(actor_weighted_jaccard.loc[a, b], 4),
                "actor_cosine": round(actor_cosine.loc[a, b], 4),
                "relation_profile_similarity": round(relation_profile_sim.loc[a, b], 4),
                "layer_composition_similarity": round(layer_composition_sim.loc[a, b], 4),
            })
    t08 = pd.DataFrame(rows).sort_values("actor_jaccard", ascending=False)
    OUT_TABLES.mkdir(parents=True, exist_ok=True)
    t08.to_csv(OUT_TABLES / "T08_story_similarity.csv", index=False, encoding="utf-8-sig")
    latex = t08.to_latex(index=False, float_format=lambda x: "%.4f" % x,
                          caption="Story similarity: all 5 metrics, all 91 story pairs (Phase 22 completion of RQ6)",
                          label="tab:t08_story_similarity")
    with open(OUT_TABLES / "T08_story_similarity.tex", "w", encoding="utf-8") as f:
        f.write(latex)

    print(f"\nWrote T08_story_similarity.csv ({len(t08)} pairs) - now the FULL 5-metric suite, no longer partial.")
    print("\nTop 5 most similar story pairs by actor_jaccard:")
    print(t08.head(5).to_string(index=False))
    print(f"\nDendrogram leaf order (Ward, relation-family+layer profile): {cluster_order}")


if __name__ == "__main__":
    main()
