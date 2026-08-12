"""
MOLA API'si

MANTIK:
  Cocuk belli sure calisinca mola hakki kazanir. Mola suresince oyun
  oynayabilir. Ebeveyn panelden hem sureleri ayarlar hem gunluk mola
  suresini gorur.

CALISMA SURESI NASIL OLCULUYOR:
  Ayri bir "sayac" istegi gondermiyoruz — bu hem fazladan trafik
  yaratir hem sekme arka plana alininca yanilir.

  Bunun yerine AnswerLog zaman damgalari kullanilir: ardisik iki cevap
  arasindaki sure MOLA_ESIGI'nden kisaysa o aralik "calisilmis" sayilir.
  Uzunsa cocuk ekrandan ayrilmis demektir, sayilmaz.

  Bu yontem gercek ekran suresine yakin bir tahmin verir ve hicbir
  ek istek gerektirmez.

TASARIM KURALI:
  Mola bir ODUL degil, dinlenme HAKKIDIR. Cocuk molayi kullanmazsa
  bir sey kaybetmez; yildiz verilmez, seri etkilenmez.
"""
from datetime import datetime, timedelta, date

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import func, desc
from sqlalchemy.orm import Session

from models import get_db, Account, AnswerLog, BreakSession, ReadingSession
from .security import get_current_account, get_profile_or_404

router = APIRouter(prefix="/api/break", tags=["break"])

# Iki cevap arasi bu sureden uzunsa cocuk ekrandan ayrilmis sayilir.
# 4 dakika: bir soruyu dusunmek icin bol, ama ara vermeyi de yakalar.
MOLA_ESIGI_SN = 240

# Tek bir cevabin katkisi en fazla bu kadar sayilir (ilk cevap icin)
ILK_CEVAP_SN = 30

OYUNLAR = [
    {
        "id": "tek_cizgi",
        "name": "Tek Çizgi",
        "description": "Sayıları sırayla birleştir, her kareden bir kez geç",
        "icon": "✏️",
    },
]


def _gun_araligi(gun: date | None = None) -> tuple[datetime, datetime]:
    g = gun or datetime.utcnow().date()
    bas = datetime.combine(g, datetime.min.time())
    return bas, bas + timedelta(days=1)


def calisma_saniyesi(db: Session, profile_id: str,
                     gun: date | None = None) -> int:
    """
    Bugun ekranda gecirilen tahmini calisma suresi (saniye).

    Ardisik cevaplar arasindaki kisa araliklar toplanir. Uzun araliklar
    (cocuk ekrandan ayrilmis) sayilmaz.
    """
    bas, son = _gun_araligi(gun)

    damgalar = [
        r[0] for r in db.query(AnswerLog.answered_at)
        .filter(AnswerLog.profile_id == profile_id,
                AnswerLog.answered_at >= bas,
                AnswerLog.answered_at < son)
        .order_by(AnswerLog.answered_at).all()
    ]

    # Okuma oturumlari da calisma sayilir; sureleri zaten kayitli
    okuma = db.query(func.coalesce(func.sum(ReadingSession.duration_ms), 0)) \
        .filter(ReadingSession.profile_id == profile_id,
                ReadingSession.created_at >= bas,
                ReadingSession.created_at < son).scalar() or 0

    toplam = int(okuma / 1000)
    if not damgalar:
        return toplam

    toplam += ILK_CEVAP_SN
    for onceki, simdiki in zip(damgalar, damgalar[1:]):
        fark = (simdiki - onceki).total_seconds()
        if 0 < fark <= MOLA_ESIGI_SN:
            toplam += int(fark)
        else:
            toplam += ILK_CEVAP_SN      # yeni oturum baslamis
    return toplam


def mola_saniyesi(db: Session, profile_id: str,
                  gun: date | None = None) -> int:
    """Bugun kullanilan toplam mola suresi (saniye)."""
    bas, son = _gun_araligi(gun)
    return int(db.query(
        func.coalesce(func.sum(BreakSession.duration_seconds), 0)
    ).filter(BreakSession.profile_id == profile_id,
             BreakSession.started_at >= bas,
             BreakSession.started_at < son).scalar() or 0)


# ---------------------------------------------------------------- DURUM

@router.get("/status")
def status(profile_id: str, acc: Account = Depends(get_current_account),
           db: Session = Depends(get_db)):
    """Mola hakki var mi, ne kadar kaldi?"""
    p = get_profile_or_404(db, acc, profile_id)

    if not p.break_enabled:
        return {"enabled": False}

    calisma = calisma_saniyesi(db, p.id)
    kullanilan = mola_saniyesi(db, p.id)

    gerekli = (p.study_minutes or 30) * 60
    mola_hakki = (p.break_minutes or 15) * 60

    # Kac tam "calisma dilimi" tamamlandi -> o kadar mola hakki
    dilim = calisma // gerekli if gerekli > 0 else 0
    toplam_hak = dilim * mola_hakki
    kalan = max(0, toplam_hak - kullanilan)

    # Devam eden mola var mi?
    acik = (db.query(BreakSession)
            .filter(BreakSession.profile_id == p.id,
                    BreakSession.ended_at.is_(None))
            .order_by(desc(BreakSession.started_at)).first())

    return {
        "enabled": True,
        "can_start": kalan > 0 and acik is None,
        "remaining_seconds": kalan,
        "study_seconds": calisma,
        "study_required": gerekli,
        # Bir sonraki mola icin daha ne kadar calismali
        "next_break_in": max(0, gerekli - (calisma % gerekli)) if gerekli else 0,
        "used_today": kullanilan,
        "break_minutes": p.break_minutes or 15,
        "study_minutes": p.study_minutes or 30,
        "active": ({"id": acik.id,
                    "started_at": acik.started_at.isoformat(),
                    "game_id": acik.game_id} if acik else None),
        "games": OYUNLAR,
    }


# ---------------------------------------------------------------- BASLAT

class BaslatIn(BaseModel):
    profile_id: str
    game_id: str = "tek_cizgi"


@router.post("/start")
def start(body: BaslatIn, acc: Account = Depends(get_current_account),
          db: Session = Depends(get_db)):
    p = get_profile_or_404(db, acc, body.profile_id)

    if not p.break_enabled:
        raise HTTPException(403, "Mola özelliği kapalı")

    calisma = calisma_saniyesi(db, p.id)
    kullanilan = mola_saniyesi(db, p.id)
    gerekli = (p.study_minutes or 30) * 60
    mola_hakki = (p.break_minutes or 15) * 60
    dilim = calisma // gerekli if gerekli > 0 else 0
    kalan = max(0, dilim * mola_hakki - kullanilan)

    # ACIK MOLA VARSA ONA DEVAM ET
    # Cocuk sayfayi yenilerse veya sekmeye geri donerse molasi
    # sifirlanmamali. Yeni oturum acmak yerine mevcut olan dondurulur;
    # kalan sure basladigi andan itibaren hesaplanir.
    acik = (db.query(BreakSession)
            .filter(BreakSession.profile_id == p.id,
                    BreakSession.ended_at.is_(None))
            .order_by(desc(BreakSession.started_at)).first())
    if acik:
        gecen = int((datetime.utcnow() - acik.started_at).total_seconds())
        kalan_sure = max(0, min(kalan, mola_hakki) - gecen)
        if kalan_sure <= 0:
            # Sure zaten dolmus: oturumu kapat ve mola hakki bitti de
            acik.ended_at = datetime.utcnow()
            acik.duration_seconds = min(mola_hakki, gecen)
            db.commit()
            raise HTTPException(400, "Mola süren doldu")
        return {"id": acik.id, "seconds": kalan_sure,
                "started_at": acik.started_at.isoformat(), "resumed": True}

    if kalan <= 0:
        raise HTTPException(400, "Henüz mola hakkın yok")

    oturum = BreakSession(profile_id=p.id, game_id=body.game_id)
    db.add(oturum)
    db.commit()

    return {"id": oturum.id, "seconds": min(kalan, mola_hakki),
            "started_at": oturum.started_at.isoformat(), "resumed": False}


# ---------------------------------------------------------------- BITIR

class BitirIn(BaseModel):
    profile_id: str
    session_id: str
    level_reached: int = 0


@router.post("/end")
def end(body: BitirIn, acc: Account = Depends(get_current_account),
        db: Session = Depends(get_db)):
    p = get_profile_or_404(db, acc, body.profile_id)
    oturum = db.get(BreakSession, body.session_id)
    if oturum is None or oturum.profile_id != p.id:
        raise HTTPException(404, "Mola oturumu bulunamadı")

    if oturum.ended_at is None:
        oturum.ended_at = datetime.utcnow()
        gecen = int((oturum.ended_at - oturum.started_at).total_seconds())
        # Sekme acik unutulursa sure sismesin: mola hakkiyla sinirla
        oturum.duration_seconds = max(0, min(gecen, (p.break_minutes or 15) * 60))
    oturum.level_reached = max(oturum.level_reached or 0, body.level_reached)
    db.commit()

    return {"duration_seconds": oturum.duration_seconds,
            "used_today": mola_saniyesi(db, p.id)}
