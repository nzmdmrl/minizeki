"""
Kimlik dogrulama + soru token'i.

KRITIK: Dogru cevap ASLA istemciye gonderilmez.
Soru token'i imzali JWT icinde tasinir.
"""
from datetime import datetime, timedelta

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
from sqlalchemy.orm import Session

import config as cfg
from models import get_db, Account, Profile

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=12)
bearer = HTTPBearer(auto_error=False)


def hash_password(p: str) -> str:
    return pwd.hash(p)


def verify_password(p: str, h: str) -> bool:
    try:
        return pwd.verify(p, h)
    except Exception:
        return False


# ---------------------------------------------------------------- ACCESS TOKEN

def create_access_token(account_id: str) -> str:
    payload = {
        "sub": account_id,
        "typ": "access",
        "exp": datetime.utcnow() + timedelta(days=cfg.ACCESS_TOKEN_EXPIRE_DAYS),
        "iat": datetime.utcnow(),
    }
    return jwt.encode(payload, cfg.SECRET_KEY, algorithm=cfg.ALGORITHM)


def get_current_account(
    cred: HTTPAuthorizationCredentials = Depends(bearer),
    db: Session = Depends(get_db),
) -> Account:
    if cred is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Giriş yapılmamış")
    try:
        payload = jwt.decode(cred.credentials, cfg.SECRET_KEY,
                             algorithms=[cfg.ALGORITHM])
        if payload.get("typ") != "access":
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Geçersiz token")
        acc = db.get(Account, payload["sub"])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Oturum süresi doldu")
    except jwt.PyJWTError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Geçersiz token")

    if acc is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Hesap bulunamadı")
    return acc


def get_profile_or_404(db: Session, account: Account, profile_id: str) -> Profile:
    p = db.get(Profile, profile_id)
    if p is None or p.account_id != account.id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Profil bulunamadı")
    return p


# ---------------------------------------------------------------- PIN

def create_pin_token(account_id: str) -> str:
    payload = {
        "sub": account_id,
        "typ": "pin",
        "exp": datetime.utcnow() + timedelta(hours=2),
    }
    return jwt.encode(payload, cfg.SECRET_KEY, algorithm=cfg.ALGORITHM)


def require_pin(
    cred: HTTPAuthorizationCredentials = Depends(bearer),
    db: Session = Depends(get_db),
) -> Account:
    """Ebeveyn paneli icin PIN dogrulanmis token gerekir."""
    if cred is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "PIN gerekli")
    try:
        payload = jwt.decode(cred.credentials, cfg.SECRET_KEY,
                             algorithms=[cfg.ALGORITHM])
    except jwt.PyJWTError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Geçersiz PIN oturumu")

    if payload.get("typ") != "pin":
        raise HTTPException(status.HTTP_403_FORBIDDEN,
                            "Bu işlem için PIN doğrulaması gerekli")
    acc = db.get(Account, payload["sub"])
    if acc is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Hesap bulunamadı")
    return acc


# ---------------------------------------------------------------- SORU TOKEN

def create_question_token(q: dict, profile_id: str, mode: str) -> str:
    """
    Dogru cevap sunucuda kalir. Istemci sadece imzali token gorur.
    """
    payload = {
        "typ": "q",
        "pid": profile_id,
        "cid": q["category_id"],
        "qid": q.get("question_id"),
        "ai": q["answer_index"],
        "opts": q["options"],
        "band": q["band"],
        "grade": q.get("grade", 1),
        "mode": mode,
        "exp": datetime.utcnow() + timedelta(minutes=cfg.QUESTION_TOKEN_EXPIRE_MIN),
    }
    return jwt.encode(payload, cfg.SECRET_KEY, algorithm=cfg.ALGORITHM)


def decode_question_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, cfg.SECRET_KEY, algorithms=[cfg.ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status.HTTP_400_BAD_REQUEST,
                            "Soru süresi doldu, yeni tur başlat")
    except jwt.PyJWTError:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Geçersiz soru")
    if payload.get("typ") != "q":
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Geçersiz soru")
    return payload


# ---------------------------------------------------------------- ADMIN

def create_admin_token(account_id: str) -> str:
    payload = {
        "sub": account_id,
        "typ": "admin",
        "exp": datetime.utcnow() + timedelta(hours=cfg.ADMIN_TOKEN_EXPIRE_HOURS),
    }
    return jwt.encode(payload, cfg.SECRET_KEY, algorithm=cfg.ALGORITHM)


def require_admin(
    cred: HTTPAuthorizationCredentials = Depends(bearer),
    db: Session = Depends(get_db),
) -> Account:
    """
    Admin paneli erisimi. IKI kosul birden:
      1. Token 'admin' tipinde (ADMIN_PASSWORD ile alinmis)
      2. Hesabin is_admin bayragi acik
    Birinin kaybi digerini yetkilendirmez.
    """
    if cred is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Admin girişi gerekli")
    try:
        payload = jwt.decode(cred.credentials, cfg.SECRET_KEY,
                             algorithms=[cfg.ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Admin oturumu doldu")
    except jwt.PyJWTError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Geçersiz oturum")

    if payload.get("typ") != "admin":
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Admin yetkisi gerekli")

    acc = db.get(Account, payload["sub"])
    if acc is None or not acc.is_admin:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Admin yetkisi gerekli")
    return acc


def audit(db: Session, admin: Account, action: str,
          target: str | None = None, detail: dict | None = None) -> None:
    """Admin islemini denetim kaydina yaz."""
    from models import AuditLog
    db.add(AuditLog(admin_id=admin.id, admin_email=admin.email,
                    action=action, target=target, detail=detail or {}))


def strip_answer(q: dict, profile_id: str, mode: str) -> dict:
    """Istemciye gonderilecek guvenli soru nesnesi."""
    return {
        "token": create_question_token(q, profile_id, mode),
        "text": q["text"],
        "options": q["options"],
        "svg": q.get("svg"),
        "emoji": q.get("emoji"),
        "image_url": q.get("image_url"),
        "category_id": q["category_id"],
        "category_name": q.get("category_name"),
        "category_icon": q.get("category_icon"),
    }
