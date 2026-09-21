#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Metacritic'ten platform bazında eleştirmen puanını ve eleştirmen sayısını okur.

Kullanım:
    python3 metacritic_pc.py battlefield-6
    python3 metacritic_pc.py mount-and-blade-ii-bannerlord tom-clancys-rainbow-six-siege

Slug, metacritic.com/game/<slug>/ adresindeki parçadır; yanlışsa site yönlendirir, betik yönlendirmeyi izler.

Neden ayrı betik: oyun sayfasının üstündeki puan varsayılan platformunkidir (çoğu zaman konsol).
Sayfa GeForce NOW'un akıttığı PC sürümünü anlattığı için PC puanı gerekir. PC eleştirmen sayfası
(`critic-reviews/?platform=pc`) tüm platformların puanını ve eleştirmen sayısını sayfaya gömülü
`__NUXT_DATA__` dizisinde taşır; değerler dizide indeksle birbirine bağlıdır, betik bunları çözer.
Kullanıcı puanı platform bazında ayrışmadığı için burada okunmaz (bkz. references/dogrulama.md).
"""
import json, re, subprocess, sys

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/124 Safari/537.36"
PLATFORMLAR = ("PC", "PlayStation 5", "PlayStation 4", "Xbox Series X", "Xbox One", "Nintendo Switch", "Nintendo Switch 2")


def getir(url):
    return subprocess.run(["curl", "-sL", "--max-time", "30", "-A", UA, url], capture_output=True, text=True).stdout


def puanlar(slug):
    h = getir(f"https://www.metacritic.com/game/{slug}/critic-reviews/?platform=pc")
    m = re.search(r'<script[^>]*id="__NUXT_DATA__"[^>]*>(.*?)</script>', h, re.S)
    if not m:
        return {}
    a = json.loads(m.group(1))
    coz = lambda v: a[v] if isinstance(v, int) and 0 <= v < len(a) else v
    sonuc = {}
    for i, x in enumerate(a[:-1]):
        d = a[i + 1]
        if x in PLATFORMLAR and isinstance(d, dict) and "score" in d and "reviewCount" in d:
            skor, sayi = coz(d["score"]), coz(d["reviewCount"])
            if isinstance(skor, (int, float)) and isinstance(sayi, int) and x not in sonuc:
                sonuc[x] = (skor, sayi)
    return sonuc


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    for slug in sys.argv[1:]:
        p = puanlar(slug)
        if not p:
            print(f"{slug}: puan okunamadı (slug ya da sayfa yapısı değişmiş olabilir; sayfayı elle kontrol et)")
            continue
        dok = " | ".join(f"{k} {v[0]}/100 ({v[1]} eleştirmen)" for k, v in p.items())
        pc = p.get("PC")
        print(f"{slug}: " + (f"PC {pc[0]}/100 ({pc[1]} eleştirmen)" if pc else "PC puanı yok") + f"  ·  döküm: {dok}")
