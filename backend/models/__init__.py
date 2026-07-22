import uuid
from datetime import datetime, date

from sqlalchemy import (
    Column, String, Integer, Float, Boolean, DateTime, Date,
    ForeignKey, JSON, Text, BigInteger, UniqueConstraint, Index,
    create_engine,
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

from config import DATABASE_URL

Base = declarative_base()


def uid():
    return str(uuid.uuid4())


# ============ HESAP & PROFIL ============

class Account(Base):
    __tablename__ = "account"

    id = Column(String(36), primary_key=True, default=uid)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255))
    pin_hash = Column(String(255), nullable=False)
    plan = Column(String(20), default="free")           # free | family
    plan_expires = Column(DateTime)
    is_admin = Column(Boolean, default=False)
    pin_fail_count = Column(Integer, default=0)
    pin_locked_until = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

    profiles = relationship("Profile", back_populates="account",
                            cascade="all, delete-orphan")


class Profile(Base):
    __tablename__ = "profile"

    id = Column(String(36), primary_key=True, default=uid)
    account_id = Column(String(36), ForeignKey("account.id", ondelete="CASCADE"),
                        nullable=False, index=True)
    name = Column(String(50), nullable=False)
    avatar_id = Column(String(20), nullable=False, default="fox")
    grade = Column(Integer, nullable=False, default=2)

    # Ayarlar
    repeat_ratio = Column(Float, default=0.20)
    allow_advance = Column(Boolean, default=True)
    subject_weights = Column(JSON, default=lambda: {
        "matematik": 1.0, "turkce": 1.0, "hayat_bilgisi": 1.0,
    })
    daily_limit_min = Column(Integer, default=30)

    # Odak modu
    focus_category_id = Column(String(50))
    focus_until = Column(Date)

    # Ilerleme
    star_balance = Column(Integer, default=0)
    streak_days = Column(Integer, default=0)
    shield_count = Column(Integer, default=2)
    shield_month = Column(String(7))                    # '2026-07'
    last_quest_date = Column(Date)

    calibrated = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    account = relationship("Account", back_populates="profiles")


# ============ ICERIK ============

class Category(Base):
    __tablename__ = "category"

    id = Column(String(50), primary_key=True)
    name = Column(String(100), nullable=False)
    subject = Column(String(30), nullable=False, index=True)
    icon = Column(String(20), nullable=False)
    grade_min = Column(Integer, nullable=False)
    grade_max = Column(Integer, nullable=False)
    is_procedural = Column(Boolean, default=False)
    generator_key = Column(String(50))
    has_upper_grade = Column(Boolean, default=True)
    is_free = Column(Boolean, default=False)            # ucretsiz planda acik mi
    sort_order = Column(Integer, default=0)


class Question(Base):
    __tablename__ = "question"

    id = Column(String(36), primary_key=True, default=uid)
    category_id = Column(String(50), ForeignKey("category.id"), nullable=False)
    grade_min = Column(Integer, nullable=False)
    grade_max = Column(Integer, nullable=False)
    band = Column(Integer, nullable=False)

    text = Column(Text, nullable=False)
    image_url = Column(String(255))
    options = Column(JSON, nullable=False)
    answer_index = Column(Integer, nullable=False)
    explanation = Column(Text)

    serve_count = Column(Integer, default=0)
    correct_count = Column(Integer, default=0)
    real_difficulty = Column(Float)

    source = Column(String(20), default="human")
    status = Column(String(20), default="live")
    created_at = Column(DateTime, default=datetime.utcnow)


Index("idx_question_serve", Question.category_id, Question.band, Question.status)


# ============ ILERLEME ============

class ProfileSkill(Base):
    __tablename__ = "profile_skill"

    profile_id = Column(String(36), ForeignKey("profile.id", ondelete="CASCADE"),
                        primary_key=True)
    category_id = Column(String(50), ForeignKey("category.id"), primary_key=True)

    level = Column(Integer, default=2)                  # gizli zorluk 1-5
    correct_streak = Column(Integer, default=0)
    wrong_streak = Column(Integer, default=0)

    total_correct = Column(Integer, default=0)
    total_wrong = Column(Integer, default=0)
    medal_level = Column(Integer, default=0)            # gorunur 0-5

    advanced_unlocked = Column(Boolean, default=False)
    advance_ratio = Column(Float, default=0.10)

    last_seen_at = Column(DateTime)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# ============ OYUN ============

class DailyQuest(Base):
    __tablename__ = "daily_quest"

    id = Column(String(36), primary_key=True, default=uid)
    profile_id = Column(String(36), ForeignKey("profile.id", ondelete="CASCADE"),
                        nullable=False, index=True)
    quest_date = Column(Date, nullable=False)
    questions = Column(JSON, nullable=False)
    progress = Column(Integer, default=0)
    correct_count = Column(Integer, default=0)
    completed_at = Column(DateTime)

    __table_args__ = (UniqueConstraint("profile_id", "quest_date",
                                       name="uq_quest_profile_date"),)


class AnswerLog(Base):
    __tablename__ = "answer_log"

    id = Column(BigInteger().with_variant(Integer, "sqlite"),
                primary_key=True, autoincrement=True)
    profile_id = Column(String(36), ForeignKey("profile.id", ondelete="CASCADE"),
                        nullable=False, index=True)
    category_id = Column(String(50), ForeignKey("category.id"), nullable=False)
    question_id = Column(String(36))                    # prosedurel -> None
    band = Column(Integer, nullable=False)
    grade = Column(Integer, nullable=False)
    is_correct = Column(Boolean, nullable=False)
    duration_ms = Column(Integer)
    mode = Column(String(10), default="quest")          # quest | free
    answered_at = Column(DateTime, default=datetime.utcnow, index=True)


Index("idx_answer_profile_cat", AnswerLog.profile_id,
      AnswerLog.category_id, AnswerLog.answered_at)


class SeenQuestion(Base):
    __tablename__ = "seen_question"

    profile_id = Column(String(36), ForeignKey("profile.id", ondelete="CASCADE"),
                        primary_key=True)
    question_id = Column(String(36), ForeignKey("question.id"), primary_key=True)
    last_seen_at = Column(DateTime, default=datetime.utcnow)


# ============ ODUL ============

class StarEvent(Base):
    __tablename__ = "star_event"

    id = Column(BigInteger().with_variant(Integer, "sqlite"),
                primary_key=True, autoincrement=True)
    profile_id = Column(String(36), ForeignKey("profile.id", ondelete="CASCADE"),
                        nullable=False, index=True)
    delta = Column(Integer, nullable=False)
    reason = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class HouseItem(Base):
    __tablename__ = "house_item"

    id = Column(String(50), primary_key=True)
    name = Column(String(100), nullable=False)
    category = Column(String(20))
    price = Column(Integer, nullable=False)
    icon = Column(String(20))
    sort_order = Column(Integer, default=0)


class OwnedItem(Base):
    __tablename__ = "owned_item"

    profile_id = Column(String(36), ForeignKey("profile.id", ondelete="CASCADE"),
                        primary_key=True)
    item_id = Column(String(50), ForeignKey("house_item.id"), primary_key=True)
    bought_at = Column(DateTime, default=datetime.utcnow)


class Badge(Base):
    __tablename__ = "badge"

    id = Column(String(50), primary_key=True)
    name = Column(String(100), nullable=False)
    icon = Column(String(20))
    description = Column(String(255))


class ProfileBadge(Base):
    __tablename__ = "profile_badge"

    profile_id = Column(String(36), ForeignKey("profile.id", ondelete="CASCADE"),
                        primary_key=True)
    badge_id = Column(String(50), ForeignKey("badge.id"), primary_key=True)
    earned_at = Column(DateTime, default=datetime.utcnow)


# ============ ADMIN ============

class AuditLog(Base):
    """
    Admin islemlerinin denetim kaydi.
    Cocuk verisine erisen her islem burada iz birakir.
    """
    __tablename__ = "audit_log"

    id = Column(BigInteger().with_variant(Integer, "sqlite"),
                primary_key=True, autoincrement=True)
    admin_id = Column(String(36), nullable=False, index=True)
    admin_email = Column(String(255))
    action = Column(String(50), nullable=False)      # question.update, account.plan...
    target = Column(String(100))                     # etkilenen kaydin id'si
    detail = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)


# ============ ENGINE ============

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    Base.metadata.create_all(bind=engine)
