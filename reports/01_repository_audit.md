# Repository Audit — Faz 1

**Tarih:** 2026-09-16
**Kaynak:** `data/audit_data.json` (programatik olarak üretilmiştir; bu rapordaki tüm sayılar oradan alınmıştır, elle girilmemiştir)
**Script:** [`src/audit.py`](../src/audit.py)
**Branch:** `claude-dk-rebuild`

---

## 1. Repository Ağacı (klonlama sonrası)

```text
.
├── README.md
├── LICENSE
├── data/
│   ├── raw/
│   │   └── dede korkut karakterler.xlsx      (13 sheet, "Source/Target/Weight/Type" şeması)
│   ├── story_level/                          (14 CSV, boy başına bir dosya, 21 kolonlu ortak şema)
│   └── final/
│       ├── 00_boy_dataset_indeksi_temiz.csv
│       ├── dede_korkut_dugumler_temiz.csv    (node list)
│       ├── dede_korkut_kenarlar_temiz.csv    (edge list)
│       ├── dede_korkut_olaylar_temiz.csv     (event list)
│       ├── dede_korkut_alias_sozlugu.csv
│       ├── dede_korkut_degisim_logu.csv
│       └── dede_korkut_degisim_logu_v3_only.csv
└── docs/
    ├── README_v2.md
    └── README_v3.md
```

`data/legacy/`, `data/processed/`, `data/derived/`, `src/`, `notebooks/`, `tests/`, `validation/`, `outputs/`, `reports/`, `paper/`, `thesis/` gibi hedef dizinler repository'de **henüz mevcut değil** — bunlar Faz 3+'ta oluşturulacak.

---

## 2. README'deki Temel Sayıların Doğrulanması

README.md şu dört sayıyı iddia ediyor: Stories=14, Nodes=333, Edges=628, Narrative Events=85.

Bu sayılar `data/final/` dosyalarından programatik olarak **yeniden hesaplandı** (kör kabul edilmedi):

| Metrik | README İddiası | Yeniden Hesaplanan | Durum |
|---|---|---|---|
| Stories (source_file sayısı) | 14 | 14 | ✅ Doğrulandı |
| Stories (edges içindeki benzersiz `boy`) | 14 | 14 | ✅ Doğrulandı |
| Nodes (satır sayısı) | 333 | 333 | ✅ Doğrulandı |
| Nodes (benzersiz `dugum_id`) | — | 333 | ✅ Duplicate ID yok |
| Edges | 628 | 628 | ✅ Doğrulandı |
| Narrative Events | 85 | 85 | ✅ Doğrulandı |

**Sonuç:** README'deki 4 temel sayı, `data/final/` dosyalarıyla tam tutarlı. Bu iyi bir başlangıç noktası — final dataset kendi içinde iç tutarlı.

Ekstra, README'de geçmeyen sayılar:
- Alias sözlüğü: **525** satır (`dede_korkut_alias_sozlugu.csv`)
- Değişim logu (v2+v3 birleşik): **346** satır, `v3_only`: **66** satır (README_v3.md'nin iddia ettiği "66 yeni değişim kaydı" ile eşleşiyor ✅)

---

## 3. KRİTİK BULGU — `story_level/` → `data/final/` İzlenebilirlik Kaybı

Bu, bu denetimin **en önemli bulgusu**dur.

`00_boy_dataset_indeksi_temiz.csv` dosyasındaki boy başına edge/event sayıları, `data/final/` dosyalarındaki gerçek `source_file` filtrelemesiyle **birebir tutarlı** (index dosyası doğru). Ancak bu sayılar, aynı boy'un `data/story_level/` dosyasındaki ham satır sayısıyla **tutarlı değil**:

| source_file | story_level satır sayısı | final (edges+events) | fark |
|---|---:|---:|---:|
| 01_girizgah.csv | 1 | 1 | +0 |
| 02_dirse_han... | 23 | 26 | **+3** |
| 03_salur_kazanin_evinin... | 51 | 51 | +0 |
| 04_kam_purenin... | 109 | 128 | **+19** |
| 05_kazan_bey_oglu_uruz... | 41 | 46 | **+5** |
| 06_duha_koca... | 22 | 24 | **+2** |
| 07_kanli_koca... | 41 | 52 | **+11** |
| 08_kazilik_koca... | 24 | 28 | **+4** |
| 09_basatin_tepegozu... | 65 | 74 | **+9** |
| 10_begil_oglu_emrenin... | 59 | 65 | **+6** |
| 11_usun_koca_oglu_seyrek... | 54 | 61 | **+7** |
| 12_salur_kazanin_tutsak... | 68 | 80 | **+12** |
| 13_ic_oguza_dis_oguzun... | 39 | 41 | **+2** |
| 14_salur_kazanin_yedi_basli... | 36 | 36 | +0 |
| **TOPLAM** | **633** | **713** | **+80** |

`data/final/` dosyaları, karşılık gelen `data/story_level/` dosyalarından **toplam 80 satır daha fazla** kayıt içeriyor (11 boy'da fark var, 3 boy'da fark yok).

**Bunun ne anlama gelebileceği (doğrulanmamış hipotezler — hiçbiri kesin değildir):**
- v2/v3 standardizasyon sürecinde bazı `story_level` satırları (örn. birden fazla ilişkiyi aynı anda kodlayan bileşik satırlar) birden fazla final edge/event satırına **bölünmüş** olabilir.
- Bu bölme işlemi `docs/README_v2.md` veya `docs/README_v3.md` içinde **belgelenmemiş**.
- `dede_korkut_degisim_logu.csv` bu tip "1 satır → N satır" dönüşümlerini izlenebilir şekilde kaydetmiyor (sadece alan bazlı `eski_deger`→`yeni_deger` değişikliklerini tutuyor, satır bölünmesini değil).

**Sonuç:** Ham (`story_level`) veri ile nihai (`final`) veri arasındaki dönüşüm **tam olarak izlenebilir değil**. Bu, projenin "hiçbir veri uydurulmayacak / provenance izlenebilir olacak" ilkesi (madde 2-3) açısından **kapatılması gereken bir şeffaflık boşluğudur**. Bu satır bölünmelerinin gerçek anlatı temelli mi (örn. tekrarlayan diyalog) yoksa kodlama artefaktı mı olduğu, orijinal araştırmacı (proje sahibi) tarafından doğrulanmadan network inşasında **varsayım olarak kullanılmayacaktır**.

**Aksiyon:** `validation/HUMAN_REVIEW_QUEUE.csv` içine bu 11 boy için "story_level→final satır sayısı uyuşmuyor, bölünme mantığı belgelenmemiş" kaydı açılacak (Faz 2/3'te).

---

## 4. KRİTİK BULGU — Raw Excel, Story-Level/Final Verinin Doğrudan Kaynağı Değil

`data/raw/dede korkut karakterler.xlsx` (13 sheet, kolonlar: `Source, Target, Weight, Type`) incelendi.

Bu dosya **çok daha basit bir şemaya** sahip (4 kolon, ağırlık + tip) ve **girizgah için sheet içermiyor** (13 sheet vs. 14 story_level dosyası — beklenen, çünkü girizgah bir boy değil). Ancak asıl sorun satır sayıları:

| Raw sheet | Raw satır | Eşleşen final `boy` | Final satır |
|---|---:|---|---:|
| Dirse Han Oğlu Boğaç Han Boyu | 15 | *(otomatik eşleştirilemedi)* | — |
| Salur Kazan'ın Evinin Yağmalanm | 22 | Salur Kazan'ın Evinin Yağmalandığı | 51 |
| Kam Püre'nin Oğlu Bamsı Beyrek | 20 | Kam Püre'nin Oğlu Bamsı Beyrek Boyu | 107 |
| Kazan Bey Oğlu Uruz Bey'in Tuts | 23 | Kazan Bey Oğlu Uruz Bey'in Tutsak Olduğu Boy | 40 |
| Duha Koca Oğlu Deli Dumrul | 9 | Duha Koca Oğlu Deli Dumrul | 22 |
| ... | ... | ... | ... |

Hiçbir sheet'in satır sayısı, karşılık gelen final boy'un edge sayısıyla eşleşmiyor (genelde raw çok daha az satır içeriyor — örn. Kam Püre: 20 vs 107). Kolon şeması da (`Source/Target/Weight/Type`) final şemasıyla (`karakter_1/karakter_2/iliski_turu/katman/kutupluluk/yonluluk/cikarma_yontemi/...`) **hiçbir 1:1 mapping'e sahip değil**.

**Sonuç:** `data/raw/dede korkut karakterler.xlsx`, mevcut `data/story_level/` ve `data/final/` verisinin **doğrudan ham kaynağı değildir**. Muhtemelen daha önceki/farklı bir taslak (V1'den de önceki bir network-export denemesi) ya da paralel bir çalışmadır. Gerçek ham kodlama süreci (orijinal metin okuması, satır satır kodlama notları) **repository'de bulunmuyor**.

Bu, madde 98 ("SOURCE EDITION PROBLEM") kapsamında kritik bir eksiklik olarak işaretlenmiştir → `validation/source_edition_metadata_required.md` Faz 2'de oluşturulacak.

**Not:** `data/raw/` klasörü değiştirilmeyecek/silinmeyecek (immutable ilkesi). Bu xlsx, "V1'den de eski bir taslak" olarak `data/legacy/` içine referans amaçlı taşınabilir ama orijinal `data/raw/` içeriği korunacaktır.

---

## 5. Veri Kalitesi Bulguları (Faz 2'de tam validation framework'e dönüştürülecek)

### 5.1 Node (`dede_korkut_dugumler_temiz.csv`) — genel olarak sağlıklı
- 333 satır, 333 benzersiz `dugum_id` → **duplicate ID yok**
- Tüm edge/event uçları (`karakter_1_id`, `karakter_2_id`, `aktor_id`, `hedef_id`) node tablosunda mevcut → **orphan endpoint yok**
- Tüm node'lar en az bir edge/event'te referans alınıyor → **kullanılmayan node yok**
- **1 adet aynı isim → 2 farklı ID çakışması bulundu:**

  | dugum_id | dugum_adi | dugum_tipi |
  |---|---|---|
  | `begilin_adamlari` | Begil'in Adamları | grup |
  | `begil_in_adamlari` | Begil'in Adamları | grup |

  Bu muhtemelen aynı kolektif aktörün iki farklı slug ile kodlanmasından kaynaklanıyor (`Begilin Adamları` → `Begil'in Adamları` standardizasyonu sırasında eski/yeni ID'nin her ikisi de tabloya girmiş olabilir; bkz. `docs/README_v3.md` madde: `Begilin Adamları` -> `Begil'in Adamları`). → `validation/entity_resolution_candidates.csv`'ye aday olarak eklenecek (Faz 2).

- Node tipi dağılımı (`dugum_tipi`): `kişi`=187, `grup`=125, `mitolojik/ilahi`=8, `hayvan`=6, `nesne/doğa`=6, `yer/coğrafya`=1.
  → **Önemli:** "person-only network" (G1) tanımı literatürde genelde `kişi` vs `grup` ikiliğine indirgenir, ama veri seti bundan daha zengin bir tipoloji içeriyor. Sensitivity analizinde (madde 34) `kişi` dışındaki tüm tipler (`grup`, `mitolojik/ilahi`, `hayvan`, `nesne/doğa`, `yer/coğrafya`) ayrı ayrı ele alınmalı, hepsi "grup" gibi tek kategoriye indirgenmemelidir.

### 5.2 Edge (`dede_korkut_kenarlar_temiz.csv`)
- **Missing endpoint: 0** — her satırda hem `karakter_1_id` hem `karakter_2_id` dolu.
- **Self-loop: 1 adet** — `DKR0220`, Kam Püre boyu, `Bamsı Beyrek` → `Bamsı Beyrek`. Beklenmeyen bir self-loop olarak işaretlendi; anlatı bağlamı (satir_no ile orijinal metne referans) manuel olarak kontrol edilmeli.
- **"Tekrarlayan" ilişki kalıpları (aynı `karakter_1_id`+`karakter_2_id`+`iliski_turu`+`boy`): 114 satır.** Örnekler incelendiğinde bunların çoğu **farklı `satir_no`** değerlerine sahip — yani muhtemelen aynı aktör çiftinin anlatı boyunca **birden fazla kez** aynı türde etkileşime girmesini temsil ediyorlar (örn. tekrarlayan diyalog), kopyala-yapıştır hatası değil. **Bu satırlar silinmeyecek** — event-level/aggregated network ayrımı (madde 12) tam olarak bu tekrarları `interaction_count` gibi bir alanda korumak için var. Ancak küçük bir alt küme gerçek kopya olabilir; tam liste `outputs/validation/` altında Faz 2'de üretilecek.
- **Relation taxonomy kapsama sorunu:** `iliski_turu` dağılımında en büyük kategori **`belirsiz` (186 / 628 = %29.6)**. Yani edge'lerin neredeyse üçte biri "belirsiz" ilişki türüne sahip. Bu, relation taxonomy tabanlı analizlerin (madde 13, katman bazlı networkler) kapsama oranını doğrudan sınırlıyor — raporlarda açıkça belirtilecek.
- **`katman` (layer) dağılımı:** `olay`=230, `iletişim`=140, `çatışma`=109, `akrabalık`=78, `otorite`=66, `mekân`=3, `kimlik`=2.
  ⚠️ **Terminoloji uyarısı:** `katman="olay"` değeri, edge tablosunun **kendi içinde** bir ilişki katmanı iken, ayrıca **tamamen ayrı bir `dede_korkut_olaylar_temiz.csv` (events) tablosu** da var. Bu iki farklı "event/olay" kavramı karıştırılmamalı — `docs/data_dictionary.md`'de açıkça ayrıştırılacak (Faz 11).
- **`agirlik` (weight):** Tüm değerler 1–5 arası tam sayı, non-numeric değer yok. Bu bir **ordinal kodlama kategorisi** gibi görünüyor (muhtemelen "ilişki yoğunluğu/önemi" skoru), tekrar sayısı (interaction count) değil. Semantiği doğrulanana kadar bu ayrım açıkça belgelenecek (madde 36).
- **`boy` alanında yazım/büyük-küçük harf tutarsızlığı:** 14 benzersiz `boy` değerinden 4 tanesi diğerlerinden farklı bir konvansiyon izliyor:
  - `'Begil Oğlu Emrenin boyu'` (küçük "boyu")
  - `'Kazılık koca oğlu yigenek boyu'` (tamamen küçük harf)
  - `'uşun koca oğlu seyrek boyu'` (tamamen küçük harf)
  - `'Dirse Han Oglu boğaç Han Boyu'` (karışık: "Oglu" aksansız, "boğaç" küçük harf)
  - `"13. Boy: Salur Kazan'ın Yedi Başlı Ejderhayı Öldürmesi"` (diğerlerinden tamamen farklı format — "13. Boy:" öneki var)

  Bu değerler `source_file` ile tutarlı şekilde eşleşiyor (analiz `source_file` üzerinden grupluyor, `boy` metni sadece görüntüleme amaçlı), dolayısıyla **network inşasını bozmuyor**, ama görsellerde/tablolarda kullanıcıya gösterilecek boy adları için bir **normalizasyon tablosu** gerekli (Faz 3, `data/processed/stories.csv`).

### 5.3 Event (`dede_korkut_olaylar_temiz.csv`)
- 85 satır, `hedef`/`hedef_id`/`hedef_tipi` 75 satırda boş (`NaN`) — beklenen, çünkü çoğu event tek aktörlü (hedefsiz) narratif eylemler (örn. "otorite/emir", "akrabalık" bildirimi). Bu **eksik veri değil, şema gereği opsiyonel alan** — `missing` olarak değil `not_applicable` olarak ele alınacak (madde 113).
- Orphan aktör ID: 0. Tüm `aktor_id`/`hedef_id` node tablosunda mevcut.

### 5.4 Değişim Logu
- `dede_korkut_degisim_logu.csv`: 346 satır, 80 tekrarlanan `kayit_id` var. Bu beklenen bir davranış olabilir (aynı kayıt birden fazla alanda düzenlenmiş olabilir — örn. hem `karakter_1` hem `katman` değişmiş, iki ayrı log satırı olarak tutulmuş), ancak bu **doğrulanmadı**. `source_file`/`degisim_tipi` kolonları 66 satırda boş — bu tam olarak `v3_only` dosyasının satır sayısına (66) denk geliyor, yani v3-only kayıtları ana loga eklenirken bu iki kolon doldurulmamış (v3_only dosyası bu kolonlara zaten sahip değil). Şema tutarsızlığı olarak not edildi, veri kaybı değil.
- Mojibake / bozuk karakter kodlaması taraması: **0 şüpheli örnek** bulundu. Türkçe karakterler (`ı, ş, ğ, ö, ü, ç, İ`) tüm dosyalarda tutarlı UTF-8 olarak okunuyor.

---

## 6. Encoding / Dtype Özeti

Tüm CSV dosyaları `utf-8-sig` ile sorunsuz okunabildi (BOM'lu UTF-8). Hiçbir dosyada encoding hatası veya latin1/cp1254 fallback gerekmedi. `data/raw/*.xlsx` standart Excel formatında, sorunsuz.

Tam dosya bazlı profil (satır/kolon/null/duplicate sayıları) → [`reports/audit_data.json`](audit_data.json).

---

## 7. Başlangıç Validation Özeti

```text
VALIDATION STATUS (Faz 1 — ön değerlendirme, Faz 2'de resmileşecek):

PASS:
  - README headline sayıları (14/333/628/85) doğrulandı
  - Node ID benzersizliği: PASS (0 duplicate)
  - Edge endpoint bütünlüğü: PASS (0 orphan, 0 missing endpoint)
  - Event actor bütünlüğü: PASS (0 orphan)
  - Encoding: PASS (mojibake yok)

WARNING:
  - 1 node adı 2 farklı ID'ye sahip (Begil'in Adamları) → entity resolution gerekiyor
  - 1 beklenmeyen self-loop (Bamsı Beyrek → Bamsı Beyrek)
  - "boy" alanında 4-5 yazım/büyük-küçük harf tutarsızlığı (kozmetik, network'ü etkilemiyor)
  - iliski_turu'nun %29.6'sı "belirsiz" (taxonomy kapsama sınırlaması)
  - 114 satırda "tekrarlayan" ilişki kalıbı — çoğunlukla meşru narratif tekrar, ama tam liste doğrulanmadı

FAIL / CRITICAL (veri silinmeyecek, ama izlenebilirlik eksik olarak işaretlendi):
  - story_level (633 satır) → final edges+events (713 satır) arasında +80 satırlık
    açıklanmamış fark; dönüşüm mantığı hiçbir dokümanda yok
  - data/raw/*.xlsx, story_level/final verisinin doğrudan ham kaynağı değil;
    gerçek ham kodlama kaynağı repository'de mevcut değil (source edition problem)
```

---

## 8. Sıradaki Adım

Faz 2 (Data Validation) başlatılacak: yukarıdaki WARNING/CRITICAL bulgular için tam `outputs/validation/` framework'ü, `validation/entity_resolution_candidates.csv`, `validation/HUMAN_REVIEW_QUEUE.csv` ve `validation/source_edition_metadata_required.md` üretilecek; `reports/02_data_quality_report.md` yazılacak.

Bu rapor, kullanıcı onayı beklemeden Faz 2'ye otomatik geçiş için temel referans olacaktır.
