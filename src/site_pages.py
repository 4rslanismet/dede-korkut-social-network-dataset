"""Expected generated-page sets for the website (DEC-019).

The set of character and story pages is derived from the CURRENT canonical
data, never hard-coded. The generator (build_site.py) uses it to remove stale
generated pages and to know what to write; validate_site.py and the tests use
the same functions to detect missing or orphan pages."""
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
CHARACTERS_DIR = DOCS / "characters"
STORIES_DIR = DOCS / "stories"


def safe_filename(node_id: str, maxlen: int = 60) -> str:
    """A handful of node_ids in the canonical dataset are pathologically long
    (composite multi-actor labels - see validation/composite_node_candidates.csv).
    Truncate deterministically with a length suffix for filesystem safety; the
    full node_id/canonical_name still appears in the page's content and in the
    JSON exports. Mirrored in docs/assets/explorer.js (DEC-012)."""
    if len(node_id) <= maxlen:
        return node_id
    return f"{node_id[:maxlen]}_{len(node_id)}"


def expected_character_pages() -> set:
    nodes = pd.read_csv(ROOT / "data" / "processed" / "nodes.csv", encoding="utf-8-sig")
    return {safe_filename(n) + ".html" for n in nodes["node_id"]}


def expected_story_pages() -> set:
    stories = pd.read_csv(ROOT / "data" / "processed" / "stories.csv", encoding="utf-8-sig")
    return {f"{s}.html" for s in stories["story_id"]}


def generated_pages(directory: Path) -> set:
    return {p.name for p in directory.glob("*.html")} if directory.exists() else set()


def remove_stale_pages(directory: Path, expected: set) -> list:
    """Delete *.html files in `directory` that are not in `expected`. Only .html
    files directly inside the generated-page directory are touched; nothing else
    (and nothing outside the directory) is ever removed. Returns removed names."""
    removed = []
    if not directory.exists():
        return removed
    for p in sorted(directory.glob("*.html")):
        if p.name not in expected:
            p.unlink()
            removed.append(p.name)
    return removed
