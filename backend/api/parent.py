from datetime import date, datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import func
from sqlalchemy.orm import Session

import config as cfg
from models import (
    get_db, Account, Profile, Category, AnswerLog, ProfileSkill,
    DailyQuest, ProfileBadge, Badge, ReadingSession, Story,
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

    # --- Okuma ve anlama ---
    okuma = _okuma_ozeti(db, p)

    return {
        "reading": okuma,
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


# Sinif bazli okuma hizi normlari (kelime/dakika) — yaklasik degerler.
# Ebeveyne ham sayi degil, "beklenen aralikta" seklinde sunulur.
WPM_NORM = {1: (40, 60), 2: (60, 90), 3: (90, 120), 4: (110, 140)}


def _okuma_ozeti(db: Session, p: Profile) -> dict:
    """
    Okuma gecmisi ozeti.

    NOT: Okuma hizi ses tanimayla degil, SURE OLCUMUYLE hesaplanir.
    Cocuk "Basla"ya basar, okur, "Okudum"a basar. Bu yontem izin
    gerektirmez, her cihazda calisir ve olcum kesindir.
    """
    oturumlar = (db.query(ReadingSession)
                 .filter(ReadingSession.profile_id == p.id)
                 .order_by(ReadingSession.created_at).all())
    if not oturumlar:
        return {"has_data": False, "total": 0}

    alt, ust = WPM_NORM.get(p.grade, (60, 90))

    # Hiz gecmisi (supheli ve sessiz okumalar haric)
    hiz_gecmis = [
        {"date": str(o.created_at)[:10], "wpm": o.wpm}
        for o in oturumlar
        if o.wpm and not o.suspicious and o.mode == "timed"
    ][-12:]

    # Anlama gecmisi
    anlama_gecmis = [
        {"date": str(o.created_at)[:10],
         "accuracy": round(100 * o.correct_count / max(1, o.total_questions))}
        for o in oturumlar
    ][-12:]

    son_hizlar = [x["wpm"] for x in hiz_gecmis[-3:]]
    ort_hiz = round(sum(son_hizlar) / len(son_hizlar)) if son_hizlar else None

    toplam_dogru = sum(o.correct_count for o in oturumlar)
    toplam_soru = sum(o.total_questions for o in oturumlar)
    ort_anlama = round(100 * toplam_dogru / max(1, toplam_soru))

    # Soru turune gore guclu/zayif alan
    tur_toplam = {"bilgi": [0, 0], "cikarim": [0, 0], "kelime": [0, 0]}
    for o in oturumlar:
        if not o.type_breakdown:
            continue
        for tur, v in o.type_breakdown.items():
            if tur in tur_toplam:
                tur_toplam[tur][0] += v.get("dogru", 0)
                tur_toplam[tur][1] += v.get("toplam", 0)

    TUR_AD = {"bilgi": "Metinde bulma", "cikarim": "Çıkarım yapma",
              "kelime": "Kelime bilgisi"}
    turler = [
        {"kod": k, "ad": TUR_AD[k],
         "accuracy": round(100 * v[0] / v[1]) if v[1] else None,
         "total": v[1]}
        for k, v in tur_toplam.items() if v[1] > 0
    ]

    # Hiz durumu
    if ort_hiz is None:
        durum = "veri_yok"
    elif ort_hiz < alt:
        durum = "gelisiyor"
    elif ort_hiz <= ust:
        durum = "beklenen"
    else:
        durum = "hizli"

    # Ebeveyne oneri
    oneri = None
    if ort_anlama < 60 and len(oturumlar) >= 3:
        oneri = ("Anlama oranı düşük seyrediyor. Bu hafta birlikte okumayı "
                 "deneyin: siz bir paragraf, çocuğunuz bir paragraf. "
                 "Sonra hikâyeyi birbirinize anlatın.")
    elif durum == "gelisiyor" and len(hiz_gecmis) >= 3:
        oneri = ("Okuma hızı yaşına göre gelişme aşamasında. Günlük kısa "
                 "okumalar en çok işe yarayan yöntemdir; hız zamanla artar. "
                 "Acele ettirmeyin.")
    elif any(t["kod"] == "cikarim" and (t["accuracy"] or 100) < 55
             for t in turler):
        oneri = ("Metinde açıkça yazan bilgileri buluyor ama çıkarım "
                 "sorularında zorlanıyor. Okuduktan sonra 'Sence neden "
                 "böyle yaptı?' gibi sorular sormayı deneyin.")

    son = oturumlar[-1]
    son_metin = db.get(Story, son.story_id)

    return {
        "has_data": True,
        "total": len(oturumlar),
        "stories_read": len({o.story_id for o in oturumlar}),
        "avg_wpm": ort_hiz,
        "wpm_status": durum,
        "wpm_norm": {"min": alt, "max": ust},
        "avg_accuracy": ort_anlama,
        "speed_history": hiz_gecmis,
        "accuracy_history": anlama_gecmis,
        "types": turler,
        "advice": oneri,
        "last": {
            "title": son_metin.title if son_metin else "—",
            "date": str(son.created_at)[:10],
            "wpm": son.wpm,
            "accuracy": round(100 * son.correct_count
                              / max(1, son.total_questions)),
            "mode": son.mode,
        },
        "peek_count": sum(1 for o in oturumlar if o.peeked),
        "suspicious_count": sum(1 for o in oturumlar if o.suspicious),
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
