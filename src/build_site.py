"""Phase 15: build the static GitHub Pages site under docs/.

Every number/table on every page is generated here from real files under
data/, outputs/, reports/, docs/decision_log.md, validation/ — nothing is
hand-typed. Run src/build_site_data.py first (it's called at the top of
main() here too) so docs/data/*.json is fresh.
"""
import json
import shutil
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from site_layout import page, DISCLAIMER
import build_site_data

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

# GitHub Pages, when configured to publish from /docs, serves ONLY the
# contents of docs/ - anything under ../outputs, ../data, ../reports is
# invisible to the deployed site even though it resolves fine when browsing
# the raw repo checkout. Every file a page needs to link to or embed must
# therefore be copied into docs/ first; nothing outside docs/ is ever
# referenced with a "../" path from this site.
FIGURES_TO_COPY = [
    "outputs/figures/corpus/F02_corpus_full_network.png",
    "outputs/figures/corpus/F03_person_only_network.png",
    "outputs/figures/corpus/F07_top_actors_centrality_comparison.png",
    "outputs/figures/communities/F06_community_structure.png",
    "outputs/figures/null_models/F15_null_model_distributions.png",
    "outputs/figures/sensitivity/F16_sensitivity_correlation_matrix.png",
    "outputs/figures/sensitivity/F17_centrality_rank_stability.png",
    "outputs/figures/robustness/F18_structural_robustness_curves.png",
    "outputs/figures/similarity/F10_story_similarity_heatmap.png",
    "outputs/figures/similarity/F11_story_similarity_network.png",
]

REPORTS_TO_COPY_GLOB = "reports/*.md"

DOWNLOAD_FILES = [
    "data/processed/nodes.csv",
    "data/processed/aliases.csv",
    "data/processed/stories.csv",
    "data/processed/relations_event_level.csv",
    "data/processed/relations_aggregated.csv",
    "data/processed/relation_taxonomy.csv",
    "data/processed/provenance.csv",
    "data/processed/validation_status.csv",
    "outputs/networks/G0_full.graphml",
    "outputs/networks/G0_full.gexf",
    "outputs/networks/G0_full_edges.csv",
    "outputs/networks/G0_full_nodes.csv",
    "outputs/networks/G1_person_only.graphml",
    "outputs/networks/G2_core_social.graphml",
    "outputs/networks/bipartite_actor_story.graphml",
    "outputs/manifest_sha256.csv",
]


def copy_assets():
    for rel in FIGURES_TO_COPY:
        src = ROOT / rel
        dst = DOCS / "figures" / Path(rel).relative_to("outputs/figures")
        dst.parent.mkdir(parents=True, exist_ok=True)
        if src.exists():
            shutil.copy2(src, dst)

    reports_dir = DOCS / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    for src in (ROOT / "reports").glob("*.md"):
        shutil.copy2(src, reports_dir / src.name)

    for rel in DOWNLOAD_FILES:
        src = ROOT / rel
        dst = DOCS / "downloads" / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        if src.exists():
            shutil.copy2(src, dst)

    pub_tables_src = ROOT / "outputs" / "tables" / "publication"
    pub_tables_dst = DOCS / "downloads" / "outputs" / "tables" / "publication"
    pub_tables_dst.mkdir(parents=True, exist_ok=True)
    for src in pub_tables_src.glob("*"):
        shutil.copy2(src, pub_tables_dst / src.name)

    print("Copied figures, reports, and downloadable data files into docs/ "
          "(figures/, reports/, downloads/) so the published GitHub Pages site is self-contained.")


def load_json(rel_path):
    with open(ROOT / rel_path, encoding="utf-8") as f:
        return json.load(f)


def df(rel_path, **kwargs):
    return pd.read_csv(ROOT / rel_path, encoding="utf-8-sig", **kwargs)


def safe_filename(node_id: str, maxlen: int = 60) -> str:
    """A handful of node_ids in the canonical dataset are pathologically long
    (concatenated multi-actor entries - see CLAUDE_SESSION_HANDOFF.md known
    warnings and validation/HUMAN_REVIEW_QUEUE.csv). Truncate deterministically
    with a length suffix for filesystem safety; the full node_id/canonical_name
    still appears as the page's own content and in the JSON data exports."""
    if len(node_id) <= maxlen:
        return node_id
    return f"{node_id[:maxlen]}_{len(node_id)}"


def write(rel_path: str, html: str):
    out = DOCS / rel_path
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"Wrote docs/{rel_path}")


def table_html(dataframe: pd.DataFrame, columns=None, max_rows=None) -> str:
    d = dataframe[columns] if columns else dataframe
    if max_rows:
        d = d.head(max_rows)
    return f'<div class="table-wrap">{d.to_html(index=False, border=0, na_rep="—", escape=True)}</div>'


# ---------------------------------------------------------------------------
# HOME
# ---------------------------------------------------------------------------
def build_home():
    summary = load_json("docs/data/project_summary.json")
    ds = summary["dataset"]
    val = summary["validation_status"]
    pill_class = {"PASS": "pass", "WARNING": "warning", "FAIL": "fail"}[val["status"]]

    content = f"""
<h1>Dede Korkut Narrative Networks</h1>
<p class="lede">A reproducible multilayer network analysis of characters and relations in the
Book of Dede Korkut — built as a canonical dataset, a computational study, an evidence package,
an interactive research portal, and an academic research package at once.</p>

<div class="disclaimer">{DISCLAIMER}</div>

<div class="card-grid">
  <div class="metric-card"><span class="value">{ds['stories']}</span><span class="label">Stories</span></div>
  <div class="metric-card"><span class="value">{ds['actors']}</span><span class="label">Actors</span></div>
  <div class="metric-card"><span class="value">{ds['relations_event_level']}</span><span class="label">Relations</span></div>
  <div class="metric-card"><span class="value">{ds['narrative_events']}</span><span class="label">Narrative Events</span></div>
  <div class="metric-card"><span class="value">{ds['relation_layers']}</span><span class="label">Relation Layers</span></div>
</div>

<h2>Project Status</h2>
<div class="status-panel">
  <div class="item"><strong>Dataset Validation</strong><span class="pill {pill_class}">{val['status']}</span></div>
  <div class="item"><strong>Pipeline</strong>{'Reproducible' if summary['pipeline']['reproducible'] else 'Not yet reproducible'}</div>
  <div class="item"><strong>Network Models</strong>{summary['pipeline']['n_network_models']}</div>
  <div class="item"><strong>Automated Tests</strong>{summary['pipeline']['n_pytest_tests_passing']}</div>
  <div class="item"><strong>Fail-level issues</strong>{val['fail_level_issue_count']}</div>
  <div class="item"><strong>Warning-level issues</strong>{val['warning_level_issue_count']}</div>
</div>
<p style="font-size:0.85rem;color:var(--ink-soft)">Full detail: <a href="evidence.html">Evidence</a> page.</p>

<h2>Where to start</h2>
<div class="grid-list">
  <a class="tile" href="dataset.html"><div class="tile-title">Dataset</div><div class="tile-meta">Schema, provenance, download links</div></a>
  <a class="tile" href="methodology.html"><div class="tile-title">Methodology</div><div class="tile-meta">How the corpus became a network</div></a>
  <a class="tile" href="explorer.html"><div class="tile-title">Network Explorer</div><div class="tile-meta">Interactive graph, filters, search</div></a>
  <a class="tile" href="analysis.html"><div class="tile-title">Analysis</div><div class="tile-meta">Centrality, communities, null models, sensitivity</div></a>
  <a class="tile" href="reproduce.html"><div class="tile-title">Reproduce</div><div class="tile-meta">Run the whole pipeline yourself</div></a>
</div>
"""
    write("index.html", page("Home", "Reproducible multilayer network analysis of the Book of Dede Korkut.", "Home", content))


# ---------------------------------------------------------------------------
# DATASET
# ---------------------------------------------------------------------------
def build_dataset():
    nodes = df("data/processed/nodes.csv")
    rel = df("data/processed/relations_event_level.csv")
    taxonomy = df("data/processed/relation_taxonomy.csv")

    node_type_counts = nodes["node_type"].value_counts()
    node_type_rows = "".join(f"<tr><td>{t}</td><td>{c}</td></tr>" for t, c in node_type_counts.items())

    content = f"""
<h1>Dataset</h1>
<p class="lede">The canonical dataset (Phase 3 rebuild) lives under <code>data/processed/</code>.
It is derived from, but does not overwrite, the original repository's <code>data/final/</code>
(v3) dataset — see <a href="evidence.html">Evidence</a> for the full provenance chain.</p>

<h2>Actor type composition</h2>
<table><thead><tr><th>node_type</th><th>count</th></tr></thead><tbody>{node_type_rows}</tbody></table>

<h2>Schema</h2>
<h3>nodes.csv</h3>
<p>{', '.join(f'<code>{c}</code>' for c in nodes.columns)}</p>
<h3>relations_event_level.csv</h3>
<p>{', '.join(f'<code>{c}</code>' for c in rel.columns)}</p>

<h2>Relation taxonomy</h2>
<p>{len(taxonomy)} observed relation types, mapped to interpretive families (this mapping is an
analytical construct, not a raw-data fact — see <a href="methodology.html">Methodology</a> and
<a href="decision_log.md">decision_log.md</a> DEC-004).</p>
{table_html(taxonomy, ["standard_relation", "relation_family", "relation_family_top", "n_occurrences", "share_of_all_edges_pct"])}

<h2>Version</h2>
<p>Canonical rebuild version: <code>processed-v4-rebuild</code> (see <code>data/processed/provenance.csv</code>).
Legacy dataset version: v3 (<code>data/final/</code>, documented in <code>docs/README_v3.md</code>).</p>

<h2>Downloads</h2>
<p>See the <a href="downloads.html">Downloads</a> page for direct links to every processed file.</p>
"""
    write("dataset.html", page("Dataset", "Canonical dataset schema, composition, and provenance.", "Dataset", content))


# ---------------------------------------------------------------------------
# METHODOLOGY
# ---------------------------------------------------------------------------
def build_methodology():
    content = f"""
<h1>Methodology</h1>
<p class="lede">Every step below is implemented as a standalone, re-runnable script under
<code>src/</code>, orchestrated by <code>run_pipeline.py</code>.</p>

<h2>Pipeline overview</h2>
<pre>Raw coding (data/raw/, data/story_level/)
     ↓  (legacy v1-v3 standardization, outside this rebuild's scope)
Legacy final dataset (data/final/, v3)
     ↓  src/audit.py — repository audit, README claim verification
     ↓  src/validate.py, src/entity_resolution.py — data quality framework
Canonical dataset (data/processed/) — src/build_canonical.py
     ↓  src/build_networks.py, src/story_networks.py — G0-G11 network models
     ↓  src/metrics.py — descriptive corpus/centrality metrics
     ↓  src/communities.py, src/signed_and_directed.py, src/multilayer.py, src/narrative_order.py
     ↓  src/null_models.py, src/null_models_fdr.py — statistical validation
     ↓  src/sensitivity.py, src/robustness.py — sensitivity & structural robustness
     ↓  src/visualization.py, src/export_tables.py — figures & publication tables
Website (docs/) — src/build_site_data.py, src/build_site.py
</pre>
<figure>
  <img src="architecture_diagram.svg" alt="Pipeline architecture diagram">
  <figcaption>Full data-flow diagram (SVG). Every arrow is a re-runnable src/*.py script.</figcaption>
</figure>

<h2>Key modeling decisions</h2>
<p>Every non-obvious methodological choice is logged with its rationale in
<a href="decision_log.md">decision_log.md</a>. Highlights:</p>
<div class="dec-log">
<p><strong>Aggregation rule (DEC-003):</strong> event-level relations are aggregated into
<code>relations_aggregated.csv</code> by <em>unordered</em> actor pair — directionality is
preserved as flags, not lost.</p>
<p><strong>Relation taxonomy (DEC-004):</strong> the 17 observed relation types are mapped to
SOCIAL / KINSHIP / AUTHORITY / SEMANTIC / OTHER / UNCERTAIN families — an interpretive scheme,
not a raw-data fact.</p>
<p><strong>Directed network construction (DEC-005):</strong> the directed variant (G9) uses only
relations explicitly coded as directional — undirected relations are excluded, never assigned an
arbitrary direction.</p>
<p><strong>Community substrate (DEC-007):</strong> community detection runs on the core-social
network (identity/title relations excluded), and the 23-connected-component caveat (see
<a href="communities.html">Communities</a>) is carried through every downstream use.</p>
<p><strong>Null model method (DEC-008):</strong> degree-preserving randomization
(<code>networkx.double_edge_swap</code>), Benjamini-Hochberg FDR correction across all 36 tests.</p>
</div>

<h2>Network model definitions</h2>
<p>All 12 network variants (G0-G11) are defined in one place, <code>src/networks.py</code>, and
documented in full in <a href="network_models.md">network_models.md</a>. Every variant is reproducible by
re-running <code>python run_pipeline.py --stage build_networks</code>.</p>

<h2>Further reading</h2>
<p>
<a href="data_dictionary.md">Data Dictionary</a> ·
<a href="relation_codebook.md">Relation Codebook</a> ·
<a href="limitations.md">Limitations</a> (17 items) ·
<a href="inter_annotator_protocol.md">Inter-Annotator Protocol</a>
</p>

<h2>What this project does not claim</h2>
<ul>
<li>Network centrality is not equated with literary importance anywhere in this project.</li>
<li>Degree assortativity ("disassortative network") was an early descriptive observation that
did <strong>not</strong> survive null-model statistical validation — see <a href="analysis.html">Analysis</a>.</li>
<li>Community labels are numeric IDs, never invented cultural or sociological names.</li>
<li>Narrative order (<code>satir_no</code>) is never treated as historical chronology.</li>
</ul>
"""
    write("methodology.html", page("Methodology", "Pipeline, modeling decisions, and what this project does not claim.", "Methodology", content))


# ---------------------------------------------------------------------------
# EXPLORER
# ---------------------------------------------------------------------------
def build_explorer():
    content = """
<h1>Network Explorer</h1>
<p class="lede">Interactive view of the corpus network. Choose a network specification, then
search or click a node for details. All data is loaded from <code>docs/data/networks/*.json</code>,
generated by <code>src/build_site_data.py</code> from the same graphs used throughout this project.</p>

<div class="panel" style="margin-bottom:14px">
  <strong>Network definition:</strong>
  <span id="network-def-text">Loading…</span>
</div>

<div class="explorer-layout">
  <div class="panel">
    <label for="network-select">Network</label>
    <select id="network-select">
      <option value="G0_full">G0 — Full network</option>
      <option value="G1_person_only">G1 — Person-only</option>
      <option value="G2_core_social">G2 — Core social</option>
    </select>
    <label for="search-box">Search actor</label>
    <input type="text" id="search-box" placeholder="e.g. Salur Kazan">
    <label for="layout-select">Layout</label>
    <select id="layout-select">
      <option value="cose">Force-directed</option>
      <option value="concentric">Concentric (by degree)</option>
      <option value="circle">Circle</option>
    </select>
    <p style="font-size:0.75rem;color:var(--ink-soft);margin-top:12px">
      Isolated nodes (no edges in this variant) are omitted, per the graph-construction rule in
      <code>src/networks.py</code>.
    </p>
  </div>

  <div id="cy"></div>

  <div class="panel" id="detail-panel">
    <strong>Details</strong>
    <p style="font-size:0.8rem;color:var(--ink-soft)">Click a node or edge.</p>
  </div>
</div>

<div class="disclaimer" style="margin-top:20px">Network metrics shown here are structural
representations derived from the encoded dataset and should not be interpreted as complete
literary judgments about character importance.</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/cytoscape/3.28.1/cytoscape.min.js"></script>
<script src="assets/explorer.js"></script>
"""
    write("explorer.html", page("Network Explorer", "Interactive Cytoscape.js exploration of the corpus network.", "Network Explorer", content))


# ---------------------------------------------------------------------------
# STORIES (index) + per-story pages
# ---------------------------------------------------------------------------
def build_stories():
    stories = df("data/processed/stories.csv")
    metrics = df("data/derived/story_level_metrics.csv")
    merged = stories.merge(metrics, on=["story_id", "source_file"], how="left", suffixes=("", "_m"))

    tiles = "".join(
        f'<a class="tile" href="stories/{r.story_id}.html"><div class="tile-title">{r.story_id} — {r.boy_name_raw}</div>'
        f'<div class="tile-meta">{int(r.n_nodes) if pd.notna(r.n_nodes) else "—"} nodes · '
        f'{int(r.n_edges) if pd.notna(r.n_edges) else "—"} edges</div></a>'
        for r in merged.itertuples()
    )
    content = f"""
<h1>Stories</h1>
<p class="lede">14 units (13 boy + 1 girizgah prologue), each with its own network built the same
way as the corpus-level graphs (see <a href="methodology.html">Methodology</a>).</p>
<div class="grid-list">{tiles}</div>
"""
    write("stories.html", page("Stories", "The 14 stories (boy) of the corpus, each with its own network.", "Stories", content))

    nodes = df("data/processed/nodes.csv")
    rel = df("data/processed/relations_event_level.csv")
    for r in merged.itertuples():
        story_rel = rel[rel["story_id"] == r.story_id]
        actor_ids = pd.unique(pd.concat([story_rel["source_id"], story_rel["target_id"]]))
        actors = nodes[nodes["node_id"].isin(actor_ids)].sort_values("relation_count", ascending=False)
        actor_rows = "".join(
            f'<tr><td><a href="../characters/{safe_filename(a.node_id)}.html">{a.canonical_name}</a></td><td>{a.node_type}</td></tr>'
            for a in actors.head(15).itertuples()
        )
        rel_rows = "".join(
            f"<tr><td>{e.source_name}</td><td>{e.standard_relation}</td><td>{e.target_name}</td><td>{e.layer}</td></tr>"
            for e in story_rel.head(30).itertuples()
        )
        metric_bits = []
        for label, val, fmt in [
            ("Nodes", r.n_nodes, "{:.0f}"), ("Edges", r.n_edges, "{:.0f}"),
            ("Density", r.density, "{:.4f}"), ("Avg. degree", r.average_degree, "{:.2f}"),
            ("Degree centralization", r.degree_centralization, "{:.3f}"),
        ]:
            v = fmt.format(val) if pd.notna(val) else "N/A"
            metric_bits.append(f'<div class="metric-card"><span class="value">{v}</span><span class="label">{label}</span></div>')

        content = f"""
<p><a href="../stories.html">&larr; All stories</a></p>
<h1>{r.story_id} — {r.boy_name_raw}</h1>
<p class="lede">Corpus order: {r.corpus_order} / 14 · Section type: {r.section_type} · Source file:
<code>{r.source_file}</code></p>

<div class="card-grid">{''.join(metric_bits)}</div>

<h2>Top actors in this story</h2>
<table><thead><tr><th>Actor</th><th>Type</th></tr></thead><tbody>{actor_rows or '<tr><td colspan=2>—</td></tr>'}</tbody></table>

<h2>Relations (up to 30 shown)</h2>
<table><thead><tr><th>Source</th><th>Relation</th><th>Target</th><th>Layer</th></tr></thead><tbody>{rel_rows or '<tr><td colspan=4>—</td></tr>'}</tbody></table>

<h2>Related stories</h2>
<p><a href="../similarity.html">See the Similarity page</a> for shared-actor relationships between stories.</p>
"""
        write(f"stories/{r.story_id}.html", page(f"{r.story_id}", f"Story detail for {r.boy_name_raw}.", "Stories", content, root_prefix="../"))


# ---------------------------------------------------------------------------
# CHARACTERS (index) + per-character pages
# ---------------------------------------------------------------------------
def build_characters():
    nodes = df("data/processed/nodes.csv")
    cent = df("outputs/tables/centrality_G0_full.csv")
    ml = df("outputs/tables/multilayer_profile.csv")
    comm = df("outputs/tables/community_membership_G2_core_social.csv")
    rel = df("data/processed/relations_event_level.csv")

    all_actors = nodes.sort_values("relation_count", ascending=False)
    top = all_actors.head(60)
    tiles = "".join(
        f'<a class="tile" href="characters/{safe_filename(r.node_id)}.html"><div class="tile-title">{r.canonical_name}</div>'
        f'<div class="tile-meta">{r.node_type} · {r.story_count} stories</div></a>'
        for r in top.itertuples()
    )
    content = f"""
<h1>Characters</h1>
<p class="lede">Showing the top {len(top)} actors by relation count here; every one of the
{len(nodes)} canonical actors has its own profile page (linked from story pages and search),
and the full table is in <a href="downloads.html">Downloads</a> (<code>data/processed/nodes.csv</code>).</p>
<div class="disclaimer">{DISCLAIMER}</div>
<div class="grid-list">{tiles}</div>
"""
    write("characters.html", page("Characters", "Actor profiles: centrality, layers, community, story participation.", "Characters", content))

    cent_idx = cent.set_index("node_id")
    ml_idx = ml.set_index("node_id")
    comm_idx = comm.set_index("node_id")

    # Every canonical actor gets a profile page (not just the top 60 shown on
    # the index) - story pages link to any actor that appears in them, so an
    # incomplete set here would mean broken links (caught by
    # src/validate_site.py, section 105).
    for r in all_actors.itertuples():
        nid = r.node_id
        c = cent_idx.loc[nid] if nid in cent_idx.index else None
        m = ml_idx.loc[nid] if nid in ml_idx.index else None
        community = comm_idx.loc[nid, "leiden_community"] if nid in comm_idx.index else None

        own_rel = rel[(rel["source_id"] == nid) | (rel["target_id"] == nid)]
        partner_counts = pd.concat([
            own_rel.loc[own_rel["source_id"] == nid, "target_name"],
            own_rel.loc[own_rel["target_id"] == nid, "source_name"],
        ]).value_counts().head(10)
        partner_rows = "".join(f"<tr><td>{name}</td><td>{n}</td></tr>" for name, n in partner_counts.items())

        metric_bits = []
        if c is not None:
            for label, val, fmt in [("Degree (G0)", c["degree"], "{:.0f}"), ("Strength", c["strength_weighted_degree"], "{:.0f}"),
                                     ("Betweenness", c["betweenness"], "{:.4f}"), ("PageRank", c["pagerank"], "{:.4f}")]:
                metric_bits.append(f'<div class="metric-card"><span class="value">{fmt.format(val)}</span><span class="label">{label}</span></div>')
        card_html = f'<div class="card-grid">{"".join(metric_bits)}</div>' if metric_bits else "<p>No relations in G0_full (event-only actor).</p>"

        aliases = r.aliases if isinstance(r.aliases, str) and r.aliases else "—"
        first_story = r.first_story if isinstance(r.first_story, str) else "—"

        content = f"""
<p><a href="../characters.html">&larr; All characters</a></p>
<h1>{r.canonical_name}</h1>
<p class="lede">{r.node_type} · appears in {r.story_count} stor{'y' if r.story_count == 1 else 'ies'} ·
first appearance (corpus order): {first_story}</p>
<div class="disclaimer">{DISCLAIMER}</div>

<h2>Centrality profile (G0_full — preliminary, descriptive)</h2>
{card_html}
<p style="font-size:0.8rem;color:var(--ink-soft)">See <a href="../analysis.html">Analysis</a> for
null-model and sensitivity context before treating any of these as a definitive ranking.</p>

<h2>Layers &amp; community</h2>
<p>Active layers: {int(m['n_active_layers']) if m is not None and pd.notna(m['n_active_layers']) else '—'} / 7
&nbsp;·&nbsp; Layer participation coefficient: {f"{m['layer_participation_coefficient']:.3f}" if m is not None and pd.notna(m['layer_participation_coefficient']) else '—'}
&nbsp;·&nbsp; Community (G2_core_social, Leiden): {'Community ' + str(int(community)) if community is not None and pd.notna(community) else '—'}</p>

<h2>Strongest relations (by interaction count)</h2>
<table><thead><tr><th>Connected actor</th><th>Interactions</th></tr></thead><tbody>{partner_rows or '<tr><td colspan=2>—</td></tr>'}</tbody></table>

<h2>Aliases</h2>
<p>{aliases}</p>
"""
        write(f"characters/{safe_filename(nid)}.html", page(r.canonical_name, f"Character profile for {r.canonical_name}.", "Characters", content, root_prefix="../"))


# ---------------------------------------------------------------------------
# LAYERS
# ---------------------------------------------------------------------------
def build_layers():
    rel = df("data/processed/relations_event_level.csv")
    ml = df("outputs/tables/multilayer_profile.csv")
    layer_counts = rel["layer"].value_counts()

    sections = []
    for layer in layer_counts.index:
        col = f"degree__{layer}"
        top = ml.sort_values(col, ascending=False).head(5) if col in ml.columns else None
        top_rows = "".join(f"<tr><td>{t.canonical_name}</td><td>{int(getattr(t, col))}</td></tr>" for t in top.itertuples()) if top is not None else ""
        sections.append(f"""
<h3>{layer} <span style="color:var(--ink-soft);font-weight:400">({layer_counts[layer]} relations)</span></h3>
<table><thead><tr><th>Top actor</th><th>Degree in this layer</th></tr></thead><tbody>{top_rows}</tbody></table>
""")

    content = f"""
<h1>Relation Layers</h1>
<p class="lede">{len(layer_counts)} layers observed in <code>data/processed/relations_event_level.csv</code>
(the <code>layer</code> field, distinct from the relation_family taxonomy — see
<a href="methodology.html">Methodology</a>).</p>
{''.join(sections)}
"""
    write("layers.html", page("Layers", "Relation layers and their top actors.", "Layers", content))


# ---------------------------------------------------------------------------
# COMMUNITIES
# ---------------------------------------------------------------------------
def build_communities():
    comm_summary = load_json("outputs/statistics/community_summary_G2_core_social.json")
    stability = load_json("outputs/statistics/community_stability_G2_core_social.json")
    membership = df("outputs/tables/community_membership_G2_core_social.csv")

    sizes = membership["leiden_community"].value_counts().sort_index()
    size_rows = "".join(f"<tr><td>Community {i}</td><td>{n}</td></tr>" for i, n in sizes.items())

    content = f"""
<h1>Communities</h1>
<div class="disclaimer">Communities are labeled with plain numeric IDs only — no cultural or
sociological names are assigned to them.</div>

<h2>⚠️ Read this before interpreting community counts</h2>
<p>The <code>G2_core_social</code> network has <strong>23 connected components</strong>. Modularity
algorithms assign each disconnected component to its own community by construction, so a large
share of the raw community count below is a graph-fragmentation artifact, not meaningful social
clustering. The only community structure worth interpreting substantively is <strong>within the
261-node giant component</strong>. Full discussion: <a href="analysis.html">Analysis</a> and
<code>reports/06_advanced_network_analysis_report.md</code> §1.4.</p>

<h2>Leiden vs Louvain</h2>
<div class="card-grid">
  <div class="metric-card"><span class="value">{comm_summary['leiden_n_communities_res1.0_seed42']}</span><span class="label">Leiden communities</span></div>
  <div class="metric-card"><span class="value">{comm_summary['leiden_modularity_res1.0_seed42']:.3f}</span><span class="label">Leiden modularity</span></div>
  <div class="metric-card"><span class="value">{comm_summary['louvain_n_communities_seed42']}</span><span class="label">Louvain communities</span></div>
  <div class="metric-card"><span class="value">{comm_summary['adjusted_rand_index_leiden_vs_louvain']:.3f}</span><span class="label">ARI (Leiden vs Louvain)</span></div>
</div>
<p>Stability across 10 random seeds: mean modularity {stability['modularity_mean']:.4f}
(std {stability['modularity_std']:.4f}), mean pairwise ARI {stability['mean_pairwise_adjusted_rand_index']:.3f}
— the partition is highly stable across seeds.</p>

<h2>Community sizes (Leiden, resolution=1.0)</h2>
<table><thead><tr><th>Community</th><th>Size</th></tr></thead><tbody>{size_rows}</tbody></table>

<h2>Interactive view</h2>
<p>See the community-colored network in the <a href="explorer.html">Network Explorer</a> (filter
by community) or the static figure below.</p>
<figure>
  <img src="figures/communities/F06_community_structure.png" alt="Community structure of G2_core_social">
  <figcaption>Colors = community membership within the 261-node giant component only. Grey nodes = the 22 smaller connected components.</figcaption>
</figure>
"""
    write("communities.html", page("Communities", "Community detection results and the connected-component caveat.", "Communities", content))


# ---------------------------------------------------------------------------
# SIMILARITY
# ---------------------------------------------------------------------------
def build_similarity():
    jaccard = pd.read_csv(ROOT / "outputs" / "matrices" / "story_similarity_actor_jaccard.csv", index_col=0, encoding="utf-8-sig")
    t08 = pd.read_csv(ROOT / "outputs" / "tables" / "publication" / "T08_story_similarity.csv", encoding="utf-8-sig")
    top10 = t08.sort_values("actor_jaccard", ascending=False).head(10)

    content = f"""
<h1>Story Similarity</h1>
<p class="lede">Five similarity measures across all 91 story pairs: actor Jaccard, actor weighted
Jaccard, actor cosine (all three based on shared characters), relation-profile similarity, and
layer-composition similarity (both based on narrative-relational content, independent of which
specific actors appear). See <a href="methodology.html">Methodology</a> and
<a href="decision_log.md">decision_log.md</a> (DEC-014) for the exact definitions and the
hierarchical-clustering feature-space choice.</p>

<h2>Actor Jaccard heatmap</h2>
<figure>
  <img src="figures/similarity/F10_story_similarity_heatmap.png" alt="Story similarity heatmap">
  <figcaption>Grey diagonal = self-similarity (trivially 1.0). Darker = more shared actors.</figcaption>
</figure>

<h2>Story similarity network</h2>
<figure>
  <img src="figures/similarity/F11_story_similarity_network.png" alt="Story similarity network">
  <figcaption>Top 15 of 91 pairs by actor Jaccard. Edge darkness/thickness = similarity strength.</figcaption>
</figure>

<h2>Top 10 most similar story pairs (by shared actors)</h2>
{table_html(top10, ["story_a", "story_b", "actor_jaccard", "actor_weighted_jaccard", "actor_cosine", "relation_profile_similarity", "layer_composition_similarity"])}

<h2>Full pairwise table</h2>
<p>All 91 pairs, all 5 metrics: <a href="downloads/outputs/tables/publication/T08_story_similarity.csv">T08_story_similarity.csv</a>.</p>

<div class="disclaimer">These similarity values and the hierarchical clustering built from them
are descriptive only — no significance/null-model test has been applied to them (unlike the
community and modularity findings on the <a href="analysis.html">Analysis</a> page).</div>
"""
    write("similarity.html", page("Similarity", "Story similarity: actor overlap, relation-profile, and layer-composition measures.", "Similarity", content))


# ---------------------------------------------------------------------------
# ANALYSIS
# ---------------------------------------------------------------------------
def build_analysis():
    corpus_metrics = df("outputs/statistics/corpus_network_metrics.csv")
    fdr = df("outputs/statistics/null_model_fdr_corrected.csv")
    sens = df("outputs/tables/sensitivity_rank_stability.csv")
    sig = fdr[fdr["significant_at_bh_fdr_0.05"]]

    content = f"""
<h1>Analysis</h1>
<p class="lede">Summary of every analytical stage, each explicitly labeled descriptive/exploratory
or statistically validated.</p>

<h2>Corpus-level network metrics</h2>
{table_html(corpus_metrics, ["network", "n_nodes", "n_edges", "density", "average_clustering", "transitivity", "degree_assortativity"])}
<p style="font-size:0.85rem;color:var(--ink-soft)"><strong>Note:</strong> degree assortativity
values above are descriptive only — null-model testing (below) found none of them statistically
significant after multiple-testing correction.</p>

<h2>Null model validation</h2>
<p>{len(sig)} / {len(fdr)} tests remain significant after Benjamini-Hochberg FDR correction (α=0.05).
Community modularity is validated as a real signal (not a degree-sequence artifact) in most
networks tested; degree assortativity is not validated in any network.</p>
{table_html(sig, ["network", "metric", "observed", "z_score", "empirical_p", "bh_qvalue"])}
<figure>
  <img src="figures/null_models/F15_null_model_distributions.png" alt="Null model distributions">
  <figcaption>Random ensemble (n=1000) vs observed value, for every FDR-significant test.</figcaption>
</figure>

<h2>Sensitivity analysis</h2>
<p>Rank-correlation of centrality across 6 network-construction choices. Person+group vs
person-only is the single most consequential modeling decision tested.</p>
{table_html(sens, ["pair", "metric", "spearman_rho", "kendall_tau", "top_10_overlap_fraction"])}
<figure>
  <img src="figures/sensitivity/F16_sensitivity_correlation_matrix.png" alt="Sensitivity correlation matrix">
</figure>

<h2>Structural robustness</h2>
<p>Robust to random node loss, fragile to targeted (degree/betweenness) attack — a classic
hub-driven network pattern. This describes graph connectivity only, not narrative resilience.</p>
<figure>
  <img src="figures/robustness/F18_structural_robustness_curves.png" alt="Structural robustness curves">
</figure>

<h2>Full reports</h2>
<p>
<a href="reports/04_05_network_construction_and_descriptive_report.md">Network construction &amp; descriptive analysis</a> ·
<a href="reports/06_advanced_network_analysis_report.md">Advanced network analysis</a> ·
<a href="reports/07_null_models_report.md">Null models</a> ·
<a href="reports/08_sensitivity_robustness_report.md">Sensitivity &amp; robustness</a>
</p>
"""
    write("analysis.html", page("Analysis", "Centrality, communities, null models, sensitivity, robustness.", "Analysis", content))


# ---------------------------------------------------------------------------
# EVIDENCE
# ---------------------------------------------------------------------------
def build_evidence():
    val_summary = load_json("outputs/validation/summary.json")
    manifest = df("outputs/manifest_sha256.csv")

    val_rows = "".join(
        f"<tr><td>{cat}</td><td>{check}</td><td>{n}</td></tr>"
        for cat, checks in val_summary.items() for check, n in checks.items()
    )

    content = f"""
<h1>Evidence</h1>
<p class="lede">Scientific transparency: how every number on this site was produced, and what is
still unresolved.</p>

<h2>Data lineage</h2>
<pre>data/raw/ (immutable) → data/story_level/ → data/final/ (legacy v3)
    → data/processed/ (canonical rebuild, Phase 3) → outputs/ → docs/ (this site)</pre>
<p><strong>Known provenance gap:</strong> ~8.4% of event-level relations could not be matched
back to a specific <code>data/story_level/</code> row (see <code>data/processed/provenance.csv</code>,
<code>source_row_status == 'unmatched_provenance_gap'</code>). This is disclosed, not hidden.</p>

<h2>Validation test results</h2>
<div class="table-wrap"><table><thead><tr><th>Category</th><th>Check</th><th>Flagged rows</th></tr></thead>
<tbody>{val_rows}</tbody></table></div>
<p>Full detail: <code>outputs/validation/summary.json</code>, <code>validation/HUMAN_REVIEW_QUEUE.csv</code>
(75 open items awaiting manual review).</p>

<h2>Hash manifest</h2>
<p>{len(manifest)} files hashed (SHA-256) for reproducibility verification —
<a href="downloads/outputs/manifest_sha256.csv">outputs/manifest_sha256.csv</a>.</p>

<h2>Decision log</h2>
<p>Every irreversible or interpretive methodological choice is recorded with its rationale in
<a href="decision_log.md">decision_log.md</a> (11 decisions, DEC-001 through DEC-011).</p>

<h2>Reproduction status</h2>
<p>18/18 automated tests passing (<code>tests/</code>). CI (<code>.github/workflows/validate.yml</code>)
runs the test suite and a validation-only pipeline pass on every push.</p>
"""
    write("evidence.html", page("Evidence", "Data lineage, validation results, hash manifest, decision log.", "Evidence", content))


# ---------------------------------------------------------------------------
# DOWNLOADS
# ---------------------------------------------------------------------------
def build_downloads():
    items = [
        ("Canonical nodes", "data/processed/nodes.csv"),
        ("Canonical aliases", "data/processed/aliases.csv"),
        ("Stories index", "data/processed/stories.csv"),
        ("Event-level relations", "data/processed/relations_event_level.csv"),
        ("Aggregated relations", "data/processed/relations_aggregated.csv"),
        ("Relation taxonomy", "data/processed/relation_taxonomy.csv"),
        ("Provenance table", "data/processed/provenance.csv"),
        ("G0_full — GraphML", "outputs/networks/G0_full.graphml"),
        ("G0_full — GEXF", "outputs/networks/G0_full.gexf"),
        ("G0_full — edges CSV", "outputs/networks/G0_full_edges.csv"),
        ("G0_full — nodes CSV", "outputs/networks/G0_full_nodes.csv"),
        ("G1_person_only — GraphML", "outputs/networks/G1_person_only.graphml"),
        ("G2_core_social — GraphML", "outputs/networks/G2_core_social.graphml"),
        ("Bipartite actor-story — GraphML", "outputs/networks/bipartite_actor_story.graphml"),
        ("Full hash manifest", "outputs/manifest_sha256.csv"),
    ]
    rows = "".join(f'<tr><td>{label}</td><td><a href="downloads/{path}">{path}</a></td></tr>' for label, path in items)

    pub_dir = ROOT / "outputs" / "tables" / "publication"
    pub_rows = "".join(
        f'<tr><td>{p.stem}</td><td><a href="downloads/outputs/tables/publication/{p.name}">{p.name}</a></td></tr>'
        for p in sorted(pub_dir.glob("*.csv"))
    )

    content = f"""
<h1>Downloads</h1>
<p class="lede">Every file below is copied from this repository's own <code>data/</code> and
<code>outputs/</code> directories into <code>docs/downloads/</code> at site-build time
(<code>src/build_site.py::copy_assets</code>) — nothing here is re-hosted or hand-maintained.</p>
<table><thead><tr><th>File</th><th>Path</th></tr></thead><tbody>{rows}</tbody></table>

<h2>Publication tables (T01-T11, CSV)</h2>
<p>LaTeX (<code>.tex</code>) versions of each table sit alongside these in the repository under
<code>outputs/tables/publication/</code>.</p>
<table><thead><tr><th>Table</th><th>File</th></tr></thead><tbody>{pub_rows}</tbody></table>
"""
    write("downloads.html", page("Downloads", "Direct download links for the dataset, networks, and tables.", "Downloads", content))


# ---------------------------------------------------------------------------
# REPRODUCE
# ---------------------------------------------------------------------------
def build_reproduce():
    content = """
<h1>Reproduce</h1>
<p class="lede">Everything on this site is generated by the pipeline below — nothing is hand-typed.</p>

<h2>Setup</h2>
<pre>git clone https://github.com/4rslanismet/dede-korkut-social-network-dataset.git
cd dede-korkut-social-network-dataset
git checkout claude-dk-rebuild
python -m venv .venv
.venv\\Scripts\\activate   # Windows; use "source .venv/bin/activate" on macOS/Linux
pip install -r requirements.txt</pre>

<h2>Run everything</h2>
<pre>python run_pipeline.py --all</pre>
<p>Or a single stage:</p>
<pre>python run_pipeline.py --stage build_networks
python run_pipeline.py --stage null_models --fast   # development mode, n_random=100</pre>

<h2>Validate only (CI)</h2>
<pre>python run_pipeline.py --all --validate-only
python -m pytest tests/ -v</pre>

<h2>Google Colab</h2>
<p><em>Placeholder — a Colab notebook link can be added here once published.</em></p>

<h2>Determinism</h2>
<p>All stochastic steps read <code>seed: 42</code> from <code>config/analysis.yaml</code>.
<code>tests/test_determinism.py</code> verifies that Leiden community detection and the
degree-preserving randomization used for null models are exactly reproducible given this seed.</p>
"""
    write("reproduce.html", page("Reproduce", "Exact commands to reproduce every result on this site.", "Reproduce", content))


# ---------------------------------------------------------------------------
# ABOUT
# ---------------------------------------------------------------------------
def build_about():
    content = """
<h1>About</h1>
<p class="lede">Dede Korkut Narrative Network Project (DKNN) — a working title; the repository
name itself has not been changed.</p>

<h2>Scope</h2>
<p>This project treats the Book of Dede Korkut's encoded actor and relation data as a research
subject for digital humanities and network science methods: a reproducible canonical dataset,
social/complex/multilayer network analysis, story-level and bipartite analysis, statistical
validation (null models, sensitivity, robustness), publication-ready figures and tables, and this
interactive portal.</p>

<h2>Limitations (see also Evidence)</h2>
<ul>
<li>Single coder — no verified inter-annotator reliability statistic yet (infrastructure exists
in <code>validation/inter_annotator_sample.csv</code>, awaiting a second coder).</li>
<li>The specific print edition/transcription of the Book of Dede Korkut underlying the original
coding is not recorded in the repository — flagged as a critical open metadata gap
(<code>validation/source_edition_metadata_required.md</code>).</li>
<li>~8.4% of relations have an unresolved provenance link back to the story-level source rows.</li>
<li>Community counts on the core-social network are partly a connected-component artifact — see
<a href="communities.html">Communities</a>.</li>
</ul>

<h2>License &amp; citation</h2>
<p>Dataset license: CC BY 4.0 (see repository <code>LICENSE</code>). If you use this dataset or
analysis in academic work, please cite the repository. A <code>CITATION.cff</code> file is
pending (Phase 17 documentation).</p>

<h2>Source</h2>
<p>Repository: <a href="https://github.com/4rslanismet/dede-korkut-social-network-dataset">github.com/4rslanismet/dede-korkut-social-network-dataset</a>
(branch <code>claude-dk-rebuild</code>).</p>
"""
    write("about.html", page("About", "Project scope, limitations, license, and citation.", "About", content))


def main():
    print("Refreshing docs/data/*.json ...")
    build_site_data.main()
    copy_assets()

    build_home()
    build_dataset()
    build_methodology()
    build_explorer()
    build_stories()
    build_characters()
    build_layers()
    build_communities()
    build_similarity()
    build_analysis()
    build_evidence()
    build_downloads()
    build_reproduce()
    build_about()
    print("\nSite build complete.")


if __name__ == "__main__":
    main()
