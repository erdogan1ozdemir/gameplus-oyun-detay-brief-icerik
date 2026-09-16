# İç link seçimi ve yerleşimi

## Link metne sonradan eklenmez, metnin içinden çıkar

En sık yapılan hata, bölümün sonuna "Kütüphanedeki diğer FPS oyunları listesine göz atabilirsin"
gibi bir cümle iliştirip linki oraya koymak. Bu cümle metne bir şey katmıyor, okuyucu onu atlıyor
ve sayfa reklam panosu gibi duruyor.

Doğrusu şu: **önce anchor'ın geçtiği cümlenin metinde zaten bulunması gerekir.** Yoksa o cümle
yazılır, ama linki taşımak için değil, gerçekten bir şey anlattığı için. Battlefield 6 örneği:

| Yerine | Böyle |
|---|---|
| "Kütüphanedeki diğer [FPS oyunları] listesine göz atabilirsin." | "Savaşı merkezine alan [FPS oyunları] arasında en çok rağbet gören çok oyunculu yapımlardan biridir." |
| "Türün diğer yapımlarını merak ediyorsan [en iyi battle royale oyunları] listemize göz atabilirsin." | "Serinin yıkım ve araç mekanikleri burada da geçerli olduğu için REDSEC, [en iyi battle royale oyunları] arasında kendine ayrı bir yer açıyor." |

İkinci sütundaki cümleler link kaldırılsa bile ayakta kalıyor. Ölçü bu: **anchor'ı sil, cümle hâlâ
anlamlı mı?** Değilse cümle linki taşımak için kurulmuş demektir, yeniden yazılır.

## Anchor, aranan terimin kendisi olur

Anchor seçilirken hedef sayfanın adı değil, **insanların gerçekten arattığı terim** esas alınır.
"FPS savaş oyunu" kimsenin aramadığı bir tamlama; "FPS oyunları" ise hem kategori sayfasının konusu
hem de hacmi olan bir kelime. Tür, platform ve tarz kelimeleri (FPS, battle royale, aksiyon RPG,
bulut oyun, ücretsiz oyunlar) metne bu yüzden doğal hâlleriyle girer: hem okuyucu için anlaşılır
kalır hem de sayfanın kelime kapsamını genişletir.

Cümleyi kurarken tür kelimesini yamamak yerine oyunun konumunu anlatan bir ifadeye yerleştir:
"savaşı merkezine alan FPS oyunları", "hikâye odaklı aksiyon RPG oyunları" gibi.


## Kurallar

**En az 4, yaklaşık 5-6 link.** Daha azı sayfayı kütüphaneden kopuk bırakıyor, daha fazlası gövdeyi
link tarlasına çeviriyor.

**Benzer niyeti karşılayan birden fazla sayfa varsa yalnız birine link verilir.** Aynı konuda iki
inceleme yazısı varsa biri seçilir; FPS ve aksiyon kategorileri gibi örtüşen iki kategori varsa
oyuna daha yakın olan seçilir. Aynı hedefe iki kez link verilmez.

**`/gfn/sistem-gereksinimleri` sayfasına link verilmez.** Ekip kararı.

**Anchor, hedef sayfanın kendi kelimesidir.** "Buraya tıkla" ya da çıplak URL kullanılmaz.

**Önerilen ama henüz yayında olmayan sayfaya link verilmez**; tıklandığında 404 dönen bağlantı
sayfaya güven kaybettirir. Link seçtikten sonra hepsinin 200 döndüğü kontrol edilir:

```bash
for u in URL1 URL2; do printf "%s %s\n" "$(curl -sSL -o /dev/null -m 20 -w '%{http_code}' "$u")" "$u"; done
```

## Aday havuzu

Ürün ve kategori sayfaları:

- `https://gameplus.com.tr/gfn/paketler` - üyelik anlatılan bölümde
- `https://gameplus.com.tr/gfn/oyunlar/{tur}` - oyunun ana türü; mevcut kategoriler: aksiyon, macera,
  bagimsiz, simulasyon, strateji, basit-eglence, fps, oynamasi-ucretsiz, mmo, yaris, spor, aile-dostu,
  bulmaca, platform, dovus-oyunu, arcade, moba, demo, tech-teknolojik-demo, canlandirma,
  populer-oyunlar, diger
- `https://gameplus.com.tr/gfn/oyunlar` - tüm kütüphane
- Mağaza kategorileri: `/gfn/oyunlar/steam`, `/epic-games`, `/xbox`, `/ea-app`, `/ubisoft-connect`, `/gog`

Blog tarafında sık kullanılanlar (tam liste için sitemap taraması `arastirma.py` çıktısında):

- `/blog/cloud-gaming-nedir` - bulut oyun kavramı ilk geçtiğinde
- `/blog/geforce-now-ile-oynanabilecek-en-iyi-multiplayer-oyunlar` - çok oyunculu bağlam
- `/blog/en-iyi-battle-royale-oyunlari-son-kalan-olmaya-hazir-misin` - battle royale modu olan oyunlar
- `/blog/en-iyi-fps-oyunlari`, `/blog/2025-in-en-iyi-fps-oyunlari` - FPS bağlamı (ikisinden biri)
- `/blog/fps-nedir-ne-ise-yarar` - tür tanımı gereken durumlarda
- Oyunun kendi inceleme yazısı varsa o (birden fazlaysa biri)

## Yerleştirme

Her link brief'te hangi bölüme ve hangi cümleye gireceğiyle birlikte yazılır. Tipik dağılım:

| Bölüm | Link |
|---|---|
| Oynanış | tür kategorisi |
| Oynanış / mod alt başlığı | mod ya da türle ilgili blog yazısı |
| GeForce NOW deneyimi | cloud gaming nedir |
| GeForce NOW deneyimi / üyelik | paketler |
| Sistem gereksinimleri | oyunun inceleme yazısı |
| Kapanış | ücretsiz oyunlar ya da kütüphane |
