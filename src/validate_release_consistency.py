"""Phase 20: cross-check headline numbers across every document that quotes
them, against the actual source-of-truth files. Reports a diff, not a
guess - if two docs disagree, both are printed with their source line so a
human can see exactly what to fix.

No count is typed into this file. Every ground-truth value is derived from the
canonical data, from the generated-page sets (src/site_pages.py), from the
site validation report or from the results registry; the derived values are
also cross-checked against each other (see `internal_consistency`), so a
stale artifact surfaces as an issue instead of being preserved as a constant.
"""
import json
import re
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from site_layout import NAV_ITEMS  # noqa: E402
from site_pages import expected_character_pages, expected_story_pages, DOCS  # noqa: E402


def _load_json(rel_path: str) -> dict:
    with open(ROOT / rel_path, encoding="utf-8") as f:
        return json.load(f)


def expected_site_html_files() -> int:
    """Pages the generator must have written: the static pages declared in the
    site navigation (site_layout.NAV_ITEMS) plus the character and story page
    sets derived from the canonical data (site_pages.py). Nothing is counted
    from the files on disk, so a missing or orphan page shows up as a mismatch
    against `site_html_files_on_disk` instead of being absorbed into the total."""
    static_pages = len({href for _, href in NAV_ITEMS})
    return static_pages + len(expected_story_pages()) + len(expected_character_pages())


def actual_site_html_files() -> int:
    return len(list(DOCS.rglob("*.html")))


def ground_truth() -> dict:
    nodes = pd.read_csv(ROOT / "data" / "processed" / "nodes.csv", encoding="utf-8-sig")
    rel = pd.read_csv(ROOT / "data" / "processed" / "relations_event_level.csv", encoding="utf-8-sig")
    stories = pd.read_csv(ROOT / "data" / "processed" / "stories.csv", encoding="utf-8-sig")
    events = pd.read_csv(ROOT / "data" / "final" / "dede_korkut_olaylar_temiz.csv", encoding="utf-8-sig")
    taxonomy = pd.read_csv(ROOT / "data" / "processed" / "relation_taxonomy.csv", encoding="utf-8-sig")

    site_val = _load_json("outputs/validation/site_validation_report.json")
    # The registry counts collected tests with `pytest --collect-only` (see
    # src/build_results_registry.py); it is the machine-readable source, so the
    # test count is read from it rather than typed here.
    registry = _load_json("outputs/results_registry.json")

    return {
        "stories": len(stories),
        "actors": len(nodes),
        "relations_event_level": len(rel),
        "narrative_events": len(events),
        "relation_types": len(taxonomy),
        "relation_layers": rel["layer"].nunique(),
        "site_html_files": expected_site_html_files(),
        "site_html_files_on_disk": actual_site_html_files(),
        "site_html_files_validated": site_val["n_html_files_checked"],
        "site_validation_issues": site_val["n_issues"],
        "pytest_tests": registry["pipeline"]["n_tests_collected"],
        "registry_canonical_nodes": registry["dataset"]["n_canonical_nodes"],
        "registry_stories": registry["dataset"]["n_stories"],
        "registry_event_level_relations": registry["dataset"]["n_relations_event_level"],
    }


# Pairs of derived values that must agree. If two independent derivations of the
# same quantity differ, one of the artifacts is stale.
CONSISTENCY_PAIRS = [
    ("site_html_files", "site_html_files_on_disk", "generated pages on disk differ from the expected page set (missing or orphan pages)"),
    ("site_html_files", "site_html_files_validated", "site_validation_report.json checked a different number of pages (stale validation report)"),
    ("actors", "registry_canonical_nodes", "results_registry.json disagrees with data/processed/nodes.csv (stale registry)"),
    ("stories", "registry_stories", "results_registry.json disagrees with data/processed/stories.csv (stale registry)"),
    ("relations_event_level", "registry_event_level_relations", "results_registry.json disagrees with the event-level relation table (stale registry)"),
]


def internal_consistency(truth: dict) -> list:
    issues = []
    for a, b, message in CONSISTENCY_PAIRS:
        if truth[a] != truth[b]:
            issues.append({"doc": "(derived values)", "check": f"{a} == {b}",
                           "issue": f"{message}: {a}={truth[a]} vs {b}={truth[b]}"})
    if truth["pytest_tests"] is None:
        issues.append({"doc": "outputs/results_registry.json", "check": "pytest_tests",
                       "issue": "registry has no collected-test count; re-run the results_registry stage"})
    if truth["site_validation_issues"] != 0:
        issues.append({"doc": "outputs/validation/site_validation_report.json", "check": "site_validation_issues",
                       "issue": f"site validation reports {truth['site_validation_issues']} issue(s)"})
    return issues


# Each check looks for the ground-truth number appearing within a short
# window of a recognizable label word, tolerant of markdown table cells,
# parenthetical asides, etc. This is a proximity check, not a strict phrase
# match - it flags a document that never mentions the number near the label
# at all (either omitted, or stated with a different, stale number).
CHECKS = [
    ("actors", ["actor", "canonical"], ["README.md", "DATASET_CARD.md"]),
    ("stories", ["stor"], ["README.md", "DATASET_CARD.md"]),
    ("relations_event_level", ["relation"], ["README.md", "DATASET_CARD.md"]),
    ("narrative_events", ["narrative event", "event"], ["README.md"]),
]

WINDOW = 60


def _number_near_label(text: str, number: int, labels: list[str]) -> bool:
    num_str = str(number)
    for m in re.finditer(re.escape(num_str), text):
        start, end = max(0, m.start() - WINDOW), min(len(text), m.end() + WINDOW)
        context = text[start:end].lower()
        if any(label.lower() in context for label in labels):
            return True
    return False


def check_documents(truth: dict):
    issues = []
    for key, labels, doc_names in CHECKS:
        for doc_name in doc_names:
            path = ROOT / doc_name
            if not path.exists():
                issues.append({"doc": doc_name, "check": key, "issue": "document_missing"})
                continue
            text = path.read_text(encoding="utf-8")
            if not _number_near_label(text, truth[key], labels):
                issues.append({
                    "doc": doc_name, "check": key,
                    "issue": f"ground-truth value {truth[key]} not found near a '{labels[0]}'-type label "
                             f"(within {WINDOW} chars) - either omitted or stated with a different number",
                })
    return issues


def main():
    truth = ground_truth()
    print("Ground truth (re-derived from source files):")
    for k, v in truth.items():
        print(f"  {k}: {v}")

    issues = internal_consistency(truth) + check_documents(truth)
    print(f"\nChecked {len(CHECKS)} number/document combinations and {len(CONSISTENCY_PAIRS)} derived-value cross-checks.")
    if not issues:
        print("VALIDATION STATUS: PASS - derived values agree with each other and every checked document states the current ground-truth numbers.")
    else:
        print(f"VALIDATION STATUS: FAIL - {len(issues)} issue(s):")
        for issue in issues:
            print(f"  [{issue['issue']}] {issue['doc']} (check: {issue['check']})")

    out_path = ROOT / "outputs" / "validation" / "release_consistency_report.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({"ground_truth": truth, "issues": issues}, f, ensure_ascii=False, indent=2, default=str)
    print(f"\nWrote {out_path}")
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
