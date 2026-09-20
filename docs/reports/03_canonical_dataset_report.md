# Canonical Dataset Report — Faz 3

**Script:** [`src/build_canonical.py`](../src/build_canonical.py)
**Girdiler:** `data/final/*.csv` (değiştirilmedi), `data/story_level/*.csv` (yalnızca provenance eşlemesi için okundu)
**Çıktılar:** `data/processed/*.csv` (8 dosya)

---

## 1. Uygulanan Dönüşümler (hepsi kod içinde izlenebilir)

1. **Tek entity-resolution birleştirmesi uygulandı:** `begil_in_adamlari` → `begilin_adamlari` (Faz 2'de bulunan yüksek güvenli tek çakışma — aynı `dugum_adi`, iki farklı ID). Sayaç alanları (`toplam_gorunum` vb.) toplanarak birleştirildi. **Diğer 17 düşük-güvenli alias çakışması otomatik birleştirilmedi**, `needs_manual_validation` olarak `aliases.csv`'de işaretli kaldı.
2. **Hiçbir edge/event satırı silinmedi veya eklenmedi** — `relations_event_level.csv` = `dede_korkut_kenarlar_temiz.csv`'nin şema-normalize edilmiş birebir kopyası (628 satır, 628 satır).
3. **Aggregation kuralı (belgelenen metodolojik karar, veri gerçeği değil):** `relations_aggregated.csv`, aktör çiftini **yönsüz** (sıralanmamış set) olarak gruplar; yönlülük bilgisi `any_directed`/`any_undirected` bayraklarında korunur, kaybolmaz.
4. **Relation taxonomy** (`relation_taxonomy.csv`), 17 gözlenen `iliski_turu` değerini SOCIAL/KINSHIP/AUTHORITY/SEMANTIC/OTHER/UNCERTAIN üst ailelerine eşler — bu **yorumlayıcı bir kategorileştirme şemasıdır**, ham veriden çıkarılan bir "gerçek" değil; her satırda gerekçe (`definition`) alanı var.
5. **Provenance eşlemesi**: her `relations_event_level.csv` satırı, `(karakter_1, karakter_2, iliski_ham)` üçlüsü üzerinden `data/story_level/` içindeki orijinal satıra **best-effort** eşlendi (kesin/varsayımsal eşleme yapılmadı).

---

## 2. Üretilen Dosyalar

| Dosya | Satır | Not |
|---|---:|---|
| `data/processed/nodes.csv` | 332 | 333 → 332 (1 birleştirme) |
| `data/processed/aliases.csv` | 525 | `resolves_to_current_node` + `validation_status` eklendi |
| `data/processed/stories.csv` | 14 | `story_id` (S01–S14), corpus_order eklendi |
| `data/processed/relations_event_level.csv` | 628 | madde 11 şeması, hiçbir satır kaybı yok |
| `data/processed/relations_aggregated.csv` | 376 | benzersiz aktör çifti |
| `data/processed/relation_taxonomy.csv` | 17 | her `standard_relation` için aile + tanım + n + % |
| `data/processed/provenance.csv` | 628 | her ilişki için story_level satır eşlemesi + durumu |
| `data/processed/validation_status.csv` | 27 | Faz 2 `summary.json`'un düzleştirilmiş hali |

---

## 3. Provenance Eşleme Sonucu

```text
matched_unique             571  (%90.9)
unmatched_provenance_gap    53  (%8.4)
matched_ambiguous            4  (%0.6)
```

571 edge, orijinal `story_level` satırına **kesin** olarak eşlenebildi. 53 edge (`unmatched_provenance_gap`) hiçbir `story_level` satırına tam metin eşleşmesiyle bağlanamadı — bunlar Faz 1'de bulunan +80 satırlık farkın somut karşılığı (satır bölünmesi/genişletmesi nedeniyle orijinal metin `story_level`'da birebir bulunamıyor). 4 edge birden fazla adaya eşleşti (`matched_ambiguous`) — aynı boy içinde aynı üçlü (karakter_1, karakter_2, iliski_ham) birden fazla kez geçiyor.

Bu üç durum da `provenance.csv`'de `source_row_status` alanında açıkça işaretlendi; "eşleşmedi" durumu asla "eşleşti" gibi gösterilmedi.

---

## 4. Relation Taxonomy Özeti (ilk 5, tam tablo `data/processed/relation_taxonomy.csv`)

| standard_relation | family | top | n | % |
|---|---|---|---:|---:|
| belirsiz | uncertain | UNCERTAIN | 186 | 29.62 |
| çatışma | conflict | SOCIAL | 102 | 16.24 |
| akrabalık | kinship | KINSHIP | 68 | 10.83 |
| otorite/emir | authority | AUTHORITY | 57 | 9.08 |
| diyalog_nötr | communication | SOCIAL | 54 | 8.60 |

`UNCERTAIN` ailesi (yalnızca `belirsiz`) analizlerde ayrı tutulacak; SOCIAL/KINSHIP/AUTHORITY/SEMANTIC ailelerine zorla dahil edilmeyecek.

---

## 5. Bilinen Sınırlamalar (bu aşamada çözülmedi, kasıtlı olarak açık bırakıldı)

- `aliases.csv`'de 17 orijinal ifade hâlâ birden fazla `standard_form`'a işaret ediyor (`needs_manual_validation_stale_target` veya bağlama duyarlı olabilir) — `validation/entity_resolution_candidates.csv`'de bekliyor.
- `first_story` alanı, boy'lar arası bir "ilk görülme" sırası kullanıyor (dosya numarası 01–14 = corpus/derleme sırası). **Bu bir anlatı kronolojisi değildir**, yalnızca corpus içi dosya sırasıdır (madde 26 kuralına uygun olarak `narrative_order` ile karıştırılmamalı, `first_story` yalnızca hangi story_id'de ilk göründüğünü gösterir).
- Aggregation yönsüz aktör çifti üzerinden yapıldı; yönlü ağ analizi (Faz 4, G9) bu aggregation'ı kullanmayacak, doğrudan `relations_event_level.csv`'nin `directionality` alanından inşa edilecek.

---

## 6. Sıradaki Adım

Faz 4 (Network Construction): `data/processed/relations_event_level.csv` ve `relations_aggregated.csv` temel alınarak madde 14'teki 11 network modeli (G0–G11) `src/build_networks.py` ile inşa edilecek, `docs/network_models.md` yazılacak.
