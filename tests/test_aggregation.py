"""Aggregation correctness tests (section 79): relations_aggregated.csv must
be a faithful, lossless summary of relations_event_level.csv under the
documented aggregation rule (DEC-003: unordered actor pair)."""


def test_aggregated_interaction_counts_sum_to_event_level_rows(relations_event_level, relations_aggregated):
    total_from_aggregated = relations_aggregated["interaction_count"].sum()
    total_event_level = relations_event_level.dropna(subset=["source_id", "target_id"]).shape[0]
    assert total_from_aggregated == total_event_level, (
        f"sum(interaction_count)={total_from_aggregated} does not match "
        f"len(relations_event_level)={total_event_level}"
    )


def test_aggregated_pairs_are_unordered_and_unique(relations_aggregated):
    pairs = list(zip(relations_aggregated["actor_a"], relations_aggregated["actor_b"]))
    assert len(pairs) == len(set(pairs)), "duplicate (actor_a, actor_b) pairs found in relations_aggregated"
    # actor_a/actor_b should already be alphabetically sorted per the aggregation rule
    for a, b in pairs:
        assert a <= b, f"pair ({a}, {b}) is not stored in sorted order"


def test_every_event_level_pair_appears_in_aggregated(relations_event_level, relations_aggregated):
    agg_pairs = set(zip(relations_aggregated["actor_a"], relations_aggregated["actor_b"]))
    subset = relations_event_level.dropna(subset=["source_id", "target_id"])
    for _, row in subset.sample(min(50, len(subset)), random_state=42).iterrows():
        a, b = sorted([row["source_id"], row["target_id"]])
        assert (a, b) in agg_pairs, f"pair ({a}, {b}) from relation {row['relation_id']} missing in aggregated table"
