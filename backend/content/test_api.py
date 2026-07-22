"""
Uctan uca API testi. Sunucu calismadan, TestClient ile.

Kullanim:  python content/test_api.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi.testclient import TestClient  # noqa: E402
from main import app  # noqa: E402

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
    print("=" * 55)
    print("MINIZEKI API TESTI")
    print("=" * 55)

    # --- Health ---
    print("\n[Health]")
    r = c.get("/api/health")
    check("health 200", r.status_code == 200)
    check(f"kategori var ({r.json().get('categories')})", r.json()["categories"] > 0)
    check(f"soru var ({r.json().get('questions')})", r.json()["questions"] > 0)

    # --- Kayit ---
    print("\n[Auth]")
    import uuid
    email = f"test-{uuid.uuid4().hex[:8]}@example.com"
    r = c.post("/api/auth/register",
               json={"email": email, "password": "sifre123", "pin": "1234"})
    check("kayit 200", r.status_code == 200, r.text[:100])
    token = r.json()["access_token"]
    H = {"Authorization": f"Bearer {token}"}

    r = c.post("/api/auth/login", json={"email": email, "password": "sifre123"})
    check("giris 200", r.status_code == 200)

    r = c.post("/api/auth/login", json={"email": email, "password": "yanlis"})
    check("yanlis sifre 401", r.status_code == 401)

    r = c.get("/api/quest/today?profile_id=xxx")
    check("tokensiz erisim 401", r.status_code == 401)

    # --- Profil ---
    print("\n[Profil]")
    r = c.post("/api/profiles", headers=H,
               json={"name": "Ali", "avatar_id": "fox", "grade": 2})
    check("profil olustur 200", r.status_code == 200, r.text[:100])
    pid = r.json()["id"]

    # Ucretsiz planda 2. profil engellenmelidir
    r = c.post("/api/profiles", headers=H,
               json={"name": "Zeynep", "avatar_id": "panda", "grade": 1})
    check("ucretsiz plan 2. profil 403", r.status_code == 403)

    # --- Kalibrasyon ---
    print("\n[Kalibrasyon]")
    r = c.get(f"/api/profiles/{pid}/calibrate", headers=H)
    check("kalibrasyon 200", r.status_code == 200, r.text[:150])
    qs = r.json()["questions"]
    check(f"8 soru geldi ({len(qs)})", len(qs) == 8)
    check("dogru cevap SIZMIYOR", all("answer_index" not in q for q in qs))
    check("token var", all("token" in q for q in qs))
    check("4 sik", all(len(q["options"]) == 4 for q in qs))

    r = c.post(f"/api/profiles/{pid}/calibrate", headers=H,
               json={"correct": 7, "total": 8})
    check("kalibrasyon kaydi 200", r.status_code == 200)

    # --- Gunluk gorev ---
    print("\n[Gunluk Gorev]")
    r = c.get(f"/api/quest/today?profile_id={pid}", headers=H)
    check("gorev 200", r.status_code == 200, r.text[:150])
    data = r.json()
    qs = data["questions"]
    check(f"soru sayisi ({len(qs)})", len(qs) >= 8)
    check("dogru cevap SIZMIYOR", all("answer_index" not in q for q in qs))

    # Ayni gun ayni gorev
    r2 = c.get(f"/api/quest/today?profile_id={pid}", headers=H)
    check("ayni gun ayni gorev", r2.json()["quest_id"] == data["quest_id"])

    # Isinma kurali: ilk soru kolay olmali (band token icinde, dolayli test)
    check("ilk soru var", len(qs) > 0 and qs[0]["text"])

    # Kategori cesitliligi
    katlar = {q["category_id"] for q in qs}
    check(f"kategori cesitliligi ({len(katlar)})", len(katlar) >= 4)

    # --- Cevaplama ---
    print("\n[Cevaplama]")
    dogru_sayisi = 0
    for i, q in enumerate(qs):
        # Ilk yarisini dogru, kalanini yanlis cevapla (deterministik degil ama akis testi)
        r = c.post("/api/answer", headers=H,
                   json={"token": q["token"], "selected": 0, "duration_ms": 2000})
        if r.status_code != 200:
            check(f"cevap {i} 200", False, r.text[:100])
            break
        if r.json()["correct"]:
            dogru_sayisi += 1
    else:
        check(f"tum sorular cevaplandi ({len(qs)})", True)

    r = c.post("/api/answer", headers=H,
               json={"token": "gecersiz.token.xxx", "selected": 0})
    check("gecersiz token 400", r.status_code == 400)

    # --- Gorev tamamlama ---
    print("\n[Gorev Tamamlama]")
    r = c.post("/api/quest/complete", headers=H,
               json={"quest_id": data["quest_id"], "correct": dogru_sayisi,
                     "total": len(qs)})
    check("tamamlama 200", r.status_code == 200, r.text[:100])
    res = r.json()
    check(f"seri basladi ({res.get('streak')})", res.get("streak") == 1)
    check(f"yildiz kazanildi ({res.get('star_balance')})", res.get("star_balance", 0) > 0)
    check("rozet verildi", len(res.get("new_badges", [])) > 0)

    # --- Kategoriler ---
    print("\n[Kategoriler]")
    r = c.get(f"/api/categories?profile_id={pid}", headers=H)
    check("kategoriler 200", r.status_code == 200)
    kats = r.json()["categories"]
    check(f"2. sinif kategorileri ({len(kats)})", len(kats) > 10)
    kilitli = [k for k in kats if k["locked"]]
    check(f"ucretsiz planda kilitli kategori var ({len(kilitli)})", len(kilitli) > 0)

    # MUFREDAT: 2. sinifta bolme OLMAMALI
    check("2. sinifta bolme YOK", not any(k["id"] == "bolme" for k in kats))
    check("2. sinifta kesir YOK", not any(k["id"] == "kesir" for k in kats))
    check("2. sinifta carpim VAR", any(k["id"] == "carpim" for k in kats))

    # --- Serbest oyun ---
    print("\n[Serbest Oyun]")
    r = c.get(f"/api/play/carpim?profile_id={pid}&count=10", headers=H)
    check("serbest oyun 200", r.status_code == 200, r.text[:100])
    if r.status_code == 200:
        check("10 soru", len(r.json()["questions"]) == 10)

    r = c.get(f"/api/play/basamak?profile_id={pid}", headers=H)
    check("kilitli kategori 402", r.status_code == 402)

    # --- Zeki'nin Evi ---
    print("\n[Zeki'nin Evi]")
    r = c.get(f"/api/house?profile_id={pid}", headers=H)
    check("ev 200", r.status_code == 200)
    ev = r.json()
    check(f"esyalar var ({ev['total_count']})", ev["total_count"] > 0)

    ucuz = min(ev["items"], key=lambda i: i["price"])
    r = c.post("/api/house/buy", headers=H,
               json={"profile_id": pid, "item_id": ucuz["id"]})
    # Yildiz yetmiyorsa 400 doner - ikisi de gecerli
    check("satin alma calisiyor", r.status_code in (200, 400), r.text[:80])

    # --- Ebeveyn paneli ---
    print("\n[Ebeveyn Paneli]")
    r = c.get(f"/api/parent/dashboard?profile_id={pid}", headers=H)
    check("PIN'siz panel 403", r.status_code == 403)

    r = c.post("/api/auth/verify-pin", headers=H, json={"pin": "9999"})
    check("yanlis PIN 401", r.status_code == 401)

    r = c.post("/api/auth/verify-pin", headers=H, json={"pin": "1234"})
    check("dogru PIN 200", r.status_code == 200, r.text[:80])
    PH = {"Authorization": f"Bearer {r.json()['pin_token']}"}

    r = c.get(f"/api/parent/dashboard?profile_id={pid}", headers=PH)
    check("panel 200", r.status_code == 200, r.text[:150])
    if r.status_code == 200:
        d = r.json()
        check("ozet var", "summary" in d)
        check("kategoriler var", len(d.get("categories", [])) > 0)
        check("sinif dagilimi var", "grade_distribution" in d)

    # Ders agirligi
    r = c.put(f"/api/parent/settings?profile_id={pid}", headers=PH,
              json={"subject_weights": {"matematik": 1.5, "turkce": 1.0,
                                        "hayat_bilgisi": 0.5, "ingilizce": 0.5}})
    check("ders agirligi 200", r.status_code == 200, r.text[:100])
    if r.status_code == 200:
        pv = r.json()["preview"]
        mat = next((p for p in pv if p["subject"] == "matematik"), None)
        check(f"matematik payi artti ({mat['percent'] if mat else '?'}%)",
              mat and mat["percent"] > 25)
        check("hicbir ders %10 alti degil", all(p["percent"] >= 9 for p in pv))
        check("hicbir ders %45 ustu degil", all(p["percent"] <= 46 for p in pv))

    # Odak modu
    r = c.put(f"/api/parent/focus?profile_id={pid}", headers=PH,
              json={"category_id": "carpim", "weeks": 1})
    check("odak modu 200", r.status_code == 200, r.text[:100])

    # Veri disari aktarma (KVKK)
    r = c.get(f"/api/parent/export?profile_id={pid}", headers=PH)
    check("veri export 200", r.status_code == 200)

    # --- Sonuc ---
    print("\n" + "=" * 55)
    print(f"BASARILI: {OK}   BASARISIZ: {FAIL}")
    print("=" * 55)
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
