"""Phase 2 data validation framework.

Runs the node/edge/event quality checks described in the project brief
(section 7) against data/final/*.csv, writes per-category CSV outputs to
outputs/validation/, and a machine-readable summary to
outputs/validation/summary.json. Nothing here mutates data/final/ — this
module only reports.
"""
import json
import re
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
FINAL = ROOT / "data" / "final"
OUT = ROOT / "outputs" / "validation"


def load():
    nodes = pd.read_csv(FINAL / "dede_korkut_dugumler_temiz.csv", encoding="utf-8-sig")
    edges = pd.read_csv(FINAL / "dede_korkut_kenarlar_temiz.csv", encoding="utf-8-sig")
    events = pd.read_csv(FINAL / "dede_korkut_olaylar_temiz.csv", encoding="utf-8-sig")
    aliases = pd.read_csv(FINAL / "dede_korkut_alias_sozlugu.csv", encoding="utf-8-sig")
    return nodes, edges, events, aliases


TURKISH_LOWER_MAP = str.maketrans("İIŞŞĞÜÖÇ", "iışşğüöç")


def norm_casefold_tr(s: str) -> str:
    return s.translate(TURKISH_LOWER_MAP).lower()


def node_checks(nodes: pd.DataFrame) -> dict:
    issues = {}

    dup_id = nodes[nodes.duplicated("dugum_id", keep=False)].sort_values("dugum_id")
    issues["duplicate_node_id"] = dup_id

    name_to_ids = nodes.groupby("dugum_adi")["dugum_id"].agg(lambda s: sorted(set(s)))
    multi_id_names = name_to_ids[name_to_ids.apply(len) > 1]
    rows = []
    for name, ids in multi_id_names.items():
        for _id in ids:
            row = nodes[nodes["dugum_id"] == _id].iloc[0]
            rows.append({"dugum_adi": name, "dugum_id": _id, "dugum_tipi": row["dugum_tipi"]})
    issues["same_name_multiple_ids"] = pd.DataFrame(rows)

    # same normalized-casefold name but different literal dugum_adi (capitalization variants)
    nodes = nodes.copy()
    nodes["_norm"] = nodes["dugum_adi"].apply(norm_casefold_tr)
    norm_groups = nodes.groupby("_norm")["dugum_adi"].agg(lambda s: sorted(set(s)))
    cap_variants = norm_groups[norm_groups.apply(len) > 1]
    cap_rows = []
    for norm, names in cap_variants.items():
        for n in names:
            sub = nodes[nodes["dugum_adi"] == n]
            for _, r in sub.iterrows():
                cap_rows.append({"normalized": norm, "dugum_adi": n, "dugum_id": r["dugum_id"]})
    issues["capitalization_variants"] = pd.DataFrame(cap_rows)

    issues["empty_or_blank_node_name"] = nodes[nodes["dugum_adi"].astype(str).str.strip() == ""]

    ws_issues = nodes[nodes["dugum_adi"].astype(str) != nodes["dugum_adi"].astype(str).str.strip()]
    issues["whitespace_in_node_name"] = ws_issues

    invalid_id = nodes[~nodes["dugum_id"].astype(str).str.match(r"^[a-z0-9_]+$")]
    issues["invalid_id_format"] = invalid_id

    return issues


def edge_checks(edges: pd.DataFrame, node_ids: set) -> dict:
    issues = {}

    missing_src = edges[edges["karakter_1_id"].isna() | (edges["karakter_1_id"].astype(str).str.strip() == "")]
    missing_tgt = edges[edges["karakter_2_id"].isna() | (edges["karakter_2_id"].astype(str).str.strip() == "")]
    issues["missing_source"] = missing_src
    issues["missing_target"] = missing_tgt

    orphan_src = edges[~edges["karakter_1_id"].astype(str).isin(node_ids)]
    orphan_tgt = edges[~edges["karakter_2_id"].astype(str).isin(node_ids)]
    issues["orphan_source_endpoint"] = orphan_src
    issues["orphan_target_endpoint"] = orphan_tgt

    valid_relations = set(edges["iliski_turu"].dropna().unique())  # data-driven, not invented
    issues["_observed_relation_types"] = pd.DataFrame({"iliski_turu": sorted(valid_relations)})

    valid_layers = {"olay", "iletişim", "çatışma", "akrabalık", "otorite", "mekân", "kimlik"}
    invalid_layer = edges[~edges["katman"].isin(valid_layers)]
    issues["invalid_layer"] = invalid_layer

    valid_polarity = {"nötr", "pozitif", "negatif", "karışık"}
    invalid_polarity = edges[~edges["kutupluluk"].isin(valid_polarity)]
    issues["invalid_polarity"] = invalid_polarity

    w = pd.to_numeric(edges["agirlik"], errors="coerce")
    invalid_weight = edges[w.isna() | (w < 1) | (w > 5)]
    issues["invalid_weight"] = invalid_weight

    valid_direction = {"yönlü", "yönsüz"}
    invalid_dir = edges[~edges["yonluluk"].isin(valid_direction)]
    issues["invalid_directionality"] = invalid_dir

    self_loops = edges[edges["karakter_1_id"].astype(str) == edges["karakter_2_id"].astype(str)]
    issues["unexpected_self_loop"] = self_loops

    dup_subset = ["karakter_1_id", "karakter_2_id", "iliski_turu", "boy", "satir_no"]
    exact_dupes = edges[edges.duplicated(subset=dup_subset, keep=False)].sort_values(dup_subset)
    issues["exact_duplicate_relationship_same_line"] = exact_dupes

    repeated_pair_pattern = edges[edges.duplicated(
        subset=["karakter_1_id", "karakter_2_id", "iliski_turu", "boy"], keep=False)]
    issues["repeated_actor_pair_relation_pattern"] = repeated_pair_pattern.sort_values(
        ["boy", "karakter_1_id", "karakter_2_id", "satir_no"])

    dup_kayit = edges[edges.duplicated("kayit_id", keep=False)]
    issues["duplicate_kayit_id"] = dup_kayit

    return issues


def event_checks(events: pd.DataFrame, node_ids: set) -> dict:
    issues = {}

    missing_actor = events[events["aktor_id"].isna() | (events["aktor_id"].astype(str).str.strip() == "")]
    issues["missing_actor"] = missing_actor

    orphan_actor = events[~events["aktor_id"].astype(str).isin(node_ids)]
    issues["orphan_actor"] = orphan_actor

    has_target = events["hedef_id"].notna() & (events["hedef_id"].astype(str).str.strip() != "")
    orphan_target = events[has_target & (~events["hedef_id"].astype(str).isin(node_ids))]
    issues["unsupported_target"] = orphan_target

    dup_kayit = events[events.duplicated("kayit_id", keep=False)]
    issues["duplicate_kayit_id"] = dup_kayit

    dup_event = events[events.duplicated(subset=["aktor_id", "hedef_id", "event_turu", "boy"], keep=False)]
    issues["duplicate_event_pattern"] = dup_event

    return issues


def alias_checks(aliases: pd.DataFrame, node_names: set) -> dict:
    issues = {}

    dup_orig = aliases[aliases.duplicated("orijinal_ad", keep=False)].sort_values("orijinal_ad")
    issues["duplicate_original_alias"] = dup_orig

    conflicting = (
        aliases.groupby("orijinal_ad")["standart_ad"].nunique().reset_index(name="n_targets")
    )
    conflicting = conflicting[conflicting["n_targets"] > 1]
    issues["alias_maps_to_multiple_targets"] = conflicting

    unresolved_targets = aliases[~aliases["standart_ad"].isin(node_names)]
    issues["alias_target_not_in_node_table"] = unresolved_targets

    return issues


def write_all(issues_by_group: dict):
    OUT.mkdir(parents=True, exist_ok=True)
    summary = {}
    for group, issues in issues_by_group.items():
        summary[group] = {}
        for name, df in issues.items():
            fname = f"{group}__{name}.csv"
            df.to_csv(OUT / fname, index=False, encoding="utf-8-sig")
            summary[group][name] = int(len(df))
    with open(OUT / "summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    return summary


def main():
    nodes, edges, events, aliases = load()
    node_ids = set(nodes["dugum_id"].astype(str))
    node_names = set(nodes["dugum_adi"].astype(str))

    issues_by_group = {
        "node": node_checks(nodes),
        "edge": edge_checks(edges, node_ids),
        "event": event_checks(events, node_ids),
        "alias": alias_checks(aliases, node_names),
    }
    summary = write_all(issues_by_group)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
