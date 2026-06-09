# Dede Korkut Hazır Veri Seti v2

Bu klasör, önceki temiz veri seti üzerinde ikinci tur standartlaştırma uygulanarak oluşturulmuştur.

## Bu turda yapılan başlıca düzeltmeler
- `Kendi Aralarında` ve `Kendi Kendine` düğümleri edge listesinden çıkarılıp olay listesine taşındı.
- Boy bağlamına göre belirsiz/genel düğümler ayrıştırıldı:
  - `Tekfur` -> `Tekfur (Boy Adı)`
  - `Kafirler` -> `Kafirler (Boy Adı)`
  - `Beyler` -> `Beyler (Boy Adı)`
  - `Bir Kişi` / `Kişi` -> `Adsız Kişi (Boy Adı)`
- Belirgin alias birleştirmeleri yapıldı:
  - `Kazan`, `Kazan Bey` -> `Salur Kazan`
  - `Beyrek` -> `Bamsı Beyrek`
  - bazı aile/grup etiketleri imla ve adlandırma açısından standardize edildi.

## Dosyalar
- `dede_korkut_kenarlar_temiz_v2.csv`: analiz için kullanılacak nihai kenar listesi
- `dede_korkut_olaylar_temiz_v2.csv`: ağ dışı ama anlatı açısından önemli olay kayıtları
- `dede_korkut_dugumler_temiz_v2.csv`: düğüm tablosu
- `dede_korkut_alias_sozlugu_v2.csv`: alias sözlüğü
- `dede_korkut_degisim_logu_v2.csv`: yapılan dönüşümlerin logu
- `00_boy_dataset_indeksi_temiz_v2.csv`: boy bazlı özet
