"""Network construction tests (section 79): G0-G11 build without error and
satisfy the structural invariants documented in docs/network_models.md."""
import pytest


@pytest.fixture(scope="module")
def graphs():
    from networks import build_all_networks
    return build_all_networks()


def test_all_defined_networks_build(graphs):
    from networks import NETWORK_DEFINITIONS
    assert set(graphs.keys()) == set(NETWORK_DEFINITIONS.keys())


def test_g0_is_superset_of_g1_by_node_type(graphs, nodes):
    g0, g1 = graphs["G0_full"], graphs["G1_person_only"]
    person_ids = set(nodes.loc[nodes["node_type"] == "kişi", "node_id"])
    g1_ids = set(g1.nodes())
    assert g1_ids <= person_ids, "G1_person_only must only contain kişi-type nodes"


def test_g9_directed_is_actually_directed(graphs):
    import networkx as nx
    assert graphs["G9_directed"].is_directed()
    for name, g in graphs.items():
        if name != "G9_directed":
            assert not g.is_directed(), f"{name} should be undirected"


def test_no_isolated_nodes_remain_in_any_variant(graphs):
    import networkx as nx
    for name, g in graphs.items():
        isolates = list(nx.isolates(g))
        assert not isolates, f"{name} unexpectedly retains isolated nodes: {isolates[:5]}"


def test_weighted_and_unweighted_share_same_topology(graphs):
    g10, g11 = graphs["G10_weighted"], graphs["G11_unweighted"]
    assert set(g10.edges()) == set(g11.edges())
    assert all(d["weight"] == 1.0 for _, _, d in g11.edges(data=True))
