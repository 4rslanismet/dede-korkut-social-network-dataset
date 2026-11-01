# Rebuild V2 — Final Report

**Branch**: `claude-complete-rebuild-v2`
**Base**: `main` (SHA 149df2ac)
**Date**: 2026-11-01
**Method**: Complete independent rebuild and verification of the Dede Korkut
Social Network Dataset project.

---

## 1. Objective

Determine whether the entire project can be reproduced from scratch, improve
remaining weaknesses, and leave the repository in a clean, transparent,
academically defensible state.

## 2. Scope

48-section specification covering: Claude Code integration, repository audit,
provenance audit, entity resolution, canonical dataset rebuild, network model
verification, weight semantics, story-level and bipartite networks, descriptive
analysis, centrality, communities, multilayer, signed, directed, narrative-order
analysis, story similarity, null models with FDR, sensitivity, robustness,
motif analysis, inter-annotator protocol, RQ evaluation, claim-evidence matrix,
results registry, figures, tables, pipeline, tests, manifest, website, paper
and thesis packages, literature plan, licensing, citation, scientific and
technical audits, AI transparency.

## 3. Summary of Findings

### 3.1 What Works

| Area | Finding |
|---|---|
| **Canonical dataset** | Byte-identical rebuild from `data/final/` via deterministic scripts |
| **Network models** | All 12 (G0–G11) build correctly with verified properties |
| **Weight semantics** | distance = 1/strength enforced in code + 12 dedicated tests |
| **Null models** | 1000 randomizations, BH-FDR: modularity significant in 7/9 networks |
| **Sensitivity** | 6 paired comparisons; 3 negligible, 3 noticeable (ρ 0.85–0.96) |
| **Robustness** | Betweenness-targeted removal fragments at ~1.9% — hub-dependent |
| **Communities** | Leiden/Louvain agree (ARI 0.899); modularity null-model validated |
| **Pipeline** | 27 stages, all PASS, deterministic (seed 42) |
| **Tests** | 70/70 pass |
| **Website** | 360 HTML files, no broken links |
| **RQ4** | Central confirmatory finding: structure differs from degree-preserving null |

### 3.2 Honest Limitations (All Documented)

| Issue | Status | Impact |
|---|---|---|
| Source edition unknown | UNRESOLVED | Cannot reproduce raw → story_level |
| Inter-annotator agreement | PENDING HUMAN CODER | No second-coder data |
| 53 provenance gaps (8.4%) | DOCUMENTED | event → story_level matching |
| 5 undocumented row dispositions | DOCUMENTED | story_level → final |
| Self-loop DKR0220 | DOCUMENTED | Requires human decision |
| 90 entity candidates | FLAGGED FOR REVIEW | Includes likely typo-duplicates |
| Signed balance insufficient | DOCUMENTED | Only 13 triangles |
| 29.6% uncertain relations | DOCUMENTED | Coded as `belirsiz` in source |
| RQ6 clusters unsupported | DOCUMENTED | Pairwise similarity only |
| Author metadata TODO | PLACEHOLDER | Requires human confirmation |

### 3.3 New Deliverables

| File | Purpose |
|---|---|
| `CLAUDE.md` | Project orientation for AI sessions |
| `docs/AI_ASSISTANCE.md` | AI transparency disclosure |
| `validation/source_baseline_hashes.csv` | Source data integrity protection |
| `validation/entity_review_candidates_v2.csv` | 90 entity candidates (expanded) |
| `validation/HUMAN_REVIEW_QUEUE_V2.csv` | 105-item review queue |
| `outputs/claim_evidence_matrix.csv` | 45 traceable scientific claims |
| `reports/REBUILD_V2_01_REPOSITORY_AUDIT.md` | Independent repository audit |
| `reports/REBUILD_V2_02_PROVENANCE_AUDIT.md` | Provenance chain audit |
| `reports/REBUILD_V2_03_CANONICAL_DATA_DIFF.md` | Canonical dataset diff |
| `reports/REBUILD_V2_04_ANALYSIS_VERIFICATION.md` | Analysis pipeline verification |
| `reports/REBUILD_V2_05_OUTPUTS_AND_INFRASTRUCTURE.md` | Outputs & infrastructure audit |
| `reports/REBUILD_V2_FINAL_REPORT.md` | This report |
| `reports/REBUILD_V2_EXECUTIVE_SUMMARY.md` | Executive summary |
| `reports/REBUILD_V2_RELEASE_CHECKLIST.md` | Release checklist |

## 4. Research Question Assessment

| RQ | Status | Confidence |
|---|---|---|
| RQ1 (structure) | Fully answered | Confirmatory |
| RQ2 (bridges) | Partially answered | Exploratory |
| RQ3 (relation-specific roles) | Fully answered | Confirmatory |
| RQ4 (null-model comparison) | **Fully answered** | **Confirmatory (central finding)** |
| RQ5 (sensitivity) | Fully answered | Descriptive |
| RQ6 (story clustering) | Partially / exploratory | Limited |
| RQ7 (narrative order) | Partially answered | Exploratory |

## 5. Technical Validation

| Check | Result |
|---|---|
| Source data hashes | ✓ Match baseline (23 files) |
| Canonical rebuild | ✓ Byte-identical to main |
| Pipeline 27 stages | ✓ ALL PASS |
| Test suite 70 tests | ✓ ALL PASS |
| Network models 12 | ✓ ALL VERIFIED |
| Weight semantics | ✓ ENFORCED |
| FDR correction | ✓ BH, α=0.05 |
| Determinism | ✓ Seed 42 |
| Website 360 pages | ✓ No broken links |
| Claim-evidence matrix | ✓ 45 claims traced |

## 6. Recommendations Before Merge

### Must-Do (Before Publication)
1. Resolve source edition metadata (human researcher required)
2. Complete inter-annotator agreement (recruit second coder)
3. Fill author metadata in CITATION.cff
4. Review 90 entity candidates (especially 15 high-priority near-duplicates)
5. Set date-released in CITATION.cff

### Should-Do
6. Decide disposition of self-loop DKR0220
7. Document the 5 dropped story-level rows
8. Resolve 53 provenance gaps where possible
9. Review 10 numeric-group-as-kişi misclassifications
10. Execute literature search plan

### Nice-to-Have
11. Add MIT license for code alongside CC-BY-4.0 for data
12. Expand test coverage for edge cases
13. Add CI/CD (GitHub Actions) for automated testing

## 7. Conclusion

The Dede Korkut Social Network Dataset project **passes independent
verification**. The computational pipeline is fully reproducible, the analysis
is methodologically sound with appropriate null-model validation, and all
limitations are honestly documented. The project is in an academically
defensible state for the claims it makes.

The primary publication blockers are non-computational: source edition
metadata, inter-annotator agreement, and author metadata — all requiring
human researcher input.

**Branch `claude-complete-rebuild-v2` is ready for human review.**

---

*This rebuild was performed by Claude (AI assistant) as documented in
`docs/AI_ASSISTANCE.md`. Final scientific responsibility remains with the
human researcher.*
