import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# --- Port ---
PORT = int(os.getenv("PORT", 8420))
HOST = os.getenv("HOST", "0.0.0.0")

# --- Database ---
# Varsayilan: SQLite (kurulum gerektirmez). Postgres icin DATABASE_URL ver.
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"sqlite:///{BASE_DIR / 'minizeki.db'}",
)

# --- Auth ---
SECRET_KEY = os.getenv("SECRET_KEY", "minizeki-dev-secret-degistir-mutlaka")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 30
QUESTION_TOKEN_EXPIRE_MIN = 15

# --- CORS ---
FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://localhost:3420")
CORS_ORIGINS = [
    FRONTEND_ORIGIN,
    "http://localhost:3420",
    "http://127.0.0.1:3420",
]

# --- Oyun ayarlari ---
QUEST_CATEGORY_COUNT = {1: 8, 2: 8, 3: 9, 4: 10}
QUEST_PER_CATEGORY = 2
FOCUS_QUESTION_COUNT = 6
SEEN_QUESTION_COOLDOWN_DAYS = 45

# Seviye guncelleme
LEVEL_UP_STREAK = 3
LEVEL_DOWN_STREAK = 2

# --- Terfi ---
# NOT: Bir kategoriden gunde ~2 soru gelir (rotasyon nedeniyle bazen 0).
# Pencereyi 30'da tutmak terfi kapisini pratikte kapatir (simulasyon bulgusu).
# 20 soru ~ 2 haftalik veri: sans elemesi icin yeterli, terfi icin ulasilabilir.
ADVANCE_MIN_ANSWERS = 40      # kategoride toplam cozulen
ADVANCE_WINDOW = 20           # son N soruya bakilir
ADVANCE_THRESHOLD = 0.85
ADVANCE_RATIO = 0.30

# Geri dusus: bir gunluk gorevde tek kategoriden 2 soru gelir.
# 12'lik pencere ~ 6 gun -> sistem gec tepki verir. 8 = ~4 gun.
DEMOTE_WINDOW = 8
DEMOTE_THRESHOLD = 0.60
DEMOTE_RATIO = 0.10

# Yildiz
STAR_QUEST_COMPLETE = 5
STAR_HIGH_ACCURACY = 3
STAR_MEDAL_UP = 10
STAR_STREAK_7 = 15
STAR_STREAK_30 = 50

# Kalkan
SHIELD_PER_MONTH = 2

# Ders agirligi
WEIGHT_VALUES = {"az": 0.5, "normal": 1.0, "cok": 1.5}
MIN_SUBJECT_SHARE = 0.10
MAX_SUBJECT_SHARE = 0.45

# Plan limitleri
FREE_CATEGORY_LIMIT = 6
FREE_FREEPLAY_PER_DAY = 1
FREE_PROFILE_LIMIT = 1
FAMILY_PROFILE_LIMIT = 4

# --- Admin ---
# Admin paneli erisimi icin ayri sifre. Hesabin is_admin=True olmasi YETMEZ;
# bu sifre de girilmeli (iki katmanli koruma).
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "")
ADMIN_TOKEN_EXPIRE_HOURS = 4

# Gercek zorluk kalibrasyonu: bir sorunun bandi ancak bu kadar servis
# edildikten sonra guvenilir sekilde olculur.
CALIBRATION_MIN_SERVES = 30

# Band -> hedef dogruluk (kalibrasyon sapmasi bu tabloya gore olculur)
BAND_TARGET_ACCURACY = {1: 0.90, 2: 0.75, 3: 0.60, 4: 0.40, 5: 0.20}
# Bu esikten fazla sapan soru "band yanlis" olarak isaretlenir
CALIBRATION_TOLERANCE = 0.20
