"""
Yildiz, seri (streak), kalkan, rozet.

Kural: Yildiz ASLA ceza olarak alinmaz. Enerji/can sistemi yok.
Seri kirilinca yildiz, rozet, madalya korunur.
"""
from datetime import date, timedelta

from sqlalchemy.orm import Session

import config as cfg
from models import StarEvent, Profile, ProfileBadge, Badge, ProfileSkill, AnswerLog


def yildiz_ver(db: Session, profile: Profile, delta: int, reason: str) -> int:
    """Yildiz ekle/harca. Bakiye event toplamiyla tutulur."""
    db.add(StarEvent(profile_id=profile.id, delta=delta, reason=reason))
    profile.star_balance = (profile.star_balance or 0) + delta
    return profile.star_balance


def _ay_str(d: date) -> str:
    return f"{d.year}-{d.month:02d}"


def kalkan_yenile(profile: Profile, bugun: date) -> None:
    """Ay basinda kalkan hakki yenilenir."""
    ay = _ay_str(bugun)
    if profile.shield_month != ay:
        profile.shield_month = ay
        profile.shield_count = cfg.SHIELD_PER_MONTH


def seri_guncelle(db: Session, profile: Profile, bugun: date) -> dict:
    """
    Gunluk gorev tamamlaninca seri guncellenir.

    Dun oynadiysa   -> +1
    2 gun once ise  -> kalkan varsa koru, yoksa sifirla
    Bugun zaten     -> degisiklik yok
    """
    kalkan_yenile(profile, bugun)

    onceki = profile.last_quest_date
    sonuc = {"streak": profile.streak_days, "shield_used": False, "broken": False}

    if onceki == bugun:
        return sonuc

    if onceki is None:
        profile.streak_days = 1
    elif onceki == bugun - timedelta(days=1):
        profile.streak_days += 1
    else:
        # Bir veya daha fazla gun atlandi
        atlanan = (bugun - onceki).days - 1
        if atlanan == 1 and (profile.shield_count or 0) > 0:
            profile.shield_count -= 1
            profile.streak_days += 1
            sonuc["shield_used"] = True
        else:
            profile.streak_days = 1
            sonuc["broken"] = True

    profile.last_quest_date = bugun
    sonuc["streak"] = profile.streak_days
    sonuc["shield_left"] = profile.shield_count
    return sonuc


def gorev_odulu(db: Session, profile: Profile, dogru: int, toplam: int,
                seri_bilgi: dict) -> dict:
    """Gunluk gorev tamamlama odulleri."""
    kazanilan = []

    yildiz_ver(db, profile, cfg.STAR_QUEST_COMPLETE, "quest_complete")
    kazanilan.append({"star": cfg.STAR_QUEST_COMPLETE, "reason": "Günlük görev tamamlandı"})

    oran = dogru / toplam if toplam else 0
    if oran >= 0.90:
        yildiz_ver(db, profile, cfg.STAR_HIGH_ACCURACY, "high_accuracy")
        kazanilan.append({"star": cfg.STAR_HIGH_ACCURACY, "reason": "%90+ doğruluk"})

    streak = seri_bilgi.get("streak", 0)
    if streak == 7:
        yildiz_ver(db, profile, cfg.STAR_STREAK_7, "streak_7")
        kazanilan.append({"star": cfg.STAR_STREAK_7, "reason": "7 gün seri"})
    elif streak == 30:
        yildiz_ver(db, profile, cfg.STAR_STREAK_30, "streak_30")
        kazanilan.append({"star": cfg.STAR_STREAK_30, "reason": "30 gün seri"})

    return {"rewards": kazanilan, "star_balance": profile.star_balance}


# ---------------------------------------------------------------- ROZET

def rozet_kontrol(db: Session, profile: Profile, ctx: dict) -> list[dict]:
    """
    ctx: {'quest_perfect': bool, 'streak': int, 'medal_up': bool}
    """
    yeni = []
    mevcut = {r[0] for r in db.query(ProfileBadge.badge_id)
              .filter(ProfileBadge.profile_id == profile.id).all()}

    def ver(bid: str):
        if bid in mevcut:
            return
        b = db.get(Badge, bid)
        if not b:
            return
        db.add(ProfileBadge(profile_id=profile.id, badge_id=bid))
        yildiz_ver(db, profile, 5, f"badge:{bid}")
        yeni.append({"id": b.id, "name": b.name, "icon": b.icon,
                     "description": b.description})

    # Ilk adim
    ver("ilk_adim")

    # Seri rozetleri
    s = ctx.get("streak", 0)
    if s >= 7:
        ver("haftalik_kahraman")
    if s >= 30:
        ver("aylik_efsane")

    # Mukemmel gun
    if ctx.get("quest_perfect"):
        ver("mukemmel_gun")

    # Merakli: 10 farkli kategoride oyna
    kat_sayisi = (db.query(AnswerLog.category_id)
                  .filter(AnswerLog.profile_id == profile.id)
                  .distinct().count())
    if kat_sayisi >= 10:
        ver("merakli")

    # Ders ustaligi: bir dersteki tum kategoriler Altin (medal>=3)
    from models import Category
    for ders, bid in [("matematik", "matematik_ustasi"),
                      ("turkce", "kelime_avcisi"),
                      ("hayat_bilgisi", "kasif")]:
        katlar = (db.query(Category.id)
                  .filter(Category.subject == ders,
                          Category.grade_min <= profile.grade,
                          Category.grade_max >= profile.grade).all())
        if not katlar:
            continue
        ids = [c[0] for c in katlar]
        altin = (db.query(ProfileSkill)
                 .filter(ProfileSkill.profile_id == profile.id,
                         ProfileSkill.category_id.in_(ids),
                         ProfileSkill.medal_level >= 3).count())
        if altin == len(ids):
            ver(bid)

    return yeni
