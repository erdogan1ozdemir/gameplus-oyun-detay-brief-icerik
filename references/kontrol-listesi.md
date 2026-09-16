# Teslim öncesi kontrol listesi

## Brief

- [ ] Main KW hacmi 12 aylık ortalama mı, sütunda sayı olarak mı duruyor?
- [ ] Yeni çıkmış oyunda son üç ayın ortalaması DİKKAT satırına yazıldı mı?
- [ ] İkincil kelimelerde fiyat, satın alma, platform ve anahtar kelimeleri var mı? (olmamalı)
- [ ] Başlık sayısı 1200-1500 kelimeye uygun mu? (7-9 H2, az sayıda H3)
- [ ] İçerik kurgusunda başlık yanına kelime sayısı yazılmış mı? (yazılmamalı)
- [ ] Hangi GAME+ paketinin gerektiğine dair başlık, soru ya da cümle var mı? (olmamalı)
- [ ] Link sayısı en az 4 mü, hepsi tam URL mi, 200 dönüyor mu?
- [ ] Aynı niyeti karşılayan iki sayfaya birden link verilmiş mi? (verilmemeli)
- [ ] `/gfn/sistem-gereksinimleri` linki var mı? (olmamalı)
- [ ] SSS soruları PAA ve arama önerilerinden mi geliyor?
- [ ] Yanıt biçimi metni olduğu gibi kopyalandı mı?
- [ ] Künye ve katalog verisi briefe sızmış mı? (sızmamalı)

## İçerik

- [ ] Gövde H2 ile mi başlıyor, belgede H1 var mı? (olmamalı)
- [ ] Kelime sayısı 1200-1500 bandında mı?
- [ ] Gövde başlıksız 1-2 paragraflık girişle mi açılıyor, giriş ilk H2'nin işini üstlenmiş mi?
- [ ] Sınıflar, modlar ve puanlar madde listesine alındı mı, yoksa paragrafa mı sıkıştırıldı?
- [ ] Sıra taşımayan liste madde imli (`mad`), yalnız başlama adımları numaralı (`li`) mi?
- [ ] Ton, sanat tasarımı, müzik ve ödüller için kısa bir paragraf var mı? Kazanılan ödül ile adaylık ayrılmış mı?
- [ ] Hikâyeden bahsedilirken olay örgüsü açığa çıkmış mı? (çıkmamalı: kurulum, mekân ve süre yeterli)
- [ ] Özel adlar (birlik, karakter, mod, harita) kaynaktaki yazımıyla mı geçiyor?
- [ ] Gövdede dört kip de görünüyor mu (geniş zaman, `-mektedir`, şimdiki zaman, ikinci tekil), yoksa tek kipe mi kilitlenmiş?
- [ ] Anlatı bölümlerindeki birinci çoğul, erişim ve başlama adımlarına sızmış mı? (sızmamalı)
- [ ] Bir cümle `-iyor` ile biterken sonraki `-mıştır` ile mi başlıyor? Geçişe köprü konmuş mu?
- [ ] Başlık üç konuyu virgülle mi diziyor? (en fazla iki konu)
- [ ] Müzik anlatılırken "skor" kelimesi kullanılmış mı? (kullanılmamalı)
- [ ] Her H2'nin ilk cümlesi başlığın sorusunu doğrudan yanıtlıyor mu?
- [ ] "Kampanya" kelimesi tek oyunculu mod için kullanılmış mı? (kullanılmamalı)
- [ ] Türkçe dil desteği yoksa gövdede tek cümleyle belirtildi mi, ayrı H2 ve SSS sorusu açılmadı mı?
- [ ] Teknik değer kümeleri tabloya alındı mı?
- [ ] Puan, gereksinim, boyut ve dil listesi **PC sürümünden** mi alınmış? Metacritic puanı "PC puanı" olarak mı yazılmış?
- [ ] Doğrulanmamış sayı var mı? Her sayının kaynağı belli mi?
- [ ] Fiyat, indirim, kampanya ya da sezon adı geçiyor mu? (geçmemeli)
- [ ] Sunucu sınıfı yazıldıysa paketler sayfasından teyit edildi mi?
- [ ] SSS yanıtları 60 kelimeyi aşıyor mu? İlk cümleler doğrudan yanıt mı?
- [ ] Linkler gövdede belirtilen bölümlere yerleşti mi?
- [ ] **Anchor'ı sil, cümle hâlâ anlamlı mı?** "…listesine göz atabilirsin" biçiminde link taşımak için kurulmuş cümle var mı?
- [ ] Hikâye, atmosfer-ses-müzik ve öne çıkan özellikler kendi bölümlerini aldı mı?
- [ ] Bölüm başına iki üç kalın vurgu var mı, yoksa her paragraf kalınla mı dolu?
- [ ] SSS'den önce kapanış çağrısı var mı?
- [ ] GFN optimizasyon durumu yazılmış mı? (yazılmamalı)
- [ ] Mağaza listesi katalogdaki variants alanıyla birebir mi? Katalogda olmayan mağaza yazılmış mı?
- [ ] Okuyucunun bilgisayarı olduğu varsayılmış mı? ("bilgisayarında … olmalı" yerine "bilgisayardan oynayanlarda")
- [ ] Bilgi cümleleri konuşma diline kaçan geçmiş zamanla mı yazılmış? ("besteledi" yerine "bestelemiştir")
- [ ] Belgenin altına kaynak notu basılmış mı? (basılmamalı, sohbette söylenir)

## Biçim taraması

```bash
python3 - <<'PY'
import zipfile, re, sys
x = zipfile.ZipFile(sys.argv[1] if len(sys.argv)>1 else "icerik.docx").read("word/document.xml").decode()
t = re.sub(r"<[^>]+>", "", re.sub(r"</w:p>", "\n", x))
for a,b in [("&amp;","&"),("&lt;","<"),("&gt;",">")]: t=t.replace(a,b)
print("uzun tire:", t.count("—"), "| çift boşluk:", len(re.findall(r"(?<=\S)  (?=\S)", t)),
      "| emoji:", len(re.findall(r"[\U0001F300-\U0001FAFF]", t)),
      "| 'kampanya':", len(re.findall(r"kampanya", t, re.I)),
      "| 'Geforce Now':", len(re.findall(r"Geforce Now", t)),
      "| ® ™:", t.count("®")+t.count("™"))
PY
```

Hepsi sıfır olmalı.

## Teslim

Kullanıcıya dosyayı gönderirken üç şeyi söyle: hangi bilgiyi hangi kaynaktan aldın, neyi
yazmadın ve neden, hangi konuda onay bekliyorsun. Bu sayfalarda en çok değer taşıyan bilgi,
yazılmayanın neden yazılmadığıdır.
