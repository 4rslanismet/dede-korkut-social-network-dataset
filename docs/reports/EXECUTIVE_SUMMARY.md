# Executive Summary

**Read time: ~4 minutes.** Full detail in `reports/FINAL_REBUILD_REPORT.md`.

## What Was Done

Starting from an existing, manually coded dataset of characters and relations in the Book of Dede
Korkut (14 stories, 333 actors, 628 relations), this project built a complete, reproducible
research pipeline: a repository audit that re-verified every claimed statistic rather than
trusting documentation; a structural data-validation framework; a canonical dataset with tracked
provenance; twelve network model variants; descriptive, community, signed, directed, multilayer,
and narrative-order analysis; statistical validation via null models with multiple-testing
correction; sensitivity and structural-robustness testing; publication figures and tables; a
363-page interactive website; and a full documentation, paper, and thesis package. Every stage is
an independently re-runnable script, orchestrated by one command
(`python run_pipeline.py --all`) and covered by 18 automated tests.

## What Was Found

The project's most important result is methodological rather than literary: a plausible-looking
descriptive finding — that this corpus's actor networks are "disassortative" (hubs avoid
connecting to other hubs) — **did not survive statistical validation against a null model** and
was withdrawn as unsupported. By contrast, the community structure detected by standard algorithms
**was** validated as a non-random signal beyond what the degree sequence alone would produce, in
7 of 9 tested networks (and on the largest connected component alone). Separately, systematic
sensitivity testing showed that actor-type inclusion (person+group vs. person-only, groups included
vs. excluded) and edge weighting change which characters appear most "central" more than the
other three construction choices tested, which barely matter; the three larger-effect choices are
close to one another (mean Spearman ρ 0.91-0.93), so none is singled out as "the" most consequential.
The network was also shown to be structurally robust to random disruption but fragile to a small
number of targeted removals, consistent with its hub-dominated structure. The story-similarity
analysis (RQ6) is exploratory: actor overlap between stories is low and evidence for discrete story
clusters is limited.

Two data-quality issues were also surfaced honestly rather than hidden: an ~80-row gap between two
stages of the legacy dataset with no documented explanation, and five nodes discovered late (while
building the website) whose names are actually comma-joined lists of multiple distinct characters
collapsed into one entry. Neither was silently corrected; both are logged for manual review.

## What the Scientific Contribution Is

1. A demonstration, with a specific worked example, that literary/narrative network studies should
   subject descriptive structural claims (especially assortativity-type statistics) to null-model
   validation before treating them as findings — a plausible pattern can fail this test.
2. A validated (not merely observed) community structure in this corpus.
3. A quantified answer to "how much does my modeling choice matter": of six construction decisions
   tested, actor-type inclusion and edge weighting change centrality rankings noticeably (ρ 0.85-0.96)
   and the other three negligibly (ρ ≥ 0.97).
4. A fully reproducible, provenance-tracked canonical dataset and pipeline that can be extended or
   re-audited by others, rather than a one-off analysis.

## What Should Happen Next

1. Obtain a second, independent coder to compute a genuine inter-annotator reliability statistic
   (the sampling and tooling are already built and waiting).
2. Resolve the two disclosed data-quality issues (the provenance gap and the five merged-name
   nodes) by returning to the original narrative text.
3. ~~Complete the story-level similarity analysis~~ — **built, but only partially answers RQ6**: all
   91 story pairs and 5 similarity metrics are computed, yet actor overlap is low (max Jaccard
   0.153) and cluster-validity checks do not support a robust discrete clustering, so RQ6 is
   PARTIALLY ANSWERED / EXPLORATORY (final academic audit, DEC-015).
4. Decide, with the repository owner, whether and when to push this work to the remote repository
   and deploy the website live; confirm citation metadata before any formal publication.
