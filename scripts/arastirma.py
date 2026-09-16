#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Bir oyun için brief araştırmasını tek seferde toplar ve JSON dosyasına yazar.

Topladıkları:
  1. Google SERP (Türkiye/Türkçe) - PAA soruları, ilk 10 organik, ilgili aramalar
  2. Uzun kuyruk kelimeler ve aylık hacimleri (Keyword Planner tabanlı)
  3. Steam mağaza verisi - resmi dil listesi, sistem gereksinimleri, Metacritic, çıkış, stüdyo
  4. gameplus.com.tr blog sitemap taraması - iç link adayları
  5. Wikipedia oyun sayfası - hikâye kurulumu, oynanış, besteci ve müzik, ödül tablosu

Kullanım:
    python3 arastirma.py "battlefield 6" --cikti bf6.json [--steam-appid 2807960]

Not: İstekler curl ile atılır. Bu makinede Python'un urllib'i kurumsal sertifika zinciri
yüzünden SSL hatası veriyor; curl çalışıyor.
"""
import argparse, base64, json, os, re, subprocess, sys, time, html

DFS = "https://api.dataforseo.com"


def kimlik():
    cfg = json.load(open(os.path.expanduser("~/.claude.json")))
    env = cfg["mcpServers"]["dfs-mcp"]["env"]
    return base64.b64encode(f"{env['DATAFORSEO_USERNAME']}:{env['DATAFORSEO_PASSWORD']}".encode()).decode()


def post(yol, govde, auth, saniye=180):
    f = "/tmp/_dfs_istek.json"
    json.dump(govde, open(f, "w"), ensure_ascii=False)
    r = subprocess.run(["curl", "-sS", "-m", str(saniye), "-X", "POST", DFS + yol,
                        "-H", f"Authorization: Basic {auth}", "-H", "Content-Type: application/json",
                        "--data-binary", f"@{f}"], capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(f"curl hatası: {r.stderr[:300]}")
    return json.loads(r.stdout)


def get(url, saniye=60, basliklar=None):
    cmd = ["curl", "-sSL", "-m", str(saniye), "-A", "Mozilla/5.0"]
    for b in (basliklar or []):
        cmd += ["-H", b]
    cmd.append(url)
    return subprocess.run(cmd, capture_output=True, text=True).stdout


def serp(kw, auth):
    res = post("/v3/serp/google/organic/live/advanced",
               [{"keyword": kw, "location_code": 2792, "language_code": "tr",
                 "device": "desktop", "depth": 20, "people_also_ask_click_depth": 2}], auth)
    items = res["tasks"][0]["result"][0]["items"]
    return {
        "paa": [q.get("title") for i in items if i["type"] == "people_also_ask" for q in i.get("items", [])],
        "organik": [{"sira": i.get("rank_group"), "domain": i.get("domain"), "baslik": i.get("title")}
                    for i in items if i["type"] == "organic"][:10],
        "ilgili_aramalar": sorted({q for i in items if i["type"] == "related_searches" for q in i.get("items", [])}),
        "maliyet": res.get("cost"),
    }


def kelimeler(kw, auth, limit=300):
    res = post("/v3/dataforseo_labs/google/keyword_suggestions/live",
               [{"keyword": kw, "location_code": 2792, "language_code": "tr",
                 "limit": limit, "order_by": ["keyword_info.search_volume,desc"]}], auth)
    out = []
    for it in res["tasks"][0]["result"][0]["items"]:
        ki = it.get("keyword_info") or {}
        if (ki.get("search_volume") or 0) >= 10:
            out.append({"kelime": it["keyword"], "hacim": ki["search_volume"],
                        "aylar": {f"{m['year']}-{m['month']:02d}": m["search_volume"]
                                  for m in (ki.get("monthly_searches") or [])}})
    return {"liste": out, "maliyet": res.get("cost")}


def steam(appid=None, ad=None):
    if not appid and ad:
        d = get("https://steamcommunity.com/actions/SearchApps/" + ad.replace(" ", "%20"))
        try:
            appid = json.loads(d)[0]["appid"]
        except Exception:
            return {"hata": "Steam app id bulunamadı"}
    raw = get(f"https://store.steampowered.com/api/appdetails?appids={appid}&l=turkish&cc=TR")
    try:
        x = json.loads(raw)[str(appid)]
    except Exception:
        return {"hata": "Steam yanıtı okunamadı"}
    if not x.get("success"):
        return {"hata": "Steam kaydı yok"}
    x = x["data"]

    def duz(s):
        s = html.unescape(re.sub(r"<br\s*/?>", "\n", s or ""))
        return re.sub("<[^>]+>", "", s).strip()

    diller = duz(x.get("supported_languages", ""))
    return {
        "appid": appid, "ad": x.get("name"), "cikis": (x.get("release_date") or {}).get("date"),
        "gelistirici": x.get("developers"), "yayinci": x.get("publishers"),
        "metacritic": x.get("metacritic"),
        "diller": diller,
        "turkce_destek": bool(re.search(r"türkçe", diller, re.I)),
        "gereksinim_min": duz((x.get("pc_requirements") or {}).get("minimum")),
        "gereksinim_onerilen": duz((x.get("pc_requirements") or {}).get("recommended")),
    }


def wikipedia(ad):
    """Oynanış, hikâye kurulumu, müzik ve ödül bölümlerini ham wikitext olarak getirir.

    Ödül ve besteci bilgisi başka hiçbir kaynakta tek yerde toplanmıyor; Wikipedia'nın
    Awards tablosu kazanan/aday ayrımını da taşıdığı için bu ayrımı kaybetmeden okunabiliyor.
    Yine de yazmadan önce ödül törenin kendi kazanan listesinden teyit edilir.
    """
    baslik = ad.strip().replace(" ", "_")
    ham = get(f"https://en.wikipedia.org/w/index.php?title={baslik}&action=raw")
    if not ham or "#REDIRECT" in ham[:60].upper():
        return {"bulundu": False, "baslik": baslik}
    def bolum(adlar, sinir=3500):
        for b in adlar:
            m = re.search(r"==+\s*" + b + r"\s*==+", ham)
            if m:
                g = ham[m.end():m.end() + sinir]
                g = re.sub(r"<ref[^>]*>.*?</ref>|<ref[^>]*/>", "", g, flags=re.S)
                return re.sub(r"\[\[([^\]|]*\|)?([^\]]*)\]\]", r"\2", g).strip()
        return ""
    return {"bulundu": True, "baslik": baslik,
            "oynanis": bolum(["Gameplay"]),
            "hikaye": bolum(["Plot", "Synopsis", "Premise"], 2200),
            "muzik": bolum(["Music", "Audio"], 1800),
            "oduller": bolum(["Awards", "Accolades"], 4000)}


def blog_envanteri(anahtarlar):
    x = get("https://gameplus.com.tr/sitemap-blog.xml")
    sluglar = [u.rsplit("/", 1)[-1] for u in re.findall(r"<loc>(.*?)</loc>", x)]
    hit = {}
    for a in anahtarlar:
        eslesen = [s for s in sluglar if a in s.lower()]
        if eslesen:
            hit[a] = eslesen[:8]
    return {"toplam_blog": len(sluglar), "eslesenler": hit}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("kelime", help="ana kelime, ör. 'battlefield 6'")
    ap.add_argument("--cikti", required=True)
    ap.add_argument("--steam-appid")
    ap.add_argument("--blog-anahtar", nargs="*", default=[],
                    help="blog sitemap'inde aranacak ek kelimeler")
    ap.add_argument("--wiki", help="İngilizce Wikipedia sayfa başlığı; boşsa oyun adı kullanılır")
    a = ap.parse_args()

    auth = kimlik()
    veri = {"kelime": a.kelime}
    print("1/5 SERP ve PAA...", flush=True)
    veri["serp"] = serp(a.kelime, auth)
    time.sleep(2)
    print("2/5 kelime kümesi...", flush=True)
    veri["kelimeler"] = kelimeler(a.kelime, auth)
    time.sleep(2)
    print("3/5 Steam...", flush=True)
    veri["steam"] = steam(a.steam_appid, a.kelime)
    print("4/5 blog envanteri...", flush=True)
    kok = a.kelime.split()[0].lower()
    veri["blog"] = blog_envanteri(list({kok, *[x.lower() for x in a.blog_anahtar],
                                        "fps", "battle-royale", "cloud", "en-iyi"}))
    print("5/5 Wikipedia...", flush=True)
    veri["wikipedia"] = wikipedia(a.wiki or a.kelime.title())
    json.dump(veri, open(a.cikti, "w"), ensure_ascii=False, indent=2)
    print(f"\nyazıldı: {a.cikti}")
    print(f"  PAA sorusu: {len(veri['serp']['paa'])} | kelime: {len(veri['kelimeler']['liste'])}"
          f" | Türkçe destek: {veri['steam'].get('turkce_destek')}"
          f" | Metacritic: {(veri['steam'].get('metacritic') or {}).get('score')}"
          f" | Wikipedia: {'var' if veri['wikipedia']['bulundu'] else 'yok'}"
          f" | ödül bölümü: {'var' if veri['wikipedia'].get('oduller') else 'yok'}")


if __name__ == "__main__":
    main()
