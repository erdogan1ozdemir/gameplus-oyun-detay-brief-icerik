---
name: gameplus-oyun-detay-brief-icerik
description: gameplus.com.tr (GeForce NOW powered by GAME+ Türkiye) oyun detay sayfaları için içerik briefi ve sayfa içeriği üretir. Brief, oyun başına tek satır olarak ortak Excel'e eklenir (Main KW ve hacim, ikincil kelimeler, alt başlıklar, içerik kurgusu, iç linkler, PAA kaynaklı SSS soruları, yanıt biçimi); içerik 750-850 kelimelik Türkçe gövde (başlıksız kısa giriş + H2 bölümleri) ve 20-60 kelimelik answer-first SSS yanıtlarından oluşur. Şu durumlarda mutlaka kullan: kullanıcı bir oyun adı verip "detay sayfası briefi", "oyun briefi", "oyun sayfası içeriği", "bu oyun için içerik yaz", "brief hazırla" dediğinde · GFN kütüphanesindeki bir oyun için SEO içeriği, alt başlık planı, SSS ya da anahtar kelime seti istendiğinde · var olan bir oyun briefini revize etmek ya da Excel'e yeni oyun satırı eklemek istendiğinde · kullanıcı yalnız oyun adı yazıp içerik beklediğinde. Kategori sayfaları (gfn/oyunlar/*) için gameplus-category-content, blog yazıları için gameplus-blog-enrich-v2 kullanılır; bu skill yalnız tek oyunluk detay sayfaları içindir.
---

# Gameplus Oyun Detay Sayfası: Brief ve İçerik

Bu skill, GeForce NOW kütüphanesindeki bir oyun için **iki çıktı** üretir:

1. **Brief satırı** - ortak Excel'e eklenen tek satır (dokuz sütun).
2. **Sayfa içeriği** - Word dosyası olarak gövde metni ve SSS yanıtları.

İkisi ayrı ayrı da istenebilir. Kullanıcı yalnız "brief" derse içeriği yazma; yalnız "içerik" derse brief satırını atla ama araştırma adımlarını yine de yap, çünkü içerik doğrulanmış veriye dayanır.

Sayfa tipi şu an sitede yok; kurallar sıfırdan üretim için yazılmıştır. Sayfada H1 oyun adı olarak bulunduğundan gövdeye ikinci bir H1 yazılmaz: metin **başlıksız kısa bir girişle** açılır, oyunu bir iki paragrafta tanıtır, ardından H2'ler gelir.

## Ne zaman devreye girer

Kullanıcı bir oyun adı verip brief, içerik, alt başlık planı, SSS ya da kelime seti istediğinde. Oyun adı tek başına yazılmış ve bağlamdan detay sayfası anlaşılıyorsa da tetiklenir.

Kategori sayfası ya da blog yazısı isteniyorsa bu skill değil, ilgili diğer skill kullanılır.

## Çalışma akışı

Beş fazı sırayla yürüt. Faz 1-2 atlanmaz: bu sayfaların tek değeri doğru bilgi vermesi, ve oyun verisi hızla eskiyen bir alan.

### Faz 1 - Katalog kaydını çek

```bash
python3 scripts/katalog.py "Battlefield 6"
```

Oyunun GFN kataloğundaki kaydını verir: aratılacak ad, arama hacmi, türler, yayıncı, mağazalar, GFN optimizasyon durumu, HDR/Reflex/RTX, kontroller, yaş sınıfı, çıkış tarihi, Türkçe etiketler. Bu kayıt briefin iskeletidir ama **tek başına yeterli değildir**; katalog alanları eskiyebiliyor ve bazıları NVIDIA adlandırmasıyla geliyor (bkz. `references/dogrulama.md`).

Katalog Excel'i bulunamazsa kullanıcıdan dosya yolunu iste.

### Faz 2 - Araştır

```bash
python3 scripts/arastirma.py "battlefield 6" --cikti /tmp/oyun.json --steam-appid 2807960
```

Tek çağrıda beş kaynağı toplar: Google SERP ve PAA soruları (Türkiye/Türkçe), uzun kuyruk kelimeler ve aylık hacimleri, Steam mağaza verisi (resmi dil listesi, sistem gereksinimleri, Metacritic, stüdyo), gameplus blog sitemap taraması, Wikipedia oyun sayfası (oynanış, hikâye kurulumu, besteci ve müzik, ödül tablosu).

Steam app id'yi bilmiyorsan parametreyi boş bırak, script oyun adıyla arar. Wikipedia başlığı oyun adından farklıysa `--wiki "Sayfa Başlığı"` ver.

Sayfayı ürün kataloğundan ayıran şey oyunu **anlatması**, bu yüzden teknik veriye ek olarak şunlar da araştırılır: oyunun tonu ve sanat tasarımı, müziği ve bestecisi, aldığı ödüller ile adaylıklar, hikâyenin kurulumu ve geçtiği yerler, sınıf ve mod tanımları. Bunların hepsi metne girmez; girenler kaynağıyla girer.

Bunun üstüne, içerikte kullanacağın her sayı için `references/dogrulama.md`'deki kaynak sırasını izle. Özellikle **hikâye modu süresi, Metacritic puanı (platforma göre değişir), ödül ile adaylık ayrımı ve GAME+ sunucu sınıfı** ayrı ayrı doğrulanır.

### Faz 3 - Briefi kur

`references/brief-kurallari.md` dokuz sütunun her birinin biçimini ve kurallarını anlatır. Özet:

- **Main KW** oyunun adıdır; hacim 12 aylık ortalamadır. Yeni çıkmış oyunlarda bu ortalama çıkış zirvesiyle şişer, son üç ayı da kontrol edip DİKKAT satırına yaz.
- **İkincil kelimeler** erişim ve oynanış niyetini taşıyanlardan seçilir. Fiyat, satın alma, platform ve anahtar (key) kelimeleri mağaza sayfalarının alanıdır, alınmaz.
- **Alt başlıklar** 750-800 kelimeye sığacak sayıda olur: pratikte 5-6 H2, H3'e girilmez ya da çok az girilir. İlişkili konular tek H2'de birleştirilir.
- **İçerik kurgusu** TON, AÇILIŞ, her H2 için bir satır, SSS, UZUNLUK, DİKKAT sırasıyla yazılır. **Başlıkların yanına kelime sayısı yazılmaz.**
- **Linkler** tam URL ile, altında yerleşeceği bölüm belirtilerek verilir. En az 4, yaklaşık 5-6 link. Seçim kuralları `references/ic-link-haritasi.md`'de.
- **SSS** soruları PAA ve arama önerilerinden gelir; yanıtları içerik ekibi yazar, brief yalnız soruyu ve yanıtta geçmesi gerekeni verir.

Satırı eklemek için:

```bash
python3 scripts/brief_satiri.py --xlsx "GeForce NOW oyun detay sayfası içerik briefleri.xlsx" --json /tmp/satir.json
```

### Faz 4 - İçeriği yaz

`references/icerik-kurallari.md` yapıyı, tonu ve bölüm bölüm ne yazılacağını anlatır. Özet:

- Gövde başlıksız 1-2 paragraflık girişle açılır, ardından H2'ler gelir; ortalama 750-850 kelime. Giriş oyunu tanıtır ve puanları madde listesiyle verir; erişim anlatısı ilk H2'de başlar.
- Sayılabilir ve paralel şeyler (sınıflar, modlar, puanlar) madde listesiyle verilir, paragrafa sıkıştırılmaz. Numaralı liste yalnız sıralı adımlar içindir.
- Oynanış bölümünün sonunda oyunun tonu, sanat tasarımı, müziği ve ödülleri kısa bir paragrafta toplanır; kazanılan ödül ile adaylık ayrı yazılır.
- Hikâyeden spoiler verilmeden bahsedilir: kurulum, oynanan birlik, geçtiği yerler ve süre yazılır; olay örgüsü yazılmaz.
- Genel geçer bilgiler geniş zamanla yazılır ("yer alır", "gerekmez"); şimdiki zaman yalnız gerçekten süregelen durumlar için kullanılır. Metnin tamamını `-iyor` ile yazmak sayfayı tek düzeleştiriyor.
- Her H2'nin ilk cümlesi o başlığın sorusunu doğrudan yanıtlar. Yapay zeka yanıtlarında alıntılanabilirlik buna bağlı.
- Ton marka sesidir: "sen" dili, geniş zaman, somut değerler. İçerik Dili Rehberi bu çıktıya uygulanmaz, o rehber müşteriye giden rapor ve sunumlar içindir.
- Teknik değer kümeleri (bağlantı hızı, sistem gereksinimleri) tabloyla verilir, paragrafa gömülmez.
- SSS yanıtları 20-60 kelime, ilk cümle doğrudan yanıt.

Dosyayı üretmek için:

```bash
python3 scripts/icerik_docx.py --json /tmp/icerik.json --out "oyun-adi-icerik.docx"
```

JSON biçimi scriptin başında yazılı. Köprüler `[LINK1]` yer tutucularıyla gövdeye gömülür.

### Faz 5 - Denetle ve teslim et

Teslimden önce `references/kontrol-listesi.md`'yi çalıştır. En sık takılınan yerler: doğrulanmamış sayı, paket gerekliliği ifadesi, "kampanya" kelimesi, uzun tire, çift boşluk.

Çıktıları çalışma klasörüne kaydet ve kullanıcıya gönder. Dosyayı gönderirken **hangi bilgiyi hangi kaynaktan aldığını ve neyi yazmadığını** kısaca söyle; bu sayfalarda en değerli şey, yazılmayanın neden yazılmadığının bilinmesi.

## Değişmeyen kurallar

Bunlar ekip tarafından defalarca düzeltildi, her oyunda geçerli:

- **Hangi GAME+ paketinin gerektiği hiçbir yerde yazılmaz.** Ne başlıkta, ne SSS'de, ne gövdede. Paketlerin ne sunduğu anlatılabilir, "bu oyun için X paketi gerekir" denmez.
- **Tek oyunculu moddan "kampanya" diye bahsedilmez.** "Hikâye modu", "campaign" ya da oyunun kendi kullandığı ad tercih edilir. Sebebi: kampanya kelimesi promosyon kampanyasıyla karışıyor.
- **Türkçe dil desteği yalnız resmi ve modsuz destek varsa bölüm olur.** Destek yoksa ayrı H2 ve SSS sorusu açılmaz, gövdede tek cümleyle belirtilir.
- **Sayfa oyunun PC sürümünü anlatır.** GeForce NOW PC sürümünü akıtıyor; Metacritic puanı, sistem gereksinimleri, kurulum boyutu ve dil listesi PC sütunundan alınır, konsol değeri yazılmaz.
- **Ödül, puan ve özel ad kulaktan yazılmaz.** Kazanılan ödül ile adaylık ayrılır, Metacritic puanının hangi platforma ait olduğu bilinir, birlik ve karakter adları kaynaktaki yazımıyla geçer.
- **Doğrulanamayan sayı yazılmaz.** Sızıntı ve söylenti kaynaklı rakam kullanılmaz; alan boş bırakılır ya da cümle çıkarılır, durum kullanıcıya söylenir.
- **Fiyat, indirim ve kampanya bilgisi yazılmaz**, değiştiğinde sayfa eskir.
- **Benzer niyetli birden fazla yazı varsa yalnız birine link verilir**; `/gfn/sistem-gereksinimleri` sayfasına link verilmez.
- Blogdaki inceleme yazılarıyla içerik örtüşmesi sorun değildir; detay sayfası kalıcı ürün sayfasıdır, blog çıkış dönemi değerlendirmesidir.

## Referanslar

| Dosya | Ne zaman okunur |
|---|---|
| `references/dogrulama.md` | Faz 2'de, her sayıyı yazmadan önce. Bilinen tuzaklar burada. |
| `references/brief-kurallari.md` | Faz 3'te, brief satırını kurarken. |
| `references/icerik-kurallari.md` | Faz 4'te, içeriği yazmadan önce. |
| `references/ic-link-haritasi.md` | Link seçerken. Mevcut sayfa envanteri ve seçim kuralları. |
| `references/kontrol-listesi.md` | Faz 5'te, teslimden önce. |
| `examples/` | Battlefield 6 brief satırı ve içeriği. Yeni oyun yazarken biçim referansı. |
