"""Cluster-validity audit for the story-similarity clustering (RQ6, DEC-015).

Ward linkage always returns a dendrogram, whatever the data look like, so the
existence of the dendrogram in F-series/T08 outputs is not evidence of
discrete story clusters. This script asks whether the 14 stories actually
show discrete cluster structure in the DEC-014 feature space (relation_family_top
proportions + layer proportions, 13-dim), using low-cost, dependency-light
checks (numpy + scipy only):

1. Cophenetic correlation of Ward / average / complete / single linkage
   (how faithfully each dendrogram preserves the pairwise distances).
2. Silhouette width for k = 2..6 under each linkage.
3. Cross-linkage agreement (adjusted Rand index between partitions from
   different linkages at the same k).
4. Bootstrap stability: relations are resampled with replacement *within*
   each story (story sizes preserved), the feature matrix rebuilt, Ward
   re-cut at k, and the partition compared with the original by ARI.
5. Permutation reference: relation-to-story assignment is shuffled
   (story sizes preserved) to obtain the silhouette / cophenetic values one
   would see if stories had no distinctive relational profile. The observed
   values are compared against this baseline (empirical one-sided p).
6. Reference distribution for the raw similarity values: what relation-profile
   / layer-composition cosine similarities look like under the same
   permutation baseline, so that "0.94-0.97" can be read against a baseline
   rather than as an absolute "high".

Nothing here changes the DEC-014 similarity matrices, T08, F10 or F11.
Output: outputs/statistics/story_similarity_cluster_validity.json
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import cophenet, fcluster, linkage
from scipy.spatial.distance import pdist

ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
OUT_STATS = ROOT / "outputs" / "statistics"

SEED = 42
N_BOOT = 1000
N_PERM = 1000
K_RANGE = list(range(2, 7))
LINKAGES = ["ward", "average", "complete", "single"]


def build_features(rel: pd.DataFrame, story_ids: list) -> np.ndarray:
    """13-dim proportion profile per story, identical to story_similarity.py."""
    def prop(col):
        counts = rel.groupby(["story_id", col]).size().unstack(fill_value=0)
        counts = counts.reindex(index=story_ids, fill_value=0)
        return counts.div(counts.sum(axis=1), axis=0).fillna(0)
    return pd.concat([prop("relation_family_top"), prop("layer")], axis=1).values


def features_from_codes(story_codes: np.ndarray, fam: np.ndarray, lay: np.ndarray,
                        n_stories: int, n_fam: int, n_lay: int) -> np.ndarray:
    """Fast vectorised equivalent of build_features on integer-coded arrays."""
    f = np.zeros((n_stories, n_fam))
    l = np.zeros((n_stories, n_lay))
    np.add.at(f, (story_codes, fam), 1)
    np.add.at(l, (story_codes, lay), 1)
    fs = f.sum(axis=1, keepdims=True)
    ls = l.sum(axis=1, keepdims=True)
    fs[fs == 0] = 1
    ls[ls == 0] = 1
    return np.hstack([f / fs, l / ls])


def silhouette(dist: np.ndarray, labels: np.ndarray) -> float:
    """Mean silhouette width from a full distance matrix. Singleton clusters
    contribute 0 (standard convention); returns nan if k < 2 or k == n."""
    n = len(labels)
    uniq = np.unique(labels)
    if len(uniq) < 2 or len(uniq) >= n:
        return float("nan")
    s = np.zeros(n)
    for i in range(n):
        own = labels == labels[i]
        if own.sum() == 1:
            s[i] = 0.0
            continue
        a = dist[i, own & (np.arange(n) != i)].mean()
        b = min(dist[i, labels == c].mean() for c in uniq if c != labels[i])
        s[i] = (b - a) / max(a, b) if max(a, b) > 0 else 0.0
    return float(s.mean())


def ari(a: np.ndarray, b: np.ndarray) -> float:
    """Adjusted Rand index (Hubert & Arabie 1985)."""
    a_u, a_i = np.unique(a, return_inverse=True)
    b_u, b_i = np.unique(b, return_inverse=True)
    cont = np.zeros((len(a_u), len(b_u)), dtype=float)
    np.add.at(cont, (a_i, b_i), 1)
    comb = lambda x: x * (x - 1) / 2.0
    sum_comb = comb(cont).sum()
    sum_a = comb(cont.sum(axis=1)).sum()
    sum_b = comb(cont.sum(axis=0)).sum()
    n_comb = comb(len(a))
    expected = sum_a * sum_b / n_comb if n_comb else 0.0
    max_index = 0.5 * (sum_a + sum_b)
    if max_index == expected:
        return 1.0
    return float((sum_comb - expected) / (max_index - expected))


def cut(Z: np.ndarray, k: int) -> np.ndarray:
    return fcluster(Z, t=k, criterion="maxclust")


def cluster_summary(X: np.ndarray, method: str):
    d = pdist(X, metric="euclidean")
    Z = linkage(X, method=method) if method != "ward" else linkage(X, method="ward")
    coph_r = float(cophenet(Z, d)[0])
    return d, Z, coph_r


def analyze(rel: pd.DataFrame, story_ids: list) -> dict:
    """Run checks 1-6 for the given stories (rel must already be restricted
    to relations of those stories). Deterministic given SEED."""
    rng = np.random.default_rng(SEED)
    n = len(story_ids)

    X = build_features(rel, story_ids)
    dist_full = np.linalg.norm(X[:, None, :] - X[None, :, :], axis=2)

    # ---- 1-3: observed validity ------------------------------------------
    observed = {}
    partitions = {}
    for m in LINKAGES:
        d, Z, coph_r = cluster_summary(X, m)
        observed[m] = {"cophenetic_correlation": round(coph_r, 4), "silhouette_by_k": {}}
        partitions[m] = {}
        for k in K_RANGE:
            lab = cut(Z, k)
            partitions[m][k] = lab
            observed[m]["silhouette_by_k"][str(k)] = round(silhouette(dist_full, lab), 4)

    agreement = {}
    for k in K_RANGE:
        agreement[str(k)] = {}
        for i, m1 in enumerate(LINKAGES):
            for m2 in LINKAGES[i + 1:]:
                agreement[str(k)][f"{m1}_vs_{m2}"] = round(ari(partitions[m1][k], partitions[m2][k]), 4)

    # cluster sizes at each k for Ward (singletons matter for interpretation)
    ward_sizes = {str(k): sorted(np.bincount(partitions["ward"][k])[1:].tolist(), reverse=True) for k in K_RANGE}

    best_k_ward = max(K_RANGE, key=lambda k: observed["ward"]["silhouette_by_k"][str(k)])

    # ---- 4: bootstrap stability (resample relations within story) ---------
    story_code = rel["story_id"].map({s: i for i, s in enumerate(story_ids)}).values
    fam_levels = sorted(rel["relation_family_top"].unique())
    lay_levels = sorted(rel["layer"].unique())
    fam = rel["relation_family_top"].map({v: i for i, v in enumerate(fam_levels)}).values
    lay = rel["layer"].map({v: i for i, v in enumerate(lay_levels)}).values
    idx_by_story = [np.where(story_code == i)[0] for i in range(n)]

    Zw = linkage(X, method="ward")
    boot_ari = {k: [] for k in K_RANGE}
    for _ in range(N_BOOT):
        pick = np.concatenate([rng.choice(ix, size=len(ix), replace=True) for ix in idx_by_story])
        Xb = features_from_codes(story_code[pick], fam[pick], lay[pick], n, len(fam_levels), len(lay_levels))
        Zb = linkage(Xb, method="ward")
        for k in K_RANGE:
            boot_ari[k].append(ari(cut(Zw, k), cut(Zb, k)))
    bootstrap = {str(k): {"mean_ari": round(float(np.mean(v)), 4),
                          "ci95_low": round(float(np.percentile(v, 2.5)), 4),
                          "ci95_high": round(float(np.percentile(v, 97.5)), 4)}
                 for k, v in boot_ari.items()}

    # ---- 5-6: permutation reference (shuffle story labels of relations) ---
    perm_sil = {k: [] for k in K_RANGE}
    perm_coph = []
    perm_rel_cos, perm_lay_cos = [], []
    tri = np.triu_indices(n, 1)
    # relation-profile cosine uses the 17-type profile, as in story_similarity.py
    type_levels = sorted(rel["standard_relation"].unique())
    typ = rel["standard_relation"].map({v: i for i, v in enumerate(type_levels)}).values

    def cos_matrix(M):
        nrm = np.linalg.norm(M, axis=1, keepdims=True)
        nrm[nrm == 0] = 1
        U = M / nrm
        return U @ U.T

    def count_matrix(codes_story, codes_cat, n_cat):
        M = np.zeros((n, n_cat))
        np.add.at(M, (codes_story, codes_cat), 1)
        return M

    obs_rel_cos = cos_matrix(count_matrix(story_code, typ, len(type_levels)))[tri]
    obs_lay_cos = cos_matrix(count_matrix(story_code, lay, len(lay_levels)))[tri]

    for _ in range(N_PERM):
        sc = rng.permutation(story_code)
        Xp = features_from_codes(sc, fam, lay, n, len(fam_levels), len(lay_levels))
        Zp = linkage(Xp, method="ward")
        dp = np.linalg.norm(Xp[:, None, :] - Xp[None, :, :], axis=2)
        perm_coph.append(cophenet(Zp, pdist(Xp))[0])
        for k in K_RANGE:
            perm_sil[k].append(silhouette(dp, cut(Zp, k)))
        perm_rel_cos.append(cos_matrix(count_matrix(sc, typ, len(type_levels)))[tri])
        perm_lay_cos.append(cos_matrix(count_matrix(sc, lay, len(lay_levels)))[tri])

    perm = {"n_permutations": N_PERM, "seed": SEED, "silhouette_by_k": {}}
    for k in K_RANGE:
        obs = observed["ward"]["silhouette_by_k"][str(k)]
        arr = np.array(perm_sil[k])
        perm["silhouette_by_k"][str(k)] = {
            "observed": obs,
            "null_mean": round(float(np.nanmean(arr)), 4),
            "null_95th_percentile": round(float(np.nanpercentile(arr, 95)), 4),
            "p_one_sided": round(float((1 + np.nansum(arr >= obs)) / (1 + np.sum(~np.isnan(arr)))), 4),
        }
    obs_c = observed["ward"]["cophenetic_correlation"]
    pc = np.array(perm_coph)
    perm["cophenetic_correlation_ward"] = {
        "observed": obs_c, "null_mean": round(float(pc.mean()), 4),
        "null_95th_percentile": round(float(np.percentile(pc, 95)), 4),
        "p_one_sided": round(float((1 + np.sum(pc >= obs_c)) / (1 + len(pc))), 4)}

    prc = np.array(perm_rel_cos)
    plc = np.array(perm_lay_cos)
    reference = {
        "relation_profile_cosine": {
            "observed_median": round(float(np.median(obs_rel_cos)), 4),
            "observed_max": round(float(obs_rel_cos.max()), 4),
            "permutation_null_median_of_pair_values": round(float(np.median(np.median(prc, axis=1))), 4),
            "permutation_null_95th_percentile_of_pair_max": round(float(np.percentile(prc.max(axis=1), 95)), 4),
        },
        "layer_composition_cosine": {
            "observed_median": round(float(np.median(obs_lay_cos)), 4),
            "observed_max": round(float(obs_lay_cos.max()), 4),
            "permutation_null_median_of_pair_values": round(float(np.median(np.median(plc, axis=1))), 4),
            "permutation_null_95th_percentile_of_pair_max": round(float(np.percentile(plc.max(axis=1), 95)), 4),
        },
    }

    # ---- verdict (mechanical, thresholds fixed a priori) ------------------
    # Conventional silhouette reading (Kaufman & Rousseeuw 1990): >0.70 strong,
    # 0.51-0.70 reasonable, 0.26-0.50 weak / possibly artificial, <=0.25 none.
    best_sil = observed["ward"]["silhouette_by_k"][str(best_k_ward)]
    best_boot = bootstrap[str(best_k_ward)]["mean_ari"]
    best_p = perm["silhouette_by_k"][str(best_k_ward)]["p_one_sided"]
    strong = best_sil > 0.50 and best_boot >= 0.75 and best_p < 0.05
    verdict = ("supported" if strong else "not_robustly_supported")

    return {
        "stories": story_ids,
        "n_stories": n,
        "relations_per_story": {s: int((rel["story_id"] == s).sum()) for s in story_ids},
        "observed": observed,
        "ward_cluster_sizes_by_k": ward_sizes,
        "best_k_by_ward_silhouette": best_k_ward,
        "cross_linkage_agreement_ari": agreement,
        "bootstrap_stability_ward": {"n_bootstrap": N_BOOT, "seed": SEED, "resampling": "relations resampled with replacement within each story", "by_k": bootstrap},
        "permutation_reference": perm,
        "similarity_value_reference": reference,
        "verdict_discrete_clusters": verdict,
    }


def main():
    rel = pd.read_csv(PROCESSED / "relations_event_level.csv", encoding="utf-8-sig")
    stories = pd.read_csv(PROCESSED / "stories.csv", encoding="utf-8-sig")
    story_ids = stories.sort_values("corpus_order")["story_id"].tolist()

    full = analyze(rel, story_ids)

    # Sensitivity: S01 (Girizgah) has a single coded relation, so its
    # proportion profile is degenerate (100% one category) and it is
    # mechanically an outlier. Re-run without it. The verdict rule below is
    # the same fixed rule; it is not tuned to this run.
    no_s01_ids = [s for s in story_ids if s != "S01"]
    no_s01 = analyze(rel[rel["story_id"].isin(no_s01_ids)], no_s01_ids)

    mat = pd.read_csv(ROOT / "outputs" / "matrices" / "story_similarity_actor_jaccard.csv",
                      index_col=0, encoding="utf-8-sig")
    v = mat.values[np.triu_indices(len(mat), 1)]
    actor_overlap = {"n_pairs": int(len(v)), "n_pairs_zero_overlap": int((v == 0).sum()),
                     "median": round(float(np.median(v)), 4), "mean": round(float(v.mean()), 4),
                     "max": round(float(v.max()), 4)}

    result = {
        "purpose": "Cluster-validity audit of the DEC-014 Ward clustering (DEC-015). A dendrogram always exists; this asks whether discrete clusters are actually supported.",
        "feature_space": "relation_family_top proportions (6-dim) + layer proportions (7-dim), each story's proportions (rows sum to 1 within each block); Euclidean distance",
        "verdict_rule": "supported only if best-k Ward silhouette > 0.50 AND bootstrap mean ARI >= 0.75 AND permutation p < 0.05; thresholds fixed before inspecting results (Kaufman & Rousseeuw 1990 silhouette convention; ARI >= 0.75 = good agreement by common convention)",
        "all_14_stories": full,
        "sensitivity_excluding_S01": no_s01,
        "actor_jaccard_distribution": actor_overlap,
    }
    with open(OUT_STATS / "story_similarity_cluster_validity.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    for label, r in [("ALL 14", full), ("EXCLUDING S01", no_s01)]:
        print(f"===== {label} =====")
        print("Cophenetic r:", {m: r["observed"][m]["cophenetic_correlation"] for m in LINKAGES})
        print("Silhouette by k (Ward):", r["observed"]["ward"]["silhouette_by_k"])
        print("Permutation null (mean, p95, p):", {k: (x["null_mean"], x["null_95th_percentile"], x["p_one_sided"]) for k, x in r["permutation_reference"]["silhouette_by_k"].items()})
        print("Bootstrap mean ARI (Ward):", {k: x["mean_ari"] for k, x in r["bootstrap_stability_ward"]["by_k"].items()})
        print("Ward cluster sizes:", r["ward_cluster_sizes_by_k"])
        print("Cosine reference:", r["similarity_value_reference"])
        print("Best k:", r["best_k_by_ward_silhouette"], "VERDICT:", r["verdict_discrete_clusters"])
    print("Actor Jaccard:", actor_overlap)


if __name__ == "__main__":
    main()
