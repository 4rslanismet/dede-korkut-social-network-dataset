# Rebuild V2 — Executive Summary

**One-line**: The Dede Korkut Social Network Dataset project passes independent
verification. The pipeline is reproducible, the analysis is sound, and all
limitations are honestly documented.

---

## Key Numbers

- **332** canonical nodes, **628** event-level relations, **376** aggregated pairs
- **12** network model variants (G0–G11), all verified
- **27** pipeline stages, all PASS
- **70** tests, all pass
- **360** website HTML files, no broken links
- **45** scientific claims traced in claim-evidence matrix
- **1000** null-model randomizations with BH-FDR correction

## Central Finding

Modularity is significantly higher than degree-preserving null networks in
**7 of 9** tested variants (BH-FDR, α=0.05). This is the project's strongest,
most defensible result (RQ4).

## What's New in This Rebuild

- **CLAUDE.md** for future AI session orientation
- **AI transparency disclosure** (`docs/AI_ASSISTANCE.md`)
- **Source data hash protection** (23 files, SHA-256)
- **Expanded entity review**: 90 candidates including near-duplicate typos
  (was 46 in existing scan)
- **Claim-evidence matrix**: 45 traceable claims with sources
- **5 independent verification reports** (repository, provenance, canonical
  data, analysis, infrastructure)

## Publication Blockers (Human Required)

1. Source edition metadata — which printed text was coded
2. Inter-annotator agreement — second coder needed
3. Author metadata in CITATION.cff
4. Entity review (90 candidates, 15 high-priority)

## Branch Status

`claude-complete-rebuild-v2` — ready for human review.
NOT merged to main. NOT deployed. NOT tagged.
