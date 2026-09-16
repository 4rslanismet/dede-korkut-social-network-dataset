# Null Models / Statistical Validation — Faz 7

**Script:** [`src/null_models.py`](../src/null_models.py), [`src/null_models_fdr.py`](../src/null_models_fdr.py)
**Config:** [`config/analysis.yaml`](../config/analysis.yaml) — `seed=42`, `null_models.n_random=1000` (FULL mode), `multiple_testing.method=benjamini_hochberg`, `alpha=0.05`
**Çıktılar:** `outputs/null_models/null_model_results_{fast,full}.json`, `outputs/statistics/null_model_summary.json`, `outputs/statistics/null_model_fdr_corrected.csv`

Bu faz, Faz 5-6'daki bütün betimleyici bulguları (clustering, modularity, assortativity) **rastgele (degree-preserving) bir ensemble'a karşı** test eder. Amaç: gözlenen yapının, yalnızca derece dağılımının bir sonucu mu yoksa gerçekten ek bir yapısal sinyal mi olduğunu ayırt etmek.

---

## 1. Yöntem (DEC-008, bkz. `docs/decision_log.md`)

- **Randomizasyon:** `networkx.double_edge_swap` — her ağın basit (ağırlıksız) kopyası üzerinde, `n_swaps = 10 × n_edges` takas denemesi. Bu, tam derece dizisini koruyan configuration-model eşdeğeri bir prosedürdür.
- **Hariç tutulan ağlar:** 20 edge'den az olan hiçbir ağ yok bu sette (en küçüğü G3_kinship: 61 edge) — ama eşik kodda açıkça tanımlı (`MIN_EDGES_FOR_NULL_COMPARISON=20`), ileride daha küçük bir ağ eklenirse otomatik `not_applicable` olacak.
- **Test edilen ağlar:** G0_full, G1_person_only, G2_core_social, G3_kinship, G4_communication, G5_cooperation_support, G6_conflict, G7_positive, G8_negative (9 ağ). G9_directed'e yönlü-uyumlu bir null model (bu fazda) uygulanmadı — bu bir sonraki iyileştirme adımı olarak not edildi (§6).
- **Test edilen metrikler:** average clustering, transitivity, degree assortativity, Louvain modularity (seed=42, tüm karşılaştırmalarda networkx'in `louvain_communities`'i — Faz 6'nın Leiden sonucuyla karıştırılmamalı, burada tutarlılık için tek bir hızlı algoritma tüm ensemble'da kullanıldı).
- **FAST mode** (`--fast`, n_random=100): geliştirme/iterasyon için, 29 saniyede tamamlandı.
- **FULL mode** (varsayılan, n_random=1000, config'ten): raporun temel aldığı sonuçlar, ~4 dakika 35 saniyede tamamlandı. FAST ve FULL sonuçları yön ve anlamlılık açısından tutarlı (bkz. §5).
- **Seed:** `config/analysis.yaml::seed=42`, her ağ için ayrıca `seed + i` (i = randomizasyon indeksi) modularity hesaplamasında kullanıldı — tam olarak raporlanmıştır.
- **Multiple testing:** 9 ağ × 4 metrik = **36 test**. Benjamini-Hochberg FDR (α=0.05) uygulandı (`statsmodels.stats.multitest.multipletests`).

---

## 2. Sonuçlar — FDR Düzeltmesi Öncesi ve Sonrası

Tam tablo: [`outputs/statistics/null_model_fdr_corrected.csv`](../outputs/statistics/null_model_fdr_corrected.csv) (36 satır, `empirical_p`'ye göre sıralı).

**12/36 test, BH-FDR düzeltmesinden sonra anlamlı kalıyor (α=0.05):**

| Ağ | Metrik | Observed | z-score | empirical p | BH q-value |
|---|---|---:|---:|---:|---:|
| G0_full | modularity (Louvain) | 0.7235 | 7.04 | 0.0010 | 0.0120 |
| G2_core_social | clustering | 0.0719 | 4.10 | 0.0010 | 0.0120 |
| G2_core_social | modularity (Louvain) | 0.7245 | 6.88 | 0.0010 | 0.0120 |
| G0_full | clustering | 0.0713 | 3.94 | 0.0020 | 0.0180 |
| G1_person_only | modularity (Louvain) | 0.6906 | 3.28 | 0.0030 | 0.0216 |
| G1_person_only | clustering | 0.0735 | 3.01 | 0.0040 | 0.0240 |
| G1_person_only | transitivity | 0.0780 | 3.00 | 0.0060 | 0.0270 |
| G6_conflict | modularity (Louvain) | 0.8692 | 2.71 | 0.0060 | 0.0270 |
| G7_positive | modularity (Louvain) | 0.7787 | 2.82 | 0.0080 | 0.0320 |
| G8_negative | modularity (Louvain) | 0.8741 | 2.58 | 0.0100 | 0.0360 |
| G4_communication | modularity (Louvain) | 0.6829 | 2.62 | 0.0110 | 0.0360 |
| G4_communication | clustering | 0.0905 | 2.20 | 0.0160 | 0.0480 |

**Anlamlı kalmayan (24/36), en dikkat çekici olanlar:**

| Ağ | Metrik | Observed | z-score | empirical p | BH q-value | Not |
|---|---|---:|---:|---:|---:|---|
| G0_full | degree_assortativity | −0.192 | −2.17 | 0.032 | **0.089** | Ham p<0.05 ama FDR sonrası anlamsız |
| G2_core_social | degree_assortativity | −0.191 | −1.87 | 0.062 | 0.149 | |
| G6_conflict | degree_assortativity | −0.241 | −1.89 | 0.062 | 0.149 | |
| G3_kinship | tüm 4 metrik | — | ~0 | ≥0.45 | ≥0.67 | Random ile ayırt edilemiyor |

---

## 3. Bilimsel Yorum

### 3.1 Modularity/community yapısı — **doğrulanmış, en güçlü bulgu**

**Test edilen 7 ağın tamamında** (G0, G1, G2, G4, G6, G7, G8 — G3 ve G5 hariç) Louvain modularity, aynı derece dizisine sahip rastgele ağlardan **istatistiksel olarak anlamlı derecede yüksek** (FDR-düzeltmeli, α=0.05). Bu, Faz 6'da bulunan community yapısının (§1, Leiden mod=0.695, 33 topluluk) **yalnızca derece dağılımının bir yan ürünü olmadığını, gerçek ek bir yapısal sinyal olduğunu gösteren ilk doğrulanmış sonuçtur.**

**Ama dikkat:** Bu doğrulama, Faz 6 §1.4'te belirtilen 23-bileşen uyarısını geçersiz kılmaz — modularity'nin rastgeleden yüksek olması beklenir çünkü rastgele (degree-preserving) ağ da genellikle bağlantısızdır ve kendi bileşenlerine sahiptir; iki taraf da bu etkiyi taşıdığı için karşılaştırma yine de anlamlıdır, ama **33 community sayısının ne kadarının dev bileşen içi gerçek alt yapı, ne kadarının küçük bileşenlerin trivial ayrılması olduğu bu testle ayrıştırılmamıştır.** Bu, gelecekteki bir iyileştirme olarak not edilmiştir (§6).

### 3.2 Clustering — kısmen doğrulanmış

G0_full, G1_person_only, G2_core_social ve G4_communication'da clustering coefficient rastgeleden anlamlı derecede yüksek. **G1_person_only'de ayrıca transitivity de anlamlı.** Bu, bu ağlarda üçgen-tipi kapanma (ör. "A-B ve B-C bağlıysa A-C de bağlı") derece dağılımının beklediğinden fazla olduğunu gösteriyor — epik anlatıda sıkça görülen "ortak sahne/grup etkileşimi" örüntüsüyle tutarlı bir yapısal bulgu.

G3_kinship, G5_cooperation_support, G6_conflict, G7_positive, G8_negative'de clustering/transitivity **rastgeleden ayırt edilemiyor** — bu ağlarda gözlenen (genelde çok düşük) clustering değerleri sadece seyreklik ve derece dağılımının beklenen sonucu, ek bir "gruplaşma" sinyali yok. **Bu bir negative/null sonuçtur ve gizlenmemiştir.**

### 3.3 Degree assortativity — **doğrulanmamış** (önemli düzeltme)

Faz 5 raporu, tüm ana varyantlarda negatif degree assortativity'yi ("disassortative", hub-and-spoke yapı) betimleyici bir bulgu olarak sundu. **Bu faz, bu gözlemin istatistiksel olarak sağlam olmadığını gösteriyor:** 9 ağın hiçbirinde degree assortativity, FDR düzeltmesinden sonra rastgeleden anlamlı şekilde farklı değil (en düşük q-value G0_full için 0.089, α=0.05 eşiğinin üzerinde). G0_full'ün ham p-değeri (0.032) düzeltme öncesi anlamlı görünüyordu ama çoklu test düzeltmesi bunu eledi.

**Sonuç:** Negatif assortativity değerleri muhtemelen büyük ölçüde derece dağılımının kendisinden (birkaç çok yüksek dereceli node + çok sayıda düşük dereceli node) kaynaklanıyor, ek bir "hub'lar birbirine bağlanmaktan kaçınıyor" sinyali olarak yorumlanamaz. **`reports/04_05_network_construction_and_descriptive_report.md`'deki "disassortative" ifadesi bu doğrulamayla güncellenmelidir** — artık "gözlenen negatif assortativity, null model karşılaştırmasında istatistiksel anlamlılığını kaybetmiştir" şeklinde çerçevelenmelidir.

### 3.4 G3_kinship — tamamen null

Akrabalık ağının 4 metriğinin tamamı (clustering=0 zaten, transitivity=0, assortativity, modularity) rastgele ağdan ayırt edilemiyor (p≥0.45). Bu, akrabalık ilişkilerinin ağaç-benzeri/seyrek yapısıyla tutarlı — akrabalık ağında ekstra bir "topluluk" veya "kümelenme" sinyali **yok**, bu dürüstçe raporlanmıştır.

---

## 4. FAST vs FULL Mode Karşılaştırması

| | FAST (n=100) | FULL (n=1000) |
|---|---:|---:|
| Süre | 29 saniye | 4 dakika 35 saniye |
| G0_full modularity z-score | 7.076 | 7.039 |
| G0_full clustering z-score | 4.272 | 3.940 |
| En küçük olası empirical_p (add-one smoothing) | 0.0099 | 0.001 |

Yön ve anlamlılık sonuçları iki mod arasında tamamen tutarlı; FULL mode yalnızca p-value çözünürlüğünü artırıyor (0.01'den 0.001'e). **FAST mode geliştirme için güvenle kullanılabilir; bu rapordaki nihai sayılar FULL mode'dan alınmıştır.**

---

## 5. Limitations

1. **G9_directed'e yönlü-uyumlu null model uygulanmadı** — `double_edge_swap` yönsüz ağlar için tasarlandı. Yönlü bir configuration-model (in/out-degree korumalı) ayrı bir implementasyon gerektiriyor; bu Faz 7'nin bir sonraki iyileştirmesi olarak `docs/decision_log.md`'ye not edildi (henüz yapılmadı).
2. **Modularity karşılaştırması Louvain (networkx) ile yapıldı, Faz 6'nın Leiden sonucuyla değil** — tutarlılık için ensemble genelinde tek, hızlı bir algoritma kullanıldı. Louvain ve Leiden sonuçları Faz 6'da zaten yüksek uyum gösterdi (ARI=0.899), bu yüzden bulgunun Leiden için de geçerli olması beklenir ama ayrıca test edilmedi.
3. **23-bileşen artefaktı bu null-model testiyle çözülmedi** — hem gözlenen hem rastgele ağ bağlantısız olabildiği için modularity karşılaştırması geçerli, ama "gerçek" topluluk sayısının (yalnızca dev bileşen içinde) rastgeleden farkı ayrıca test edilmedi.
4. **Motif/triad enrichment bu fazda yapılmadı** — Faz 6'nın triadic census'u (G9_directed, ezici çoğunlukla "003") burada null model ile karşılaştırılmadı; ağın seyrekliği göz önüne alındığında bu, ayrı ve dikkatli bir tasarım gerektiriyor (gelecek iş, Faz 10).
5. **`double_edge_swap`, bazı çok kısıtlı (küçük/yoğun) ağlarda tüm istenen takasları tamamlayamayabilir** (`nx.NetworkXAlgorithmError` durumunda kısmi sonuçla devam edildi, kod içinde `try/except` ile ele alındı) — bu ağların hiçbirinde hata gözlenmedi (hepsi başarıyla tamamlandı), ama bu bir potansiyel sınırlama olarak belgelenmiştir.

---

## 6. Sıradaki Adım / Gelecek İyileştirmeler

- **Faz 8 (Sensitivity Analysis):** person-only vs person+group, weighted vs unweighted, vb. — bu null-model sonuçlarının network tanım kararlarına ne kadar duyarlı olduğunu test edecek.
- Gelecek iyileştirme (bu fazın kapsamı dışında, backlog'a not edildi): G9_directed için yönlü null model; dev-bileşen-only modularity null testi; motif/triad null karşılaştırması.

---

## 7. Descriptive/Exploratory vs Doğrulanmış — Güncellenmiş Tablo

| Bulgu | Faz 5-6'daki durum | Faz 7 sonrası durum |
|---|---|---|
| Community/modularity yapısı (7 ağda) | Descriptive | **Doğrulanmış** (BH-FDR, α=0.05) |
| Clustering (G0/G1/G2/G4) | Descriptive | **Doğrulanmış** (BH-FDR, α=0.05) |
| Transitivity (yalnızca G1) | Descriptive | **Doğrulanmış** (BH-FDR, α=0.05) |
| Negatif degree assortativity (tüm ağlar) | Descriptive, "disassortative" olarak sunuldu | **Doğrulanmadı** — null modelden ayırt edilemiyor, iddia geri çekildi |
| G3_kinship yapısı | Descriptive | **Null sonuç** — hiçbir metrik rastgeleden farklı değil |
| Centrality sıralamaları (Salur Kazan, Bamsı Beyrek) | Descriptive | Bu fazda test edilmedi (null model centrality karşılaştırması yapılmadı) — hâlâ Faz 8 sensitivity'i bekliyor |
