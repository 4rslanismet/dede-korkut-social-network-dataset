# Fix Pass Report — Independent Review of `4e89da5`

# Starting reviewed commit

`4e89da5` ("Verify full end-to-end reproducibility before release"), branch `claude-dk-rebuild`, independently
reviewed and pushed to the remote. The fix pass lives on the **local** branch `claude-dk-fixpass`, created from that
commit; nothing was pushed, merged, tagged or deployed, and `main` is untouched.

Result of the review: the scientific core passed (canonical data, network definitions, null models, robustness
numbers, RQ6, manifest, licence consistency) but the branch was **not ready to merge/deploy/publish** until the items
below were corrected. Status after this pass: **validated research repository — publication blockers remain.**

# Independent-review issues

Status key: FIXED · DISCLOSED · DEFERRED — HUMAN ACTION REQUIRED · NOT APPLICABLE.

| # | Issue (review severity) | Status | Where |
|---|---|---|---|
| 1 | Weighted betweenness used tie strength as path distance (MAJOR) | **FIXED** | DEC-017; `src/networks.py`, `src/metrics.py`; `tests/test_distance_semantics.py` |
| 2 | Composite-node disclosure under-inclusive: "5 nodes" (MAJOR) | **FIXED** (scan, queue, disclosures) / **DEFERRED — HUMAN ACTION REQUIRED** (the manual review itself) | DEC-018; `src/composite_nodes.py`; `validation/composite_node_candidates.csv` |
| 3 | 3 stale/orphan character pages; validator blind to them (MINOR) | **FIXED** (generator + validator) | DEC-019; `src/site_pages.py`, `src/build_site.py`, `src/validate_site.py` |
| 4 | Story pages mixed raw relation records with aggregated-graph metrics (MINOR) | **FIXED** | DEC-019; story pages, `story_metrics.json`, T03 |
| 5 | Robustness wording: "giant component halved" vs. threshold on all nodes (MINOR) | **FIXED** | `reports/08`, T11, F06/F18 text, site, paper, thesis |
| 5b | Degree- vs betweenness-targeted difference is tie-break dependent (MINOR) | **FIXED** (claim not made; evidence added) | `src/robustness.py` tie-break sensitivity; T11 exact columns |
| 6 | Stale counts: manifest entries, stage count, grup/other node counts (MINOR) | **FIXED** (derived or removed, test-enforced) | `tests/test_text_consistency.py`, registry |
| 7 | Hard-coded scientific numbers/constants in the site generators (MINOR) | **FIXED** | `outputs/results_registry.json`; `src/build_site*.py` |
| 8 | Reproduce page omitted the site build; hard-coded transient branch (MINOR) | **FIXED** | site build/validation added to `run_pipeline.py`; page rewritten |
| 9 | Characters index exposed 60 of 332 actors (MINOR) | **FIXED** | filterable table of all actors; reachability validated |
| 10 | Nested null-model networks / single Louvain partition not disclosed (MINOR) | **DISCLOSED** (methodology unchanged) | paper, methodology, report 07, site |
| 11 | Source-code licence unresolved (nice-to-have) | **DISCLOSED** / **DEFERRED — HUMAN ACTION REQUIRED** | README, DATASET_CARD, limitations 18, site About |
| 12 | Paper package is not a finished manuscript | **DISCLOSED** | outline banner, limitations 19, reports |
| 13a | Source edition/transcription metadata | **DEFERRED — HUMAN ACTION REQUIRED** | unchanged |
| 13b | Second annotator / inter-annotator reliability | **DEFERRED — HUMAN ACTION REQUIRED** | unchanged |
| 13c | Manual review of unresolved entity items | **DEFERRED — HUMAN ACTION REQUIRED** | unchanged (queue expanded, nothing auto-resolved) |
| 13d | `CITATION.cff` owner metadata | **DEFERRED — HUMAN ACTION REQUIRED** | unchanged |
| 13e | Separate code-licence choice | **DEFERRED — HUMAN ACTION REQUIRED** | not chosen on the owner's behalf |
| — | RQ6 status | NOT APPLICABLE (unchanged: PARTIALLY ANSWERED / EXPLORATORY) | — |

Additional defects found while fixing (not in the review): the story-metrics merge hid the aggregated edge count
behind a `_m` suffix (root cause of #4); F06/F15/T05 captions and the T11 caption carried hard-typed numbers; the
Evidence page said "75 open items" and "11 decisions"; the About page said `CITATION.cff` was "pending"; the
home-page pipeline panel showed constants (`18/18`, `reproducible=True`); `paper/methods.md` quoted stage/test counts
in words ("eighteen"). All were fixed and are covered by tests or derived from data.

# Weighted betweenness

**Old semantics.** The edge attribute `weight` is tie *strength* (sum of coded 1–5 intensities per actor pair).
`metrics.py` called `nx.betweenness_centrality(g, weight="weight")`; NetworkX reads that argument as a *distance*, so a
stronger tie was a *longer* path. The sensitivity comparison inherited the same call (it uses `centrality_profile`).

**Corrected semantics.** Strength and distance are separate. `strength_to_distance(s) = 1/s` (rejects `s ≤ 0`/NaN),
applied on a copy of the graph (`with_distance`); weighted betweenness uses `weight="distance"`. Hop-count betweenness is
kept as its own measure (`betweenness_hop`); in G11 (all strengths 1) both coincide, which is the "unweighted" arm of the
weighted-vs-unweighted comparison. Every `betweenness_centrality` call was classified before anything was changed:

| Call | Class | Action |
|---|---|---|
| `metrics.py:centrality_profile` | B — strength-derived weighted | corrected (distance = 1/strength) + new `betweenness_hop` column (A) |
| `robustness.py` (2 calls, targeted removal) | A — hop-count, intentionally unweighted | unchanged; documented as such |
| other shortest-path uses (`diameter`, `average_shortest_path_length`, `eccentricity`, `harmonic_centrality(distance=None)`) | A — hop-count | unchanged |
| PageRank, strength, eigenvector, community detection | `weight` correctly read as strength | unchanged |

**Affected artifacts** (found by searching every consumer of the `betweenness` column, then confirmed by the diff):
`outputs/tables/centrality_G0/G1/G2/G9.csv` (only the betweenness column changed; degree, strength, PageRank are
identical), T04, F07, `sensitivity_analysis_results.json`, `sensitivity_rank_stability.csv`, T10, F16 (F17 is
degree-based and did not change), `docs/data/actor_metrics.json`, 311 character pages, the Analysis page, paper §1/§4 and
tables/figures, thesis results mapping / RQ1 / RQ5, reports 08 and FINAL, Top-5 finding #3. Not affected: null models,
communities, PageRank, robustness (hop-count), RQ6.

**Changed rankings** (old committed table vs. regenerated table, Spearman ρ of betweenness / top-10 overlap): G0 0.826 /
0.5; G1 0.849 / 0.7; G2 0.826 / 0.5; G9 0.941 / 0.5. In G0: Salur Kazan 0.388 (rank 1) → 0.598 (1); Bamsı Beyrek 0.223
(2) → 0.191 (3); Bayındır Han 0.108 (3) → 0.191 (2) — Bayındır Han and Bamsı Beyrek differ by 0.0001; Uruz 0.079 (7) →
0.106 (4). Salur Kazan is first on every measure in G0, G1, G2 and G9. The claim that Salur Kazan **and** Bamsı Beyrek lead
betweenness in every specification is **withdrawn** (Bamsı Beyrek is second in G2 and effectively tied for second in G0
under distance = 1/strength, fourth in G1, and second under hop-count in G0/G2/G9). Centrality statements are now written
per network specification and definition.

**Changed sensitivity numbers** (only betweenness cells changed; 14 of 18 cells are identical):

| Pair | betweenness ρ old → new |
|---|---|
| person+group vs person-only | 0.887 → 0.892 |
| weighted vs unweighted | 0.930 → 0.886 |
| groups included vs excluded | 0.896 → 0.949 |
| explicit-only vs explicit+inferred | 0.971 → 0.984 |
| girizgah / core-social | 1.000 → 1.000 |

Regenerated per-pair mean ρ: person+group vs person-only 0.911, weighted vs unweighted 0.912, groups included vs
excluded 0.952, explicit vs inferred 0.985, girizgah 1.000, core-social 1.000 (`outputs/results_registry.json` →
`sensitivity`). The pipeline's regenerated cells agree with the reviewer's independent recomputation, but no value was
copied from the review.

**Did any headline finding change?** No. Top-5 finding #3 was rewritten from the regenerated values: person+group vs
person-only and weighted vs unweighted are numerically tied (0.911 vs 0.912) and are not ranked; groups included/excluded
is a smaller effect (just under the 0.95 "noticeable" threshold); the rest are ≥ 0.98; the ordering of the six pairs is
unchanged, but the earlier weighted-betweenness value (0.930) and the placement of groups included/excluded among the
large-effect choices were artifacts of the error. Findings #1, #2, #4, #5 are unaffected.

**Regression protection.** `tests/test_distance_semantics.py`: stronger tie ⇒ shorter distance (5 → 0.2, 1 → 1.0);
non-positive/NaN strength fails loudly; on a synthetic graph the strong two-step route makes the intermediary carry
betweenness (the old call would give it zero); G11 betweenness equals hop-count; a static scan fails if any `src/*.py`
passes `weight="weight"` to `betweenness_centrality`; and the committed G0 centrality table and the weighted-vs-unweighted
sensitivity cell must equal a fresh computation.

# Composite nodes

`src/composite_nodes.py` (new pipeline stage after `build_canonical`) flags **review candidates** — never auto-splits or
auto-merges: comma lists, " ve " conjunctions, `/ + &`, and ≥ 6-word names. Generated counts
(`outputs/statistics/composite_node_summary.json`, mirrored in the registry):

- **46 of 332** canonical nodes are candidates (triggers, not exclusive: 10 comma, 36 "ve", 12 long-phrase);
  priority 11 high / 4 medium / 31 low.
- They touch **46 of 628 relations (7.3%)** and **48 of 1,256 relation endpoints (3.8%)**.
- 5 were already queued from the hand-found DEC-013 items (kept; not duplicated); **41 new queue items** were added
  (category `composite_node_candidate`), giving a 121-row `HUMAN_REVIEW_QUEUE.csv`. Re-running the stage is idempotent.
- Under-approximation is disclosed (misses " ile " constructions and short phrases); a candidate is not necessarily an error.

Disclosures were corrected everywhere the old "5" appeared (README, DATASET_CARD, limitations 11, paper supplement and
outline, thesis, reports, site Evidence/About/Characters pages), and the limitation was added to the **main paper text**
(Results §8, Methods). `tests/test_text_consistency.py` fails on any reappearance of a "5 composite/concatenated" statement and
checks that quoted candidate counts equal the scan. **Not resolved: this remains a publication blocker until a human
reviews the candidates against the original text.**

# Website cleanup

- **Expected character pages:** derived from the current canonical data (332); story pages 14; top-level pages 14
  (`src/site_pages.py`). No count is hard-coded.
- **Stale pages removed:** 3 orphan character pages (untruncated legacy filenames of the 95-, 62- and 108-character node
  IDs; content identical to their current counterparts, unlinked). The generator now deletes stale `*.html` in the two
  generated-page directories before writing; nothing outside them is touched.
- **Final validated page counts:** 360 HTML files = 14 + 14 + 332 (`validate_site.py`: links, assets, JSON, expected ==
  generated, every page reachable from its index) — the previous 363 included the 3 stale pages.
- **Story edge labelling:** cards show **Raw relation records** (from `stories.csv`) and **Aggregated network edges**
  (aggregated undirected graph) separately; density, average degree and centralization are labelled as aggregated-graph
  values; T03 and `story_metrics.json` carry both counts. The root cause (an ambiguous `_m` merge suffix) was fixed at the source.
- **Other:** all 332 actors are listed on the filterable Characters index; scientific numbers come from
  `outputs/results_registry.json` (the build fails if a required value is missing); the Reproduce page documents the
  complete path and no longer names the transient branch; `run_pipeline.py --all` now includes `results_registry`,
  `build_site` and `validate_site`.

# Robustness wording

Exact corrected interpretation: for **G0_full (311 nodes)** the largest connected component (LCC) is compared with two
separately labelled bases. Against **all 311 G0 nodes** (LCC < 50% of 311): random removal needs 25.1% of nodes (78);
targeted removal, checked after every removal, needs 6–7 nodes (degree, over 200 random tie-breaks among equal-degree
nodes) and 6 nodes (hop-count betweenness). Against the **261-node initial giant component** (LCC < 50% of 261): random
30.9% (96 nodes); targeted 9 nodes. Removing 10% thresholds: 17 nodes for both targeted strategies (degree tie-break range
15–17). The old grid figures (degree 12 vs betweenness 6 nodes; 3.9% vs 1.9%) are 6-node-checkpoint artifacts, so **no claim is
made that one targeted strategy is more destructive than the other**; the supported conclusion is only that targeted
removal is substantially more disruptive than random removal (G0_full only; graph connectivity, not narrative
resilience). T11 now labels the basis and gives grid and exact crossings; F18's y-axis ("largest component / original network
size") was already correct.

# Stale counts

Derived or removed, and enforced by `tests/test_text_consistency.py` / `tests/test_site_consistency.py`: manifest entries
(207, was "192"), pipeline stages (27, was "19"/"23"), tests collected (53, was "18"), node types (187 `kişi` / 124 `grup` /
21 other — the old "125 group / 20 other" counted the merged duplicate), canonical nodes (332), pages (360), stories (14),
network variants (12), and the G2 component figures on the site (23 components; 261-node giant component; 22 smaller).
Prose no longer duplicates volatile counts; they live in `outputs/results_registry.json`, `outputs/manifest_sha256.csv` and
`outputs/validation/site_validation_report.json`.

# Validation (final regenerated state)

`python run_pipeline.py --all` (FULL mode; n_random = 1000): **27/27 stages PASS** (7 min 13 s); `pytest` 53/53 PASS;
`run_pipeline.py --all --validate-only` PASS; `validate_site.py` 360 files, 0 issues; `validate_release_consistency.py` PASS;
manifest: 207 entries, 0 hash mismatches, 0 missing; `data/raw`, `data/final`, `data/story_level` byte-identical to `main`.
All scientific outputs other than those listed above (null-model FDR table, communities, story similarity and cluster
validity, corpus metrics, T01/T02/T05–T09) are byte-identical to the reviewed state. Run-metadata-only churn (SVG dates/ids
for unchanged figures) was not committed.

# Remaining publication blockers

Explicitly unresolved and **not** closable by code (owner/manual action):

1. **Source edition/transcription metadata** — needs the repository owner (`validation/source_edition_metadata_required.md`).
2. **Second annotator / inter-annotator reliability** — needs a real second coder; no value is fabricated.
3. **Manual review of unresolved entity items** — the 121-row `HUMAN_REVIEW_QUEUE.csv`, including the 46 candidate composite
   nodes; needs the original text.
4. **`CITATION.cff` owner metadata** — author and release-date `TODO`s.
5. **Source-code licence** — the dataset is CC BY 4.0; no code licence was chosen.
6. **Manuscript** — Introduction, Discussion and References unwritten; no literature review.

State when this fix pass ended (`e5989c3`): not pushed, not merged, no Pages deployment, no tag or release. Recommended
next step at that time: independent re-review of `claude-dk-fixpass` — done; see the final section below.

# Independent re-review and final merge-prep cleanup

**Independent re-review** (of `e5989c3`, after the branch was pushed): **READY FOR TECHNICAL MERGE** — 0 critical and 0 major
issues; the Top-5 findings were re-derived from code and data, 5/5 verified; a clean-clone `python run_pipeline.py --all`
ran 27/27 stages PASS with only cosmetic regeneration drift (timestamps, SVG ids, LF/CRLF line endings, float noise ≤ 1e-13).
It listed seven minor items. Status of each after the final merge-prep commit (no scientific output, canonical data or
methodology changed; `data/raw`, `data/final`, `data/story_level` untouched):

| # | Minor item | Status |
|---|---|---|
| 1 | Release-consistency validator hard-coded 363 pages / 18 tests | **FIXED** — every value is derived (page set from `site_layout.NAV_ITEMS` + data, test count from the registry, node/story counts from the data) and cross-checked; `tests/test_release_consistency.py` blocks typed counts |
| 2 | `paper/manuscript_outline.md` pre-correction sensitivity values and a transient branch name | **FIXED** — values from `outputs/results_registry.json` (0.911 / 0.912 tied, 0.952, min 0.849), "no winner" wording, repository-neutral availability text |
| 3 | Stale "never pushed / local only" status text | **FIXED** — `NEXT_TASK.md`, `project_state.json`, `RELEASE_CHECKLIST.md`, `FINAL_REBUILD_REPORT.md`, `EXECUTIVE_SUMMARY.md`, handoff |
| 4 | Residual hard-coded site numbers | **FIXED** — G2 component count, story-unit count, "/ N" corpus order and "of N pairs" (site caption and F11 figure title) are derived; the F11 display limit (15) stays a named UI constant shared by generator and figure |
| 5 | Composite detector misses "Egreke Yol Gösterdi", "Kayın Ata - Kayın Anası" | **DOCUMENTED, intentionally not changed** — heuristic/under-inclusive by design (`docs/limitations.md` §11, `src/composite_nodes.py`); the 46 candidates and the 121-row queue are unchanged because the queue is regenerated by the pipeline and changing the detector was out of scope; the publication blocker stays open |
| 6 | Two tracked machine-specific absolute paths | **FIXED** — handoff and `project_state.json`; a test blocks new ones |
| 7 | Old betweenness 0.3879 in `reports/15_16_web_portal_report.md` | **FIXED** — labelled PRE-FIX / SUPERSEDED with a pointer to DEC-017 and T04 |

Stale-value sweep (363, 18 tests, 19/23 stages, 192, 125 grup, "5 concatenated/composite", the pre-fix betweenness value, 0.930, 0.887, 0.926,
`claude-dk-rebuild`, "never pushed", "local only"): every remaining hit is CURRENT VALID (e.g. ρ 0.926 is person+group PageRank
in the current sensitivity table), HISTORICAL/AUDIT (decision log, session handoff, changelog, per-phase reports, this report,
each identified as historical or carrying an update note) or NEGATING/EXPLANATORY ("was 192", "earlier value 0.930"); the
STALE ERRORS found (the validator constants, outline values, status text, the architecture diagram's "18 tests" / "363-page"
labels, the absolute paths and the unlabelled pre-fix betweenness value) were corrected.
