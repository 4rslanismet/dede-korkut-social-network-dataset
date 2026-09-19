"""Text/number consistency of the CURRENT-STATUS documents (DEC-017/018/019).

Historical records (docs/decision_log.md, CLAUDE_SESSION_HANDOFF.md, CHANGELOG.md,
reports/FIX_PASS_REPORT.md) legitimately describe earlier states and are exempt;
every document that states the project's current facts is checked against the
data, the registry and the pipeline definition."""
import json
import re
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]

CURRENT_STATUS_GLOBS = [
    "README.md", "DATASET_CARD.md", "NEXT_TASK.md",
    "docs/limitations.md", "docs/methodology.md", "docs/network_models.md", "docs/data_dictionary.md",
    "paper/*.md", "thesis/*.md",
    "reports/EXECUTIVE_SUMMARY.md", "reports/FINAL_REBUILD_REPORT.md", "reports/RELEASE_CHECKLIST.md",
    "reports/08_sensitivity_robustness_report.md", "reports/13_14_reproducibility_report.md",
    "docs/*.html",
]


def _current_docs():
    files = []
    for g in CURRENT_STATUS_GLOBS:
        files.extend(sorted(ROOT.glob(g)))
    return [f for f in files if f.is_file()]


def _hits(pattern, flags=re.IGNORECASE):
    rx = re.compile(pattern, flags)
    out = []
    for f in _current_docs():
        for i, line in enumerate(f.read_text(encoding="utf-8").splitlines(), start=1):
            if rx.search(line):
                out.append(f"{f.relative_to(ROOT)}:{i}: {line.strip()[:120]}")
    return out


def test_no_stale_five_composite_nodes_statement():
    hits = _hits(r"\b(?:5|five)\b[^.\n]{0,25}\b(?:concatenated|composite)")
    assert not hits, "stale '5 composite/concatenated nodes' statements:\n" + "\n".join(hits)


def test_composite_counts_in_docs_match_the_reproducible_scan():
    reg = json.loads((ROOT / "outputs" / "results_registry.json").read_text(encoding="utf-8"))["composite_nodes"]
    n = reg["n_candidate_nodes"]
    # every document that quotes "N candidate composite nodes" must quote the scan's number
    for f in _current_docs():
        for m in re.finditer(r"(\d+)\s+(?:canonical actor labels are )?candidate composite nodes", f.read_text(encoding="utf-8")):
            assert int(m.group(1)) == n, f"{f.relative_to(ROOT)} says {m.group(1)} candidate composite nodes; scan found {n}"


def test_paper_main_text_mentions_composite_node_limitation():
    text = (ROOT / "paper" / "results.md").read_text(encoding="utf-8") + (ROOT / "paper" / "methods.md").read_text(encoding="utf-8")
    assert re.search(r"composite", text, re.I), "the main paper text must state the composite-node limitation"


def test_no_ambiguous_giant_component_denominator_wording():
    hits = _hits(r"halves? the giant|giant component halves|halve the giant|dev bileşenin yarısı|dev bileşeni yarıya|"
                 r"half of (?:its|the) original size|below 50% of its original size")
    assert not hits, "ambiguous robustness denominator wording:\n" + "\n".join(hits)


def test_no_single_most_consequential_claim():
    hits = _hits(r"single most consequential|most consequential (?:modeling|network|construction)|en etkili modelleme")
    assert not hits, "unsupported 'single most consequential' claim:\n" + "\n".join(hits)


def test_stage_counts_quoted_in_docs_match_the_pipeline():
    import run_pipeline
    n = len(run_pipeline.STAGES)
    bad = []
    for f in _current_docs():
        for m in re.finditer(r"(\d+)\s+(?:implemented\s+|pipeline\s+)?(?:stages|aşama)\b", f.read_text(encoding="utf-8"), flags=re.I):
            if int(m.group(1)) != n:
                bad.append(f"{f.relative_to(ROOT)}: '{m.group(0)}' (pipeline has {n} stages)")
    assert not bad, "\n".join(bad)


def test_manifest_file_counts_quoted_in_docs_match_the_manifest():
    n = len(pd.read_csv(ROOT / "outputs" / "manifest_sha256.csv", encoding="utf-8-sig"))
    bad = []
    rx = re.compile(r"(\d+)[- ](?:file|files|dosya)[^.\n]{0,60}(?:SHA|hash|manifest)|(?:SHA-256|hash manifest|manifest)[^.\n]{0,60}?(\d+)\s+(?:files|dosya)", re.I)
    for f in _current_docs():
        for m in rx.finditer(f.read_text(encoding="utf-8")):
            q = int(m.group(1) or m.group(2))
            if q != n:
                bad.append(f"{f.relative_to(ROOT)}: '{m.group(0)[:70]}' (manifest has {n} entries)")
    assert not bad, "\n".join(bad)


def test_node_type_counts_in_dataset_card_and_limitations_match_the_data(nodes):
    counts = nodes["node_type"].value_counts()
    person, group = int(counts.get("kişi", 0)), int(counts.get("grup", 0))
    other = len(nodes) - person - group
    card = (ROOT / "DATASET_CARD.md").read_text(encoding="utf-8")
    assert f"{person} person" in card and f"{group} group" in card and f"{other} of other types" in card
    lim = (ROOT / "docs" / "limitations.md").read_text(encoding="utf-8")
    m = re.search(r"(\d+) of (\d+) canonical actors are `grup`-type \(plus (\d+) more", lim)
    assert m and (int(m.group(1)), int(m.group(2)), int(m.group(3))) == (group, len(nodes), other)


def test_sensitivity_table_uses_corrected_weighted_betweenness(nodes):
    """The committed sensitivity table must equal a fresh computation with distance = 1/strength
    for the weighted-vs-unweighted pair (the one whose betweenness arm changed with DEC-017)."""
    from metrics import centrality_profile
    from networks import build_all_networks
    from scipy.stats import spearmanr
    graphs = build_all_networks()
    a = centrality_profile("G10_weighted", graphs["G10_weighted"], nodes).set_index("node_id")
    b = centrality_profile("G11_unweighted", graphs["G11_unweighted"], nodes).set_index("node_id")
    common = a.index.intersection(b.index)
    fresh = spearmanr(a.loc[common, "betweenness"], b.loc[common, "betweenness"])[0]
    t = pd.read_csv(ROOT / "outputs" / "tables" / "sensitivity_rank_stability.csv", encoding="utf-8-sig")
    stored = float(t[(t["pair"] == "weighted_vs_unweighted") & (t["metric"] == "betweenness")]["spearman_rho"].iloc[0])
    assert stored == pytest.approx(fresh, abs=1e-9), f"stored sensitivity rho {stored} != fresh {fresh}: table is stale"


def test_t04_and_actor_metrics_json_match_the_corrected_centrality_table():
    cent = pd.read_csv(ROOT / "outputs" / "tables" / "centrality_G0_full.csv", encoding="utf-8-sig").set_index("canonical_name")
    t04 = pd.read_csv(ROOT / "outputs" / "tables" / "publication" / "T04_centrality_results.csv", encoding="utf-8-sig")
    for _, r in t04.iterrows():
        assert r["betweenness"] == pytest.approx(cent.loc[r["canonical_name"], "betweenness"], abs=6e-4)  # T04 is rounded to 3 dp
    am = json.loads((ROOT / "docs" / "data" / "actor_metrics.json").read_text(encoding="utf-8"))
    cent_id = pd.read_csv(ROOT / "outputs" / "tables" / "centrality_G0_full.csv", encoding="utf-8-sig").set_index("node_id")
    for nid in list(cent_id.index)[:40]:
        assert am[nid]["betweenness"] == pytest.approx(cent_id.loc[nid, "betweenness"], abs=1e-9)
