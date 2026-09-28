#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Türkçe desteğini PC listesinden teyit eder: GeForce NOW kaydının PC mağaza sürümleri (Xbox hariç) ile
Steam mağaza sayfasındaki dil tablosu (Arayüz / Tam ses / Altyazı) karşılaştırılır.

Kullanım:
    python3 dil_teyit.py "Forza Horizon 6"
    python3 dil_teyit.py "Apex Legends" --appid 1172470     # GFN kaydında Steam sürümü yoksa
    python3 dil_teyit.py --appid 1903340                     # yalnız Steam tablosu

Neden: Xbox listesi PC sürümünde olmayan katmanları gösterebiliyor (007 First Light ve Age of Empires IV'te
Türkçe dublaj görünüyor, PC sürümünde yok). Kullanıcı kararı (28.09.2026): PC listesi esas alınır ve her
brief'te teyit edilir. Steam tablosu ile GFN PC birleşimi uyuşmuyorsa ya da dublaj görünüyorsa sonuç
yayıncı kaynağından (duyuru, resmi SSS) ayrıca doğrulanır; mağaza metaverisi ses seçeneğini listeleyip gerçek
dublaj olmayabiliyor (Overwatch).
"""
import argparse, html, re, subprocess, sys, os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dil_hucresi as dh

TERIM = (("ux", "Menü"), ("subtitles", "Altyazı"), ("speech", "Türkçe dublaj"))


def yaz(f):
    return " + ".join(ad for kod, ad in TERIM if kod in f) or "Yok"


def steam_tablosu(appid):
    """Steam sayfasındaki dil tablosundan Türkçe satırı: {ux, speech, subtitles} kümesi; tablo yoksa None."""
    cerez = "birthtime=0; lastagecheckage=1-0-1900; wants_mature_content=1; Steam_Language=english"
    h = subprocess.run(["curl", "-sL", "--max-time", "25", "-H", f"Cookie: {cerez}",
                        f"https://store.steampowered.com/app/{appid}/?l=english&cc=tr"],
                       capture_output=True, text=True).stdout
    t = re.search(r'<table[^>]*game_language_options[^>]*>.*?</table>', h, re.S)
    if not t: return None, (re.search(r"<title>(.*?)</title>", h, re.S) or [None, "?"])[1].strip()
    ad = html.unescape((re.search(r'id="appHubAppName"[^>]*>(.*?)</div>', h) or [None, "?"])[1])
    for tr in re.findall(r"<tr[^>]*>(.*?)</tr>", t.group(0), re.S):
        hucre = re.findall(r"<td[^>]*>(.*?)</td>", tr, re.S)
        if hucre and re.sub(r"<[^>]+>|\s", "", hucre[0]).lower() == "turkish":
            tik = [bool(re.search(r"&#10004;|✔", c)) for c in hucre[1:4]]
            return {k for k, v in zip(("ux", "speech", "subtitles"), tik) if v}, ad
    return set(), ad


def gfn_pc(g):
    """GFN kaydının PC mağaza sürümlerindeki Türkçe katmanları (Xbox hariç) ve Steam app id'leri."""
    pc, xbox, appids = {}, set(), []
    for v in g.get("variants", []):
        m = re.search(r"/app/(\d+)", v.get("storeUrl") or "")
        if m: appids.append(m.group(1))
        sl = (v.get("gfn") or {}).get("supportedLanguages") or []
        if not sl: continue
        f = set().union(*[set(l.get("availableFeatures") or []) for l in sl if l["language"].lower() == "tr_tr"])
        if v["appStore"] == "XBOX": xbox |= f
        else:
            mg = dh.MAGAZA.get(v["appStore"] or "NONE", str(v["appStore"]).title())
            pc[mg] = pc.get(mg, set()) | f
    return pc, xbox, appids


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("oyun", nargs="?")
    ap.add_argument("--appid", help="Steam app id (GFN kaydında Steam sürümü yoksa)")
    a = ap.parse_args()
    g = dh.bul(a.oyun) if a.oyun else None
    pc, xbox, appids = gfn_pc(g) if g else ({}, set(), [])
    if g:
        print(g["title"])
        for mg, f in pc.items(): print(f"  GFN {mg}: {yaz(f)}")
        if xbox: print(f"  GFN Xbox (esas alınmaz): {yaz(xbox)}")
    elif a.oyun:
        print(f"GFN kaydı bulunamadı: {a.oyun}")
    birlesim = set().union(*pc.values()) if pc else None
    steam = None
    for appid in ([a.appid] if a.appid else appids)[:1]:
        steam, ad = steam_tablosu(appid)
        print(f"  Steam #{appid} ({ad}): " + ("dil tablosu okunamadı" if steam is None else yaz(steam)))
    notlar = []
    if steam is None and birlesim is None:
        notlar.append("PC verisi yok: yayıncı sayfasından teyit edilir.")
    elif steam is None:
        notlar.append("Steam tablosu yok: GFN PC listesi esas; yayıncı ya da Epic sayfasından teyit edilir.")
    elif birlesim is not None and steam != birlesim:
        notlar.append(f"GFN PC birleşimi ({yaz(birlesim)}) ile Steam ({yaz(steam)}) ayrışıyor: yayıncı kaynağından teyit edilir.")
    if "speech" in (steam or set()) | (birlesim or set()):
        notlar.append("Türkçe dublaj görünüyor: yayıncı kaynağından teyit edilmeden yazılmaz.")
    sonuc = steam if steam is not None else birlesim
    print("Sonuç (PC listesi): Türkçe: " + (yaz(sonuc) if sonuc is not None else "Veri yok"))
    for n in notlar: print("TEYİT:", n)
    if not notlar:
        print("Uyumlu: GFN PC listesi ve Steam dil tablosu aynı.")
        print(f"Brief satırı: Türkçe: {yaz(sonuc)} (teyit: Steam dil tablosu)")
    else:
        print("Brief satırı: teyitten sonra yazılır, ör. \"Türkçe: Menü (teyit: Steam dil tablosu; EA kaydındaki altyazı resmi değil)\"")


if __name__ == "__main__":
    main()
