"""Phase 4 (cont.): per-story networks (section 15) and the actor x story
bipartite network with its two projections (section 16)."""
import json
from pathlib import Path

import networkx as nx
import pandas as pd

from networks import build_story_graph, load_processed

ROOT = Path(__file__).resolve().parents[1]
OUT_STORIES = ROOT / "outputs" / "networks" / "stories"
OUT_MATRICES = ROOT / "outputs" / "matrices"


def story_level_metrics(nodes: pd.DataFrame, rel: pd.DataFrame, stories: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, srow in stories.iterrows():
        sid = srow["story_id"]
        g = build_story_graph(nodes, rel, sid)
        n = g.number_of_nodes()
        m = g.number_of_edges()
        row = {
            "story_id": sid,
            "source_file": srow["source_file"],
            "boy_name_raw": srow["boy_name_raw"],
            "n_nodes": n,
            "n_edges": m,
            "density": nx.density(g) if n > 1 else None,
            "average_degree": (2 * m / n) if n else None,
            "average_clustering": nx.average_clustering(g) if n > 2 else None,
            "transitivity": nx.transitivity(g) if n > 2 else None,
            "n_connected_components": nx.number_connected_components(g) if n else None,
            "largest_component_size": max((len(c) for c in nx.connected_components(g)), default=0) if n else None,
        }
        if n > 1:
            largest = max(nx.connected_components(g), key=len)
            sub = g.subgraph(largest)
            try:
                row["average_shortest_path_length"] = nx.average_shortest_path_length(sub)
            except Exception:
                row["average_shortest_path_length"] = None
        else:
            row["average_shortest_path_length"] = None

        # Freeman degree centralization (undirected, section 115)
        if n > 2:
            degrees = dict(g.degree())
            max_deg = max(degrees.values())
            max_possible = (n - 1) * (n - 2)
            centralization = sum(max_deg - d for d in degrees.values()) / max_possible if max_possible > 0 else None
            row["degree_centralization"] = centralization
        else:
            row["degree_centralization"] = None

        rows.append(row)

        OUT_STORIES.mkdir(parents=True, exist_ok=True)
        nx.write_graphml(g, OUT_STORIES / f"{sid}.graphml")

    return pd.DataFrame(rows)


def build_bipartite(nodes: pd.DataFrame, rel: pd.DataFrame, stories: pd.DataFrame):
    """Actor x story incidence: an actor is incident to a story if it
    appears as source or target of at least one relation in that story."""
    pairs = set()
    for _, r in rel.dropna(subset=["source_id", "target_id"]).iterrows():
        pairs.add((r["source_id"], r["story_id"]))
        pairs.add((r["target_id"], r["story_id"]))

    B = nx.Graph()
    actor_ids = sorted({p[0] for p in pairs})
    story_ids = sorted({p[1] for p in pairs})
    B.add_nodes_from(actor_ids, bipartite=0)
    B.add_nodes_from(story_ids, bipartite=1)
    B.add_edges_from(sorted(pairs))  # sorted: set iteration order varies between runs (hash randomization)

    incidence = pd.DataFrame(0, index=actor_ids, columns=story_ids)
    for a, s in pairs:
        incidence.loc[a, s] = 1

    return B, incidence


def project_actor(incidence: pd.DataFrame) -> pd.DataFrame:
    """Actor projection: co-occurrence counts (number of shared stories).
    NOTE (section 16): this simple co-occurrence projection is known to
    inflate the apparent connectivity of actors with high story_count —
    reported explicitly in docs/network_models.md, not silently used as
    a definitive social network."""
    mat = incidence.values
    co = mat @ mat.T
    return pd.DataFrame(co, index=incidence.index, columns=incidence.index)


def project_story(incidence: pd.DataFrame) -> pd.DataFrame:
    mat = incidence.values
    co = mat.T @ mat
    return pd.DataFrame(co, index=incidence.columns, columns=incidence.columns)


DOC_MARKER = "\n## Story-level networks"


def update_network_models_doc(n_actors: int, n_stories: int, n_incidences: int):
    """build_networks.py rewrites docs/network_models.md from scratch, which
    used to drop the story-level / bipartite sections (they had been appended
    by hand). This stage now (re)writes them idempotently, with the actor /
    story / incidence counts taken from the data instead of typed in."""
    path = ROOT / "docs" / "network_models.md"
    with open(path, encoding="utf-8") as f:
        text = f.read()
    if DOC_MARKER in text:
        text = text[:text.index(DOC_MARKER)]
    section = f"""
## Story-level networks

Built by [`src/story_networks.py`](../src/story_networks.py): one undirected weighted graph per
`story_id` (S01-S14), built the same way as the aggregated corpus graphs (unordered actor pairs,
`weight` = sum of `agirlik`). Per-story metrics (nodes, edges, density, average degree, clustering,
transitivity, connected components, average shortest path on the giant component, Freeman degree
centralization per section 115) are written to `data/derived/story_level_metrics.csv`. GraphML
exports live in `outputs/networks/stories/<story_id>.graphml`.

`S01` (Girizgah, the prologue) has only 2 nodes/1 edge — degree centralization is undefined (n<3)
and this story is flagged for the girizgah-included-vs-excluded sensitivity arm (section 15, 29).

## Actor x story bipartite network

Built by the same script. An actor is incident to a story if it appears as source or target of at
least one event-level relation in that story (`data/processed/relations_event_level.csv`). Outputs:

- `outputs/matrices/actor_story_incidence.csv` — {n_actors} actors x {n_stories} stories, {n_incidences} incidences
- `outputs/networks/bipartite_actor_story.graphml`
- `outputs/matrices/actor_projection_cooccurrence.csv` — actor x actor co-occurrence counts (shared stories)
- `outputs/matrices/story_projection_shared_actors.csv` — story x story shared-actor counts

**Degree inflation warning (required by section 16):** the actor projection is a simple
co-occurrence count, not a weighted/normalized projection. Actors with a high `story_count` (see
`data/processed/nodes.csv`) will show inflated projected-degree purely as a function of appearing
in many stories, independent of any direct narrative interaction. This projection should be treated
as descriptive only; it is not used as an edge-weighted "social" network for centrality claims
elsewhere in this project."""
    with open(path, "w", encoding="utf-8") as f:
        f.write(text.rstrip("\n") + "\n" + section + "\n")


def main():
    nodes, rel = load_processed()
    stories = pd.read_csv(ROOT / "data" / "processed" / "stories.csv", encoding="utf-8-sig")

    metrics = story_level_metrics(nodes, rel, stories)
    derived_dir = ROOT / "data" / "derived"
    derived_dir.mkdir(parents=True, exist_ok=True)
    metrics.to_csv(derived_dir / "story_level_metrics.csv", index=False, encoding="utf-8-sig")
    print(metrics[["story_id", "n_nodes", "n_edges", "density", "degree_centralization"]].to_string(index=False))

    B, incidence = build_bipartite(nodes, rel, stories)
    OUT_MATRICES.mkdir(parents=True, exist_ok=True)
    incidence.to_csv(OUT_MATRICES / "actor_story_incidence.csv", encoding="utf-8-sig")
    nx.write_graphml(B, ROOT / "outputs" / "networks" / "bipartite_actor_story.graphml")

    actor_proj = project_actor(incidence)
    story_proj = project_story(incidence)
    actor_proj.to_csv(OUT_MATRICES / "actor_projection_cooccurrence.csv", encoding="utf-8-sig")
    story_proj.to_csv(OUT_MATRICES / "story_projection_shared_actors.csv", encoding="utf-8-sig")

    update_network_models_doc(len(incidence.index), len(incidence.columns), B.number_of_edges())

    print(f"\nBipartite: {B.number_of_nodes()} nodes ({len(incidence.index)} actors, {len(incidence.columns)} stories), {B.number_of_edges()} incidences")


if __name__ == "__main__":
    main()
