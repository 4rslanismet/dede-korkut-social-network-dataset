"""Phase 16: website validation (section 105).

Crawls every generated HTML file under docs/, extracts href/src attributes,
and checks that every internal (non-http, non-mailto, non-anchor-only)
reference resolves to an actual file on disk. Also checks that every
docs/data/*.json file referenced by a <script> fetch() call exists and is
valid JSON, and that every image referenced actually exists.

This does not require a running server - it resolves paths exactly the way
a static file server would (relative to the referencing HTML file's own
directory), which is what matters for GitHub Pages.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

LINK_ATTR_RE = re.compile(r'(?:href|src)="([^"]+)"')
FETCH_RE = re.compile(r'fetch\("([^"]+)"')


def is_external(url: str) -> bool:
    return url.startswith(("http://", "https://", "mailto:", "#", "//"))


def check_html_file(html_path: Path) -> list[dict]:
    issues = []
    text = html_path.read_text(encoding="utf-8")
    base_dir = html_path.parent

    refs = LINK_ATTR_RE.findall(text) + FETCH_RE.findall(text)
    for ref in refs:
        if is_external(ref):
            continue
        clean = ref.split("#")[0].split("?")[0]
        if not clean:
            continue
        target = (base_dir / clean).resolve()
        if not target.exists():
            issues.append({
                "file": str(html_path.relative_to(ROOT)),
                "reference": ref,
                "resolved_path": str(target.relative_to(ROOT)) if ROOT in target.parents else str(target),
                "issue": "missing_file",
            })
    return issues


def check_json_files() -> list[dict]:
    issues = []
    data_dir = DOCS / "data"
    if not data_dir.exists():
        return [{"file": "docs/data", "issue": "missing_directory", "reference": "docs/data"}]
    for path in data_dir.rglob("*.json"):
        try:
            with open(path, encoding="utf-8") as f:
                json.load(f)
        except json.JSONDecodeError as e:
            issues.append({"file": str(path.relative_to(ROOT)), "issue": "invalid_json", "reference": str(e)})
    return issues


def check_nav_consistency() -> list[dict]:
    """Every page in NAV_ITEMS should exist, and every top-level page should
    include the full nav (checked implicitly since they all use site_layout.page)."""
    import sys
    sys.path.insert(0, str(ROOT / "src"))
    from site_layout import NAV_ITEMS

    issues = []
    for label, href in NAV_ITEMS:
        target = DOCS / href
        if not target.exists():
            issues.append({"file": "site_layout.NAV_ITEMS", "reference": href, "issue": "missing_nav_target"})
    return issues


def main():
    all_issues = []
    html_files = list(DOCS.rglob("*.html"))
    for html_path in html_files:
        all_issues.extend(check_html_file(html_path))

    all_issues.extend(check_json_files())
    all_issues.extend(check_nav_consistency())

    print(f"Checked {len(html_files)} HTML files under docs/.")
    if not all_issues:
        print("VALIDATION STATUS: PASS - no broken internal links, missing assets, or invalid JSON found.")
    else:
        print(f"VALIDATION STATUS: FAIL - {len(all_issues)} issue(s) found:\n")
        for issue in all_issues:
            print(f"  [{issue['issue']}] {issue['file']}  ->  {issue['reference']}")

    out_path = ROOT / "outputs" / "validation" / "site_validation_report.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({"n_html_files_checked": len(html_files), "n_issues": len(all_issues), "issues": all_issues},
                   f, ensure_ascii=False, indent=2)
    print(f"\nWrote {out_path}")

    return 0 if not all_issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
