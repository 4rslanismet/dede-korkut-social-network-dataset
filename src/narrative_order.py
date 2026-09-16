"""Phase 6 (cont.): narrative-order network evolution (section 26) and
exploratory dynamic centrality (section 27).

Terminology discipline (explicitly required by section 26): `satir_no` is
treated as *narrative order within a story*, never as chronological time.
Stories where `satir_no` is missing for most rows are excluded and marked
not_applicable rather than silently guessed at."""
from pathlib import Path

import networkx as nx
import pandas as pd

from networks import load_processed

ROOT = Path(__file__).resolve().parents[1]
OUT_TABLES = ROOT / "outputs" / "tables"

MIN_ROWS_FOR_WINDOWS = 6  # need at least ~2 rows/window for 3 windows to be meaningful


def narrative_windows_for_story(story_rel: pd.DataFrame, story_id: str) -> list[dict]:
    valid = story_rel.dropna(subset=["narrative_order"]).sort_values("narrative_order")
    if len(valid) < MIN_ROWS_FOR_WINDOWS:
        return [{
            "story_id": story_id, "window": "not_applicable", "n_rows_with_narrative_order": len(valid),
            "reason": f"fewer than {MIN_ROWS_FOR_WINDOWS} rows with a usable narrative_order (satir_no)",
        }]

    n = len(valid)
    third = n // 3
    windows = {
        "early": valid.iloc[:third],
        "middle": valid.iloc[third: 2 * third if 2 * third > third else third + 1],
        "late": valid.iloc[2 * third if 2 * third > third else third + 1:],
    }

    rows = []
    seen_nodes = set()
    cumulative_edges = 0
    for wname in ["early", "middle", "late"]:
        w = windows[wname]
        if w.empty:
            continue
        active_nodes = set(w["source_id"]).union(set(w["target_id"]))
        new_nodes = active_nodes - seen_nodes
        seen_nodes |= active_nodes
        cumulative_edges += len(w)

        conflict_share = (w["relation_family"] == "conflict").mean() if len(w) else None
        support_share = w["relation_family"].isin(["support", "cooperation"]).mean() if len(w) else None

        rows.append({
            "story_id": story_id,
            "window": wname,
            "n_relations_in_window": len(w),
            "active_nodes_in_window": len(active_nodes),
            "new_nodes_in_window": len(new_nodes),
            "cumulative_edges": cumulative_edges,
            "cumulative_distinct_nodes": len(seen_nodes),
            "conflict_intensity": conflict_share,
            "support_intensity": support_share,
        })
    return rows


def dynamic_centrality_trajectory(rel: pd.DataFrame, stories: pd.DataFrame, top_k: int = 6) -> pd.DataFrame:
    """Cumulative degree of the top-K globally-central characters across
    *corpus reading order* (story 01 -> 14). This tracks the corpus
    presentation order, not real chronology (section 26 rule)."""
    all_deg = pd.concat([
        rel[["source_id"]].rename(columns={"source_id": "node_id"}),
        rel[["target_id"]].rename(columns={"target_id": "node_id"}),
    ]).value_counts("node_id")
    top_nodes = all_deg.head(top_k).index.tolist()

    rows = []
    for node_id in top_nodes:
        cumulative = 0
        for _, srow in stories.sort_values("corpus_order").iterrows():
            story_rel = rel[rel["story_id"] == srow["story_id"]]
            deg_in_story = ((story_rel["source_id"] == node_id) | (story_rel["target_id"] == node_id)).sum()
            cumulative += deg_in_story
            rows.append({
                "node_id": node_id,
                "corpus_order": srow["corpus_order"],
                "story_id": srow["story_id"],
                "degree_in_story": int(deg_in_story),
                "cumulative_degree_corpus_order": int(cumulative),
            })
    return pd.DataFrame(rows)


def main():
    OUT_TABLES.mkdir(parents=True, exist_ok=True)
    nodes, rel = load_processed()
    stories = pd.read_csv(ROOT / "data" / "processed" / "stories.csv", encoding="utf-8-sig")

    all_rows = []
    for _, srow in stories.iterrows():
        story_rel = rel[rel["story_id"] == srow["story_id"]]
        all_rows.extend(narrative_windows_for_story(story_rel, srow["story_id"]))
    windows_df = pd.DataFrame(all_rows)
    windows_df.to_csv(OUT_TABLES / "narrative_order_windows.csv", index=False, encoding="utf-8-sig")
    print(windows_df.to_string(index=False))

    traj = dynamic_centrality_trajectory(rel, stories, top_k=6)
    traj = traj.merge(nodes.set_index("node_id")[["canonical_name"]], left_on="node_id", right_index=True, how="left")
    traj.to_csv(OUT_TABLES / "dynamic_centrality_trajectory.csv", index=False, encoding="utf-8-sig")
    print(f"\nDynamic centrality trajectory: {traj['node_id'].nunique()} characters x {traj['story_id'].nunique()} stories")


if __name__ == "__main__":
    main()
