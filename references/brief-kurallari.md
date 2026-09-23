# Brief Excel'i: sütunlar ve kurallar

Brief, oyun başına **tek satır** olarak ortak Excel'e eklenir. Dosya adı
`GeForce NOW oyun detay sayfası içerik briefleri.xlsx`, sekme `Oyun Detay Briefleri`.

## Düzen

Tablo başlığı **1. satırda**, veri **2. satırdan** başlar. Üstte başlık ya da not bloğu yoktur,
birleştirilmiş hücre kullanılmaz, dondurma A2'dedir. Başlık satırı Calibri 11 kalın beyaz `#434343`
dolgulu; gövde Calibri 10 `#10332F`, sola ve dikeyde ortalı, kaydırmalı. Sütun genişlikleri sırayla
22, 20, 12, 38, 48, 134, 72, 66, 58.

`scripts/brief_satiri.py` bu biçimi kendisi kuruyor; elle hücre biçimlendirmeye gerek yok.

## Sütunlar

**Oyun Adı** - katalogdaki başlık, marka sembolleri temizlenmiş hali.

**Main KW** - oyunun aranan adı, küçük harfle. Katalogdaki "Aratılacak oyun adı" alanı.

**Main KW Hacim** - 12 aylık ortalama aylık arama, `#,##0` biçiminde sayı olarak.

**İkincil Kelimeler** - aynı hücrede alt alta, `kelime (hacim)` biçiminde, hacme göre azalan.
Seçim ölçütü: sayfanın gerçekten karşılayabileceği niyet. Erişim, oynanış, mod, içerik ve teknik
sorular alınır. Fiyat, satın alma, platform (ps5/xbox), anahtar/key, yama gibi kelimeler mağaza ve
üçüncü taraf sayfalarının alanıdır, alınmaz. Hacim verisi olmayan ama hedeflenen kelime `(-)` ile yazılır.

**Alt Başlıklar** - `H2: Başlık` ve gerekiyorsa `H3: Başlık` satırları. Sayı 1200-1500 kelimeye göre
belirlenir: 7-9 H2 ve az sayıda H3. Hikâye, oynanış, atmosfer-ses ve öne çıkan özellikler kendi
H2'lerini alır; bölüm başına 130-180 kelime düşer. Oyunun yapısı bir bölümü karşılamıyorsa (hikâyesi
olmayan çok oyunculu bir oyun gibi) o başlık açılmaz, yerine oyunun gerçekten sahip olduğu konu gelir.
Başlık en fazla iki konu taşır.

**Sıra sabittir: oyun önce, GeForce NOW sonra.** Oyuna ait başlıklar (hikâye, oynanış, atmosfer, öne
çıkan özellikler) baştan verilir; bulutla ilgili her şey tek bir H2'de toplanır ve sona yakın durur:

```
H2: {Oyun} GeForce NOW'da Nasıl Oynanır?
H3: {Oyun}'ı GAME+ ile Oynamak
H3: Bağlantı Hızı ve Görüntü Kalitesi
H2: {Oyun} Sistem Gereksinimleri ve İndirme
H2: {Oyun} Ücretsiz mi, Nasıl Başlanır?
```

Başta ayrı bir erişim H2'si ve sonda ayrı bir "GeForce NOW ile {Oyun} Deneyimi" H2'si açılmaz; iki
başlık da aynı üç cümleyi (kütüphanede yer alır, hesabını bağla, indirme ve donanım derdi yok)
tekrarlıyordu. Gerekçenin tamamı `icerik-kurallari.md`'deki Yapı bölümünde.

**İçerik Kurgusu** - şu sırayla yazılır:

```
TON: Sayfanın kime, hangi beklentiyle yazıldığı; hitap baştan sona "sen" (birinci çoğul yok).

AÇILIŞ: Gövde başlıksız 1-2 paragraflık girişle açılır; oyunu genel olarak tanıtır, puanlar madde listesiyle verilir, resmi dil desteği tek cümleyle belirtilir. Sayfada H1 bulunduğu için bu girişe başlık konmaz.

H2 · Başlık: Bu bölümde ne anlatılır, hangi kelime nerede karşılanır, hangi biçim kullanılır.
H2 · Başlık: ...
H2 · {Oyun} GeForce NOW'da Nasıl Oynanır: Erişim yanıtı (kütüphane, mağaza hesabı, indirme boyutu) ve bulutun kazandırdıkları tek bölümde; cihaz çeşitliliği ve kontrol desteği (gamepad / dokunmatik / direksiyon / kısmi).
H3 · GAME+ ile Oynamak: Hangi hesapla açıldığı, satın alma durumu; paketlerin sunduğu değerler anlatılır, gereken paket yazılmaz.
H3 · Bağlantı Hızı ve Görüntü Kalitesi: 15 Mbps 1080p/30, 35 Mbps 1440p/60, 50 Mbps 4K/60 FPS tablosu; oyunun HDR / RTX / NVIDIA Reflex desteği.

SSS: Sayfanın ayrı modülünde yer alır ve gövde kelime sayısına dahil değildir.

BİÇİM: Sınıflar, modlar, puanlar ve öne çıkan özellikler madde listesiyle; teknik değer kümeleri tabloyla verilir. Önemli terim ve değerler kalın yazılır. Hikâye, atmosfer-ses-müzik ve öne çıkan özellikler kendi bölümlerini alır; hikâyeden spoiler verilmeden bahsedilir. Son bölümün ardından kısa bir kapanış çağrısı gelir; kapanışta oyunu oynamak için GeForce NOW Ultimate ya da Performance paketlerinden birinin seçilebileceğini söyleyen bir iki cümlelik satın alma çağrısı bulunur, fiyat ve paket özelliği yazılmaz.
UZUNLUK: Ortalama 1200-1500 kelime gövde. Paragraf en fazla 3-4 cümle; teknik değerler rakamla.
DİKKAT: Yazılmayacaklar, doğrulanacaklar, hacim uyarısı.
```

Başlıkların yanına kelime sayısı yazılmaz. Koşullu bir uyarı varsa (Türkçe desteği gibi) DİKKAT'in
sonuna kalın yazılır; `brief_satiri.py` bunu `kurgu_kalin` alanıyla basar.

**Kurgu hücresi yaklaşık 30 satıra sığmalıdır.** Excel satır yüksekliği en fazla 409 punto; İçerik
Kurgusu sütununda (genişlik 134) bu yaklaşık 30 satır metin eder, fazlası hücrede görünmez kalır.
`brief_satiri.py` taşan satırda uyarı verir. Kurgu satırları bu yüzden telgraf üslubuyla yazılır:
ne anlatılacağı, hangi kelimenin nerede karşılanacağı ve doğrulanmış değerler; açıklayıcı cümle
kurulmaz. Telgraf üslubu mecaza izin vermez: kurgu satırındaki ifade içeriğe çoğu zaman olduğu gibi
geçiyor. "32 GB RAM şartının bulutta cihaza yüklenmediği" yazılırsa içerikte de "bu şart cihazına
yüklenmez" cümlesi çıkıyor; doğrusu "32 GB RAM'in bulutta oyuncunun cihazında aranmadığı". H2 başına 1-2 ekran satırı hedeflenir. Toplu brief
hazırlanırken ortak satırlar (TON, GeForce NOW H2 ve H3'leri, BİÇİM, UZUNLUK) tek yerden üretilir,
oyuna özgü satırlar ayrı yazılır.

**Link Verilecek Sayfalar** - numaralı liste, her link iki satır:

```
1. anchor metni : https://gameplus.com.tr/...
   H2 · Bölüm adı bölümünde, hangi cümlede.
```

Anchor, insanların arattığı terimin kendisidir ("FPS oyunları", "en iyi battle royale oyunları").
Tam URL yazılır. Linkin yerleşeceği satırda, anchor'ın hangi cümlenin içinde geçeceği belirtilir;
link taşımak için ayrı cümle kurulmaz. Seçim ve yerleştirme kuralları `ic-link-haritasi.md`'de.

**SSS'ler** - numaralı soru, altında `Yanıtta:` satırı. Sorular Google'ın "Bunlar da sorulmuş"
kutusundan ve arama önerilerinden gelir; uydurulmaz. 8-10 soru yeterli. Yanıtları içerik ekibi yazar,
brief yalnız soruyu ve yanıtta geçmesi gerekeni verir. **"{Oyun} Türkçe mi?" sorusu her briefte yer alır**;
resmi destek yoksa yanıt notu "resmi Türkçe desteği olmadığı" olur. Sorular kullanıcının arattığı
biçimde ve doğal sözdizimiyle yazılır: "kaçta çıktı" değil "ne zaman çıktı", "ne oyunu" değil "nasıl bir
oyun", "bilgisayarımı kaldırır mı" değil "Bilgisayarım X'i kaldırır mı", "neyin devamı" değil "hangi serinin
devamı". Arama ifadesi kısa olsa da sayfadaki soru anlamlı ve tam kurulur. Sayfanın konusu dışına düşen
sorular ("mobil sürüm neden kapandı") GeForce NOW'a bağlanan karşılığıyla değiştirilir ("telefonda
oynanır mı"). Tarihe bağlı notlar da zamandan bağımsız yazılır ("çıkınca güncellenir" türü not bırakılmaz).

**Yanıt Biçimi** - oyunlar arasında değişmeyen, kullanıcının onayladığı metin:

```
• Her yanıt ort. 20-60 kelimedir. (Max 60, minimum değer de olabilir)
• İlk cümle soruyu doğrudan yanıtlar (evet, hayır ya da net değer); gerekçe ikinci cümlede verilir.
• Yanıt kendi başına okunur; "yukarıda belirtildiği gibi" türünde gönderme yapılmaz.
• Sayısal değer varsa yanıtta rakamla geçer (GB, saat, Mbps, çözünürlük).
• Oyun adı yanıtta en az bir kez tam haliyle geçer.
• Gövde metnindeki cümleler birebir tekrarlanmaz, SSS kısmında daha net ve direkt answer first odaklı ilerlenmelidir.
• Doğrulanamayan bilgi yazılmaz; yanıtlanamayan soru listeden çıkarılır.
```

Bu metin olduğu gibi kopyalanır. FAQPage schema maddesi ekip tarafından çıkarıldı, geri eklenmez.

## Briefe girmeyenler

Sayfa künyesi ve katalog verisi (yayıncı, geliştirici, yaş sınırı, mağaza bağlantısı) briefe
yazılmaz. Bunlar sayfanın künye tablosundan gelir; brief içerik planıdır.

**Teknoloji bayrakları bunun istisnasıdır.** HDR, RTX ve NVIDIA Reflex desteği gövdede anlatıldığı
için briefte de yer alır: bağlantı hızı H3'ünün satırına, katalog JSON'undaki variant bayraklarından
(`HDR_ENABLED`, `RTX_ENABLED`, `REFLEX_ENABLED`) okunarak yazılır. Oyunda bu bayraklardan hiçbiri
yoksa satır "katalogda HDR, RTX ve Reflex desteği görünmüyor; bu teknolojilerden söz edilmez" diye
kapanır, böylece içerik ekibi olmayan desteği uydurmaz.
