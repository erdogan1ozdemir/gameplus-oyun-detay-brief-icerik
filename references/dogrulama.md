# Doğrulama: hangi bilgi hangi kaynaktan

Oyun verisi hızla eskiyor ve elimizdeki kaynaklar birbiriyle çelişebiliyor. Her sayı için
aşağıdaki sıra izlenir. Üstteki kaynak alttakini ezer.

## Kaynak sırası

| Bilgi | Birincil kaynak | İkincil | Not |
|---|---|---|---|
| Sistem gereksinimleri | Steam `appdetails` (`pc_requirements`) | EA / yayıncı sayfası | Steam Türkçe çeviriyle döner, doğrudan kullanılabilir |
| Kurulum boyutu | Steam gereksinimleri (min ve önerilen ayrı) | - | Minimum ve önerilen farklıysa ikisi de yazılır |
| Resmi dil desteği | Steam `supported_languages` | PlayStation destek sayfası | Türkçe listede yoksa **yok** demektir; topluluk yaması resmi destek sayılmaz |
| Metacritic puanı | metacritic.com sayfasının kendisi | Steam `metacritic` alanı | Steam'in değeri önbellekten gelir ve 1-2 puan geride kalabilir |
| Hikâye modu süresi | HowLongToBeat | Oyun basını (GamesRadar, IGN) | İki bağımsız kaynak örtüşmüyorsa süre yazılmaz |
| GFN paket ve sunucu değerleri | `gameplus.com.tr/gfn/paketler` | - | **Tek geçerli kaynak budur** |
| GFN'de var mı, optimize mi | GFN oyun kataloğu (`katalog.py`) | nvidia.com GFN sayfası | Katalog "Tam optimize / Tam optimize değil" verir |
| Oyunun modları, hikâyesi, mekanikleri | Markanın kendi blog yazısı | Yayıncı sayfası | Blog varsa önce o okunur, ton ve terim tutarlılığı için |
| Çıkış tarihi | Katalog + Steam | - | GFN yayın tarihi ile mağaza satış tarihi farklı olabilir |

## Bilinen tuzaklar

**GAME+ Türkiye'de RTX 5080 yok.** Paketler sayfasına göre Performance = GeForce RTX / 8 vCPU /
1440p / 60 FPS'e kadar / 6 saatlik oturum, Ultimate = **GeForce RTX 4080** / 16 vCPU / 4K HDR /
240 FPS'e kadar / 8 saatlik oturum. Markanın kendi blog yazılarında "RTX 5080 sınıfı sunucular"
ifadesi geçiyor; bu global GFN tarafına ait ve Türkiye paketlerine uymuyor. Sunucu sınıfı yazılacaksa
paketler sayfasından teyit edilir.

**Katalogdaki üyelik seviyesi NVIDIA adlandırmasıyla gelir.** `Üyelik seviyesi: Premium` gibi
değerler GAME+ paket adları (Performance / Ultimate) ile aynı şey değildir. Zaten hangi paketin
gerektiği yazılmadığı için bu alan içerikte kullanılmaz, yalnız iç bilgi olarak kalır.

**Main KW hacmi yeni oyunlarda yanıltıcıdır.** 12 aylık ortalama, çıkış ayındaki zirveyi taşır.
Battlefield 6 örneğinde 12 aylık ortalama 49.500 iken Ekim 2025 zirvesi 135.000, Mayıs-Temmuz 2026
ortalaması 15.900. Standart 12 aylık değer sütunda kalır, son üç ayın ortalaması DİKKAT satırına yazılır.

**Katalogdaki `sortName` alanı oyun adı değildir.** Sıralama anahtarıdır ve bir bölümü sıra numarası
taşır (`counter_strike_4`, `fallout_03a`). Aratılacak ad `title` alanından üretilir.

**Steam'in geliştirici alanı katalogdan farklı olabilir.** Battlefield 6'da Steam "Battlefield Studios",
katalog "Electronic Arts DICE" diyor. İkisi de doğru; resmi mağaza kaydı esas alınır, gerekirse
ikisi birlikte yazılır ("DICE'ın başını çektiği Battlefield Studios").

**Sezon içeriği yazılmaz.** Sezon adı ve o sezonun haritaları yazılırsa sayfa her sezonda eskir.
"Haritalar sezon güncellemeleriyle genişliyor" düzeyinde genel kalınır.

## Doğrulanamayan bilgiyle ne yapılır

Üç adım, sırayla:

1. İçeriğe yazma. Cümleyi ya da bölümü çıkar.
2. Kullanıcıya sohbette söyle: hangi bilgi, neden doğrulanamadı, hangi kaynaklara bakıldı.
3. Kullanıcı elle veri verirse ekle; vermezse alan kalıcı olarak boş kalır.

Bu, sayfanın en kolay kaybedeceği şeyin güven olmasından kaynaklanıyor. Tek bir yanlış GB değeri
ya da olmayan bir Türkçe desteği vaadi, sayfanın tamamını şüpheli hale getiriyor.
