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

    # ================= OKUMA VE ANLAMA =================
    print("\n[Okuma ve Anlama]")
    from models import SessionLocal as _SL, StoryQuestion as _SQ
    from collections import Counter as _C

    rr = c.get(f"/api/reading/story?profile_id={pid}", headers=H)
    check("metin alma 200", rr.status_code == 200, rr.text[:80])

    if rr.status_code == 200:
        st = rr.json()
        check(f"metin var ({st['word_count']} kelime)", st["word_count"] > 15)
        check("5 soru bagli", st["question_count"] == 5)

        rq = c.get(f"/api/reading/questions?story_id={st['id']}"
                   f"&profile_id={pid}", headers=H)
        check("sorular 200", rq.status_code == 200)
        oq = rq.json()["questions"]
        check(f"5 soru geldi ({len(oq)})", len(oq) == 5)
        check("dogru cevap SIZMIYOR", all("answer_index" not in x for x in oq))
        check(f"soru turleri cesitli ({len({x['type'] for x in oq})})",
              len({x["type"] for x in oq}) >= 2)

        # Metinde satir kirilmasi olmamali (kaynak dosyadaki bicimlendirme
        # ekrana sizmamali) - tek \n sadece paragraf ayrimi icin olabilir
        _tekli = [x for x in st["text"].split("\n\n")
                  if "\n" in x]
        check("metinde cumle ortasi satir kirilmasi yok", len(_tekli) == 0)

        # Tam dogru -> rozet + odul
        _db = _SL()
        _dogru = [q.answer_index for q in _db.query(_SQ)
                  .filter(_SQ.story_id == st["id"])
                  .order_by(_SQ.sort_order).all()]
        _db.close()
        rc = c.post("/api/reading/complete", headers=H, json={
            "profile_id": pid, "story_id": st["id"], "mode": "timed",
            "duration_ms": 45000, "answers": _dogru})
        check("okuma tamamlama 200", rc.status_code == 200, rc.text[:80])
        if rc.status_code == 200:
            dd = rc.json()
            check(f"tam dogru ({dd['correct']}/{dd['total']})",
                  dd["correct"] == dd["total"])
            check("hiz hesaplandi", dd.get("speed") is not None)
            check("odul verildi", len(dd.get("rewards", [])) > 0)
            # Bug: reading.py rozet kontrolunu hic cagirmiyordu
            check("new_badges alani var", "new_badges" in dd)
            check(f"okuma rozeti verildi ({len(dd.get('new_badges', []))})",
                  len(dd.get("new_badges", [])) > 0)

        # Sessiz okuma: hiz olculmemeli
        st2 = c.get(f"/api/reading/story?profile_id={pid}", headers=H).json()
        rc2 = c.post("/api/reading/complete", headers=H, json={
            "profile_id": pid, "story_id": st2["id"], "mode": "silent",
            "answers": [0, 0, 0, 0, 0]})
        check("sessiz okumada hiz yok",
              rc2.status_code == 200 and rc2.json().get("speed") is None)

        # Imkansiz hizli -> supheli
        st3 = c.get(f"/api/reading/story?profile_id={pid}", headers=H).json()
        rc3 = c.post("/api/reading/complete", headers=H, json={
            "profile_id": pid, "story_id": st3["id"], "mode": "timed",
            "duration_ms": 2000, "answers": [0, 0, 0, 0, 0]})
        check("okumadan gecme tespit edildi",
              rc3.status_code == 200 and rc3.json().get("suspicious") is True)

    # Bug: tum dogru cevaplar A sikkindaydi
    _db = _SL()
    _dag = _C(x.answer_index for x in _db.query(_SQ).all())
    _db.close()
    _tp = sum(_dag.values())
    if _tp > 20:
        _en = max(_dag.values())
        check(f"okuma cevaplari dengeli (en cok %{100 * _en // _tp})",
              _en <= _tp * 0.45)

    # Okuma sorulari /api/answer'a gitse bile kategori istatistigine
    # KARISMAMALI. Asil kayit ReadingSession'da tutulur; ikisi birden
    # olursa cevap iki kez sayilir ve seviye motoru bozulur.
    from models import AnswerLog as _AL
    st4 = c.get(f"/api/reading/story?profile_id={pid}", headers=H).json()
    oq4 = c.get(f"/api/reading/questions?story_id={st4['id']}"
                f"&profile_id={pid}", headers=H).json()["questions"]
    _db = _SL()
    _once = _db.query(_AL).filter(_AL.profile_id == pid,
                                  _AL.category_id == "okuma").count()
    _db.close()
    ra = c.post("/api/answer", headers=H, json={
        "token": oq4[0]["token"], "selected": 0, "duration_ms": 0})
    check("okuma sorusu /api/answer ile cevaplanabiliyor",
          ra.status_code == 200, ra.text[:80])
    if ra.status_code == 200:
        check("cevap dogru/yanlis donuyor", "answer_index" in ra.json())
    _db = _SL()
    _sonra = _db.query(_AL).filter(_AL.profile_id == pid,
                                   _AL.category_id == "okuma").count()
    _db.close()
    check("okuma cevabi AnswerLog'a yazilmiyor", _sonra == _once)

    # Okuma gunluk goreve GIRMEMELI (tek basina 1-2 dakika surer)
    rq2 = c.get(f"/api/quest/today?profile_id={pid}", headers=H)
    if rq2.status_code == 200:
        check("okuma gunluk goreve girmiyor",
              "okuma" not in {x["category_id"] for x in rq2.json()["questions"]})

    # --- Tur ici tekrar (regresyon) ---
    # Bug: ayni tur icinde ayni soru birden fazla kez gelebiliyordu.
    # Cocuk 10 soruluk turda 7 kez ayni soruyu goruyordu.
    print("\n[Tur ici tekrar]")
    from collections import Counter
    tekrar_toplam = 0
    for kat_id in ["es_anlamli", "okulumuz", "geometri", "carpim", "saat"]:
        rr = c.get(f"/api/play/{kat_id}?profile_id={pid}&count=10", headers=H)
        if rr.status_code != 200:
            continue
        qq = rr.json()["questions"]
        imza = [(x["text"], tuple(x["options"]), (x.get("svg") or "")[:60])
                for x in qq]
        tekrar_toplam += len(imza) - len(set(imza))
    check(f"serbest oyunda tur ici tekrar yok ({tekrar_toplam})",
          tekrar_toplam == 0)

    rr = c.get(f"/api/quest/today?profile_id={pid}", headers=H)
    if rr.status_code == 200:
        qq = rr.json()["questions"]
        imza = [(x["text"], tuple(x["options"]), (x.get("svg") or "")[:60])
                for x in qq]
        check(f"gunluk gorevde tekrar yok ({len(imza) - len(set(imza))})",
              len(imza) == len(set(imza)))

    # --- Sonuc ---
    print("\n" + "=" * 55)
    print(f"BASARILI: {OK}   BASARISIZ: {FAIL}")
    print("=" * 55)
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
