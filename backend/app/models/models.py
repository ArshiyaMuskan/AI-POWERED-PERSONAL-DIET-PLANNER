from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base


def utc_now():
    return datetime.now(timezone.utc)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    name = Column(String(120), nullable=False)
    age = Column(Integer, nullable=True)
    height = Column(Float, nullable=True)
    weight = Column(Float, nullable=True)
    activity_level = Column(String(50), nullable=True)
    dietary_preference = Column(String(50), nullable=True)
    goal = Column(String(80), nullable=True)
    allergies = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), default=utc_now)

    plans = relationship("DietPlan", back_populates="user", cascade="all, delete-orphan")
    files = relationship("UserFile", back_populates="user", cascade="all, delete-orphan")


class DietPlan(Base):
    __tablename__ = "diet_plans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    breakfast = Column(Text, nullable=False)
    lunch = Column(Text, nullable=False)
    snack = Column(Text, nullable=False)
    dinner = Column(Text, nullable=False)
    nutrition_summary = Column(Text, nullable=False)
    hydration_reminder = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), default=utc_now)

    user = relationship("User", back_populates="plans")


class UserFile(Base):
    __tablename__ = "user_files"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    filename = Column(String(255), nullable=False)
    storage_path = Column(String(500), nullable=False)
    content_type = Column(String(120), nullable=True)
    size_bytes = Column(Integer, nullable=False)
    uploaded_at = Column(DateTime(timezone=True), default=utc_now)

    user = relationship("User", back_populates="files")
