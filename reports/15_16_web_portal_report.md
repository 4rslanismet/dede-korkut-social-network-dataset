# Web Portal & Website Validation — Faz 15-16

> **TARİHSEL KAYIT (Faz 15-16 anı) — güncel sonuç değildir.** Bu rapordaki sayılar o günkü durumu yansıtır:
> "363 sayfa" 3 eski (orphan) sayfa içeriyordu; güncel beklenen sayfa kümesi veriden türetilir (14 statik + 14 boy + 332
> karakter = 360, `outputs/validation/site_validation_report.json`). **PRE-FIX / SUPERSEDED:** betweenness 0.3879
> DEC-017 düzeltmesinden önce, mesafe = güç kullanılarak üretilmişti; güncel yöntem ve değerler için
> `docs/decision_log.md` DEC-017 ve `outputs/tables/publication/T04_centrality_results.csv`'ye bakın.

**Scriptler:** [`src/build_site_data.py`](../src/build_site_data.py), [`src/build_site.py`](../src/build_site.py), [`src/site_layout.py`](../src/site_layout.py), [`docs/assets/explorer.js`](../docs/assets/explorer.js), [`src/validate_site.py`](../src/validate_site.py)

---

## 1. Faz 15 — Web Portal

Statik bir GitHub Pages sitesi `docs/` altında inşa edildi — 14 nav bölümünün tamamı (Home, Dataset, Methodology, Network Explorer, Stories, Characters, Layers, Communities, Similarity, Analysis, Evidence, Downloads, Reproduce, About), madde 52'deki tam listeyle birebir.

**Veri katmanı:** `src/build_site_data.py`, `docs/data/{project_summary,actor_metrics,story_metrics,network_summary}.json` ve `docs/data/networks/{G0_full,G1_person_only,G2_core_social}.json` (Cytoscape formatı) üretiyor — hepsi gerçek `data/processed/` ve `outputs/` dosyalarından, hiçbir sayı elle yazılmadı.

**Sayfa sayıları:** 363 HTML dosyası — 14 statik sayfa + 14 boy detay sayfası (`stories/S01-S14.html`) + **332 karakter profil sayfası** (`characters/*.html`, tüm canonical aktörler için, yalnızca ilk 60 değil — çünkü boy sayfaları herhangi bir aktöre link verebiliyordu, eksik sayfa üretimi kırık link yaratırdı).

**Network Explorer:** Cytoscape.js (cdnjs üzerinden), 3 network varyantı arasında geçiş, arama (highlight+auto-fit), 3 layout seçeneği, node/edge tıklama ile detay paneli. Tarayıcıda canlı test edildi: arama "Kazan" → Salur Kazan doğru vurgulandı; node/edge tıklama detay panelini doğru dolduruyor.

**⚠️ Kritik düzeltme — GitHub Pages path sorunu:** İlk taslakta sayfalar `../outputs/...`, `../data/...`, `../reports/...` gibi repo-root-göreli yollar kullanıyordu. Bu, dosyaları yerel diskte (`file://` veya repo-root sunucusu) görüntülerken çalışıyor gibi görünse de, **GitHub Pages yalnızca `docs/` klasörünü yayınladığı için gerçek sitede bu linklerin tamamı 404 verirdi**. Düzeltme: `copy_assets()` fonksiyonu, kullanılan 8 figürü (`docs/figures/`), tüm `reports/*.md`'yi (`docs/reports/`) ve indirilebilir veri/network/tablo dosyalarını (`docs/downloads/`) **site build sırasında `docs/` içine kopyalıyor**, tüm linkler buna göre güncellendi. Bu, gerçek bir dev-server testiyle (Python `http.server`, `docs/` kökünden) yakalandı — yalnızca `file://` önizlemesi bunu göstermemişti.

**İkinci düzeltme — dosya adı uzunluğu:** Canonical veri setinde 5 node, virgülle ayrılmış birden fazla karakter adını tek bir node'da birleştirmiş (aşağıda, yeni bulgu). Bunlardan biri 239 karakter uzunluğunda bir `node_id`'ye sahip, bu da Windows dosya yolu sınırını aşıp `characters/<id>.html` yazımını başarısız kılıyordu. `safe_filename()` (Python ve JS'de eşleştirilmiş, deterministik kesme+uzunluk-soneki) ile çözüldü — yalnızca dosya adı kısaltıldı, `node_id`/`canonical_name` verisi değiştirilmedi.

---

## 2. YENİ BULGU — Birleştirilmiş Çoklu-Aktör Node'ları (Website inşası sırasında keşfedildi)

Site inşası sırasında **5 node**'un `canonical_name` alanının virgülle ayrılmış birden fazla farklı karakter/grup adı içerdiği keşfedildi — ör.:

- `beyrek_yigenek_kazan_kara_budak_deli_dundar_uruz` → "Beyrek, Yigenek, Kazan, Kara Budak, Deli Dündar, Uruz" (6 farklı karakter, tek node, `relation_count=0`)
- `kazan_kardesi_kara_gone_kiyan_selcuk_oglu_deli_dundar_...` → 10 farklı karakter/grup adı, tek node (`relation_count=1`)

Bu, muhtemelen v1-v3 kodlama sürecinde aynı satırda birden fazla karakterin birlikte anıldığı bir anlatı satırının ayrı ayrı node/ilişkilere bölünmemiş olmasından kaynaklanıyor. **Bu Faz 2'nin otomatik doğrulama testlerinden hiçbirini ihlal etmiyordu** (benzersiz ID, orphan yok, vb.) — yalnızca içerik/anlamsal bir kalite sorunu, yapısal değil.

**Aksiyon:** Otomatik olarak düzeltilmedi (node bölme + ilişki yeniden türetme gerektirir, bu website inşası kapsamının dışında). `validation/HUMAN_REVIEW_QUEUE.csv`'ye 5 yeni madde eklendi (**HR0076-HR0080**, kategori: `concatenated_multi_actor_node`). Bu node'ların karakter sayfaları site üzerinde hâlâ mevcut (gerçek veriyi olduğu gibi gösteriyor), sadece dosya adları güvenli uzunlukta kesildi.

---

## 3. Faz 16 — Website Validation

`src/validate_site.py` yazıldı: `docs/` altındaki her HTML dosyasını tarıyor, her `href`/`src`/`fetch()` referansını dosya sisteminde gerçekten var olup olmadığına göre kontrol ediyor (GitHub Pages'in bir statik dosya sunucusu gibi çözümleyeceği şekilde), `docs/data/*.json`'ın geçerli JSON olduğunu doğruluyor, ve nav öğelerinin hepsinin var olduğunu kontrol ediyor.

**İlk çalıştırma:** 85 kırık link bulundu (yukarıdaki iki hatanın sonucu). **Düzeltme sonrası:** `outputs/validation/site_validation_report.json` → **363 HTML dosyası kontrol edildi, 0 sorun.**

```text
VALIDATION STATUS: PASS - no broken internal links, missing assets, or invalid JSON found.
```

Ayrıca gerçek bir tarayıcıda (Python `http.server`, port 8123) manuel olarak test edildi: Home, Network Explorer (arama+tıklama), Communities (23-bileşen uyarısı + figür), Analysis (3 figür), Evidence (manifest linki), bir karakter sayfası (Salur Kazan — sayılar Faz 5 ile birebir tutarlı: degree=72, strength=436, betweenness=0.3879 **[PRE-FIX / SUPERSEDED: DEC-017'den önce, mesafe = güç ile üretilmişti; güncel bilimsel sonuç olarak kullanılmamalı — düzeltilmiş mesafe-ağırlıklı betweenness (mesafe = 1/strength) 0.598, bkz. T04]**, pagerank=0.0921).

---

## 4. Bilinen Sınırlamalar

- **Similarity sayfası kısmi** — yalnızca ham shared-actor projeksiyonu (madde 17'nin tam benzerlik metrik seti hâlâ eksik, açıkça sayfada belirtildi).
- Yalnızca 3 network varyantı (G0, G1, G2) Explorer'da mevcut — G3-G11 henüz JSON'a export edilmedi (kolayca eklenebilir, `src/build_site_data.py::build_cytoscape_json` genelleştirilmiş).
- Mobil/responsive görünüm ve klavye erişilebilirliği (madde 69-70) sistematik olarak test edilmedi — CSS responsive kurallar içeriyor (`grid-template-columns: repeat(auto-fit/auto-fill,...)`) ama gerçek cihazda doğrulanmadı.
- TR/EN dil altyapısı (madde 71) uygulanmadı — site yalnızca İngilizce (madde 71'in izin verdiği varsayılan).
- Site henüz gerçek GitHub Pages'e deploy edilmedi (branch henüz push edilmedi) — yalnızca yerel sunucuda test edildi.

---

## 5. Sıradaki Adım

Faz 17 (Documentation: data dictionary, relation codebook, methodology.md, limitations.md, architecture diagram) → Faz 18-19 (paper/thesis package) → Faz 20-21 (final validation, final reports).
