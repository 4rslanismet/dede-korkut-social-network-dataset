# Data Quality Report — Faz 2

**Kaynak:** [`outputs/validation/summary.json`](../outputs/validation/summary.json) ve `outputs/validation/*.csv` (26 dosya, hepsi programatik olarak üretildi)
**Script'ler:** [`src/validate.py`](../src/validate.py), [`src/entity_resolution.py`](../src/entity_resolution.py)
**Önceki adım:** [`reports/01_repository_audit.md`](01_repository_audit.md)

Bu rapor, Faz 1'de tespit edilen bulguları tam bir programatik validation framework'üne dönüştürür. Her sayı `outputs/validation/summary.json`'dan alınmıştır; hiçbiri elle girilmemiştir. `data/final/` **değiştirilmedi** — bu aşama yalnızca rapor üretir.

---

## 1. Node Kontrolleri (333 satır)

| Kontrol | Sonuç | Not |
|---|---:|---|
| duplicate_node_id | 0 | ✅ |
| same_name_multiple_ids | 2 satır (1 çakışma çifti) | ⚠️ `Begil'in Adamları` → `begilin_adamlari` / `begil_in_adamlari` |
| capitalization_variants (aynı normalize edilmiş isim, farklı yazım) | 0 | ✅ node tablosunun kendi içinde büyük/küçük harf çakışması yok |
| empty_or_blank_node_name | 0 | ✅ |
| whitespace_in_node_name | 0 | ✅ |
| invalid_id_format (`^[a-z0-9_]+$` dışı) | 0 | ✅ tüm ID'ler slug formatına uygun |

**Değerlendirme:** Node tablosu yapısal olarak çok sağlam. Tek gerçek sorun, Faz 1'de bulunan `Begil'in Adamları` çift-ID çakışması (bkz. §3).

---

## 2. Edge Kontrolleri (628 satır)

| Kontrol | Sonuç | Not |
|---|---:|---|
| missing_source / missing_target | 0 / 0 | ✅ |
| orphan_source_endpoint / orphan_target_endpoint | 0 / 0 | ✅ |
| invalid_layer (gözlenen 7 katman dışı) | 0 | ✅ |
| invalid_polarity (nötr/pozitif/negatif/karışık dışı) | 0 | ✅ |
| invalid_weight (1–5 aralığı dışı / sayısal değil) | 0 | ✅ |
| invalid_directionality (yönlü/yönsüz dışı) | 0 | ✅ |
| duplicate_kayit_id | 0 | ✅ |
| unexpected_self_loop | 1 | ⚠️ `DKR0220`, Bamsı Beyrek → Bamsı Beyrek |
| exact_duplicate_relationship_same_line (aynı satir_no) | 2 | ⚠️ **yanlış pozitif** — bkz. aşağıda |
| repeated_actor_pair_relation_pattern (aynı çift+ilişki+boy, farklı satir_no) | 114 | ℹ️ bilgilendirici, hata değil |

### 2.1 "exact_duplicate_relationship_same_line" — incelendi, gerçek hata değil

İki satır (`DKR0814`, `DKR0815`) `karakter_1_id`, `karakter_2_id`, `iliski_turu` ve `boy` açısından aynı görünüyor çünkü ikisinin de `satir_no` alanı boş (`NaN`). Ancak `iliski_ham`, `not` ve `ham_satir` alanlarına bakıldığında bunlar **iki farklı, kasıtlı olarak eklenmiş coğrafi-epitet kaydı**:

- DKR0814: "Türkistan'ın direği" (ağırlık 3)
- DKR0815: "Türkistan'ın her yanında tanınan" (ağırlık 2)

`not` alanında açıkça "kullanıcı talebine göre eklendi" / "ayrı satır olarak eklendi" yazıyor — yani araştırmacı bu ikisini bilinçli olarak ayrı tutmuş. **Sonuç: gerçek bir duplicate değil**, sadece `satir_no` boş olduğu için basit subset-based duplicate testinde yan yana düştüler. Aggregation (madde 12) sırasında bu iki kayıt, `Salur Kazan`–`Türkistan` çiftinin ağırlıklı toplamına ayrı ayrı katkı yapmalı, tek bir kayıtmış gibi birleştirilmemelidir.

### 2.2 "repeated_actor_pair_relation_pattern" (114 satır) — event-level/aggregated ayrımının tam olarak var olma nedeni

Bu 114 satır, aynı aktör çiftinin aynı `boy` içinde aynı `iliski_turu` ile **farklı `satir_no`** değerlerinde tekrar etmesinden kaynaklanıyor (örn. `300 Kafir`–`Egrek` "belirsiz" ilişkisi satır 674 ve 678'de iki kez). Bunlar anlatı boyunca gerçekleşen **ayrı etkileşimlerdir**, hatalı kopya değil. Bu satırlar **event-level tabloda korunacak**; `data/processed/relations_aggregated.csv` üretilirken (Faz 3) bu tekrarlar `interaction_count`, `total_weight` gibi alanlarda toplanacak, silinmeyecek.

### 2.3 Relation type kapsamı

Gözlenen 17 benzersiz `iliski_turu` değeri `outputs/validation/edge___observed_relation_types.csv` içinde listelendi. En büyük kategori `belirsiz` (%29.6, Faz 1'de raporlandı) — relation taxonomy (Faz 3, madde 13) bu kapsama sınırını açıkça belirtecek.

---

## 3. Event Kontrolleri (85 satır)

| Kontrol | Sonuç | Not |
|---|---:|---|
| missing_actor | 0 | ✅ |
| orphan_actor | 0 | ✅ |
| unsupported_target (hedef var ama node tablosunda yok) | 0 | ✅ |
| duplicate_kayit_id | 0 | ✅ |
| duplicate_event_pattern (aynı aktör+hedef+event_turu+boy) | 11 | ℹ️ edge'lerdeki gibi muhtemelen meşru tekrar; Faz 3'te tek tek incelenecek |

Event tablosu yapısal olarak sağlam.

---

## 4. Alias Sözlüğü Kontrolleri (525 satır) — En Fazla Sorunlu Alan

Bu bölüm, `dede_korkut_alias_sozlugu.csv`'nin basit bir "eski isim → güncel isim" lookup tablosu **olmadığını**, aksine v1→v2→v3 boyunca birikmiş **çok-adımlı bir standardizasyon geçmişi** olduğunu ortaya koyuyor.

| Kontrol | Sonuç |
|---|---:|
| duplicate_original_alias (aynı `orijinal_ad` birden fazla satırda) | 248 satır / 112 benzersiz `orijinal_ad` |
| ... bunlardan `standart_ad` tutarsız olanlar | 17 / 112 |
| alias_maps_to_multiple_targets | 17 benzersiz `orijinal_ad` |
| alias_target_not_in_node_table | 73 satır / 45 benzersiz `standart_ad` |

**Bulgular:**

1. **Çoğu duplicate zararsız:** 112 tekrarlanan `orijinal_ad` değerinden 95'i aynı `standart_ad`'a işaret ediyor — bunlar sadece `taraf` kolonunda (`karakter_1` / `karakter_2` / `event_aktor` vb.) farklılaşıyor, yani "bu isim hem kaynak hem hedef rolünde görülebilir" bilgisini kodluyor. Zararsız.

2. **17 gerçek çakışma:** Aynı `orijinal_ad` farklı `standart_ad` değerlerine standardize edilmiş. Örnekler:
   - `begil bey` → `Begil` **ve** `Begil Bey`
   - `beyrek` → `Bamsı Beyrek` **ve** `Beyrek`
   - `burla` → `Burla` **ve** `Burla Hatun`
   - `iç oğuz beyleri` → `Iç Oğuz Beyleri` **ve** `İç Oğuz Beyleri` (noktalama/aksan farkı — muhtemelen v2→v3 arası tutarsızlık)

   Bunlar iki farklı nedenden olabilir: (a) **bağlama duyarlı standardizasyon** (aynı ham ifade farklı boy'larda farklı karaktere işaret edebilir — README_v3'te belgelenen davranış), ya da (b) **eskimiş ara-adım eşlemesi** (v2'de bir isme, v3'te başka bir isme standardize edilmiş, ikisi de log'da kalmış). Alias tablosunda `boy`/`source_file` kolonu olmadığı için bu ikisi ayırt edilemiyor.

3. **73 satırda hedef (standart_ad), güncel node tablosunda yok** (45 benzersiz isim, örn. `Beyler`, `Burla`, `Begil Bey`, `Dirse'nin Karısı`, `Askerleri`). Bunlar muhtemelen **v1/v2 ara-standardizasyon adımları** — `docs/README_v3.md`'de belgelenen ek bağlamsal ayrıştırma kuralları (`Beyler` → `Beyler (Bamsı Beyrek Boyu)` gibi) bu isimleri **tekrar** standardize etmiş, ama alias sözlüğü zincirin sadece ilk adımını tutmuş, son (v3) adıma kadar takip etmemiş.

**Sonuç:** Alias sözlüğü **tek adımda güvenilir bir lookup tablosu olarak kullanılamaz**. Yeni bir araştırmacı "bu ham ifade hangi canonical entity'ye karşılık geliyor" diye sorduğunda, sözlüğün zincirleme takip edilmesi (chase-through) veya v3 node tablosuyla çapraz doğrulanması gerekir. Bu, Faz 3'teki canonical `aliases.csv` yeniden inşasında (tek-adımlı, node tablosuyla tutarlı) düzeltilecek.

---

## 5. Üretilen Validation Artifactları

```text
outputs/validation/
├── summary.json                                     (bu raporun kaynağı)
├── node__*.csv            (6 dosya)
├── edge__*.csv            (10 dosya)
├── event__*.csv           (5 dosya)
└── alias__*.csv           (3 dosya)

validation/
├── entity_resolution_candidates.csv   (18 aday çift — hiçbiri otomatik birleştirilmedi)
├── HUMAN_REVIEW_QUEUE.csv             (75 madde: entity resolution, stale alias, provenance gap, self-loop)
└── source_edition_metadata_required.md
```

`entity_resolution_candidates.csv` şeması: `entity_a, entity_b, entity_a_name, entity_b_name, similarity_score, evidence, proposed_action, confidence, manual_review_required` — madde 8'de istenen tam alan seti.

`HUMAN_REVIEW_QUEUE.csv` şeması: `item_id, category, source, issue, proposed_action, confidence, requires_human_decision, notes` — madde 128'de istenen tam alan seti. 75 maddenin dağılımı:
- entity_resolution: 18
- stale_alias_target: 45
- provenance_gap: 11 (Faz 1'deki 11 boy'luk story_level↔final satır sayısı uyuşmazlığı)
- unexpected_self_loop: 1

---

## 6. Güncellenmiş Validation Status

```text
VALIDATION STATUS: WARNING

PASS:
  - Node ID bütünlüğü, format, boşluk/whitespace: tam PASS
  - Edge endpoint bütünlüğü, layer/polarity/weight/directionality domain kontrolleri: tam PASS
  - Event actor/target bütünlüğü: tam PASS
  - "Duplicate" gibi görünen 2 edge kaydı incelendi → gerçek hata değil (kasıtlı ayrı epitet kayıtları)

WARNING (insan kararı gerektiriyor, veri değiştirilmedi):
  - 1 node-adı → 2 farklı ID çakışması (Begil'in Adamları)
  - Alias sözlüğü tek-adımlı lookup olarak güvenilir değil (73 satır stale target, 17 gerçek çakışma)
  - 1 beklenmeyen self-loop
  - 11 boy'da story_level→final satır sayısı uyuşmazlığı (Faz 1'den taşındı)

FAIL: yok — hiçbir kritik/blocking hata bulunmadı; final release'i engelleyen bir durum yok,
      ama yukarıdaki WARNING maddeleri Faz 3'teki canonical model inşasından önce
      HUMAN_REVIEW_QUEUE.csv üzerinden değerlendirilmelidir.
```

---

## 7. Sıradaki Adım

Faz 3 (Canonical Dataset): `data/processed/` altında `nodes.csv`, `aliases.csv` (tek-adımlı, düzeltilmiş), `stories.csv`, `relations_event_level.csv`, `relations_aggregated.csv`, `relation_taxonomy.csv`, `provenance.csv`, `validation_status.csv` inşa edilecek. `Begil'in Adamları` çakışması bu aşamada `entity_resolution_candidates.csv`'deki öneriye göre (yüksek güven, otomatik uygulanabilir) çözülecek; düşük güvenli 17 alias çakışması ise `needs_manual_validation=1` ile ayrı tutulacak.
