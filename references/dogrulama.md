# Doğrulama: hangi bilgi hangi kaynaktan

Oyun verisi hızla eskiyor ve elimizdeki kaynaklar birbiriyle çelişebiliyor. Her sayı için
aşağıdaki sıra izlenir. Üstteki kaynak alttakini ezer.

## Kaynak sırası

| Bilgi | Birincil kaynak | İkincil | Not |
|---|---|---|---|
| Sistem gereksinimleri | Steam `appdetails` (`pc_requirements`) | EA / yayıncı sayfası | Steam Türkçe çeviriyle döner, doğrudan kullanılabilir |
| Kurulum boyutu | Steam gereksinimleri (min ve önerilen ayrı) | - | Minimum ve önerilen farklıysa ikisi de yazılır |
| Resmi dil desteği | Steam `supported_languages` | PlayStation destek sayfası | Türkçe listede yoksa **yok** demektir; topluluk yaması resmi destek sayılmaz |
| Metacritic puanı | metacritic.com platform dökümündeki **PC** satırı | Steam `metacritic` alanı (zaten PC) | Sayfa başlığındaki puan PC'ninki olmayabilir |
| Hikâye modu süresi | HowLongToBeat | Oyun basını (GamesRadar, IGN) | İki bağımsız kaynak örtüşmüyorsa süre yazılmaz |
| GFN paket ve sunucu değerleri | `gameplus.com.tr/gfn/paketler` | - | **Tek geçerli kaynak budur** |
| GFN'de var mı | GFN oyun kataloğu (`katalog.py`) | nvidia.com GFN sayfası | Optimizasyon durumu iç bilgidir, içeriğe yazılmaz |
| Hangi mağazadan oynanabilir | Katalogdaki `Mağazalar` / `variants` alanı | - | Oyun başka mağazada satılsa da GFN o kopyayı açmıyor olabilir |
| Oyunun modları, hikâyesi, mekanikleri | Markanın kendi blog yazısı | Yayıncı sayfası | Blog varsa önce o okunur, ton ve terim tutarlılığı için |
| Çıkış tarihi | Katalog + Steam | - | GFN yayın tarihi ile mağaza satış tarihi farklı olabilir |
| Ödüller ve adaylıklar | Törenin resmi kazanan listesi | Wikipedia oyun sayfası `Awards` bölümü | "Aday gösterildi" ile "kazandı" ayrımı tek tek kontrol edilir |
| Besteci, müzik ve ses tasarımı | Wikipedia oyun sayfası `Music` bölümü | Oyun basını röportajları | Skoru besteleyen ile parçaları veren grup farklı olabilir |
| Hikâye kurulumu ve geçtiği yerler | Wikipedia oyun sayfası `Plot` bölümü | Yayıncı sayfası | Yalnız kurulum ve mekânlar alınır, olay örgüsü alınmaz |
| Sınıf, mod ve mekanik tanımları | Wikipedia `Gameplay` bölümü + yayıncı sayfası | Markanın blog yazısı | Silah tipleri Türkçeye çevrilirken karıştırılmaya açık (bkz. tuzaklar) |

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

**Her şey PC sürümünden alınır.** GeForce NOW oyunun PC sürümünü akıttığı için sayfanın anlattığı
sürüm de PC sürümüdür. Puan, sistem gereksinimleri, kurulum boyutu, dil listesi ve sürüm farkı taşıyan
her değer PC sütunundan okunur; konsol değeri yazılmaz. Sayfada tek bir sürüm anlatılmazsa okuyucu
kendi kurulumuyla eşleşmeyen bir sayıya bakmış oluyor.

**Metacritic'in tek bir puanı yoktur.** Oyun sayfasının üstündeki puan varsayılan platformunkidir;
platform dökümü sağda ayrı durur. Battlefield 6'da sayfa başlığındaki puan 83/100 (71 eleştirmen)
iken **PC puanı 82/100 (64 eleştirmen)**, PS5 83, Xbox Series X 84. Yazılan değer PC'ninkidir ve Not
bölümünde hangi platforma ait olduğu belirtilir. Steam'in `metacritic` alanı zaten PC puanını döndürür,
hızlı teyit için kullanılabilir.

**Kullanıcı skoru platform bazında ayrışmaz.** Metacritic oyuncu puanını tüm platformlar için tek
sayı olarak verir. Yazılırsa bu not düşülür, "PC kullanıcı skoru" diye sunulmaz.

**Silah sınıfı adları Türkçeye çevrilirken kayıyor.** SMG "makineli tabanca", LMG "hafif makineli
tüfek"tir; ikisi de "hafif makineli" diye yazılırsa iki sınıf aynı silahı kullanıyor görünür.
Sınıf açıklaması yazmadan önce hangi sınıfın hangi silah ailesini kullandığı kaynaktan teyit edilir.

**Birlik, karakter ve yer adları birebir aktarılır.** Battlefield 6'nın timi "Dagger 1-3"tür,
"Dagger 13" değil. Kulaktan yazılan özel ad, doğrulanmamış sayı kadar hızlı güven kaybettiriyor.

**Katalogdaki `sortName` alanı oyun adı değildir.** Sıralama anahtarıdır ve bir bölümü sıra numarası
taşır (`counter_strike_4`, `fallout_03a`). Aratılacak ad `title` alanından üretilir.

**Steam'in geliştirici alanı katalogdan farklı olabilir.** Battlefield 6'da Steam "Battlefield Studios",
katalog "Electronic Arts DICE" diyor. İkisi de doğru; resmi mağaza kaydı esas alınır, gerekirse
ikisi birlikte yazılır ("DICE'ın başını çektiği Battlefield Studios").

**Mağaza listesi katalogdan gelir, mağazadan değil.** Battlefield 6 Epic Games Store'da da satılıyor,
ama GFN kataloğunda yalnız EA App ve Steam variantları var; Epic'ten alınan kopya GeForce NOW'da
açılmıyor. "Şu mağazada da var" bilgisi oyunun satıldığı yerden değil, **katalogdaki variants
alanından** okunur. Yanlış mağaza yazmak, okuyucunun oynayamayacağı bir kopyayı satın almasına yol açar.

**GFN optimizasyon durumu içeriğe yazılmaz.** Katalogdaki "Tam optimize / Tam optimize değil" alanı
iç bilgidir; okuyucuya bir şey ifade etmiyor ve NVIDIA bu durumu sessizce değiştirebiliyor.

**Sezon içeriği yazılmaz.** Sezon adı ve o sezonun haritaları yazılırsa sayfa her sezonda eskir.
"Haritalar sezon güncellemeleriyle genişliyor" düzeyinde genel kalınır.

**Katalogdaki ad, insanların arattığı ad olmayabilir.** Katalog kelimesi NVIDIA'nın uzun adından
üretildiği için bazen neredeyse hiç aranmaz: "mount and blade 2 bannerlord" ayda 297 iken "bannerlord"
33.100; "tom clancys rainbow six siege x" ayda 4 iken "rainbow six siege" 8.100. Main KW belirlenmeden
önce adın kısa ve yaygın biçimleri hacim aracında yan yana ölçülür, en çok aranan oyun biçimi seçilir,
katalog adının hacmi DİKKAT satırında not edilir. Tek kelimelik ya da kısaltma adlar ("rust", "wow",
"r6") başka anlamlar da taşır: SERP'te ilk sonuçların oyuna ait olduğu görülmeden ana kelime yapılmaz;
ikincil kelimeye alınırsa hacmin bir kısmının başka anlamlara gittiği DİKKAT'e yazılır.

**Canlı servis oyunlarında mod, ad ve erişim modeli değişir.** Rainbow Six Siege'in "Siege X" adı
Mart 2026'da bırakıldı, 6'ya 6 Dual Front modu Haziran 2026'da kaldırıldı; Overwatch 2 adı Şubat
2026'da Overwatch'a döndü. Wikipedia ve katalog bu değişikliklerin gerisinde kalabiliyor. Çok oyunculu
ve ücretsiz oyunlarda mod listesi, ücretsiz erişimin kapsamı ve oyunun güncel adı yayıncının son sezon
sayfasından ya da resmi haberinden teyit edilir; kaldırılmış bir mod anlatılırsa sayfa ilk günden eskir.

**DLC'nin sistem gereksinimi ana oyundan ayrı olabilir.** Bannerlord'un War Sails genişlemesi önerilen
donanımı i5-13600K ve RTX 3060'a çıkarıyor, 35 GB ek alan istiyor. Gereksinim tablosu yazılırken
Steam'de DLC'nin kendi kaydı da okunur (`appdetails` içindeki `dlc` listesi); fark varsa tabloya ayrı
satır olarak girer. Bu, bulutta oynamanın faydasını somut gösteren bir veri de olur.

**Türkçe arayüzü olan oyunda özel adlar yerelleştirmedeki yazımla geçer.** Bannerlord'da "Calradia"
Türkçe sürümde Kalradya, "Khuzait" Kuzait Hanlığı'dır. Okuyucu oyunu Türkçe oynuyorsa adı o biçimde
tanır. Türkçe Vikipedi'nin seçkin maddeleri bu yazımı ve Türkiye bağlamını (stüdyo, yerel yayın)
çoğu zaman İngilizce sayfadan daha ayrıntılı taşır; İngilizce sayfayla çelişen sayı varsa (Warband'den
kaç yıl önce geçtiği gibi) sayı yazılmaz.

**Metacritic PC puanı betikle okunur.** `python3 scripts/metacritic_pc.py <slug>` PC eleştirmen
sayfasından tüm platformların puanını ve eleştirmen sayısını döker. Wikipedia'daki puan kutusu çıkış
dönemine aittir ve eleştirmen sayısı taşımaz; yalnız yedek kaynaktır.

## Doğrulanamayan bilgiyle ne yapılır

Üç adım, sırayla:

1. İçeriğe yazma. Cümleyi ya da bölümü çıkar.
2. Kullanıcıya sohbette söyle: hangi bilgi, neden doğrulanamadı, hangi kaynaklara bakıldı.
3. Kullanıcı elle veri verirse ekle; vermezse alan kalıcı olarak boş kalır.

Bu, sayfanın en kolay kaybedeceği şeyin güven olmasından kaynaklanıyor. Tek bir yanlış GB değeri
ya da olmayan bir Türkçe desteği vaadi, sayfanın tamamını şüpheli hale getiriyor.
