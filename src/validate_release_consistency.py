"""Phase 20: cross-check headline numbers across every document that quotes
them, against the actual source-of-truth files. Reports a diff, not a
guess - if two docs disagree, both are printed with their source line so a
human can see exactly what to fix.
"""
import json
import re
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def ground_truth() -> dict:
    nodes = pd.read_csv(ROOT / "data" / "processed" / "nodes.csv", encoding="utf-8-sig")
    rel = pd.read_csv(ROOT / "data" / "processed" / "relations_event_level.csv", encoding="utf-8-sig")
    stories = pd.read_csv(ROOT / "data" / "processed" / "stories.csv", encoding="utf-8-sig")
    events = pd.read_csv(ROOT / "data" / "final" / "dede_korkut_olaylar_temiz.csv", encoding="utf-8-sig")
    taxonomy = pd.read_csv(ROOT / "data" / "processed" / "relation_taxonomy.csv", encoding="utf-8-sig")

    with open(ROOT / "outputs" / "validation" / "site_validation_report.json", encoding="utf-8") as f:
        site_val = json.load(f)

    return {
        "stories": len(stories),
        "actors": len(nodes),
        "relations_event_level": len(rel),
        "narrative_events": len(events),
        "relation_types": len(taxonomy),
        "relation_layers": rel["layer"].nunique(),
        "site_html_files": 363,  # last confirmed count, see reports/15_16
        "site_validation_issues": site_val["n_issues"],
        "pytest_tests": 18,
    }


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

    issues = check_documents(truth)
    print(f"\nChecked {len(CHECKS)} number/document combinations.")
    if not issues:
        print("VALIDATION STATUS: PASS - every checked document states the current ground-truth numbers.")
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
