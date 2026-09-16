#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Oyunu GFN katalog Excel'inde bulur ve brief için gereken alanları JSON basar.

Kullanım:
    python3 katalog.py "Battlefield 6" [--xlsx /yol/gameplus-oyun-katalogu-ve-top100.xlsx]

Katalog dosyası verilmezse bilinen yollarda aranır. Oyun adı kısmi eşleşmeyle bulunur;
birden fazla eşleşme varsa hepsi listelenir ve seçim kullanıcıya bırakılır.
"""
import argparse, json, os, sys, unicodedata, re

VARSAYILAN = [
    os.path.expanduser("~/Desktop/Claude Projects/Game+  copy/gameplus-oyun-katalogu-ve-top100.xlsx"),
    os.path.expanduser("~/Downloads/gameplus-oyun-katalogu-ve-top100.xlsx"),
]
ALANLAR = ["Oyun", "Aratılacak oyun adı", "2026 avg search vol.", "2026 clickstream arama hacmi",
           "Türler", "Yayıncı", "Geliştirici", "Mağazalar", "GFN optimizasyon", "Üyelik seviyesi",
           "RTX", "HDR", "Reflex", "NVIDIA teknolojileri", "Kontroller", "Maks. çevrimiçi oyuncu",
           "Derecelendirme", "Yaş sınıfı", "En erken çıkış tarihi", "Mağaza satış tarihi",
           "Türkçe anahtar kelime sayısı", "Oyuna özgü tagler", "Kısa açıklama", "id", "cmsId"]


def normalize(s):
    # ® ™ © önce atılır: NFKD bunları "R", "TM", "C" harflerine açıp eşleşmeyi bozuyor
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
    ap.add_argument("--xlsx")
    a = ap.parse_args()

    yol = a.xlsx or next((p for p in VARSAYILAN if os.path.exists(p)), None)
    if not yol or not os.path.exists(yol):
        sys.exit("Katalog Excel'i bulunamadı; --xlsx ile yol verin.")

    from openpyxl import load_workbook
    ws = load_workbook(yol, data_only=True)["GFN Oyun Kataloğu"]
    bas = {ws.cell(row=1, column=c).value: c for c in range(1, ws.max_column + 1)}
    hedef = normalize(a.oyun)

    bulunan = []
    for r in range(2, ws.max_row + 1):
        ad = ws.cell(row=r, column=bas["Oyun"]).value
        if not ad:
            continue
        n = normalize(ad)
        if n == hedef or hedef in n:
            bulunan.append({f: ws.cell(row=r, column=bas[f]).value for f in ALANLAR if f in bas})

    if not bulunan:
        sys.exit(f"'{a.oyun}' katalogda bulunamadı.")
    for k in bulunan:
        for alan, deger in list(k.items()):
            if hasattr(deger, "isoformat"):
                k[alan] = deger.isoformat()[:10]
    print(json.dumps({"eslesme": len(bulunan), "kayitlar": bulunan}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
