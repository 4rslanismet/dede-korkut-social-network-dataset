"""Phase 7 (cont.): Benjamini-Hochberg FDR correction across all null-model
tests (section 112 - multiple comparison problem). Reads the full-mode null
model results and adds BH-adjusted q-values."""
import json
from pathlib import Path

import pandas as pd
import yaml
from statsmodels.stats.multitest import multipletests

ROOT = Path(__file__).resolve().parents[1]
OUT_STATS = ROOT / "outputs" / "statistics"

with open(ROOT / "config" / "analysis.yaml", encoding="utf-8") as f:
    CONFIG = yaml.safe_load(f)
ALPHA = CONFIG["multiple_testing"]["alpha"]


def main():
    with open(ROOT / "outputs" / "null_models" / "null_model_results_full.json", encoding="utf-8") as f:
        data = json.load(f)

    rows = []
    for network, res in data["results"].items():
        if res["status"] != "computed":
            continue
        for metric, vals in res["metrics"].items():
            rows.append({
                "network": network, "metric": metric,
                "observed": vals["observed"], "z_score": vals["z_score"],
                "empirical_p": vals["empirical_p"],
            })

    df = pd.DataFrame(rows)
    reject, qval, _, _ = multipletests(df["empirical_p"], alpha=ALPHA, method="fdr_bh")
    df["bh_qvalue"] = qval
    df["significant_at_bh_fdr_" + str(ALPHA)] = reject

    df = df.sort_values("empirical_p")
    df.to_csv(OUT_STATS / "null_model_fdr_corrected.csv", index=False, encoding="utf-8-sig")
    print(f"{len(df)} tests, alpha={ALPHA}, method=fdr_bh")
    print(df.to_string(index=False))
    print(f"\n{int(reject.sum())}/{len(df)} tests remain significant after BH-FDR correction")


if __name__ == "__main__":
    main()
