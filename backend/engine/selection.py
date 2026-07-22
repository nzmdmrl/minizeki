"""
Kategori secimi + soru secimi.

Gunluk gorev akisi:
  1. Ders agirligina gore kontenjan
  2. Her ders icinde: yarisi zayif, yarisi rotasyon
  3. Odak modu varsa o kategori 6 soru alir
  4. Her kategoriden soru sec (prosedurel -> uret, yazili -> havuzdan)
  5. Isinma kurali: ilk soru kolay
"""
import random
from datetime import datetime, timedelta

from sqlalchemy import func, desc
from sqlalchemy.orm import Session

import config as cfg
from generators import generate
from models import Category, Question, ProfileSkill, SeenQuestion, AnswerLog
from .bands import band_sec, sinif_dagilimi, sinif_sec, durum_belirle
from .level import get_or_create_skill
from .weights import normalize, kontenjan


def kategoriler_for_grade(db: Session, grade: int, plan: str = "family") -> list[Category]:
    q = db.query(Category).filter(
        Category.grade_min <= grade, Category.grade_max >= grade
    )
    if plan == "free":
        q = q.filter(Category.is_free.is_(True))
    return q.order_by(Category.sort_order).all()


def _son_dogruluk(db: Session, profile_id: str, category_id: str, n: int = 8):
    """
    Son N sorudaki dogruluk. Tek kategoriden gunde ~2 soru gelir,
    yani 8 soru ~ son 4 gunluk veri. Daha genis pencere sistemi
    gec tepki verdirir (simulasyon bulgusu).
    """
    rows = (db.query(AnswerLog.is_correct)
            .filter(AnswerLog.profile_id == profile_id,
                    AnswerLog.category_id == category_id)
            .order_by(desc(AnswerLog.answered_at)).limit(n).all())
    if not rows:
        return None
    return sum(1 for r in rows if r[0]) / len(rows)


def secilecek_kategoriler(db: Session, profile, plan: str = "family") -> list[Category]:
    """
    Gunluk gorev icin kategori secimi.
    Her ders kendi kontenjani icinde: yarisi zayif + yarisi rotasyon.
    """
    hepsi = kategoriler_for_grade(db, profile.grade, plan)
    if not hepsi:
        return []

    hedef = cfg.QUEST_CATEGORY_COUNT.get(profile.grade, 8)
    hedef = min(hedef, len(hepsi))

    dersler = sorted({c.subject for c in hepsi})
    oran = normalize(profile.subject_weights or {}, dersler)
    kont = kontenjan(oran, hedef)

    secilen: list[Category] = []
    for ders, adet in kont.items():
        ders_kat = [c for c in hepsi if c.subject == ders]
        if not ders_kat:
            continue
        adet = min(adet, len(ders_kat))

        # Skill bilgisi
        def skill_level(c):
            s = db.get(ProfileSkill, (profile.id, c.id))
            return s.level if s else 2

        def son_gorulme(c):
            s = db.get(ProfileSkill, (profile.id, c.id))
            return (s.last_seen_at if s else None) or datetime(2000, 1, 1)

        # Yarisi zayif (level dusuk), yarisi rotasyon (uzun suredir gorulmemis)
        zayif_adet = adet // 2 + adet % 2
        zayif = sorted(ders_kat, key=skill_level)[:zayif_adet]
        kalan = [c for c in ders_kat if c not in zayif]
        rotasyon = sorted(kalan, key=son_gorulme)[:adet - len(zayif)]

        secilen += zayif + rotasyon

    # Kontenjan yuvarlamasi yuzunden eksik/fazla olabilir
    if len(secilen) < hedef:
        eksik = [c for c in hepsi if c not in secilen]
        eksik.sort(key=lambda c: (db.get(ProfileSkill, (profile.id, c.id)).level
                                  if db.get(ProfileSkill, (profile.id, c.id)) else 2))
        secilen += eksik[:hedef - len(secilen)]
    secilen = secilen[:hedef]

    return secilen


def soru_uret(db: Session, profile, category: Category, adet: int,
              mode: str = "quest") -> list[dict]:
    """Bir kategoriden `adet` soru uretir/secer."""
    skill = get_or_create_skill(db, profile.id, category.id)
    son_dog = _son_dogruluk(db, profile.id, category.id)
    toplam = skill.total_correct + skill.total_wrong
    durum = durum_belirle(skill.level, son_dog, toplam)

    dist = sinif_dagilimi(
        profile.grade, profile.repeat_ratio or 0.20,
        skill.level, skill.advanced_unlocked, skill.advance_ratio or 0.10,
    )

    sorular = []
    for _ in range(adet):
        grade = sinif_sec(dist)
        band = band_sec(skill.level, durum)

        if category.is_procedural:
            q = generate(category.generator_key, grade, band)
            q.update({
                "category_id": category.id,
                "category_name": category.name,
                "category_icon": category.icon,
                "grade": grade,
                "question_id": None,
            })
            sorular.append(q)
        else:
            q = _havuzdan_sec(db, profile, category, grade, band)
            if q:
                sorular.append(q)

    return sorular


def _havuzdan_sec(db: Session, profile, category: Category,
                  grade: int, band: int) -> dict | None:
    """Yazili soru havuzundan secim. 45 gun tekrar filtresi."""
    cutoff = datetime.utcnow() - timedelta(days=cfg.SEEN_QUESTION_COOLDOWN_DAYS)

    gorulen = (db.query(SeenQuestion.question_id)
               .filter(SeenQuestion.profile_id == profile.id,
                       SeenQuestion.last_seen_at > cutoff)
               .scalar_subquery())

    def sorgu(bands: list[int], grades: list[int], filtrele: bool):
        q = db.query(Question).filter(
            Question.category_id == category.id,
            Question.status == "live",
            Question.band.in_(bands),
            Question.grade_min <= max(grades),
            Question.grade_max >= min(grades),
        )
        if filtrele:
            q = q.filter(~Question.id.in_(gorulen))
        return q.order_by(func.random()).first()

    # 1. Tam eslesme
    row = sorgu([band], [grade], True)
    # 2. Komsu bantlar
    if not row:
        row = sorgu([max(1, band - 1), band, min(5, band + 1)], [grade], True)
    # 3. Sinif kisitini gevset
    if not row:
        row = sorgu([1, 2, 3, 4, 5], [profile.grade], True)
    # 4. Havuz yetersiz -> tekrar filtresini kaldir
    if not row:
        row = sorgu([1, 2, 3, 4, 5], [profile.grade], False)
    if not row:
        return None

    return {
        "text": row.text,
        "options": list(row.options),
        "answer_index": row.answer_index,
        "band": row.band,
        "explanation": row.explanation or "",
        "svg": None,
        "emoji": None,
        "image_url": row.image_url,
        "procedural": False,
        "question_id": row.id,
        "category_id": category.id,
        "category_name": category.name,
        "category_icon": category.icon,
        "grade": row.grade_min,
    }


def gunluk_gorev_uret(db: Session, profile, plan: str = "family") -> list[dict]:
    """Gunluk gorevin tam soru listesi."""
    kategoriler = secilecek_kategoriler(db, profile, plan)
    if not kategoriler:
        return []

    # Odak modu: bir kategori 6 soru alir, digerlerinin payi azalir
    odak_id = None
    if profile.focus_category_id and profile.focus_until:
        from datetime import date
        if profile.focus_until >= date.today():
            odak_id = profile.focus_category_id

    sorular: list[dict] = []

    if odak_id and any(c.id == odak_id for c in kategoriler):
        odak_cat = next(c for c in kategoriler if c.id == odak_id)
        sorular += soru_uret(db, profile, odak_cat, cfg.FOCUS_QUESTION_COUNT)

        digerleri = [c for c in kategoriler if c.id != odak_id]
        # Toplam soru sayisi sabit kalsin
        toplam_hedef = len(kategoriler) * cfg.QUEST_PER_CATEGORY
        kalan = toplam_hedef - cfg.FOCUS_QUESTION_COUNT
        if digerleri:
            per = max(1, kalan // len(digerleri))
            for c in digerleri[:kalan // per if per else 0]:
                sorular += soru_uret(db, profile, c, per)
    else:
        for c in kategoriler:
            sorular += soru_uret(db, profile, c, cfg.QUEST_PER_CATEGORY)

    random.shuffle(sorular)

    # ISINMA KURALI: ilk soru her zaman kolay
    # Ilk soruda yanilan cocuk turu birakir.
    sorular.sort(key=lambda q: 0 if q["band"] <= 2 else 1)
    if len(sorular) > 1:
        kolay = [q for q in sorular if q["band"] <= 2]
        zor = [q for q in sorular if q["band"] > 2]
        if kolay:
            ilk = kolay.pop(random.randrange(len(kolay)))
            gerisi = kolay + zor
            random.shuffle(gerisi)
            sorular = [ilk] + gerisi

    return sorular
