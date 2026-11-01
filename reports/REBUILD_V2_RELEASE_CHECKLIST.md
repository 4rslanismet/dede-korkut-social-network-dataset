# Rebuild V2 — Release Checklist

## Before Merge to Main

- [x] Branch created from main (SHA 149df2ac)
- [x] Source data hashes verified (23 files)
- [x] Full pipeline runs (27/27 PASS)
- [x] All tests pass (70/70)
- [x] Network models verified (12/12)
- [x] Weight semantics enforced (DEC-017)
- [x] Null models with BH-FDR (36 tests, 12 significant)
- [x] Sensitivity analysis (6 pairs)
- [x] Robustness analysis (3 strategies)
- [x] Community analysis (Leiden + Louvain, ARI 0.899)
- [x] Story similarity (5 matrices, validity audit)
- [x] Website rebuilt and validated (360 files)
- [x] Claim-evidence matrix (45 claims)
- [x] RQ1–RQ7 evaluation complete
- [x] AI transparency documented
- [x] CLAUDE.md created
- [x] No fabricated references
- [x] Claude NOT listed as author
- [x] Manifest hashes generated

## Before Publication (Requires Human)

- [ ] Source edition metadata filled (`validation/source_edition_metadata_required.md`)
- [ ] Inter-annotator agreement completed (second coder)
- [ ] Author metadata in CITATION.cff (given-names, family-names)
- [ ] date-released in CITATION.cff
- [ ] Entity review candidates resolved (90 items, 15 high-priority)
- [ ] Self-loop DKR0220 disposition decided
- [ ] 5 dropped story-level rows documented
- [ ] Human review of rebuild reports

## Deployment (Do NOT Execute Without Human Approval)

- [ ] Merge `claude-complete-rebuild-v2` → `main`
- [ ] Enable GitHub Pages from `docs/`
- [ ] Create version tag
- [ ] Update version in CITATION.cff
