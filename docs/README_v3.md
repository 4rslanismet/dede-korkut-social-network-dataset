# Dede Korkut Veri Seti v3

Bu sürüm, v2 temiz veri seti üzerinden ek bağlamsal ve anlamsal standardizasyonlar yapılarak üretilmiştir.

## Bu turda özellikle yapılanlar
- `Aruz` ve `Aruz Koca` **ayrı anlatı aktörleri** olarak korunmuştur.
- Kolektif düğümler (`600 Kafir`, `40 Ince Belli Kız` vb.) **korunmuş**, ancak gerekli yerlerde `grup` tipine sabitlenmiştir.
- Genel ve bağlamdan kopuk hedefler bağlamsal olarak netleştirilmiştir:
  - `Askerleri` -> `Tekfurun Askerleri` / `Kazanın Askerleri`
  - `Beyleri` -> `Tekfurun Beyleri` / `İç Oğuz Beyleri`
  - `Çevresine`, `Çevresindekilere` -> `Çevresindekiler`
  - `Beylere` -> `Beyler (Bamsı Beyrek Boyu)`
- Düğüm alanına sızmış eylem/olay ifadeleri edge listesinden çıkarılıp olay listesine taşınmıştır:
  - `DKR0252`, `DKR0345`, `DKR0708`, `DKR0122`, `DKR0167`
- Yazım ve varyant standardizasyonları yapılmıştır:
  - `Iç Oğuz` -> `İç Oğuz`
  - `Iç Oğuz Beyleri` -> `İç Oğuz Beyleri`
  - `Begilin Adamları` -> `Begil'in Adamları`
  - `Anne Babası` -> `Anne ve Babası`
  - `Yalancı Oğlu Yaltaçuk` / `Yaltaçuk` -> `Yalançı Oğlu Yaltaçuk`
  - `Burla`, `Uzun Boylu Burla Hatun` -> `Burla Hatun`
  - `Selcen` -> `Selcen Hatun`
- Açık kolektif düğüm tipleri düzeltilmiştir:
  - `Tekfurun Askerleri`, `Tekfurun Beyleri`, `Tekfurun Adamları`, `Bamsı'nın Kız Kardeşleri`, `Kocalar`, `Yarar Kocalar`, `Beyrek'in 40 Yoldaşları`

## Dosyalar
- `dede_korkut_kenarlar_temiz_v3.csv`: Nihai kenar listesi
- `dede_korkut_olaylar_temiz_v3.csv`: Tek düğümlü/olay temelli kayıtlar
- `dede_korkut_dugumler_temiz_v3.csv`: Güncel düğüm sözlüğü
- `dede_korkut_alias_sozlugu_v3.csv`: Genişletilmiş alias sözlüğü
- `dede_korkut_degisim_logu_v3.csv`: v2 + v3 birleşik değişim logu
- `dede_korkut_degisim_logu_v3_only.csv`: yalnızca bu turda yapılan değişiklikler
- `00_boy_dataset_indeksi_temiz_v3.csv`: boy bazlı özet

## Özet
- Düğüm sayısı: 333
- Kenar sayısı: 628
- Olay sayısı: 85
- Bu turdaki yeni değişim kaydı: 66

Not: Bu sürüm, ağ analizine doğrudan verilebilecek işlenmiş veri setidir.
