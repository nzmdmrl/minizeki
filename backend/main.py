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
