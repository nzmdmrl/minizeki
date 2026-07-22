from datetime import date, datetime

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

import config as cfg
from models import (
    get_db, Account, Profile, Category, Question, DailyQuest,
    AnswerLog, SeenQuestion, ProfileSkill,
)
from engine import (
    gunluk_gorev_uret, soru_uret, update_skill, check_advance, check_demote,
    seri_guncelle, gorev_odulu, rozet_kontrol, kategoriler_for_grade,
    MEDAL_NAMES, MEDAL_ICONS, MEDAL_THRESHOLDS,
)
from .security import (
    get_current_account, get_profile_or_404, strip_answer, decode_question_token,
)

router = APIRouter(prefix="/api", tags=["play"])


# ---------------------------------------------------------------- GUNLUK GOREV

@router.get("/quest/today")
def quest_today(profile_id: str, acc: Account = Depends(get_current_account),
                db: Session = Depends(get_db)):
    """
    Gunun gorevi. Ayni gun icinde tekrar cagrilirsa AYNI sorular doner.
    Gece yarisi SUNUCU saatiyle yenilenir (cihaz saatiyle degil).
    """
    p = get_profile_or_404(db, acc, profile_id)
    bugun = date.today()

    dq = db.query(DailyQuest).filter(
        DailyQuest.profile_id == p.id, DailyQuest.quest_date == bugun
    ).first()

    if dq is None:
        sorular = gunluk_gorev_uret(db, p, acc.plan)
        if not sorular:
            raise HTTPException(500, "Soru üretilemedi")
        dq = DailyQuest(profile_id=p.id, quest_date=bugun, questions=sorular)
        db.add(dq)
        db.commit()
        db.refresh(dq)

    sorular = dq.questions
    return {
        "quest_id": dq.id,
        "date": str(bugun),
        "total": len(sorular),
        "progress": dq.progress or 0,
        "completed": dq.completed_at is not None,
        "questions": [strip_answer(q, p.id, "quest") for q in sorular],
    }


class QuestCompleteIn(BaseModel):
    quest_id: str
    correct: int = Field(ge=0)
    total: int = Field(ge=1)


@router.post("/quest/complete")
def quest_complete(body: QuestCompleteIn,
                   acc: Account = Depends(get_current_account),
                   db: Session = Depends(get_db)):
    dq = db.get(DailyQuest, body.quest_id)
    if dq is None:
        raise HTTPException(404, "Görev bulunamadı")
    p = get_profile_or_404(db, acc, dq.profile_id)

    if dq.completed_at is not None:
        return {"already_completed": True, "streak": p.streak_days,
                "star_balance": p.star_balance}

    dq.completed_at = datetime.utcnow()
    dq.correct_count = body.correct
    dq.progress = body.total

    seri = seri_guncelle(db, p, date.today())
    odul = gorev_odulu(db, p, body.correct, body.total, seri)
    rozetler = rozet_kontrol(db, p, {
        "quest_perfect": body.correct == body.total,
        "streak": seri["streak"],
    })

    # En zayif kategori -> Zeki'nin Onerisi
    oneri = None
    kats = kategoriler_for_grade(db, p.grade, acc.plan)
    if kats:
        skills = []
        for c in kats:
            s = db.get(ProfileSkill, (p.id, c.id))
            if s and (s.total_correct + s.total_wrong) >= 5:
                oran = s.total_correct / max(1, s.total_correct + s.total_wrong)
                skills.append((oran, c))
        if skills:
            skills.sort(key=lambda x: x[0])
            zayif = skills[0][1]
            oneri = {"category_id": zayif.id, "category_name": zayif.name,
                     "icon": zayif.icon,
                     "message": f"{zayif.name} konusunda biraz pratik yapalım mı?"}

    db.commit()
    return {
        "correct": body.correct, "total": body.total,
        "streak": seri["streak"],
        "shield_used": seri.get("shield_used", False),
        "streak_broken": seri.get("broken", False),
        "shield_left": p.shield_count,
        "rewards": odul["rewards"],
        "star_balance": odul["star_balance"],
        "new_badges": rozetler,
        "suggestion": oneri,
    }


# ---------------------------------------------------------------- SERBEST OYUN

@router.get("/play/{category_id}")
def free_play(category_id: str, profile_id: str, count: int = 10,
              acc: Account = Depends(get_current_account),
              db: Session = Depends(get_db)):
    p = get_profile_or_404(db, acc, profile_id)
    cat = db.get(Category, category_id)
    if cat is None:
        raise HTTPException(404, "Kategori bulunamadı")
    if not (cat.grade_min <= p.grade <= cat.grade_max):
        raise HTTPException(400, "Bu kategori bu sınıf için uygun değil")

    # Ucretsiz plan: gunde 1 serbest tur
    if acc.plan == "free":
        if not cat.is_free:
            raise HTTPException(status.HTTP_402_PAYMENT_REQUIRED,
                                "Bu kategori Aile planında açık")
        bugun_free = db.query(AnswerLog).filter(
            AnswerLog.profile_id == p.id,
            AnswerLog.mode == "free",
            AnswerLog.answered_at >= datetime.combine(date.today(), datetime.min.time()),
        ).count()
        if bugun_free >= cfg.FREE_FREEPLAY_PER_DAY * 10:
            raise HTTPException(status.HTTP_402_PAYMENT_REQUIRED,
                                "Bugünlük serbest oyun hakkın doldu. Yarın görüşürüz!")

    count = max(5, min(20, count))
    sorular = soru_uret(db, p, cat, count, mode="free")
    db.commit()
    if not sorular:
        raise HTTPException(500, "Bu kategoride soru bulunamadı")

    return {
        "category": {"id": cat.id, "name": cat.name, "icon": cat.icon},
        "total": len(sorular),
        "questions": [strip_answer(q, p.id, "free") for q in sorular],
    }


# ---------------------------------------------------------------- CEVAP

class AnswerIn(BaseModel):
    token: str
    selected: int = Field(ge=0, le=3)
    duration_ms: int = 0


@router.post("/answer")
def answer(body: AnswerIn, acc: Account = Depends(get_current_account),
           db: Session = Depends(get_db)):
    """
    Cevap dogrulama SUNUCU tarafinda. Dogru cevap istemcide yok.
    """
    payload = decode_question_token(body.token)
    p = get_profile_or_404(db, acc, payload["pid"])

    is_correct = body.selected == payload["ai"]
    cat_id = payload["cid"]
    qid = payload.get("qid")

    # Log
    db.add(AnswerLog(
        profile_id=p.id, category_id=cat_id, question_id=qid,
        band=payload["band"], grade=payload["grade"],
        is_correct=is_correct, duration_ms=max(0, body.duration_ms),
        mode=payload.get("mode", "quest"),
    ))

    # Yazili soru: gorulme kaydi + kalibrasyon
    if qid:
        seen = db.get(SeenQuestion, (p.id, qid))
        if seen:
            seen.last_seen_at = datetime.utcnow()
        else:
            db.add(SeenQuestion(profile_id=p.id, question_id=qid))

        q = db.get(Question, qid)
        if q:
            q.serve_count = (q.serve_count or 0) + 1
            if is_correct:
                q.correct_count = (q.correct_count or 0) + 1
            if q.serve_count >= 50:
                q.real_difficulty = 1 - (q.correct_count / q.serve_count)

    # Seviye guncelleme
    medal = update_skill(db, p.id, cat_id, is_correct)
    db.flush()

    # Terfi / geri dusus
    terfi = check_advance(db, p, cat_id)
    check_demote(db, p, cat_id)

    if medal["medal_up"]:
        from engine import yildiz_ver
        yildiz_ver(db, p, cfg.STAR_MEDAL_UP, f"medal:{cat_id}")

    db.commit()

    skill = db.get(ProfileSkill, (p.id, cat_id))
    return {
        "correct": is_correct,
        "answer_index": payload["ai"],
        "correct_option": payload["opts"][payload["ai"]],
        "medal_up": medal["medal_up"],
        "medal": {"level": medal["medal_level"], "name": medal["medal_name"],
                  "icon": medal["medal_icon"]} if medal["medal_up"] else None,
        # Cocuga 'ust sinif' denmez, sadece 'yeni sorular acildi'
        "advanced": terfi,
        "advance_message": "✨ Yeni sorular açıldı!" if terfi else None,
        "total_correct": skill.total_correct if skill else 0,
        "star_balance": p.star_balance,
    }


# ---------------------------------------------------------------- KATEGORILER

@router.get("/categories")
def categories(profile_id: str, acc: Account = Depends(get_current_account),
               db: Session = Depends(get_db)):
    p = get_profile_or_404(db, acc, profile_id)
    hepsi = db.query(Category).filter(
        Category.grade_min <= p.grade, Category.grade_max >= p.grade
    ).order_by(Category.sort_order).all()

    out = []
    for c in hepsi:
        s = db.get(ProfileSkill, (p.id, c.id))
        tc = s.total_correct if s else 0
        ml = s.medal_level if s else 0

        # Sonraki madalyaya ilerleme
        if ml >= 5:
            progress, next_at = 100, None
        else:
            onceki = MEDAL_THRESHOLDS[ml - 1] if ml > 0 else 0
            sonraki = MEDAL_THRESHOLDS[ml]
            progress = int(100 * (tc - onceki) / max(1, sonraki - onceki))
            next_at = sonraki

        locked = acc.plan == "free" and not c.is_free
        out.append({
            "id": c.id, "name": c.name, "subject": c.subject, "icon": c.icon,
            "medal_level": ml, "medal_name": MEDAL_NAMES[ml],
            "medal_icon": MEDAL_ICONS[ml],
            "total_correct": tc, "progress": max(0, min(100, progress)),
            "next_at": next_at, "locked": locked,
        })
    return {"categories": out}
