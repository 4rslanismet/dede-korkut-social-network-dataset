# Sensitivity Analysis & Structural Robustness — Faz 8

**Scriptler:** [`src/sensitivity.py`](../src/sensitivity.py), [`src/robustness.py`](../src/robustness.py)
**Config:** [`config/analysis.yaml`](../config/analysis.yaml) → `sensitivity.variants` (6 çift), `robustness` (3 strateji, `n_random_trials=100`), `seed=42`
**Çıktılar:** `outputs/statistics/sensitivity_analysis_results.json`, `outputs/tables/sensitivity_rank_stability.csv`, `outputs/statistics/robustness_*_G0_full.csv`, `outputs/statistics/robustness_summary_G0_full.json`

> **Düzeltme notu (bağımsız inceleme sonrası, DEC-017 ve DEC-019).** Bu raporun ilk sürümü iki hata içeriyordu:
> (1) ağırlıklı betweenness, ilişki *gücü* olan `weight` alanını NetworkX'e doğrudan *mesafe* olarak veriyordu (güçlü bağ = uzun yol);
> artık `distance = 1 / strength` kullanılıyor, ağırlıksız (hop-count) betweenness ayrı bir ölçü olarak korunuyor. Aşağıdaki tüm sayılar düzeltilmiş
> hesaplamadan gelir. (2) Robustness bölümü eşiği yanlış adlandırıyordu (asıl eşik *tüm G0 node'larının* %50'siydi, dev bileşenin değil); artık iki payda ayrı ve etiketli raporlanıyor.
> İlk sürümdeki "person+group vs person-only en etkili tek karar" yorumu da desteklenmediği için kaldırıldı (bkz. §2.4).

---

## 1. Sensitivity Analysis — Yöntem

Master prompt madde 29/34-36'da istenen 6 karşılaştırma çifti, `data/processed/relations_event_level.csv` üzerinde inşa edildi (3'ü zaten var olan G0-G11 varyantlarını yeniden kullanıyor, 3'ü bu faz için yeni filtrelerle inşa edildi). Her çift için degree/betweenness/PageRank sıralamaları, **ortak aktör kümesi** üzerinden Spearman ρ, Kendall τ ve top-10/top-20 overlap oranı ile karşılaştırıldı.

**Betweenness tanımı (DEC-017):** kenar özniteliği `weight` ilişki gücüdür (kodlanmış 1-5 `agirlik` değerlerinin toplamı). En kısa yol tabanlı ağırlıklı betweenness bu yüzden **mesafe = 1 / güç** ile hesaplanır (güçlü bağ = kısa yol). `weighted_vs_unweighted` çiftinin "unweighted" kolu G11'dir: tüm güçler 1 olduğundan betweenness'i hop-count betweenness'e eşittir. Merkezilik tablolarında ayrıca `betweenness_hop` sütunu bulunur.

**Önemli metodolojik not:** Bu analiz hiçbir varyantı "doğru" ilan etmiyor — amaç yalnızca hangi network-inşa kararının sıralamaları ne kadar değiştirdiğini ölçmek. Korelasyonlar farklı ortak-node kümeleri üzerinde hesaplanıyor (n=154 ile 311 arası) ve korelasyonlar arası farklar için istatistiksel test yapılmadı.

---

## 2. Sonuçlar — Etki Büyüklüğüne Göre Sıralı

| Karşılaştırma | Degree ρ | Betweenness ρ | PageRank ρ | Ortalama ρ | Top-10 overlap (ort.) | Yorum |
|---|---:|---:|---:|---:|---:|---|
| **Person+group vs person-only** | 0.916 | 0.892 | 0.926 | 0.911 | 0.83 | Orta etki |
| **Weighted vs unweighted** | 1.000* | 0.886 | 0.849 | 0.912 | 0.83 | Orta etki (yalnızca ağırlık-duyarlı metriklerde) |
| **Group dahil vs hariç** | 0.950 | 0.949 | 0.957 | 0.952 | 0.83 | Küçük-orta etki (0.95 eşiğinin hemen altında) |
| **Explicit-only vs explicit+inferred** | 0.982 | 0.984 | 0.989 | 0.985 | 0.90 | Çok küçük etki |
| **Girizgah dahil vs hariç** | 1.000 | 1.000 | 1.000 | 1.000 | 0.93 | **İhmal edilebilir etki** |
| **Tüm ilişkiler vs core-social** | 1.000 | 1.000 | 1.000 | 1.000 | 0.93 | **İhmal edilebilir etki** |

*Weighted vs unweighted'de plain degree, tanımı gereği birebir aynı (aynı edge seti, sadece ağırlık değişiyor) — bu satırın "1.000" değeri bir sensitivity bulgusu değil, yapısal bir zorunluluktur.

**Not:** Sınıflandırma kuralı `outputs/results_registry.json`'da tanımlıdır: "belirgin" = üç ölçütten en az birinde ρ < 0.95. Bu kurala göre **üç seçim** belirgin (person+group vs person-only, weighted vs unweighted, group dahil/hariç), üçü ihmal edilebilir (ρ ≥ 0.98). Belirgin üç seçimin ortalama ρ değerleri arasındaki fark 0.041'dir ve group dahil/hariç eşiğin hemen altında kalır; person+group vs person-only ile weighted vs unweighted ise sayısal olarak **fiilen eşittir** (0.911 vs 0.912) — aralarında sıralama iddiası yapılmaz. Top-10 overlap yalnızca 10 node üzerinden hesaplanan, yüksek varyanslı bir ölçüdür; sınıflandırma esas olarak Spearman ρ'ya dayanır.

### 2.1 Girizgah ve core-social filtrelemesi: pratik olarak sıfır etki

Girizgah'ın (yalnızca 1 ilişki kaydı) dahil/hariç tutulması ve SEMANTIC/kimlik ilişkilerinin çıkarılması (`G2_core_social`), degree/betweenness sıralamalarını **birebir** koruyor (ρ=1.000), PageRank'ta neredeyse birebir (ρ≥0.9997, τ=0.997-0.998). Not: bu iki karşılaştırma yalnızca çok az sayıda ilişkiyi (1 ve 5) çıkardığı için zaten güçlü bir test değildir; sonuç, kararların bu veri setinde pratik etkisi olmadığını gösterir.

### 2.2 Explicit-only vs tüm ilişkiler: küçük etki

Yalnızca `açık_ilişki` (596/628 = %94.9) ile kodlanmış ilişkileri kullanmak, tüm veri setini (çıkarımsal ilişkiler dahil) kullanmakla neredeyse aynı sıralamayı veriyor (ρ ≥ 0.98 üç metrikte de). Bu, sadece 32 çıkarımsal kaydın (%5.1) toplam yapıyı önemli ölçüde değiştirmediğini gösteriyor — ama bu oranın küçüklüğü göz önüne alındığında beklenen bir sonuç.

### 2.3 Weighted vs unweighted: PageRank ve betweenness ağırlık şemasına duyarlı

Ağırlıklı/ağırlıksız karşılaştırmasında **PageRank en çok değişen metrik** (ρ=0.849), betweenness da belirgin biçimde değişiyor (ρ=0.886; ağırlıklı kol mesafe = 1/güç, ağırlıksız kol hop-count). Bu, `agirlik` alanının (1-5 ordinal skala, anlamı doğrulanmamış bir "yoğunluk" kodlaması) ağırlık-duyarlı metrikleri gerçekten etkilediğini gösteriyor — `agirlik`'in tam semantiği belirsiz olduğu için (bkz. madde 36, henüz çözülmedi) bu, **PageRank ve ağırlıklı betweenness sonuçlarının ağırlık kodlama şemasına bağımlı olduğu** anlamına geliyor ve ihtiyatla yorumlanmalı. (İlk sürümde bu çift için betweenness ρ=0.930 raporlanmıştı; bu değer gücün mesafe olarak kullanıldığı hatalı hesaptan geliyordu.)

### 2.4 Person+group vs person-only: orta etki, weighted vs unweighted ile fiilen eşit

Bu çiftte degree ρ=0.916, betweenness ρ=0.892, PageRank ρ=0.926 (ortalama 0.911); top-10 overlap ölçüte göre 0.7-1.0 arasında dalgalanıyor. Kolektif aktörleri (grup, mitolojik/ilahi, hayvan, nesne/doğa, yer/coğrafya — 332 node'un 145'i, `kişi` olmayanlar) tamamen çıkarmak sıralamayı belirgin biçimde değiştiriyor: bir karakterin G0'daki (kolektif aktörler dahil) sıralaması ile G1'deki (yalnızca kişiler) sıralaması arasında ölçülebilir bir fark var. **Ancak bu, "tek en etkili karar" olarak sunulamaz:** weighted vs unweighted ile ortalama ρ farkı 0.001'dir (0.911 vs 0.912), karşılaştırmalar farklı node kümelerinde yapılıyor ve korelasyonlar arası fark test edilmedi. Doğru ifade: aktör-tipi dahil etme ve kenar ağırlıklandırma, sıralamayı en çok değiştiren iki (sayısal olarak eşit) seçimdir; group dahil/hariç daha küçük bir etki gösterir.

### 2.5 Grup dahil/hariç (yalnızca 'grup' tipi çıkarıldığında): küçük-orta etki

`G1_person_only`'den farklı olarak yalnızca `dugum_tipi=='grup'` olan node'ları çıkarmak (mitolojik/hayvan/nesne/yer korunuyor), person+group'tan daha az ama yine de ölçülebilir bir etki yaratıyor (ρ=0.949-0.957, ortalama 0.952). Bu, etkinin bir kısmının **kolektif/grup aktörlerden** kaynaklandığını, mitolojik/hayvan/nesne tipi node'ların katkısının nispeten küçük olduğunu düşündürüyor (doğrudan test edilmedi, bu bir çıkarımdır).

---

## 3. Structural Robustness (madde 30-31)

**Ağ:** `G0_full` (311 node, 376 edge; başlangıç dev bileşeni 261 node). Üç kaldırma stratejisi, `config/analysis.yaml::robustness` parametreleriyle (`n_random_trials=100`, seed=42). En büyük bağlı bileşen (LCC) **iki ayrı paydayla** karşılaştırılır; ikisi farklı soruları yanıtlar ve karıştırılmaz:

- **Payda A — tüm G0 node'ları (311):** LCC < %50 × 311.
- **Payda B — başlangıç dev bileşeni (261):** LCC < %50 × 261.

Kaldırılan node oranı (G0 node'larının yüzdesi; parantez içinde node sayısı). "Grid" = her 6 node'da bir (%2) kontrol edilen kontrol noktaları; "kesin" = her kaldırmadan sonra kontrol:

| Payda | Eşik | Random (100 deneme ort.) | Degree-targeted (grid) | Degree-targeted (kesin; tie-break aralığı) | Betweenness-targeted (grid) | Betweenness-targeted (kesin) |
|---|---|---:|---:|---:|---:|---:|
| A: tüm 311 node | LCC < %50 | **%25.1** (78) | %3.9 (12) | 7 (6-7) | %1.9 (6) | 6 |
| A: tüm 311 node | LCC < %10 | %61.7 (192) | %5.8 (18) | 17 (15-17) | %5.8 (18) | 17 |
| B: başlangıç dev bileşeni 261 | LCC < %50 | %30.9 (96) | %3.9 (12) | 9 (9-9) | %3.9 (12) | 9 |
| B: başlangıç dev bileşeni 261 | LCC < %10 | %65.6 (204) | %5.8 (18) | 17 (15-17) | %5.8 (18) | 17 |

Betweenness-targeted kaldırma **ağırlıksız hop-count betweenness** ile sıralanır (kasıtlı olarak güç-türevi değil; DEC-017'de kategori A). Degree-targeted "kesin" sütunu, eşit dereceli node'lar arasındaki tie-break sırası rastgele değiştirilerek (200 tekrar, seed=43) hesaplanmıştır.

### 3.1 Yorum — hedefli kaldırma rastgeleden çok daha yıkıcı

Ağ, **rastgele node kaybına karşı oldukça dayanıklı**: LCC'nin tüm G0 node'larının yarısının altına düşmesi için node'ların yaklaşık dörtte birinin (%25.1) rastgele kaldırılması gerekiyor (dev bileşene göre ölçüldüğünde %30.9). **Hedefli kaldırmada ise yalnızca 6-9 node** (toplamın yaklaşık %2-3'ü) yeterli. Bu, heterojen derece dağılımına sahip ağlarda **klasik ve iyi bilinen bir örüntüdür** (Albert-Jeong-Barabási tipi "robust yet fragile" davranışı) ve Faz 5'te bulunan hub yapısıyla tutarlıdır. Desteklenen sonuç yalnızca budur: **hedefli kaldırma rastgele kaldırmadan büyük ölçüde daha yıkıcıdır.**

**Degree-targeted ile betweenness-targeted arasında sıralama iddiası yapılmaz.** İlk sürümde raporlanan %3.9 (degree) vs %1.9 (betweenness) farkı büyük ölçüde 6 node'luk kontrol noktası çözünürlüğünün ve tie-break'in bir artefaktıdır: kesin sayımda degree-targeted 6-7, betweenness-targeted 6 node'da eşiği geçiyor — fiilen aynı.

**Bu, "structural robustness" olarak adlandırılmıştır — "narrative resilience" değil (madde 31'in açık isimlendirme kuralı).** Bulgu yalnızca graf bağlantısallığı hakkındadır; anlatının kendisinin bir karakterin "kaybı"na nasıl tepki vereceği gibi edebi bir iddia içermez.

### 3.2 Limitations

- Betweenness-targeted kaldırma, hesaplama maliyeti nedeniyle her adımda değil ~15 kaldırmada bir (n/20) yeniden hesaplandı; degree-targeted her kaldırmadan sonra yeniden hesaplanır.
- Yalnızca `G0_full` üzerinde çalıştırıldı — diğer network varyantlarında (ör. `G1_person_only`) robustness eğrileri farklı olabilir, test edilmedi.
- Ortalama path length eğrisi hesaplanmadı (yalnızca dev bileşen boyutu/bileşen sayısı).
- Random kaldırma yalnızca grid çözünürlüğünde (6 node) raporlanır.

---

## 4. Genel Değerlendirme

| Bulgu | Sınıf | Durum |
|---|---|---|
| Girizgah/core-social filtrelemesinin ihmal edilebilir etkisi | Betimleyici (rank correlation) | Ölçülmüş, varsayım değil; ancak çok az ilişkiyi etkileyen zayıf bir test |
| Aktör-tipi dahil etme (person+group vs person-only) ve kenar ağırlıklandırma sıralamayı en çok değiştiren iki seçim | Betimleyici (rank correlation) | Sayısal olarak fiilen eşit (ortalama ρ 0.911 vs 0.912); tek "en etkili" seçim iddiası yok; fark testi yapılmadı |
| PageRank ve ağırlıklı betweenness'in ağırlık şemasına duyarlılığı | Betimleyici (rank correlation) | `agirlik` semantiği hâlâ belirsiz (madde 36) — ihtiyatla yorumlanmalı |
| Hedefli kaldırmanın rastgeleden çok daha yıkıcı olması | Betimleyici (robustness curve, yalnızca G0) | Klasik hub-yapısı örüntüsü, edebi yorum yapılmadı; degree vs betweenness sıralaması desteklenmiyor |

**Faz 5-7'deki centrality bulgularının network-tanım kararlarına duyarlılığı ölçülmüştür — ve duyarlılık gerçektir.** Salur Kazan; G0, G1, G2 ve G9'un hepsinde degree, strength, PageRank ve iki betweenness tanımında da (mesafe = 1/güç ve hop-count) ilk sırada. Bamsı Beyrek degree/strength/PageRank'ta G0-G2'de ikinci, ancak betweenness sırası **tanıma bağlı**: hop-count'ta G0/G2/G9'da ikinci, mesafe = 1/güç ile G0'da Bayındır Han'la fiilen eşit (0.1912 vs 0.1914), G1'de ise Bayındır Han ve Uruz'un ardında. Daha alt sıradaki karakterlerin sıralaması modelleme kararına göre daha da değişebiliyor (top-10 overlap 0.7-1.0). Bu nedenle betweenness tabanlı her sıralama iddiası, tanımı ve ağ belirtimiyle birlikte yazılmalıdır.

---

## 5. Sıradaki Adım

Faz 9/10 (Motif/Triad ek analizler, yalnızca metodolojik olarak uygunsa) → Faz 11 (Publication Figures) → Faz 12 (Tables) → ... (bkz. `CLAUDE_SESSION_HANDOFF.md`).
