# DEDE KORKUT DIGITAL HUMANITIES & NETWORK SCIENCE PROJECT
## COMPLETE END-TO-END REBUILD MASTER INSTRUCTION

Bu görevde yalnızca kod öneren veya analiz tavsiyesi veren bir yardımcı değilsin.

Google Colab ortamına bağlı, repository üzerinde çalışan bir:

- araştırma mühendisi,
- veri mühendisi,
- network scientist,
- digital humanities araştırmacısı,
- veri kalite denetçisi,
- reproducibility engineer,
- bilimsel görselleştirme geliştiricisi,
- web geliştiricisi,
- akademik araştırma destek sistemi

gibi hareket edeceksin.

Bütün işlemleri mümkün olduğu ölçüde doğrudan Colab üzerinde gerçekleştir.

Bana "şu kodu çalıştır" deme.

Kodu sen yaz, çalıştır, hatasını kontrol et, düzelt, tekrar çalıştır, çıktılarını doğrula ve dosyaları oluştur.

---

# 0. PROJE

GitHub repository:

https://github.com/4rslanismet/dede-korkut-social-network-dataset.git

Repository'yi Colab ortamına klonla.

Tercihen çalışma branch'i:

`claude-dk-rebuild`

olsun.

Ana branch üzerinde doğrudan değişiklik yapma.

GitHub authentication veya push izni hazır değilse push yapmaya çalışma.

Bütün sistemi önce Colab filesystem üzerinde tamamla.

---

# 1. ANA HEDEF

Dede Korkut anlatılarındaki karakterler, kolektif aktörler, sosyal ilişkiler ve anlatılar arası bağlantılardan hareketle akademik olarak savunulabilir, tekrar üretilebilir ve genişletilebilir bir:

**Digital Humanities + Social Network Analysis + Complex Networks + Multilayer Network Analysis**

araştırma altyapısı oluştur.

Bu çalışma yalnızca:

"Karakterlerin degree centrality değerlerini hesapladık."

seviyesinde kalmayacaktır.

Hedef:

- yüksek kaliteli araştırma veri seti,
- açık veri modeli,
- çok katmanlı network modeli,
- story-level analiz,
- corpus-level analiz,
- multilayer analiz,
- signed network analizi,
- directed network analizi,
- bipartite network analizi,
- narrative-order analizi,
- community analysis,
- null-model analizi,
- robustness analizi,
- sensitivity analysis,
- akademik görseller,
- publication-ready tablolar,
- interaktif web portalı,
- reproducible pipeline,
- validation sistemi,
- tez/makale çıktıları

oluşturmaktır.

---

# 2. EN ÖNEMLİ BİLİMSEL KURAL

Hiçbir veri uydurulmayacaktır.

Repository veya kullanılan güvenilir kaynak tarafından açık biçimde desteklenmeyen:

- ilişki,
- karakter özelliği,
- cinsiyet,
- aile bağı,
- toplumsal statü,
- soy,
- kabile,
- siyasi konum,
- anlatısal rol,
- faction,
- düşmanlık,
- dostluk,
- kahramanlık derecesi,
- psikolojik özellik,
- kronoloji

LLM tarafından tahmin edilerek veri setine eklenmeyecektir.

LLM inference ile oluşturulan herhangi bir veri:

**verified ground truth**

olarak kullanılamaz.

Gerekirse:

`needs_manual_validation = 1`

olarak ayrı tutulmalıdır.

---

# 3. VERİ KÖKENİ / PROVENANCE

Her veri kaydının mümkün olduğunca kaynağı izlenebilir olmalıdır.

Şunları koru:

- source_file
- source_row
- original/raw expression
- standardized expression
- transformation
- rationale
- extraction method
- validation status
- annotator
- version

Ham veri kesinlikle korunmalıdır.

`data/raw/`

immutable kabul edilecektir.

Mevcut temiz veri:

`data/final/`

başlangıç referansıdır.

Yeni veri doğrulanmadan mevcut final dataset üzerine yazma.

---

# 4. MEVCUT REPOSITORY'NİN TAM DENETİMİ

Önce bütün repository ağacını çıkar.

Şunları incele:

- README
- LICENSE
- data/raw
- data/story_level
- data/final
- docs
- bütün CSV dosyaları
- bütün XLSX dosyaları
- alias sözlükleri
- change logs
- boy indeksleri

Dosya başına:

- dosya adı
- boyut
- kolonlar
- satır sayısı
- null değer sayısı
- duplicate sayısı
- veri tipleri
- encoding
- potansiyel kalite sorunları

raporla.

Oluştur:

`reports/01_repository_audit.md`

---

# 5. MEVCUT SAYILARIN DOĞRULANMASI

Repository README veya belgelerinde geçen tüm temel istatistikleri yeniden hesapla.

Örneğin:

- boy/bölüm sayısı
- node sayısı
- edge sayısı
- event sayısı
- alias sayısı
- kişi sayısı
- grup sayısı
- ilişki türü sayısı
- layer sayısı

Mevcut README değerlerini kör biçimde kabul etme.

Programatik olarak yeniden üret.

Tutarsızlık varsa raporla.

---

# 6. RAW EXCEL DENETİMİ

Raw Excel dosyasını eksiksiz incele.

Her sheet için:

- sheet adı
- boyut
- kolonlar
- null değerler
- duplicate kayıtlar
- sıra yapısı
- karakter kodlamaları
- ilişki kodlamaları
- ham açıklamalar

çıkar.

Raw → story_level → final dönüşümünün ne kadar takip edilebilir olduğunu değerlendir.

---

# 7. VERİ KALİTE TESTLERİ

Programatik validation framework oluştur.

Kontrol et:

## Node sorunları

- duplicate node ID
- duplicate canonical entity
- aynı ID farklı isim
- aynı isim farklı ID
- kişi/grup çakışması
- boş node
- geçersiz ID
- Türkçe karakter sorunu
- capitalization problemi
- whitespace problemi
- alias collision

## Edge sorunları

- missing source
- missing target
- orphan endpoint
- invalid relation
- invalid layer
- invalid polarity
- invalid weight
- invalid directionality
- unexpected self-loop
- duplicate relationship
- inconsistent reciprocal relationship
- source_file mismatch
- narrative row mismatch

## Event sorunları

- ilişki olması gerekirken event kalması
- event olması gerekirken edge olması
- missing actor
- unsupported target
- duplicate event

Validation çıktıları:

`outputs/validation/`

altında saklansın.

Ayrıca:

`reports/02_data_quality_report.md`

üret.

---

# 8. ENTITY RESOLUTION

Canonical entity sistemi yeniden değerlendir.

Özellikle:

- yazım varyantları
- unvanlar
- lakaplar
- kişi/grup ayrımı
- bağlamsal isimler
- aynı karakterin farklı adlandırmaları

kontrol edilsin.

Ancak otomatik fuzzy matching sonucu doğrudan merge yapma.

Her önerilen merge için:

- entity A
- entity B
- similarity score
- evidence
- proposed action
- confidence
- manual review required

alanları olan tablo üret.

Örneğin:

`validation/entity_resolution_candidates.csv`

---

# 9. YENİ CANONICAL VERİ MODELİ

Yeni sistem mümkünse şu yapıya sahip olsun:

```text
data/
├── raw/
├── story_level/
├── legacy/
├── processed/
│   ├── nodes.csv
│   ├── aliases.csv
│   ├── stories.csv
│   ├── relations_event_level.csv
│   ├── relations_aggregated.csv
│   ├── narrative_events.csv
│   ├── relation_taxonomy.csv
│   ├── provenance.csv
│   └── validation_status.csv
└── derived/
    ├── networks/
    ├── matrices/
    ├── similarity/
    └── temporal/
```

---

# 10. NODE SCHEMA

Mümkünse:

```text
node_id
canonical_name
node_type
aliases
first_story
story_count
relation_count
event_count
validation_status
source
notes
```

Metadata kanıtla destekleniyorsa ayrıca:

```text
gender
faction
lineage
social_status
narrative_role
```

eklenebilir.

Ama desteklenmiyorsa boş bırak.

Tahmin etme.

---

# 11. EDGE SCHEMA

Event-level relation tablosunda mümkün olduğunca:

```text
relation_id
story_id
story_name
section_type
narrative_order
source_id
source_name
source_type
target_id
target_name
target_type
raw_relation
standard_relation
relation_family
layer
weight
polarity
directionality
extraction_method
confidence
source_file
source_row
raw_evidence
validation_status
notes
```

tut.

---

# 12. EVENT-LEVEL VE AGGREGATED NETWORK AYRIMI

Bu ayrım kesinlikle korunmalıdır.

## Event-level

Anlatıda gerçekleşen her ayrı interaction.

## Aggregated

Aynı aktör çifti arasındaki ilişkilerin belirli kurallarla birleştirilmiş hali.

Aggregation sonucu ham tekrar bilgisi kaybolmamalıdır.

Örneğin:

```text
interaction_count
total_weight
positive_count
negative_count
stories_shared
relation_types
```

korunmalıdır.

---

# 13. RELATION TAXONOMY

Mevcut ilişki türlerini yeniden denetle.

Taxonomy oluştur:

- kinship
- communication
- cooperation
- support
- conflict
- authority
- loyalty
- protection
- captivity
- marriage
- identity/title
- group membership
- opposition
- other
- uncertain

Ancak sadece mevcut datanın izin verdiği ölçüde.

Daha üst düzey family yapısı oluştur:

## SOCIAL

- communication
- cooperation
- support
- conflict

## KINSHIP

- parent-child
- sibling
- spouse
- lineage

## AUTHORITY

- command
- hierarchy

## SEMANTIC

- identity
- title
- membership

Bunların hepsini:

`data/processed/relation_taxonomy.csv`

içinde açık mapping olarak tut.

---

# 14. ANALİZ AĞLARI

Tek network üzerinden bütün sonuçları hesaplama.

En az aşağıdaki network modellerini üret.

## G0 — FULL NETWORK

Tüm node ve ilişkiler.

## G1 — PERSON ONLY

Yalnızca kişi aktörleri.

## G2 — CORE SOCIAL NETWORK

Semantic/identity ilişkileri hariç gerçek sosyal etkileşimler.

## G3 — KINSHIP NETWORK

## G4 — COMMUNICATION NETWORK

## G5 — COOPERATION/SUPPORT NETWORK

## G6 — CONFLICT NETWORK

## G7 — POSITIVE NETWORK

## G8 — NEGATIVE NETWORK

## G9 — DIRECTED NETWORK

## G10 — WEIGHTED NETWORK

## G11 — UNWEIGHTED NETWORK

Her network tanımını:

`docs/network_models.md`

içinde açıkça yaz.

---

# 15. STORY-LEVEL NETWORKS

Her boy için ayrı network oluştur.

Her story için:

- nodes
- edges
- density
- average degree
- clustering
- components
- centralization
- reciprocity
- assortativity
- modularity

uygun olduğu ölçüde hesapla.

Story'leri karşılaştır.

Girizgâh bir "boy" değilse bunu story type üzerinden ayrı değerlendir.

---

# 16. ACTOR × STORY BIPARTITE NETWORK

Actor-story incidence matrix üret.

Bipartite graph oluştur.

Buradan iki projection üret:

## Actor projection

Aynı anlatılarda birlikte görünen aktörler.

## Story projection

Ortak karakterlere göre birbirine benzeyen anlatılar.

Projection sırasında degree inflation riskini açıkça raporla.

---

# 17. STORY SIMILARITY

Story similarity için en az:

### Actor Jaccard

### Weighted Jaccard

### Cosine similarity

### Relation profile similarity

### Layer composition similarity

hesapla.

Çıktılar:

- similarity matrix
- heatmap
- story network
- hierarchical clustering dendrogram

olsun.

---

# 18. CORPUS LEVEL NETWORK METRICS

Uygun ağlarda:

- node count
- edge count
- density
- connected components
- giant component
- isolates
- average degree
- weighted degree / strength
- in-degree
- out-degree
- reciprocity
- clustering coefficient
- transitivity
- assortativity
- average shortest path
- diameter
- eccentricity
- k-core
- coreness

hesapla.

Her metrik her ağda zorla hesaplanmayacak.

---

# 19. CENTRALITY

Uygun ağlarda:

- degree centrality
- weighted degree / strength
- in-degree centrality
- out-degree centrality
- betweenness centrality
- closeness centrality
- harmonic centrality
- eigenvector centrality
- PageRank

hesapla.

Disconnected networklerde closeness kullanımına dikkat et.

Gerekirse harmonic centrality tercih et.

---

# 20. CHARACTER IMPORTANCE

"En önemli karakter" gibi tek metrikli sonuç verme.

Çok boyutlu karakter profili oluştur.

Örneğin:

```text
degree
strength
betweenness
pagerank
story_count
layer_count
community_bridge_score
coreness
```

gibi ölçülerle karakter profili üret.

Composite skor üretilecekse:

- zorunlu değil,
- exploratory olarak kalmalı,
- ağırlıkları açıkça açıklanmalı.

---

# 21. COMMUNITY DETECTION

En az:

- Leiden
- Louvain

uygula.

Birden fazla random seed çalıştır.

Resolution sensitivity incele.

Community stability hesaplamaya çalış.

Çıktılar:

- modularity
- community count
- membership
- community size
- inter-community edges

---

# 22. COMMUNITY BRIDGES

Her node için mümkün olduğunca:

- within-module degree
- participation coefficient
- inter-community edge count

hesapla.

Broker karakterleri belirle.

Bunların:

- sadece yüksek degree,
- gerçek cross-community bridge

olup olmadığını ayır.

---

# 23. MULTILAYER / MULTIPLEX NETWORK

Relation layer'ları üzerinden multiplex network modeli oluştur.

Her node için:

- number of active layers
- degree per layer
- strength per layer
- layer participation coefficient
- cross-layer diversity
- versatility

hesaplamayı değerlendir.

Bir karakterin farklı layer'lardaki rollerini karşılaştır.

Örneğin:

```text
kinship central
conflict peripheral
communication bridge
```

gibi sonuçları ancak metrikler destekliyorsa raporla.

---

# 24. SIGNED NETWORK

Positive / negative / neutral ilişkiler güvenilir ise signed network analizi yap.

Hesapla:

- positive degree
- negative degree
- positive strength
- negative strength
- positive-negative ratio

Uygunsa:

- signed triads
- structural balance

analiz et.

Küçük veya seyrek networklerde güçlü çıkarım yapma.

---

# 25. DIRECTED NETWORK

Directionality güvenilir olan ilişkiler için:

- in-degree
- out-degree
- reciprocity
- PageRank
- HITS, uygunsa
- triad census

hesapla.

---

# 26. NARRATIVE ORDER NETWORK EVOLUTION

`satir_no` veya benzeri alan güvenilir anlatı sırası içeriyorsa:

Bunu:

**narrative order**

olarak adlandır.

Gerçek kronolojik zaman olarak adlandırma.

Story başına anlatıyı örneğin:

- early
- middle
- late

veya quantile window'lara böl.

Her pencere için:

- active nodes
- cumulative edges
- new nodes
- centrality
- conflict intensity
- support intensity

gibi metrikleri çıkar.

---

# 27. DYNAMIC CENTRALITY

Story boyunca merkezi aktörlerin nasıl değiştiğini exploratory olarak göster.

Örneğin:

`centrality trajectory`

grafikleri oluştur.

---

# 28. NULL MODELS

Bu proje için önemli bir bilimsel doğrulama katmanı oluştur.

Uygun networklerde degree-preserving randomization veya configuration model kullan.

En az uygun metrikler için:

- clustering
- transitivity
- assortativity
- modularity
- motifs / triads

gerçek network ile random ensemble'ı karşılaştır.

En azından mümkün olan durumlarda:

```text
observed
random_mean
random_std
z_score
percentile
empirical_p
```

raporla.

Random seed kaydedilsin.

---

# 29. SENSITIVITY ANALYSIS

Ana bulguları aşağıdaki model değişikliklerinde tekrar hesapla:

### Person + group
vs
### Person only

---

### Weighted
vs
### Unweighted

---

### All relations
vs
### Core social

---

### Explicit relations
vs
### Explicit + inferred

---

### Group nodes included
vs
### excluded

---

### Girizgâh included
vs
### excluded

uygun olduğu sürece.

---

# 30. CENTRALITY ROBUSTNESS

Her alternatif model arasında centrality ranking'lerini karşılaştır.

Özellikle:

- Spearman correlation
- Kendall tau
- top-k overlap

hesapla.

Amaç:

Ana karakter sonuçlarının network modelleme kararlarına ne kadar bağımlı olduğunu bulmak.

---

# 31. STRUCTURAL ROBUSTNESS

Exploratory olarak:

- random node removal
- high-degree removal
- high-betweenness removal

senaryoları oluştur.

Her adımda:

- largest component
- number of components
- connectivity
- average path length uygunsa

ölç.

Bunu:

**structural robustness**

olarak adlandır.

"Narrative resilience" gibi aşırı yoruma gitme.

---

# 32. MOTIF / TRIAD ANALYSIS

Network yeterince büyükse:

- triad census
- selected motifs

incele.

Null networklerle motif enrichment karşılaştır.

Küçük networklerde aşırı istatistiksel yorum yapma.

---

# 33. ASSORTATIVITY VE HOMOPHILY

Sadece metadata kanıtlanmışsa attribute assortativity değerlendir.

Örneğin:

- faction
- gender
- actor type

Ancak metadata yoksa LLM tahminiyle homophily analizi yapma.

---

# 34. CHARACTER TYPE BIAS

Kişi ve kolektif node'ların aynı networkte bulunmasının merkeziyet sonuçlarını nasıl etkilediğini ölç.

Person-only sensitivity bunun ana parçasıdır.

Group node'ların:

- degree inflation
- brokerage inflation
- community distortion

yaratıp yaratmadığını test et.

---

# 35. EXTRACTION METHOD BIAS

`cikarma_yontemi` alanını kullan.

Örneğin:

- explicit
- inferred
- inferred kinship
- standardized

gibi kategorilerin network sonuçlarına etkisini incele.

Explicit-only network ile tüm networkü karşılaştır.

Bu analiz önemlidir.

---

# 36. EDGE WEIGHT SENSITIVITY

Mevcut ağırlıkların anlamını araştır.

Ağırlıklar kodlama kategorisi ise bunu tekrar sayısı gibi yorumlama.

Ağırlıkların semantiğini dokümante et.

Alternative edge-weight schemes gerekiyorsa exploratory karşılaştırma yap.

---

# 37. INTER-ANNOTATOR VALIDATION

Şu anda tek araştırmacı kodlaması varsa reliability değeri uydurma.

Bunun yerine ikinci insan kodlayıcı için örnek veri oluştur.

`validation/inter_annotator_sample.csv`

Stratified sample yap:

- farklı story'ler
- farklı relation types
- farklı layers
- explicit/inferred kayıtlar

Doldurulacak kolonlar:

```text
relation_id
actor_1
actor_2
raw_evidence
coder1_relation
coder2_relation
coder1_layer
coder2_layer
coder1_polarity
coder2_polarity
agreement
notes
```

Ayrıca:

`docs/inter_annotator_protocol.md`

oluştur.

---

# 38. COHEN KAPPA / KRIPPENDORFF ALPHA

İkinci annotation verisi gelirse:

- Cohen's kappa
- Krippendorff's alpha

hesaplanabilecek script hazırla.

Ama gerçek ikinci annotator sonucu olmadan değer üretme.

---

# 39. METADATA EXTENSION TEMPLATE

Gelecekte manuel doğrulama ile eklenebilecek:

- gender
- lineage
- clan
- role
- social status
- human/supernatural
- protagonist/antagonist

gibi özellikler için:

`validation/manual_actor_metadata_template.csv`

oluştur.

Ama bunları şimdiki analizde tahmini olarak kullanma.

---

# 40. İLERİ NETWORK ANALİZLERİ

Ana analizler tamamlandıktan sonra exploratory appendix olarak değerlendir:

- Node2Vec
- network embeddings
- role similarity
- structural equivalence
- cosine similarity of network signatures
- unsupervised actor clustering

Bunları ana bilimsel katkının yerine koyma.

---

# 41. NETWORK EMBEDDING

Node2Vec yaparsan:

- seed
- dimensions
- walk length
- walks per node
- p
- q

raporla.

UMAP/t-SNE görselleştirmesi yapabilirsin.

Ama kümeleri otomatik olarak sosyolojik gerçeklik gibi yorumlama.

---

# 42. STORY EMBEDDING

Story network feature vector'ları üzerinden:

- PCA
- hierarchical clustering

uygulanabilir.

Her story için feature vector:

```text
size
density
clustering
modularity
conflict ratio
kinship ratio
support ratio
centralization
```

gibi mevcut ölçülerden üretilebilir.

---

# 43. RESEARCH QUESTIONS

Veriyi denetledikten sonra aşağıdaki soruları değerlendir ve gerekiyorsa rafine et.

## RQ1

Dede Korkut anlatılarındaki aktör ağı yapısal olarak nasıl örgütlenmektedir?

## RQ2

Hangi aktörler anlatılar ve ilişki katmanları arasında köprü rolü üstlenmektedir?

## RQ3

Akrabalık, iletişim, işbirliği ve çatışma ağları karakterlere farklı yapısal roller atamakta mıdır?

## RQ4

Corpus ağı benzer degree yapısına sahip null ağlardan anlamlı biçimde ayrılmakta mıdır?

## RQ5

Ana network bulguları farklı network construction tercihlerine karşı ne kadar kararlıdır?

## RQ6

Dede Korkut boyları karakter kompozisyonu ve ilişki profilleri açısından hangi kümelenmeleri göstermektedir?

## RQ7

Anlatı boyunca karakter merkeziliği ve ilişki yoğunluğu nasıl değişmektedir?

Eğer veri bir soruyu cevaplamaya yetmiyorsa bunu çıkar.

---

# 44. HYPOTHESIS TESTING

Sadece veri izin verirse hipotez oluştur.

Post-hoc sonucu hipotezmiş gibi sunma.

Exploratory ve confirmatory analizleri açıkça ayır.

---

# 45. OUTPUT DIRECTORY

Tüm sonuçlar düzenli şekilde:

```text
outputs/
├── figures/
│   ├── corpus/
│   ├── stories/
│   ├── layers/
│   ├── communities/
│   ├── similarity/
│   ├── sensitivity/
│   ├── null_models/
│   ├── robustness/
│   └── narrative_order/
├── tables/
├── networks/
├── matrices/
├── statistics/
├── validation/
└── web/
```

altında olsun.

---

# 46. PUBLICATION-QUALITY FIGURES

Her görsel:

- okunabilir
- bilimsel
- açıklamalı
- uygun font büyüklüğüne sahip
- yüksek çözünürlüklü

olsun.

Mümkünse:

- PNG
- SVG
- PDF

üret.

---

# 47. NETWORK VISUALIZATION PRINCIPLES

Hairball üretme.

Büyük networklerde:

- weighted edge opacity
- degree/centrality-based size
- community layout
- selective labels

kullan.

Her aktörün label'ını göstermeye çalışma.

---

# 48. ANA FIGÜRLER

En az aşağıdaki figürleri üretmeye çalış:

### F01
Dataset construction workflow

### F02
Corpus full network

### F03
Person-only network

### F04
Core social network

### F05
Multilayer overview

### F06
Community structure

### F07
Top actors centrality comparison

### F08
Story-level network metric comparison

### F09
Actor × story bipartite

### F10
Story similarity heatmap

### F11
Story similarity network

### F12
Layer participation

### F13
Positive/negative network comparison

### F14
Narrative-order evolution

### F15
Null-model comparison

### F16
Sensitivity correlation matrix

### F17
Centrality rank stability

### F18
Structural robustness curves

---

# 49. TABLOLAR

Publication-ready tablolar üret.

Örneğin:

### T01
Dataset overview

### T02
Relation taxonomy

### T03
Story-level statistics

### T04
Centrality results

### T05
Community statistics

### T06
Layer-specific metrics

### T07
Actor-story participation

### T08
Story similarity

### T09
Null model tests

### T10
Sensitivity analysis

### T11
Robustness results

Hem CSV hem mümkünse LaTeX formatında oluştur.

---

# 50. İNTERAKTİF WEB PORTALI

Projenin sonuçlarını görüntülemek için tam bir GitHub Pages web sitesi oluştur.

Site:

`docs/`

dizininden yayınlanabilecek şekilde tasarlansın.

Hedef URL yapısı:

`https://4rslanismet.github.io/dede-korkut-social-network-dataset/`

olabilecek şekilde hazırlanmalıdır.

---

# 51. WEB SİTESİ ANA SAYFASI

Modern, sade ve akademik görünümlü landing page oluştur.

Ana sayfada:

## Project title

**Dede Korkut Narrative Networks**

Alt açıklama:

**A reproducible multilayer network analysis of characters and relations in the Book of Dede Korkut**

uygun olabilir.

Ana metrik kartları:

- stories
- actors
- relations
- narrative events
- relation layers

Gerçek veriden otomatik gelsin.

Hardcoded sayı kullanma.

---

# 52. WEBSITE NAVIGATION

Navbar en az:

```text
Home
Dataset
Methodology
Network Explorer
Stories
Characters
Layers
Communities
Similarity
Analysis
Evidence
Downloads
Reproduce
About
```

içersin.

---

# 53. DATASET PAGE

Dataset sayfasında:

- dataset description
- schema
- counts
- node types
- relation types
- layers
- version
- provenance
- download links

olsun.

---

# 54. METHODOLOGY PAGE

Şunları açıkla:

- raw data
- coding
- entity normalization
- alias resolution
- relation taxonomy
- graph construction
- network variants
- statistical methods
- sensitivity analysis
- validation

---

# 55. INTERACTIVE NETWORK EXPLORER

Cytoscape.js tercih edilebilir.

Interactive graph özellikleri:

- zoom
- pan
- search
- node selection
- edge selection
- tooltip
- filter

---

# 56. NETWORK FILTERS

Explorer'da filtreler:

- story
- actor type
- relation layer
- relation type
- polarity
- directionality
- community

olsun.

---

# 57. NODE DETAIL PANEL

Node tıklanınca:

- name
- type
- story count
- degree
- strength
- betweenness
- PageRank
- community
- layers
- connected actors

göster.

Sadece gerçekten hesaplanmış metrikleri göster.

---

# 58. EDGE DETAIL PANEL

Edge seçilince:

- source
- target
- relation
- layer
- story
- weight
- polarity
- directionality
- extraction method

göster.

Raw evidence paylaşımı telif açısından uygunsa göster; değilse yalnızca kısa provenance bilgisi göster.

---

# 59. STORY PAGES

Her boy için ayrı detay sayfası oluştur.

Örneğin:

`stories/bogac-han.html`

Sayfada:

- story title
- node count
- edge count
- network metrics
- top actors
- relation distribution
- interactive story network
- related stories

olsun.

---

# 60. CHARACTER PAGES

Önemli/canonical aktörler için otomatik sayfalar oluştur.

Örneğin:

`characters/salur-kazan.html`

İçerik:

- canonical name
- aliases
- stories
- centrality profile
- layer profile
- community
- strongest relations
- story participation

---

# 61. LAYER PAGES

Her relation layer için:

- description
- statistics
- top actors
- network
- layer comparison

göster.

---

# 62. COMMUNITY PAGE

Community analysis sayfasında:

- number of communities
- modularity
- community sizes
- representative nodes
- interactive community network

göster.

Community'lere keyfi kültürel isimler verme.

Varsayılan:

Community 1
Community 2

gibi nötr isim kullan.

---

# 63. STORY SIMILARITY PAGE

Interactive:

- heatmap
- similarity network
- clustering

sun.

Similarity metriği seçilebilsin.

---

# 64. ANALYSIS PAGE

Akademik analizlerin sonuçlarını göster:

- centrality
- communities
- multilayer
- signed network
- narrative order
- robustness
- null models
- sensitivity

Her bölüm ilgili figür ve tabloyla desteklensin.

---

# 65. EVIDENCE PAGE

Bilimsel şeffaflık için:

- data lineage
- change logs
- validation tests
- hash manifest
- source mapping
- reproduction status

göster.

---

# 66. DOWNLOADS PAGE

İndirilebilir:

- nodes.csv
- event-level relations
- aggregated relations
- events
- aliases
- story metrics
- actor metrics
- GraphML
- GEXF
- JSON
- Cytoscape JSON

sağla.

---

# 67. REPRODUCE PAGE

Tekrar üretim talimatlarını açıkça göster.

Örneğin:

```bash
git clone ...
pip install -r requirements.txt
python run_pipeline.py
```

Ayrıca Google Colab notebook linki için placeholder bırak.

---

# 68. WEB DATA PIPELINE

Site içindeki sayılar ve tablolar mümkün olduğunca analiz çıktılarından otomatik üretilsin.

Hardcoded sonuçları minimuma indir.

Python build script ile:

CSV/JSON → website data

dönüşümü yap.

---

# 69. WEB RESPONSIVENESS

Site:

- desktop
- tablet
- mobile

üzerinde düzgün çalışsın.

---

# 70. WEBSITE ACCESSIBILITY

Uygun:

- semantic HTML
- alt text
- contrast
- keyboard navigation

uygula.

---

# 71. WEBSITE DİLİ

Varsayılan akademik İngilizce olabilir.

Mümkünse TR / EN altyapısı tasarla.

Ama iki dil birbirine karışmasın.

İki dil yapılacaksa aynı içeriğin tutarlı çevirisini sağla.

---

# 72. WEB VISUAL STYLE

Tema:

- sade
- modern
- akademik
- veri odaklı
- gereksiz animasyondan uzak

olsun.

Dede Korkut bağlamını çağrıştıran hafif estetik öğeler kullanılabilir ama siteyi folklor temalı oyun arayüzüne çevirme.

---

# 73. REPRODUCIBLE ANALYSIS PIPELINE

Repository içinde:

```text
src/
├── ingest.py
├── normalize.py
├── validate.py
├── build_networks.py
├── metrics.py
├── communities.py
├── multilayer.py
├── similarity.py
├── null_models.py
├── sensitivity.py
├── robustness.py
├── visualization.py
├── export.py
└── build_site_data.py
```

benzeri modüler yapı oluştur.

---

# 74. NOTEBOOKS

En az:

```text
notebooks/
01_data_audit.ipynb
02_data_cleaning.ipynb
03_network_construction.ipynb
04_corpus_analysis.ipynb
05_story_analysis.ipynb
06_multilayer_analysis.ipynb
07_story_similarity.ipynb
08_null_models.ipynb
09_sensitivity_analysis.ipynb
10_figures_and_tables.ipynb
```

oluştur.

Notebooklar ana kaynak değil, pipeline gösterimi olsun.

Asıl logic `src/` içinde olsun.

---

# 75. MASTER PIPELINE

Root'ta:

`run_pipeline.py`

oluştur.

Bu script:

1. validate environment
2. load data
3. normalize
4. validate
5. construct networks
6. calculate metrics
7. calculate communities
8. calculate similarity
9. null models
10. sensitivity
11. robustness
12. generate figures
13. generate tables
14. export graphs
15. build website data
16. run final validation

sırasıyla çalışsın.

---

# 76. CONFIG

Analiz parametrelerini kod içine dağınık şekilde yazma.

`config/analysis.yaml`

oluştur.

Örneğin:

```yaml
seed: 42
community:
  algorithm: leiden

null_models:
  n_random: 1000

sensitivity:
  enabled: true
```

---

# 77. ENVIRONMENT

Oluştur:

`requirements.txt`

ve gerekiyorsa:

`environment.yml`

Ana paketler muhtemelen:

- pandas
- numpy
- scipy
- networkx
- igraph
- leidenalg
- matplotlib
- plotly
- scikit-learn
- statsmodels
- openpyxl
- pyarrow
- pyyaml
- pytest

olabilir.

Gereksiz dependency ekleme.

---

# 78. RANDOM SEED

Tüm stochastic işlemlerde seed kullan.

Python, numpy, community detection ve randomization seed'leri mümkün olduğunca kontrol edilsin.

---

# 79. AUTOMATED TESTS

`tests/`

oluştur.

Test et:

- schema
- IDs
- edge endpoints
- aliases
- graph size
- aggregation correctness
- deterministic outputs
- website data generation

---

# 80. VALIDATION GATE

Pipeline finalinde:

```text
VALIDATION STATUS:
PASS
WARNING
FAIL
```

oluştur.

Critical error varsa:

final release üretme.

---

# 81. HASH MANIFEST

Önemli input/output dosyalarının SHA-256 hash'lerini oluştur.

Örneğin:

`outputs/manifest_sha256.csv`

Bu reproducibility açısından önemlidir.

---

# 82. VERSIONING

Yeni çalışmayı:

`v4`

veya:

`research-rebuild-v1`

gibi açık biçimde versiyonla.

Legacy V3'ü kaybetme.

---

# 83. DATA DICTIONARY

Oluştur:

`docs/data_dictionary.md`

Her kolon için:

- field
- type
- meaning
- allowed values
- nullability
- source

belirt.

---

# 84. RELATION CODEBOOK

`docs/relation_codebook.md`

oluştur.

Her relation:

- definition
- parent family
- directionality
- polarity expectations
- examples

içersin.

---

# 85. METHODOLOGY DOCUMENT

`docs/methodology.md`

tez/makale yöntem bölümünün teknik kaynağı olacak düzeyde ayrıntılı olsun.

---

# 86. LIMITATIONS

`docs/limitations.md`

açık biçimde şunları tartışsın:

- single coder
- source edition dependency
- group actors
- inferred relations
- edge weighting
- incomplete metadata
- narrative-order ≠ historical time
- network projection artifacts
- entity resolution uncertainty
- interpretation limits

---

# 87. DATASET CARD

`DATASET_CARD.md`

oluştur.

İçerik:

- motivation
- composition
- collection
- preprocessing
- intended uses
- limitations
- ethical considerations
- license
- citation

---

# 88. CITATION FILE

`CITATION.cff`

oluştur.

Eksik author/publication metadata varsa placeholder veya TODO kullan.

Bilgi uydurma.

---

# 89. CHANGELOG

`CHANGELOG.md`

oluştur.

Legacy → rebuild değişikliklerini açıkça göster.

---

# 90. CONTRIBUTING

`CONTRIBUTING.md`

oluştur.

Özellikle yeni relation annotation eklemek isteyen araştırmacı için kuralları tanımla.

---

# 91. ACADEMIC MANUSCRIPT PACKAGE

Repository içinde:

```text
paper/
├── manuscript_outline.md
├── methods.md
├── results.md
├── tables/
├── figures/
└── supplementary_material.md
```

oluştur.

---

# 92. MAKALE TASLAĞI

Analiz tamamlandıktan sonra gerçek sonuçlardan hareketle İngilizce akademik makale taslağı hazırla.

Çalışma başlığı için örneğin:

**Mapping Narrative Structure in the Book of Dede Korkut: A Reproducible Multilayer Network Analysis**

veya gerçek sonuçlara göre daha uygun bir alternatif oluştur.

---

# 93. MANUSCRIPT STRUCTURE

Taslak:

1. Introduction
2. Related Work
3. Materials and Data
4. Methods
5. Results
6. Discussion
7. Limitations
8. Conclusion
9. Data and Code Availability

yapısında olsun.

---

# 94. RESULTS WRITING RULE

Sonuç yazarken yalnızca gerçekten hesaplanmış bulguları yaz.

Metrik sonucu:

"X actor is the most important character"

şeklinde aşırı yorumlama.

Doğrusu:

"X exhibited the highest betweenness centrality under the person-only core-social network specification."

gibi ölçüye bağlı ifade olsun.

---

# 95. THESIS PACKAGE

Ayrıca:

`thesis/`

dizininde:

```text
thesis/
├── proposed_structure.md
├── research_questions.md
├── methodology_mapping.md
├── results_mapping.md
├── figure_inventory.md
└── table_inventory.md
```

oluştur.

Bu belgeler yüksek lisans tezine entegrasyon için kullanılacak.

---

# 96. SUPPLEMENTARY MATERIAL

Ek materyal oluştur.

İçinde:

- full metric tables
- sensitivity results
- null model details
- coding protocol
- taxonomy
- validation results

olsun.

---

# 97. LITERATURE REVIEW HAZIRLIĞI

Bu Colab görevi internet araştırması yapmak zorunda değildir.

Ancak literatürde karşılaştırılması gereken kavramları ve arama sorgularını:

`reports/literature_search_plan.md`

dosyasına yaz.

Örneğin:

- literary network analysis
- narrative social networks
- multilayer literary networks
- digital humanities network analysis
- epic narrative networks
- Book of Dede Korkut computational analysis

---

# 98. SOURCE EDITION PROBLEM

Dede Korkut'un hangi metin/edition/transkripsiyon üzerinden kodlandığı repository'de açık değilse bunu kritik metadata eksikliği olarak işaretle.

Tahmin etme.

Oluştur:

`validation/source_edition_metadata_required.md`

Bu bilgi daha sonra araştırmacı tarafından doldurulabilir.

---

# 99. COPYRIGHT

Ham edebi metin repository'de yoksa internetten rastgele metin indirip repoya ekleme.

Telif durumu net olmayan metni redistribute etme.

Sadece mevcut kullanıcı verilerini kullan.

---

# 100. README YENİDEN TASARIMI

Root README güçlü akademik proje README'si olsun.

En az:

- project overview
- key features
- dataset snapshot
- repository structure
- methodology
- reproducibility
- website
- citation
- license

içersin.

---

# 101. ARCHITECTURE DIAGRAM

Proje veri akışını gösteren diyagram üret:

```text
Raw Coding
     ↓
Entity Resolution
     ↓
Canonical Dataset
     ↓
Validation
     ↓
Network Construction
     ↓
Analysis
     ↓
Statistical Validation
     ↓
Figures / Tables
     ↓
Website / Manuscript
```

SVG/PNG üret.

---

# 102. REPOSITORY STRUCTURE TARGET

Final repository tercihen:

```text
.
├── README.md
├── LICENSE
├── CITATION.cff
├── CHANGELOG.md
├── CONTRIBUTING.md
├── DATASET_CARD.md
├── requirements.txt
├── run_pipeline.py
├── config/
├── data/
│   ├── raw/
│   ├── story_level/
│   ├── legacy/
│   ├── processed/
│   └── derived/
├── src/
├── notebooks/
├── tests/
├── validation/
├── outputs/
├── reports/
├── paper/
├── thesis/
└── docs/
```

olsun.

---

# 103. GITHUB ACTIONS

Mümkünse:

`.github/workflows/validate.yml`

oluştur.

Push/PR sırasında en az:

```bash
python -m pytest
python run_pipeline.py --validate-only
```

çalıştırabilecek CI hazırla.

Runtime çok uzunsa ağır null-model analizlerini CI dışında bırak.

---

# 104. GITHUB PAGES

Web portalını GitHub Pages'e uygun hale getir.

Site relative path ile çalışmalı.

Local path hardcode etme.

---

# 105. SITE VALIDATION

Web build sonrası kontrol et:

- broken links
- missing assets
- missing JSON
- invalid paths
- missing figures

Site validation script oluştur.

---

# 106. WEB PERFORMANCE

Network Explorer'a tüm corpus graph'unu gereksiz dev payload olarak gömme.

Gerekirse lazy loading veya ayrı JSON dosyaları kullan.

---

# 107. GRAPH EXPORTS

Her önemli network için mümkünse:

- GraphML
- GEXF
- Cytoscape JSON
- edge CSV
- node CSV

üret.

---

# 108. MACHINE-READABLE RESULTS

Önemli sonuçlar ayrıca JSON olarak dışa aktarılsın.

Örneğin:

```text
docs/data/project_summary.json
docs/data/actor_metrics.json
docs/data/story_metrics.json
docs/data/network_summary.json
```

Website bunları kullansın.

---

# 109. ANALYSIS SUMMARY

Oluştur:

`outputs/analysis_summary.json`

Burada final gerçek sayılar makine tarafından okunabilir biçimde bulunsun.

README ve web sitesi mümkünse bunu temel alsın.

---

# 110. EXPLORATORY / CONFIRMATORY AYRIMI

Her analizi:

- descriptive
- inferential
- exploratory

olarak etiketle.

Exploratory sonuçları doğrulanmış teori gibi sunma.

---

# 111. EFFECT SIZES

İstatistiksel karşılaştırma yapılırsa yalnızca p-value raporlama.

Uygun effect size veya magnitude bilgisi ver.

---

# 112. MULTIPLE TESTING

Çok sayıda istatistiksel test yapılırsa multiple comparison problemini değerlendir.

Gerekirse:

- Benjamini-Hochberg FDR

uygula.

---

# 113. MISSING DATA

Eksik veri durumlarını:

- missing
- not applicable
- unknown

olarak ayır.

Hepsini 0 yapma.

---

# 114. NETWORK DENSITY NORMALIZATION

Farklı büyüklükte story networkleri karşılaştırırken node/edge sayısından kaynaklanan farklılıkları dikkate al.

Ham metrikleri sorgusuz biçimde doğrudan kıyaslama.

---

# 115. CENTRALIZATION

Uygunsa Freeman-style graph centralization hesapla.

Bunu node centrality ile karıştırma.

---

# 116. CROSS-STORY ACTORS

Birden fazla boyda bulunan aktörleri ayrıca analiz et.

Hesapla:

- story participation count
- narrative bridge role
- actor-story betweenness, uygunsa

---

# 117. CORE-PERIPHERY

Network uygunsa exploratory:

- core-periphery structure
- k-core decomposition

incele.

---

# 118. ARTICULATION POINTS

Graph teorisi açısından:

- articulation points
- bridges

belirle.

Bunları anlatısal zorunluluk olarak değil, network connectivity açısından yorumla.

---

# 119. CLI

Mümkünse:

```bash
python run_pipeline.py --stage audit
python run_pipeline.py --stage analysis
python run_pipeline.py --stage website
python run_pipeline.py --all
```

gibi kullanım oluştur.

---

# 120. LOGGING

Pipeline terminal çıktısını düzenli logging ile üret.

`logs/`

altına timestamp logları yaz.

---

# 121. PERFORMANCE

Null model veya ağır analizlerde runtime aşırı uzarsa:

- paralelleştirme
- caching

değerlendir.

Ama reproducibility bozma.

---

# 122. CACHE

Derived sonuçların yeniden hesaplanmasını azaltmak için cache kullanılabilir.

Ancak input hash değiştiğinde cache invalidate edilmeli.

---

# 123. RELEASE PREPARATION

Final validation PASS olduktan sonra:

`reports/RELEASE_CHECKLIST.md`

üret.

Kontrol et:

- dataset valid
- pipeline reproducible
- README updated
- website builds
- figures exist
- tests pass
- hashes generated
- citation file exists

---

# 124. FINAL PROJECT REPORT

Sonunda:

`reports/FINAL_REBUILD_REPORT.md`

oluştur.

Rapor en az şu bölümleri içersin:

## Initial State

Başlangıç repository durumu.

## Data Audit

Bulunan kalite problemleri.

## Data Corrections

Yapılan değişiklikler.

## Preserved Decisions

Bilinçli olarak korunan V3 kararları.

## Canonical Model

Yeni veri modeli.

## Network Models

Kullanılan network tanımları.

## Analyses

Gerçekleştirilen analizler.

## Statistical Validation

Null model ve diğer testler.

## Sensitivity

Model tercihlerine karşı kararlılık.

## Key Findings

Verinin gerçekten desteklediği en güçlü bulgular.

## Limitations

Bütün metodolojik sınırlılıklar.

## Website

Oluşturulan portal yapısı.

## Reproducibility

Pipeline ve validation.

## Academic Outputs

Tez ve makalede kullanılabilecek sonuçlar.

## Future Work

İkinci annotator, metadata enrichment vb.

---

# 125. EXECUTIVE SUMMARY

Ayrıca:

`reports/EXECUTIVE_SUMMARY.md`

oluştur.

Burada kısa biçimde:

- ne yaptık
- ne bulduk
- bilimsel katkı ne
- bundan sonra ne yapılmalı

anlat.

---

# 126. EN GÜÇLÜ BULGULAR

Final raporda:

**Top 5 strongest defensible findings**

başlığı oluştur.

Ancak gerçekten analiz sonucu oluşan bulguları seç.

İstatistik üretmeden sonuç yazma.

---

# 127. NEGATIVE RESULTS

Beklenen bir yapısal özellik çıkmadıysa gizleme.

Negative/null sonuçları da raporla.

---

# 128. HUMAN REVIEW QUEUE

Otomatik olarak karar verilemeyen bütün konuları:

`validation/HUMAN_REVIEW_QUEUE.csv`

içine koy.

Alanlar:

```text
item_id
category
source
issue
proposed_action
confidence
requires_human_decision
notes
```

---

# 129. PROJECT STATUS DASHBOARD

Web sitesi ana sayfasına küçük reproducibility/status paneli koy.

Örneğin:

```text
Dataset Validation: PASS
Pipeline: Reproducible
Network Models: 11
Stories analyzed: X
Last Build: ...
```

Değerleri build çıktısından al.

---

# 130. WEBSITE "METHOD TRANSPARENCY"

Her interaktif grafikte:

"Network definition"

butonu veya bilgi alanı olsun.

Kullanıcı hangi edge'lerin dahil edildiğini bilsin.

---

# 131. WEBSITE "DOWNLOAD THIS VIEW"

Mümkünse Network Explorer'daki filtrelenmiş görünümü:

- PNG
- CSV

olarak indirme fonksiyonunu değerlendir.

---

# 132. WEB STORY COMPARISON

Kullanıcı iki story seçip şu metrikleri kıyaslayabilsin:

- nodes
- edges
- density
- centralization
- modularity
- conflict ratio
- support ratio

---

# 133. WEB CHARACTER COMPARISON

İki karakter karşılaştırma görünümü oluşturmak uygunsa:

- story count
- degree
- betweenness
- PageRank
- layers
- community

göster.

---

# 134. WEBSITE DISCLAIMER

Site açıkça şunu belirtmeli:

Network metrics are structural representations derived from the encoded dataset and should not be interpreted as complete literary judgments about character importance.

---

# 135. WEB SOURCES / CITATION

Citation bölümünde:

- repository citation
- dataset version
- license
- forthcoming publication placeholder

olsun.

Uydurma DOI verme.

---

# 136. PROJECT NAME

Çalışma için geçici teknik ad kullanılabilir:

**Dede Korkut Narrative Network Project — DKNN**

Ancak repository adını hemen değiştirme.

Final raporda proje isim alternatifleri önerebilirsin.

---

# 137. ÇALIŞMA SIRASI

Şu sırayı uygula:

## PHASE 1
Repository audit

## PHASE 2
Data validation

## PHASE 3
Canonical dataset

## PHASE 4
Network construction

## PHASE 5
Descriptive analysis

## PHASE 6
Advanced network analysis

## PHASE 7
Statistical validation

## PHASE 8
Sensitivity analysis

## PHASE 9
Figures and tables

## PHASE 10
Web portal

## PHASE 11
Documentation

## PHASE 12
Paper/thesis package

## PHASE 13
Final validation

## PHASE 14
Release report

---

# 138. ÇALIŞMA BİÇİMİN

Her phase tamamlandıktan sonra bana kısa durum mesajı ver:

```text
PHASE X COMPLETE

Created:
...

Key findings:
...

Warnings:
...

Next:
...
```

Ardından çalışmaya devam et.

Benden her küçük adımda izin isteme.

---

# 139. HATALAR

Kod hata verirse:

1. traceback oku
2. nedeni belirle
3. düzelt
4. yeniden çalıştır
5. sonucu doğrula

Hata mesajını görüp işi yarıda bırakma.

---

# 140. GERÇEKLİK KONTROLÜ

Bir analiz metodolojik olarak yapılamıyorsa:

"uyguladım"

deme.

Örneğin yeterli örnek yoksa:

"not applicable"

olarak işaretle.

---

# 141. AKADEMİK TUTUM

Amaç mümkün olduğunca çok sonuç üretmek değildir.

Amaç:

**az ama güvenilir sonuç**

üretmektir.

Modeli olduğundan büyük gösterme.

---

# 142. FINAL QUALITY GATE

Proje ancak aşağıdaki şartlarda final sayılabilir:

- raw data korunmuş
- canonical data üretilmiş
- provenance korunmuş
- validation tests geçmiş
- network definitions dokümante edilmiş
- analyses reproducible
- figures regenerated
- tables regenerated
- sensitivity analysis tamamlanmış
- web portal build edilmiş
- broken links temizlenmiş
- README doğru
- paper package üretilmiş
- thesis package üretilmiş
- final report üretilmiş

---

# 143. SON GIT DURUMU

İş sonunda bana:

```bash
git status
git diff --stat
```

benzeri özet ver.

Yeni directory tree göster.

---

# 144. COMMIT PLAN

Değişiklikleri mantıksal commit'lere ayır.

Örneğin:

```text
1. Add reproducible data validation pipeline
2. Introduce canonical Dede Korkut dataset schema
3. Add multilayer network construction and analysis
4. Add statistical and sensitivity analyses
5. Add publication-quality figures and tables
6. Build interactive GitHub Pages research portal
7. Add reproducibility and methodological documentation
8. Add manuscript and thesis research packages
```

---

# 145. GITHUB PUSH

Ben açıkça istemeden main branch'e doğrudan push yapma.

Çalışma branch'i hazırla.

Final değişiklikleri bana raporla.

---

# 146. PROJENİN NİHAİ FELSEFESİ

Bu repository yalnızca CSV dosyalarının depolandığı bir alan olmayacak.

Nihai repository şu beş rolü aynı anda taşımalıdır:

## 1. DATASET

Araştırmacı veriyi indirebilir.

## 2. COMPUTATIONAL STUDY

Analiz tamamen yeniden üretilebilir.

## 3. EVIDENCE PACKAGE

Sonuçların nasıl üretildiği görülebilir.

## 4. INTERACTIVE RESEARCH PORTAL

Networkler ve sonuçlar tarayıcıdan incelenebilir.

## 5. ACADEMIC RESEARCH PACKAGE

Tez ve makale üretimi için gereken metot, tablo, görsel ve sonuçlar hazırdır.

---

# 147. İLK GÖREV

Şimdi henüz hiçbir şeyi yeniden tasarlamaya çalışma.

Öncelikle:

1. repository'yi clone et,
2. directory tree çıkar,
3. raw, story_level ve final dosyalarını tara,
4. mevcut V3 sayılarını yeniden hesapla,
5. schema ve veri problemlerini belirle,
6. `reports/01_repository_audit.md` oluştur,
7. başlangıç validation özetini bana göster.

Bundan sonra yukarıdaki phase planına göre kesintisiz devam et.

Mevcut verinin desteklemediği hiçbir bilgiyi uydurma.

Her önemli metodolojik kararı kod ve dokümantasyonla izlenebilir hale getir.

Nihai hedef:

**akademik olarak savunulabilir, çok katmanlı, istatistiksel olarak doğrulanmış, tamamen yeniden üretilebilir ve interaktif web portalıyla yayımlanan Dede Korkut anlatı ağı araştırma platformu oluşturmaktır.**