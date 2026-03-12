"""SQLAlchemy ORM 모델"""

import uuid
from datetime import datetime

from sqlalchemy import JSON, Boolean, Column, Date, DateTime, ForeignKey, String, Text
from sqlalchemy.types import CHAR, TypeDecorator

from src.infrastructure.database.connection import Base


class UUIDType(TypeDecorator):
    """DB 엔진에 관계없이 UUID를 저장하는 커스텀 타입 (PostgreSQL: native UUID, SQLite: CHAR(36))"""

    impl = CHAR(36)
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is not None:
            return str(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            return uuid.UUID(value)
        return value


class UserModel(Base):
    __tablename__ = "users"

    id = Column(UUIDType, primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False, default="customer")
    is_verified = Column(Boolean, nullable=False, default=False)
    verification_token = Column(String(255), nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now)


class ArtistModel(Base):
    __tablename__ = "artists"

    id = Column(UUIDType, primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    category = Column(String(50), nullable=False)
    description = Column(Text, nullable=False)
    profile_image_url = Column(String(500), nullable=True)
    gallery_images = Column(JSON, nullable=False, default=list)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)


class PerformanceModel(Base):
    __tablename__ = "performances"

    id = Column(UUIDType, primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    event_date = Column(Date, nullable=False)
    venue = Column(String(255), nullable=False)
    image_url = Column(String(500), nullable=True)
    artist_id = Column(UUIDType, ForeignKey("artists.id", ondelete="SET NULL"), nullable=True)
    is_featured = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)


class InquiryModel(Base):
    __tablename__ = "inquiries"

    id = Column(UUIDType, primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=True)
    subject = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    status = Column(String(20), nullable=False, default="pending")
    admin_reply = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
