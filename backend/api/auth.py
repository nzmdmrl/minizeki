from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Session

from models import get_db, Account
from .security import (
    hash_password, verify_password, create_access_token, create_pin_token,
    get_current_account,
)

router = APIRouter(prefix="/api/auth", tags=["auth"])

PIN_MAX_FAIL = 5
PIN_LOCK_MINUTES = 15


class RegisterIn(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=100)


class LoginIn(BaseModel):
    email: EmailStr
    password: str


class PinIn(BaseModel):
    pin: str = Field(min_length=4, max_length=4)


class TokenOut(BaseModel):
    access_token: str
    plan: str
    email: str


@router.post("/register", response_model=TokenOut)
def register(body: RegisterIn, db: Session = Depends(get_db)):
    if db.query(Account).filter(Account.email == body.email.lower()).first():
        raise HTTPException(status.HTTP_409_CONFLICT, "Bu e-posta zaten kayıtlı")

    acc = Account(
        email=body.email.lower(),
        password_hash=hash_password(body.password),
        pin_hash=hash_password("0000"),
        plan="free",
    )
    db.add(acc)
    db.commit()
    db.refresh(acc)
    return TokenOut(access_token=create_access_token(acc.id),
                    plan=acc.plan, email=acc.email)


@router.post("/login", response_model=TokenOut)
def login(body: LoginIn, db: Session = Depends(get_db)):
    acc = db.query(Account).filter(Account.email == body.email.lower()).first()
    if not acc or not verify_password(body.password, acc.password_hash):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "E-posta veya şifre hatalı")
    return TokenOut(access_token=create_access_token(acc.id),
                    plan=acc.plan, email=acc.email)


@router.post("/verify-pin")
def verify_pin(body: PinIn, acc: Account = Depends(get_current_account),
               db: Session = Depends(get_db)):
    """
    Ebeveyn paneli erisimi. 5 yanlis denemede 15 dk kilit.
    """
    now = datetime.utcnow()
    if acc.pin_locked_until and acc.pin_locked_until > now:
        kalan = int((acc.pin_locked_until - now).total_seconds() // 60) + 1
        raise HTTPException(status.HTTP_429_TOO_MANY_REQUESTS,
                            f"Çok fazla deneme. {kalan} dakika sonra tekrar deneyin.")

    if not verify_password(body.pin, acc.pin_hash):
        acc.pin_fail_count = (acc.pin_fail_count or 0) + 1
        if acc.pin_fail_count >= PIN_MAX_FAIL:
            acc.pin_locked_until = now + timedelta(minutes=PIN_LOCK_MINUTES)
            acc.pin_fail_count = 0
            db.commit()
            raise HTTPException(status.HTTP_429_TOO_MANY_REQUESTS,
                                f"Çok fazla deneme. {PIN_LOCK_MINUTES} dakika kilitlendi.")
        db.commit()
        kalan = PIN_MAX_FAIL - acc.pin_fail_count
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                            f"PIN hatalı. {kalan} deneme hakkınız kaldı.")

    acc.pin_fail_count = 0
    acc.pin_locked_until = None
    db.commit()
    return {"pin_token": create_pin_token(acc.id)}


@router.get("/me")
def me(acc: Account = Depends(get_current_account)):
    return {"id": acc.id, "email": acc.email, "plan": acc.plan}
