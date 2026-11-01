# Documentation — Faz 17

Bu faz yeni analiz üretmedi — Faz 1-16'da zaten üretilen bilgiyi (şemalar, ilişki taksonomisi,
metodolojik kararlar, dağınık limitasyonlar) sentezleyip kalıcı, tek-parça dokümanlara dönüştürdü.

## Üretilen Dosyalar

| Dosya | İçerik |
|---|---|
| `docs/data_dictionary.md` | `data/processed/`'un 8 dosyasının tamamı — alan/tip/anlam/izin verilen değerler/null oranı/kaynak, gerçek `non-null`/`nunique` sayılarıyla |
| `docs/relation_codebook.md` | 17 ilişki türünün tamamı, gerçek `raw_evidence` örnekleriyle (`relations_event_level.csv`'den çekildi, uydurulmadı) |
| `docs/methodology.md` | Genişletilmiş, tez-metodoloji-bölümü kaynağı olacak düzeyde; her DEC-XXX kararına atıf var |
| `docs/limitations.md` | 17 madde, dağınık limitasyonların tek dokümanda konsolidasyonu (yeni: madde 11 — Faz 15'te bulunan 5 birleştirilmiş node) |
| `DATASET_CARD.md` | Motivation/composition/collection/preprocessing/intended uses/limitations/ethics/license/citation |
| `CITATION.cff` | Yazar adı/yayın tarihi alanları **TODO** olarak bırakıldı — uydurulmadı |
| `CHANGELOG.md` | Legacy v3 → bu rebuild'in tam değişim listesi (Added/Fixed/Discovered-not-fixed/Known-incomplete) |
| `CONTRIBUTING.md` | Yeni ilişki ekleme, metadata ekleme, entity merge önerme, website değişikliği kuralları |
| `docs/architecture_diagram.svg` | 11 kutulu veri akışı diyagramı, tarayıcıda görsel olarak doğrulandı |
| `README.md` | Kökten yeniden tasarlandı — gerçek sayılar, repo yapısı, metodoloji özeti, reproducibility, website, citation, license |

## Doğrulama

Site build + `validate_site.py` yeniden çalıştırıldı (yeni dokümanlara linkler eklendiği için):
**363/363 dosya PASS, 0 sorun.**

## Not: CITATION.cff Yazar Bilgisi

Repository sahibinin gerçek adı/soyadı bilinmiyor (yalnızca GitHub kullanıcı adı `4rslanismet`
biliniyor). Madde 88'in kuralına uyularak ("Eksik author/publication metadata varsa placeholder
veya TODO kullan... Bilgi uydurma") bu alanlar `TODO` olarak bırakıldı.

## Sıradaki Adım

Faz 18 (Paper Package) → Faz 19 (Thesis Package) → Faz 20 (Final Validation) → Faz 21 (Final Reports).
