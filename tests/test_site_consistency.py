"""Generated-website consistency (DEC-019): expected page sets come from the
current canonical data, story pages keep raw relation records and aggregated
edges apart, and every count the site shows is derived from source data."""
import json
import re
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


def _visible(path: Path) -> str:
    t = path.read_text(encoding="utf-8")
    t = re.sub(r"<script.*?</script>|<style.*?</style>", "", t, flags=re.S)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", t))


def test_no_orphan_or_missing_character_pages():
    from site_pages import CHARACTERS_DIR, expected_character_pages, generated_pages
    expected, generated = expected_character_pages(), generated_pages(CHARACTERS_DIR)
    assert not (generated - expected), f"stale/orphan character pages: {sorted(generated - expected)[:5]}"
    assert not (expected - generated), f"missing character pages: {sorted(expected - generated)[:5]}"


def test_expected_character_page_count_follows_canonical_nodes(nodes):
    from site_pages import expected_character_pages
    assert len(expected_character_pages()) == len(nodes), "safe_filename must give one distinct page per canonical node"


def test_every_character_page_is_reachable_from_the_character_index():
    from site_pages import expected_character_pages
    index = (DOCS / "characters.html").read_text(encoding="utf-8")
    linked = set(re.findall(r'characters/([^"/]+\.html)', index))
    missing = expected_character_pages() - linked
    assert not missing, f"{len(missing)} character pages are not linked from characters.html, e.g. {sorted(missing)[:3]}"


def test_story_pages_match_expected_set():
    from site_pages import STORIES_DIR, expected_story_pages, generated_pages
    assert generated_pages(STORIES_DIR) == expected_story_pages()


def test_story_pages_separate_raw_records_from_aggregated_edges(stories):
    metrics = pd.read_csv(ROOT / "data" / "derived" / "story_level_metrics.csv", encoding="utf-8-sig").set_index("story_id")
    t03 = pd.read_csv(ROOT / "outputs" / "tables" / "publication" / "T03_story_level_statistics.csv", encoding="utf-8-sig").set_index("story_id")
    n_differ = 0
    for _, s in stories.iterrows():
        sid = s["story_id"]
        raw, agg = int(s["n_edges"]), int(metrics.loc[sid, "n_edges"])
        n_differ += raw != agg
        text = _visible(DOCS / "stories" / f"{sid}.html")
        assert re.search(rf"\b{raw}\s+Raw relation records", text), f"{sid}: page does not show {raw} raw relation records"
        assert re.search(rf"\b{agg}\s+Aggregated network edges", text), f"{sid}: page does not show {agg} aggregated edges"
        assert int(t03.loc[sid, "n_relation_records"]) == raw and int(t03.loc[sid, "n_edges_aggregated"]) == agg, f"{sid}: T03 disagrees with source"
    assert n_differ > 0, "sanity: raw and aggregated counts are expected to differ for at least one story"


def test_story_page_density_uses_the_aggregated_graph(stories):
    metrics = pd.read_csv(ROOT / "data" / "derived" / "story_level_metrics.csv", encoding="utf-8-sig").set_index("story_id")
    for sid in stories["story_id"]:
        n, e = int(metrics.loc[sid, "n_nodes"]), int(metrics.loc[sid, "n_edges"])
        if n > 1:
            assert metrics.loc[sid, "density"] == pytest.approx(2 * e / (n * (n - 1)), rel=1e-9), f"{sid}: density is not computed on the aggregated edge count"


def test_site_project_summary_is_derived_from_source_data(nodes, relations_event_level, stories):
    summary = json.loads((DOCS / "data" / "project_summary.json").read_text(encoding="utf-8"))
    ds = summary["dataset"]
    assert ds["actors"] == len(nodes)
    assert ds["relations_event_level"] == len(relations_event_level)
    assert ds["stories"] == len(stories)
    assert ds["relation_layers"] == relations_event_level["layer"].nunique()
    import run_pipeline
    assert summary["pipeline"]["n_stages"] == len(run_pipeline.STAGES)
    index = _visible(DOCS / "index.html")
    for value in (ds["actors"], ds["relations_event_level"], ds["stories"]):
        assert re.search(rf"\b{value}\b", index)


def test_results_registry_matches_source_data(nodes, relations_event_level, relations_aggregated):
    reg = json.loads((ROOT / "outputs" / "results_registry.json").read_text(encoding="utf-8"))
    d = reg["dataset"]
    assert d["n_canonical_nodes"] == len(nodes)
    assert d["n_relations_event_level"] == len(relations_event_level)
    assert d["n_aggregated_pairs"] == len(relations_aggregated)
    assert d["node_type_counts"] == {k: int(v) for k, v in nodes["node_type"].value_counts().items()}
    import run_pipeline
    assert reg["pipeline"]["n_stages"] == len(run_pipeline.STAGES) and reg["pipeline"]["stage_names"] == run_pipeline.STAGE_NAMES


def test_total_generated_page_count_follows_source_data(nodes, stories):
    """Total HTML pages = top-level pages (site_layout.NAV_ITEMS) + one per story + one per canonical node."""
    from site_layout import NAV_ITEMS
    n_top = len(list(DOCS.glob("*.html")))
    assert n_top == len(NAV_ITEMS)
    total = len(list(DOCS.rglob("*.html")))
    assert total == n_top + len(stories) + len(nodes), f"{total} pages on disk vs expected {n_top + len(stories) + len(nodes)}"
    report = json.loads((ROOT / "outputs" / "validation" / "site_validation_report.json").read_text(encoding="utf-8"))
    assert report["n_html_files_checked"] == total and report["n_issues"] == 0


def test_registry_network_counts_match_network_outputs():
    from networks import NETWORK_DEFINITIONS
    reg = json.loads((ROOT / "outputs" / "results_registry.json").read_text(encoding="utf-8"))["networks"]
    summary = json.loads((ROOT / "outputs" / "networks" / "network_summary.json").read_text(encoding="utf-8"))
    assert reg["n_models"] == len(NETWORK_DEFINITIONS) == len(summary)
    for name, s in summary.items():
        assert (reg["models"][name]["n_nodes"], reg["models"][name]["n_edges"]) == (s["n_nodes"], s["n_edges"])


def test_site_generator_has_no_hardcoded_scientific_constants():
    """The generators must not carry typed copies of scientific results (DEC-019)."""
    for name in ("build_site.py", "build_site_data.py"):
        text = (ROOT / "src" / name).read_text(encoding="utf-8")
        for bad in ("18/18", '"n_network_models": 12', '"reproducible": True', "7 of 9", "261-node",
                    "23 connected components", "Spearman &rho; 0.85", "0.37&ndash;0.56", "0.54&ndash;0.79",
                    "23-connected-component", "of 91 pairs", "The 14 stories", "/ 14 ·"):
            assert bad not in text, f"{name} still contains the hard-coded value {bad!r}"
    # the F11 figure code must not carry the pair count either (it is derived from the similarity matrix)
    viz = (ROOT / "src" / "visualization.py").read_text(encoding="utf-8")
    assert "of 91 pairs" not in viz, "src/visualization.py still hard-codes the number of story pairs"


def test_f11_display_limit_is_the_same_in_generator_and_figure_code():
    """'Top N pairs' is a display limit shared by the figure and its site caption; the two copies must agree."""
    limits = []
    for name in ("build_site.py", "visualization.py"):
        m = re.search(r"^F11_TOP_PAIRS\s*=\s*(\d+)", (ROOT / "src" / name).read_text(encoding="utf-8"), flags=re.M)
        assert m, f"src/{name} must define F11_TOP_PAIRS"
        limits.append(int(m.group(1)))
    assert limits[0] == limits[1], f"F11_TOP_PAIRS differs between build_site.py and visualization.py: {limits}"


def test_site_counts_shown_on_pages_come_from_the_data():
    """The stories/methodology pages must show the CURRENT story count, pair count and G2 component count."""
    reg = json.loads((ROOT / "outputs" / "results_registry.json").read_text(encoding="utf-8"))
    n_units, n_pairs = reg["dataset"]["n_stories"], reg["story_similarity"]["n_pairs"]
    n_comp = reg["networks"]["g2_core_social"]["n_components"]
    stories_html = (ROOT / "docs" / "stories.html").read_text(encoding="utf-8")
    assert f"The {n_units} story units" in stories_html
    assert f"{n_comp}-connected-component caveat" in (ROOT / "docs" / "methodology.html").read_text(encoding="utf-8")
    assert f"of {n_pairs} pairs by actor Jaccard" in (ROOT / "docs" / "similarity.html").read_text(encoding="utf-8")
    assert f"/ {n_units} ·" in (ROOT / "docs" / "stories" / "S01.html").read_text(encoding="utf-8")


def test_validate_site_detects_an_orphan_page(tmp_path, monkeypatch):
    """The validator must flag a stale generated page (checked against a scratch copy of the page set)."""
    import site_pages
    fake_dir = tmp_path / "characters"
    fake_dir.mkdir()
    for name in site_pages.expected_character_pages():
        (fake_dir / name).write_text("<html></html>", encoding="utf-8")
    (fake_dir / "stale_old_page.html").write_text("<html></html>", encoding="utf-8")
    monkeypatch.setattr(site_pages, "CHARACTERS_DIR", fake_dir)
    generated = site_pages.generated_pages(fake_dir)
    assert "stale_old_page.html" in (generated - site_pages.expected_character_pages())
    removed = site_pages.remove_stale_pages(fake_dir, site_pages.expected_character_pages())
    assert removed == ["stale_old_page.html"]
    assert site_pages.generated_pages(fake_dir) == site_pages.expected_character_pages()
