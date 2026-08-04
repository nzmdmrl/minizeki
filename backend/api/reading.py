"""
OKUMA VE ANLAMA API'si

AKIS:
  1. GET  /api/reading/story    -> seviyeye uygun metin
  2. Cocuk okur (sure frontend'de olculur)
  3. GET  /api/reading/questions -> 5 anlama sorusu (cevap sizmaz)
  4. POST /api/reading/complete  -> sure + cevaplar -> analiz

NEDEN SES TANIMA YOK:
  Okuma hizi = kelime / sure. Bunun icin mikrofona gerek yoktur.
  Ses tanima (a) cocuk sesinde guvenilmez, (b) sesi ucuncu tarafa gonderir,
  (c) iOS Safari'de calismaz, (d) maliyetlidir. Sure olcumu ise kesindir,
  izin gerektirmez ve her cihazda calisir.
"""
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import func, desc
from sqlalchemy.orm import Session

import config as cfg
from models import (
    get_db, Account, Story, StoryQuestion, ReadingSession, ProfileSkill,
)
from engine import get_or_create_skill, yildiz_ver, okuma_rozet_kontrol
from .security import get_current_account, get_profile_or_404

router = APIRouter(prefix="/api/reading", tags=["reading"])

# Sinif bazli okuma hizi normlari (kelime/dakika).
# Literaturde gecen yaklasik degerler; kesin resmi rakam degildir.
# Ebeveyne ham sayi yerine "beklenen aralikta" seklinde sunulur.
WPM_NORM = {
    1: (40, 60),
    2: (60, 90),
    3: (90, 120),
    4: (110, 140),
}

# Bu hizin ustu insan icin gercekci degil -> okumadan gecmis say
WPM_SUPHELI = 350

STAR_OKUMA = 5          # okuma turu tamamlama odulu
STAR_ANLAMA_IYI = 3     # %80+ anlama bonusu


# ---------------------------------------------------------------- METIN SEC

@router.get("/story")
def get_story(profile_id: str, story_id: str | None = None,
              acc: Account = Depends(get_current_account),
              db: Session = Depends(get_db)):
    """
    Cocuga uygun bir metin dondurur.

    Secim: sinifina uygun + son 30 gunde okumadigi metinler arasindan,
    okuma seviyesine en yakin olan. Hepsini okuduysa en eskiye doner.
    """
    p = get_profile_or_404(db, acc, profile_id)

    if story_id:
        s = db.get(Story, story_id)
        if s is None or s.status != "live":
            raise HTTPException(404, "Metin bulunamadı")
    else:
        # Okuma seviyesi: gecmis oturumlardan tahmin
        skill = get_or_create_skill(db, p.id, "okuma")
        hedef_seviye = skill.level

        cutoff = datetime.utcnow() - timedelta(days=30)
        okunan = (db.query(ReadingSession.story_id)
                  .filter(ReadingSession.profile_id == p.id,
                          ReadingSession.created_at > cutoff)
                  .distinct().scalar_subquery())

        temel = db.query(Story).filter(
            Story.status == "live",
            Story.grade_min <= p.grade,
            Story.grade_max >= p.grade,
        )

        # ONCELIK SIRASI:
        #   1. Kendi sinifi icin yazilmis, okunmamis metin
        #   2. Herhangi bir uygun okunmamis metin
        #   3. Hepsini okuduysa rastgele tekrar
        #
        # Kendi sinifina oncelik onemli: alt sinif metinleri cok kisadir
        # (orn. 1. sinif 22 kelime) ve okuma hizi olcumu guvenilmez olur.
        s = (temel.filter(Story.grade_min == p.grade)
             .filter(~Story.id.in_(okunan))
             .order_by(func.abs(Story.level - hedef_seviye), func.random())
             .first())
        if s is None:
            s = (temel.filter(~Story.id.in_(okunan))
                 .order_by(func.abs(Story.level - hedef_seviye), func.random())
                 .first())
        if s is None:
            s = (temel.filter(Story.grade_min == p.grade)
                 .order_by(func.random()).first())
        if s is None:
            s = temel.order_by(func.random()).first()
        if s is None:
            raise HTTPException(404, "Bu sınıf için metin bulunamadı")

    db.commit()
    return {
        "id": s.id,
        "title": s.title,
        "text": s.text,
        "word_count": s.word_count,
        "question_count": db.query(StoryQuestion).filter(
            StoryQuestion.story_id == s.id).count(),
    }


# ---------------------------------------------------------------- SORULAR

@router.get("/questions")
def get_questions(story_id: str, profile_id: str,
                  acc: Account = Depends(get_current_account),
                  db: Session = Depends(get_db)):
    """Anlama sorulari. Dogru cevap istemciye GONDERILMEZ."""
    from .security import create_question_token

    p = get_profile_or_404(db, acc, profile_id)
    s = db.get(Story, story_id)
    if s is None:
        raise HTTPException(404, "Metin bulunamadı")

    sorular = (db.query(StoryQuestion)
               .filter(StoryQuestion.story_id == story_id)
               .order_by(StoryQuestion.sort_order).all())
    if not sorular:
        raise HTTPException(404, "Bu metne ait soru yok")

    cikti = []
    for q in sorular:
        sahte = {
            "category_id": "okuma",
            "question_id": q.id,
            "answer_index": q.answer_index,
            "options": list(q.options),
            "band": 3,
            "grade": s.grade_min,
        }
        cikti.append({
            "token": create_question_token(sahte, p.id, "reading"),
            "text": q.text,
            "options": list(q.options),
            "type": q.type,
        })
    return {"story_id": story_id, "questions": cikti}


# ---------------------------------------------------------------- TAMAMLA

class ReadingIn(BaseModel):
    profile_id: str
    story_id: str
    mode: str = "timed"                 # timed | silent
    duration_ms: int = 0
    answers: list[int] = Field(default_factory=list)
    peeked: bool = False                # sorularda metne geri bakti mi
    reread: bool = False                # bu bir tekrar okuma mi


@router.post("/complete")
def complete(body: ReadingIn, acc: Account = Depends(get_current_account),
             db: Session = Depends(get_db)):
    """
    Okuma turunu bitirir ve analiz doner.

    mode="timed"  : hiz + anlama olculur
    mode="silent" : cocuk "sessiz okudum" dedi -> SADECE anlama olculur
    """
    p = get_profile_or_404(db, acc, body.profile_id)
    s = db.get(Story, body.story_id)
    if s is None:
        raise HTTPException(404, "Metin bulunamadı")

    sorular = (db.query(StoryQuestion)
               .filter(StoryQuestion.story_id == s.id)
               .order_by(StoryQuestion.sort_order).all())

    # --- Anlama ---
    dogru = 0
    kirilim = {"bilgi": [0, 0], "cikarim": [0, 0], "kelime": [0, 0]}
    for i, q in enumerate(sorular):
        secilen = body.answers[i] if i < len(body.answers) else -1
        ok = secilen == q.answer_index
        if ok:
            dogru += 1
        t = q.type if q.type in kirilim else "bilgi"
        kirilim[t][1] += 1
        if ok:
            kirilim[t][0] += 1

    # --- Hiz ---
    wpm = None
    supheli = False
    if body.mode == "timed" and body.duration_ms > 0:
        dakika = body.duration_ms / 60000
        wpm = int(round(s.word_count / dakika)) if dakika > 0 else 0
        supheli = wpm > WPM_SUPHELI

    # --- Kayit ---
    oturum = ReadingSession(
        profile_id=p.id, story_id=s.id, mode=body.mode,
        duration_ms=body.duration_ms or None, wpm=wpm,
        word_count=s.word_count,
        correct_count=dogru, total_questions=len(sorular),
        type_breakdown={k: {"dogru": v[0], "toplam": v[1]}
                        for k, v in kirilim.items()},
        peeked=body.peeked, reread=body.reread, suspicious=supheli,
    )
    db.add(oturum)

    # --- Okuma seviyesi (anlama oranina gore) ---
    skill = get_or_create_skill(db, p.id, "okuma")
    oran = dogru / len(sorular) if sorular else 0
    if oran >= 0.8 and skill.level < 5:
        skill.correct_streak += 1
        if skill.correct_streak >= 2:
            skill.level += 1
            skill.correct_streak = 0
    elif oran < 0.5 and skill.level > 1:
        skill.wrong_streak += 1
        if skill.wrong_streak >= 2:
            skill.level -= 1
            skill.wrong_streak = 0
    skill.total_correct += dogru
    skill.total_wrong += len(sorular) - dogru
    skill.last_seen_at = datetime.utcnow()

    # --- Odul (tekrar okumada yildiz verilmez) ---
    oduller = []
    if not body.reread:
        yildiz_ver(db, p, STAR_OKUMA, "reading_complete")
        oduller.append({"star": STAR_OKUMA, "reason": "Okuma tamamlandı"})
        if oran >= 0.8:
            yildiz_ver(db, p, STAR_ANLAMA_IYI, "reading_comprehension")
            oduller.append({"star": STAR_ANLAMA_IYI, "reason": "Çok iyi anladın"})

    db.flush()

    # --- Rozetler ---
    # Okuma kendi rozet setini kullanir; gunluk gorev rozetleri
    # (seri, mukemmel gun) okuma turlarinda tetiklenmez.
    rozetler = okuma_rozet_kontrol(db, p)

    db.commit()

    # --- Cocuga gosterilecek geri bildirim ---
    if oran >= 0.8:
        mesaj = "Hikâyeyi çok iyi anlamışsın!"
    elif oran >= 0.6:
        mesaj = "Güzel! Birkaç ayrıntı gözünden kaçmış."
    else:
        mesaj = "Bir daha okumak ister misin? İkinci okuyuşta daha çok şey fark edilir."

    # Cok kisa metinde sure olcumu hassas degildir: 5 saniyelik sapma
    # 25 kelimelik metinde %30 fark yaratir. Bu durumda hiz gosterilmez.
    MIN_KELIME_HIZ = 30

    hiz_bilgi = None
    if wpm is not None and not supheli and s.word_count >= MIN_KELIME_HIZ:
        alt, ust = WPM_NORM.get(p.grade, (60, 90))
        if wpm < alt:
            durum = "gelisiyor"
        elif wpm <= ust:
            durum = "beklenen"
        else:
            durum = "hizli"
        hiz_bilgi = {"wpm": wpm, "durum": durum, "alt": alt, "ust": ust}

    return {
        "correct": dogru,
        "total": len(sorular),
        "accuracy": round(100 * oran),
        "message": mesaj,
        "speed": hiz_bilgi,
        "suspicious": supheli,
        "rewards": oduller,
        "new_badges": rozetler,
        "star_balance": p.star_balance,
        "offer_reread": oran < 0.6 and not body.reread,
        "breakdown": {k: {"dogru": v[0], "toplam": v[1]}
                      for k, v in kirilim.items()},
    }


# ---------------------------------------------------------------- OZET

@router.get("/summary")
def summary(profile_id: str, acc: Account = Depends(get_current_account),
            db: Session = Depends(get_db)):
    """Cocugun kendi okuma gecmisi (kategoriler ekraninda gosterilir)."""
    p = get_profile_or_404(db, acc, profile_id)
    oturumlar = (db.query(ReadingSession)
                 .filter(ReadingSession.profile_id == p.id)
                 .order_by(desc(ReadingSession.created_at)).limit(20).all())
    if not oturumlar:
        return {"total": 0, "stories_read": 0}

    hizlar = [o.wpm for o in oturumlar if o.wpm and not o.suspicious]
    return {
        "total": len(oturumlar),
        "stories_read": len({o.story_id for o in oturumlar}),
        "last_wpm": hizlar[0] if hizlar else None,
        "avg_accuracy": round(
            100 * sum(o.correct_count for o in oturumlar)
            / max(1, sum(o.total_questions for o in oturumlar))),
    }
