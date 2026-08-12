import logging

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

import config as cfg
from models import init_db
from api import auth, profile, play, parent, house, admin, reading, break_time

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("minizeki")

app = FastAPI(
    title="Minizeki API",
    description="İlkokul (1–4. sınıf) eğitim oyunu platformu",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=cfg.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(play.router)
app.include_router(parent.router)
app.include_router(house.router)
app.include_router(admin.router)
app.include_router(reading.router)
app.include_router(break_time.router)


# Reverse proxy'ler (Traefik, nginx) /api onekini keserek isteyi iletebilir.
# Coolify varsayilan olarak boyle yapar:
#     tarayici /api/health  ->  Traefik keser  ->  backend'e /health gelir
# Ama tum route'lar /api ile tanimli oldugu icin 404 olusur.
#
# Bu middleware oneki geri ekler. Iki ortamda da calisir:
#   - Proxy arkasinda: /health gelir -> /api/health'e cevrilir
#   - Dogrudan erisimde: /api/health gelir -> zaten dogru, dokunulmaz
MUAF_YOLLAR = {"/", "/docs", "/redoc", "/openapi.json", "/favicon.ico"}


@app.middleware("http")
async def api_oneki_uyumu(request: Request, call_next):
    yol = request.scope.get("path", "")
    if yol not in MUAF_YOLLAR and not yol.startswith("/api"):
        request.scope["path"] = "/api" + yol
    return await call_next(request)


@app.on_event("startup")
def startup():
    init_db()

    # Sema guncelleme: modele yeni alan eklendiginde mevcut veritabanina
    # da eklenmeli. Yoksa "no such column" hatasi tum uygulamayi coker.
    # Bu adim veri kaybetmez, sadece eksik kolonlari tamamlar.
    try:
        from models.migrate import semayi_guncelle
        yeni = semayi_guncelle()
        if yeni:
            log.info("Sema guncellendi: %s", ", ".join(yeni))
    except Exception as e:
        log.error("Sema guncellenemedi (%s: %s)", type(e).__name__, e)
    log.info("Minizeki API hazir | port=%s | db=%s",
             cfg.PORT, cfg.DATABASE_URL.split("://")[0])
    if not cfg.ADMIN_PASSWORD:
        log.warning("ADMIN_PASSWORD ayarli degil -> admin paneli KAPALI")
    if cfg.SECRET_KEY.startswith("minizeki-dev-secret"):
        log.warning("SECRET_KEY varsayilan! Uretimde MUTLAKA degistirin.")

    _otomatik_seed()


def _otomatik_seed():
    """
    Baslangicta kategori/rozet/esya/soru bankasini senkronize eder.

    NEDEN: Docker/Coolify gibi ortamlarda deploy sonrasi SSH ile
    'python content/seed.py' calistirmak zorunda kalmamak icin.

    GUVENLI MI: Evet, seed idempotenttir —
      - Mevcut sorulari SILMEZ, sadece eksikleri ekler
      - Cocuk verisine (hesap, profil, cevap gecmisi) DOKUNMAZ
      - Ayni soru iki kez eklenmez (metin + dogru cevap kontrolu)

    AUTO_SEED=0 ile kapatilabilir.
    """
    import os
    if os.getenv("AUTO_SEED", "1") not in ("1", "true", "True"):
        log.info("AUTO_SEED kapali - soru bankasi senkronu atlandi")
        return

    try:
        from models import SessionLocal, Question
        from content.seed import (
            seed_categories, seed_badges, seed_house, seed_questions,
            seed_stories, dogrula,
        )
        db = SessionLocal()
        try:
            once = db.query(Question).count()
            k = seed_categories(db)
            b = seed_badges(db)
            h = seed_house(db)
            seed_stories(db)
            eklenen, _ = seed_questions(db)
            sonra = db.query(Question).count()

            if k or b or h or eklenen:
                log.info("Seed: +%d kategori, +%d rozet, +%d esya, +%d soru "
                         "(toplam %d -> %d)", k, b, h, eklenen, once, sonra)
            else:
                log.info("Seed: degisiklik yok (%d soru)", sonra)

            for uyari in dogrula(db):
                log.warning("Seed uyarisi: %s", uyari)
        finally:
            db.close()
    except Exception as e:
        # Seed hatasi uygulamayi DUSURMEMELI - mevcut sorularla calismaya devam et
        log.error("Otomatik seed basarisiz (%s: %s) - uygulama devam ediyor",
                  type(e).__name__, e)


@app.get("/api/health")
def health():
    from models import SessionLocal, Category, Question
    db = SessionLocal()
    try:
        return {
            "status": "ok",
            "categories": db.query(Category).count(),
            "questions": db.query(Question).count(),
        }
    finally:
        db.close()


# Tanitim sayfasi bu ucu kullanir. Icerik buyudukce sayfadaki rakamlar
# kendiliginden guncellensin diye var.
#
# GUVENLIK: Auth YOK cunku giris yapmamis ziyaretci cagirir.
# Bu yuzden SADECE icerik istatistigi doner — hicbir cocuk/hesap verisi yok.
_STATS_CACHE: dict = {"veri": None, "zaman": 0.0}
_STATS_TTL = 600  # 10 dakika

DERS_ADLARI = {
    "matematik": "Matematik",
    "turkce": "Türkçe",
    "hayat_bilgisi": "Hayat Bilgisi",
    "fen": "Fen Bilimleri",
    "sosyal": "Sosyal Bilgiler",
    "ingilizce": "İngilizce",
}
DERS_SIRASI = ["matematik", "turkce", "hayat_bilgisi", "fen", "sosyal", "ingilizce"]


@app.get("/api/public/stats")
def public_stats(response: Response):
    """Tanitim sayfasi icin icerik ozeti. Cocuk verisi icermez."""
    import time
    from models import SessionLocal, Category, Question

    # Bu uc herkese acik: auth yok, cocuk verisi yok, sadece icerik sayilari
    # (zaten sitede gorunen bilgi). Boylece FRONTEND_ORIGIN yanlis ayarlansa
    # bile tanitim sayfasi canli rakamlari gosterebilir.
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Cache-Control"] = "public, max-age=600"

    simdi = time.time()
    if _STATS_CACHE["veri"] and simdi - _STATS_CACHE["zaman"] < _STATS_TTL:
        return _STATS_CACHE["veri"]

    db = SessionLocal()
    try:
        kategoriler = db.query(Category).order_by(Category.sort_order).all()
        soru_sayisi = db.query(Question).filter(Question.status == "live").count()

        dersler = []
        for ders in DERS_SIRASI:
            kats = [c for c in kategoriler if c.subject == ders]
            if not kats:
                continue
            gmin = min(c.grade_min for c in kats)
            gmax = max(c.grade_max for c in kats)
            dersler.append({
                "kod": ders,
                "ad": DERS_ADLARI.get(ders, ders),
                "sinif": f"{gmin}–{gmax}" if gmin != gmax else str(gmin),
                "konular": [c.name for c in kats],
            })

        veri = {
            "kategori": len(kategoriler),
            "soru": soru_sayisi,
            "prosedurel": sum(1 for c in kategoriler if c.is_procedural),
            "dersler": dersler,
        }
        _STATS_CACHE.update({"veri": veri, "zaman": simdi})
        return veri
    finally:
        db.close()


@app.get("/")
def root():
    return {"name": "Minizeki API", "version": "1.0.0", "docs": "/docs"}


@app.exception_handler(Exception)
async def unhandled(request: Request, exc: Exception):
    log.exception("Beklenmeyen hata: %s %s", request.method, request.url.path)
    return JSONResponse(status_code=500,
                        content={"detail": "Bir şeyler ters gitti"})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=cfg.HOST, port=cfg.PORT, reload=True)
