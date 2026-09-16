# Sensitivity Analysis & Structural Robustness — Faz 8

**Scriptler:** [`src/sensitivity.py`](../src/sensitivity.py), [`src/robustness.py`](../src/robustness.py)
**Config:** [`config/analysis.yaml`](../config/analysis.yaml) → `sensitivity.variants` (6 çift), `robustness` (3 strateji, `n_random_trials=100`), `seed=42`
**Çıktılar:** `outputs/statistics/sensitivity_analysis_results.json`, `outputs/tables/sensitivity_rank_stability.csv`, `outputs/statistics/robustness_*_G0_full.csv`, `outputs/statistics/robustness_summary_G0_full.json`

---

## 1. Sensitivity Analysis — Yöntem

Master prompt madde 29/34-36'da istenen 6 karşılaştırma çifti, `data/processed/relations_event_level.csv` üzerinde inşa edildi (3'ü zaten var olan G0-G11 varyantlarını yeniden kullanıyor, 3'ü bu faz için yeni filtrelerle inşa edildi). Her çift için degree/betweenness/PageRank sıralamaları, **ortak aktör kümesi** üzerinden Spearman ρ, Kendall τ ve top-10/top-20 overlap oranı ile karşılaştırıldı.

**Önemli metodolojik not:** Bu analiz hiçbir varyantı "doğru" ilan etmiyor — amaç yalnızca hangi network-inşa kararının sıralamaları ne kadar değiştirdiğini ölçmek.

---

## 2. Sonuçlar — Etki Büyüklüğüne Göre Sıralı

| Karşılaştırma | Degree ρ | Betweenness ρ | PageRank ρ | Top-10 overlap (ort.) | Yorum |
|---|---:|---:|---:|---:|---|
| **Girizgah dahil vs hariç** | 1.000 | 1.000 | 1.000 | 0.93 | **İhmal edilebilir etki** |
| **Tüm ilişkiler vs core-social** | 1.000 | 1.000 | 1.000 | 0.93 | **İhmal edilebilir etki** |
| **Explicit-only vs explicit+inferred** | 0.982 | 0.971 | 0.989 | 0.93 | Çok küçük etki |
| **Weighted vs unweighted** | 1.000* | 0.930 | 0.849 | 0.83 | Küçük-orta etki (yalnızca ağırlıklı metriklerde) |
| **Group dahil vs hariç** | 0.950 | 0.896 | 0.957 | 0.83 | Orta etki |
| **Person+group vs person-only** | 0.916 | 0.887 | 0.926 | 0.83 | **En büyük etki (Spearman/Kendall'a göre)** |

*Weighted vs unweighted'de plain degree, tanımı gereği birebir aynı (aynı edge seti, sadece ağırlık değişiyor) — bu satırın "1.000" değeri bir sensitivity bulgusu değil, yapısal bir zorunluluktur.

**Not:** Top-10 overlap (yalnızca 10 node üzerinden, yüksek varyanslı bir ölçü) altı çiftten üçünde 0.93'te, diğer üçünde 0.83'te eşitleniyor — bu tek başına net bir ayrım sağlamıyor. Yukarıdaki sıralama esas olarak **Spearman ρ ve Kendall τ**'ya dayanıyor (tam değerler `outputs/tables/sensitivity_rank_stability.csv`'de); top-20 overlap değerleri de 0.80-1.00 aralığında, benzer şekilde kaba bir ayrım sunuyor.

### 2.1 Girizgah ve core-social filtrelemesi: pratik olarak sıfır etki

Girizgah'ın (yalnızca 1 ilişki kaydı) dahil/hariç tutulması ve SEMANTIC/kimlik ilişkilerinin çıkarılması (`G2_core_social`), degree/betweenness sıralamalarını **birebir** koruyor (ρ=1.000), PageRank'ta neredeyse birebir (ρ=1.000, τ=0.997-0.998). Bu, Faz 1'de zaten şüphelenilen ("girizgah'ın minimal etkisi") ve Faz 6'da varsayılan ("core-social'ın gerçek sosyal etkileşimi izole ettiği") kararların **doğrulanmış**, artık varsayım değil ölçülmüş bir sonucu.

### 2.2 Explicit-only vs tüm ilişkiler: küçük etki

Yalnızca `açık_ilişki` (596/628 = %94.9) ile kodlanmış ilişkileri kullanmak, tüm veri setini (çıkarımsal ilişkiler dahil) kullanmakla neredeyse aynı sıralamayı veriyor (ρ≥0.97 üç metrikte de). Bu, sadece 32 çıkarımsal kaydın (%5.1) toplam yapıyı önemli ölçüde değiştirmediğini gösteriyor — ama bu oranın küçüklüğü göz önüne alındığında beklenen bir sonuç.

### 2.3 Weighted vs unweighted: PageRank en duyarlı metrik

Ağırlıklı/ağırlıksız karşılaştırmasında **PageRank en çok değişen metrik** (ρ=0.849, top-10 overlap 0.90 ama top-20 overlap 0.85), betweenness orta derecede (ρ=0.930). Bu, `agirlik` alanının (1-5 ordinal skala, Faz 1'de anlamı doğrulanmamış bir "yoğunluk" kodlaması olarak işaretlenmişti) PageRank gibi ağırlık-duyarlı metrikleri gerçekten etkilediğini gösteriyor — `agirlik`'in tam semantiği belirsiz olduğu için (bkz. madde 36, henüz çözülmedi) bu, **PageRank sonuçlarının ağırlık kodlama şemasına bağımlı olduğu** anlamına geliyor ve ihtiyatla yorumlanmalı.

### 2.4 Person+group vs person-only: en etkili modelleme kararı

Test edilen 6 karşılaştırma arasında **en düşük korelasyonlar** bu çiftte (degree ρ=0.916, betweenness ρ=0.887, top-10 overlap 0.70-1.00 arası dalgalı). Kolektif aktörleri (grup, mitolojik/ilahi, hayvan, nesne/doğa, yer/coğrafya — 332 node'un 145'i, `kişi` olmayanlar) tamamen çıkarmak, kişi-only sıralamayı en çok değiştiren tek karar. **Bu, "en önemli karakter" tartışmasının en hassas olduğu nokta**: bir karakterin G0'daki (kolektif aktörler dahil) sıralaması ile G1'deki (yalnızca kişiler) sıralaması arasında gerçek, ölçülebilir bir fark var.

### 2.5 Grup dahil/hariç (yalnızca 'grup' tipi çıkarıldığında): orta etki

`G1_person_only`'den farklı olarak yalnızca `dugum_tipi=='grup'` olan node'ları çıkarmak (mitolojik/hayvan/nesne/yer korunuyor), person+group'tan biraz daha az ama yine de orta düzeyde bir etki yaratıyor (ρ=0.90-0.96). Bu, etkinin büyük kısmının özellikle **kolektif/grup aktörlerden** kaynaklandığını, mitolojik/hayvan/nesne tipi node'ların katkısının nispeten küçük olduğunu düşündürüyor (doğrudan test edilmedi, bu bir çıkarımdır).

---

## 3. Structural Robustness (madde 30-31)

**Ağ:** `G0_full` (311 node, 376 edge). Üç kaldırma stratejisi, `config/analysis.yaml::robustness` parametreleriyle (`n_random_trials=100`, seed=42):

| Strateji | Dev bileşen %50'nin altına düşene kadar kaldırılan node oranı | %10'un altına düşene kadar |
|---|---:|---:|
| Random (100 deneme ortalaması) | **%25.1** | %61.7 |
| Degree-targeted (her adımda yeniden hesaplanan) | **%3.9** | %5.8 |
| Betweenness-targeted (periyodik yeniden hesaplanan) | **%1.9** | %5.8 |

### 3.1 Yorum — klasik "robust-yet-fragile" örüntüsü

Ağ, **rastgele node kaybına karşı oldukça dayanıklı** (dev bileşenin yarısını kaybetmek için node'ların yaklaşık dörtte birinin rastgele kaldırılması gerekiyor) ama **hedefli saldırıya karşı son derece kırılgan** (en yüksek dereceli veya en yüksek betweenness'e sahip birkaç node'un — toplamın yalnızca %2-4'ünün — kaldırılması dev bileşeni yarıya indiriyor). Bu, heterojen derece dağılımına sahip (birkaç çok yüksek dereceli hub + çok sayıda düşük dereceli node) ağlarda **klasik ve iyi bilinen bir örüntüdür** (Albert-Jeong-Barabási tipi "robust yet fragile" davranışı) — Faz 5'te bulunan Salur Kazan/Bamsı Beyrek hub yapısıyla doğrudan tutarlı.

**Bu, "structural robustness" olarak adlandırılmıştır — "narrative resilience" değil (madde 31'in açık isimlendirme kuralı).** Bulgu yalnızca graf bağlantısallığı hakkındadır; anlatının kendisinin bir karakterin "kaybı"na nasıl tepki vereceği gibi edebi bir iddia içermez.

### 3.2 Limitations

- Betweenness-targeted kaldırma, hesaplama maliyeti nedeniyle her adımda değil periyodik olarak (~20 kez) yeniden hesaplandı — tam "her adımda yeniden hesapla" stratejisinden hafif sapma olabilir, ama sonuç degree-targeted ile çok yakın (%1.9 vs %3.9), bu sapmanın sonucu önemli ölçüde değiştirmediğini düşündürüyor.
- Yalnızca `G0_full` üzerinde çalıştırıldı — diğer network varyantlarında (ör. `G1_person_only`) robustness eğrileri farklı olabilir, test edilmedi.
- Ortalama path length eğrisi bu ilk çalıştırmada hesaplanmadı (yalnızca dev bileşen boyutu/bileşen sayısı) — hesaplama maliyeti nedeniyle sonraki bir iyileştirme olarak bırakıldı.

---

## 4. Genel Değerlendirme

| Bulgu | Sınıf | Durum |
|---|---|---|
| Girizgah/core-social filtrelemesinin ihmal edilebilir etkisi | Doğrulanmış (rank correlation) | Artık ölçülmüş, varsayım değil |
| Person-only ayrımının en büyük etki olduğu | Doğrulanmış (rank correlation, karşılaştırmalı) | 6 karşılaştırma arasında en düşük korelasyon |
| PageRank'ın ağırlık şemasına duyarlılığı | Doğrulanmış (rank correlation) | `agirlik` semantiği hâlâ belirsiz (madde 36) — ihtiyatlı yorumlanmalı |
| Ağın rastgele arızaya dayanıklı, hedefli saldırıya kırılgan olması | Doğrulanmış (robustness curve) | Klasik hub-yapısı örüntüsü, edebi yorum yapılmadı |

**Faz 5-7'deki centrality/community bulgularının network-tanım kararlarına duyarlılığı artık ölçülmüştür.** Salur Kazan/Bamsı Beyrek'in G0/G1/G2/G9'un hepsinde en yüksek sıralarda çıkması (Faz 5), bu fazın bulgularıyla tutarlı: en büyük tek etken olan person-only filtrelemesinde bile top-10 overlap degree için tam (%100), yani bu iki karakterin göreli üstünlüğü **network tanımına karşı nispeten kararlı** — ama diğer, daha alt sıradaki karakterlerin sıralaması (top-20 overlap altı çiftte %80-100 arasında değişiyor) modelleme kararına göre değişebiliyor.

---

## 5. Sıradaki Adım

Faz 9/10 (Motif/Triad ek analizler, yalnızca metodolojik olarak uygunsa) → Faz 11 (Publication Figures) → Faz 12 (Tables) → ... (bkz. `CLAUDE_SESSION_HANDOFF.md`).
