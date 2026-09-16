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

**Alt Başlıklar** - `H2: Başlık` ve gerekiyorsa `H3: Başlık` satırları. Sayı 750-800 kelimeye göre
belirlenir: 5-6 H2, H3'e girilmez ya da en çok bir iki tane. Fazla başlık, her bölümü 80 kelimeye
düşürüp metni listeye çeviriyor. İlişkili konular tek H2'de birleştirilir (modlar + battle royale +
hikâye modu gibi).

**İçerik Kurgusu** - şu sırayla yazılır:

```
TON: Sayfanın kime, hangi beklentiyle yazıldığı.

AÇILIŞ: Gövde başlıksız 1-2 paragraflık girişle açılır; oyunu genel olarak tanıtır, puanlar madde listesiyle verilir, resmi dil desteği tek cümleyle belirtilir. Sayfada H1 bulunduğu için bu girişe başlık konmaz.

H2 · Başlık: Bu bölümde ne anlatılır, hangi kelime nerede karşılanır, hangi biçim kullanılır.
H2 · Başlık: ...

SSS: Sayfanın ayrı modülünde yer alır ve gövde kelime sayısına dahil değildir.

BİÇİM: Sınıflar, modlar ve puanlar madde listesiyle; teknik değer kümeleri tabloyla verilir. Oynanış bölümünün sonunda oyunun tonu, sanat tasarımı, müziği ve ödülleri kısa bir paragrafta toplanır. Hikâyeden spoiler verilmeden bahsedilir.
UZUNLUK: Ortalama 750-850 kelime gövde. Paragraf en fazla 3-4 cümle; teknik değerler rakamla.
DİKKAT: Yazılmayacaklar, doğrulanacaklar, hacim uyarısı.
```

Başlıkların yanına kelime sayısı yazılmaz. Koşullu bir uyarı varsa (Türkçe desteği gibi) DİKKAT'in
sonuna kalın yazılır; `brief_satiri.py` bunu `kurgu_kalin` alanıyla basar.

**Link Verilecek Sayfalar** - numaralı liste, her link iki satır:

```
1. anchor metni : https://gameplus.com.tr/...
   H2 · Bölüm adı bölümünde, hangi cümlede.
```

Anchor, hedef sayfanın kendi kelimesidir. Tam URL yazılır. Seçim kuralları
`ic-link-haritasi.md`'de.

**SSS'ler** - numaralı soru, altında `Yanıtta:` satırı. Sorular Google'ın "Bunlar da sorulmuş"
kutusundan ve arama önerilerinden gelir; uydurulmaz. 8-10 soru yeterli. Yanıtları içerik ekibi yazar,
brief yalnız soruyu ve yanıtta geçmesi gerekeni verir.

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

Sayfa künyesi ve katalog verisi (yayıncı, geliştirici, yaş sınırı, RTX/HDR, mağaza bağlantısı)
briefe yazılmaz. Bunlar sayfanın künye tablosundan gelir; brief içerik planıdır.
