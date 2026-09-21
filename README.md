# Gameplus Oyun Detay Sayfası: Brief ve İçerik

gameplus.com.tr (GeForce NOW powered by GAME+ Türkiye) oyun detay sayfaları için **içerik briefi** ve
**sayfa içeriği** üreten Claude Code skill'i, referansları ve örnekleri.

Kütüphanede 2.100'ün üzerinde oyun var ve her biri için aynı yapıda bir detay sayfası açılacak.
Bu depo, o sayfaların briefini ve içeriğini oyundan oyuna tutarlı üretmek için kullanılan süreci
tutuyor: hangi kaynaktan hangi bilgi alınır, brief hangi sütunlardan oluşur, içerik nasıl kurgulanır
ve teslimden önce ne kontrol edilir.

## İçindekiler

```
SKILL.md                    Beş fazlı çalışma akışı ve değişmeyen kurallar
references/
  dogrulama.md              Hangi bilgi hangi kaynaktan alınır, bilinen tuzaklar
  brief-kurallari.md        Brief Excel'inin dokuz sütunu ve biçim kuralları
  icerik-kurallari.md       İçerik yapısı, ton, bölüm kalıpları
  ic-link-haritasi.md       İç link seçim kuralları ve aday sayfa envanteri
  kontrol-listesi.md        Teslim öncesi denetim
scripts/
  katalog.py                Oyunu GFN katalog Excel'inde bulur
  arastirma.py              SERP + PAA, kelime kümesi, Steam verisi, blog envanteri
  brief_satiri.py           Brief Excel'ine oyun satırı ekler
  icerik_docx.py            İçerik JSON'undan Word dosyası üretir
assets/
  brief-sablonu.xlsx        Boş brief Excel'i (yalnız başlık satırı)
examples/
  ornek-brief-battlefield-6.xlsx        Doldurulmuş brief
  ornek-brief-satiri-battlefield-6.json brief_satiri.py girdisi
  ornek-icerik-battlefield-6.docx       Yazılmış sayfa içeriği
  ornek-icerik-battlefield-6.json       icerik_docx.py girdisi
```

## Hızlı kullanım

```bash
# 1. Katalog kaydı
python3 scripts/katalog.py "Battlefield 6"

# 2. Araştırma (SERP + PAA, kelimeler, Steam, blog envanteri)
python3 scripts/arastirma.py "battlefield 6" --cikti /tmp/oyun.json --steam-appid 2807960

# 3. Brief satırını ekle
python3 scripts/brief_satiri.py --xlsx brief.xlsx --json satir.json

# 4. İçeriği üret
python3 scripts/icerik_docx.py --json icerik.json --out battlefield-6-icerik.docx
```

`arastirma.py`, DataForSEO kimliklerini `~/.claude.json` içindeki MCP yapılandırmasından okur;
depoda kimlik bilgisi tutulmaz.

## Sürecin özeti

Detay sayfası kalıcı ürün sayfasıdır: oyuncunun "bu oyun nedir, GeForce NOW üzerinden oynayabilir
miyim, nasıl başlarım" sorusunu karşılar. Blogdaki inceleme yazıları çıkış dönemine ait
değerlendirmelerdir ve ayrı bir iş görür.

- Sayfada H1 oyun adı olarak bulunduğu için gövdeye başlık konmaz; **başlıksız kısa bir girişle** açılır, ardından H2'ler gelir.
- Gövde ortalama **1200-1500 kelime**, 7-9 H2 ve az sayıda H3.
- SSS soruları Google'ın "Bunlar da sorulmuş" kutusundan ve arama önerilerinden gelir; yanıtlar
  20-60 kelime ve ilk cümle doğrudan cevaptır.
- **Oyuna özel paket gerekliliği yazılmaz.** Kapanışta bir iki cümleyle oyunu oynamak için GeForce NOW Ultimate ya da Performance paketlerinden birinin seçilebileceği söylenir ve okuyucu satın almaya çağrılır; fiyat ve paket özelliği yazılmaz.
- Tek oyunculu moddan "kampanya" diye bahsedilmez.
- Doğrulanamayan sayı yazılmaz; alan boş bırakılır ve durum ekibe bildirilir.

Ayrıntılar `SKILL.md` ve `references/` altında.

## Kurulum

Claude Code'da kullanmak için depoyu kişisel skill dizinine kopyalayın:

```bash
git clone https://github.com/erdogan1ozdemir/gameplus-oyun-detay-brief-icerik.git \
  ~/.claude/skills/gameplus-oyun-detay-brief-icerik
```

Gereken Python paketleri: `openpyxl`, `python-docx`. Araştırma scripti `curl` kullanır.
