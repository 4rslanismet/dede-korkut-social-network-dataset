"""Phase 13: inter-annotator reliability infrastructure (section 37-38).

Builds a stratified sample for a second human coder to independently
annotate. No second-coder data is invented — coder2_* columns and
`agreement` are left blank for a human to fill in. Stratification varies
across story, relation type, layer, and explicit/inferred extraction
method, as required by section 37.
"""
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

ROOT = Path(__file__).resolve().parents[1]
VALIDATION_DIR = ROOT / "validation"

with open(ROOT / "config" / "analysis.yaml", encoding="utf-8") as f:
    CONFIG = yaml.safe_load(f)
SEED = CONFIG["seed"]

TARGET_SAMPLE_SIZE = 70


def build_sample() -> pd.DataFrame:
    rel = pd.read_csv(ROOT / "data" / "processed" / "relations_event_level.csv", encoding="utf-8-sig")
    rng = np.random.default_rng(SEED)

    # Stratify on (relation_family_top, extraction_method) so both rare
    # categories (e.g. explicit vs inferred, which is heavily skewed 596:32)
    # and common ones are represented, then sample proportionally within
    # each stratum with a floor of at least 1 row per non-empty stratum.
    rel = rel.dropna(subset=["standard_relation", "layer", "extraction_method"])
    strata = rel.groupby(["relation_family_top", "extraction_method"], group_keys=False)

    n_strata = strata.ngroups
    per_stratum = max(1, TARGET_SAMPLE_SIZE // n_strata)

    sampled_parts = []
    for _, group in strata:
        n = min(len(group), per_stratum)
        sampled_parts.append(group.sample(n=n, random_state=SEED))
    sample = pd.concat(sampled_parts)

    # Top up to the target size (or as close as possible) with additional
    # random rows not already selected, biased toward story diversity.
    remaining_needed = TARGET_SAMPLE_SIZE - len(sample)
    if remaining_needed > 0:
        pool = rel.drop(sample.index)
        # prioritize under-represented stories in the current sample
        story_counts = sample["story_id"].value_counts()
        pool = pool.assign(_story_rank=pool["story_id"].map(lambda s: story_counts.get(s, 0)))
        pool = pool.sort_values("_story_rank")
        extra = pool.head(remaining_needed)
        sample = pd.concat([sample, extra])

    sample = sample.sample(frac=1, random_state=SEED).reset_index(drop=True)  # shuffle presentation order

    out = pd.DataFrame({
        "relation_id": sample["relation_id"],
        "story_id": sample["story_id"],
        "story_name": sample["story_name"],
        "actor_1": sample["source_name"],
        "actor_2": sample["target_name"],
        "raw_evidence": sample["raw_evidence"],
        "extraction_method": sample["extraction_method"],
        "coder1_relation": sample["standard_relation"],
        "coder2_relation": "",
        "coder1_layer": sample["layer"],
        "coder2_layer": "",
        "coder1_polarity": sample["polarity"],
        "coder2_polarity": "",
        "agreement": "",
        "notes": "",
    })
    return out


def main():
    VALIDATION_DIR.mkdir(parents=True, exist_ok=True)
    sample = build_sample()
    out_path = VALIDATION_DIR / "inter_annotator_sample.csv"
    sample.to_csv(out_path, index=False, encoding="utf-8-sig")

    print(f"Wrote {out_path} ({len(sample)} rows)")
    print("\nStratification check (extraction_method x relation_family_top not directly retained, "
          "showing relation type and extraction method distributions):")
    print(sample["coder1_relation"].value_counts())
    print()
    print(sample["extraction_method"].value_counts())
    print()
    print(f"Distinct stories represented: {sample['story_id'].nunique()} / 14")


if __name__ == "__main__":
    main()
