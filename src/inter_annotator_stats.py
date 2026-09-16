"""Phase 13 (cont.): Cohen's kappa / Krippendorff's alpha computation,
ready to run once a real second coder has filled in
validation/inter_annotator_sample.csv.

This script deliberately REFUSES to produce a number from placeholder
(empty) coder2_* data - see docs/inter_annotator_protocol.md. Running it
before a second coder has annotated the sample will print a clear
not_applicable status, not a fabricated statistic.
"""
import json
from pathlib import Path

import pandas as pd
from sklearn.metrics import cohen_kappa_score

ROOT = Path(__file__).resolve().parents[1]
SAMPLE_PATH = ROOT / "validation" / "inter_annotator_sample.csv"
OUT_STATS = ROOT / "outputs" / "statistics"

FIELDS = [("relation", "coder1_relation", "coder2_relation"),
          ("layer", "coder1_layer", "coder2_layer"),
          ("polarity", "coder1_polarity", "coder2_polarity")]


def krippendorff_alpha_nominal(labels_a: list, labels_b: list) -> float:
    """Krippendorff's alpha for nominal data, 2 raters, no missing values
    (a direct closed-form reduction of the general coincidence-matrix
    formula for exactly 2 fully-observed raters per unit)."""
    import itertools
    n = len(labels_a)
    all_labels = sorted(set(labels_a) | set(labels_b))
    if len(all_labels) < 2:
        return float("nan")

    observed_disagreement = sum(1 for a, b in zip(labels_a, labels_b) if a != b) / n

    pooled = labels_a + labels_b
    counts = {lab: pooled.count(lab) for lab in all_labels}
    total = len(pooled)
    expected_disagreement = 1 - sum((c / total) ** 2 for c in counts.values())
    # small-sample correction factor consistent with the standard alpha derivation
    expected_disagreement = expected_disagreement * total / (total - 1)

    if expected_disagreement == 0:
        return 1.0
    return 1 - observed_disagreement / expected_disagreement


def main():
    if not SAMPLE_PATH.exists():
        print("not_applicable: validation/inter_annotator_sample.csv does not exist. "
              "Run src/build_inter_annotator_sample.py first.")
        return

    df = pd.read_csv(SAMPLE_PATH, encoding="utf-8-sig", keep_default_na=False)

    results = {}
    any_filled = False
    for field_name, c1_col, c2_col in FIELDS:
        filled = df[(df[c2_col].astype(str).str.strip() != "")]
        n_filled = len(filled)
        if n_filled == 0:
            results[field_name] = {
                "status": "not_applicable",
                "reason": f"{c2_col} is empty for all {len(df)} rows - no second-coder data yet. "
                          f"See docs/inter_annotator_protocol.md.",
            }
            continue
        if n_filled < len(df):
            print(f"WARNING: {field_name} has {n_filled}/{len(df)} rows filled in by coder 2; "
                  f"computing agreement on the filled subset only.")
        any_filled = True

        a = filled[c1_col].tolist()
        b = filled[c2_col].tolist()
        kappa = cohen_kappa_score(a, b)
        alpha = krippendorff_alpha_nominal(a, b)
        agreement_pct = sum(1 for x, y in zip(a, b) if x == y) / len(a)

        results[field_name] = {
            "status": "computed",
            "n_rows": n_filled,
            "n_sample_total": len(df),
            "percent_agreement": agreement_pct,
            "cohens_kappa": kappa,
            "krippendorffs_alpha": alpha,
        }

    OUT_STATS.mkdir(parents=True, exist_ok=True)
    with open(OUT_STATS / "inter_annotator_agreement.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2, default=str)

    for field_name, res in results.items():
        if res["status"] == "not_applicable":
            print(f"{field_name}: NOT_APPLICABLE - {res['reason']}")
        else:
            print(f"{field_name}: n={res['n_rows']}, agreement={res['percent_agreement']:.1%}, "
                  f"kappa={res['cohens_kappa']:.3f}, alpha={res['krippendorffs_alpha']:.3f}")

    if not any_filled:
        print("\nNo inter-annotator statistic was computed - this is expected until a real "
              "second coder fills in validation/inter_annotator_sample.csv. Do not report a "
              "kappa/alpha value anywhere until this changes.")


if __name__ == "__main__":
    main()
