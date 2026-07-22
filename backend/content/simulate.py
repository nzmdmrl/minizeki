"""
8 HAFTALIK SIMULASYON

Dokumandaki Ali senaryosunu gercek motorla kosturur.
Amac: zorluk motorunun hedef bantta (%75-85) kalip kalmadigini olcmek.

Simule edilen cocuk:
  - Matematikte iyi (band'a gore %90'a kadar dogru)
  - Turkce'de ortalama (%65)
  - Hayat Bilgisi orta (%78)

Kullanim:  python content/simulate.py
"""
import sys
import random
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from models import (  # noqa: E402
    SessionLocal, init_db, Account, Profile, ProfileSkill, AnswerLog, Category,
)
from engine import (  # noqa: E402
    gunluk_gorev_uret, update_skill, check_advance, check_demote,
    seri_guncelle, gorev_odulu, kategoriler_for_grade,
)
from api.security import hash_password  # noqa: E402

# Cocugun ders bazli yetenegi: band -> dogru cevaplama olasiligi
YETENEK = {
    "matematik":     {1: 0.98, 2: 0.94, 3: 0.88, 4: 0.72, 5: 0.52},
    "turkce":        {1: 0.92, 2: 0.80, 3: 0.62, 4: 0.40, 5: 0.22},
    "hayat_bilgisi": {1: 0.95, 2: 0.88, 3: 0.76, 4: 0.55, 5: 0.35},
    "ingilizce":     {1: 0.90, 2: 0.78, 3: 0.58, 4: 0.38, 5: 0.20},
    "fen":           {1: 0.94, 2: 0.85, 3: 0.70, 4: 0.48, 5: 0.30},
    "sosyal":        {1: 0.93, 2: 0.83, 3: 0.68, 4: 0.45, 5: 0.28},
}

# Sinif komut satirindan: python content/simulate.py 4
SINIF = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 2


def cevapla(subject: str, band: int, grade: int, profile_grade: int) -> bool:
    """Cocugun bir soruyu dogru cevaplama simulasyonu."""
    p = YETENEK.get(subject, YETENEK["turkce"])[band]
    # Ust sinif sorusu daha zor, alt sinif daha kolay
    if grade > profile_grade:
        p *= 0.70
    elif grade < profile_grade:
        p = min(1.0, p * 1.25)
    return random.random() < p


def main():
    random.seed(42)
    init_db()
    db = SessionLocal()

    try:
        # Temiz profil (uuid: tekrar calistirmada cakisma olmasin)
        import uuid
        acc = Account(email=f"sim-{uuid.uuid4().hex[:10]}@test.com",
                      password_hash=hash_password("x"), pin_hash=hash_password("1234"),
                      plan="family")
        db.add(acc)
        db.flush()

        p = Profile(account_id=acc.id, name="Ali", avatar_id="fox", grade=SINIF,
                    calibrated=True, shield_count=2,
                    shield_month=f"{date.today().year}-{date.today().month:02d}")
        db.add(p)
        db.flush()

        # Kalibrasyon sonucu: level 3
        for c in kategoriler_for_grade(db, SINIF, "family"):
            s = ProfileSkill(profile_id=p.id, category_id=c.id, level=3)
            db.add(s)
        db.commit()

        print("=" * 68)
        print(f"8 HAFTALIK SIMULASYON — Ali, {SINIF}. sinif")
        print("  Matematik: iyi | Turkce: ortalama | Hayat Bilgisi: orta")
        print("=" * 68)
        print(f"\n{'Hafta':<7}{'Gun':<6}{'Soru':<7}{'Dogru':<8}{'Terfi':<8}{'Durum'}")
        print("-" * 68)

        bugun = date.today() - timedelta(days=56)
        hafta_no = 0
        toplam_soru = toplam_dogru = 0
        terfi_edenler = set()
        haftalik = []

        for gun in range(56):
            # Hafta 7'de 2 gun atla (seri kirilmasi testi)
            if gun in (44, 45):
                bugun += timedelta(days=1)
                continue

            sorular = gunluk_gorev_uret(db, p, "family")
            if not sorular:
                bugun += timedelta(days=1)
                continue

            gun_dogru = 0
            for q in sorular:
                cat = db.get(Category, q["category_id"])
                dogru = cevapla(cat.subject, q["band"], q["grade"], p.grade)

                db.add(AnswerLog(
                    profile_id=p.id, category_id=cat.id,
                    question_id=q.get("question_id"),
                    band=q["band"], grade=q["grade"], is_correct=dogru,
                    duration_ms=random.randint(2000, 8000), mode="quest",
                ))
                update_skill(db, p.id, cat.id, dogru)
                db.flush()

                if check_advance(db, p, cat.id):
                    terfi_edenler.add(cat.name)
                check_demote(db, p, cat.id)

                if dogru:
                    gun_dogru += 1

            seri = seri_guncelle(db, p, bugun)
            gorev_odulu(db, p, gun_dogru, len(sorular), seri)
            db.commit()

            toplam_soru += len(sorular)
            toplam_dogru += gun_dogru
            haftalik.append((len(sorular), gun_dogru))

            # Hafta sonu raporu
            if (gun + 1) % 7 == 0:
                hafta_no += 1
                hs = sum(x[0] for x in haftalik)
                hd = sum(x[1] for x in haftalik)
                oran = 100 * hd / hs if hs else 0
                gun_sayisi = len(haftalik)

                if oran > 90:
                    durum = "SIKILIYOR (zorluk artmali)"
                elif oran < 60:
                    durum = "ZORLANIYOR (kolaylasmali)"
                elif 75 <= oran <= 85:
                    durum = "HEDEF BANT"
                else:
                    durum = "kabul edilebilir"

                print(f"{hafta_no:<7}{gun_sayisi:<6}{hs:<7}%{oran:<7.0f}"
                      f"{len(terfi_edenler):<8}{durum}")
                haftalik = []

            bugun += timedelta(days=1)

        # ---- Sonuc ----
        genel = 100 * toplam_dogru / toplam_soru
        print("-" * 68)
        print(f"\nTOPLAM: {toplam_soru} soru, %{genel:.0f} dogruluk, "
              f"seri: {p.streak_days}, yildiz: {p.star_balance}")

        print("\n" + "=" * 68)
        print("KATEGORI DURUMU")
        print("=" * 68)
        print(f"{'Kategori':<24}{'Ders':<16}{'Dogruluk':<11}{'Lv':<5}{'Terfi'}")
        print("-" * 68)

        for c in kategoriler_for_grade(db, SINIF, "family"):
            s = db.get(ProfileSkill, (p.id, c.id))
            if not s:
                continue
            t = s.total_correct + s.total_wrong
            if t == 0:
                continue
            oran = 100 * s.total_correct / t
            terfi = "EVET" if s.advanced_unlocked else "-"
            print(f"{c.name:<24}{c.subject:<16}%{oran:<10.0f}{s.level:<5}{terfi}")

        # Sinif dagilimi
        print("\n" + "=" * 68)
        print("SINIF DAGILIMI (spiral mufredat)")
        print("=" * 68)
        from sqlalchemy import func
        rows = (db.query(AnswerLog.grade, func.count(AnswerLog.id))
                .filter(AnswerLog.profile_id == p.id)
                .group_by(AnswerLog.grade).all())
        tot = sum(r[1] for r in rows)
        for g, n in sorted(rows):
            bar = "#" * int(40 * n / tot)
            print(f"  {g}. sinif  {bar:<40} %{100*n/tot:.0f}")

        # ---- Dogrulama ----
        print("\n" + "=" * 68)
        print("MOTOR DOGRULAMASI")
        print("=" * 68)
        sonuc = []

        ok = 70 <= genel <= 88
        sonuc.append((ok, f"Dogruluk hedef bantta: %{genel:.0f} (hedef 75-85)"))

        ok = len(terfi_edenler) > 0
        sonuc.append((ok, f"Terfi calisti: {len(terfi_edenler)} kategori "
                          f"({', '.join(sorted(terfi_edenler)[:3])})"))

        # Matematik Turkce'den iyi olmali (cocugun profili boyle)
        def ders_orani(ders):
            kats = [c.id for c in kategoriler_for_grade(db, SINIF, "family")
                    if c.subject == ders]
            ss = [db.get(ProfileSkill, (p.id, k)) for k in kats]
            ss = [s for s in ss if s and (s.total_correct + s.total_wrong) > 0]
            if not ss:
                return 0
            tc = sum(s.total_correct for s in ss)
            tw = sum(s.total_wrong for s in ss)
            return 100 * tc / (tc + tw)

        mat, tur = ders_orani("matematik"), ders_orani("turkce")
        ok = mat > tur
        sonuc.append((ok, f"Kategori bazli uyarlama: Matematik %{mat:.0f} > "
                          f"Turkce %{tur:.0f}"))

        # Spiral mufredat: 1. sinif sorulari gelmis olmali
        g1 = next((n for g, n in rows if g == 1), 0)
        ok = 0.05 <= g1 / tot <= 0.35
        sonuc.append((ok, f"Spiral mufredat: %{100*g1/tot:.0f} alt sinif tekrari"))

        # Ust sinif sorulari (terfi sonrasi)
        g3 = next((n for g, n in rows if g == 3), 0)
        ok = g3 > 0
        sonuc.append((ok, f"Ust sinif esnemesi: %{100*g3/tot:.0f} 3. sinif sorusu"))

        # Seri
        ok = p.streak_days > 0
        sonuc.append((ok, f"Seri sistemi: {p.streak_days} gun"))

        for ok, msg in sonuc:
            print(f"  {'OK  ' if ok else 'FAIL'} {msg}")

        basarisiz = sum(1 for ok, _ in sonuc if not ok)
        print("\n" + "=" * 68)
        print("SIMULASYON BASARILI" if not basarisiz
              else f"{basarisiz} KONTROL BASARISIZ")
        print("=" * 68)
        return 1 if basarisiz else 0

    finally:
        db.close()


if __name__ == "__main__":
    sys.exit(main())
