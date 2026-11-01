# Technical Results Package

Publication-ready reference tables and statistical summaries. Every number traces to
a pipeline output file cited inline. No number is hand-typed.

Evidence class labels: **[C]** confirmatory, **[D]** descriptive, **[E]** exploratory,
**[N]** negative result.

---

## 1. Network Model Comparison (12 variants)

Source: `outputs/networks/network_summary.json`

| Model | Scope | Nodes | Edges | Directed | Components | Largest | Density | Avg C | Transitivity |
|---|---|---:|---:|---|---:|---:|---:|---:|---:|
| G0 | Full corpus | 311 | 376 | No | 23 | 261 | 0.0078 | 0.071 | 0.041 |
| G1 | Person only | 154 | 182 | No | 14 | 121 | 0.0154 | 0.073 | 0.078 |
| G2 | Core social | 309 | 374 | No | 23 | 259 | 0.0079 | 0.072 | 0.042 |
| G3 | Kinship | 83 | 61 | No | 22 | 24 | 0.0179 | 0.000 | 0.000 |
| G4 | Communication | 74 | 73 | No | 11 | 43 | 0.0270 | 0.090 | 0.061 |
| G5 | Cooperation | 73 | 65 | No | 12 | 45 | 0.0247 | 0.018 | 0.014 |
| G6 | Conflict | 114 | 92 | No | 23 | 43 | 0.0143 | 0.003 | 0.013 |
| G7 | Positive | 127 | 116 | No | 18 | 82 | 0.0145 | 0.029 | 0.020 |
| G8 | Negative | 126 | 102 | No | 25 | 57 | 0.0130 | 0.003 | 0.012 |
| G9 | Directed | 221 | 324 | Yes | 13* | 194 | 0.0067 | — | — |
| G10 | Weighted | 311 | 376 | No | 23 | 261 | 0.0078 | 0.071 | 0.041 |
| G11 | Unweighted | 311 | 376 | No | 23 | 261 | 0.0078 | 0.071 | 0.041 |

\* G9 components are weakly connected. G0, G10, G11 share identical topology; G10
preserves original weight (ağırlık 1–5), G11 forces all weights to 1.

---

## 2. Null-Model Results Matrix **[C]**

Source: `outputs/statistics/null_model_fdr_corrected.csv` (T09)
Method: 1,000 degree-preserving randomizations (double_edge_swap), BH-FDR α = 0.05.

### 2a. Significant results (12/36)

| Network | Metric | Observed | z | p_emp | q_BH | Direction |
|---|---|---:|---:|---:|---:|---|
| G0 | Modularity | 0.723 | 7.04 | 0.001 | 0.012 | Higher |
| G2 | Modularity | 0.724 | 6.88 | 0.001 | 0.012 | Higher |
| G2 | Clustering | 0.072 | 4.10 | 0.001 | 0.012 | Higher |
| G0 | Clustering | 0.071 | 3.94 | 0.002 | 0.018 | Higher |
| G1 | Modularity | 0.691 | 3.28 | 0.003 | 0.022 | Higher |
| G1 | Clustering | 0.073 | 3.01 | 0.004 | 0.024 | Higher |
| G1 | Transitivity | 0.078 | 3.00 | 0.006 | 0.027 | Higher |
| G6 | Modularity | 0.869 | 2.71 | 0.006 | 0.027 | Higher |
| G7 | Modularity | 0.779 | 2.82 | 0.008 | 0.032 | Higher |
| G8 | Modularity | 0.874 | 2.58 | 0.010 | 0.036 | Higher |
| G4 | Modularity | 0.683 | 2.62 | 0.011 | 0.036 | Higher |
| G4 | Clustering | 0.090 | 2.20 | 0.016 | 0.048 | Higher |

### 2b. Network × Metric significance matrix

| Network | Modularity | Clustering | Transitivity | Assortativity |
|---|---|---|---|---|
| G0 | **q=0.012** | **q=0.012** | q=0.356 | q=0.089 |
| G1 | **q=0.022** | **q=0.024** | **q=0.027** | q=0.749 |
| G2 | **q=0.012** | **q=0.012** | q=0.293 | q=0.149 |
| G3 | q=0.673 | q=1.000 | q=1.000 | q=1.000 |
| G4 | **q=0.036** | **q=0.048** | q=0.162 | q=0.293 |
| G5 | q=0.673 | q=1.000 | q=0.755 | q=1.000 |
| G6 | **q=0.027** | q=0.963 | q=1.000 | q=0.149 |
| G7 | **q=0.032** | q=0.572 | q=1.000 | q=0.567 |
| G8 | **q=0.036** | q=0.963 | q=1.000 | q=0.220 |

Bold = significant at BH-FDR α = 0.05. G3 and G5 show no significant deviation
from the null on any metric. G3 is a forest (zero clustering/transitivity by
structure); this is a low-information null, not evidence about kinship. **[N]**

### 2c. Summary by metric

| Metric | Significant / Tested | Networks |
|---|---:|---|
| Modularity | 7 / 9 | G0, G1, G2, G4, G6, G7, G8 |
| Clustering | 4 / 9 | G0, G1, G2, G4 |
| Transitivity | 1 / 9 | G1 only |
| Assortativity | 0 / 9 | none — retracted as structural claim **[N]** |
| **Total** | **12 / 36** | |

---

## 3. Community Structure **[C]**

Source: `outputs/statistics/community_summary_G2_core_social.json`

| Algorithm | Modularity | Communities | Network |
|---|---:|---:|---|
| Leiden (res=1.0, seed 42) | 0.695 | 33 | G2 |
| Louvain (seed 42) | 0.711 | 34 | G2 |

Adjusted Rand Index (Leiden vs Louvain): **0.899**

Giant-component robustness check: G0 giant component (261 nodes) observed Louvain
modularity 0.692 vs null mean 0.615 (z = 9.9, p = 0.001;
`outputs/statistics/audit_top5_checks.json`).

**Caveat:** G2 has 23 connected components; modularity-maximizing algorithms assign
each disconnected component its own community. The raw count of 33 partly reflects
fragmentation. Only structure within the 261-node giant component is interpreted as
socially meaningful clustering.

---

## 4. Sensitivity Analysis **[D]**

Source: `outputs/statistics/sensitivity_analysis_results.json` (T10)
Weighted betweenness uses distance = 1/strength (DEC-017).

| Pair | n_common | ρ Degree | ρ Between. | ρ PageRank | Mean ρ | Tier |
|---|---:|---:|---:|---:|---:|---|
| All relations vs core social | 309 | ≈1.000 | ≈1.000 | 0.999 | ≈1.000 | Negligible |
| Explicit vs explicit+inferred | 293 | 0.982 | 0.984 | 0.989 | 0.985 | Negligible |
| Girizgah incl. vs excl. | 310 | ≈1.000 | ≈1.000 | 1.000 | ≈1.000 | Negligible |
| Person+group vs person only | 154 | 0.916 | 0.892 | 0.926 | 0.911 | Noticeable |
| Weighted vs unweighted | 311 | 1.000† | 0.886 | 0.849 | 0.912 | Noticeable |
| Groups incl. vs excl. | 183 | 0.950 | 0.949 | 0.957 | 0.952 | Noticeable |

† Degree is identical by construction (same edge set). Mean ρ for this pair is
over betweenness and PageRank only.

All correlations ≥ 0.849. The three noticeable pairs are not ranked against each
other (differences between correlations were not tested).

---

## 5. Structural Robustness **[D]**

Source: `outputs/statistics/robustness_summary_G0_full.json` (T11)
G0: 311 nodes, 376 edges, 100 random trials (seed 42).

### 5a. Fraction removed to halve giant component (all-nodes basis)

| Strategy | Grid checkpoint | Exact crossing |
|---|---:|---:|
| Random | 25.1% (~78 nodes) | — |
| Degree-targeted | 3.9% (12 nodes) | 6–7 nodes (2.0–2.3%) |
| Betweenness-targeted | 1.9% (6 nodes) | 6 nodes (1.9%) |

### 5b. Fraction removed to reduce to 10% (all-nodes basis)

| Strategy | Grid | Exact |
|---|---:|---:|
| Random | 61.7% | — |
| Degree-targeted | 5.8% | 15–17 nodes |
| Betweenness-targeted | 5.8% | 17 nodes |

Degree-targeted tie-break sensitivity: 200 trials with random tie-breaks among
equal-degree nodes; 50%-threshold crossing at 6–7 nodes (all stable).

At the 10% threshold the two targeted strategies converge (both 17 nodes exact).
The gap at the 50% threshold (6 vs 6–7) is a resolution artifact; **no claim is
made that one targeted strategy is more destructive than the other**. The supported
conclusion: targeted removal is substantially more disruptive than random removal,
consistent with hub-dependent structure.

---

## 6. Story Similarity **[D/E]**

Source: `outputs/results_registry.json`, T08, `outputs/statistics/story_similarity_cluster_validity.json`

### 6a. Pairwise similarity descriptives (91 pairs, 14 stories)

| Metric | Median | Max | Max pair | Zero-overlap pairs |
|---|---:|---:|---|---:|
| Actor Jaccard | 0.030 | 0.153 | S03–S05 | 28 / 91 |

S03–S05 share 11 actors (Jaccard = 0.153, weighted Jaccard = 0.222). This is the
top pair on Jaccard measures only; actor cosine, relation-profile cosine and
layer-composition cosine each have a different top pair.

### 6b. Cluster validity audit

| k | Silhouette | Bootstrap ARI | Permutation p | Pass rule? |
|---|---:|---:|---:|---|
| 2 | 0.56 | — | — | No (isolates S01) |
| 3 | 0.48 | ~0.55 | — | No |
| 4 | 0.42 | ~0.54 | — | No |
| 5 | 0.40 | ~0.54 | — | No |
| 6 | 0.37 | ~0.54 | — | No |

Pre-set rule: silhouette > 0.50 AND bootstrap ARI ≥ 0.75 AND permutation p < 0.05.
**No k passes.** Evidence for discrete clusters is limited. **[N for clustering; D for pairwise]**

---

## 7. Directed Network **[D]**

Source: `outputs/statistics/directed_triad_census_G9.json`
G9: 221 nodes, 324 directed edges, 13 weakly connected components. Reciprocity: 0.358.

Dominant triads: 003 (1,719,566), 012 (41,160), 102 (10,977).
Only 44 of 1,774,630 triads are closed — insufficient for enrichment testing.

Salur Kazan: out-degree 53, in-degree 30, HITS hub 0.425, authority 0.016 —
coded predominantly as relation initiator.

---

## 8. Signed Network **[N]**

Source: `outputs/statistics/signed_structural_balance.json`

Only 13 triangles among positively/negatively signed edges. Below the 15-triangle
pre-inspection threshold (DEC-012). Structural balance **not assessed** — reported
as a data-sparsity limitation, not a finding.

---

## 9. Open Limitations and Publication Blockers

### Limitations documented in analyses

| Issue | Impact | Source |
|---|---|---|
| Source edition unknown | Cannot reproduce raw → story_level | `validation/source_edition_metadata_required.md` |
| Single coder | No inter-annotator reliability | `docs/inter_annotator_protocol.md` |
| 53 provenance gaps (8.4%) | Event → story_level matching | `data/processed/provenance.csv` |
| 90 entity-review candidates | 15 high-priority near-duplicates | `validation/entity_review_candidates_v2.csv` |
| 29.6% uncertain relations | Coded as belirsiz | `data/processed/relation_taxonomy.csv` |
| Self-loop DKR0220 | Requires human decision | Propagates to 7/12 variants |
| Edge weight semantics undocumented | Sensitivity ρ = 0.85–0.96 | `docs/limitations.md` item 7 |

### Human-required publication blockers

1. **Source edition metadata** — which printed text was coded (human researcher)
2. **Inter-annotator agreement** — recruit and run second coder
3. **CITATION.cff author metadata** — given-names, family-names, date-released
4. **Entity review** — resolve 90 candidates (especially 15 high-priority)

---

## Evidence Traceability

Every number in this document traces to a specific file:
- Network properties → `outputs/networks/network_summary.json`
- Null-model tests → `outputs/statistics/null_model_fdr_corrected.csv` (= T09)
- Sensitivity → `outputs/statistics/sensitivity_analysis_results.json` (= T10)
- Robustness → `outputs/statistics/robustness_summary_G0_full.json` (= T11)
- Communities → `outputs/statistics/community_summary_G2_core_social.json`
- Story similarity → `outputs/results_registry.json`, `outputs/statistics/story_similarity_cluster_validity.json`
- Directed → `outputs/statistics/directed_triad_census_G9.json`
- Signed → `outputs/statistics/signed_structural_balance.json`
- Claim-evidence matrix → `outputs/claim_evidence_matrix.csv` (45 claims, all VERIFIED)
