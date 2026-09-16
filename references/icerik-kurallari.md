# İçerik yazımı: yapı, ton ve bölüm kalıpları

## Ton

Bu sayfa tüketiciye dönük ürün içeriğidir, rapor değil. Marka sesi: **"sen" dili, geniş zaman,
somut değerler**. İçerik Dili Rehberi bu çıktıya uygulanmaz; o rehber müşteriye giden rapor,
sunum ve audit dosyaları içindir.

Okuyucu ya oyunu tanıyor ve GeForce NOW üzerinden oynayıp oynayamayacağını merak ediyor, ya da
oyunu yeni duymuş ve ne olduğuna bakıyor. Her iki durumda da beklediği şey hızlı cevap. Bu yüzden
**her H2'nin ilk cümlesi o başlığın sorusunu doğrudan yanıtlar**, açıklama sonra gelir. Yapay zeka
yanıtlarında alıntılanabilirlik de buna bağlı: alıntılanan şey neredeyse her zaman bölümün ilk cümlesi.

Sayfa oyunun **PC sürümünü** anlatır; GeForce NOW akışa aldığı sürüm budur. Puan, gereksinim ve boyut değerleri PC'ninkidir, puan yazılırken de bu belirtilir ("Metacritic PC puanı").

Sıfatla değil değerle anlatılır. "Muhteşem grafikler" yerine "4K HDR akış", "çok hızlı" yerine
"30 milisaniyenin altında gecikme".

## Zaman kipi

Metnin tamamını şimdiki zamanla ("açılıyor", "sunuyor", "gerekiyor") yazmak, sayfayı tek düze ve
anlık bir habere benzetiyor. Genel geçer bilgiler **geniş zamanla** yazılır: "oyun kütüphanede yer
alır", "indirme gerekmez", "Reflex gecikmeyi düşürür", "REDSEC ücretsiz oynanır". Bunlar her zaman
doğru olan şeyler, geniş zaman onları kalıcı bir tanım gibi okutuyor.

Şimdiki zaman, gerçekten süregelen ve değişmekte olan durumlar için saklanır: "haritalar sezon
güncellemeleriyle genişlemeye devam ediyor", "oyun zaman içinde büyüyor". Okuyucunun yaptığı işler
ikinci tekil geniş zamanla verilir: "oynamaya başlarsın", "REDSEC'e girebilirsin", "Oynat'a bastığın
anda savaş alanına girersin".

Pratik ölçü: gövdedeki `-iyor` çekimlerini say. Battlefield 6 metninde 60'tan 3'e indi ve kalan üçü
de gerçekten süregelen durumları anlatıyor. Bu oran iyi bir hedef.

## Yapı

Gövde, **başlıksız kısa bir girişle açılır**: oyunu genel olarak tanıtan bir ya da iki paragraf.
Sayfada H1 zaten oyun adı olduğu için bu girişe başlık konmaz, doğrudan metin gelir. Giriş oyunun ne
olduğunu, kim yaptığını, ne zaman çıktığını ve seri içindeki yerini söyler; erişim ve "nasıl oynanır"
anlatısı girişte değil, ilk H2'de başlar. Böylece oyunu tanımayan okuyucu da sayfaya bir yerden giriyor.

Ortalama **750-850 kelime**, 5-6 H2. Bölüm başına düşen 120-150 kelime, bir konuyu gerçekten
anlatmaya yetiyor; daha fazla başlık koyarsan her bölüm madde listesine dönüşüyor. Madde listeleri
paragraftan hızlı okunduğu için listeli metinlerde bandın üst ucuna yaklaşmak sorun değil.

Tipik iskelet (oyuna göre değişir):

0. **Giriş (başlıksız, 1-2 paragraf)** - birinci paragraf oyunun ne olduğunu, kimin yaptığını, ne
   zaman çıktığını ve seri içindeki yerini söyler. İkinci paragraf oyunun kapsamını (çok oyunculu +
   tek oyunculu) verir, puanları **madde listesiyle** yazar ve resmi dil desteğini tek cümleyle
   belirtir.
1. **{Oyun} GeForce NOW'da Nasıl Oynanır?** - yalnız erişim yanıtı: oyun kütüphanede mi, hangi mağaza
   hesabıyla bağlanıyor, kurulum gerekiyor mu, ücretsiz mod varsa şartı ne. Künye bilgisi girişte
   verildiği için burada tekrarlanmaz.
2. **{Oyun} Oynanışı ve Oyun Modları** - mekanikler, sınıflar, modlar, atmosfer ve müzik, tek oyunculu taraf.
3. **GeForce NOW ile {Oyun} Deneyimi** - bulutun ne değiştirdiği, cihaz çeşitliliği, bağlantı hızı tablosu.
4. **{Oyun} Sistem Gereksinimleri ve İndirme** - PC gereksinimleri tablosu, ardından bulut karşıtlığı.
5. **{Oyun} Ücretsiz mi, Nasıl Başlanır?** - erişim modeli + numaralı başlama adımları.

Türkçe dil desteği yalnız **resmi ve modsuz** destek varsa kendi H2'sini alır. Destek yoksa ayrı
bölüm açılmaz, birinci bölümde tek cümleyle belirtilir. Okuyucunun bunu öğrenmek için sayfayı
taraması gerekmemeli.

## Madde listesi kullanımı

Sayılabilir ve paralel yapıdaki şeyler paragrafa gömülmez, **madde listesiyle** verilir: sınıflar,
oyun modları, puanlar, adımlar, paket farkları. Dört sınıfı tek paragrafta noktalı virgülle sıralamak
okuyucuyu aradığını taramaya zorluyor; liste hem hızlı okunuyor hem de yapay zeka yanıtlarında
bütün olarak alınabiliyor.

Biçim: `Ad: tek cümlelik tanım.` Madde başına bir fikir, 10-20 kelime. Liste öncesinde onu tanıtan
kısa bir cümle bulunur ("Serinin dört klasik sınıfı geri döndü:"). İki maddelik liste yapılmaz,
altı maddeyi geçen liste bölünür.

Numaralı liste yalnız **sıralı adımlar** için kullanılır (başlama adımları). Sıra taşımayan her şey
madde imli listedir. `icerik_docx.py` içinde numaralı liste `li`, madde imli liste `mad` tipidir.

## Atmosfer, müzik ve ödüller

Teknik anlatım tek başına oyunun neye benzediğini anlatmıyor. Oynanış bölümünün sonunda, oyunun
**tonu, sanat tasarımı, müziği ve aldığı ödüller** kısa bir paragrafta toplanır. Sıfat yığmadan,
somut örnekle: "yıkılan binanın tozu, çatışma ilerledikçe değişen harita silueti ve sesin geldiği yön"
gibi. Besteci adı yazılır, ödül adı ve yılı tam verilir, kazanılan ödül ile adaylık ayrı ayrı belirtilir.

Ödül yoksa bölüm zorlanmaz; ton ve sanat tasarımı tek cümleyle geçilir. Uydurma ödül ya da
"övgü topladı" gibi kaynaksız genelleme yazılmaz.

## Hikâyeden spoiler vermeden bahsetmek

Hikâye modu olan oyunlarda okuyucu "ne anlatıyor ve ne kadar sürüyor" sorusunun yanıtını bekliyor;
olay örgüsünü değil. Yazılabilecekler: kurulum (hangi yıl, hangi çatışma, kime karşı), oynadığın
birlik, bölümlerin geçtiği yerler, anlatı biçimi, HowLongToBeat süresi.

Yazılmayacaklar: dönüm noktaları, kimin öldüğü, sonun nasıl bağlandığı, karakterlerin kimliğine dair
açığa çıkan bilgiler. Ölçü şu: cümleyi oyunu oynamamış biri okuduğunda merakı artmalı, kapanmamalı.

## Tablo kullanımı

Teknik değer kümeleri paragrafa gömülmez, tabloyla verilir. İki tipik tablo:

**Bağlantı hızı** - sayfadaki hız bloğuyla tutarlı: 15 Mbps / 1080p / 30 FPS, 35 Mbps / 1440p /
60 FPS, 50 Mbps / 4K / 60 FPS.

**Sistem gereksinimleri** - Steam'den alınan minimum ve önerilen sütunlarıyla: işletim sistemi,
işlemci, bellek, ekran kartı, depolama. Tam tablo yerine bu beş satır yeterli; ayrıntı için blog
yazısına link verilir.

## Bölüm bölüm ne yazılır

**Erişim bölümü.** İlk iki cümle: oyun kütüphanede mi, kurulum gerekiyor mu, hangi mağaza hesabıyla
bağlanıyor. Sonra oyunun ne olduğu tek cümlede. Ardından stüdyo, çıkış tarihi, Metacritic puanı ve
resmi dil desteği. Uzun giriş yazılmaz.

**Oynanış bölümü.** Oyunun kendi terimleriyle anlatılır (sistem adları, sınıf adları, mod adları
İngilizce kalır). Sınıflar ve modlar madde listesiyle verilir; bölümün sonunda ton, sanat tasarımı,
müzik ve ödüller kısa bir paragrafta toplanır. Tek oyunculu taraftan **"kampanya" diye bahsedilmez**; "hikâye modu", "campaign"
ya da oyunun kendi adı kullanılır. Sebebi kampanya kelimesinin promosyon kampanyasıyla karışması.
Hikâye süresi doğrulanabiliyorsa kaynağıyla yazılır.

**GeForce NOW bölümü.** Sayfanın ayrıştığı yer. Bulutun somut olarak ne değiştirdiği: indirme ve
güncelleme beklememek, donanım gerekmemesi, aynı kütüphanenin telefonda, Mac'te ve televizyonda
açılması, gecikme. Paketlerin ne sunduğu anlatılabilir; **"bu oyun için X paketi gerekir" denmez.**

**Sistem gereksinimleri bölümü.** Karşıtlık üzerine kurulur: PC tarafında ne gerekiyor, bulutta
bunların hiçbiri gerekmiyor. "Bilgisayarım kaldırır mı" sorusu burada karşılanır.

**Kapanış bölümü.** Erişim modeli (ücretsiz mod var mı, tam sürüm nasıl alınır) ve 3-4 maddelik
numaralı başlama adımları. Adımlar sayfadaki Oynat çağrısına bağlanır.

## SSS yanıtları

Brief'teki yanıt biçimi kuralları geçerli: 20-60 kelime, ilk cümle doğrudan yanıt, kendi başına
okunur, sayılar rakamla, oyun adı tam haliyle bir kez.

Gövdedeki cümleler birebir tekrarlanmaz. SSS daha kısa ve daha keskin yazılır; gövde anlatır,
SSS cevaplar.

Yanıtlanamayan soru listeden çıkarılır. Örneğin resmi Türkçe desteği yoksa "Türkçe mi?" sorusu
SSS'de yer almaz, bilgi gövdede tek cümleyle geçer.

## Yazarken kaçınılacaklar

- Fiyat, indirim, kampanya bilgisi ve sezon adı: hepsi sayfayı eskitir.
- Eleştirmen alıntısı ve uzun puan dökümü: Metacritic tek sayı olarak yeterli.
- Doğrulanmamış süre, boyut ve oyuncu sayısı.
- Marka sembolleri (® ™), emoji, uzun tire.
- "Geforce Now" yazımı; doğrusu GeForce NOW.
