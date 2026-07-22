"""
Admin paneli API testi.

Kullanim:  python content/test_admin.py
"""
import sys
import os
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# Sunucu import edilmeden ONCE ayarlanmali
os.environ["ADMIN_PASSWORD"] = "test-admin-sifresi"

import config as cfg  # noqa: E402
cfg.ADMIN_PASSWORD = "test-admin-sifresi"

from fastapi.testclient import TestClient  # noqa: E402
from main import app  # noqa: E402
from models import SessionLocal, Account, Question  # noqa: E402

c = TestClient(app)
OK, FAIL = 0, 0


def check(ad, kosul, detay=""):
    global OK, FAIL
    if kosul:
        OK += 1
        print(f"  OK   {ad}")
    else:
        FAIL += 1
        print(f"  FAIL {ad} {detay}")


def main():
    print("=" * 58)
    print("ADMIN PANELI TESTI")
    print("=" * 58)

    # --- Hazirlik: 2 hesap (biri admin, biri normal) ---
    admin_email = f"admin-{uuid.uuid4().hex[:8]}@test.com"
    user_email = f"user-{uuid.uuid4().hex[:8]}@test.com"

    r = c.post("/api/auth/register", json={
        "email": admin_email, "password": "sifre123", "pin": "1234"})
    AT = r.json()["access_token"]
    AH = {"Authorization": f"Bearer {AT}"}

    r = c.post("/api/auth/register", json={
        "email": user_email, "password": "sifre123", "pin": "5678"})
    UT = r.json()["access_token"]
    UH = {"Authorization": f"Bearer {UT}"}

    # --- Yetki: admin olmayan giremez ---
    print("\n[Yetki]")
    r = c.post("/api/admin/login", headers=UH, json={"password": "test-admin-sifresi"})
    check("admin olmayan hesap 403", r.status_code == 403, r.text[:80])

    r = c.post("/api/admin/login", headers=AH, json={"password": "test-admin-sifresi"})
    check("is_admin=False iken 403", r.status_code == 403)

    # Hesabi admin yap
    db = SessionLocal()
    acc = db.query(Account).filter(Account.email == admin_email).first()
    acc.is_admin = True
    db.commit()
    db.close()

    r = c.post("/api/admin/login", headers=AH, json={"password": "yanlis-sifre"})
    check("yanlis admin sifresi 401", r.status_code == 401)

    r = c.post("/api/admin/login", headers=AH, json={"password": "test-admin-sifresi"})
    check("dogru sifre + is_admin 200", r.status_code == 200, r.text[:80])
    ADM = {"Authorization": f"Bearer {r.json()['admin_token']}"}

    # Normal access_token admin ucuna erisemez
    r = c.get("/api/admin/overview", headers=AH)
    check("access_token admin ucuna giremez 403", r.status_code == 403)

    r = c.get("/api/admin/overview", headers=UH)
    check("normal kullanici admin ucuna giremez", r.status_code in (401, 403))

    # --- Genel bakis ---
    print("\n[Genel bakis]")
    r = c.get("/api/admin/overview", headers=ADM)
    check("overview 200", r.status_code == 200, r.text[:100])
    d = r.json()
    check(f"hesap sayisi ({d['users']['accounts']})", d["users"]["accounts"] >= 2)
    check(f"kategori ({d['content']['categories']})", d["content"]["categories"] > 0)
    check(f"canli soru ({d['content']['questions_live']})",
          d["content"]["questions_live"] > 0)
    check(f"ureteç ({d['content']['generators']})", d["content"]["generators"] == 18)
    check("saglik durumu var", "status" in d["health"])

    r = c.get("/api/admin/activity-chart?days=14", headers=ADM)
    check("aktivite grafigi 200", r.status_code == 200)
    check("14 gunluk veri", len(r.json()["data"]) == 14)

    # --- Kategoriler ---
    print("\n[Kategoriler]")
    r = c.get("/api/admin/categories", headers=ADM)
    check("kategoriler 200", r.status_code == 200)
    kats = r.json()["categories"]
    # Kategori sayisi icerik eklendikce artar - sabit sayi beklemek yerine
    # DB ile seed_data tutarliligini kontrol et
    from content.seed_data import CATEGORIES
    check(f"kategori sayisi seed ile ayni ({len(kats)}/{len(CATEGORIES)})",
          len(kats) == len(CATEGORIES))
    proc = [k for k in kats if k["is_procedural"]]
    beklenen_proc = len([c for c in CATEGORIES if c[6]])
    check(f"prosedurel sayisi ({len(proc)}/{beklenen_proc})",
          len(proc) == beklenen_proc)
    # Mufredat: 1-2. sinifta Fen olmamali
    fen_alt = [k for k in kats if k["subject"] == "fen" and k["grade_min"] <= 2]
    check("1-2. sinifta Fen kategorisi YOK", len(fen_alt) == 0)
    sos_alt = [k for k in kats if k["subject"] == "sosyal" and k["grade_min"] <= 3]
    check("1-3. sinifta Sosyal kategorisi YOK", len(sos_alt) == 0)

    # --- Uretecler ---
    print("\n[Uretecler]")
    r = c.get("/api/admin/generators", headers=ADM)
    check("uretec listesi 200", r.status_code == 200)
    check(f"18 uretec ({len(r.json()['generators'])})",
          len(r.json()["generators"]) == 18)

    r = c.get("/api/admin/generators/carpim/preview?grade=2&band=3&count=5",
              headers=ADM)
    check("uretec onizleme 200", r.status_code == 200, r.text[:80])
    if r.status_code == 200:
        s = r.json()["samples"]
        check(f"5 ornek ({len(s)})", len(s) == 5)
        check("her ornekte 4 sik", all(len(x["options"]) == 4 for x in s))
        # MUFREDAT: 2. sinif carpim max 5
        carpanlar = []
        for x in s:
            try:
                carpanlar.append(int(x["text"].split("×")[0].strip()))
            except Exception:
                pass
        check(f"2.sinif carpim <=5 ({max(carpanlar) if carpanlar else '?'})",
              all(a <= 5 for a in carpanlar))

    r = c.get("/api/admin/generators/saat/preview?grade=2&band=2", headers=ADM)
    check("saat SVG uretiyor", r.status_code == 200 and r.json()["samples"][0]["svg"])

    # --- Sorular ---
    print("\n[Sorular]")
    r = c.get("/api/admin/questions?size=10", headers=ADM)
    check("soru listesi 200", r.status_code == 200)
    check(f"toplam soru ({r.json()['total']})", r.json()["total"] > 300)

    r = c.get("/api/admin/questions?category_id=es_anlamli", headers=ADM)
    check(f"kategori filtresi ({r.json()['total']})", r.json()["total"] > 0)

    r = c.get("/api/admin/questions?q=okul", headers=ADM)
    check(f"metin arama ({r.json()['total']})", r.json()["total"] > 0)

    # Yeni soru
    yeni = {
        "category_id": "es_anlamli", "grade_min": 2, "grade_max": 4, "band": 2,
        "text": "TEST: 'deneme' kelimesinin eş anlamlısı?",
        "options": ["sınama", "başlangıç", "bitiş", "orta"],
        "answer_index": 0, "explanation": "deneme = sınama", "status": "draft",
    }
    r = c.post("/api/admin/questions", headers=ADM, json=yeni)
    check("soru ekle 200", r.status_code == 200, r.text[:100])
    qid = r.json().get("id")

    r = c.post("/api/admin/questions", headers=ADM, json=yeni)
    check("ayni soru tekrar 409", r.status_code == 409)

    # Prosedurel kategoriye soru eklenemez
    kotu = dict(yeni, category_id="carpim", text="TEST prosedurel")
    r = c.post("/api/admin/questions", headers=ADM, json=kotu)
    check("prosedurel kategoriye soru 400", r.status_code == 400, r.text[:80])

    # Tekrar eden sik
    kotu = dict(yeni, text="TEST tekrar sik",
                options=["a", "a", "b", "c"])
    r = c.post("/api/admin/questions", headers=ADM, json=kotu)
    check("tekrar eden sik 400", r.status_code == 400)

    # Kategori sinif araligi disi
    # NOT: Sabit sinif yazmak yerine kategorinin GERCEK araligini okuyup
    # disina cikiyoruz - kategori araligi degisirse test bozulmasin.
    kats_all = c.get("/api/admin/categories", headers=ADM).json()["categories"]
    hedef = next(k for k in kats_all if k["id"] == "es_anlamli")
    if hedef["grade_min"] > 1:
        disari = {"grade_min": 1, "grade_max": 1}          # alt sinira sarkma
    elif hedef["grade_max"] < 4:
        disari = {"grade_min": 4, "grade_max": 4}          # ust sinira sarkma
    else:
        disari = None                                       # kategori 1-4 tamamini kapsiyor
    if disari:
        kotu = dict(yeni, text="TEST sinif disi", **disari)
        r = c.post("/api/admin/questions", headers=ADM, json=kotu)
        check("kategori sinif araligi disi 400", r.status_code == 400, r.text[:80])
    else:
        # Kategori tum siniflari kapsiyorsa baska bir kategoriyle dene
        dar = next((k for k in kats_all
                    if not k["is_procedural"] and k["grade_min"] > 1), None)
        if dar:
            kotu = dict(yeni, category_id=dar["id"], text="TEST sinif disi",
                        grade_min=1, grade_max=1)
            r = c.post("/api/admin/questions", headers=ADM, json=kotu)
            check("kategori sinif araligi disi 400", r.status_code == 400, r.text[:80])
        else:
            check("kategori sinif araligi kontrolu (atlandi)", True)

    # Durum degistir
    r = c.put(f"/api/admin/questions/{qid}/status", headers=ADM,
              json={"status": "live"})
    check("taslak -> canli 200", r.status_code == 200)

    # Guncelle
    guncel = dict(yeni, text="TEST: guncellenmis soru", status="live")
    r = c.put(f"/api/admin/questions/{qid}", headers=ADM, json=guncel)
    check("soru guncelle 200", r.status_code == 200, r.text[:80])

    # Sil
    r = c.delete(f"/api/admin/questions/{qid}", headers=ADM)
    check("soru sil 200", r.status_code == 200, r.text[:80])

    # --- Ice/disa aktarma ---
    print("\n[Ice/disa aktarma]")
    # Benzersiz metin: test tekrar calistiginda 'zaten var' hatasi olmasin
    tag = uuid.uuid4().hex[:6]
    rows = [
        [2, 2, 4, f"IMPORT {tag} 1: 'hızlı' eş anlamlısı?",
         ["çabuk", "yavaş", "ağır", "durgun"], 0, "hızlı = çabuk"],
        [3, 2, 4, f"IMPORT {tag} 2: 'küçük' eş anlamlısı?",
         ["ufak", "büyük", "geniş", "uzun"], 0, "küçük = ufak"],
        [9, 2, 4, f"IMPORT {tag} HATALI: band 9",
         ["a", "b", "c", "d"], 0, ""],                    # band gecersiz
        [2, 2, 4, f"IMPORT {tag} HATALI: tekrar sik",
         ["a", "a", "c", "d"], 0, ""],                    # sik tekrari
    ]
    r = c.post("/api/admin/questions/import", headers=ADM,
               json={"category_id": "es_anlamli", "rows": rows,
                     "status": "draft"})
    check("ice aktarma 200", r.status_code == 200, r.text[:100])
    if r.status_code == 200:
        d = r.json()
        check(f"2 gecerli eklendi ({d['added']})", d["added"] == 2)
        check(f"2 hata yakalandi ({d['error_count']})", d["error_count"] == 2)

    # Ayni satirlar tekrar -> hepsi 'zaten var' (idempotent)
    r = c.post("/api/admin/questions/import", headers=ADM,
               json={"category_id": "es_anlamli", "rows": rows[:2],
                     "status": "draft"})
    check("tekrar ice aktarma idempotent",
          r.status_code == 200 and r.json()["added"] == 0,
          r.text[:80])

    r = c.get("/api/admin/questions/export?category_id=es_anlamli", headers=ADM)
    check("disa aktarma 200", r.status_code == 200)
    check(f"satir formati dogru", r.status_code == 200
          and len(r.json()["rows"][0]) == 7)

    # --- Kalibrasyon ---
    print("\n[Kalibrasyon]")
    # Yapay istatistik: band 1 (%90 hedef) ama gercekte %20 -> cok zor
    db = SessionLocal()
    q = db.query(Question).filter(Question.status == "live").first()
    q.band = 1
    q.serve_count = 100
    q.correct_count = 20
    db.commit()
    test_qid = q.id
    db.close()

    r = c.get("/api/admin/calibration?only_bad=true", headers=ADM)
    check("kalibrasyon 200", r.status_code == 200, r.text[:80])
    if r.status_code == 200:
        d = r.json()
        bulunan = next((x for x in d["questions"] if x["id"] == test_qid), None)
        check("sapan soru yakalandi", bulunan is not None)
        if bulunan:
            check(f"gercek dogruluk %20 ({bulunan['real_accuracy']})",
                  bulunan["real_accuracy"] == 20)
            check(f"band 5 onerildi ({bulunan['suggested_band']})",
                  bulunan["suggested_band"] == 5)
            check(f"'Cok zor' teshisi ({bulunan['verdict']})",
                  bulunan["verdict"] == "Çok zor")

    r = c.post("/api/admin/calibration/apply", headers=ADM)
    check("kalibrasyon uygula 200", r.status_code == 200)
    db = SessionLocal()
    q = db.get(Question, test_qid)
    check(f"band duzeltildi 1->{q.band}", q.band == 5)
    db.close()

    # --- Hesaplar ---
    print("\n[Hesaplar]")
    r = c.get("/api/admin/accounts", headers=ADM)
    check("hesap listesi 200", r.status_code == 200)
    check(f"hesaplar geldi ({r.json()['total']})", r.json()["total"] >= 2)

    r = c.get(f"/api/admin/accounts?q={user_email[:8]}", headers=ADM)
    check("e-posta arama", r.status_code == 200 and r.json()["total"] >= 1)

    uid = next(a["id"] for a in c.get("/api/admin/accounts", headers=ADM).json()
               ["accounts"] if a["email"] == user_email)

    r = c.put(f"/api/admin/accounts/{uid}/plan", headers=ADM,
              json={"plan": "family", "days": 30})
    check("plan degistir 200", r.status_code == 200, r.text[:80])
    check("plan family oldu", r.json()["plan"] == "family")

    # Kendi adminligini kaldiramaz
    aid = next(a["id"] for a in c.get("/api/admin/accounts", headers=ADM).json()
               ["accounts"] if a["email"] == admin_email)
    r = c.put(f"/api/admin/accounts/{aid}/admin", headers=ADM,
              json={"is_admin": False})
    check("kendi adminligini kaldiramaz 400", r.status_code == 400)

    # Profil gizliligi
    r = c.get(f"/api/admin/accounts/{uid}/profiles", headers=ADM)
    check("hesap profilleri 200", r.status_code == 200)
    if r.status_code == 200:
        ps = r.json()["profiles"]
        check("cocuk ADI gosterilmiyor (gizlilik)",
              all("name" not in p for p in ps))

    # --- Audit ---
    print("\n[Audit log]")
    r = c.get("/api/admin/audit", headers=ADM)
    check("audit 200", r.status_code == 200)
    logs = r.json()["logs"]
    check(f"islemler kaydedildi ({len(logs)})", len(logs) > 5)
    aksiyonlar = {l["action"] for l in logs}
    check("question.create kaydi var", "question.create" in aksiyonlar)
    check("account.plan kaydi var", "account.plan" in aksiyonlar)
    check("calibration.apply kaydi var", "calibration.apply" in aksiyonlar)
    check("admin.login_failed kaydi var", "admin.login_failed" in aksiyonlar)

    # --- Panel kapali senaryosu ---
    print("\n[Panel kapali]")
    eski = cfg.ADMIN_PASSWORD
    cfg.ADMIN_PASSWORD = ""
    r = c.post("/api/admin/login", headers=AH, json={"password": "x"})
    check("ADMIN_PASSWORD yoksa 503", r.status_code == 503, r.text[:80])
    cfg.ADMIN_PASSWORD = eski

    print("\n" + "=" * 58)
    print(f"BASARILI: {OK}   BASARISIZ: {FAIL}")
    print("=" * 58)
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
