"""
Bant dagilimi (zorluk) + sinif dagilimi (spiral mufredat).

KALIBRASYON NOTU (simulasyon bulgusu):
  Bantlarin hedef dogruluk degerleri:
    band 1 = %90 | band 2 = %75 | band 3 = %60 | band 4 = %40 | band 5 = %20

  Sistemin hedefi %75-85 dogruluk (yakinsal gelisim alani).
  Level'i dogrudan band'a eslersek (lvl3 -> band3) cocuk %60 alir — hedefin
  altinda, motivasyon kirici.

  Bu yuzden level -> band eslemesi BIR KADEME ASAGI kaydirilir:
    lvl 1 -> band 1 (%90) | lvl 2 -> band 1-2 | lvl 3 -> band 2 (%75)
    lvl 4 -> band 3 (%60-75 arasi) | lvl 5 -> band 4 (%40-60, ustalar icin)

  Boylece cogunluk %75-85 bandinda kalir; level 5'e ulasan cocuk zorlanir
  ama bu zaten terfi (ust sinif) sinyalidir.
"""
import random

import config as cfg

# level -> merkez band
LEVEL_TO_BAND = {1: 1, 2: 2, 3: 2, 4: 3, 5: 4}


def durum_belirle(level: int, son_dogruluk: float | None, toplam: int) -> str:
    """
    Hedef: %75-85 dogruluk (yakinsal gelisim alani).

    Esikler seviye guncellemesiyle CAKISMAMALI: seviye zaten 3-dogru/2-yanlis
    ile hareket ediyor. Bu fonksiyon sadece ince ayar yapar.
    """
    if toplam < 8:
        return "yeni"                # kalibrasyon: genis yelpaze
    if son_dogruluk is None:
        return "normal"
    if son_dogruluk < 0.65:
        return "zorlaniyor"          # eziliyor -> bir alt bant
    if son_dogruluk > 0.88:
        return "sikiliyor"           # cok kolay -> bir ust bant
    return "normal"


def band_sec(level: int, durum: str = "normal") -> int:
    """
    Cocugun seviyesi merkez alinarak agirlikli bant secimi.

    Agirligin cogu level'in KENDISINDE toplanir; komsu bantlar cesitlilik
    icin az pay alir. Boylece level 5'teki cocuk cogunlukla band 5 gorur,
    level 2'deki cocuk band 2.

    'durum' ince ayar yapar:
      zorlaniyor -> agirlik bir alt banda kayar
      sikiliyor  -> bir ust banda kayar
    """
    if durum == "yeni":
        # Kalibrasyon: genis yelpaze, gercek seviyeyi bulmak icin
        return random.choices([1, 2, 3, 4, 5], weights=[2, 3, 3, 2, 1], k=1)[0]

    merkez = LEVEL_TO_BAND.get(level, 2)
    if durum == "zorlaniyor":
        merkez = max(1, merkez - 1)
    elif durum == "sikiliyor":
        merkez = min(5, merkez + 1)

    # Merkeze uzakliga gore agirlik: 0 uzak=6, 1 uzak=2, 2+ uzak=0
    agirlik = []
    for b in (1, 2, 3, 4, 5):
        d = abs(b - merkez)
        agirlik.append(6 if d == 0 else (2 if d == 1 else 0))

    return random.choices([1, 2, 3, 4, 5], weights=agirlik, k=1)[0]


def sinif_dagilimi(profile_grade: int, repeat_ratio: float,
                   skill_level: int, advanced_unlocked: bool,
                   advance_ratio: float) -> dict[int, float]:
    """
    Spiral mufredat: alt sinif tekrari + ana kutle + ust sinif esnemesi.

    Zayifsa tekrar orani artar, ustalastiysa azalir.
    """
    repeat = repeat_ratio
    if skill_level <= 2:
        repeat = min(repeat + 0.15, 0.40)      # zorlaniyor -> daha cok tekrar
    elif skill_level >= 5:
        repeat = max(repeat - 0.10, 0.05)      # ustalasti -> az tekrar

    advance = advance_ratio if advanced_unlocked else 0.0

    if profile_grade <= 1:
        repeat = 0.0                            # 1. sinifin alti yok
    if profile_grade >= 4:
        advance = 0.0                           # 4. sinifin ustu yok

    main = max(0.0, 1.0 - repeat - advance)

    dist = {}
    if repeat > 0:
        dist[profile_grade - 1] = repeat
    dist[profile_grade] = main
    if advance > 0:
        dist[profile_grade + 1] = advance
    return dist


def sinif_sec(dist: dict[int, float]) -> int:
    grades = list(dist.keys())
    weights = [dist[g] for g in grades]
    if sum(weights) == 0:
        return grades[0]
    return random.choices(grades, weights=weights, k=1)[0]
