# Relation Codebook

Every observed value of `standard_relation` (`data/processed/relation_taxonomy.csv`), with its
parent family, directionality/polarity as **actually observed** in the data (not a prescriptive
rule — see the caveat at the end of each entry), and one real example pulled from
`data/processed/relations_event_level.csv`'s `raw_evidence` field.

The family assignments (`relation_family`, `relation_family_top`) are an **interpretive
categorization scheme** (DEC-004 in `docs/decision_log.md`), not a fact extracted from the raw
data — they group semantically similar relation types for analysis (section 13 of the project
brief), and a future researcher could reasonably draw the family boundaries differently.

---

### `akrabalık` (kinship) — 68 occurrences (10.8%)
- **Family:** kinship → KINSHIP
- **Observed directionality:** predominantly yönsüz (undirected) — kinship is treated as
  symmetric at this coding granularity (parent/child/sibling/spouse are not distinguished as
  separate relation types).
- **Observed polarity:** predominantly pozitif.
- **Example:** Bayındır Han–Kam Gan, weight 5, evidence: *"Kam Gan oğlu bayındır han - hanlar
  hanı"*.

### `belirsiz` (uncertain) — 186 occurrences (29.6%) — **largest category**
- **Family:** uncertain → UNCERTAIN (deliberately not folded into any other family)
- The relation type could not be determined from the source text at coding time. **This is the
  single largest coverage gap in the dataset** — any relation-family-based analysis should report
  results with and without this category, or explicitly note its exclusion.
- **Example:** Karaçuk Çoban–Kıyan Güci, evidence: *"karaçuk çoban - kıyan güci (kardeş)"* — note
  the raw evidence literally says "kardeş" (sibling), yet was coded `belirsiz` rather than
  `akrabalık`; this project does not second-guess or re-code the original annotator's judgment.

### `coğrafi_epitet` (geographic epithet) — 3 occurrences
- **Family:** identity_title → SEMANTIC
- An epithet connecting an actor to a place (e.g. "pillar of Turkistan"). Excluded from the
  "core social" network (G2) because it is not a social interaction.
- **Example:** Salur Kazan–Türkistan, evidence: *"Salur Kazan - Türkistan (Türkistan'ın direği)"*.

### `destek/yardım` (support/aid) — 27 occurrences
- **Family:** support → SOCIAL
- **Example:** Boğaç–Hekimler, evidence: *"boğaç - hekimler (iyileştirme)"*.

### `diyalog_nötr` / `diyalog_olumlu` / `diyalog_olumsuz` (neutral/positive/negative dialogue) — 54 / 29 / 12 occurrences
- **Family:** communication → SOCIAL
- Speech-act relations, pre-split by polarity at coding time (so `polarity` and this relation
  type's valence agree by construction for these three).
- **Examples:** diyalog_nötr — Dirse Han–Bayındır Han'ın Adamları, *"Dirse Han - bayındır han'ın
  adamları (diy0)"*; diyalog_olumlu — Hızır–Boğaç, *"Hızır - boğaç (diy+ şifanın yolu)"*;
  diyalog_olumsuz — Dirse Han'ın 40 Adamı–Dirse Han, *"Dirse Han'ın 40 adamı - dirse (diy - 2 kez
  iftira)"*.

### `duygusal_tepki` (emotional reaction) — 4 occurrences
- **Family:** other → OTHER (does not fit cleanly into a social-interaction family)
- **Example:** Bamsı'nın Anne Babası–Bamsı'nın Haberi Gelince, *"bamsı'nın anne babası - bamsı'nın
  haberi gelince (yas tutma)"* (mourning).

### `evlilik/bağlaşıklık` (marriage/alliance) — 10 occurrences
- **Family:** marriage_alliance → KINSHIP
- **Example:** Ak Melik–Alp Eren, *"ak melik - alp eren (alp eren damat)"* (son-in-law).

### `gerilim` (tension) — 7 occurrences
- **Family:** conflict → SOCIAL
- Narrative tension short of open conflict.
- **Example:** Dirse Han'ın 40 Adamı–Boğaç Han, *"Dirse'nin 40 adamı - boğaç han (tuzağa
  çekme)"* (luring into a trap).

### `hareket/eylem` (movement/action) — 9 occurrences
- **Family:** other → OTHER (generic, ambiguous family)
- **Example:** Boğaç–Boğaç'ın 40 Adamı, *"Boğaç - boğaç'ın 40 adamı (hareket)"*.

### `ikna/müzakere` (persuasion/negotiation) — 42 occurrences
- **Family:** cooperation → SOCIAL
- **Example:** Dirse Han'ın 40 Adamı–Dirse Han, *"Dirse han'ın 40 adamı - dirse (ikna)"*.

### `kimlik/unvan` (identity/title) — 2 occurrences
- **Family:** identity_title → SEMANTIC
- **Example:** Dede Korkut–Bayat Boyu, *"Dede korkut - bayat boyu"*.

### `otorite/emir` (authority/command) — 57 occurrences
- **Family:** authority → AUTHORITY
- **Example:** Dirse Han–Oğlu ve 40 Adamı, *"Dirse - oğlu ve 40 adamı (emir - av)"* (order to
  hunt).

### `tören/ritüel` (ceremony/ritual) — 7 occurrences
- **Family:** other → OTHER
- **Example:** Salur Kazan–Karaçuk Çoban, *"kazan - karaçuk çoban (yemek yeme)"*.

### `çatışma` (conflict) — 102 occurrences (16.2%) — second-largest category
- **Family:** conflict → SOCIAL
- **Observed polarity:** predominantly negatif.
- **Example:** Dirse Han'ın 40 Adamı–Dirse Han, *"dirse'nin 40 adamı - dirse (çatışma - dirse esir
  alındı)"* (Dirse taken captive).

### `ödül/değişim` (reward/exchange) — 9 occurrences
- **Family:** cooperation → SOCIAL
- **Example:** Salur Kazan–Karaçuk Çoban, *"kazan - karaçuk çoban (ödül - imrahor)"*.

---

## Notes on `weight` (`agirlik`)

Every relation carries an integer weight 1-5. **The exact semantics of this scale are not fully
documented in the source repository** (see `docs/limitations.md`) — it appears to function as an
ordinal "intensity/importance" coding rather than a literal interaction-repeat count (repeat
interactions between the same actor pair are instead captured by `interaction_count` in
`relations_aggregated.csv`). Phase 8's sensitivity analysis found `weight` materially affects
weighted centrality measures (PageRank rank correlation dropped to ρ=0.849 between weighted and
unweighted variants — the most weight-sensitive metric tested), so any use of `weight` in a
publication should flag this open semantic question.

## Notes on `layer` vs. `relation_family`

These are two **different, independently-coded** classification fields on the same relation row —
do not conflate them. `layer` (7 values: akrabalık, iletişim, çatışma, otorite, kimlik, mekân,
olay) is the original coder's own categorical field. `relation_family`/`relation_family_top` is
this rebuild's later interpretive mapping of `standard_relation` (DEC-004). They agree in spirit
for most rows but are not defined as the same axis — e.g. `layer="olay"` groups relations the
original coder considered event-like, which is a different criterion from any single
`relation_family`.
