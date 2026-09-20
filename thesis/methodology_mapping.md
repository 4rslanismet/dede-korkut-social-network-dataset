# Methodology Mapping

Maps each thesis chapter/research question to the exact script(s) and report(s) that implement
and document it — so a thesis author can trace any methodological claim back to runnable code.

| Thesis Topic | RQ | Script(s) | Report(s) |
|---|---|---|---|
| Repository audit, provenance | Ch.3 | `src/audit.py` | `reports/01_repository_audit.md` |
| Data validation | Ch.3 | `src/validate.py`, `src/entity_resolution.py` | `reports/02_data_quality_report.md` |
| Canonical dataset construction | Ch.3 | `src/build_canonical.py` | `reports/03_canonical_dataset_report.md` |
| Network model definitions (G0-G11) | Ch.4 | `src/networks.py`, `src/build_networks.py` | `docs/network_models.md` |
| Story-level & bipartite networks | Ch.4, RQ2 | `src/story_networks.py` | `docs/network_models.md` |
| Descriptive metrics & centrality | Ch.5, RQ1 | `src/metrics.py` | `reports/04_05_network_construction_and_descriptive_report.md` |
| Community detection (Leiden/Louvain) | Ch.5, RQ1 | `src/communities.py` | `reports/06_advanced_network_analysis_report.md` §1 |
| Signed network analysis | Ch.7, RQ2 | `src/signed_and_directed.py` | `reports/06...` §2 |
| Directed network / HITS / triad census | Ch.5/7, RQ1 | `src/signed_and_directed.py` | `reports/06...` §3 |
| Multilayer/versatility analysis | Ch.7, RQ2 | `src/multilayer.py` | `reports/06...` §4 |
| Narrative-order windowing, dynamic centrality | Ch.7, RQ7 | `src/narrative_order.py` | `reports/06...` §5-6 |
| Null-model statistical validation | Ch.5, RQ4 | `src/null_models.py`, `src/null_models_fdr.py` | `reports/07_null_models_report.md` |
| Sensitivity analysis | Ch.6, RQ5 | `src/sensitivity.py` | `reports/08_sensitivity_robustness_report.md` §1-2 |
| Structural robustness | Ch.6, RQ5 | `src/robustness.py` | `reports/08...` §3 |
| Motif/triad decision (skipped) | Ch.7 | — (see `docs/decision_log.md` DEC-010) | `reports/09_12_figures_tables_report.md` §1 |
| Figures | Ch.5-7 | `src/visualization.py` | `reports/09_12_figures_tables_report.md` §2 |
| Publication tables | Ch.5-7 | `src/export_tables.py` | `reports/09_12_figures_tables_report.md` §3 |
| Inter-annotator infrastructure | Ch.9 (future work) | `src/build_inter_annotator_sample.py`, `src/inter_annotator_stats.py` | `reports/13_14_reproducibility_report.md` §1 |
| Reproducibility pipeline | Ch.4 | `run_pipeline.py`, `tests/` | `reports/13_14...` §2 |
| Web portal | Appendix / companion | `src/build_site_data.py`, `src/build_site.py`, `src/validate_site.py` | `reports/15_16_web_portal_report.md` |
| Story similarity (RQ6, exploratory) | Ch.7 | `src/story_similarity.py`, `src/story_similarity_validity.py` (post-project) | `docs/decision_log.md` DEC-014, DEC-015, `thesis/results_mapping.md` RQ6 |

Every methodological decision referenced implicitly above (e.g., *which* null model, *which*
aggregation rule) is documented explicitly with its rationale in `docs/decision_log.md`
(DEC-001 through DEC-013) — cite by decision number in the thesis text rather than re-deriving the
rationale.
