"""Release-consistency validator (src/validate_release_consistency.py) must DERIVE its
ground truth, never carry typed counts (final merge-prep pass).

Regression this guards against: the validator once hard-coded `site_html_files = 363` and
`pytest_tests = 18` in ground_truth(), and those stale numbers were written into the tracked
outputs/validation/release_consistency_report.json."""
import ast
import json
from pathlib import Path

import pandas as pd
import pytest

import validate_release_consistency as vrc

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src" / "validate_release_consistency.py"


def _ground_truth_dict_node() -> ast.Dict:
    tree = ast.parse(SRC.read_text(encoding="utf-8"))
    fn = next(n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == "ground_truth")
    ret = next(n for n in ast.walk(fn) if isinstance(n, ast.Return))
    assert isinstance(ret.value, ast.Dict)
    return ret.value


def test_ground_truth_contains_no_literal_numbers():
    """Every value returned by ground_truth() must be an expression, not an int/float literal."""
    literals = {ast.literal_eval(k): v.value for k, v in zip(_ground_truth_dict_node().keys, _ground_truth_dict_node().values)
                if isinstance(v, ast.Constant) and isinstance(v.value, (int, float)) and not isinstance(v.value, bool)}
    assert not literals, f"ground_truth() carries typed counts instead of derived values: {literals}"


def test_validator_source_has_no_historical_site_or_test_counts():
    text = SRC.read_text(encoding="utf-8")
    for stale in ("363", "\"pytest_tests\": 18", "pytest_tests\": 18", "last confirmed count"):
        assert stale not in text, f"validate_release_consistency.py still contains {stale!r}"


def test_derived_page_and_test_counts_match_independent_counts():
    truth = vrc.ground_truth()
    nodes = pd.read_csv(ROOT / "data" / "processed" / "nodes.csv", encoding="utf-8-sig")
    stories = pd.read_csv(ROOT / "data" / "processed" / "stories.csv", encoding="utf-8-sig")
    from site_layout import NAV_ITEMS
    n_static = len({href for _, href in NAV_ITEMS})
    assert truth["site_html_files"] == n_static + len(stories) + len(nodes)
    assert truth["site_html_files_on_disk"] == len(list((ROOT / "docs").rglob("*.html")))
    reg = json.loads((ROOT / "outputs" / "results_registry.json").read_text(encoding="utf-8"))
    assert truth["pytest_tests"] == reg["pipeline"]["n_tests_collected"]
    assert truth["actors"] == len(nodes) and truth["stories"] == len(stories)


def test_registry_test_count_equals_the_number_of_collected_tests():
    """results_registry.json records `pytest --collect-only`; the validator reads its test count from there,
    so a registry that was not regenerated after tests were added must fail here instead of going stale."""
    import subprocess
    import sys
    out = subprocess.run([sys.executable, "-m", "pytest", "--collect-only", "-q", "-p", "no:cacheprovider", str(ROOT / "tests")],
                         capture_output=True, text=True, encoding="utf-8", cwd=ROOT).stdout
    collected = sum(1 for line in out.splitlines() if "::" in line)
    reg = json.loads((ROOT / "outputs" / "results_registry.json").read_text(encoding="utf-8"))
    assert reg["pipeline"]["n_tests_collected"] == collected, (
        f"registry says {reg['pipeline']['n_tests_collected']} tests, pytest collects {collected}: "
        "re-run `python run_pipeline.py --stage results_registry`")


def test_internal_consistency_is_clean_on_the_committed_state():
    assert vrc.internal_consistency(vrc.ground_truth()) == []


def test_internal_consistency_flags_a_stale_page_count():
    """A generated site whose page count no longer matches the data must be reported, not absorbed."""
    truth = vrc.ground_truth()
    stale = dict(truth, site_html_files_on_disk=truth["site_html_files"] + 3)
    issues = vrc.internal_consistency(stale)
    assert any("site_html_files" in i["check"] for i in issues)
    stale_reg = dict(truth, registry_canonical_nodes=truth["actors"] - 1)
    assert any("actors" in i["check"] for i in vrc.internal_consistency(stale_reg))


def test_stored_release_report_matches_a_fresh_derivation():
    """The tracked report must be regenerated whenever a derived value changes (no historical constants)."""
    stored = json.loads((ROOT / "outputs" / "validation" / "release_consistency_report.json").read_text(encoding="utf-8"))
    fresh = json.loads(json.dumps(vrc.ground_truth(), default=str))
    assert stored["ground_truth"] == fresh, "release_consistency_report.json is stale: re-run src/validate_release_consistency.py"
    assert stored["issues"] == []
