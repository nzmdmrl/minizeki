import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

import config as cfg
from models import init_db
from api import auth, profile, play, parent, house, admin

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


@app.on_event("startup")
def startup():
    init_db()
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
            seed_categories, seed_badges, seed_house, seed_questions, dogrula,
        )
        db = SessionLocal()
        try:
            once = db.query(Question).count()
            k = seed_categories(db)
            b = seed_badges(db)
            h = seed_house(db)
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
