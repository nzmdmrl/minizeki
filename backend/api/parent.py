from datetime import date, datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import func
from sqlalchemy.orm import Session

import config as cfg
from models import (
    get_db, Account, Profile, Category, AnswerLog, ProfileSkill,
    DailyQuest, ProfileBadge, Badge,
)
from engine import kategoriler_for_grade, normalize, MEDAL_NAMES, MEDAL_ICONS
from .security import require_pin, get_profile_or_404

router = APIRouter(prefix="/api/parent", tags=["parent"])

SUBJECT_NAMES = {
    "matematik": "Matematik",
    "turkce": "Türkçe",
    "hayat_bilgisi": "Hayat Bilgisi",
    "fen": "Fen Bilimleri",
    "sosyal": "Sosyal Bilgiler",
    "ingilizce": "İngilizce",
}


@router.get("/dashboard")
def dashboard(profile_id: str, acc: Account = Depends(require_pin),
              db: Session = Depends(get_db)):
    p = get_profile_or_404(db, acc, profile_id)
    bugun = date.today()
    hafta_once = datetime.utcnow() - timedelta(days=7)
    sekiz_hafta = datetime.utcnow() - timedelta(days=56)

    # --- Ozet ---
    toplam_soru = db.query(AnswerLog).filter(
        AnswerLog.profile_id == p.id, AnswerLog.answered_at >= sekiz_hafta
    ).count()
    dogru_soru = db.query(AnswerLog).filter(
        AnswerLog.profile_id == p.id, AnswerLog.answered_at >= sekiz_hafta,
        AnswerLog.is_correct.is_(True),
    ).count()
    oynanan_gun = db.query(DailyQuest).filter(
        DailyQuest.profile_id == p.id,
        DailyQuest.completed_at.isnot(None),
        DailyQuest.quest_date >= bugun - timedelta(days=56),
    ).count()

    # Bugun
    bugun_bas = datetime.combine(bugun, datetime.min.time())
    bugun_sure = db.query(func.coalesce(func.sum(AnswerLog.duration_ms), 0)).filter(
        AnswerLog.profile_id == p.id, AnswerLog.answered_at >= bugun_bas
    ).scalar() or 0
    bugun_soru = db.query(AnswerLog).filter(
        AnswerLog.profile_id == p.id, AnswerLog.answered_at >= bugun_bas
    ).count()
    bugun_quest = db.query(DailyQuest).filter(
        DailyQuest.profile_id == p.id, DailyQuest.quest_date == bugun
    ).first()

    # --- Kategoriler ---
    kats = kategoriler_for_grade(db, p.grade, "family")
    kat_out, zayif = [], []
    for c in kats:
        s = db.get(ProfileSkill, (p.id, c.id))
        if not s:
            continue
        toplam = s.total_correct + s.total_wrong
        if toplam == 0:
            continue
        oran = round(100 * s.total_correct / toplam)
        item = {
            "id": c.id, "name": c.name, "subject": c.subject,
            "subject_name": SUBJECT_NAMES.get(c.subject, c.subject),
            "icon": c.icon, "accuracy": oran, "total": toplam,
            "medal_level": s.medal_level,
            "medal_icon": MEDAL_ICONS[s.medal_level],
            "medal_name": MEDAL_NAMES[s.medal_level],
            "advanced": bool(s.advanced_unlocked),
            "level": s.level,
        }
        kat_out.append(item)
        if oran < 65 and toplam >= 10:
            zayif.append(item)

    kat_out.sort(key=lambda x: -x["accuracy"])
    zayif.sort(key=lambda x: x["accuracy"])

    # --- Sinif dagilimi (bu hafta) ---
    dag_rows = db.query(AnswerLog.grade, func.count(AnswerLog.id)).filter(
        AnswerLog.profile_id == p.id, AnswerLog.answered_at >= hafta_once
    ).group_by(AnswerLog.grade).all()
    dag_toplam = sum(r[1] for r in dag_rows) or 1
    grade_dist = [{"grade": r[0], "count": r[1],
                   "percent": round(100 * r[1] / dag_toplam)} for r in dag_rows]
    grade_dist.sort(key=lambda x: x["grade"])

    # --- Ders dagilimi (bu hafta) ---
    ders_rows = (db.query(Category.subject, func.count(AnswerLog.id))
                 .join(Category, Category.id == AnswerLog.category_id)
                 .filter(AnswerLog.profile_id == p.id,
                         AnswerLog.answered_at >= hafta_once)
                 .group_by(Category.subject).all())
    ders_toplam = sum(r[1] for r in ders_rows) or 1
    subject_dist = [{"subject": r[0], "name": SUBJECT_NAMES.get(r[0], r[0]),
                     "count": r[1], "percent": round(100 * r[1] / ders_toplam)}
                    for r in ders_rows]
    subject_dist.sort(key=lambda x: -x["percent"])

    # --- 4 haftalik trend ---
    trend = []
    for i in range(3, -1, -1):
        bas = datetime.utcnow() - timedelta(days=(i + 1) * 7)
        son = datetime.utcnow() - timedelta(days=i * 7)
        t = db.query(AnswerLog).filter(
            AnswerLog.profile_id == p.id,
            AnswerLog.answered_at >= bas, AnswerLog.answered_at < son).count()
        d = db.query(AnswerLog).filter(
            AnswerLog.profile_id == p.id, AnswerLog.is_correct.is_(True),
            AnswerLog.answered_at >= bas, AnswerLog.answered_at < son).count()
        trend.append({"week": f"{4 - i}. hafta", "total": t,
                      "accuracy": round(100 * d / t) if t else 0})

    # --- Rozetler ---
    rozetler = (db.query(Badge).join(ProfileBadge, ProfileBadge.badge_id == Badge.id)
                .filter(ProfileBadge.profile_id == p.id).all())

    return {
        "profile": {
            "id": p.id, "name": p.name, "grade": p.grade,
            "avatar_id": p.avatar_id, "streak": p.streak_days,
            "stars": p.star_balance,
        },
        "summary": {
            "days_played": oynanan_gun,
            "total_questions": toplam_soru,
            "accuracy": round(100 * dogru_soru / toplam_soru) if toplam_soru else 0,
            "streak": p.streak_days,
        },
        "today": {
            "minutes": round(bugun_sure / 60000, 1),
            "questions": bugun_soru,
            "quest_done": bool(bugun_quest and bugun_quest.completed_at),
            "quest_correct": bugun_quest.correct_count if bugun_quest else 0,
            "limit_minutes": p.daily_limit_min,
        },
        "categories": kat_out,
        "weak": zayif[:3],
        "grade_distribution": grade_dist,
        "subject_distribution": subject_dist,
        "trend": trend,
        "badges": [{"id": b.id, "name": b.name, "icon": b.icon} for b in rozetler],
        "settings": {
            "repeat_ratio": p.repeat_ratio,
            "allow_advance": p.allow_advance,
            "subject_weights": p.subject_weights,
            "daily_limit_min": p.daily_limit_min,
            "focus_category_id": p.focus_category_id,
            "focus_until": str(p.focus_until) if p.focus_until else None,
        },
    }


class SettingsIn(BaseModel):
    grade: int | None = Field(default=None, ge=1, le=4)
    repeat_ratio: float | None = Field(default=None, ge=0.05, le=0.40)
    allow_advance: bool | None = None
    daily_limit_min: int | None = Field(default=None, ge=5, le=180)
    subject_weights: dict[str, float] | None = None


@router.put("/settings")
def update_settings(profile_id: str, body: SettingsIn,
                    acc: Account = Depends(require_pin),
                    db: Session = Depends(get_db)):
    p = get_profile_or_404(db, acc, profile_id)

    if body.grade is not None:
        p.grade = body.grade
    if body.repeat_ratio is not None:
        p.repeat_ratio = body.repeat_ratio
    if body.allow_advance is not None:
        p.allow_advance = body.allow_advance
    if body.daily_limit_min is not None:
        p.daily_limit_min = body.daily_limit_min
    if body.subject_weights is not None:
        temiz = {k: v for k, v in body.subject_weights.items()
                 if v in (0.5, 1.0, 1.5)}
        if temiz:
            p.subject_weights = temiz

    db.commit()

    kats = kategoriler_for_grade(db, p.grade, "family")
    dersler = sorted({c.subject for c in kats})
    oran = normalize(p.subject_weights or {}, dersler)
    return {
        "ok": True,
        "preview": [{"subject": d, "name": SUBJECT_NAMES.get(d, d),
                     "percent": round(100 * oran[d])} for d in oran],
    }


class FocusIn(BaseModel):
    category_id: str | None = None
    weeks: int = Field(default=1, ge=1, le=2)


@router.put("/focus")
def set_focus(profile_id: str, body: FocusIn,
              acc: Account = Depends(require_pin),
              db: Session = Depends(get_db)):
    """Odak modu: bir kategori gunluk gorevde 2 yerine 6 soru alir."""
    p = get_profile_or_404(db, acc, profile_id)

    if body.category_id is None:
        p.focus_category_id = None
        p.focus_until = None
        db.commit()
        return {"ok": True, "focus": None}

    cat = db.get(Category, body.category_id)
    if cat is None or not (cat.grade_min <= p.grade <= cat.grade_max):
        raise HTTPException(400, "Geçersiz kategori")

    p.focus_category_id = cat.id
    p.focus_until = date.today() + timedelta(weeks=body.weeks)
    db.commit()
    return {"ok": True, "focus": {"category_id": cat.id, "name": cat.name,
                                  "until": str(p.focus_until)}}


@router.get("/export")
def export_data(profile_id: str, acc: Account = Depends(require_pin),
                db: Session = Depends(get_db)):
    """KVKK: veri tasinabilirligi."""
    p = get_profile_or_404(db, acc, profile_id)
    logs = db.query(AnswerLog).filter(AnswerLog.profile_id == p.id).all()
    skills = db.query(ProfileSkill).filter(ProfileSkill.profile_id == p.id).all()
    return {
        "profile": {"name": p.name, "grade": p.grade,
                    "created_at": str(p.created_at)},
        "answers": [{"category": a.category_id, "correct": a.is_correct,
                     "band": a.band, "grade": a.grade,
                     "at": str(a.answered_at)} for a in logs],
        "skills": [{"category": s.category_id, "level": s.level,
                    "correct": s.total_correct, "wrong": s.total_wrong,
                    "medal": s.medal_level} for s in skills],
    }
