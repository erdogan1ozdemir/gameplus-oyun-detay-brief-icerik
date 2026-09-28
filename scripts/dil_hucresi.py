#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Oyunun resmi dil desteğini GeForce NOW katalog dökümünden (gfn_apps_TR.json) okuyup brief hücresine çevirir.

Kullanım:
    python3 dil_hucresi.py "Forza Horizon 6"

Neden: dil verisi GeForce NOW'un kendi kaydından okunur, ama esas alınan PC listesidir (kullanıcı kararı,
28.09.2026): Xbox variantı PC sürümünde olmayan katmanları gösterebildiği için (007 First Light ve Age of Empires
IV'te Türkçe dublaj görünüyor, PC sürümünde yok) PC mağaza variantı varken Xbox listesi hesaba katılmaz.
Kayıt mağaza variantı başına dil ve kapsam taşır: ux = menü, subtitles = altyazı, speech = seslendirme.
Her brief'te Türkçe satırı `dil_teyit.py` ile Steam dil tablosuna karşı teyit edilir ve hücreye teyitli satır
yazılır (hucre(g, dogrulama=...)). İçerikte mağaza farkı yazılmaz.
"""
import json, os, re, sys, unicodedata

VARSAYILAN = [os.path.expanduser("~/Desktop/Claude Projects/Game+  copy/Veri Dosyaları/gfn_apps_TR.json"),
              os.path.expanduser("~/Downloads/gfn_apps_TR.json")]

AD = {"en_us":"İngilizce","en_gb":"İngilizce (Birleşik Krallık)","fr_fr":"Fransızca","fr_ca":"Fransızca (Kanada)",
"de_de":"Almanca","es_es":"İspanyolca","es_mx":"İspanyolca (Latin Amerika)","ru_ru":"Rusça","zh_cn":"Çince (Basitleştirilmiş)",
"zh_tw":"Çince (Geleneksel)","zh_sg":"Çince (Singapur)","ja_jp":"Japonca","it_it":"İtalyanca","pt_br":"Portekizce (Brezilya)",
"pt_pt":"Portekizce","ko_kr":"Korece","pl_pl":"Lehçe","tr_tr":"Türkçe","cs_cz":"Çekçe","nl_nl":"Felemenkçe","uk_ua":"Ukraynaca",
"ar_sa":"Arapça","hu_hu":"Macarca","th_th":"Tayca","sv_se":"İsveççe","da_dk":"Danca","fi_fi":"Fince","nb_no":"Norveççe",
"ro_ro":"Rumence","el_gr":"Yunanca","vi_vn":"Vietnamca","id_id":"Endonezyaca","bg_bg":"Bulgarca","sk_sk":"Slovakça",
"hi_in":"Hintçe","ca_es":"Katalanca","lt_lt":"Litvanca","ms_my":"Malayca","hr_hr":"Hırvatça","sr_rs":"Sırpça","et_ee":"Estonca",
"eu_es":"Baskça","fa_ir":"Farsça","sl_si":"Slovence","is_is":"İzlandaca","he_il":"İbranice","gl_es":"Galiçyaca","lv_lv":"Letonca",
"be_by":"Belarusça","mk_mk":"Makedonca","ka_ge":"Gürcüce","kk_kz":"Kazakça","ta_in":"Tamilce","af_za":"Afrikaanca",
"kn_in":"Kannada","mr_in":"Marathi","te_in":"Telugu","gu_in":"Gucaratça","tt_ru":"Tatarca","mn_mn":"Moğolca"}
SIRA = list(AD)  # yaygınlık sırasına yakın


def dil_ozet(g):
    """Mağaza variantlarının birleşimi: dil -> {ux, subtitles, speech}."""
    m, bos = {}, True
    for v in g.get("variants", []):
        sl = (v.get("gfn") or {}).get("supportedLanguages")
        if sl: bos = False
        for l in sl or []:
            m.setdefault(l["language"].lower(), set()).update(l.get("availableFeatures") or [])
    return (None if bos else m)

def listele(m, ozellik):
    k = [c for c in m if ozellik in m[c]]
    k.sort(key=lambda c: (SIRA.index(c) if c in SIRA else 999, c))
    return ", ".join(AD.get(c, c) for c in k) or "-"

MAGAZA = {"STEAM": "Steam", "EPIC": "Epic", "XBOX": "Xbox", "GOG": "GOG", "EA_APP": "EA App", "BATTLENET": "Battle.net",
          "UPLAY": "Ubisoft Connect", "UBISOFT": "Ubisoft Connect", "ORIGIN": "EA App", "GAIJIN": "Gaijin",
          "WARGAMING": "Wargaming", "NV_BUNDLE": "NVIDIA paketi", "NVIDIA": "NVIDIA",
          "UNKNOWN": "yayıncının kendi başlatıcısı", "NONE": "yayıncının kendi başlatıcısı"}

def kapsam(f):
    return " + ".join(ad for kod, ad in (("ux", "Arayüz"), ("subtitles", "Altyazı"), ("speech", "Seslendirme")) if kod in f)

def turkce(g):
    """Türkçe durumu mağaza variantı bazında okunur. Türkçe bazı mağazalarda yoksa "(yalnız X)", katmanlar
    mağazaya göre değişiyorsa "(Seslendirme yalnız Xbox)" gibi not düşülür."""
    var, yok = {}, []
    for v in g.get("variants", []):
        sl = (v.get("gfn") or {}).get("supportedLanguages") or []
        if not sl: continue
        mag = MAGAZA.get(v["appStore"] or "NONE", str(v["appStore"]).title())
        f = set().union(*[set(l.get("availableFeatures") or []) for l in sl if l["language"].lower() == "tr_tr"])
        if f: var[mag] = var.get(mag, set()) | f
        else: yok.append(mag)
    if not var and not yok: return "Veri yok"
    if not var: return "Yok"
    ortak = set.intersection(*var.values()); hepsi = set().union(*var.values())
    notlar = [f"yalnız {', '.join(sorted(var))}"] if yok else []
    for kod, ad in (("ux", "Arayüz"), ("subtitles", "Altyazı"), ("speech", "Seslendirme")):
        if kod in hepsi - ortak:
            notlar.append(f"{ad} yalnız {', '.join(sorted(m for m, f in var.items() if kod in f))}")
    return (kapsam(ortak) or kapsam(hepsi)) + (f" ({'; '.join(notlar)})" if notlar else "")


TERIM = (("ux", "Menü"), ("subtitles", "Altyazı"), ("speech", "Türkçe dublaj"))


def pc_variantlari(g):
    """Dil verisi olan variantlar; PC mağaza variantı varsa Xbox dışarıda kalır. (variantlar, yalniz_xbox)"""
    vs = [v for v in g.get("variants", []) if (v.get("gfn") or {}).get("supportedLanguages")]
    pc = [v for v in vs if v["appStore"] != "XBOX"]
    return (pc, False) if pc else (vs, bool(vs))


def turkce_satiri(g):
    """PC listesinden Türkçe satırı; terimler Menü, Altyazı, Türkçe dublaj. PC mağazaları ayrışıyorsa ya da
    yalnız Xbox verisi varsa teyit gerektiğini döndürür."""
    vs, yalniz_xbox = pc_variantlari(g)
    var, yok = {}, []
    for v in vs:
        sl = v["gfn"]["supportedLanguages"]
        f = set().union(*[set(l.get("availableFeatures") or []) for l in sl if l["language"].lower() == "tr_tr"])
        (var.setdefault(v["appStore"], set()).update(f) if f else yok.append(v["appStore"]))
    if not var and not yok: return "Türkçe: Veri yok (GeForce NOW kaydında dil listesi boş; Steam'den bakılır)", True
    if not var: return "Türkçe: Yok" + (" (yalnız Xbox listesi var)" if yalniz_xbox else ""), yalniz_xbox
    hepsi = set().union(*var.values()); ortak = set.intersection(*var.values())
    satir = "Türkçe: " + " + ".join(ad for kod, ad in TERIM if kod in hepsi)
    return satir + (" (yalnız Xbox listesi var)" if yalniz_xbox else ""), bool(yok) or hepsi != ortak or yalniz_xbox


def hucre(g, dogrulama=None):
    """Brief'in 'Resmi Dil Desteği (PC)' hücresi. dogrulama: dil_teyit.py ile teyit edilmiş Türkçe satırı.
    Listeler PC mağaza sürümlerinde ortak dillerdir, bir mağazadaki fazlalık ayrıca yazılır."""
    if g is None: return "GeForce NOW kaydı bulunamadı."
    vs, _ = pc_variantlari(g)
    magaza = {}
    for v in vs:
        mg = MAGAZA.get(v["appStore"] or "NONE", str(v["appStore"]).title())
        for l in v["gfn"]["supportedLanguages"]:
            for f in l.get("availableFeatures") or []:
                magaza.setdefault(mg, {}).setdefault(f, set()).add(l["language"].lower())
    tr, ayrisiyor = turkce_satiri(g)
    satirlar = [dogrulama or tr]
    if not dogrulama:
        satirlar.append("Teyit edilmedi: dil_teyit.py ile Steam dil tablosuna karşı teyit edilir"
                        + ("; PC listeleri ayrışıyor, yayıncı kaynağına da bakılır." if ayrisiyor else "."))
    if not magaza: return "\n".join(satirlar)
    satirlar.append("")
    sirala = lambda k: sorted(k, key=lambda c: (SIRA.index(c) if c in SIRA else 999, c))
    for kod, ad in (("ux", "Menü"), ("subtitles", "Altyazı"), ("speech", "Seslendirme")):
        kumeler = [m.get(kod, set()) for m in magaza.values()]
        ortak = set.intersection(*kumeler) if kumeler else set()
        metin = ", ".join(AD.get(c, c) for c in sirala(ortak)) or "-"
        fazla = [f"{mg} listesinde +{len(m.get(kod, set()) - ortak)} dil" for mg, m in sorted(magaza.items())
                 if len(magaza) > 1 and m.get(kod, set()) - ortak]
        satirlar.append(f"{ad} ({len(ortak)}): {metin}" + (f" · {'; '.join(fazla)}" if fazla else ""))
    return "\n".join(satirlar)


def normalize(s):
    for ch in "®™©℠": s = (s or "").replace(ch, "")
    s = unicodedata.normalize("NFKD", s); s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", " ", s.replace("İ", "i").replace("I", "i").lower()).strip()


def bul(oyun, yol=None):
    yol = yol or next((p for p in VARSAYILAN if os.path.exists(p)), None)
    if not yol: return None
    items = json.load(open(yol, encoding="utf-8"))["items"]
    idx = {normalize(g["title"]): g for g in items}
    n = normalize(oyun)
    return idx.get(n) or next((v for k, v in idx.items() if n in k or k in n), None)


if __name__ == "__main__":
    if len(sys.argv) < 2: sys.exit('kullanım: python3 dil_hucresi.py "Oyun Adı"')
    g = bul(sys.argv[1])
    print((g["title"] + "\n\n") if g else "", hucre(g), sep="")
