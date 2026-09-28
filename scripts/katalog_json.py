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
- **Dil desteği yalnız yeni dökümde vardır.** `gfn_apps_TR.json` (Türkiye mağazası dökümü, 25.09.2026)
  mağaza variantı başına `supportedLanguages` taşır: dil + `availableFeatures` (ux = arayüz,
  subtitles = altyazı, speech = seslendirme). Eski `all_games_1.json`'da bu alan yoktur. Steam
  variantlarında 110 oyunluk örneklemde Steam'le %97 uyumlu; birkaç oyunda Türkçe sonradan eklendiği
  için JSON'da görünmüyor, bazı oyunlarda da mağazalar ayrışıyor (HoI4: Xbox'ta var, Steam'de yok).
  Kaynak GeForce NOW kaydıdır (kullanıcı kararı, 28.09.2026); kayıt eksik görünüyorsa kullanıcıya söylenir.
- `keywords` alanındaki Türkçe etiketler (Aksiyon, Zengin Hikâye) NVIDIA'nın çevrilmiş tür
  etiketleridir; dil sinyali değildir.
- `contentRatings` **USK** (Almanya) derecesidir. Türkiye için PEGI ayrıca kontrol edilir.
- Teknoloji bayrakları oyun düzeyinde değil, mağaza variantı düzeyindedir: `HDR_ENABLED`,
  `RTX_ENABLED`, `REFLEX_ENABLED`.
"""
import argparse, json, os, re, sys, unicodedata

VARSAYILAN = [os.path.expanduser("~/Desktop/Claude Projects/Game+  copy/Veri Dosyaları/gfn_apps_TR.json"),
              os.path.expanduser("~/Downloads/inbound/all_games_1.json"),
              os.path.expanduser("~/Downloads/all_games_1.json")]
DIL = {"ux": "arayüz", "subtitles": "altyazı", "speech": "seslendirme"}


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
            diller = gf.get("supportedLanguages")
            if diller is not None:
                tr = [l for l in diller if l["language"].lower() == "tr_tr"]
                kapsam = ", ".join(DIL.get(f, f) for f in (tr[0].get("availableFeatures") or [])) if tr else "yok"
                print(f"            dil: {len(diller)} · Türkçe: {kapsam}")
            if v.get("storeUrl"):
                print(f"            {v['storeUrl']}")
        print("\nKISA AÇIKLAMA:\n" + (g.get("shortDescription") or "-"))
        uzun = re.sub(r"\n{2,}", "\n", g.get("longDescription") or "-")
        print("\nUZUN AÇIKLAMA:\n" + (uzun if a.tam else uzun[:4000]))
        print("\nNot: Türkçe durumu bu kayıttan okunur, mağazalar ayrışabilir (brief hücresi: dil_hucresi.py); "
              "keywords alanı çevrilmiş tür etiketidir. Yaş sınırı USK'dır, PEGI ayrıca kontrol edilir.")


if __name__ == "__main__":
    main()
