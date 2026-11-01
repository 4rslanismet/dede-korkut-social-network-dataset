"""Determinism tests (section 79, 78): the same seed must produce the same
result on repeated runs for every stochastic pipeline step."""
import yaml


def _load_seed():
    from pathlib import Path
    root = Path(__file__).resolve().parents[1]
    with open(root / "config" / "analysis.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)["seed"]


def test_leiden_community_detection_is_deterministic_given_seed(graphs=None):
    from networks import build_all_networks
    from communities import nx_to_igraph, run_leiden

    graphs = build_all_networks()
    g = graphs["G2_core_social"]
    ig_g, node_order = nx_to_igraph(g)
    seed = _load_seed()

    membership_1, mod_1 = run_leiden(ig_g, resolution=1.0, seed=seed)
    membership_2, mod_2 = run_leiden(ig_g, resolution=1.0, seed=seed)

    assert membership_1 == membership_2, "Leiden partition must be identical across runs with the same seed"
    assert mod_1 == mod_2


def test_double_edge_swap_randomization_is_deterministic_given_seed():
    import numpy as np
    from networks import build_all_networks
    from null_models import randomized_copy

    graphs = build_all_networks()
    g = graphs["G3_kinship"]
    seed = _load_seed()

    rng_1 = np.random.default_rng(seed)
    rng_2 = np.random.default_rng(seed)
    h1 = randomized_copy(g, rng_1)
    h2 = randomized_copy(g, rng_2)

    assert sorted(h1.edges()) == sorted(h2.edges()), (
        "degree-preserving randomization must be reproducible given the same seed"
    )
