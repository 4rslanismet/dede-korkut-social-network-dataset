# Dede Korkut Narrative Networks

A reproducible, multilayer social-network analysis of characters and relations in the Book of
Dede Korkut — a canonical dataset, a computational study, an evidence package, an interactive
research portal, and an academic research package built on one shared, auditable pipeline.

**This is not a "degree centrality" project.** It is a full research infrastructure: repository
audit and data validation, a canonical data model with tracked provenance, 12 network model
variants, community/signed/directed/multilayer/narrative-order analysis, null-model statistical
validation, sensitivity and structural-robustness testing, publication figures and tables, and an
interactive website (a profile page for every actor and every story) — all generated from the same
source data, all re-runnable with one command.

**Website:** https://4rslanismet.github.io/dede-korkut-social-network-dataset/ (once deployed —
see [Reproduce](docs/reproduce.html))
**Development history:** the rebuild was developed on the `claude-dk-rebuild` and `claude-dk-fixpass`
branches and independently reviewed twice (see [`CHANGELOG.md`](CHANGELOG.md)).
**Status:** technically validated — publication blockers remain (source-edition metadata, second
annotator, manual entity review, `CITATION.cff` owner metadata, code-licence decision, unwritten
Introduction/Discussion/References); the project is not publication-ready. See
[`reports/RELEASE_CHECKLIST.md`](reports/RELEASE_CHECKLIST.md).

## Key Features

- **Canonical dataset** (`data/processed/`) with full provenance tracking back to the legacy
  coding, and an explicit, disclosed record of what could and couldn't be traced.
- **12 network model variants** (G0-G11: full, person-only, core-social, kinship, communication,
  cooperation/support, conflict, positive, negative, directed, weighted, unweighted), each defined
  by one auditable filter rule in `src/networks.py`.
- **Statistically validated findings**: every descriptive structural claim (community structure,
  clustering) was tested against a degree-preserving null model with multiple-testing correction —
  and one earlier finding (a "disassortative network" claim) was retracted after failing that test.
- **Sensitivity-tested**: 6 network-construction choices compared by how much they change centrality
  rankings, so no finding is presented without knowing how fragile it is to modeling decisions.
  Weighted betweenness uses distance = 1/tie strength (DEC-017).
- **Interactive web portal** (`docs/`, GitHub Pages): a Cytoscape.js network explorer, and a
  profile page for every one of the 332 canonical actors — generated, not hand-written.
- **Reproducible end to end**: one seed (`config/analysis.yaml`), one pipeline
  (`run_pipeline.py`, including the website build and validation), automated tests, a SHA-256 hash
  manifest, and a CI validation gate.

## Dataset Snapshot

*(Numbers below are the legacy v3 dataset this rebuild started from; the canonical rebuild has
332 nodes after one entity-resolution merge — see `docs/decision_log.md` DEC-002. Every number
here is re-derived and cross-checked in `reports/01_repository_audit.md`, not hand-typed.)*

| Metric | Value |
|---|---|
| Stories | 14 (13 boy + 1 girizgah) |
| Canonical actors | 332 (333 legacy − 1 merge) |
| Event-level relations | 628 |
| Narrative events | 85 |
| Relation types | 17, mapped to 6 interpretive families |
| Relation layers | 7 |
| Network model variants | 12 (G0-G11) |
| Candidate composite actor nodes (manual review pending) | 46 of 332 (`validation/composite_node_candidates.csv`) |

## Repository Structure

```text
.
├── README.md, LICENSE, CITATION.cff, CHANGELOG.md, CONTRIBUTING.md, DATASET_CARD.md
├── CLAUDE_SESSION_HANDOFF.md, NEXT_TASK.md, project_state.json   # session continuity artifacts
├── requirements.txt, requirements-lock.txt, run_pipeline.py
├── config/analysis.yaml            # seed, algorithm parameters — nothing hardcoded in src/
├── data/
│   ├── raw/                        # immutable original workbook
│   ├── story_level/                # immutable per-story legacy coding
│   ├── final/                      # immutable legacy v3 dataset
│   ├── processed/                  # canonical rebuild (this project's main dataset)
│   └── derived/                    # story-level metrics, etc.
├── src/                            # one script per pipeline stage, each independently runnable
├── tests/                          # pytest suite
├── validation/                     # entity-resolution candidates, human review queue, IAA sample
├── outputs/                        # figures, tables, statistics, networks, validation results
├── reports/                        # one report per project phase (01 through 15-16)
├── docs/                           # the GitHub Pages website + all narrative documentation
├── paper/, thesis/                 # academic output packages (in progress)
└── .github/workflows/validate.yml  # CI: tests + validation-only pipeline pass
```

## Methodology

See [`docs/methodology.md`](docs/methodology.md) for the full pipeline description (detailed
enough to serve as a thesis methods-section source), [`docs/network_models.md`](docs/network_models.md)
for the 12 network definitions, [`docs/decision_log.md`](docs/decision_log.md) for every
non-obvious methodological decision with its rationale, and [`docs/limitations.md`](docs/limitations.md)
for a consolidated, itemized list of everything this project does and does not claim.

## Reproducibility

```bash
git clone https://github.com/4rslanismet/dede-korkut-social-network-dataset.git
cd dede-korkut-social-network-dataset
# to reproduce a specific published state, check out its release tag or commit
python -m venv .venv && .venv\Scripts\activate   # or: source .venv/bin/activate
pip install -r requirements.txt
python run_pipeline.py --all      # analysis, figures/tables, manifest, website build + validation
python -m pytest tests/
```

Full detail: [`docs/reproduce.html`](docs/reproduce.html).

## Website

The `docs/` directory is a complete, self-contained GitHub Pages site (Home, Dataset,
Methodology, Network Explorer, Stories, Characters, Layers, Communities, Similarity, Analysis,
Evidence, Downloads, Reproduce, About) built entirely from this repository's own pipeline outputs
— see [`reports/15_16_web_portal_report.md`](reports/15_16_web_portal_report.md).

## Citation

See [`CITATION.cff`](CITATION.cff). Author/publication metadata there is intentionally marked
`TODO` where genuinely unconfirmed — nothing is invented.

## License

The **dataset** is licensed CC BY 4.0 — see [`LICENSE`](LICENSE). A separate licence for the
**source code** has not been chosen yet; that is an open decision for the repository owner and is
not implied by this file.
