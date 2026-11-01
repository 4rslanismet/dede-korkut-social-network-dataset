"""Phase 1 repository audit: file inventory, README claim verification,
cross-file consistency checks. Writes machine-readable JSON that the
markdown report is built from (no numbers are invented in prose)."""
import json
import re
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "reports" / "audit_data.json"


def file_meta(path: Path) -> dict:
    return {
        "path": str(path.relative_to(ROOT)).replace("\\", "/"),
        "size_bytes": path.stat().st_size,
    }


def csv_profile(path: Path) -> dict:
    meta = file_meta(path)
    encoding_used = None
    df = None
    for enc in ("utf-8-sig", "utf-8", "cp1254", "latin1"):
        try:
            df = pd.read_csv(path, encoding=enc, dtype=str, keep_default_na=False, na_values=[""])
            encoding_used = enc
            break
        except Exception:
            continue
    if df is None:
        meta["error"] = "could not read with any tested encoding"
        return meta

    meta["encoding_used"] = encoding_used
    meta["n_rows"] = int(df.shape[0])
    meta["n_cols"] = int(df.shape[1])
    meta["columns"] = list(df.columns)

    null_counts = {c: int(df[c].isna().sum()) for c in df.columns}
    meta["null_counts"] = {c: v for c, v in null_counts.items() if v > 0}
    meta["fully_null_columns"] = [c for c, v in null_counts.items() if v == meta["n_rows"] and meta["n_rows"] > 0]

    meta["n_exact_duplicate_rows"] = int(df.duplicated().sum())

    whitespace_issues = {}
    for c in df.columns:
        col = df[c].dropna().astype(str)
        bad = col[(col != col.str.strip())]
        if len(bad) > 0:
            whitespace_issues[c] = int(len(bad))
    meta["leading_trailing_whitespace_by_col"] = whitespace_issues

    if "kayit_id" in df.columns:
        meta["n_duplicate_kayit_id"] = int(df["kayit_id"].duplicated().sum())

    return meta, df


def profile_dir(dirpath: Path) -> dict:
    result = {}
    for f in sorted(dirpath.glob("*.csv")):
        prof, _df = csv_profile(f)
        result[f.name] = prof
    return result


def profile_xlsx(path: Path) -> dict:
    meta = file_meta(path)
    xl = pd.ExcelFile(path)
    sheets = {}
    for sh in xl.sheet_names:
        df = xl.parse(sh, dtype=str)
        sheets[sh] = {
            "n_rows": int(df.shape[0]),
            "n_cols": int(df.shape[1]),
            "columns": list(df.columns),
            "n_exact_duplicate_rows": int(df.duplicated().sum()),
            "null_counts": {c: int(df[c].isna().sum()) for c in df.columns if df[c].isna().sum() > 0},
        }
    meta["sheets"] = sheets
    meta["n_sheets"] = len(sheets)
    return meta


def recompute_headline_numbers(final_dir: Path) -> dict:
    nodes = pd.read_csv(final_dir / "dede_korkut_dugumler_temiz.csv", encoding="utf-8-sig")
    edges = pd.read_csv(final_dir / "dede_korkut_kenarlar_temiz.csv", encoding="utf-8-sig")
    events = pd.read_csv(final_dir / "dede_korkut_olaylar_temiz.csv", encoding="utf-8-sig")
    index_df = pd.read_csv(final_dir / "00_boy_dataset_indeksi_temiz.csv", encoding="utf-8-sig")
    aliases = pd.read_csv(final_dir / "dede_korkut_alias_sozlugu.csv", encoding="utf-8-sig")
    changelog = pd.read_csv(final_dir / "dede_korkut_degisim_logu.csv", encoding="utf-8-sig")

    n_stories_index = int(index_df.shape[0])
    n_stories_from_edges = edges["boy"].nunique() if "boy" in edges.columns else None
    n_stories_from_source_file = edges["source_file"].nunique() if "source_file" in edges.columns else None

    readme_claims = {"stories": 14, "nodes": 333, "edges": 628, "narrative_events": 85}
    recomputed = {
        "stories_from_index_file_rows": n_stories_index,
        "stories_unique_boy_in_edges": int(n_stories_from_edges) if n_stories_from_edges is not None else None,
        "stories_unique_source_file_in_edges": int(n_stories_from_source_file) if n_stories_from_source_file is not None else None,
        "nodes_rows": int(nodes.shape[0]),
        "nodes_unique_dugum_id": int(nodes["dugum_id"].nunique()) if "dugum_id" in nodes.columns else None,
        "edges_rows": int(edges.shape[0]),
        "events_rows": int(events.shape[0]),
        "aliases_rows": int(aliases.shape[0]),
        "changelog_rows": int(changelog.shape[0]),
    }

    # cross-check index file's own per-story edge/event counts against actual story_level files
    index_check_rows = []
    sl_dir = ROOT / "data" / "story_level"
    for _, row in index_df.iterrows():
        sf = row["source_file"]
        sl_path = sl_dir / sf
        actual_rows = None
        if sl_path.exists():
            actual_rows = int(pd.read_csv(sl_path, encoding="utf-8-sig").shape[0])
        edges_for_story = int((edges["source_file"] == sf).sum()) if "source_file" in edges.columns else None
        events_for_story = int((events["source_file"] == sf).sum()) if "source_file" in events.columns else None
        index_check_rows.append({
            "source_file": sf,
            "index_edge_kaydi": int(row["edge_kaydi"]) if not pd.isna(row["edge_kaydi"]) else None,
            "index_event_kaydi": (None if pd.isna(row["event_kaydi"]) else int(row["event_kaydi"])),
            "story_level_file_rows": actual_rows,
            "final_kenarlar_rows_for_story": edges_for_story,
            "final_olaylar_rows_for_story": events_for_story,
        })

    return {
        "readme_claims": readme_claims,
        "recomputed": recomputed,
        "per_story_consistency": index_check_rows,
    }


def node_edge_consistency(final_dir: Path) -> dict:
    nodes = pd.read_csv(final_dir / "dede_korkut_dugumler_temiz.csv", encoding="utf-8-sig")
    edges = pd.read_csv(final_dir / "dede_korkut_kenarlar_temiz.csv", encoding="utf-8-sig")
    events = pd.read_csv(final_dir / "dede_korkut_olaylar_temiz.csv", encoding="utf-8-sig")

    node_ids = set(nodes["dugum_id"].astype(str))

    edge_ids_used = set()
    for col in ("karakter_1_id", "karakter_2_id"):
        edge_ids_used |= set(edges[col].dropna().astype(str))

    event_ids_used = set()
    for col in ("aktor_id", "hedef_id"):
        if col in events.columns:
            event_ids_used |= set(events[col].dropna().astype(str))

    all_referenced = edge_ids_used | event_ids_used

    orphan_edge_endpoints = sorted(edge_ids_used - node_ids)
    orphan_event_actors = sorted(event_ids_used - node_ids)
    unreferenced_nodes = sorted(node_ids - all_referenced)

    dup_name_to_ids = (
        nodes.groupby("dugum_adi")["dugum_id"].nunique().reset_index()
    )
    dup_name_to_ids = dup_name_to_ids[dup_name_to_ids["dugum_id"] > 1]

    dup_id_rows = nodes[nodes.duplicated("dugum_id", keep=False)].sort_values("dugum_id")

    self_loops = edges[edges["karakter_1_id"].astype(str) == edges["karakter_2_id"].astype(str)]

    missing_endpoint = edges[edges["karakter_1_id"].isna() | edges["karakter_2_id"].isna() |
                              (edges["karakter_1_id"].astype(str).str.len() == 0) |
                              (edges["karakter_2_id"].astype(str).str.len() == 0)]

    exact_dup_edges = edges[edges.duplicated(
        subset=["karakter_1_id", "karakter_2_id", "iliski_turu", "boy"], keep=False
    )].sort_values(["boy", "karakter_1_id", "karakter_2_id"])

    return {
        "n_nodes": len(node_ids),
        "n_orphan_edge_endpoints": len(orphan_edge_endpoints),
        "orphan_edge_endpoints_sample": orphan_edge_endpoints[:20],
        "n_orphan_event_actor_ids": len(orphan_event_actors),
        "orphan_event_actor_ids_sample": orphan_event_actors[:20],
        "n_unreferenced_nodes": len(unreferenced_nodes),
        "unreferenced_nodes_sample": unreferenced_nodes[:20],
        "n_names_mapping_to_multiple_ids": int(dup_name_to_ids.shape[0]),
        "names_mapping_to_multiple_ids_sample": dup_name_to_ids.head(20).to_dict("records"),
        "n_duplicate_node_id_rows": int(dup_id_rows.shape[0]),
        "n_self_loop_edges": int(self_loops.shape[0]),
        "self_loop_sample": self_loops[["kayit_id", "boy", "karakter_1", "karakter_2"]].head(10).to_dict("records"),
        "n_edges_missing_endpoint": int(missing_endpoint.shape[0]),
        "n_exact_duplicate_relationship_rows": int(exact_dup_edges.shape[0]) ,
    }


def relation_layer_overview(final_dir: Path) -> dict:
    edges = pd.read_csv(final_dir / "dede_korkut_kenarlar_temiz.csv", encoding="utf-8-sig")
    out = {}
    for col in ("iliski_turu", "katman", "kutupluluk", "yonluluk", "cikarma_yontemi", "bolum_tipi", "karakter_1_tipi", "karakter_2_tipi"):
        if col in edges.columns:
            vc = edges[col].fillna("<NULL>").value_counts()
            out[col] = vc.to_dict()
    # weight distribution
    if "agirlik" in edges.columns:
        w = pd.to_numeric(edges["agirlik"], errors="coerce")
        out["_agirlik_stats"] = {
            "n_non_numeric": int(w.isna().sum() - edges["agirlik"].isna().sum()),
            "min": None if w.dropna().empty else float(w.min()),
            "max": None if w.dropna().empty else float(w.max()),
            "unique_values": sorted(w.dropna().unique().tolist()),
        }
    return out


def raw_xlsx_vs_processed(raw_path: Path, final_dir: Path) -> dict:
    xl = pd.ExcelFile(raw_path)
    edges = pd.read_csv(final_dir / "dede_korkut_kenarlar_temiz.csv", encoding="utf-8-sig")
    sl_dir = ROOT / "data" / "story_level"

    rows = []
    for sh in xl.sheet_names:
        df = xl.parse(sh, dtype=str)
        n_raw = int(df.shape[0])
        # best-effort match of sheet name to a story_level file / boy value by substring
        boy_match = None
        for b in edges["boy"].dropna().unique():
            if sh.strip()[:15].lower() in str(b).lower() or str(b).lower()[:15] in sh.strip().lower():
                boy_match = b
                break
        n_final = int((edges["boy"] == boy_match).sum()) if boy_match else None
        rows.append({
            "raw_sheet": sh,
            "raw_rows": n_raw,
            "raw_columns": list(df.columns),
            "matched_boy_in_final": boy_match,
            "final_kenarlar_rows_for_matched_boy": n_final,
        })
    return {
        "n_raw_sheets": len(xl.sheet_names),
        "n_story_level_files": len(list(sl_dir.glob("*.csv"))),
        "comparison": rows,
    }


def main():
    data = {}
    data["raw_dir"] = profile_dir(ROOT / "data" / "raw")  # no csvs expected here, kept for completeness
    data["raw_xlsx"] = profile_xlsx(ROOT / "data" / "raw" / "dede korkut karakterler.xlsx")
    data["story_level"] = profile_dir(ROOT / "data" / "story_level")
    final_profiles = profile_dir(ROOT / "data" / "final")
    data["final"] = final_profiles
    data["headline_numbers"] = recompute_headline_numbers(ROOT / "data" / "final")
    data["node_edge_consistency"] = node_edge_consistency(ROOT / "data" / "final")
    data["relation_layer_overview"] = relation_layer_overview(ROOT / "data" / "final")
    data["raw_vs_processed"] = raw_xlsx_vs_processed(ROOT / "data" / "raw" / "dede korkut karakterler.xlsx", ROOT / "data" / "final")

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2, default=str)
    print(f"Wrote {OUT_JSON}")


if __name__ == "__main__":
    main()
