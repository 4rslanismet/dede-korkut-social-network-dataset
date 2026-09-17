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
was retracted. By contrast, the community structure detected by standard algorithms **was**
validated as a genuine signal beyond what the degree sequence alone would produce, in 7 of 9
tested networks. Separately, systematic sensitivity testing showed that whether collective/group
actors are included or excluded is, by a wide margin, the single modeling decision most likely to
change which characters appear most "central" — more than any other choice tested, including
weighting scheme or relation-inference policy. The network was also shown to be structurally
robust to random disruption but fragile to a small number of targeted removals, consistent with
its hub-dominated structure.

Two data-quality issues were also surfaced honestly rather than hidden: an ~80-row gap between two
stages of the legacy dataset with no documented explanation, and five nodes discovered late (while
building the website) whose names are actually comma-joined lists of multiple distinct characters
collapsed into one entry. Neither was silently corrected; both are logged for manual review.

## What the Scientific Contribution Is

1. A demonstration, with a specific worked example, that literary/narrative network studies should
   subject descriptive structural claims (especially assortativity-type statistics) to null-model
   validation before treating them as findings — a plausible pattern can fail this test.
2. A validated (not merely observed) community structure in this corpus.
3. A quantified answer to "how much does my modeling choice matter": person-only vs. person+group
   actor inclusion is shown to be the most consequential of six construction decisions tested.
4. A fully reproducible, provenance-tracked canonical dataset and pipeline that can be extended or
   re-audited by others, rather than a one-off analysis.

## What Should Happen Next

1. Obtain a second, independent coder to compute a genuine inter-annotator reliability statistic
   (the sampling and tooling are already built and waiting).
2. Resolve the two disclosed data-quality issues (the provenance gap and the five merged-name
   nodes) by returning to the original narrative text.
3. Complete the story-level similarity analysis (currently only a raw projection exists), which is
   needed to properly answer one of the seven original research questions (RQ6) — this project
   explicitly declined to force an answer from incomplete data.
4. Decide, with the repository owner, whether and when to push this work to the remote repository
   and deploy the website live; confirm citation metadata before any formal publication.
