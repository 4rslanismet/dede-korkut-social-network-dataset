"""Phase 3: build the canonical data model under data/processed/.

Every transformation applied here is deliberately narrow and documented in
this docstring / inline comments, so it can be audited later:

1. Entity resolution: the single high-confidence duplicate found in Phase 2
   (`Begil'in Adamları` under two node IDs) is merged. No other automatic
   merges are applied — everything else in
   validation/entity_resolution_candidates.csv stays open pending manual
   review (`needs_manual_validation=1`).
2. Event-level relations table (`relations_event_level.csv`) is a
   column-renamed, schema-normalized copy of
   `data/final/dede_korkut_kenarlar_temiz.csv` — no rows are dropped, added,
   or reinterpreted.
3. Aggregation to `relations_aggregated.csv` groups by an *unordered* actor
   pair (see AGGREGATION RULE below) — this specific choice is recorded in
   docs/methodology.md (Phase 11) as a modeling decision, not a data fact.
4. `relation_taxonomy.csv` maps the 17 observed `iliski_turu` values to a
   higher-level family (SOCIAL / KINSHIP / AUTHORITY / SEMANTIC / OTHER /
   UNCERTAIN). This mapping is an interpretive analytical construct (as
   called for in section 13 of the project brief), not a raw-data fact; the
   rationale for each mapping is recorded in the table itself.
5. Provenance: each event-level relation is best-effort matched back to its
   originating row in data/story_level/<source_file> by exact match on
   (karakter_1, karakter_2, iliski_ham). Where no unique match is found,
   `source_row_status` records why, rather than guessing.
"""
import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
FINAL = ROOT / "data" / "final"
STORY_LEVEL = ROOT / "data" / "story_level"
PROCESSED = ROOT / "data" / "processed"

# ---------------------------------------------------------------------------
# Relation taxonomy: observed iliski_turu -> (relation_family, top_level_family)
# Interpretive mapping, documented rationale per row. Every one of the 17
# observed values (from outputs/validation/edge___observed_relation_types.csv)
# is covered; nothing here is invented evidence about specific relationships,
# only a categorization scheme for the relation *types themselves*.
# ---------------------------------------------------------------------------
RELATION_TAXONOMY = [
    ("akrabalık", "kinship", "KINSHIP", "Explicit kin relation (parent-child, sibling, spouse, lineage not further distinguished at this coding granularity)"),
    ("evlilik/bağlaşıklık", "marriage_alliance", "KINSHIP", "Marriage or marriage-based alliance between actors/groups"),
    ("diyalog_nötr", "communication", "SOCIAL", "Neutral-valence dialogue/speech act"),
    ("diyalog_olumlu", "communication", "SOCIAL", "Positive-valence dialogue/speech act"),
    ("diyalog_olumsuz", "communication", "SOCIAL", "Negative-valence dialogue/speech act"),
    ("ikna/müzakere", "cooperation", "SOCIAL", "Persuasion or negotiation between actors"),
    ("destek/yardım", "support", "SOCIAL", "Aid, assistance, or backing given by one actor to another"),
    ("çatışma", "conflict", "SOCIAL", "Direct conflict or hostility"),
    ("gerilim", "conflict", "SOCIAL", "Narrative tension short of open conflict"),
    ("otorite/emir", "authority", "AUTHORITY", "Command, order, or hierarchical instruction"),
    ("kimlik/unvan", "identity_title", "SEMANTIC", "Naming, titling, or identity-establishing relation (not a social interaction)"),
    ("coğrafi_epitet", "identity_title", "SEMANTIC", "Geographic epithet attached to an actor (e.g. 'pillar of Turkistan')"),
    ("tören/ritüel", "other", "OTHER", "Ceremonial or ritual act not cleanly social/kinship/authority"),
    ("ödül/değişim", "cooperation", "SOCIAL", "Reward or exchange between actors"),
    ("duygusal_tepki", "other", "OTHER", "Emotional reaction not directed as a social interaction per se"),
    ("hareket/eylem", "other", "OTHER", "Generic action/movement relation, ambiguous family"),
    ("belirsiz", "uncertain", "UNCERTAIN", "Relation type could not be determined from the source text at coding time"),
]


def load_final():
    nodes = pd.read_csv(FINAL / "dede_korkut_dugumler_temiz.csv", encoding="utf-8-sig")
    edges = pd.read_csv(FINAL / "dede_korkut_kenarlar_temiz.csv", encoding="utf-8-sig")
    events = pd.read_csv(FINAL / "dede_korkut_olaylar_temiz.csv", encoding="utf-8-sig")
    aliases = pd.read_csv(FINAL / "dede_korkut_alias_sozlugu.csv", encoding="utf-8-sig")
    index_df = pd.read_csv(FINAL / "00_boy_dataset_indeksi_temiz.csv", encoding="utf-8-sig")
    return nodes, edges, events, aliases, index_df


MERGE_DROP_ID = "begil_in_adamlari"
MERGE_KEEP_ID = "begilin_adamlari"


def apply_entity_resolution(nodes, edges, events):
    """Apply the single high-confidence merge from Phase 2. Everything else
    in entity_resolution_candidates.csv is left untouched (low confidence)."""
    nodes = nodes.copy()
    row_drop = nodes[nodes["dugum_id"] == MERGE_DROP_ID]
    row_keep_mask = nodes["dugum_id"] == MERGE_KEEP_ID
    if not row_drop.empty and row_keep_mask.any():
        for col in ["toplam_gorunum", "edge_gorunumu", "event_gorunumu", "boy_sayisi"]:
            nodes.loc[row_keep_mask, col] = nodes.loc[row_keep_mask, col].values[0] + row_drop[col].values[0]
        nodes = nodes[nodes["dugum_id"] != MERGE_DROP_ID].reset_index(drop=True)

    edges = edges.copy()
    for col in ("karakter_1_id", "karakter_2_id"):
        edges[col] = edges[col].replace(MERGE_DROP_ID, MERGE_KEEP_ID)

    events = events.copy()
    for col in ("aktor_id", "hedef_id"):
        events[col] = events[col].replace(MERGE_DROP_ID, MERGE_KEEP_ID)

    return nodes, edges, events


def build_stories(index_df: pd.DataFrame, edges: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for i, r in index_df.reset_index(drop=True).iterrows():
        sf = r["source_file"]
        boy_values = edges.loc[edges["source_file"] == sf, "boy"]
        raw_boy_name = boy_values.iloc[0] if len(boy_values) else None
        rows.append({
            "story_id": f"S{i+1:02d}",
            "corpus_order": i + 1,
            "source_file": sf,
            "boy_name_raw": raw_boy_name,
            "section_type": "girizgah" if sf == "01_girizgah.csv" else "boy",
            "n_edges": int(r["edge_kaydi"]),
            "n_events": 0 if pd.isna(r["event_kaydi"]) else int(r["event_kaydi"]),
            "n_nodes_declared_in_index": int(r["dugum_sayisi"]),
        })
    return pd.DataFrame(rows)


def build_relations_event_level(edges: pd.DataFrame, stories: pd.DataFrame) -> pd.DataFrame:
    sf_to_story = dict(zip(stories["source_file"], stories["story_id"]))
    tax_map = {r[0]: (r[1], r[2]) for r in RELATION_TAXONOMY}

    out = pd.DataFrame({
        "relation_id": edges["kayit_id"],
        "story_id": edges["source_file"].map(sf_to_story),
        "story_name": edges["boy"],
        "section_type": edges["bolum_tipi"],
        "narrative_order": edges["satir_no"],
        "source_id": edges["karakter_1_id"],
        "source_name": edges["karakter_1"],
        "source_type": edges["karakter_1_tipi"],
        "target_id": edges["karakter_2_id"],
        "target_name": edges["karakter_2"],
        "target_type": edges["karakter_2_tipi"],
        "raw_relation": edges["iliski_ham"],
        "standard_relation": edges["iliski_turu"],
        "relation_family": edges["iliski_turu"].map(lambda x: tax_map.get(x, (None, None))[0]),
        "relation_family_top": edges["iliski_turu"].map(lambda x: tax_map.get(x, (None, None))[1]),
        "layer": edges["katman"],
        "weight": edges["agirlik"],
        "polarity": edges["kutupluluk"],
        "directionality": edges["yonluluk"],
        "extraction_method": edges["cikarma_yontemi"],
        "confidence": pd.NA,  # not present in source data at this granularity — not invented
        "source_file": edges["source_file"],
        "source_row": pd.NA,  # filled in by attach_provenance()
        "raw_evidence": edges["ham_satir"],
        "validation_status": "ok",
        "notes": edges["not"],
    })
    return out


def build_relations_aggregated(rel_event: pd.DataFrame) -> pd.DataFrame:
    """AGGREGATION RULE (documented choice, see module docstring):
    group by the *unordered* actor pair (frozenset of source_id/target_id).
    Directionality/polarity information is preserved as counts, not
    collapsed silently."""
    df = rel_event.copy()
    pair = df.apply(lambda r: tuple(sorted([str(r["source_id"]), str(r["target_id"])])), axis=1)
    df["_actor_a"] = pair.map(lambda p: p[0])
    df["_actor_b"] = pair.map(lambda p: p[1])

    rows = []
    for (actor_a, actor_b), g in df.groupby(["_actor_a", "_actor_b"]):
        w = pd.to_numeric(g["weight"], errors="coerce")
        rows.append({
            "actor_a": actor_a,
            "actor_b": actor_b,
            "interaction_count": len(g),
            "total_weight": w.sum(),
            "positive_count": int((g["polarity"] == "pozitif").sum()),
            "negative_count": int((g["polarity"] == "negatif").sum()),
            "neutral_count": int((g["polarity"] == "nötr").sum()),
            "mixed_count": int((g["polarity"] == "karışık").sum()),
            "stories_shared": g["story_id"].nunique(),
            "story_ids": ";".join(sorted(g["story_id"].dropna().unique())),
            "relation_types": ";".join(sorted(g["standard_relation"].dropna().unique())),
            "relation_families": ";".join(sorted(g["relation_family"].dropna().unique())),
            "layers": ";".join(sorted(g["layer"].dropna().unique())),
            "any_directed": bool((g["directionality"] == "yönlü").any()),
            "any_undirected": bool((g["directionality"] == "yönsüz").any()),
        })

    agg = pd.DataFrame(rows)
    agg.insert(0, "pair_id", [f"P{i+1:04d}" for i in range(len(agg))])
    return agg


def build_relation_taxonomy(edges: pd.DataFrame) -> pd.DataFrame:
    counts = edges["iliski_turu"].value_counts()
    total = len(edges)
    rows = []
    for rel_type, family, top_family, definition in RELATION_TAXONOMY:
        n = int(counts.get(rel_type, 0))
        rows.append({
            "standard_relation": rel_type,
            "relation_family": family,
            "relation_family_top": top_family,
            "definition": definition,
            "n_occurrences": n,
            "share_of_all_edges_pct": round(100 * n / total, 2) if total else None,
        })
    df = pd.DataFrame(rows).sort_values("n_occurrences", ascending=False).reset_index(drop=True)
    return df


def attach_provenance(rel_event: pd.DataFrame, edges: pd.DataFrame) -> pd.DataFrame:
    """Best-effort match of each final edge row back to its story_level row
    by exact (karakter_1, karakter_2, iliski_ham) within the same
    source_file. Records match status explicitly instead of assuming 1:1."""
    rel_event = rel_event.copy()
    match_status = []
    source_row = []

    sl_cache = {}
    for sf in edges["source_file"].unique():
        sl_cache[sf] = pd.read_csv(STORY_LEVEL / sf, encoding="utf-8-sig")

    for _, e in edges.iterrows():
        sl = sl_cache[e["source_file"]]
        candidates = sl[
            (sl["karakter_1"] == e["karakter_1"]) &
            (sl["karakter_2"] == e["karakter_2"]) &
            (sl["iliski_ham"].astype(str) == str(e["iliski_ham"]))
        ]
        if len(candidates) == 1:
            source_row.append(int(candidates.index[0]))
            match_status.append("matched_unique")
        elif len(candidates) > 1:
            source_row.append(pd.NA)
            match_status.append("matched_ambiguous")
        else:
            source_row.append(pd.NA)
            match_status.append("unmatched_provenance_gap")

    rel_event["source_row"] = source_row
    rel_event["source_row_status"] = match_status
    return rel_event


def build_provenance_table(rel_event: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame({
        "relation_id": rel_event["relation_id"],
        "source_file_final": "data/final/dede_korkut_kenarlar_temiz.csv",
        "source_file_story_level": "data/story_level/" + rel_event["source_file"],
        "source_row_in_story_level": rel_event["source_row"],
        "source_row_status": rel_event["source_row_status"],
        "transformation": "column rename + taxonomy family mapping (see src/build_canonical.py)",
        "extraction_method": rel_event["extraction_method"],
        "validation_status": rel_event["validation_status"],
        "annotator": "original repository coder (identity not recorded in source data)",
        "version": "processed-v4-rebuild",
    })


def build_nodes(nodes: pd.DataFrame, edges: pd.DataFrame, events: pd.DataFrame,
                 aliases: pd.DataFrame, stories: pd.DataFrame) -> pd.DataFrame:
    sf_to_story = dict(zip(stories["source_file"], stories["story_id"]))
    sf_to_order = dict(zip(stories["source_file"], stories["corpus_order"]))

    edges_long = pd.concat([
        edges[["karakter_1_id", "source_file"]].rename(columns={"karakter_1_id": "node_id"}),
        edges[["karakter_2_id", "source_file"]].rename(columns={"karakter_2_id": "node_id"}),
    ])
    events_long = pd.concat([
        events[["aktor_id", "source_file"]].rename(columns={"aktor_id": "node_id"}),
        events.dropna(subset=["hedef_id"])[["hedef_id", "source_file"]].rename(columns={"hedef_id": "node_id"}),
    ])

    rel_count = edges_long.groupby("node_id").size()
    event_count = events_long.groupby("node_id").size()
    story_count = pd.concat([edges_long, events_long]).groupby("node_id")["source_file"].nunique()

    def first_story_for(node_id: str):
        sfs = pd.concat([
            edges_long.loc[edges_long["node_id"] == node_id, "source_file"],
            events_long.loc[events_long["node_id"] == node_id, "source_file"],
        ])
        if sfs.empty:
            return None
        orders = sfs.map(sf_to_order).dropna()
        if orders.empty:
            return None
        min_sf = sfs[orders.idxmin()] if orders.idxmin() in sfs.index else sfs.iloc[orders.values.argmin()]
        return sf_to_story.get(min_sf)

    alias_map = aliases.groupby("standart_ad")["orijinal_ad"].apply(lambda s: sorted(set(s)))

    review_ids = {MERGE_KEEP_ID, MERGE_DROP_ID}

    rows = []
    for _, r in nodes.iterrows():
        nid = r["dugum_id"]
        rows.append({
            "node_id": nid,
            "canonical_name": r["dugum_adi"],
            "node_type": r["dugum_tipi"],
            "aliases": ";".join(alias_map.get(r["dugum_adi"], [])),
            "first_story": first_story_for(nid),
            "story_count": int(story_count.get(nid, 0)),
            "relation_count": int(rel_count.get(nid, 0)),
            "event_count": int(event_count.get(nid, 0)),
            "validation_status": "needs_manual_validation" if nid in review_ids else "ok",
            "source": "data/final/dede_korkut_dugumler_temiz.csv (v3) + entity resolution merge (Phase 3)" if nid == MERGE_KEEP_ID else "data/final/dede_korkut_dugumler_temiz.csv (v3)",
            "notes": "Merged with former node_id 'begil_in_adamlari' (identical canonical_name) in Phase 3 entity resolution; see validation/entity_resolution_candidates.csv" if nid == MERGE_KEEP_ID else "",
        })
    return pd.DataFrame(rows)


def build_aliases_canonical(aliases: pd.DataFrame, nodes: pd.DataFrame) -> pd.DataFrame:
    node_names = set(nodes["dugum_adi"])
    df = aliases.copy()
    df["resolves_to_current_node"] = df["standart_ad"].isin(node_names)
    df["validation_status"] = df["resolves_to_current_node"].map(
        lambda ok: "ok" if ok else "needs_manual_validation_stale_target"
    )
    return df.rename(columns={"orijinal_ad": "raw_form", "standart_ad": "standard_form", "taraf": "role_context"})


def build_validation_status_table() -> pd.DataFrame:
    with open(ROOT / "outputs" / "validation" / "summary.json", encoding="utf-8") as f:
        summary = json.load(f)
    rows = []
    for group, checks in summary.items():
        for check, n in checks.items():
            rows.append({"category": group, "check": check, "n_flagged": n})
    return pd.DataFrame(rows)


def main():
    PROCESSED.mkdir(parents=True, exist_ok=True)
    nodes, edges, events, aliases, index_df = load_final()
    nodes, edges, events = apply_entity_resolution(nodes, edges, events)

    stories = build_stories(index_df, edges)
    rel_event = build_relations_event_level(edges, stories)
    rel_event = attach_provenance(rel_event, edges)
    rel_agg = build_relations_aggregated(rel_event)
    taxonomy = build_relation_taxonomy(edges)
    provenance = build_provenance_table(rel_event)
    nodes_out = build_nodes(nodes, edges, events, aliases, stories)
    aliases_out = build_aliases_canonical(aliases, nodes)
    validation_status = build_validation_status_table()

    stories.to_csv(PROCESSED / "stories.csv", index=False, encoding="utf-8-sig")
    rel_event.to_csv(PROCESSED / "relations_event_level.csv", index=False, encoding="utf-8-sig")
    rel_agg.to_csv(PROCESSED / "relations_aggregated.csv", index=False, encoding="utf-8-sig")
    taxonomy.to_csv(PROCESSED / "relation_taxonomy.csv", index=False, encoding="utf-8-sig")
    provenance.to_csv(PROCESSED / "provenance.csv", index=False, encoding="utf-8-sig")
    nodes_out.to_csv(PROCESSED / "nodes.csv", index=False, encoding="utf-8-sig")
    aliases_out.to_csv(PROCESSED / "aliases.csv", index=False, encoding="utf-8-sig")
    validation_status.to_csv(PROCESSED / "validation_status.csv", index=False, encoding="utf-8-sig")

    print("nodes:", len(nodes_out))
    print("relations_event_level:", len(rel_event))
    print("relations_aggregated (unordered pairs):", len(rel_agg))
    print("stories:", len(stories))
    print("provenance match status counts:")
    print(rel_event["source_row_status"].value_counts())


if __name__ == "__main__":
    main()
