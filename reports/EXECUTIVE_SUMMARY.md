# Executive Summary

**Read time: ~4 minutes.** Full detail in `reports/FINAL_REBUILD_REPORT.md`.

**Status: technically validated — ready for PR / technical merge review; publication blockers remain** (the
project is not publication-ready; see "What Should Happen Next").

## What Was Done

Starting from an existing, manually coded dataset of characters and relations in the Book of Dede
Korkut (14 stories, 333 actors, 628 relations), this project built a complete, reproducible
research pipeline: a repository audit that re-verified every claimed statistic rather than
trusting documentation; a structural data-validation framework; a canonical dataset with tracked
provenance; twelve network model variants; descriptive, community, signed, directed, multilayer,
and narrative-order analysis; statistical validation via null models with multiple-testing
correction; sensitivity and structural-robustness testing; publication figures and tables; an
interactive website with a profile page for every actor and story; and a documentation, paper and
thesis package (the paper package is an outline, methods, results and supplement — not a finished
manuscript). Every stage is an independently re-runnable script, orchestrated by one command
(`python run_pipeline.py --all`, which also builds and validates the website) and covered by automated tests.
The work was independently reviewed; that review's findings were corrected in a fix pass (below).

## What Was Found

The project's most important result is methodological rather than literary: a plausible-looking
descriptive finding — that this corpus's actor networks are "disassortative" (hubs avoid
connecting to other hubs) — **did not survive statistical validation against a null model** and
was withdrawn as unsupported. By contrast, the community structure detected by standard algorithms
**was** validated as a non-random signal beyond what the degree sequence alone would produce, in
7 of 9 tested network specifications (which are related and partly nested, so not seven independent
replications), and on the largest connected component alone. Separately, systematic sensitivity
testing (weighted betweenness computed with distance = 1/tie strength) showed that actor-type
inclusion (person+group vs. person-only) and edge weighting change which characters appear most
"central" more than the other choices tested; those two are numerically tied (mean Spearman ρ 0.911
vs. 0.912), so neither is singled out, and the remaining choices barely matter. The network was also
shown to be structurally robust to random disruption but fragile to a small number of targeted
removals (targeted removal is far more disruptive; degree- vs betweenness-targeted is not ranked),
consistent with its hub-dominated structure. The story-similarity analysis (RQ6) is exploratory:
actor overlap between stories is low and evidence for discrete story clusters is limited.

Data-quality issues were surfaced honestly rather than hidden: an ~80-row gap between two stages of
the legacy dataset with no documented explanation, and 46 canonical actor labels flagged by a
reproducible scan as candidate composite nodes (comma lists, "X ve Y" constructions, sentence-like
names that may denote several actors; 3.8% of relation endpoints). Neither was silently corrected;
both are logged for manual review.

## What the Independent Review Changed

An independent review of the pushed state found one methodological error and several disclosure and
consistency gaps; all were corrected on the `claude-dk-fixpass` branch: weighted betweenness had used
tie strength as path distance (now 1/strength; Salur Kazan stays first everywhere, but the claim that
Bamsı Beyrek also leads betweenness in every specification was withdrawn); the composite-node
disclosure was under-inclusive (5 → 46 candidates); and the website's stale pages, hand-typed numbers
and ambiguous robustness wording were fixed. No headline finding was reversed. A second, independent
re-review of `claude-dk-fixpass` (at `e5989c3`) re-derived the results from the code and data, found no
critical or major issues, verified the Top-5 findings 5/5 and listed seven minor cleanup items, which the
final merge-prep commit addresses (last section of `reports/FIX_PASS_REPORT.md`).

## What the Scientific Contribution Is

1. A demonstration, with a specific worked example, that literary/narrative network studies should
   subject descriptive structural claims (especially assortativity-type statistics) to null-model
   validation before treating them as findings — a plausible pattern can fail this test.
2. A validated (not merely observed) community structure in this corpus.
3. A quantified answer to "how much does my modeling choice matter": of six construction decisions
   tested, actor-type inclusion and edge weighting change centrality rankings noticeably (ρ 0.85-0.96)
   and three others negligibly (ρ ≥ 0.98).
4. A fully reproducible, provenance-tracked canonical dataset and pipeline that can be extended or
   re-audited by others, rather than a one-off analysis.

## What Should Happen Next

Publication blockers (owner or manual action required — none can be closed by the pipeline):

1. Obtain a second, independent coder to compute a genuine inter-annotator reliability statistic
   (the sampling and tooling are already built and waiting).
2. Manually review the 46 candidate composite actor nodes and the other open items in
   `validation/HUMAN_REVIEW_QUEUE.csv` against the original narrative text. The composite scan is a
   heuristic and under-inclusive by design, so the review should cover the whole node list, not only the
   flagged candidates (`docs/limitations.md` §11).
3. Confirm the source edition/transcription used for the original coding
   (`validation/source_edition_metadata_required.md`).
4. Provide the `CITATION.cff` author and release-date metadata, and decide on a source-code licence
   (the dataset is CC BY 4.0).
5. For a paper: write the Introduction, Discussion and References (no literature review has been done).

Not a blocker: the story-similarity analysis is built and reported as PARTIALLY ANSWERED / EXPLORATORY.
Whether and when to merge to `main` and deploy the website is a decision for the repository owner, who is
asked to review the pull request from `claude-dk-fixpass` into `main` (the branch has already been through an
independent re-review). The paper should not be published before the blockers above are closed.
