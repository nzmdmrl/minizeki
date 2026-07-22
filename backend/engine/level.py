"""
Gizli zorluk seviyesi + gorunur madalya + terfi/geri dusus.
"""
from datetime import datetime

from sqlalchemy import desc
from sqlalchemy.orm import Session

import config as cfg
from models import ProfileSkill, AnswerLog, Category

# Gorunur madalya esikleri (kumulatif dogru sayisi)
MEDAL_THRESHOLDS = [50, 150, 300, 500, 800]
MEDAL_NAMES = ["", "Bronz", "Gümüş", "Altın", "Elmas", "Usta"]
MEDAL_ICONS = ["", "🥉", "🥈", "🥇", "💎", "👑"]


def get_or_create_skill(db: Session, profile_id: str, category_id: str) -> ProfileSkill:
    skill = db.get(ProfileSkill, (profile_id, category_id))
    if skill is None:
        skill = ProfileSkill(profile_id=profile_id, category_id=category_id, level=2)
        db.add(skill)
        db.flush()
    return skill


def update_skill(db: Session, profile_id: str, category_id: str,
                 is_correct: bool) -> dict:
    """
    Cevap sonrasi seviye guncelleme.
    3 dogru ust uste -> level +1
    2 yanlis ust uste -> level -1
    """
    skill = get_or_create_skill(db, profile_id, category_id)
    onceki_madalya = skill.medal_level

    if is_correct:
        skill.total_correct += 1
        skill.correct_streak += 1
        skill.wrong_streak = 0
        if skill.correct_streak >= cfg.LEVEL_UP_STREAK and skill.level < 5:
            skill.level += 1
            skill.correct_streak = 0
    else:
        skill.total_wrong += 1
        skill.wrong_streak += 1
        skill.correct_streak = 0
        if skill.wrong_streak >= cfg.LEVEL_DOWN_STREAK and skill.level > 1:
            skill.level -= 1
            skill.wrong_streak = 0

    skill.last_seen_at = datetime.utcnow()

    # Gorunur madalya
    yeni_madalya = 0
    for i, esik in enumerate(MEDAL_THRESHOLDS):
        if skill.total_correct >= esik:
            yeni_madalya = i + 1
    skill.medal_level = yeni_madalya

    return {
        "medal_up": yeni_madalya > onceki_madalya,
        "medal_level": yeni_madalya,
        "medal_name": MEDAL_NAMES[yeni_madalya],
        "medal_icon": MEDAL_ICONS[yeni_madalya],
    }


def _son_n_dogruluk(db: Session, profile_id: str, category_id: str, n: int):
    rows = (db.query(AnswerLog.is_correct)
            .filter(AnswerLog.profile_id == profile_id,
                    AnswerLog.category_id == category_id)
            .order_by(desc(AnswerLog.answered_at))
            .limit(n).all())
    if len(rows) < n:
        return None
    return sum(1 for r in rows if r[0]) / n


def check_advance(db: Session, profile, category_id: str) -> bool:
    """
    Terfi kontrolu. Ucu birden saglanmali:
      1. Kategori seviyesi 5
      2. Son 30 soruda dogruluk >= %85
      3. Toplam >= 60 soru
    """
    if not profile.allow_advance or profile.grade >= 4:
        return False

    cat = db.get(Category, category_id)
    if cat is None or not cat.has_upper_grade:
        return False

    skill = get_or_create_skill(db, profile.id, category_id)
    if skill.advanced_unlocked or skill.level < 5:
        return False

    toplam = skill.total_correct + skill.total_wrong
    if toplam < cfg.ADVANCE_MIN_ANSWERS:
        return False

    dogruluk = _son_n_dogruluk(db, profile.id, category_id, cfg.ADVANCE_WINDOW)
    if dogruluk is None or dogruluk < cfg.ADVANCE_THRESHOLD:
        return False

    skill.advanced_unlocked = True
    skill.advance_ratio = cfg.ADVANCE_RATIO
    return True


def check_demote(db: Session, profile, category_id: str) -> bool:
    """
    Geri dusus. Kilit KALKMAZ, sadece oran iner.
    Cocuk 'actigim seyi kaybettim' hissetmemeli.
    Pencere 12 -> ayni gun icinde tepki verir.
    """
    skill = get_or_create_skill(db, profile.id, category_id)
    if not skill.advanced_unlocked:
        return False
    if skill.advance_ratio <= cfg.DEMOTE_RATIO:
        return False

    dogruluk = _son_n_dogruluk(db, profile.id, category_id, cfg.DEMOTE_WINDOW)
    if dogruluk is None or dogruluk >= cfg.DEMOTE_THRESHOLD:
        return False

    skill.advance_ratio = cfg.DEMOTE_RATIO
    return True
