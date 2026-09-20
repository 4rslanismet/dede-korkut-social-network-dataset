"""Tie strength vs. shortest-path distance (DEC-017).

The edge attribute `weight` is tie STRENGTH (larger = stronger). NetworkX
shortest-path functions read their `weight=` argument as DISTANCE. These tests
make sure a stronger tie is always a SHORTER derived distance and that no
source file hands strength directly to a shortest-path betweenness call."""
import re
from pathlib import Path

import networkx as nx
import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]


def test_stronger_tie_is_shorter_distance():
    from networks import strength_to_distance
    assert strength_to_distance(5) == pytest.approx(0.2)
    assert strength_to_distance(1) == pytest.approx(1.0)
    assert strength_to_distance(5) < strength_to_distance(1)


@pytest.mark.parametrize("bad", [0, -1, -0.5, float("nan"), None, "x"])
def test_non_positive_or_invalid_strength_fails_loudly(bad):
    from networks import strength_to_distance
    with pytest.raises(ValueError):
        strength_to_distance(bad)


def test_with_distance_derives_distance_and_keeps_strength():
    from networks import with_distance
    g = nx.Graph()
    g.add_edge("A", "B", weight=5.0)
    g.add_edge("A", "C", weight=1.0)
    h = with_distance(g)
    assert h["A"]["B"]["distance"] == pytest.approx(0.2)
    assert h["A"]["C"]["distance"] == pytest.approx(1.0)
    assert h["A"]["B"]["weight"] == 5.0 and h["A"]["C"]["weight"] == 1.0  # strength preserved
    assert "distance" not in g["A"]["B"]  # input graph not modified


def test_with_distance_rejects_zero_strength_edge():
    from networks import with_distance
    g = nx.Graph()
    g.add_edge("A", "B", weight=0.0)
    with pytest.raises(ValueError):
        with_distance(g)


def _strong_two_hop_graph():
    """A-B and B-C are strong ties (5); the direct A-C shortcut is weak (1).
    With distance = 1/strength the two-hop route A-B-C (0.2+0.2 = 0.4) beats the
    weak direct edge (1.0), so B lies on the shortest A-C path. Passing strength
    as distance would reverse this (direct 1.0 < two-hop 10.0) and give B zero."""
    g = nx.Graph()
    g.add_edge("A", "B", weight=5.0)
    g.add_edge("B", "C", weight=5.0)
    g.add_edge("A", "C", weight=1.0)
    return g


def test_centrality_profile_betweenness_uses_inverse_strength():
    from metrics import centrality_profile
    g = _strong_two_hop_graph()
    nodes = pd.DataFrame({"node_id": ["A", "B", "C"], "canonical_name": ["A", "B", "C"],
                          "node_type": ["kişi"] * 3, "story_count": [1, 1, 1]})
    prof = centrality_profile("synthetic", g, nodes).set_index("node_id")
    assert prof.loc["B", "betweenness"] > 0, "strong ties must form the shortest path through B"
    assert prof.loc["A", "betweenness"] == 0 and prof.loc["C", "betweenness"] == 0
    # what the old (buggy) call would have produced: strength read as distance -> B on no shortest path
    wrong = nx.betweenness_centrality(g, weight="weight", normalized=True)
    assert wrong["B"] == 0
    # hop-count betweenness is reported separately: a triangle has no intermediary at all
    assert prof.loc["B", "betweenness_hop"] == 0


def test_unweighted_variant_betweenness_equals_hop_count(nodes):
    """G11 has all strengths = 1, so its weighted (1/strength) betweenness must
    equal the hop-count column."""
    from metrics import centrality_profile
    from networks import build_all_networks
    g11 = build_all_networks()["G11_unweighted"]
    prof = centrality_profile("G11_unweighted", g11, nodes)
    assert np.allclose(prof["betweenness"], prof["betweenness_hop"])


def test_no_source_passes_strength_directly_to_betweenness():
    """Static guard: betweenness_centrality(..., weight="weight") is forbidden.
    Weighted betweenness must use weight="distance"; hop-count must use weight=None."""
    pat = re.compile(r"betweenness_centrality\s*\([^)]*weight\s*=\s*['\"]weight['\"]", re.S)
    offenders = [str(p.relative_to(ROOT)) for p in (ROOT / "src").glob("*.py")
                 if pat.search(p.read_text(encoding="utf-8"))]
    assert not offenders, f"strength passed as distance to betweenness in: {offenders}"


def test_published_centrality_tables_use_corrected_betweenness(nodes):
    """Guards against stale outputs: the committed G0 centrality table must equal a
    fresh computation with distance = 1/strength (and must NOT match the old
    strength-as-distance values)."""
    from metrics import centrality_profile
    from networks import build_all_networks
    g0 = build_all_networks()["G0_full"]
    fresh = centrality_profile("G0_full", g0, nodes).set_index("node_id")
    published = pd.read_csv(ROOT / "outputs" / "tables" / "centrality_G0_full.csv", encoding="utf-8-sig").set_index("node_id")
    assert "betweenness_hop" in published.columns, "centrality table predates DEC-017 (no betweenness_hop column)"
    common = fresh.index.intersection(published.index)
    assert np.allclose(fresh.loc[common, "betweenness"], published.loc[common, "betweenness"], atol=1e-9)
    old = nx.betweenness_centrality(g0, weight="weight", normalized=True)
    old_series = pd.Series(old).loc[common]
    assert not np.allclose(old_series, published.loc[common, "betweenness"], atol=1e-6)
