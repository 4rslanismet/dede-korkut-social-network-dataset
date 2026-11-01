"""Composite-node candidate detector (DEC-018).

Some canonical actors have labels that may denote SEVERAL actors collapsed
into one node (comma-separated lists, "X ve Y" constructions, sentence-like
phrases). Whether a given label is a legitimate collective entity or an
un-split list can only be decided by a human against the original text, so
this script NEVER merges or splits anything: it flags REVIEW CANDIDATES,
quantifies how much of the network they touch, and adds each one (once) to
validation/HUMAN_REVIEW_QUEUE.csv as category `composite_node_candidate`.

Triggers (a candidate can match several; none of them implies an error):
  comma_list       name contains a comma
  ve_conjunction   name contains the conjunction " ve "
  slash_plus_amp   name contains "/", "+" or "&"
  long_phrase      name has >= 6 whitespace-separated words (sentence-like)
Limitation (by design): this is a HEURISTIC and it is under-inclusive. " ile " ("with")
constructions, hyphen-joined names and phrases shorter than 6 words are not detected. Known
examples it does not flag: "Egreke Yol Gösterdi" (a possible sentence fragment) and
"Kayın Ata - Kayın Anası" (possibly two kin terms in one node). A flag is a triage aid, not
proof, and the absence of a flag does not mean a node is a single actor; the flagged count is the
output of the rules above, not an estimate of how many nodes are truly composite. Manual entity
review against the original text remains required (a publication blocker), and this script
never splits, merges or recodes a node.

Outputs
  validation/composite_node_candidates.csv
  outputs/statistics/composite_node_summary.json
  validation/HUMAN_REVIEW_QUEUE.csv   (composite_node_candidate rows appended;
                                       previously queued nodes are not duplicated)

Pipeline position: after build_canonical (needs data/processed) and after
entity_resolution (which regenerates the queue)."""
import json
import re
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
VALIDATION = ROOT / "validation"
OUT_STATS = ROOT / "outputs" / "statistics"

QUEUE_CATEGORY = "composite_node_candidate"
LONG_PHRASE_WORDS = 6
PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


def find_triggers(name: str) -> list:
    triggers = []
    if "," in name:
        triggers.append("comma_list")
    if re.search(r"\sve\s", name, flags=re.IGNORECASE):
        triggers.append("ve_conjunction")
    if re.search(r"[/+&]", name):
        triggers.append("slash_plus_amp")
    if len(name.split()) >= LONG_PHRASE_WORDS:
        triggers.append("long_phrase")
    return triggers


def n_name_parts(name: str) -> int:
    return len([p for p in re.split(r",|\sve\s|[/+&]", name, flags=re.IGNORECASE) if p.strip()])


def classify(name: str, node_type: str, triggers: list) -> tuple:
    """(suggested_review_category, review_priority, note)"""
    parts = n_name_parts(name)
    if "comma_list" in triggers and parts >= 3:
        return ("possible_multi_actor_list", "high",
                f"{parts} comma/conjunction-separated parts; likely several actors in one node")
    if len(triggers) >= 2 and "long_phrase" in triggers:
        return ("possible_sentence_fragment_or_list", "high",
                "long phrase that also matches another composite trigger")
    if "comma_list" in triggers:
        return ("possible_pair_or_fragment", "medium",
                "two comma-separated parts; may be a pair of actors or an action fragment")
    if "ve_conjunction" in triggers and node_type != "grup":
        return ("individual_type_names_multiple_actors", "medium",
                f"typed '{node_type}' but the label joins several names with 've'")
    if "ve_conjunction" in triggers or "slash_plus_amp" in triggers:
        return ("likely_collective_label_verify_intent", "low",
                "typed as a group; may be a legitimate collective entity (e.g. 'X ve Askerleri')")
    return ("possible_sentence_fragment_not_actor", "medium" if node_type != "grup" else "low",
            "long phrase only; may be a description rather than an actor"
            + ("" if node_type == "grup" else f" (typed '{node_type}', i.e. as an individual)"))


def build_candidates(nodes: pd.DataFrame, rel: pd.DataFrame, queue: pd.DataFrame) -> pd.DataFrame:
    endpoints = pd.concat([rel["source_id"], rel["target_id"]]).value_counts()
    queued = {}
    manual = queue[queue["category"] == "concatenated_multi_actor_node"]
    for item_id, issue in zip(manual["item_id"], manual["issue"]):
        m = re.search(r"node_id='([^']+)'", str(issue))
        if m:
            queued[m.group(1)] = item_id

    rows = []
    for _, n in nodes.iterrows():
        name = str(n["canonical_name"])
        triggers = find_triggers(name)
        if not triggers:
            continue
        nid = n["node_id"]
        category, priority, note = classify(name, n["node_type"], triggers)
        rows.append({
            "node_id": nid,
            "canonical_name": name,
            "trigger": "+".join(triggers),
            "story_count": int(n["story_count"]),
            "relation_endpoint_count": int(endpoints.get(nid, 0)),
            "relation_count": int(((rel["source_id"] == nid) | (rel["target_id"] == nid)).sum()),
            "current_type": n["node_type"],
            "suggested_review_category": category,
            "requires_human_review": True,
            "notes": note,
            "n_name_parts": n_name_parts(name),
            "review_priority": priority,
            "already_queued_as": queued.get(nid, ""),
        })
    df = pd.DataFrame(rows)
    df["_p"] = df["review_priority"].map(PRIORITY_ORDER)
    return df.sort_values(["_p", "node_id"]).drop(columns="_p").reset_index(drop=True)


def append_to_queue(queue: pd.DataFrame, cand: pd.DataFrame) -> tuple:
    """Idempotent: drop earlier composite_node_candidate rows, then append one row per
    candidate that is not already covered by a hand-written concatenated-node item."""
    base = queue[queue["category"] != QUEUE_CATEGORY].copy()
    next_id = int(base["item_id"].str.slice(2).astype(int).max()) + 1
    new_rows = []
    for _, c in cand[cand["already_queued_as"] == ""].iterrows():
        new_rows.append({
            "item_id": f"HR{next_id:04d}",
            "category": QUEUE_CATEGORY,
            "source": "data/processed/nodes.csv (validation/composite_node_candidates.csv)",
            "issue": (f"node_id='{c['node_id']}' canonical_name='{c['canonical_name']}' matches composite trigger(s) "
                      f"{c['trigger']} (type={c['current_type']}, {c['relation_count']} relations, "
                      f"{c['story_count']} stories): {c['notes']}."),
            "proposed_action": ("Manual review against the original text: keep as one collective entity, or split into "
                                "separate actors and re-derive the relations. NOT resolved automatically."),
            "confidence": "medium" if c["review_priority"] == "high" else "low",
            "requires_human_decision": True,
            "notes": f"review_priority={c['review_priority']}; category={c['suggested_review_category']}",
        })
        next_id += 1
    out = pd.concat([base, pd.DataFrame(new_rows, columns=queue.columns)], ignore_index=True)
    return out, len(new_rows)


def summarize(cand: pd.DataFrame, nodes: pd.DataFrame, rel: pd.DataFrame, n_new_queue: int) -> dict:
    ids = set(cand["node_id"])
    total_endpoints = int(2 * len(rel))
    touching = rel["source_id"].isin(ids) | rel["target_id"].isin(ids)
    endpoints_on = int(rel["source_id"].isin(ids).sum() + rel["target_id"].isin(ids).sum())
    trig = {}
    for t in cand["trigger"]:
        for part in t.split("+"):
            trig[part] = trig.get(part, 0) + 1
    return {
        "purpose": "Candidate composite actor labels requiring manual entity-resolution review (DEC-018). Not auto-resolved; a candidate is not necessarily an error.",
        "detector": {"triggers": ["comma_list", "ve_conjunction", "slash_plus_amp", f"long_phrase(>={LONG_PHRASE_WORDS} words)"],
                     "not_detected": "' ile ' constructions and shorter sentence-like phrases (under-approximation)"},
        "n_canonical_nodes": int(len(nodes)),
        "n_candidate_nodes": int(len(cand)),
        "share_of_nodes": round(len(cand) / len(nodes), 4),
        "by_priority": cand["review_priority"].value_counts().to_dict(),
        "by_trigger": trig,
        "by_current_type": cand["current_type"].value_counts().to_dict(),
        "n_already_in_queue_from_dec013": int((cand["already_queued_as"] != "").sum()),
        "n_new_queue_items_added": int(n_new_queue),
        "relations_total": int(len(rel)),
        "relations_touching_candidates": int(touching.sum()),
        "share_of_relations": round(float(touching.mean()), 4),
        "relation_endpoints_total": total_endpoints,
        "relation_endpoints_on_candidates": endpoints_on,
        "share_of_endpoints": round(endpoints_on / total_endpoints, 4),
        "candidates_with_zero_relations": int((cand["relation_count"] == 0).sum()),
    }


def main():
    nodes = pd.read_csv(PROCESSED / "nodes.csv", encoding="utf-8-sig")
    rel = pd.read_csv(PROCESSED / "relations_event_level.csv", encoding="utf-8-sig")
    queue = pd.read_csv(VALIDATION / "HUMAN_REVIEW_QUEUE.csv", encoding="utf-8-sig")

    cand = build_candidates(nodes, rel, queue)
    cand.to_csv(VALIDATION / "composite_node_candidates.csv", index=False, encoding="utf-8-sig")

    new_queue, n_new = append_to_queue(queue, cand)
    new_queue.to_csv(VALIDATION / "HUMAN_REVIEW_QUEUE.csv", index=False, encoding="utf-8-sig")

    summary = summarize(cand, nodes, rel, n_new)
    OUT_STATS.mkdir(parents=True, exist_ok=True)
    with open(OUT_STATS / "composite_node_summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print(f"composite-node candidates: {summary['n_candidate_nodes']} of {summary['n_canonical_nodes']} nodes")
    print(f"  by priority: {summary['by_priority']} | by trigger: {summary['by_trigger']}")
    print(f"  already queued (DEC-013): {summary['n_already_in_queue_from_dec013']} | new queue items: {n_new}")
    print(f"  relations touching candidates: {summary['relations_touching_candidates']}/{summary['relations_total']} "
          f"({summary['share_of_relations']:.1%}); endpoints: {summary['relation_endpoints_on_candidates']}/"
          f"{summary['relation_endpoints_total']} ({summary['share_of_endpoints']:.1%})")
    print(f"HUMAN_REVIEW_QUEUE.csv now has {len(new_queue)} rows")


if __name__ == "__main__":
    main()
