#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""İçerik JSON'unu teslimden önce denetler: yapı, biçim, link, SSS ve teknoloji bayrakları.

Kullanım:
    python3 icerik_denetim.py --json /tmp/icerik.json
    python3 icerik_denetim.py --json /tmp/icerik.json --katalog-adi "Forza Horizon 6"

Neden betik: bu kontroller her oyunda aynı; elle yapıldığında en çok kaçan üç şey uzun tire,
"kampanya" kelimesi ve kapanıştaki paket cümlesinin unutulması oluyordu. Teknoloji bayrakları
(HDR, RTX, NVIDIA Reflex) katalog JSON'undan okunur ve metinle karşılaştırılır: desteklenen
teknoloji anılmamışsa eksik, desteklenmeyen teknoloji anılmışsa yanlış bilgi demektir.

Bulgu varsa çıkış kodu 1 olur; docx üretmeden önce çalıştırılır.
"""
import argparse, json, os, re, sys, unicodedata
from collections import Counter

VARSAYILAN_KATALOG = [os.path.expanduser("~/Downloads/inbound/all_games_1.json"),
                      os.path.expanduser("~/Downloads/all_games_1.json")]

BICIM = [("—", "uzun tire"), ("–", "en tire"), (r"(?<=\S)  +(?=\S)", "çift boşluk"),
         (r"(?i)kampanya", "kampanya"), (r"Geforce Now", "yanlış yazım (GeForce NOW)"),
         ("®|™", "marka sembolü"), (r"(?i)optimi[zs]", "optimizasyon"),
         (r"(?i)paketi? gerek", "paket gerekliliği"), (r"(?i)\bTL\b|₺", "fiyat"),
         (r"[\U0001F300-\U0001FAFF]", "emoji"), (r"\.\.", "çift nokta"),
         (r" ,| \.", "boşluk-noktalama"), (r"(?i)\bçıkacak\b|\byakında\b", "zamana bağlı ifade")]

KAPANIS = "**GeForce NOW Ultimate** ya da **Performance** paketlerinden"

# Editör okumasında düzeltilen cümle hataları (bkz. icerik-kurallari.md, Cümle kurgusu ve kelime seçimi)
BIRINCI_COGUL = (r"\b\w+(?:ıyoruz|iyoruz|uyoruz|üyoruz|ıyorduk|iyorduk|acağız|eceğiz|abiliriz|ebiliriz)\b"
                 r"|\b(?!günümüz)\w+(?:ımız|imiz|umuz|ümüz)(?:a|e|ı|i|u|ü|da|de|dan|den|la|le|ın|in|un|ün)?\b"
                 r"|\bbiz(?:im|e|i|den)?\b")
MECAZ = r"(?i)(?:şart|gereksinim|gereklilik)\w*[^.;]{0,40}?(?:yüklen|bin)\w*|cihaz\w* (?:yüklen|bin)\w*"
UYARI_DESEN = [
    (r"\b(?:Most|Best) [A-Z]\w+", "ödül dalı İngilizce kalmış olabilir (tören adı özgün, dal Türkçe)"),
    (r"bilinen \(", "parantez cümlenin söylediğini tekrar ediyor olabilir"),
    (r"(?i)kendi içinde okunabil", "oyun için 'okunur' fiili (oynanır)"),
]
TEKRAR_DISI = {"oyunu", "oyunl", "oyunc", "oynan", "oynay", "oynam", "oynad", "gefor", "nvidi", "ultim",
               "perfo", "paket", "hesab", "kütüp", "sunuc", "bulut", "kadar"}

TEKNOLOJI = {"HDR_ENABLED": ("HDR", r"\bHDR\b"),
             "RTX_ENABLED": ("RTX", r"\bRTX\b|ışın izleme"),
             "REFLEX_ENABLED": ("NVIDIA Reflex", r"\bReflex\b")}


def normalize(s):
    for ch in "®™©℠":
        s = (s or "").replace(ch, "")
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.replace("İ", "i").replace("I", "i").lower()
    s = s.translate(str.maketrans("çğıöşü", "cgiosu"))
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def bayraklar(oyun_adi, yol=None):
    yol = yol or next((p for p in VARSAYILAN_KATALOG if os.path.exists(p)), None)
    if not yol:
        return None, "katalog JSON'u bulunamadı, teknoloji bayrakları denetlenmedi"
    items = json.load(open(yol, encoding="utf-8"))["items"]
    ara = normalize(oyun_adi)
    esles = [g for g in items if normalize(g["title"]) == ara] or \
            [g for g in items if ara in normalize(g["title"]) or normalize(g["title"]) in ara]
    if not esles:
        return None, f"'{oyun_adi}' katalogda bulunamadı, teknoloji bayrakları denetlenmedi"
    b = set()
    for v in esles[0].get("variants", []):
        b |= {f["key"] for f in (v.get("gfn") or {}).get("features") or []}
    return b, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", required=True)
    ap.add_argument("--katalog-adi", help="katalogdaki oyun başlığı (metinden farklıysa)")
    ap.add_argument("--katalog-json")
    ap.add_argument("--tekrar", action="store_true",
                    help="aynı cümlede aynı kökün iki kez geçtiği yerleri okuma listesi olarak basar")
    a = ap.parse_args()

    d = json.load(open(a.json, encoding="utf-8"))
    g, oyun = d["govde"], d["oyun"]
    duz = lambda i: re.sub(r"\*\*", "", re.sub(r"\[LINK(\d+)\]", lambda m: d["linkler"]["LINK" + m.group(1)][0], i))
    govde_metin = " ".join(duz(i) for t, i in g if t in ("p", "li", "mad"))
    tum = govde_metin + " " + " ".join(q + " " + c for q, c in d["sss"])
    sorun, uyari = [], []

    # uzunluk ve başlık sayısı
    kelime = len(govde_metin.split())
    h2 = [v for t, v in g if t == "H2"]
    h3 = [v for t, v in g if t == "H3"]
    if not 1200 <= kelime <= 1550:
        sorun.append(f"gövde {kelime} kelime; 1200-1500 bandı dışında")
    if not 7 <= len(h2) <= 9:
        sorun.append(f"{len(h2)} H2 var; 7-9 olmalı")
    if g[0][0] != "p":
        sorun.append("gövde başlıksız girişle açılmıyor")
    if any(t == "p" and re.match(r"Gövde \d+ kelime", i) for t, i in g):
        sorun.append("künye/meta satırı gövdeye basılmış")

    # GeForce NOW bölümü tek başlıktır ve GAME+ H3'ünün hemen öncesindedir
    gfn = [k for k, (t, v) in enumerate(g) if t == "H2" and "GeForce NOW" in v]
    if len(gfn) != 1:
        sorun.append(f"GeForce NOW H2'si {len(gfn)} kez geçiyor; erişim ve bulut deneyimi tek başlıkta toplanır")
    else:
        k = gfn[0]
        if not g[k][1].endswith("GeForce NOW'da Nasıl Oynanır?"):
            sorun.append(f"GeForce NOW başlığı '{g[k][1]}'; '{oyun} GeForce NOW'da Nasıl Oynanır?' olmalı")
        sonraki_h3 = next((v for t, v in g[k + 1:] if t in ("H2", "H3")), "")
        if "GAME+ ile Oynamak" not in sonraki_h3:
            sorun.append(f"GeForce NOW H2'sinden sonra '{oyun}'ı GAME+ ile Oynamak' H3'ü gelmiyor ({sonraki_h3 or 'yok'})")
    if any("Deneyimi" in v and "GeForce NOW" in v for v in h2 + h3):
        sorun.append("'GeForce NOW ile ... Deneyimi' başlığı kaldırıldı; tek başlık kullanılır")

    # linkler
    kull = re.findall(r"\[LINK\d+\]", " ".join(i for t, i in g if t != "tablo"))
    for k in d["linkler"]:
        n = kull.count(f"[{k}]")
        if n != 1:
            sorun.append(f"{k} {n} kez kullanılmış")
    for k in set(kull):
        if k[1:-1] not in d["linkler"]:
            sorun.append(f"{k} tanımsız")
    if len(d["linkler"]) < 4:
        sorun.append(f"{len(d['linkler'])} iç link var; en az 4 olmalı")

    # biçim
    for pat, ad in BICIM:
        for m in re.finditer(pat, tum):
            sorun.append(f"{ad}: …{tum[max(0, m.start() - 45):m.end() + 45]}…")

    # hitap ve cümle kurgusu
    for m in re.finditer(BIRINCI_COGUL, tum):
        sorun.append(f"birinci çoğul (hitap sen olmalı): …{tum[max(0, m.start() - 40):m.end() + 20]}…")
    for m in re.finditer(MECAZ, tum):
        sorun.append(f"mecaz fiil (şart cihaza yüklenmez, cihazda aranmaz): …{tum[max(0, m.start() - 30):m.end() + 20]}…")
    for desen, ad in UYARI_DESEN:
        for m in re.finditer(desen, tum):
            uyari.append(f"{ad}: …{tum[max(0, m.start() - 40):m.end() + 30]}…")
    kok = lambda w: w.replace("İ", "i").replace("I", "ı").lower()[:5]   # Türkçe küçük harf
    for t, i in g:
        m = re.match(r"\*\*(.+?):\*\*\s*(.+)", i) if t == "mad" else None
        if not m:
            continue
        et = [kok(w) for w in re.findall(r"\w+", m.group(1)) if len(w) >= 5]
        gv = [kok(w) for w in re.findall(r"\w+", duz(m.group(2))) if len(w) >= 5]
        if et and gv and (len(set(et) & set(gv)) >= 2 or et[-1] == gv[-1]):
            uyari.append(f"madde tanımı etiketini tekrar ediyor olabilir: {duz(i)[:110]}")

    # kapanış paket çağrısı
    if KAPANIS not in " ".join(i for t, i in g if t == "p"):
        sorun.append("kapanışta GeForce NOW Ultimate ya da Performance paket önerisi yok")

    # SSS
    if not any("Türkçe" in q for q, _ in d["sss"]):
        sorun.append("SSS'de Türkçe sorusu yok; destek olmasa da sorulur")
    for q, c in d["sss"]:
        n = len(c.split())
        if not 20 <= n <= 60:
            sorun.append(f"SSS yanıtı {n} kelime: {q}")

    # teknoloji bayrakları
    # Paket cümleleri ("Ultimate paketleri GeForce RTX 4080 sunucularda 4K HDR…") hizmetin
    # özelliğini anlatır, oyunun desteğini değil; bayrak denetiminin dışında tutulur.
    iddia = " ".join(c for c in re.split(r"(?<=[.!?:;]) +", govde_metin)
                     if not re.search(r"Ultimate|paketler|paketi", c))
    b, not_ = bayraklar(a.katalog_adi or oyun, a.katalog_json)
    if not_:
        uyari.append(not_)
    else:
        for anahtar, (ad, desen) in TEKNOLOJI.items():
            var, anildi = anahtar in b, bool(re.search(desen, iddia))
            if var and not anildi:
                sorun.append(f"{ad} katalogda destekli ama metinde geçmiyor")
            if not var and anildi:
                sorun.append(f"{ad} katalogda destekli değil ama metinde geçiyor")

    # kip dağılımı (bilgi amaçlı)
    kip = {k: len(re.findall(p, govde_metin)) for k, p in
           [("-iyor", r"\w+(?:ıyor|iyor|uyor|üyor)(?:uz|sun|lar)?\b"),
            ("-mektedir", r"\w+(?:mektedir|maktadır)\b"), ("-mıştır", r"\w+(?:mıştır|miştir|muştur|müştür)\b")]}

    print(f"{oyun}: {kelime} kelime · {len(h2)} H2 · {len(h3)} H3 · {len(d['linkler'])} link · {len(d['sss'])} SSS "
          f"· kip: " + ", ".join(f"{k} {v}" for k, v in kip.items()))
    if b:
        print("teknoloji:", ", ".join(sorted(TEKNOLOJI[x][0] for x in b if x in TEKNOLOJI)) or "-")
    for u in uyari:
        print("NOT:", u)
    if a.tekrar:
        ad_kok = {kok(w) for w in re.findall(r"\w+", oyun)}
        for t, i in g:
            if t not in ("p", "li", "mad"):
                continue
            for c in re.split(r"(?<=[.!?;:]) +", duz(i)):
                say = Counter(kok(w) for w in re.findall(r"[^\W\d_]+", c) if len(w) >= 5)
                kokler = [k for k, n in say.items() if n > 1 and k not in TEKRAR_DISI and k not in ad_kok]
                if kokler:
                    print(f"OKU ({', '.join(kokler)}): {c[:150]}")
    print("SORUN YOK" if not sorun else "SORUNLAR:\n  " + "\n  ".join(sorun))
    sys.exit(1 if sorun else 0)


if __name__ == "__main__":
    main()
