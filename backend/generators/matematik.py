"""
Matematik prosedurel soru uretecleri.

Her uretecte celdiriciler COCUGUN GERCEKTE YAPTIGI HATALARDAN uretilir.
Rastgele celdirici kullanilirsa cocuk sikki eleyerek bulur, ogrenmez.
"""
import random

from .base import register, finalize, pick3


# ---------------------------------------------------------------- TOPLAMA

TOPLAMA_RANGE = {
    # (sinif, band): (min, max)
    (1, 1): (1, 5),   (1, 2): (1, 9),   (1, 3): (2, 10),
    (1, 4): (5, 15),  (1, 5): (5, 20),
    (2, 1): (5, 20),  (2, 2): (10, 40), (2, 3): (10, 60),
    (2, 4): (20, 89), (2, 5): (30, 99),
    (3, 1): (20, 80), (3, 2): (50, 200), (3, 3): (100, 500),
    (3, 4): (200, 800), (3, 5): (300, 999),
    (4, 1): (100, 500), (4, 2): (200, 1500), (4, 3): (500, 4000),
    (4, 4): (1000, 7000), (4, 5): (2000, 9999),
}


def _toplama_celdirici(dogru: int, a: int, b: int) -> list:
    """Elde unutma, basamak kaymasi, cikarma ile karistirma."""
    adaylar = {
        a - b if a > b else b - a,   # islem karistirma (+ yerine -)
        dogru - 10,                  # elde unutma
        dogru + 10,                  # fazladan elde
        dogru - 1,                   # sayma hatasi
        dogru + 1,
        dogru - 9,
        dogru + 9,
    }
    adaylar = {x for x in adaylar if x > 0}
    return pick3(adaylar, dogru)


@register("toplama")
def gen_toplama(grade: int, band: int) -> dict:
    lo, hi = TOPLAMA_RANGE.get((grade, band), (1, 20))
    a = random.randint(lo, hi)
    b = random.randint(lo, hi)
    dogru = a + b
    return finalize(
        f"{a} + {b} = ?", dogru, _toplama_celdirici(dogru, a, b), band,
        explanation=f"{a} + {b} = {dogru}",
    )


# ---------------------------------------------------------------- CIKARMA

def _cikarma_celdirici(dogru: int, a: int, b: int) -> list:
    """Onluk bozmayi unutma, ters cikarma, toplama ile karistirma."""
    adaylar = {
        a + b,          # islem karistirma (- yerine +)
        dogru + 10,     # onluk bozmayi unutma
        dogru - 10,
        dogru + 1,
        dogru - 1,
        abs(b - a),     # ters cikarma refleksi
        dogru + 9,
    }
    adaylar = {x for x in adaylar if x >= 0}
    return pick3(adaylar, dogru)


@register("cikarma")
def gen_cikarma(grade: int, band: int) -> dict:
    lo, hi = TOPLAMA_RANGE.get((grade, band), (1, 20))
    a = random.randint(lo + 2, hi)
    b = random.randint(lo, max(lo, a - 1))
    dogru = a - b
    return finalize(
        f"{a} - {b} = ?", dogru, _cikarma_celdirici(dogru, a, b), band,
        explanation=f"{a} - {b} = {dogru}",
    )


# --------------------------------------------------- TOPLAMA-CIKARMA (karma)

@register("toplama_cikarma")
def gen_toplama_cikarma(grade: int, band: int) -> dict:
    return random.choice([gen_toplama, gen_cikarma])(grade, band)


# ---------------------------------------------------------------- CARPIM

CARPIM_RANGE = {
    # 2. sinif: SADECE 1-5 tablosu (MEB mufredati)
    (2, 1): (2, 3), (2, 2): (2, 4), (2, 3): (2, 5),
    (2, 4): (3, 5), (2, 5): (4, 5),
    # 3. sinif: 1-10 tablosu
    (3, 1): (2, 5), (3, 2): (2, 7), (3, 3): (2, 10),
    (3, 4): (4, 10), (3, 5): (6, 10),
    # 4. sinif: cok basamakli
    (4, 1): (2, 10), (4, 2): (5, 12), (4, 3): (10, 30),
    (4, 4): (10, 60), (4, 5): (12, 99),
}

CARPIM_B_MAX = {2: 5, 3: 10, 4: 9}


def _carpim_celdirici(dogru: int, a: int, b: int) -> list:
    """Komsu satir/sutun, toplama ile karistirma, elde hatasi."""
    adaylar = {
        (a + 1) * b,    # komsu satir
        (a - 1) * b,    # komsu satir
        a * (b + 1),    # komsu sutun
        a * (b - 1),    # komsu sutun
        a + b,          # islem karistirma
        dogru + 10,     # elde hatasi
        dogru - 10,
    }
    adaylar = {x for x in adaylar if x > 0}
    return pick3(adaylar, dogru)


@register("carpim")
def gen_carpim(grade: int, band: int) -> dict:
    lo, hi = CARPIM_RANGE.get((grade, band), (2, 5))
    b_max = CARPIM_B_MAX.get(grade, 5)
    a = random.randint(lo, hi)
    b = random.randint(2, b_max)
    dogru = a * b
    return finalize(
        f"{a} × {b} = ?", dogru, _carpim_celdirici(dogru, a, b), band,
        explanation=f"{a} × {b} = {dogru}",
    )


# ---------------------------------------------------------------- BOLME
# 3. sinif ve uzeri (2. sinifta bolme YOKTUR)

def _bolme_celdirici(dogru: int, a: int, b: int) -> list:
    """Carpma ile karistirma, komsu deger."""
    adaylar = {
        a * b,          # islem karistirma
        dogru + 1,
        dogru - 1,
        dogru + 2,
        b,              # boleni cevap sanma
        a - b,
    }
    adaylar = {x for x in adaylar if x > 0}
    return pick3(adaylar, dogru)


@register("bolme")
def gen_bolme(grade: int, band: int) -> dict:
    ranges = {1: (2, 5), 2: (2, 6), 3: (2, 9), 4: (3, 10), 5: (4, 12)}
    lo, hi = ranges.get(band, (2, 5))
    b = random.randint(2, min(hi, 10))
    sonuc = random.randint(lo, hi)
    a = b * sonuc                       # kalansiz garanti
    return finalize(
        f"{a} ÷ {b} = ?", sonuc, _bolme_celdirici(sonuc, a, b), band,
        explanation=f"{a} ÷ {b} = {sonuc}",
    )


# ---------------------------------------------------------------- SAYILAR

@register("sayilar")
def gen_sayilar(grade: int, band: int) -> dict:
    """Siralama / karsilastirma / oncesi-sonrasi."""
    limits = {1: 20, 2: 100, 3: 1000, 4: 10000}
    limit = limits.get(grade, 100)
    tip = random.choice(["buyuk", "kucuk", "sonraki", "onceki", "sirala"])

    if tip in ("buyuk", "kucuk"):
        sayilar = random.sample(range(1, limit + 1), 4)
        dogru = max(sayilar) if tip == "buyuk" else min(sayilar)
        soru = "En büyük sayı hangisidir?" if tip == "buyuk" else "En küçük sayı hangisidir?"
        digerleri = [s for s in sayilar if s != dogru]
        # Siklarin kendisi zaten sayilar -> ayrica metinde gostermeye gerek yok
        return finalize(soru, dogru, digerleri, band,
                        explanation=f"Doğru cevap: {dogru}")

    if tip in ("sonraki", "onceki"):
        n = random.randint(2, limit - 2)
        dogru = n + 1 if tip == "sonraki" else n - 1
        soru = f"{n} sayısından sonra gelen sayı hangisidir?" if tip == "sonraki" \
            else f"{n} sayısından önce gelen sayı hangisidir?"
        adaylar = {n, n + 2, n - 2, dogru + 1, dogru - 1}
        return finalize(soru, dogru, pick3(adaylar, dogru), band,
                        explanation=f"{dogru}")

    # sirala: kucukten buyuge dizinin dogru hali
    # 3 sayinin 6 permutasyonu var -> dogru haric 5 celdirici garantili
    import itertools
    sayilar = random.sample(range(1, limit + 1), 3)
    sirali = sorted(sayilar)

    def fmt(seq):
        return " < ".join(str(x) for x in seq)

    dogru = fmt(sirali)
    tum_perm = [fmt(p) for p in itertools.permutations(sayilar)]
    yanlis = [p for p in tum_perm if p != dogru]
    random.shuffle(yanlis)

    return finalize(
        "Bu sayıları küçükten büyüğe doğru sıralayan hangisidir?",
        dogru, yanlis, band, explanation=dogru,
    )


# ---------------------------------------------------------------- BASAMAK

BASAMAK_ADI = ["birler", "onlar", "yüzler", "binler", "on binler"]


@register("basamak")
def gen_basamak(grade: int, band: int) -> dict:
    haneler = {1: 2, 2: 2, 3: 3, 4: 4}
    h = haneler.get(grade, 2)
    if grade >= 3 and band >= 4:
        h += 1

    lo = 10 ** (h - 1)
    hi = 10 ** h - 1
    n = random.randint(lo, hi)
    s = str(n)

    idx = random.randint(0, h - 1)                 # 0 = birler
    rakam = int(s[-(idx + 1)])
    ad = BASAMAK_ADI[idx]

    # Celdirici: sayidaki diger rakamlar (komsu basamak hatasi) + yakin rakamlar
    adaylar = {int(c) for c in s if int(c) != rakam}
    adaylar |= {rakam + 1, rakam - 1, rakam + 2}
    adaylar = {x for x in adaylar if 0 <= x <= 9 and x != rakam}

    # Rakam her zaman tek haneli olmali
    ek = [x for x in range(10) if x != rakam and x not in adaylar]
    random.shuffle(ek)
    while len(adaylar) < 3 and ek:
        adaylar.add(ek.pop())

    return finalize(
        f"{n} sayısının {ad} basamağındaki rakam kaçtır?",
        rakam, pick3(adaylar, rakam), band,
        explanation=f"{n} → {ad} basamağı = {rakam}",
    )


# ---------------------------------------------------------------- RITMIK

RITMIK_ADIM = {1: [2, 5, 10], 2: [2, 3, 4, 5, 10], 3: [3, 4, 6, 7, 8, 9], 4: [6, 7, 8, 9]}


@register("ritmik")
def gen_ritmik(grade: int, band: int) -> dict:
    adimlar = RITMIK_ADIM.get(grade, [2, 5])
    adim = random.choice(adimlar)
    geri = band >= 4 and grade >= 2 and random.random() < 0.3

    if geri:
        bas = adim * random.randint(5, 12)
        dizi = [bas - adim * i for i in range(4)]
    else:
        bas = adim * random.randint(1, 5)
        dizi = [bas + adim * i for i in range(4)]

    dogru = dizi[-1]
    gosterim = ", ".join(str(x) for x in dizi[:-1]) + ", ?"

    adaylar = {
        dogru + adim, dogru - adim,      # bir adim kayma
        dogru + 1, dogru - 1,            # sayma hatasi
        dizi[-2] + 1,
    }
    adaylar = {x for x in adaylar if x > 0}

    yon = "geriye" if geri else "ileriye"
    return finalize(
        f"{gosterim}\n({adim}'şer {yon} sayıyoruz)",
        dogru, pick3(adaylar, dogru), band,
        explanation=f"{dizi[-2]} {'-' if geri else '+'} {adim} = {dogru}",
    )


# ---------------------------------------------------------------- SAAT

def _saat_svg(saat: int, dakika: int) -> str:
    """Analog saat SVG'si uretir."""
    import math
    cx = cy = 100
    r = 90

    # Akrep: saat + dakika kaymasi
    akrep_aci = (saat % 12) * 30 + dakika * 0.5 - 90
    yelkovan_aci = dakika * 6 - 90

    ax = cx + 45 * math.cos(math.radians(akrep_aci))
    ay = cy + 45 * math.sin(math.radians(akrep_aci))
    yx = cx + 72 * math.cos(math.radians(yelkovan_aci))
    yy = cy + 72 * math.sin(math.radians(yelkovan_aci))

    rakamlar = ""
    for i in range(1, 13):
        aci = i * 30 - 90
        x = cx + 72 * math.cos(math.radians(aci))
        y = cy + 72 * math.sin(math.radians(aci))
        rakamlar += (f'<text x="{x:.1f}" y="{y + 6:.1f}" text-anchor="middle" '
                     f'font-size="16" font-weight="600" fill="#334155">{i}</text>')

    cizgiler = ""
    for i in range(60):
        aci = math.radians(i * 6 - 90)
        uzun = i % 5 == 0
        r1 = r - (10 if uzun else 5)
        x1 = cx + r1 * math.cos(aci); y1 = cy + r1 * math.sin(aci)
        x2 = cx + r * math.cos(aci);  y2 = cy + r * math.sin(aci)
        cizgiler += (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                     f'stroke="#94a3b8" stroke-width="{2 if uzun else 1}"/>')

    return f'''<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg" width="200" height="200">
<circle cx="{cx}" cy="{cy}" r="{r}" fill="#fff" stroke="#1e293b" stroke-width="4"/>
{cizgiler}{rakamlar}
<line x1="{cx}" y1="{cy}" x2="{ax:.1f}" y2="{ay:.1f}" stroke="#1e293b" stroke-width="6" stroke-linecap="round"/>
<line x1="{cx}" y1="{cy}" x2="{yx:.1f}" y2="{yy:.1f}" stroke="#3b82f6" stroke-width="4" stroke-linecap="round"/>
<circle cx="{cx}" cy="{cy}" r="6" fill="#1e293b"/>
</svg>'''


SAAT_DAKIKA = {
    # (sinif, band): olasi dakikalar
    (2, 1): [0], (2, 2): [0, 30], (2, 3): [0, 30],
    (2, 4): [0, 15, 30, 45], (2, 5): [0, 15, 30, 45],
    (3, 1): [0, 30], (3, 2): [0, 15, 30, 45], (3, 3): list(range(0, 60, 5)),
    (3, 4): list(range(0, 60, 5)), (3, 5): list(range(0, 60, 5)),
    (4, 1): [0, 15, 30, 45], (4, 2): list(range(0, 60, 5)),
    (4, 3): list(range(0, 60, 5)), (4, 4): list(range(0, 60)),
    (4, 5): list(range(0, 60)),
}


def _fmt(s: int, d: int) -> str:
    return f"{s}:{d:02d}"


@register("saat")
def gen_saat(grade: int, band: int) -> dict:
    dakikalar = SAAT_DAKIKA.get((grade, band), [0, 30])
    saat = random.randint(1, 12)
    dakika = random.choice(dakikalar)
    dogru = _fmt(saat, dakika)

    # Tipik hatalar: akrep/yelkovan karistirma, saat kaymasi, yarim saat kaymasi
    adaylar = {
        _fmt(saat % 12 + 1, dakika),                  # 1 saat ileri
        _fmt((saat - 2) % 12 + 1, dakika),            # 1 saat geri
        _fmt(saat, (dakika + 30) % 60),               # yarim saat kayma
        _fmt(saat, (dakika + 15) % 60),               # ceyrek kayma
        _fmt(max(1, dakika // 5) if dakika else 12, (saat * 5) % 60),  # akrep/yelkovan ters
    }

    return finalize(
        "Saat kaçı gösteriyor?", dogru, pick3(adaylar, dogru), band,
        explanation=f"Saat {dogru}", svg=_saat_svg(saat, dakika),
    )


# ---------------------------------------------------------------- PARA

PARA_BIRIM = [1, 5, 10, 20, 50]


@register("para")
def gen_para(grade: int, band: int) -> dict:
    tip = random.choice(["topla", "ustu"]) if grade >= 2 and band >= 3 else "topla"

    if tip == "topla":
        adet = 2 if band <= 2 else 3
        paralar = [random.choice(PARA_BIRIM) for _ in range(adet)]
        dogru = sum(paralar)
        gosterim = " + ".join(f"{p}₺" for p in paralar)
        adaylar = {
            dogru + 5, dogru - 5, dogru + 10, dogru - 10,
            dogru + 1, dogru - 1,
        }
        adaylar = {x for x in adaylar if x > 0}
        return finalize(
            f"{gosterim} = kaç ₺?", f"{dogru}₺",
            [f"{x}₺" for x in pick3(adaylar, dogru)], band,
            explanation=f"{gosterim} = {dogru}₺", emoji="💰",
        )

    # para ustu
    fiyat = random.randint(3, 45)
    verilen = random.choice([x for x in [10, 20, 50, 100] if x > fiyat])
    dogru = verilen - fiyat
    adaylar = {
        verilen + fiyat,          # islem karistirma
        dogru + 10, dogru - 10,
        dogru + 1, dogru - 1,
        fiyat,
    }
    adaylar = {x for x in adaylar if x > 0}
    return finalize(
        f"{fiyat}₺'lik bir oyuncak aldın. {verilen}₺ verdin.\nKaç ₺ para üstü alırsın?",
        f"{dogru}₺", [f"{x}₺" for x in pick3(adaylar, dogru)], band,
        explanation=f"{verilen} - {fiyat} = {dogru}₺", emoji="🧸",
    )


# ---------------------------------------------------------------- ORUNTU

ORUNTU_EMOJI = ["🔴", "🔵", "🟡", "🟢", "🟣", "🟠"]
ORUNTU_SEKIL = ["▲", "■", "●", "◆", "★"]


@register("oruntu")
def gen_oruntu(grade: int, band: int) -> dict:
    if grade == 1 or band <= 2:
        # Renk/sekil oruntusu
        havuz = random.choice([ORUNTU_EMOJI, ORUNTU_SEKIL])
        periyot = 2 if band <= 2 else 3
        birim = random.sample(havuz, periyot)
        dizi = (birim * 3)[:6]
        dogru = birim[6 % periyot]
        gosterim = " ".join(dizi) + " ?"
        digerleri = [x for x in havuz if x != dogru][:3]
        return finalize(
            f"Örüntüyü tamamla:\n{gosterim}", dogru, digerleri, band,
            explanation=f"Örüntü {periyot}'li tekrar ediyor.",
        )

    # Sayi oruntusu
    tip = random.choice(["artan", "carpan"]) if band >= 4 and grade >= 3 else "artan"
    if tip == "artan":
        adim = random.randint(2, 9)
        bas = random.randint(1, 20)
        dizi = [bas + adim * i for i in range(4)]
    else:
        carpan = random.randint(2, 3)
        bas = random.randint(1, 4)
        dizi = [bas * (carpan ** i) for i in range(4)]

    dogru = dizi[-1]
    gosterim = ", ".join(str(x) for x in dizi[:-1]) + ", ?"
    adaylar = {dogru + 1, dogru - 1, dogru + 2, dizi[-2] * 2, dizi[-2] + 1}
    adaylar = {x for x in adaylar if x > 0}
    return finalize(
        f"Örüntüyü tamamla:\n{gosterim}", dogru, pick3(adaylar, dogru), band,
        explanation=f"Kural: {'+' if tip == 'artan' else '×'}"
                    f"{adim if tip == 'artan' else carpan}",
    )


# ---------------------------------------------------------------- KESIR
# 3. sinif ve uzeri

@register("kesir")
def gen_kesir(grade: int, band: int) -> dict:
    payda = random.choice([2, 3, 4] if band <= 2 else [2, 3, 4, 5, 6, 8])
    pay = random.randint(1, payda - 1)

    dolu = "🟧" * pay + "⬜" * (payda - pay)
    dogru = f"{pay}/{payda}"
    adaylar = {
        f"{payda - pay}/{payda}",       # tersini sayma
        f"{payda}/{pay}",               # pay/payda ters
        f"{pay}/{payda + 1}",
        f"{pay + 1}/{payda}",
    }
    return finalize(
        f"Turuncu bölüm kesir olarak kaçtır?\n{dolu}",
        dogru, pick3(adaylar, dogru), band,
        explanation=f"{payda} parçanın {pay} tanesi → {dogru}",
    )


# ---------------------------------------------------------------- SAYMA

SAYMA_EMOJI = ["🍎", "🍌", "🐟", "🌸", "⭐", "🚗", "🐝", "🎈"]


@register("sayma")
def gen_sayma(grade: int, band: int) -> dict:
    limits = {1: 10, 2: 20}
    limit = limits.get(grade, 15)
    n = random.randint(2, min(limit, 3 + band * 3))
    emoji = random.choice(SAYMA_EMOJI)
    adaylar = {n + 1, n - 1, n + 2, n - 2}
    adaylar = {x for x in adaylar if x > 0}
    return finalize(
        f"Kaç tane {emoji} var?\n\n{emoji * n}",
        n, pick3(adaylar, n), band, explanation=f"{n} tane",
    )
