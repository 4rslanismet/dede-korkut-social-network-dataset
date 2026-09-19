# Decision Log

Bu dosya, projede alınan geri döndürülemez veya yorumlayıcı metodolojik kararları kaydeder. Her karar `DEC-XXX` formatındadır. Yeni oturumlar bu kararları **varsayılan olarak değiştirmemeli**; değiştirmek isterlerse burada gerekçeli bir güncelleme (yeni DEC numarası, eskisine referans) eklemeli.

---

### DEC-001
**Question:** Collective/group aktörler (ör. "600 Kafir", "Tekfurun Askerleri") ana corpus network'üne dahil edilsin mi?

**Decision:** Evet, `G0_full` ve `G2_core_social` gibi ana varyantlara dahil edildi; ayrıca yalnızca `kişi` tipindeki node'ları içeren `G1_person_only` varyantı ayrı üretildi (`src/networks.py`).

**Rationale:** Kolektif aktörler repository'de gerçek, kodlanmış anlatı varlıkları (uydurulmadı); ama degree/brokerage şişirmesi riski taşıyorlar (madde 34).

**Status:** `G1_person_only` üretildi (Faz 4, tamamlandı). Sistematik person-only vs person+group **sensitivity karşılaştırması henüz yapılmadı** (Faz 8, bekliyor).

---

### DEC-002
**Question:** `dede_korkut_dugumler_temiz.csv`'de aynı `dugum_adi` ("Begil'in Adamları") için bulunan iki farklı `dugum_id` (`begilin_adamlari`, `begil_in_adamlari`) nasıl ele alınmalı?

**Decision:** Otomatik olarak birleştirildi — `begil_in_adamlari` → `begilin_adamlari`. Sayaç alanları (`toplam_gorunum`, `edge_gorunumu`, `event_gorunumu`, `boy_sayisi`) toplanarak birleştirildi. Edge/event tablolarındaki tüm referanslar yeniden yönlendirildi.

**Rationale:** Yüksek güven — aynı `dugum_adi`, aynı `dugum_tipi` (grup), tek makul açıklama iki farklı slug ile aynı entity'nin iki kez kodlanmış olması. `validation/entity_resolution_candidates.csv`'de "confidence: high" olarak işaretliydi.

**Status:** Uygulandı (Faz 3, `src/build_canonical.py::apply_entity_resolution`). **Diğer 17 düşük-güven alias çakışması BENZER ŞEKİLDE otomatik birleştirilmedi** — bunlar `validation/HUMAN_REVIEW_QUEUE.csv`'de açık kaldı.

---

### DEC-003
**Question:** `relations_aggregated.csv` üretilirken aktör çiftleri yönlü mü yönsüz mü gruplanmalı?

**Decision:** **Yönsüz** (unordered) aktör çifti üzerinden gruplama yapıldı. Yönlülük bilgisi kaybolmuyor — `any_directed`/`any_undirected` bayrakları her satırda tutuluyor.

**Rationale:** Master prompt madde 12 kesin bir kural vermiyor ("belirli kurallarla birleştirilmiş" diyor, kuralı bize bırakıyor). Yönsüz gruplama, SNA literatüründe en yaygın varsayılan aggregation biçimi ve directed-özel analizler (`G9_directed`) zaten ayrı, kendi yönlü verisiyle inşa ediliyor — aggregation kararının directed analizleri bozması engellendi.

**Status:** Uygulandı (Faz 3, `src/build_canonical.py::build_relations_aggregated`). `docs/methodology.md` yazıldığında (Faz 17) bu karar oraya da taşınmalı.

---

### DEC-004
**Question:** 17 gözlenen `iliski_turu` değeri hangi üst-seviye ailelere (SOCIAL/KINSHIP/AUTHORITY/SEMANTIC) eşlenmeli?

**Decision:** Her `iliski_turu` değeri tek bir `relation_family` + `relation_family_top`'a eşlendi (bkz. `src/build_canonical.py::RELATION_TAXONOMY` ve `data/processed/relation_taxonomy.csv`). `belirsiz` → ayrı `UNCERTAIN` üst-ailesi (SOCIAL/KINSHIP/vb. içine zorla dahil edilmedi). `tören/ritüel`, `duygusal_tepki`, `hareket/eylem` → `OTHER` (net bir aileye oturmuyorlar).

**Rationale:** Bu **yorumlayıcı bir kategorileştirme şemasıdır**, ham veriden çıkarılmış bir "gerçek" değil — her satırda `definition` alanıyla gerekçelendirildi. Master prompt madde 13'ün önerdiği taksonomiye (kinship/communication/cooperation/support/conflict/authority/identity-title/membership/uncertain) mümkün olduğunca sadık kalındı.

**Status:** Uygulandı. Yeni oturum bu eşlemeyi **değiştirmeden önce** mevcut tüm G3-G8 network tanımlarının (`src/networks.py`) buna bağımlı olduğunu unutmamalı — değişiklik network tanımlarını da etkiler.

---

### DEC-005
**Question:** `G9_directed` varyantında `yönsüz` olarak kodlanmış ilişkiler nasıl ele alınmalı?

**Decision:** **Tamamen dışlandı** — ne karşılıklı (reciprocal) edge olarak eklendi, ne de yönü keyfi atandı. `G9_directed` yalnızca `directionality == 'yönlü'` (441/628 satır) üzerinden inşa edildi.

**Rationale:** Yönsüz bir ilişkiye yapay bir yön atamak veri uydurmak anlamına gelir (madde 2 ihlali). Bu, `G9_directed`'ın neden 332 canonical node'un yalnızca 221'ini içerdiğini açıklıyor (111 node yalnızca yönsüz ilişkilerle bağlı).

**Status:** Uygulandı (Faz 4, `src/networks.py::NETWORK_DEFINITIONS["G9_directed"]`). `docs/network_models.md`'de belgelendi.

---

### DEC-006
**Question:** Signed network'te structural balance (signed triads) analizi yapılabilir mi?

**Decision:** **Hayır — "not_applicable" olarak işaretlendi.** Pozitif/negatif işaretli edge'ler arasında yalnızca 13 üçgen bulundu; kod içinde belgelenmiş bir eşik (15 üçgen) altında kaldığı için analiz zorla çalıştırılmadı.

**Rationale:** Master prompt madde 24 ve 32 açıkça "küçük veya seyrek networklerde güçlü çıkarım yapma" diyor. 13 üçgen üzerinden bir "balanced fraction" raporlamak, seyrek bir edebi network için istatistiksel olarak anlamsız ve yanıltıcı olurdu.

**Status:** Uygulandı (Faz 6, `src/signed_and_directed.py::structural_balance_check`). Eşik (15) veriden türetilmedi, kod içinde açıkça sabit ve gerekçeli olarak belirtildi — bu eşiğin kendisi de tartışmaya açık, yeni oturum değiştirebilir ama gerekçesiz değiştirmemeli.

---

### DEC-007
**Question:** Community detection için hangi network kullanılmalı (G0 mi, G2 mi)?

**Decision:** `G2_core_social` (SEMANTIC/identity ilişkileri hariç tüm ilişkiler) birincil substrat olarak seçildi.

**Rationale:** Kimlik/unvan/epitet ilişkileri (`SEMANTIC` ailesi) gerçek sosyal etkileşim değil — bunları community detection'a dahil etmek yapay olarak "aynı unvanı taşıyanlar" gibi anlamsız kümeler yaratabilirdi. `G0_full` yerine `G2_core_social` kullanmak madde 21'in "gerçek sosyal etkileşim" vurgusuyla uyumlu.

**Status:** Uygulandı (Faz 6, `src/communities.py`). **Not:** graf 23 bağlantısız bileşenden oluşuyor; bu, community sayısını (33) yapay olarak şişiriyor çünkü her izole bileşen otomatik olarak ayrı bir "community" oluyor. Bu nüans artık `reports/06_advanced_network_analysis_report.md` §1.4'te açıkça belgelendi.

---

### DEC-008
**Question:** Null model (degree-preserving randomization) için hangi yöntem kullanılmalı, hangi metrikler karşılaştırılmalı, ve hangi ağlar bu karşılaştırma için çok küçük/seyrek sayılmalı?

**Decision:**
- Randomizasyon: `networkx.double_edge_swap`, her ağın basit (ağırlıksız) kopyası üzerinde, `n_swaps = 10 × n_edges`. Bu, tam derece dizisini koruyan configuration-model eşdeğeridir.
- Karşılaştırılan metrikler: average clustering, transitivity, degree assortativity, Louvain modularity (seed=42).
- Minimum eşik: 20 edge'den az olan ağlar `not_applicable` sayılır (`MIN_EDGES_FOR_NULL_COMPARISON=20` — bu değer veriden türetilmedi, kod içinde açıkça sabit ve gerekçeli).
- Çoklu test düzeltmesi: Benjamini-Hochberg FDR (α=0.05, `config/analysis.yaml::multiple_testing`), 9 ağ × 4 metrik = 36 test üzerinde.

**Rationale:** `double_edge_swap`, networkx'te en yaygın ve iyi test edilmiş degree-preserving randomizasyon yöntemidir; `configuration_model`'in çoklu-kenar/self-loop sadeleştirme adımlarını gerektirmez. Louvain (Leiden yerine) ensemble genelinde tutarlılık ve hız için seçildi — Faz 6'da Leiden ile yüksek uyum (ARI=0.899) zaten gösterilmişti. 36 testin çoğu (24/36) tek tek p<0.05 sınırına yakın/altında çıkabilirdi; FDR düzeltmesi olmadan yanlış-pozitif riski yüksek olurdu (madde 112 kuralı).

**Status:** Uygulandı (Faz 7, `src/null_models.py`, `src/null_models_fdr.py`). **Önemli sonuç:** FDR düzeltmesi sonrası degree assortativity hiçbir ağda anlamlı çıkmadı — Faz 5'in "disassortative network" betimlemesi geri çekildi (bkz. `reports/07_null_models_report.md` §3.3, `reports/04_05_network_construction_and_descriptive_report.md`'e düzeltme notu eklendi). **Açık kalan iş:** G9_directed için yönlü-uyumlu bir null model henüz uygulanmadı; dev-bileşen-only modularity testi ve motif/triad null karşılaştırması da yapılmadı — bunlar gelecekteki iyileştirmeler olarak not edildi, mevcut Faz 7 kapsamının dışında bırakıldı.

---

### DEC-009
**Question:** Sensitivity analysis için hangi 6 karşılaştırma çifti nasıl inşa edilmeli, karşılaştırma nasıl ölçülmeli; structural robustness için hangi kaldırma stratejileri ve durdurma/örnekleme kuralları kullanılmalı?

**Decision:**
- Sensitivity: `config/analysis.yaml::sensitivity.variants`'daki 6 çift, 3'ü mevcut G0/G1/G2/G10/G11 varyantlarını yeniden kullanarak, 3'ü (explicit-only, groups-excluded-only, girizgah-excluded) yeni filtrelerle inşa edildi. Karşılaştırma ölçütü: ortak node kümesi üzerinde Spearman ρ, Kendall τ, top-10/top-20 overlap (degree, betweenness, pagerank için).
- "Groups excluded" (yalnızca `dugum_tipi=='grup'` çıkarılır) kasıtlı olarak `G1_person_only`'den (tüm `kişi`-dışı tipler çıkarılır: grup+mitolojik+hayvan+nesne+yer) **farklı** bir filtre olarak tanımlandı — madde 29'un "group nodes included/excluded" maddesi person-only'den ayrı bir soru olarak okundu.
- Robustness: `G0_full` üzerinde random (100 deneme, seed=42), degree-targeted (her adımda yeniden hesaplanan), betweenness-targeted (~20 adımda bir yeniden hesaplanan — tam "her adımda" değil, hesaplama maliyeti nedeniyle) kaldırma. Adım büyüklüğü: orijinal node sayısının %2'si.
- Ortak node sayısı 5'ten azsa sensitivity karşılaştırması `not_applicable` sayılır (kodda sabit, veriden türetilmedi).

**Rationale:** Rank-correlation tabanlı karşılaştırma, "hangi network tanımı doğru" sorusundan kaçınıp "bu karar sıralamayı ne kadar değiştiriyor" sorusuna odaklanıyor — madde 30'un istediği tam olarak bu. Betweenness'i her adımda yeniden hesaplamak (311 node için ~300 kez tam betweenness hesaplama) gereksiz maliyetli olduğundan periyodik yeniden hesaplama tercih edildi; sonuç degree-targeted'e çok yakın çıktı (%1.9 vs %3.9 eşiği), bu yaklaşımın sonucu ciddi çarpıtmadığını düşündürüyor.

**Status:** Uygulandı (Faz 8, `src/sensitivity.py`, `src/robustness.py`). **Bulgu:** Person+group vs person-only, test edilen 6 çift arasında sıralamaları en çok değiştiren karar (Spearman ρ=0.887-0.926); girizgah ve core-social filtrelemesi ihmal edilebilir etkiye sahip (ρ=1.000). Ağ, rastgele node kaybına dayanıklı (dev bileşen %50 altına düşmek için ~%25 rastgele kaldırma gerekiyor) ama hedefli saldırıya kırılgan (~%2-4 hedefli kaldırma yeterli) — klasik "robust yet fragile" örüntüsü, "structural robustness" olarak adlandırıldı, "narrative resilience" olarak değil (madde 31 kuralı).

---

### DEC-010
**Question:** G9_directed'in triadic census'u (Faz 6) için null model tabanlı motif/enrichment analizi (madde 32) yapılmalı mı?

**Decision:** **Hayır — "not_applicable" olarak işaretlendi.** Kapalı triad kategorilerinin (030T+030C+120D+120U+120C+210+300) toplamı yalnızca **44** — toplam 1.774.630 triad'ın %0.0025'i, ve bireysel kategoriler tek haneli sayılara sahip (300: 1, 030C: 2, 120D: 3, vb.). Ayrıca bu networkx sürümünde (3.6.1) yönlü ağlar için hazır bir `directed_double_edge_swap` yok; `directed_configuration_model` kullanmak self-loop/multi-edge sadeleştirmesi gerektiriyor ve tam derece korumasını bozabiliyor.

**Rationale:** Hem örneklem büyüklüğü hem de uygun bir yönlü null model altyapısının maliyeti göz önüne alındığında, bu analiz Faz 6/7'nin kendi emsaliyle (13 üçgen → not_applicable, eşik 15) tutarlı bir şekilde atlandı. Madde 32 zaten "küçük networklerde aşırı istatistiksel yorum yapma" diyor — 44 örnek üzerinden 7 farklı motif kategorisi için z-score üretmek yanıltıcı olurdu.

**Status:** Atlandı, gerekçeli. Gelecekte (backlog) uygun bir yönlü randomizasyon yöntemi (elle yazılmış directed double-edge-swap) eklenirse, yalnızca **toplam kapalı-triad sayısı** (44) tek bir null karşılaştırmasıyla test edilebilir — kategori bazlı değil.

---

### DEC-011
**Question:** Inter-annotator örneklemi nasıl seçilmeli; pipeline orkestrasyonu (`run_pipeline.py`) nasıl tasarlanmalı?

**Decision:**
- Örneklem: `(relation_family_top, extraction_method)` üzerinden stratifiye, hedef 70 satır, seed=42. Kör değerlendirme için `coder1_*` sütunlarının ikinci kodlayıcıya verilmeden önce gizlenmesi gerektiği protokolde açıkça belirtildi.
- `inter_annotator_stats.py`, `coder2_*` sütunları boşsa **kesinlikle** bir kappa/alpha değeri üretmeyip `not_applicable` döndürüyor — bu davranış test edildi.
- `run_pipeline.py`, her aşamayı ayrı bir `subprocess` olarak çalıştırıyor (import yerine) — script'lerin `if __name__=="__main__"` bloklarını ve kendi `argparse` arayüzlerini (ör. `null_models.py --fast`) bozmadan yeniden kullanmayı sağlıyor. Her aşama `logs/`'a ayrı log yazıyor, ilk hatada durup PASS/FAIL özeti veriyor.

**Rationale:** Stratifiye örnekleme, madde 37'nin "farklı story/relation type/layer/explicit-inferred" şartını karşılıyor. `not_applicable` davranışı, madde 38'in "gerçek ikinci annotator sonucu olmadan değer üretme" kuralının doğrudan uygulanması. Subprocess-tabanlı orkestrasyon, mevcut script'leri yeniden yazmadan (DRY) tek bir giriş noktası sağlıyor.

**Status:** Uygulandı (Faz 13-14). `run_pipeline.py --all` (FULL mode, `--fast` olmadan) bu oturumda uçtan uca test edilmedi — yalnızca `--stage audit`, `--stage hash_manifest`, `--all --validate-only` doğrulandı. Her aşama zaten Faz 1-12'de ayrı ayrı çalıştırılıp doğrulanmıştı. **[Güncelleme: 2026-09-19'da tam `--all` çalıştırması yapıldı ve PASS — bkz. DEC-016.]**

---

### DEC-012
**Question:** GitHub Pages sitesi (Faz 15) `outputs/`, `data/`, `reports/` gibi `docs/` dışındaki dosyalara nasıl erişmeli? Aşırı uzun `node_id` değerleri (ör. 239 karakter) dosya adı olarak kullanılabilir mi?

**Decision:**
- GitHub Pages `/docs`'tan yayın yaptığında yalnızca `docs/` içeriği sunulur — `../outputs/...` gibi yollar gerçek sitede 404 verir (yerel dosya sisteminde veya repo-root sunucusunda çalışıyor gibi görünse bile). Çözüm: `src/build_site.py::copy_assets()` kullanılan figürleri (`docs/figures/`), tüm `reports/*.md`'yi (`docs/reports/`) ve indirilebilir dosyaları (`docs/downloads/`) site build sırasında `docs/` içine kopyalıyor; hiçbir sayfa `docs/` dışına "../" ile çıkmıyor.
- `characters/<node_id>.html` dosya adları, 60 karakterden uzun `node_id`'ler için `{ilk_60_karakter}_{orijinal_uzunluk}` olarak kesiliyor (`safe_filename()`, Python ve JS'de eşleştirilmiş). Yalnızca dosya adı etkileniyor; `node_id`/`canonical_name` verisi değişmiyor.

**Rationale:** Bu hata yalnızca gerçek bir HTTP sunucusuyla (`python -m http.server`, `docs/` kökünden) test edilerek yakalandı — `file://` önizlemesi (statik snapshot) bunu göstermedi. Bu, gelecekteki oturumlar için önemli bir metodolojik ders: **site değişiklikleri her zaman `docs/`'u kök dizin olarak simüle eden gerçek bir sunucuyla test edilmeli**, doğrudan dosya açarak değil.

**Status:** Uygulandı (Faz 15-16). `src/validate_site.py` (Faz 16) bu tip hataları otomatik yakalayacak şekilde yazıldı — 363 HTML dosyasının tamamı artık 0 kırık link/eksik asset ile doğrulanıyor.

---

### DEC-013
**Question:** Website inşası sırasında keşfedilen 5 "birleştirilmiş çoklu-aktör node"u (ör. `canonical_name="Beyrek, Yigenek, Kazan, Kara Budak, Deli Dündar, Uruz"`, tek bir node_id altında) nasıl ele alınmalı?

**Decision:** Otomatik olarak **düzeltilmedi/bölünmedi**. `validation/HUMAN_REVIEW_QUEUE.csv`'ye 5 yeni madde eklendi (HR0076-HR0080, kategori `concatenated_multi_actor_node`). Bu node'lar site üzerinde oldukları gibi (birleşik isimleriyle) gösteriliyor; yalnızca dosya adları `safe_filename()` ile kısaltıldı.

**Rationale:** Bu node'ları doğru şekilde ayırmak (her karakteri ayrı node yapmak + hangi ilişkinin hangi karaktere ait olduğunu yeniden türetmek) orijinal ham metne dönüp incelemeyi gerektirir — bu bir website-inşa görevinin kapsamı dışında, dikkatli bir entity-resolution çalışması gerektirir (madde 8 kuralı: "otomatik fuzzy matching sonucu doğrudan merge yapma"). Veriyi olduğu gibi bırakıp şeffafça işaretlemek, sessizce yanlış bir bölme yapmaktan daha güvenli.

**Status:** Açık, `HUMAN_REVIEW_QUEUE.csv`'de bekliyor. Bu 5 node'un `relation_count`'u çok düşük (0-1), bu yüzden network analizlerine (Faz 5-8) etkisi ihmal edilebilir düzeyde olmalı, ama bu doğrulanmadı.

---

### DEC-014
**Question:** Proje 21 fazın tamamlanmasının ardından, tek açık kalan araştırma sorusu olan RQ6 (boy kümelemesi/story similarity) tamamlanırken: (a) hangi 5 benzerlik metriği hesaplanmalı, (b) hiyerarşik kümeleme hangi özellik uzayında yapılmalı?

**Decision:**
- 5 metrik: actor Jaccard (ikili küme örtüşmesi), actor weighted Jaccard (boy-içi etkileşim sayısı ağırlıklı), actor cosine (aynı ağırlık vektörleri üzerinden kosinüs), relation-profile similarity (17 `standard_relation` tipi üzerinden kosinüs), layer-composition similarity (7 layer üzerinden kosinüs).
- Hiyerarşik kümeleme (Ward linkage), **ham aktör kimliği üzerinden DEĞİL**, her boy'un `relation_family_top` (6 boyut) + `layer` (7 boyut) oranlarından oluşan **sabit, karşılaştırılabilir 13-boyutlu bir profil vektörü** üzerinde çalıştırıldı.

**Rationale:** Ham aktör vektörleri 332 boyutlu ve çoğu boy-çifti arasında neredeyse hiç ortak aktör olmadığından (çoğu boy'un kendine özgü karakterleri var) çok seyrek ve kümeleme için anlamlı bir metrik uzayı oluşturmuyor. Buna karşılık `relation_family_top`/`layer` oranları her boy için doğrudan karşılaştırılabilir, sabit boyutlu bir "anlatısal-ilişkisel profil" sunuyor — "hangi boylar benzer karakterleri paylaşıyor" (aktör-tabanlı ağ, F11) ile "hangi boylar benzer ilişki türü/katman kompozisyonuna sahip" (içerik-tabanlı kümeleme) sorularını kasıtlı olarak ayırıyor.

**Status:** Uygulandı (`src/story_similarity.py`). En yüksek actor Jaccard: S03–S05 (0.153), ardından S08–S10 (0.133) — bu, değerlendirilen boylar arasında *göreli olarak en çok örtüşen* çifttir; mutlak örtüşme düşüktür (medyan 0.030). `data/processed/relations_event_level.csv`'nin tamamı kullanıldı, hiçbir veri uydurulmadı — tüm 5 metrik ve kümeleme sonucu `outputs/matrices/` ve `outputs/statistics/story_similarity_clustering.json`'da makine-okunabilir olarak mevcut.

**Revizyon (DEC-015, final akademik denetim):** Bu kaydın ilk sürümü "RQ6 artık answerable: yes" ve S03–S05 için "Salur Kazan/esaret temalı" diyordu. İkisi de geri alındı: (1) "esaret teması" kanonik veri setinde kodlanmış bir değişken değildir, bu bir nitel yorumdu ve bulgu olarak yazılmamalıydı; (2) Ward dendrogramı her zaman üretilir, kümelerin varlığının kanıtı değildir ve küme geçerliliği denetlenmemişti. RQ6 durumu **PARTIALLY ANSWERED / EXPLORATORY** olarak düzeltildi. Bkz. DEC-015.

---

### DEC-015
**Question:** Yayın öncesi final akademik denetimde: RQ6 (boy benzerliği/kümeleme) için hangi durum ve hangi ifade veriyle desteklenir; FINAL_REBUILD_REPORT'taki "Top 5 findings" iddiaları kendi çıktı dosyalarıyla tutarlı mı?

**Decision:**
1. **RQ6 = PARTIALLY ANSWERED / EXPLORATORY.** İkili benzerlikler betimsel olarak hesaplandı ve görselleştirildi; ayrık küme yapısı için kanıt sınırlıdır. Kabul edilen ifade: "Story-level similarity can be quantified and visualized, but evidence for a robust discrete clustering structure is limited."
2. **Bulgu düzeltmeleri:** (a) Maks. actor Jaccard 0.153 düşük örtüşmedir (medyan 0.030; 91 çiftin 28'i hiç ortak aktör paylaşmıyor) — "güçlü benzerlik/yüksek benzer hikâyeler/net küme" ifadeleri yasak, "değerlendirilen boylar arasında göreli olarak en çok örtüşen çift" kullanılır. (b) S03–S05 yalnızca iki Jaccard ölçüsünde birinci; actor cosine/relation-profile/layer-composition'da 6./6./7. — önceki "ilişki/katman profilinde de en benzer" ifadesi yanlıştı. (c) Kosinüs değerleri (0.94–0.98) az sayıda kategori üzerindeki sayımlar için doğası gereği yüksektir; permütasyon tabanlı referansta çift-maksimumunun %95'i 0.987 (gözlenen maks. 0.985). (d) "Esaret teması" kodlanmış değişken değil (yapısal tema alanı yok; S03'ün serbest metin ilişki ifadelerinde esir/esaret/tutsak/kurtar/yağma terimlerinin hiçbiri geçmiyor, S05'te 40 satırın 2'sinde geçiyor); bulgu olarak kaldırıldı, gerektiğinde nitel yorum olarak etiketlenir (S12'nin başlığı Kazan'ın tutsaklığını ve Uruz'un kurtarışını adlandırır, S03/S05'inki değil).
3. **Küme geçerliliği** (`src/story_similarity_validity.py` → `outputs/statistics/story_similarity_cluster_validity.json`): silhouette 0.37–0.56 (k=2–6; k=2 yalnızca 1-ilişkili S01'i ayırır ve permütasyon referansının altındadır), S01 hariç bootstrap ARI k=2'de 0.746, k≥4'te ~0.54, linkage yöntemleri k=4–5'te ayrışır, Ward cophenetic r=0.73. Önceden belirlenen destek kuralı (silhouette > 0.50, bootstrap ARI ≥ 0.75, permütasyon p < 0.05) hiçbir k için (S01 dahil/hariç) sağlanmadı. Silhouette k≥3'te permütasyon referansını aşar (boylar örnekleme gürültüsünden fazla farklıdır) — bu, süreklilikle de tutarlıdır. Kümeleme sonucu bulgu olarak sunulmaz; dendrogram yaprak sırası bir görselleştirme sırasıdır.
4. **Top-5 doğrulaması** (`src/audit_top5_checks.py` → `outputs/statistics/audit_top5_checks.json`): 5/5 iddia çıktı dosyaları, doğru ağ modeli ve etki yönüyle doğrulandı; ifadeler şöyle düzeltildi: #1 dev bileşende de geçerli (z=9.9), yalnızca Louvain, "topluluk = sosyal birim" iddiası yok; #2 "geri çekildi" = desteklenmiyor (yokluğun kanıtı değil; G0_full ham p=0.032, q=0.089); #3 "tek en etkili karar, geniş farkla" **desteklenmedi** — aktör-tipi dahil etme ve ağırlıklandırma birlikte en etkili üç seçimdir (ortalama ρ 0.91–0.93; PageRank'ta weighted-vs-unweighted ρ=0.849 en düşük), fark testi yok, düğüm kümeleri farklı (n=154–311); #4 G3 bir orman (83 düğüm, 61 kenar, 22 bileşen) olduğundan clustering/transitivity yapısal olarak sıfırdır, bu "genuine null" değil düşük-bilgili null; #5 eşik özgün 311 düğüme göredir (261'lik dev bileşene değil), hedefli kaldırma çözünürlüğü 6 düğüm, betweenness her 15 kaldırmada bir yeniden hesaplanır, yalnızca G0_full.
5. **Tekrarlanabilirlik hatası düzeltildi:** `run_pipeline.py --all` story-similarity aşamasını içermiyordu ve `export_tables.py` tam T08'i eski kısmi projeksiyonla ezerdi. `story_similarity` ve `story_similarity_validity` aşamaları eklendi, `export_tables.t08_story_similarity` tam tabloyu ezmez. F10/F11 başlık/altyazıları düşük örtüşmeyi belirtir.
6. **Değişmeyen açık release blocker'lar (denetim bunların durumunu değiştirmedi):** kaynak baskı doğrulaması (dış girdi), inter-annotator reliability (ikinci kodlayıcı gerekli), çözülmemiş birleşik/entity vakaları HR0076–HR0080 vd. (orijinal metin incelemesi), `CITATION.cff` kişisel/bibliyografik metadata.

**Rationale:** Benzerliğin hesaplanmış olması RQ6'yı otomatik olarak "answered" yapmaz; ayrık küme yapısı doğrulanamadığı için RQ6 kısmen cevaplanmış, keşfsel olarak işaretlendi. Hiçbir sonuç "iyileştirilmedi": destek kuralı ilk çalıştırmadan önce betiğe yazıldı ve olumsuz sonuç olduğu gibi raporlandı. Dürüstlük notu: S01 (tek ilişkili girizgah) hariç duyarlılık analizi, ilk çalıştırmada k=2 ayrımının yalnızca S01'i ayırdığı görüldükten *sonra* eklendi; aynı sabit kural uygulandı ve o analiz de desteği sağlamadı (silhouette 0.487 < 0.50, ARI 0.746 < 0.75).

**Status:** Uygulandı. Paper, thesis, website, README ve raporlar tutarlı hâle getirildi.

---

### DEC-016
**Question:** Release öncesi son teknik doğrulama: tam `python run_pipeline.py --all` (FULL mode) uçtan uca çalıştığında bilimsel çıktılar aynen yeniden üretiliyor mu, ve pipeline idempotent mi?

**Mode:** FULL — `--fast` yok; `config/analysis.yaml` `null_models.n_random: 1000`, `robustness.n_random_trials: 100`, `seed: 42` (raporlanan sayıların kaynağı; ayrı bir `--full` bayrağı yok).

**Bulgu:** 1. koşu (commit `2e08975`): 23/23 aşama PASS, ~7 dk; bilimsel çıktılar birebir aynı. Ancak koşu, elle eklenmiş iki içeriği **sildi** (pipeline idempotent değildi): (a) `validation/HUMAN_REVIEW_QUEUE.csv`'den HR0076–HR0080 (Faz 15'te elle eklenen 5 birleşik-aktör düğümü, DEC-013) — `entity_resolution.py` kuyruğu yalnızca otomatik kontrollerden yeniden üretiyordu; (b) `docs/network_models.md`'nin story-level/bipartite bölümleri — `build_networks.py` dosyayı sıfırdan yazıyordu.

**Decision (düzeltme):** (a) İnsan tarafından bulunan maddeler `validation/manual_review_items.csv` dosyasında tutuluyor ve `entity_resolution.py` bunları otomatik satırların ardına ID'leri devam ettirerek ekliyor; (b) `story_networks.py` aşaması bu bölümleri idempotent olarak (sayılar veriden hesaplanarak) yeniden yazıyor; (c) bipartite `.graphml` kenarları sıralı yazılıyor (set iterasyon sırası koşular arasında değişiyordu; içerik aynıydı). Bilimsel kod değişmedi. Her iki dosya HEAD ile birebir aynı yeniden üretiliyor ve tekrar koşuda da değişmiyor.

**Sonuç (2. koşu, düzeltilmiş kod):** 23/23 aşama PASS, ~7 dk 18 sn. `outputs/statistics/`, `matrices/`, `null_models/`, `data/processed/`, tüm yayın tabloları (T08 tam 91 çift dahil), tüm PNG figürler ve paper/thesis/site sayfaları (RQ6 = PARTIALLY ANSWERED / EXPLORATORY) commit'lenmiş sürümle **birebir aynı**. Beklenen, bilimsel olmayan farklar: `.gexf` `lastmodifieddate`; `.svg` `dc:date` + rastgele element id'leri; `centrality_*.csv`/T04'te ≤1.1e-13 kayan nokta gürültüsü (tanımlayıcılar ve satır sırası aynı). Yalnızca `.gexf` tarih satırları commit'lendi; SVG/centrality gürültüsü commit'lenmedi (içerik değişikliği yok).

**Kapsam notları:** `build_site.py`, `validate_site.py`, `pytest` ve `validate_release_consistency.py` `run_pipeline.py` `STAGES` içinde değil; pipeline'dan sonra ayrıca çalıştırıldı (hepsi PASS). Bunları `STAGES`'e eklemek öneri olarak bırakıldı (pipeline sözleşmesini değiştirir). Windows `core.autocrlf=true` altında LF ile yazılan dosyaların (ör. `.gexf`) manifest hash'leri, taze bir CRLF checkout'unda değil, yalnızca pipeline'ın yazdığı hâliyle eşleşir.

**Status:** Uygulandı; açık release blocker'lar (kaynak baskı doğrulaması, inter-annotator reliability, birleşik/entity vakaları, `CITATION.cff` metadata) değişmedi.
