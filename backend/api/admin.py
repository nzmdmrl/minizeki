"""
Admin paneli API'si.

GUVENLIK: Bu uclar TUM cocuklarin verisine erisir.
  - require_admin: hesap is_admin + ayri ADMIN_PASSWORD
  - Her degistiren islem audit_log'a yazilir
  - Cocuk profillerinin ADI gosterilmez (gizlilik) - sadece istatistik
"""
from datetime import datetime, date, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import func, desc, and_
from sqlalchemy.orm import Session

import config as cfg
from models import (
    get_db, Account, Profile, Category, Question, AnswerLog, ProfileSkill,
    DailyQuest, AuditLog, HouseItem, Badge, StarEvent,
)
from generators import REGISTRY
from .security import (
    get_current_account, create_admin_token, require_admin, audit,
    verify_password,
)

router = APIRouter(prefix="/api/admin", tags=["admin"])


# ================================================================ GIRIS

class AdminLoginIn(BaseModel):
    password: str


@router.post("/login")
def admin_login(body: AdminLoginIn,
                acc: Account = Depends(get_current_account),
                db: Session = Depends(get_db)):
    """
    Admin paneline giris. Once normal hesapla giris yapilmis olmali.
    ADMIN_PASSWORD ortam degiskeni bos ise panel TAMAMEN kapalidir.
    """
    if not cfg.ADMIN_PASSWORD:
        raise HTTPException(
            status.HTTP_503_SERVICE_UNAVAILABLE,
            "Admin paneli kapalı. ADMIN_PASSWORD ortam değişkenini ayarlayın.",
        )
    if not acc.is_admin:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Bu hesap admin değil")
    if body.password != cfg.ADMIN_PASSWORD:
        audit(db, acc, "admin.login_failed")
        db.commit()
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Şifre hatalı")

    audit(db, acc, "admin.login")
    db.commit()
    return {"admin_token": create_admin_token(acc.id), "email": acc.email}


@router.get("/me")
def admin_me(admin: Account = Depends(require_admin)):
    return {"id": admin.id, "email": admin.email, "is_admin": True}


# ================================================================ GENEL BAKIS

@router.get("/overview")
def overview(admin: Account = Depends(require_admin), db: Session = Depends(get_db)):
    bugun = date.today()
    bugun_bas = datetime.combine(bugun, datetime.min.time())
    hafta = datetime.utcnow() - timedelta(days=7)
    ay = datetime.utcnow() - timedelta(days=30)

    # --- Kullanicilar ---
    toplam_hesap = db.query(Account).count()
    toplam_profil = db.query(Profile).count()
    odeyen = db.query(Account).filter(Account.plan == "family").count()

    # Aktif profiller (soru cozmus)
    dau = (db.query(AnswerLog.profile_id)
           .filter(AnswerLog.answered_at >= bugun_bas)
           .distinct().count())
    wau = (db.query(AnswerLog.profile_id)
           .filter(AnswerLog.answered_at >= hafta)
           .distinct().count())
    mau = (db.query(AnswerLog.profile_id)
           .filter(AnswerLog.answered_at >= ay)
           .distinct().count())

    # --- Icerik ---
    kategori_sayisi = db.query(Category).count()
    prosedurel = db.query(Category).filter(Category.is_procedural.is_(True)).count()
    canli_soru = db.query(Question).filter(Question.status == "live").count()
    taslak_soru = db.query(Question).filter(Question.status == "draft").count()
    emekli_soru = db.query(Question).filter(Question.status == "retired").count()

    # --- Aktivite ---
    bugun_cevap = db.query(AnswerLog).filter(
        AnswerLog.answered_at >= bugun_bas).count()
    hafta_cevap = db.query(AnswerLog).filter(
        AnswerLog.answered_at >= hafta).count()
    bugun_gorev = db.query(DailyQuest).filter(
        DailyQuest.quest_date == bugun,
        DailyQuest.completed_at.isnot(None)).count()

    # --- Sistem sagligi: dogruluk hedef bantta mi? ---
    hafta_toplam = hafta_cevap
    hafta_dogru = db.query(AnswerLog).filter(
        AnswerLog.answered_at >= hafta,
        AnswerLog.is_correct.is_(True)).count()
    dogruluk = round(100 * hafta_dogru / hafta_toplam) if hafta_toplam else 0

    if hafta_toplam < 50:
        saglik, mesaj = "unknown", "Yeterli veri yok"
    elif 75 <= dogruluk <= 85:
        saglik, mesaj = "good", "Doğruluk hedef bantta (%75–85)"
    elif dogruluk > 90:
        saglik, mesaj = "warn", "Çocuklar sıkılıyor olabilir — sorular çok kolay"
    elif dogruluk < 60:
        saglik, mesaj = "bad", "Çocuklar zorlanıyor — sorular çok zor"
    else:
        saglik, mesaj = "ok", "Kabul edilebilir aralıkta"

    # --- Gunluk gorev tamamlama orani ---
    hafta_basladi = db.query(DailyQuest).filter(
        DailyQuest.quest_date >= bugun - timedelta(days=7)).count()
    hafta_bitti = db.query(DailyQuest).filter(
        DailyQuest.quest_date >= bugun - timedelta(days=7),
        DailyQuest.completed_at.isnot(None)).count()
    tamamlama = round(100 * hafta_bitti / hafta_basladi) if hafta_basladi else 0

    # --- Kalibrasyon bekleyen ---
    hatali_band = _kalibrasyon_sapma_sayisi(db)

    return {
        "users": {
            "accounts": toplam_hesap, "profiles": toplam_profil,
            "paying": odeyen,
            "conversion": round(100 * odeyen / toplam_hesap, 1) if toplam_hesap else 0,
            "dau": dau, "wau": wau, "mau": mau,
        },
        "content": {
            "categories": kategori_sayisi,
            "procedural": prosedurel,
            "written": kategori_sayisi - prosedurel,
            "questions_live": canli_soru,
            "questions_draft": taslak_soru,
            "questions_retired": emekli_soru,
            "generators": len(REGISTRY),
        },
        "activity": {
            "answers_today": bugun_cevap,
            "answers_week": hafta_cevap,
            "quests_today": bugun_gorev,
            "completion_rate": tamamlama,
        },
        "health": {
            "status": saglik, "message": mesaj,
            "accuracy_week": dogruluk,
            "miscalibrated_questions": hatali_band,
        },
    }


def _kalibrasyon_sapma_sayisi(db: Session) -> int:
    """Bandi gercek zorlugundan sapan soru sayisi."""
    qs = db.query(Question).filter(
        Question.serve_count >= cfg.CALIBRATION_MIN_SERVES,
        Question.status == "live").all()
    n = 0
    for q in qs:
        gercek = q.correct_count / q.serve_count
        hedef = cfg.BAND_TARGET_ACCURACY.get(q.band, 0.6)
        if abs(gercek - hedef) > cfg.CALIBRATION_TOLERANCE:
            n += 1
    return n


@router.get("/activity-chart")
def activity_chart(days: int = 14, admin: Account = Depends(require_admin),
                   db: Session = Depends(get_db)):
    """Gunluk cevap ve dogruluk grafigi."""
    days = max(7, min(60, days))
    out = []
    for i in range(days - 1, -1, -1):
        g = date.today() - timedelta(days=i)
        bas = datetime.combine(g, datetime.min.time())
        son = bas + timedelta(days=1)
        t = db.query(AnswerLog).filter(
            AnswerLog.answered_at >= bas, AnswerLog.answered_at < son).count()
        d = db.query(AnswerLog).filter(
            AnswerLog.answered_at >= bas, AnswerLog.answered_at < son,
            AnswerLog.is_correct.is_(True)).count()
        aktif = (db.query(AnswerLog.profile_id).filter(
            AnswerLog.answered_at >= bas, AnswerLog.answered_at < son)
            .distinct().count())
        out.append({
            "date": str(g), "answers": t, "active": aktif,
            "accuracy": round(100 * d / t) if t else 0,
        })
    return {"data": out}


# ================================================================ KALIBRASYON

@router.get("/calibration")
def calibration(only_bad: bool = True, limit: int = 100,
                admin: Account = Depends(require_admin),
                db: Session = Depends(get_db)):
    """
    GERCEK ZORLUK KALIBRASYONU

    Sistem her sorunun gercek zorlugunu olcer:
        gercek_dogruluk = correct_count / serve_count

    Bunu bandin hedefiyle karsilastirir. Sapma buyukse soru yanlis banttadir
    ve zorluk motoru bozulur. Bu ekran onlari bulur ve dogru bandi onerir.
    """
    qs = (db.query(Question)
          .filter(Question.serve_count >= cfg.CALIBRATION_MIN_SERVES,
                  Question.status == "live")
          .order_by(desc(Question.serve_count)).limit(500).all())

    out = []
    for q in qs:
        gercek = q.correct_count / q.serve_count
        hedef = cfg.BAND_TARGET_ACCURACY.get(q.band, 0.6)
        sapma = gercek - hedef

        # Gercek dogruluga en yakin band
        onerilen = min(cfg.BAND_TARGET_ACCURACY,
                       key=lambda b: abs(cfg.BAND_TARGET_ACCURACY[b] - gercek))
        hatali = abs(sapma) > cfg.CALIBRATION_TOLERANCE

        if only_bad and not hatali:
            continue

        cat = db.get(Category, q.category_id)
        out.append({
            "id": q.id,
            "text": q.text[:90],
            "category_id": q.category_id,
            "category_name": cat.name if cat else q.category_id,
            "band": q.band,
            "suggested_band": onerilen,
            "serve_count": q.serve_count,
            "correct_count": q.correct_count,
            "real_accuracy": round(100 * gercek),
            "target_accuracy": round(100 * hedef),
            "deviation": round(100 * sapma),
            "miscalibrated": hatali,
            "verdict": ("Çok kolay" if sapma > cfg.CALIBRATION_TOLERANCE
                        else "Çok zor" if sapma < -cfg.CALIBRATION_TOLERANCE
                        else "Doğru bantta"),
        })

    out.sort(key=lambda x: -abs(x["deviation"]))
    return {
        "min_serves": cfg.CALIBRATION_MIN_SERVES,
        "tolerance": round(100 * cfg.CALIBRATION_TOLERANCE),
        "total": len(out),
        "questions": out[:limit],
    }


@router.post("/calibration/apply")
def apply_calibration(admin: Account = Depends(require_admin),
                      db: Session = Depends(get_db)):
    """
    Sapan tum sorulari onerilen banda TASI.
    Toplu islem — audit'e yazilir.
    """
    qs = db.query(Question).filter(
        Question.serve_count >= cfg.CALIBRATION_MIN_SERVES,
        Question.status == "live").all()

    degisen = []
    for q in qs:
        gercek = q.correct_count / q.serve_count
        hedef = cfg.BAND_TARGET_ACCURACY.get(q.band, 0.6)
        if abs(gercek - hedef) <= cfg.CALIBRATION_TOLERANCE:
            continue
        yeni = min(cfg.BAND_TARGET_ACCURACY,
                   key=lambda b: abs(cfg.BAND_TARGET_ACCURACY[b] - gercek))
        if yeni == q.band:
            continue
        degisen.append({"id": q.id, "from": q.band, "to": yeni})
        q.band = yeni
        q.real_difficulty = 1 - gercek

    audit(db, admin, "calibration.apply", detail={"count": len(degisen)})
    db.commit()
    return {"updated": len(degisen), "changes": degisen[:50]}


# ================================================================ SORULAR

@router.get("/questions")
def list_questions(category_id: str | None = None, status_f: str | None = None,
                   band: int | None = None, grade: int | None = None,
                   q: str | None = None, page: int = 1, size: int = 50,
                   admin: Account = Depends(require_admin),
                   db: Session = Depends(get_db)):
    query = db.query(Question)

    if category_id:
        query = query.filter(Question.category_id == category_id)
    if status_f:
        query = query.filter(Question.status == status_f)
    if band:
        query = query.filter(Question.band == band)
    if grade:
        query = query.filter(Question.grade_min <= grade,
                             Question.grade_max >= grade)
    if q:
        query = query.filter(Question.text.ilike(f"%{q}%"))

    total = query.count()
    size = max(10, min(200, size))
    rows = (query.order_by(Question.category_id, Question.band)
            .offset((max(1, page) - 1) * size).limit(size).all())

    cats = {c.id: c.name for c in db.query(Category).all()}
    return {
        "total": total, "page": page, "size": size,
        "pages": (total + size - 1) // size,
        "questions": [{
            "id": r.id, "category_id": r.category_id,
            "category_name": cats.get(r.category_id, r.category_id),
            "grade_min": r.grade_min, "grade_max": r.grade_max,
            "band": r.band, "text": r.text, "options": r.options,
            "answer_index": r.answer_index, "explanation": r.explanation,
            "status": r.status, "source": r.source,
            "serve_count": r.serve_count, "correct_count": r.correct_count,
            "real_accuracy": (round(100 * r.correct_count / r.serve_count)
                              if r.serve_count else None),
        } for r in rows],
    }


class QuestionIn(BaseModel):
    category_id: str
    grade_min: int = Field(ge=1, le=4)
    grade_max: int = Field(ge=1, le=4)
    band: int = Field(ge=1, le=5)
    text: str = Field(min_length=3)
    options: list[str] = Field(min_length=4, max_length=4)
    answer_index: int = Field(ge=0, le=3)
    explanation: str = ""
    status: str = "draft"
    image_url: str | None = None


def _validate_question(db: Session, b: QuestionIn) -> None:
    cat = db.get(Category, b.category_id)
    if cat is None:
        raise HTTPException(400, "Kategori bulunamadı")
    if cat.is_procedural:
        raise HTTPException(
            400, f"'{cat.name}' prosedürel bir kategori — soruları algoritma "
                 f"üretir, elle soru eklenemez.")
    if len(set(b.options)) != 4:
        raise HTTPException(400, "Şıklar birbirinden farklı olmalı")
    if any(not o.strip() for o in b.options):
        raise HTTPException(400, "Boş şık olamaz")
    if b.grade_min > b.grade_max:
        raise HTTPException(400, "Sınıf aralığı hatalı")
    if not (cat.grade_min <= b.grade_min and b.grade_max <= cat.grade_max):
        raise HTTPException(
            400, f"'{cat.name}' kategorisi {cat.grade_min}–{cat.grade_max}. "
                 f"sınıflar için. Bu aralığın dışına çıkamazsınız.")
    if b.status not in ("draft", "review", "live", "retired"):
        raise HTTPException(400, "Geçersiz durum")


@router.post("/questions")
def create_question(body: QuestionIn, admin: Account = Depends(require_admin),
                    db: Session = Depends(get_db)):
    _validate_question(db, body)

    varmi = db.query(Question).filter(
        Question.category_id == body.category_id,
        Question.text == body.text).first()
    if varmi:
        raise HTTPException(409, "Bu soru zaten var")

    q = Question(
        category_id=body.category_id, grade_min=body.grade_min,
        grade_max=body.grade_max, band=body.band, text=body.text,
        options=body.options, answer_index=body.answer_index,
        explanation=body.explanation, status=body.status,
        image_url=body.image_url, source="human",
    )
    db.add(q)
    db.flush()
    audit(db, admin, "question.create", q.id, {"category": body.category_id})
    db.commit()
    return {"id": q.id, "ok": True}


@router.put("/questions/{qid}")
def update_question(qid: str, body: QuestionIn,
                    admin: Account = Depends(require_admin),
                    db: Session = Depends(get_db)):
    q = db.get(Question, qid)
    if q is None:
        raise HTTPException(404, "Soru bulunamadı")
    _validate_question(db, body)

    onceki = {"band": q.band, "text": q.text, "status": q.status}

    # Soru metni veya siklar degistiyse istatistik gecersizdir
    icerik_degisti = (q.text != body.text or list(q.options) != body.options
                      or q.answer_index != body.answer_index)

    q.category_id = body.category_id
    q.grade_min = body.grade_min
    q.grade_max = body.grade_max
    q.band = body.band
    q.text = body.text
    q.options = body.options
    q.answer_index = body.answer_index
    q.explanation = body.explanation
    q.status = body.status
    q.image_url = body.image_url

    if icerik_degisti:
        q.serve_count = 0
        q.correct_count = 0
        q.real_difficulty = None

    audit(db, admin, "question.update", qid,
          {"before": onceki, "stats_reset": icerik_degisti})
    db.commit()
    return {"ok": True, "stats_reset": icerik_degisti}


class StatusIn(BaseModel):
    status: str


@router.put("/questions/{qid}/status")
def set_status(qid: str, body: StatusIn, admin: Account = Depends(require_admin),
               db: Session = Depends(get_db)):
    q = db.get(Question, qid)
    if q is None:
        raise HTTPException(404, "Soru bulunamadı")
    if body.status not in ("draft", "review", "live", "retired"):
        raise HTTPException(400, "Geçersiz durum")

    onceki = q.status
    q.status = body.status
    if body.status == "live" and onceki != "live":
        q.approved_by = admin.email

    audit(db, admin, "question.status", qid,
          {"from": onceki, "to": body.status})
    db.commit()
    return {"ok": True}


@router.delete("/questions/{qid}")
def delete_question(qid: str, admin: Account = Depends(require_admin),
                    db: Session = Depends(get_db)):
    """
    Soru silmek yerine EMEKLIYE AYIRMAK tercih edilmeli:
    silinen sorunun answer_log kayitlari sahipsiz kalir.
    """
    q = db.get(Question, qid)
    if q is None:
        raise HTTPException(404, "Soru bulunamadı")

    if q.serve_count > 0:
        raise HTTPException(
            400, "Bu soru çocuklara gösterilmiş. Silmek yerine 'Emekli' "
                 "durumuna alın — istatistikler korunur.")

    audit(db, admin, "question.delete", qid, {"text": q.text[:60]})
    db.delete(q)
    db.commit()
    return {"ok": True}


class BulkStatusIn(BaseModel):
    ids: list[str]
    status: str


@router.post("/questions/bulk-status")
def bulk_status(body: BulkStatusIn, admin: Account = Depends(require_admin),
                db: Session = Depends(get_db)):
    if body.status not in ("draft", "review", "live", "retired"):
        raise HTTPException(400, "Geçersiz durum")
    n = (db.query(Question).filter(Question.id.in_(body.ids))
         .update({Question.status: body.status}, synchronize_session=False))
    audit(db, admin, "question.bulk_status",
          detail={"count": n, "status": body.status})
    db.commit()
    return {"updated": n}


# ================================================================ ICE AKTARMA

class ImportIn(BaseModel):
    category_id: str
    # [band, grade_min, grade_max, text, [4 sik], answer_index, explanation]
    rows: list[list]
    status: str = "draft"


@router.post("/questions/import")
def import_questions(body: ImportIn, admin: Account = Depends(require_admin),
                     db: Session = Depends(get_db)):
    """
    Toplu soru ice aktarma.

    Beklenen satir formati (content/sorular_*.py ile ayni):
      [band, sinif_min, sinif_max, "soru", ["a","b","c","d"], dogru_index, "aciklama"]
    """
    cat = db.get(Category, body.category_id)
    if cat is None:
        raise HTTPException(400, "Kategori bulunamadı")
    if cat.is_procedural:
        raise HTTPException(400, f"'{cat.name}' prosedürel — soru eklenemez")

    eklenen, hatalar = 0, []
    for i, r in enumerate(body.rows):
        try:
            band, gmin, gmax, text, opts, ai, expl = (list(r) + [""])[:7]
            if len(opts) != 4 or len(set(opts)) != 4:
                raise ValueError("4 farklı şık gerekli")
            if not (0 <= ai < 4):
                raise ValueError("answer_index 0-3 arası olmalı")
            if not (1 <= band <= 5):
                raise ValueError("band 1-5 arası olmalı")
            if db.query(Question).filter(Question.category_id == body.category_id,
                                         Question.text == text).first():
                raise ValueError("zaten var")

            db.add(Question(
                category_id=body.category_id, grade_min=gmin, grade_max=gmax,
                band=band, text=text, options=list(opts), answer_index=ai,
                explanation=expl, status=body.status, source="import",
            ))
            eklenen += 1
        except Exception as e:
            hatalar.append({"row": i + 1, "error": str(e)})

    audit(db, admin, "question.import", body.category_id,
          {"added": eklenen, "errors": len(hatalar)})
    db.commit()
    return {"added": eklenen, "errors": hatalar[:20],
            "error_count": len(hatalar)}


@router.get("/questions/export")
def export_questions(category_id: str | None = None,
                     admin: Account = Depends(require_admin),
                     db: Session = Depends(get_db)):
    """content/sorular_*.py formatinda disari aktarir."""
    query = db.query(Question)
    if category_id:
        query = query.filter(Question.category_id == category_id)
    rows = query.order_by(Question.category_id, Question.band).all()

    audit(db, admin, "question.export", category_id, {"count": len(rows)})
    db.commit()
    return {
        "count": len(rows),
        "rows": [[r.band, r.grade_min, r.grade_max, r.text,
                  list(r.options), r.answer_index, r.explanation or ""]
                 for r in rows],
    }


# ================================================================ KATEGORILER

@router.get("/categories")
def admin_categories(admin: Account = Depends(require_admin),
                     db: Session = Depends(get_db)):
    cats = db.query(Category).order_by(Category.sort_order).all()
    out = []
    for c in cats:
        canli = db.query(Question).filter(
            Question.category_id == c.id, Question.status == "live").count()
        taslak = db.query(Question).filter(
            Question.category_id == c.id, Question.status == "draft").count()

        # Bu kategoride cocuklarin gercek performansi
        toplam = db.query(AnswerLog).filter(
            AnswerLog.category_id == c.id).count()
        dogru = db.query(AnswerLog).filter(
            AnswerLog.category_id == c.id,
            AnswerLog.is_correct.is_(True)).count()

        uyari = None
        if not c.is_procedural and canli < 20:
            uyari = f"Sadece {canli} canlı soru — en az 20 olmalı"
        elif toplam >= 50:
            oran = 100 * dogru / toplam
            if oran > 92:
                uyari = f"%{oran:.0f} doğruluk — sorular çok kolay"
            elif oran < 55:
                uyari = f"%{oran:.0f} doğruluk — sorular çok zor"

        out.append({
            "id": c.id, "name": c.name, "subject": c.subject, "icon": c.icon,
            "grade_min": c.grade_min, "grade_max": c.grade_max,
            "is_procedural": c.is_procedural, "generator_key": c.generator_key,
            "has_upper_grade": c.has_upper_grade, "is_free": c.is_free,
            "sort_order": c.sort_order,
            "questions_live": canli, "questions_draft": taslak,
            "answers": toplam,
            "accuracy": round(100 * dogru / toplam) if toplam else None,
            "warning": uyari,
        })
    return {"categories": out}


class CategoryIn(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    subject: str
    icon: str = "📘"
    grade_min: int = Field(ge=1, le=4)
    grade_max: int = Field(ge=1, le=4)
    has_upper_grade: bool = True
    is_free: bool = False
    sort_order: int = 100


@router.put("/categories/{cid}")
def update_category(cid: str, body: CategoryIn,
                    admin: Account = Depends(require_admin),
                    db: Session = Depends(get_db)):
    c = db.get(Category, cid)
    if c is None:
        raise HTTPException(404, "Kategori bulunamadı")
    if body.grade_min > body.grade_max:
        raise HTTPException(400, "Sınıf aralığı hatalı")

    onceki = {"name": c.name, "grade_min": c.grade_min,
              "grade_max": c.grade_max, "is_free": c.is_free}
    c.name = body.name
    c.subject = body.subject
    c.icon = body.icon
    c.grade_min = body.grade_min
    c.grade_max = body.grade_max
    c.has_upper_grade = body.has_upper_grade
    c.is_free = body.is_free
    c.sort_order = body.sort_order

    audit(db, admin, "category.update", cid, {"before": onceki})
    db.commit()
    return {"ok": True}


# ================================================================ PROSEDUREL TEST

@router.get("/generators")
def list_generators(admin: Account = Depends(require_admin),
                    db: Session = Depends(get_db)):
    kullanim = {}
    for c in db.query(Category).filter(Category.is_procedural.is_(True)).all():
        kullanim.setdefault(c.generator_key, []).append(c.name)
    return {
        "generators": [{"key": k, "used_by": kullanim.get(k, [])}
                       for k in sorted(REGISTRY.keys())],
    }


@router.get("/generators/{key}/preview")
def preview_generator(key: str, grade: int = 2, band: int = 3, count: int = 5,
                      admin: Account = Depends(require_admin)):
    """
    Prosedurel uretecin ornek ciktisi.
    Celdiricilerin gercekten 'tipik hata' olup olmadigini gozle kontrol icin.
    """
    if key not in REGISTRY:
        raise HTTPException(404, "Üreteç bulunamadı")
    from generators import generate
    count = max(1, min(20, count))
    out = []
    for _ in range(count):
        try:
            q = generate(key, grade, band)
            out.append({
                "text": q["text"], "options": q["options"],
                "correct": q["options"][q["answer_index"]],
                "explanation": q.get("explanation", ""),
                "svg": q.get("svg"),
            })
        except Exception as e:
            raise HTTPException(500, f"Üreteç hatası: {e}")
    return {"key": key, "grade": grade, "band": band, "samples": out}


# ================================================================ HESAPLAR

@router.get("/accounts")
def list_accounts(q: str | None = None, plan: str | None = None,
                  page: int = 1, size: int = 50,
                  admin: Account = Depends(require_admin),
                  db: Session = Depends(get_db)):
    query = db.query(Account)
    if q:
        query = query.filter(Account.email.ilike(f"%{q}%"))
    if plan:
        query = query.filter(Account.plan == plan)

    total = query.count()
    size = max(10, min(100, size))
    rows = (query.order_by(desc(Account.created_at))
            .offset((max(1, page) - 1) * size).limit(size).all())

    out = []
    for a in rows:
        profiller = db.query(Profile).filter(Profile.account_id == a.id).all()
        son = None
        if profiller:
            ids = [p.id for p in profiller]
            r = (db.query(func.max(AnswerLog.answered_at))
                 .filter(AnswerLog.profile_id.in_(ids)).scalar())
            son = str(r) if r else None
        out.append({
            "id": a.id, "email": a.email, "plan": a.plan,
            "is_admin": bool(a.is_admin),
            "plan_expires": str(a.plan_expires) if a.plan_expires else None,
            "created_at": str(a.created_at),
            "profile_count": len(profiller),
            "last_activity": son,
        })
    return {"total": total, "page": page, "pages": (total + size - 1) // size,
            "accounts": out}


class PlanIn(BaseModel):
    plan: str
    days: int | None = None


@router.put("/accounts/{aid}/plan")
def set_plan(aid: str, body: PlanIn, admin: Account = Depends(require_admin),
             db: Session = Depends(get_db)):
    a = db.get(Account, aid)
    if a is None:
        raise HTTPException(404, "Hesap bulunamadı")
    if body.plan not in ("free", "family"):
        raise HTTPException(400, "Geçersiz plan")

    onceki = a.plan
    a.plan = body.plan
    a.plan_expires = (datetime.utcnow() + timedelta(days=body.days)
                      if body.plan == "family" and body.days else None)

    audit(db, admin, "account.plan", aid,
          {"email": a.email, "from": onceki, "to": body.plan,
           "days": body.days})
    db.commit()
    return {"ok": True, "plan": a.plan,
            "expires": str(a.plan_expires) if a.plan_expires else None}


class AdminFlagIn(BaseModel):
    is_admin: bool


@router.put("/accounts/{aid}/admin")
def set_admin(aid: str, body: AdminFlagIn, admin: Account = Depends(require_admin),
              db: Session = Depends(get_db)):
    a = db.get(Account, aid)
    if a is None:
        raise HTTPException(404, "Hesap bulunamadı")
    if a.id == admin.id and not body.is_admin:
        raise HTTPException(400, "Kendi admin yetkinizi kaldıramazsınız")

    a.is_admin = body.is_admin
    audit(db, admin, "account.admin", aid,
          {"email": a.email, "is_admin": body.is_admin})
    db.commit()
    return {"ok": True}


@router.get("/accounts/{aid}/profiles")
def account_profiles(aid: str, admin: Account = Depends(require_admin),
                     db: Session = Depends(get_db)):
    """
    GIZLILIK: Cocugun ADI gosterilmez. Sadece istatistik.
    Destek icin gereken minimum bilgi.
    """
    a = db.get(Account, aid)
    if a is None:
        raise HTTPException(404, "Hesap bulunamadı")

    audit(db, admin, "account.view_profiles", aid, {"email": a.email})
    db.commit()

    out = []
    for p in db.query(Profile).filter(Profile.account_id == aid).all():
        toplam = db.query(AnswerLog).filter(AnswerLog.profile_id == p.id).count()
        dogru = db.query(AnswerLog).filter(
            AnswerLog.profile_id == p.id, AnswerLog.is_correct.is_(True)).count()
        gorev = db.query(DailyQuest).filter(
            DailyQuest.profile_id == p.id,
            DailyQuest.completed_at.isnot(None)).count()
        out.append({
            "id": p.id,
            "grade": p.grade,
            "created_at": str(p.created_at),
            "answers": toplam,
            "accuracy": round(100 * dogru / toplam) if toplam else None,
            "quests_completed": gorev,
            "streak": p.streak_days,
            "stars": p.star_balance,
            "calibrated": bool(p.calibrated),
        })
    return {"account_email": a.email, "profiles": out}


# ================================================================ AUDIT

@router.get("/audit")
def audit_log(action: str | None = None, page: int = 1, size: int = 50,
              admin: Account = Depends(require_admin),
              db: Session = Depends(get_db)):
    query = db.query(AuditLog)
    if action:
        query = query.filter(AuditLog.action.ilike(f"%{action}%"))
    total = query.count()
    size = max(10, min(200, size))
    rows = (query.order_by(desc(AuditLog.created_at))
            .offset((max(1, page) - 1) * size).limit(size).all())
    return {
        "total": total, "page": page, "pages": (total + size - 1) // size,
        "logs": [{
            "id": r.id, "admin_email": r.admin_email, "action": r.action,
            "target": r.target, "detail": r.detail,
            "created_at": str(r.created_at),
        } for r in rows],
    }
