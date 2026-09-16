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
