#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Oyunun ham GFN katalog kaydını (all_games JSON) basar: tanıtım metni, mağaza variantları, teknoloji bayrakları.

Kullanım:
    python3 katalog_json.py "Forza Horizon 6"
    python3 katalog_json.py "Fortnite" --json ~/Downloads/inbound/all_games_1.json

Neden ayrı betik: `katalog.py` katalog Excel'ini okur ve yalnız kısa açıklamayı taşır. Ham JSON'daki
**longDescription**, oyunun kendi tanıtım metnidir ve Steam ile Wikipedia'da bulunmayan ayrıntıları
taşır (ilerleme sistemi, mod ve bölge adları, yoldaş ve düşman adları, erişilebilirlik seçenekleri).
İçerik yazmadan önce bu metin de okunur; içeriğe giren her bilgi yine kaynağıyla doğrulanır.

Bilinmesi gerekenler:
- **JSON'da dil desteği alanı yoktur.** `keywords` alanındaki Türkçe etiketler (Aksiyon, Zengin Hikâye)
  NVIDIA'nın çevrilmiş tür etiketleridir; Türkçesi olmayan oyunlarda da görünür, dil sinyali değildir.
  Türkçe desteği Steam `supported_languages` ya da yayıncı mağazasından doğrulanır.
- `contentRatings` **USK** (Almanya) derecesidir. Türkiye için PEGI ayrıca kontrol edilir.
- Teknoloji bayrakları oyun düzeyinde değil, mağaza variantı düzeyindedir: `HDR_ENABLED`,
  `RTX_ENABLED`, `REFLEX_ENABLED`.
"""
import argparse, json, os, re, sys, unicodedata

VARSAYILAN = [os.path.expanduser("~/Downloads/inbound/all_games_1.json"),
              os.path.expanduser("~/Downloads/all_games_1.json")]


def normalize(s):
    for ch in "®™©℠":
        s = (s or "").replace(ch, "")
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.replace("İ", "i").replace("I", "i").lower()
    s = s.translate(str.maketrans("çğıöşü", "cgiosu"))
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("oyun")
    ap.add_argument("--json")
    ap.add_argument("--tam", action="store_true", help="uzun açıklamayı kırpmadan yazar")
    a = ap.parse_args()

    yol = a.json or next((p for p in VARSAYILAN if os.path.exists(p)), None)
    if not yol:
        sys.exit("Katalog JSON'u bulunamadı; --json ile yolunu ver.")
    items = json.load(open(yol, encoding="utf-8"))["items"]

    ara = normalize(a.oyun)
    tam = [g for g in items if normalize(g["title"]) == ara]
    bulunan = tam or [g for g in items if ara in normalize(g["title"])]
    if not bulunan:
        sys.exit(f"'{a.oyun}' katalogda bulunamadı ({len(items)} oyun tarandı).")
    if len(bulunan) > 1 and not tam:
        print("Birden fazla eşleşme:", ", ".join(g["title"] for g in bulunan[:10]))

    for g in bulunan[:3]:
        r = g.get("contentRatings") or {}
        print("=" * 70)
        print(f"{g['title']} · {g['publisherName']} / {g['developerName']}")
        print("türler:", ", ".join(g["genres"]), "| kontroller:", ", ".join(g["supportedControls"]))
        print("yerel oyuncu:", g["maxLocalPlayers"], "| çevrim içi oyuncu:", g["maxOnlinePlayers"],
              "|", r.get("type", "-"), r.get("categoryKey", "-"), r.get("interactiveElementKeys") or "")
        print("çıkış:", (g.get("computedValues") or {}).get("earliestReleaseDate", "")[:10])
        for v in g.get("variants", []):
            gf = v.get("gfn") or {}
            bayrak = {f["key"]: f["value"] for f in gf.get("features") or []}
            print(f"  variant: {v['appStore']:10} {gf.get('optimizationStatus',''):18}"
                  f" {gf.get('releaseDate','')[:10]}  {bayrak}")
            if v.get("storeUrl"):
                print(f"            {v['storeUrl']}")
        print("\nKISA AÇIKLAMA:\n" + (g.get("shortDescription") or "-"))
        uzun = re.sub(r"\n{2,}", "\n", g.get("longDescription") or "-")
        print("\nUZUN AÇIKLAMA:\n" + (uzun if a.tam else uzun[:4000]))
        print("\nNot: JSON'da dil desteği alanı yok; keywords alanı çevrilmiş tür etiketidir. "
              "Yaş sınırı USK'dır, PEGI ayrıca kontrol edilir.")


if __name__ == "__main__":
    main()
