"""Phase 2: build entity-resolution candidate list and the human review
queue from the validation outputs. Produces proposals only — no automatic
merges are applied to data/final/."""
import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
FINAL = ROOT / "data" / "final"
VAL_OUT = ROOT / "outputs" / "validation"
VALIDATION_DIR = ROOT / "validation"


def build_entity_resolution_candidates() -> pd.DataFrame:
    nodes = pd.read_csv(FINAL / "dede_korkut_dugumler_temiz.csv", encoding="utf-8-sig")
    aliases = pd.read_csv(FINAL / "dede_korkut_alias_sozlugu.csv", encoding="utf-8-sig")

    rows = []

    # 1) same dugum_adi, two different dugum_id (node table internal conflict)
    same_name = pd.read_csv(VAL_OUT / "node__same_name_multiple_ids.csv", encoding="utf-8-sig")
    for name, grp in same_name.groupby("dugum_adi"):
        ids = grp["dugum_id"].tolist()
        for i in range(len(ids) - 1):
            rows.append({
                "entity_a": ids[i],
                "entity_b": ids[i + 1],
                "entity_a_name": name,
                "entity_b_name": name,
                "similarity_score": 1.0,
                "evidence": "identical dugum_adi, distinct dugum_id in dede_korkut_dugumler_temiz.csv",
                "proposed_action": "merge (keep one dugum_id, remap edges/events referencing the other)",
                "confidence": "high",
                "manual_review_required": True,
            })

    # 2) alias table: same orijinal_ad standardized to >1 different standart_ad
    conflict = (
        aliases.groupby("orijinal_ad")["standart_ad"].agg(lambda s: sorted(set(s)))
    )
    conflict = conflict[conflict.apply(len) > 1]
    for orig, targets in conflict.items():
        for i in range(len(targets)):
            for j in range(i + 1, len(targets)):
                rows.append({
                    "entity_a": targets[i],
                    "entity_b": targets[j],
                    "entity_a_name": targets[i],
                    "entity_b_name": targets[j],
                    "similarity_score": None,
                    "evidence": f"alias_sozlugu: orijinal_ad='{orig}' standardized to both targets "
                                f"(likely context-dependent disambiguation across different boy/story, "
                                f"or a leftover multi-hop standardization chain)",
                    "proposed_action": "manual review: confirm whether context-dependent (keep separate) "
                                       "or a stale intermediate mapping (chase to final v3 name)",
                    "confidence": "low",
                    "manual_review_required": True,
                })

    df = pd.DataFrame(rows).drop_duplicates(subset=["entity_a", "entity_b", "evidence"])
    return df


def build_human_review_queue(entity_candidates: pd.DataFrame) -> pd.DataFrame:
    rows = []
    item_id = 1

    for _, r in entity_candidates.iterrows():
        rows.append({
            "item_id": f"HR{item_id:04d}",
            "category": "entity_resolution",
            "source": "data/final/dede_korkut_dugumler_temiz.csv or dede_korkut_alias_sozlugu.csv",
            "issue": f"{r['entity_a_name']} vs {r['entity_b_name']}: {r['evidence']}",
            "proposed_action": r["proposed_action"],
            "confidence": r["confidence"],
            "requires_human_decision": True,
            "notes": "",
        })
        item_id += 1

    # alias targets that don't resolve to any current node name (multi-hop / stale mapping)
    aliases = pd.read_csv(FINAL / "dede_korkut_alias_sozlugu.csv", encoding="utf-8-sig")
    nodes = pd.read_csv(FINAL / "dede_korkut_dugumler_temiz.csv", encoding="utf-8-sig")
    node_names = set(nodes["dugum_adi"])
    unresolved = aliases[~aliases["standart_ad"].isin(node_names)]
    for standart_ad, grp in unresolved.groupby("standart_ad"):
        rows.append({
            "item_id": f"HR{item_id:04d}",
            "category": "stale_alias_target",
            "source": "data/final/dede_korkut_alias_sozlugu.csv",
            "issue": f"standart_ad='{standart_ad}' does not match any current dugum_adi in "
                     f"dede_korkut_dugumler_temiz.csv (appears {len(grp)}x as a standardization target; "
                     f"likely a v1/v2 intermediate name later re-standardized in v3)",
            "proposed_action": "trace forward through degisim_logu to the current v3 name, or confirm entity was removed",
            "confidence": "medium",
            "requires_human_decision": True,
            "notes": f"original forms: {sorted(grp['orijinal_ad'].unique().tolist())[:5]}",
        })
        item_id += 1

    # story_level -> final row-count gap (from Phase 1 audit)
    with open(ROOT / "reports" / "audit_data.json", encoding="utf-8") as f:
        audit = json.load(f)
    for row in audit["headline_numbers"]["per_story_consistency"]:
        sl = row["story_level_file_rows"]
        fin = (row["final_kenarlar_rows_for_story"] or 0) + (row["final_olaylar_rows_for_story"] or 0)
        if sl is not None and fin != sl:
            rows.append({
                "item_id": f"HR{item_id:04d}",
                "category": "provenance_gap",
                "source": f"data/story_level/{row['source_file']}",
                "issue": f"story_level has {sl} rows but final edges+events has {fin} rows for this "
                         f"source_file (diff={fin - sl:+d}); split/expansion logic is undocumented",
                "proposed_action": "confirm with original annotator whether rows were intentionally split; "
                                   "document the transformation rule in docs/methodology.md",
                "confidence": "medium",
                "requires_human_decision": True,
                "notes": "",
            })
            item_id += 1

    # self-loop
    self_loops = pd.read_csv(VAL_OUT / "edge__unexpected_self_loop.csv", encoding="utf-8-sig")
    for _, r in self_loops.iterrows():
        rows.append({
            "item_id": f"HR{item_id:04d}",
            "category": "unexpected_self_loop",
            "source": "data/final/dede_korkut_kenarlar_temiz.csv",
            "issue": f"kayit_id={r['kayit_id']}, boy={r['boy']}: self-loop {r['karakter_1']} -> {r['karakter_2']}",
            "proposed_action": "verify against original narrative line (satir_no) whether this is a genuine "
                                "reflexive act or a coding error",
            "confidence": "low",
            "requires_human_decision": True,
            "notes": "",
        })
        item_id += 1

    return pd.DataFrame(rows)


def append_manual_review_items(queue: pd.DataFrame) -> pd.DataFrame:
    """Append items found by human/ad-hoc inspection after the automated
    checks (e.g. the five concatenated multi-actor nodes, DEC-013), kept in
    validation/manual_review_items.csv. Without this, a fresh pipeline run
    regenerated the queue from the automated checks only and silently
    dropped them. IDs continue after the automated rows."""
    path = VALIDATION_DIR / "manual_review_items.csv"
    if not path.exists():
        return queue
    manual = pd.read_csv(path, encoding="utf-8-sig")
    manual.insert(0, "item_id", [f"HR{len(queue) + 1 + i:04d}" for i in range(len(manual))])
    return pd.concat([queue, manual[queue.columns]], ignore_index=True)


def build_source_edition_note():
    text = """# Source Edition Metadata — REQUIRED

## Problem

`data/raw/dede korkut karakterler.xlsx` does not correspond, row-for-row or
column-for-column, to `data/story_level/*.csv` or `data/final/*.csv` (see
`reports/01_repository_audit.md`, section 4). Its schema (`Source, Target,
Weight, Type`) is a different, coarser network-export format than the
21-column `story_level` schema.

This means the actual raw coding source used to produce `story_level` (i.e.,
which printed edition, transcription, or translation of the Book of Dede
Korkut was read line-by-line to produce `satir_no`-referenced records) is
**not present in this repository** and is **not documented** in
`README.md`, `docs/README_v2.md`, or `docs/README_v3.md`.

Per the project's provenance rule, this is treated as a critical missing
metadata item, not guessed at.

## Information needed from the original researcher/annotator

- [ ] Which printed edition / critical text of Dede Korkut was used as the
      reading source (e.g. Ergin, Gökyay, Tezcan-Boeschoten, or another)?
- [ ] Edition year and publisher.
- [ ] Whether `satir_no` refers to a specific edition's line numbering, a
      manuscript's, or an internal working transcription.
- [ ] Whether `data/raw/dede korkut karakterler.xlsx` was an earlier,
      abandoned coding pass, or a separate exercise unrelated to
      `story_level`/`final`.
- [ ] Whether original line-by-line raw coding notes (pre-story_level) exist
      anywhere outside this repository and could be added under
      `data/raw/` without violating copyright (see project rule 99 — do not
      redistribute copyrighted source text; only structured coding
      annotations, not the literary text itself, should be added).

## Until this is filled in

- `data/raw/` is left untouched.
- Any academic output (paper/thesis package) referencing "the text of Dede
  Korkut" must say the specific edition is **unspecified in the current
  repository metadata**, not assume a specific one.
"""
    return text


def main():
    VALIDATION_DIR.mkdir(parents=True, exist_ok=True)

    candidates = build_entity_resolution_candidates()
    candidates.to_csv(VALIDATION_DIR / "entity_resolution_candidates.csv", index=False, encoding="utf-8-sig")

    queue = append_manual_review_items(build_human_review_queue(candidates))
    queue.to_csv(VALIDATION_DIR / "HUMAN_REVIEW_QUEUE.csv", index=False, encoding="utf-8-sig")

    with open(VALIDATION_DIR / "source_edition_metadata_required.md", "w", encoding="utf-8") as f:
        f.write(build_source_edition_note())

    print(f"entity_resolution_candidates.csv: {len(candidates)} rows")
    print(f"HUMAN_REVIEW_QUEUE.csv: {len(queue)} rows")


if __name__ == "__main__":
    main()
