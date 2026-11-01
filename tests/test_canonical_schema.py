"""Schema and referential-integrity tests for data/processed/ (section 79)."""
import re


def test_node_id_unique(nodes):
    assert nodes["node_id"].is_unique, "node_id must be unique in nodes.csv"


def test_node_id_format(nodes):
    pattern = re.compile(r"^[a-z0-9_]+$")
    bad = nodes[~nodes["node_id"].astype(str).str.match(pattern)]
    assert bad.empty, f"non-slug node_id values found: {bad['node_id'].tolist()}"


def test_no_duplicate_relation_ids(relations_event_level):
    assert relations_event_level["relation_id"].is_unique


def test_edge_endpoints_reference_existing_nodes(nodes, relations_event_level):
    node_ids = set(nodes["node_id"])
    missing_source = ~relations_event_level["source_id"].isin(node_ids)
    missing_target = ~relations_event_level["target_id"].isin(node_ids)
    assert not missing_source.any(), (
        f"{missing_source.sum()} relations reference a source_id not in nodes.csv"
    )
    assert not missing_target.any(), (
        f"{missing_target.sum()} relations reference a target_id not in nodes.csv"
    )


def test_no_missing_endpoints(relations_event_level):
    assert relations_event_level["source_id"].notna().all()
    assert relations_event_level["target_id"].notna().all()


def test_stories_have_unique_ids(stories):
    assert stories["story_id"].is_unique
    assert stories["source_file"].is_unique


def test_weight_within_expected_range(relations_event_level):
    w = relations_event_level["weight"].dropna()
    assert (w >= 1).all() and (w <= 5).all(), "agirlik/weight expected to stay within the observed 1-5 coding scale"


def test_relation_family_top_is_known_category(relations_event_level):
    known = {"SOCIAL", "KINSHIP", "AUTHORITY", "SEMANTIC", "OTHER", "UNCERTAIN"}
    observed = set(relations_event_level["relation_family_top"].dropna().unique())
    assert observed <= known, f"unexpected relation_family_top values: {observed - known}"
