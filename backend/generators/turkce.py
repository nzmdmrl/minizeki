"""
Turkce prosedurel soru uretecleri.
"""
import random

from .base import register, finalize, pick3
from .kelime_havuzu import (
    kelimeler_for_grade, turkce_sort_key, SESLI,
)


# ---------------------------------------------------------------- HECE

@register("hece")
def gen_hece(grade: int, band: int) -> dict:
    havuz = kelimeler_for_grade(grade)
    # Band arttikca daha uzun kelimeler
    hedef_min = 1 if band <= 2 else 2
    hedef_max = 2 if band <= 2 else (3 if band <= 4 else 4)
    aday = [k for k in havuz if hedef_min <= len(k[1]) <= hedef_max]
    if not aday:
        aday = havuz

    kelime, heceler, _ = random.choice(aday)
    dogru = len(heceler)

    adaylar = {dogru + 1, dogru - 1, dogru + 2}
    adaylar = {x for x in adaylar if x >= 1}

    return finalize(
        f'"{kelime}" kelimesi kaç hecelidir?',
        dogru, pick3(adaylar, dogru), band,
        explanation=" - ".join(heceler),
    )


# ---------------------------------------------------------------- ALFABETIK

@register("alfabetik")
def gen_alfabetik(grade: int, band: int) -> dict:
    havuz = kelimeler_for_grade(grade)

    # Her zaman 4 kelime: 1 dogru + 3 celdirici = tam 4 sik
    for _ in range(50):
        secim = random.sample(havuz, 4)
        harfler = [k[0][0].lower() for k in secim]
        if len(set(harfler)) == 4:      # band dusukse ilk harfler farkli olsun
            break
    else:
        secim = random.sample(havuz, 4)

    kelimeler = [k[0] for k in secim]
    sirali = sorted(kelimeler, key=turkce_sort_key)

    # Band 4+: bazen "son gelen" sorulur
    son_mu = band >= 4 and random.random() < 0.4
    dogru = sirali[-1] if son_mu else sirali[0]
    soru = "Alfabetik sıraya göre hangisi SON gelir?" if son_mu \
        else "Alfabetik sıraya göre hangisi İLK gelir?"

    return finalize(
        f"{soru}\n\n" + " · ".join(kelimeler),
        dogru, [k for k in kelimeler if k != dogru], band,
        explanation=" → ".join(sirali),
    )


# ---------------------------------------------------------------- EKSIK HARF

@register("eksik_harf")
def gen_eksik_harf(grade: int, band: int) -> dict:
    havuz = kelimeler_for_grade(grade)
    aday = [k for k in havuz if len(k[0]) >= 4]
    kelime = random.choice(aday)[0]

    idx = random.randint(1, len(kelime) - 2)     # bas ve son harf degil
    dogru = kelime[idx]
    gizli = kelime[:idx] + "_" + kelime[idx + 1:]

    # Celdirici: once benzer sesler, sonra ayni tur (sesli/sessiz) harflerle doldur
    benzer = {
        "a": "eı", "e": "ai", "ı": "ai", "i": "ıe",
        "o": "öu", "ö": "oü", "u": "üo", "ü": "uö",
        "b": "pd", "p": "bt", "d": "tb", "t": "dp",
        "c": "çj", "ç": "cs", "s": "şz", "ş": "sç",
        "k": "gh", "g": "kğ", "ğ": "gy", "h": "kg",
        "m": "n", "n": "mr", "r": "ln", "l": "rn",
        "v": "fy", "f": "v", "y": "jğ", "z": "s",
    }
    adaylar = {c for c in benzer.get(dogru, "") if c != dogru}

    # Dogru sesliyse celdiriciler de sesli olsun (aksi halde soru kolaylasir)
    havuz_harf = "aeıioöuü" if dogru in SESLI else "bcçdfgğhjklmnprsştvyz"
    ek = [c for c in havuz_harf if c != dogru and c not in adaylar]
    random.shuffle(ek)
    while len(adaylar) < 3 and ek:
        adaylar.add(ek.pop())

    return finalize(
        f"Eksik harfi bul:\n\n{gizli}",
        dogru, pick3(adaylar, dogru), band,
        explanation=kelime,
    )


# ---------------------------------------------------------------- SESLI HARF

@register("sesli_harf")
def gen_sesli_harf(grade: int, band: int) -> dict:
    havuz = kelimeler_for_grade(grade)
    kelime = random.choice([k for k in havuz if len(k[0]) >= 3])[0]

    tip = random.choice(["kac_sesli", "hangisi_sesli"]) if band >= 3 else "kac_sesli"

    if tip == "kac_sesli":
        dogru = sum(1 for c in kelime.lower() if c in SESLI)
        adaylar = {dogru + 1, dogru - 1, dogru + 2}
        adaylar = {x for x in adaylar if x >= 1}
        sesliler = [c for c in kelime.lower() if c in SESLI]
        return finalize(
            f'"{kelime}" kelimesinde kaç tane sesli harf vardır?',
            dogru, pick3(adaylar, dogru), band,
            explanation="Sesli harfler: " + ", ".join(sesliler),
        )

    # Hangisi sesli harf?
    dogru = random.choice(list(SESLI))
    sessizler = [c for c in "bcçdfgğhjklmnprsştvyz"]
    return finalize(
        "Aşağıdakilerden hangisi sesli harftir?",
        dogru, random.sample(sessizler, 3), band,
        explanation="Sesli harfler: a, e, ı, i, o, ö, u, ü",
    )


# ---------------------------------------------------------------- ANAGRAM

@register("anagram")
def gen_anagram(grade: int, band: int) -> dict:
    havuz = kelimeler_for_grade(grade)
    uzunluk = (4, 5) if band <= 3 else (5, 8)
    aday = [k for k in havuz if uzunluk[0] <= len(k[0]) <= uzunluk[1]]
    if not aday:
        aday = [k for k in havuz if len(k[0]) >= 4]

    dogru = random.choice(aday)[0]
    harfler = list(dogru)
    random.shuffle(harfler)
    karisik = " ".join(h.upper() for h in harfler)

    # Celdirici: ayni uzunlukta baska kelimeler
    digerleri = [k[0] for k in havuz if len(k[0]) == len(dogru) and k[0] != dogru]
    if len(digerleri) < 3:
        digerleri = [k[0] for k in havuz if k[0] != dogru]

    return finalize(
        f"Bu harflerden hangi kelime oluşur?\n\n{karisik}",
        dogru, random.sample(digerleri, min(3, len(digerleri))), band,
        explanation=dogru,
    )
