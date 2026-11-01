# Advanced Network Analysis — Faz 6

**Scriptler:** [`src/communities.py`](../src/communities.py), [`src/signed_and_directed.py`](../src/signed_and_directed.py), [`src/multilayer.py`](../src/multilayer.py), [`src/narrative_order.py`](../src/narrative_order.py)
**Config:** [`config/analysis.yaml`](../config/analysis.yaml) (seed=42, community.n_seeds=10, community.resolution_values=[0.5,0.75,1.0,1.25,1.5])
**Önceki adım:** [`reports/04_05_network_construction_and_descriptive_report.md`](04_05_network_construction_and_descriptive_report.md)

Bu raporda "descriptive/exploratory" olarak etiketlenen her sonuç, henüz null-model (Faz 7) veya sensitivity (Faz 8) ile doğrulanmamıştır. **Hiçbir bulgu tek başına "en önemli karakter" veya kesin edebi yargı olarak sunulmamaktadır.**

---

## 1. Community Detection

**Ağ:** `G2_core_social` (309 node, 374 edge — SEMANTIC/kimlik ilişkileri hariç tüm ilişkiler)

### 1.1 Leiden vs Louvain (seed=42, resolution=1.0)

| Algoritma | Modularity | Community sayısı |
|---|---:|---:|
| Leiden (RBConfiguration, resolution=1.0) | **0.6950** | **33** |
| Louvain | **0.7114** | **34** |
| Leiden vs Louvain Adjusted Rand Index | **0.899** | — |

İki algoritma birbirine yüksek oranda benzer partisyonlar üretiyor (ARI 0.899), modularity değerleri de birbirine yakın (0.695 vs 0.711).

### 1.2 Seed stabilitesi (10 seed, Leiden, resolution=1.0)

- Modularity: ortalama **0.6981**, std **0.0028** (çok düşük varyans)
- Community sayısı: 10 seed'in **hepsinde tam olarak 33** (std=0)
- Ortalama ikili (pairwise) Adjusted Rand Index: **0.908**

**Yorum:** Leiden partisyonu bu ağ için yüksek derecede kararlı — farklı random seed'ler pratik olarak aynı community yapısını buluyor.

### 1.3 Resolution sensitivity (Leiden, seed=42)

| Resolution | Community sayısı | Modularity | En büyük community | En küçük community |
|---:|---:|---:|---:|---:|
| 0.50 | 30 | 0.6460 | 115 | 2 |
| 0.75 | 32 | 0.6944 | 78 | 2 |
| 1.00 | 33 | 0.6950 | 72 | 2 |
| 1.25 | 36 | 0.7024 | 59 | 2 |
| 1.50 | 36 | 0.7100 | 53 | 2 |

Resolution arttıkça community sayısı monoton artıyor, modularity de hafifçe artıyor — beklenen davranış, keskin bir faz geçişi/eşik yok.

### 1.4 ⚠️ KRİTİK METODOLOJİK UYARI — 33 community sayısı kısmen trivial bileşen artefaktı

`G2_core_social` ağı **23 bağlantısız bileşenden** oluşuyor (bkz. `outputs/statistics/corpus_network_metrics.csv`). Leiden/Louvain gibi modularity-tabanlı algoritmalar, bağlantısız her bileşeni **otomatik olarak ayrı community'ler** olarak ele alır — bir bileşen içinde gerçek bir alt-yapı olmasa bile o bileşen en az 1 community sayılır. Dolayısıyla:

- **33 community'nin büyük bir kısmı, dev bileşen (261 node) dışındaki 22 küçük bileşenin (bazıları 2-3 node'luk izole ikili/üçlü gruplar) trivial olarak "kendi community'si" sayılmasından kaynaklanıyor.**
- Anlamlı, yorumlanabilir community yapısı yalnızca **261 node'luk dev bileşen içinde** aranmalıdır. Dev bileşen dışındaki "community"ler (küçük izole bileşenler) sosyal kümelenme değil, yalnızca bağlantısızlığın bir yan ürünüdür.
- Bu ayrım daha önce hiçbir raporda yazılı değildi; bu rapor bunu ilk kez açıkça belirtmektedir. **İleride community sonuçları raporlanırken/görselleştirilirken (Faz 11 figürleri) yalnızca dev bileşen alt kümesi kullanılmalı**, ya da toplam community sayısı raporlanırken bu artefakt açıkça belirtilmelidir.

### 1.5 Community Bridge Metrics (participation coefficient, within-module degree)

`outputs/tables/community_bridge_metrics_G2_core_social.csv`. En yüksek participation coefficient (birden fazla community'ye dağılmış bağlantılar, gerçek bir "köprü" adayı):

| Karakter | Participation coefficient | Inter-community edge sayısı |
|---|---:|---:|
| Aruz | 0.778 | 8 |
| Bayındır Han | 0.719 | 9 |
| Çevresindekiler | 0.667 | 2 |
| Dış Oğuz Beyleri | 0.667 | 2 |
| Anne ve Babası | 0.667 | 2 |

**Aruz** (İç Oğuz'a Dış Oğuz'un Asi Olup Beyrek'i Öldürdüğü boyundaki "hain" figürü) hem yüksek participation coefficient'e hem de makul sayıda inter-community edge'e sahip — bu onu **gerçek bir cross-community köprü adayı** yapıyor, sadece yüksek dereceli bir node olmasından değil (madde 22 ayrımı: "sadece yüksek degree" vs "gerçek cross-community bridge"). Ancak bu, henüz tek bir partisyon üzerinden hesaplandı — resolution/algoritma değişse bridge listesi değişebilir, bu da **exploratory** bir bulgudur.

---

## 2. Signed Network Analysis

**Kaynak:** `outputs/tables/signed_network_profile.csv`, `outputs/statistics/signed_structural_balance.json`

### 2.1 Positive/Negative Degree Profili (ilk 5, positive_degree'ye göre)

| Karakter | Positive degree | Negative degree | Pozitif/Negatif oran |
|---|---:|---:|---:|
| Salur Kazan | 59 | 19 | 3.11 |
| Bamsı Beyrek | 21 | 8 | 2.63 |
| Bayındır Han | 13 | 1 | 13.00 |
| Kan Turalı | 9 | 4 | 2.25 |
| Dede Korkut | 8 | 3 | 2.67 |

### 2.2 Structural Balance — **NOT APPLICABLE**

Pozitif/negatif işaretli edge'ler arasında yalnızca **13 üçgen** bulundu — kod içinde belgelenmiş eşiğin (**15 üçgen**) altında. Bu nedenle structural balance (signed triads) analizi **zorla çalıştırılmadı**, `not_applicable` olarak işaretlendi:

> "Only 13 triangles exist among edges with a definite (pozitif/negatif) polarity — below the documented threshold of 15 needed to say anything statistically meaningful about structural balance. Reporting a balance ratio on this few triangles would overstate what a sparse literary network supports."

Bu, madde 24 ve 32'nin "küçük/seyrek networklerde güçlü çıkarım yapma" kuralının doğrudan uygulanmasıdır — **negative/null bir sonuç, gizlenmeden raporlanmıştır.**

---

## 3. Directed Network Analysis

**Ağ:** `G9_directed` (221 node, 324 edge, yalnızca `directionality == 'yönlü'` ilişkiler)

### 3.1 Triadic Census

`outputs/statistics/directed_triad_census_G9.json` (networkx `triadic_census`, 16 triad tipi, MAN etiketleme):

| Triad tipi | Sayı |
|---|---:|
| 003 (bağlantısız üçlü) | 1.719.566 |
| 012 | 41.160 |
| 102 | 10.977 |
| 021D | 776 |
| 111U | 891 |
| 021C | 567 |
| 111D | 296 |
| 201 | 243 |
| 021U | 110 |
| 210 | 17 |
| 030T | 9 |
| 120U | 7 |
| 120C | 5 |
| 120D | 3 |
| 030C | 2 |
| 300 (tam bağlı) | 1 |

Ağ çok seyrek olduğu için ezici çoğunluk (003) bağlantısız üçlülerden oluşuyor — bu beklenen bir sonuç, ayrıca yorumlanmadı. Yalnızca 1 tam-bağlı (300) triad var; küçük sayıda kapalı üçgen (030T/030C/120*/210) motif-tipi analiz için **çok az örnek** sunuyor (bkz. Faz 10, motif analizi gerekirse null model ile karşılaştırılacak, tek başına yorumlanmayacak).

### 3.2 Reciprocity

`G9_directed` reciprocity = **0.358** (`outputs/statistics/corpus_network_metrics.csv`) — yönlü ilişkilerin yaklaşık üçte biri karşılıklı.

### 3.3 HITS (hub/authority)

`outputs/tables/centrality_G9_directed.csv`. En yüksek **hub** skoru: **Salur Kazan (0.425)** — açık ara önde, sonra Bamsı Beyrek (0.057). En yüksek **authority** skoru: **Karaçuk Çoban (0.050)**, Bayındır Han (0.047), Türkistan (0.045), Lala Kılbaş (0.040), Bamsı Beyrek (0.038).

**Yorum:** Salur Kazan'ın out-degree'si (53) in-degree'sinden (30) belirgin şekilde yüksek ve hub skoru authority skorundan çok daha büyük (0.425 vs 0.016) — bu, Salur Kazan'ın yönlü ilişkilerde ağırlıklı olarak **başlatıcı/kaynak** rolünde kodlandığını gösteriyor, alıcı/hedef rolünde değil. Bu yapısal bir gözlemdir, edebi bir "kahramanlık" yargısı değildir.

---

## 4. Multilayer / Multiplex Analysis

**Kaynak:** `outputs/tables/multilayer_profile.csv`. 7 gözlenen layer: `akrabalık, iletişim, kimlik, mekân, olay, otorite, çatışma`.

En çok layer'da aktif olan karakterler (n_active_layers'a göre):

| Karakter | Aktif layer sayısı (/ 7) | Layer participation coefficient |
|---|---:|---:|
| Salur Kazan | 7 | 0.766 |
| Dede Korkut | 6 | 0.531 |
| Uruz | 5 | 0.782 |
| Bayındır Han | 5 | 0.741 |
| Basat | 5 | 0.678 |
| Kan Turalı | 5 | 0.740 |
| Tepegöz | 5 | 0.620 |
| Aruz | 5 | 0.420 |

**Yorum:** Salur Kazan yalnızca en yüksek dereceli node değil, aynı zamanda **tüm 7 layer'da aktif olan tek karakter** — bu, onun rolünün tek bir ilişki türüne (ör. yalnızca çatışma veya yalnızca akrabalık) indirgenemeyeceğini, anlatı boyunca birden çok işlevsel rolde (akraba, otorite figürü, çatışmanın tarafı, iletişim kuran) yer aldığını gösteriyor. Bu **yapısal bir gözlemdir**; "en çok yönlü karakter" gibi bir edebi yargıya dönüştürülmemiştir.

Uruz'un participation coefficient'i (0.782) Salur Kazan'dan (0.766) bile yüksek, ama toplam derecesi çok daha düşük (29 vs 156) — yani Uruz'un az sayıdaki bağlantısı, sahip olduğu 5 layer'a nispeten **daha eşit dağılmış** durumda. Bu iki metriğin (aktif layer sayısı vs participation coefficient) farklı şeyler ölçtüğünü gösteren iyi bir örnek.

---

## 5. Narrative-Order Analysis

**Kaynak:** `outputs/tables/narrative_order_windows.csv`. `satir_no` (→ `narrative_order`) yalnızca **anlatı içi sıra** olarak kullanılmıştır, tarihsel/kronolojik zaman olarak **yorumlanmamıştır** (madde 26 kuralı).

### 5.1 Kapsam

- **S01 (Girizgah): `not_applicable`** — yalnızca 1 ilişki kaydı var, pencereleme için (eşik: en az 6) yetersiz.
- **Diğer 13 boy** için early/middle/late pencerelemesi başarıyla üretildi.

### 5.2 Doğrulama (internal consistency check)

Her boy için pencereleme sonunda ulaşılan `cumulative_distinct_nodes` değeri, Faz 4'te bağımsız olarak hesaplanmış story-level network node sayılarıyla (`data/derived/story_level_metrics.csv`) karşılaştırıldı:

- 12/13 boy'da **birebir eşleşme** (ör. S04: 70=70, S09: 41=41, S14: 20=20).
- **S03'te küçük bir sapma:** pencereleme 47 node buluyor, story-level network 48 node içeriyor. Fark, S03'te `satir_no` alanı boş olan 2 satırdan kaynaklanıyor (Faz 1 audit'te zaten tespit edilmişti) — bu satırlardaki bir node yalnızca o satırlarda görünüyor olabilir, pencereleme yalnızca geçerli `narrative_order`'lı satırları kullandığı için bu node'u kaçırıyor. **Bu bilinen, açıklanmış, kabul edilebilir bir sınırlamadır**, gizlenmemektedir.

Bu çapraz kontrol, pipeline'ın iç tutarlılığı için olumlu bir bulgu.

### 5.3 Örüntüler (yalnızca betimleyici)

Birçok boy'da **çatışma yoğunluğu (`conflict_intensity`) late pencerede early pencereye göre belirgin şekilde artıyor** — ör. S03 (0.00→0.71), S05 (0.00→0.71), S08 (0.25→0.50). Bu, epik anlatı yapısında beklenen bir "yükselen aksiyon → çatışma/doruk" örüntüsüyle tutarlı, ancak bu **yalnızca 13 boy üzerinden betimleyici bir gözlemdir**, istatistiksel bir test (ör. trend testi) yapılmamıştır ve tüm boylarda tutarlı değildir (ör. S06'da conflict_intensity early=0.29, late=0.00 — tam tersi yönde).

---

## 6. Dynamic Centrality (Exploratory)

**Kaynak:** `outputs/tables/dynamic_centrality_trajectory.csv`. Corpus'taki toplam ilişki sayısına göre en yüksek dereceli 6 karakterin, **corpus sunuluş sırasına göre** (S01→S14, gerçek kronoloji değil) kümülatif ilişki-örneği sayısı.

| Karakter | Final kümülatif değer | Görünüm örüntüsü |
|---|---:|---|
| Salur Kazan | 156 | Neredeyse tüm boylar boyunca dağılmış (S03, S04, S05, S09-S14) |
| Bamsı Beyrek | 64 | Ağırlıklı olarak kendi boyunda (S04: +48), sonra S12-S13'te tekrar |
| Bayındır Han | 36 | Birçok boyda düşük-orta düzeyde dağılmış |
| Uruz | 29 | S03, S05, S12'de yoğunlaşmış |
| Tepegöz | 28 | **Yalnızca S09'da** (kendi boyu) |
| Basat | 27 | Ağırlıklı S09, küçük bir kalıntı S13'te |

**Yorum:** Bu tablo, "yüksek toplam dereceye sahip olma" ile "corpus boyunca yaygın görünme" arasındaki farkı somut olarak gösteriyor: Tepegöz ve Basat yüksek toplam dereceye sahip ama **tek bir boyda yoğunlaşmış** (yerel merkeziyet), Salur Kazan ve Bamsı Beyrek ise **birden fazla boyda tekrar eden** karakterler (corpus-çapında merkeziyet). Bu ayrım, "en önemli karakter" gibi tek boyutlu bir sıralamanın neden yanıltıcı olabileceğinin somut bir örneğidir — iki farklı türde merkeziyet var ve ikisi de geçerli, farklı sorulara cevap veriyor.

---

## 7. Genel Değerlendirme: Descriptive/Exploratory vs Doğrulanmış

| Bulgu | Sınıf | Doğrulama durumu |
|---|---|---|
| Community sayısı/modularity (Leiden/Louvain) | Descriptive | Seed stabilitesi test edildi (yüksek); resolution sensitivity test edildi. **Null model karşılaştırması henüz yok (Faz 7).** |
| Community bridge adayları (Aruz, Bayındır Han) | Exploratory | Tek partisyon üzerinden; algoritma/resolution değişkenliğine karşı robustluk test edilmedi. |
| Signed positive/negative profili | Descriptive | Doğrudan veriden sayım, ek doğrulama gerekmiyor. |
| Structural balance | N/A | Veri yetersiz, resmi olarak "not applicable". |
| Directed triadic census, reciprocity, HITS | Descriptive | Null model (configuration model) karşılaştırması henüz yok (Faz 7). |
| Multilayer versatility (Salur Kazan 7/7 layer) | Descriptive | Kişi/grup ayrımına duyarlılığı test edilmedi (Faz 8). |
| Narrative-order pencereleri, çatışma yükselişi örüntüsü | Descriptive | Tutarlılığı iç-çapraz-kontrol ile doğrulandı; istatistiksel trend testi yapılmadı. |
| Dynamic centrality trajectory | Exploratory | Yalnızca top-6 karakterle sınırlı, istatistiksel test yok. |

**Hiçbir bulgu bu raporda "en önemli karakter", "kahramanın gerçek rolü" gibi edebi bir sonuca dönüştürülmemiştir.** Tüm merkeziyet/köprü/versatilite bulguları network-yapısal terimlerle ifade edilmiştir (ör. "yüksek hub skoru", "7 layer'da aktif") ve Faz 7-8 tamamlanmadan güçlü/kesin bilimsel iddia olarak kullanılmayacaktır.

---

## 8. Limitations (bu faza özgü, genel limitasyonlar için `CLAUDE_SESSION_HANDOFF.md`'ye bakınız)

1. **23-bileşen artefaktı** (§1.4) — community sayısı raporlanırken her zaman bu uyarıyla birlikte sunulmalı.
2. **Structural balance analizi yapılamadı** — veri hacmi yetersiz, ileride ek relation kodlaması gelirse tekrar denenebilir.
3. **Triadic census, seyrek ağda ezici çoğunlukla "003" (bağlantısız)** — motif-tipi yorumlama için null model şart (Faz 7'yi bekliyor).
4. **S03'te 2 satırlık `satir_no` eksikliği**, narrative-order pencerelemesinde küçük bir node-sayım sapmasına yol açıyor (47 vs 48) — düzeltilmedi, sadece belgelendi.
5. **Dynamic centrality yalnızca top-6 karakterle sınırlı** — kapsamlı bir "tüm karakterler için trajectory" tablosu üretilmedi (hesaplama maliyeti/rapor okunabilirliği dengesi).
6. Bu fazdaki **hiçbir bulgu, person-only/weighted/explicit-only gibi alternatif network tanımlarına karşı test edilmedi** — bu tam olarak Faz 8'in konusu.

---

## 9. Sıradaki Adım

Faz 7 (Null Models / Statistical Validation): uygun network'lerde degree-preserving randomizasyon (configuration model), clustering/transitivity/assortativity/modularity için observed vs random_mean/std/z-score/percentile/empirical-p karşılaştırması.
