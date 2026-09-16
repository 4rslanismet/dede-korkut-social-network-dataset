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

**Status:** Uygulandı (Faz 13-14). `run_pipeline.py --all` (FULL mode, `--fast` olmadan) bu oturumda uçtan uca test edilmedi — yalnızca `--stage audit`, `--stage hash_manifest`, `--all --validate-only` doğrulandı. Her aşama zaten Faz 1-12'de ayrı ayrı çalıştırılıp doğrulanmıştı.

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
