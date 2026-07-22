import random
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

import config as cfg
from models import get_db, Account, Profile, ProfileSkill
from engine import kategoriler_for_grade, get_or_create_skill, kalkan_yenile
from engine.selection import soru_uret
from .security import get_current_account, get_profile_or_404, strip_answer

router = APIRouter(prefix="/api/profiles", tags=["profile"])

AVATARS = ["fox", "bear", "panda", "owl", "frog", "cat"]


class ProfileIn(BaseModel):
    name: str = Field(min_length=1, max_length=30)
    avatar_id: str = "fox"
    grade: int = Field(ge=1, le=4)


class ProfileOut(BaseModel):
    id: str
    name: str
    avatar_id: str
    grade: int
    star_balance: int
    streak_days: int
    shield_count: int
    calibrated: bool
    quest_done_today: bool


def _to_out(p: Profile) -> ProfileOut:
    return ProfileOut(
        id=p.id, name=p.name, avatar_id=p.avatar_id, grade=p.grade,
        star_balance=p.star_balance or 0, streak_days=p.streak_days or 0,
        shield_count=p.shield_count or 0, calibrated=bool(p.calibrated),
        quest_done_today=(p.last_quest_date == date.today()),
    )


@router.get("", response_model=list[ProfileOut])
def list_profiles(acc: Account = Depends(get_current_account),
                  db: Session = Depends(get_db)):
    rows = db.query(Profile).filter(Profile.account_id == acc.id) \
        .order_by(Profile.created_at).all()
    for p in rows:
        kalkan_yenile(p, date.today())
    db.commit()
    return [_to_out(p) for p in rows]


@router.post("", response_model=ProfileOut)
def create_profile(body: ProfileIn, acc: Account = Depends(get_current_account),
                   db: Session = Depends(get_db)):
    limit = cfg.FAMILY_PROFILE_LIMIT if acc.plan == "family" else cfg.FREE_PROFILE_LIMIT
    mevcut = db.query(Profile).filter(Profile.account_id == acc.id).count()
    if mevcut >= limit:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            f"Ücretsiz planda {limit} profil açabilirsiniz. Aile planına geçin."
            if acc.plan == "free" else f"En fazla {limit} profil açabilirsiniz.",
        )
    if body.avatar_id not in AVATARS:
        body.avatar_id = "fox"

    p = Profile(
        account_id=acc.id, name=body.name.strip(),
        avatar_id=body.avatar_id, grade=body.grade,
        shield_month=f"{date.today().year}-{date.today().month:02d}",
        shield_count=cfg.SHIELD_PER_MONTH,
    )
    db.add(p)
    db.commit()
    db.refresh(p)
    return _to_out(p)


@router.get("/{profile_id}", response_model=ProfileOut)
def get_profile(profile_id: str, acc: Account = Depends(get_current_account),
                db: Session = Depends(get_db)):
    p = get_profile_or_404(db, acc, profile_id)
    kalkan_yenile(p, date.today())
    db.commit()
    return _to_out(p)


@router.delete("/{profile_id}")
def delete_profile(profile_id: str, acc: Account = Depends(get_current_account),
                   db: Session = Depends(get_db)):
    p = get_profile_or_404(db, acc, profile_id)
    db.delete(p)
    db.commit()
    return {"ok": True}


# ---------------------------------------------------------------- KALIBRASYON

@router.get("/{profile_id}/calibrate")
def calibration_questions(profile_id: str,
                          acc: Account = Depends(get_current_account),
                          db: Session = Depends(get_db)):
    """
    8 soruluk tanisma turu. 'Test' gibi gorunmez, ilk oyun gibi gorunur.
    Farkli kategorilerden, orta zorlukta.
    """
    p = get_profile_or_404(db, acc, profile_id)
    kats = kategoriler_for_grade(db, p.grade, acc.plan)
    if not kats:
        raise HTTPException(500, "Bu sınıf için kategori bulunamadı")

    secim = random.sample(kats, min(8, len(kats)))
    sorular = []
    for c in secim:
        qs = soru_uret(db, p, c, 1, mode="calib")
        sorular += qs
    while len(sorular) < 8 and kats:
        c = random.choice(kats)
        sorular += soru_uret(db, p, c, 1, mode="calib")
    sorular = sorular[:8]
    db.commit()

    return {"questions": [strip_answer(q, p.id, "calib") for q in sorular]}


class CalibrateIn(BaseModel):
    correct: int = Field(ge=0, le=8)
    total: int = Field(ge=1, le=8)


@router.post("/{profile_id}/calibrate")
def submit_calibration(profile_id: str, body: CalibrateIn,
                       acc: Account = Depends(get_current_account),
                       db: Session = Depends(get_db)):
    """
    Kalibrasyon sonucu -> baslangic seviyesi + tekrar orani.
    Cocuga puan gosterilmez, sadece 'Harika! Hazirsin'.
    """
    p = get_profile_or_404(db, acc, profile_id)
    oran = body.correct / body.total

    if oran >= 0.85:
        level, repeat = 3, 0.15
    elif oran >= 0.60:
        level, repeat = 2, 0.20
    elif oran >= 0.40:
        level, repeat = 2, 0.25
    else:
        level, repeat = 1, 0.35

    p.repeat_ratio = repeat
    p.calibrated = True

    for c in kategoriler_for_grade(db, p.grade, acc.plan):
        s = get_or_create_skill(db, p.id, c.id)
        s.level = level

    db.commit()
    return {"ok": True, "message": "Harika! Hazırsın 🎉"}
