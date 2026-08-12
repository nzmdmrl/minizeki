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


def aktif_mod(p) -> str:
    """
    Profilin gecerli mola modu.

    break_enabled ESKI alandir. Eski kayitlarda False ise mod "off"
    kabul edilir; boylece break_mode kolonu sonradan eklendiginde
    molayi kapatmis ebeveynlerde mola kendiliginden acilmaz.
    """
    if p.break_enabled is False:
        return "off"
    mod = (p.break_mode or "earned").lower()
    return mod if mod in ("off", "earned", "free") else "earned"


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


def _acik_molayi_duzelt(db: Session, p, mola_hakki: int):
    """
    Acik kalmis mola oturumlarini toparlar.

    Cocuk tablette ekran koruyucuya duserse veya sekme kapanirsa
    "mola bitti" bildirimi sunucuya ULASMAYABILIR. O zaman oturum
    acik kalir ve cocuk geri donunce yeni mola baslatamaz.

    Kural:
      - Suresi dolmus acik oturum -> kapatilir (sure hakla sinirli)
      - Suresi devam eden oturum  -> DOKUNULMAZ, cocuk devam eder
      - Onceki gunlerden kalan    -> kapatilir
    """
    simdi = datetime.utcnow()
    bugun_bas, _ = _gun_araligi()

    acik_liste = (db.query(BreakSession)
                  .filter(BreakSession.profile_id == p.id,
                          BreakSession.ended_at.is_(None))
                  .order_by(desc(BreakSession.started_at)).all())

    guncel = None
    degisti = False
    for o in acik_liste:
        gecen = int((simdi - o.started_at).total_seconds())
        eski_gun = o.started_at < bugun_bas
        if eski_gun or gecen >= mola_hakki or guncel is not None:
            # Kapat: sure hakla sinirlanir, boylece acik unutulan
            # oturum gunluk toplami sisirmez.
            o.ended_at = simdi
            o.duration_seconds = max(0, min(gecen, mola_hakki))
            degisti = True
        else:
            guncel = o

    if degisti:
        db.commit()
    return guncel


# ---------------------------------------------------------------- DURUM

@router.get("/status")
def status(profile_id: str, acc: Account = Depends(get_current_account),
           db: Session = Depends(get_db)):
    """Mola hakki var mi, ne kadar kaldi?"""
    p = get_profile_or_404(db, acc, profile_id)
    mod = aktif_mod(p)

    if mod == "off":
        return {"enabled": False, "mode": "off"}

    mola_hakki = (p.break_minutes or 15) * 60

    # ONCE acik molalari toparla, SONRA sureleri hesapla.
    # Ters sirada yapilirsa kapatilan oturumun suresi gunluk
    # toplama yansimaz ve cocuk hakkindan fazla mola yapabilir.
    acik = _acik_molayi_duzelt(db, p, mola_hakki)

    calisma = calisma_saniyesi(db, p.id)
    kullanilan = mola_saniyesi(db, p.id)

    ortak = {
        "enabled": True,
        "mode": mod,
        "study_seconds": calisma,
        "used_today": kullanilan,
        "break_minutes": p.break_minutes or 15,
        "active": ({"id": acik.id,
                    "started_at": acik.started_at.isoformat(),
                    "game_id": acik.game_id} if acik else None),
        "games": OYUNLAR,
    }

    if mod == "free":
        # Serbest mod: calisma sarti yok, sadece gunluk tavan.
        tavan = (p.break_daily_limit or 0) * 60      # 0 = sinirsiz
        kalan_gun = (max(0, tavan - kullanilan) if tavan else mola_hakki)
        kalan = min(kalan_gun, mola_hakki) if tavan else mola_hakki
        if acik:
            # Devam eden mola: kalan sure baslangictan hesaplanir
            gecen = int((datetime.utcnow() - acik.started_at).total_seconds())
            kalan = max(0, min(kalan, mola_hakki) - gecen)
        return {
            **ortak,
            "can_start": kalan > 0,
            "remaining_seconds": kalan,
            "daily_limit": p.break_daily_limit or 0,
            "daily_left": kalan_gun,
        }

    # Kazanilan mod: belli sure calisinca hak olusur
    gerekli = (p.study_minutes or 30) * 60
    dilim = calisma // gerekli if gerekli > 0 else 0
    kalan = max(0, dilim * mola_hakki - kullanilan)
    if acik:
        gecen = int((datetime.utcnow() - acik.started_at).total_seconds())
        kalan = max(0, min(kalan + gecen, mola_hakki) - gecen)
    return {
        **ortak,
        "can_start": kalan > 0,
        "remaining_seconds": kalan,
        "study_required": gerekli,
        "next_break_in": max(0, gerekli - (calisma % gerekli)) if gerekli else 0,
        "study_minutes": p.study_minutes or 30,
    }


# ---------------------------------------------------------------- BASLAT

class BaslatIn(BaseModel):
    profile_id: str
    game_id: str = "tek_cizgi"


@router.post("/start")
def start(body: BaslatIn, acc: Account = Depends(get_current_account),
          db: Session = Depends(get_db)):
    p = get_profile_or_404(db, acc, body.profile_id)
    mod = aktif_mod(p)

    if mod == "off":
        raise HTTPException(403, "Mola özelliği kapalı")

    mola_hakki = (p.break_minutes or 15) * 60
    acik = _acik_molayi_duzelt(db, p, mola_hakki)
    kullanilan = mola_saniyesi(db, p.id)

    if mod == "free":
        tavan = (p.break_daily_limit or 0) * 60
        if tavan:
            kalan = min(max(0, tavan - kullanilan), mola_hakki)
        else:
            kalan = mola_hakki
        hata_metni = "Bugünkü mola sürenin tamamını kullandın"
    else:
        calisma = calisma_saniyesi(db, p.id)
        gerekli = (p.study_minutes or 30) * 60
        dilim = calisma // gerekli if gerekli > 0 else 0
        kalan = max(0, dilim * mola_hakki - kullanilan)
        hata_metni = "Henüz mola hakkın yok"

    # ACIK MOLA VARSA ONA DEVAM ET
    # Cocuk sayfayi yenilerse veya sekmeye geri donerse molasi
    # sifirlanmamali. Yeni oturum acmak yerine mevcut olan dondurulur;
    # kalan sure basladigi andan itibaren hesaplanir.
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
        raise HTTPException(400, hata_metni)

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
