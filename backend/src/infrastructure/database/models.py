"""SQLAlchemy ORM 모델 — scripts/create_tables.sql (com 스키마) 기준"""

import uuid
from datetime import datetime

from sqlalchemy import (
    CHAR,
    BigInteger,
    Boolean,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    SmallInteger,
    String,
    Text,
    UniqueConstraint,
)

from src.infrastructure.database.connection import Base


def gen_id() -> str:
    """UUID 앞 8자리(hex) — DB의 com.gen_id()와 동일 규칙"""
    return uuid.uuid4().hex[:8]


class UserModel(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "com"}

    id = Column(CHAR(8), primary_key=True, default=gen_id)
    email = Column(String(255), nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    name = Column(String(100), nullable=True)
    phone = Column(String(20), nullable=True)
    role = Column(String(20), nullable=False, default="customer")  # customer | admin
    is_verified = Column(Boolean, nullable=False, default=False)
    verification_token = Column(String(255), nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    deleted_at = Column(DateTime, nullable=True)  # 회원탈퇴 (soft delete)


class CategoryModel(Base):
    __tablename__ = "categories"
    __table_args__ = {"schema": "com"}

    id = Column(SmallInteger, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    sort_order = Column(SmallInteger, nullable=False, default=0)


class GenreModel(Base):
    __tablename__ = "genres"
    __table_args__ = (
        UniqueConstraint("category_id", "name"),
        {"schema": "com"},
    )

    id = Column(SmallInteger, primary_key=True, autoincrement=True)
    category_id = Column(SmallInteger, ForeignKey("com.categories.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(50), nullable=False)
    sort_order = Column(SmallInteger, nullable=False, default=0)


class ArtistModel(Base):
    __tablename__ = "artists"
    __table_args__ = {"schema": "com"}

    id = Column(CHAR(8), primary_key=True, default=gen_id)
    genre_id = Column(SmallInteger, ForeignKey("com.genres.id"), nullable=False, index=True)
    name = Column(String(255), nullable=False, index=True)
    members = Column(String(50), nullable=True)  # 예) 솔로, 5인조
    description = Column(Text, nullable=False, default="")
    like_count = Column(Integer, nullable=False, default=0)
    view_count = Column(BigInteger, nullable=False, default=0)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)


class ArtistImageModel(Base):
    """상세 이미지 슬라이더 (첫 번째가 대표/카드 썸네일)"""

    __tablename__ = "artist_images"
    __table_args__ = {"schema": "com"}

    id = Column(CHAR(8), primary_key=True, default=gen_id)
    artist_id = Column(CHAR(8), ForeignKey("com.artists.id", ondelete="CASCADE"), nullable=False, index=True)
    image_url = Column(String(500), nullable=False)
    sort_order = Column(SmallInteger, nullable=False, default=0)


class ArtistPortfolioModel(Base):
    """포트폴리오 — tag: 주요활동 | 앨범 | 수상내역 | 경력사항"""

    __tablename__ = "artist_portfolios"
    __table_args__ = {"schema": "com"}

    id = Column(CHAR(8), primary_key=True, default=gen_id)
    artist_id = Column(CHAR(8), ForeignKey("com.artists.id", ondelete="CASCADE"), nullable=False, index=True)
    tag = Column(String(30), nullable=False)
    year = Column(SmallInteger, nullable=False)
    content = Column(Text, nullable=False)


class ArtistVideoModel(Base):
    __tablename__ = "artist_videos"
    __table_args__ = {"schema": "com"}

    id = Column(CHAR(8), primary_key=True, default=gen_id)
    artist_id = Column(CHAR(8), ForeignKey("com.artists.id", ondelete="CASCADE"), nullable=False, index=True)
    video_url = Column(String(500), nullable=False)
    title = Column(String(255), nullable=True)
    sort_order = Column(SmallInteger, nullable=False, default=0)


class ShowModel(Base):
    """기획공연 — 예정/지난 구분은 event_date로 파생"""

    __tablename__ = "shows"
    __table_args__ = {"schema": "com"}

    id = Column(CHAR(8), primary_key=True, default=gen_id)
    category_id = Column(SmallInteger, ForeignKey("com.categories.id"), nullable=True)
    title = Column(String(255), nullable=False)
    event_date = Column(Date, nullable=False, index=True)
    venue = Column(String(255), nullable=False)
    description = Column(Text, nullable=False, default="")
    intro = Column(Text, nullable=False, default="")  # 하단 "공연 소개" 본문 (문단은 빈 줄 구분)
    image_url = Column(String(500), nullable=True)
    like_count = Column(Integer, nullable=False, default=0)
    view_count = Column(BigInteger, nullable=False, default=0)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)


class ShowLineupModel(Base):
    """공연 출연진 (M:N)"""

    __tablename__ = "show_lineups"
    __table_args__ = {"schema": "com"}

    show_id = Column(CHAR(8), ForeignKey("com.shows.id", ondelete="CASCADE"), primary_key=True)
    artist_id = Column(CHAR(8), ForeignKey("com.artists.id", ondelete="CASCADE"), primary_key=True, index=True)
    sort_order = Column(SmallInteger, nullable=False, default=0)


class ShowTicketModel(Base):
    """예매 링크 (회차별 복수, 예정 공연만)"""

    __tablename__ = "show_tickets"
    __table_args__ = {"schema": "com"}

    id = Column(CHAR(8), primary_key=True, default=gen_id)
    show_id = Column(CHAR(8), ForeignKey("com.shows.id", ondelete="CASCADE"), nullable=False, index=True)
    label = Column(String(255), nullable=False)
    url = Column(String(500), nullable=False)
    sort_order = Column(SmallInteger, nullable=False, default=0)


class ShowVideoModel(Base):
    """공연 영상 섹션 (유튜브 embed)"""

    __tablename__ = "show_videos"
    __table_args__ = {"schema": "com"}

    id = Column(CHAR(8), primary_key=True, default=gen_id)
    show_id = Column(CHAR(8), ForeignKey("com.shows.id", ondelete="CASCADE"), nullable=False, index=True)
    video_url = Column(String(500), nullable=False)
    title = Column(String(255), nullable=True)
    sort_order = Column(SmallInteger, nullable=False, default=0)


class WishlistModel(Base):
    __tablename__ = "wishlists"
    __table_args__ = {"schema": "com"}

    user_id = Column(CHAR(8), ForeignKey("com.users.id", ondelete="CASCADE"), primary_key=True)
    artist_id = Column(CHAR(8), ForeignKey("com.artists.id", ondelete="CASCADE"), primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now)


class ShowWishlistModel(Base):
    """공연 찜 — 공연 상세 ♥ 토글, 찜리스트 공연 테이블"""

    __tablename__ = "show_wishlists"
    __table_args__ = {"schema": "com"}

    user_id = Column(CHAR(8), ForeignKey("com.users.id", ondelete="CASCADE"), primary_key=True)
    show_id = Column(CHAR(8), ForeignKey("com.shows.id", ondelete="CASCADE"), primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now)


class CartModel(Base):
    __tablename__ = "carts"
    __table_args__ = {"schema": "com"}

    user_id = Column(CHAR(8), ForeignKey("com.users.id", ondelete="CASCADE"), primary_key=True)
    artist_id = Column(CHAR(8), ForeignKey("com.artists.id", ondelete="CASCADE"), primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now)


class QuoteModel(Base):
    """견적 — user_id NULL = 비로그인 문의. status: received(접수완료) | replied(회신완료)"""

    __tablename__ = "quotes"
    __table_args__ = {"schema": "com"}

    id = Column(CHAR(8), primary_key=True, default=gen_id)
    user_id = Column(CHAR(8), ForeignKey("com.users.id", ondelete="SET NULL"), nullable=True, index=True)
    email = Column(String(255), nullable=False)  # 회신 받을 이메일 (스냅샷)
    name = Column(String(100), nullable=False)  # 담당자 이름
    phone = Column(String(20), nullable=False)
    event_title = Column(String(255), nullable=False)  # 행사명
    event_date = Column(Date, nullable=True)  # 달력 선택 시
    event_date_text = Column(String(100), nullable=True)  # 직접 입력 시 (둘 중 하나만)
    region = Column(String(50), nullable=True)  # 행사지역 (시/도)
    content = Column(Text, nullable=False, default="")
    show_id = Column(CHAR(8), ForeignKey("com.shows.id", ondelete="SET NULL"), nullable=True)  # 첨부된 공연
    status = Column(String(20), nullable=False, default="received", index=True)
    quote_file_url = Column(String(500), nullable=True)  # 회신완료 시 견적서 파일
    replied_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now)


class QuoteArtistModel(Base):
    """견적에 포함된 아티스트 (선택한 아티스트 n팀)"""

    __tablename__ = "quote_artists"
    __table_args__ = {"schema": "com"}

    quote_id = Column(CHAR(8), ForeignKey("com.quotes.id", ondelete="CASCADE"), primary_key=True)
    artist_id = Column(CHAR(8), ForeignKey("com.artists.id", ondelete="CASCADE"), primary_key=True)


class QuoteAttachmentModel(Base):
    __tablename__ = "quote_attachments"
    __table_args__ = {"schema": "com"}

    id = Column(CHAR(8), primary_key=True, default=gen_id)
    quote_id = Column(CHAR(8), ForeignKey("com.quotes.id", ondelete="CASCADE"), nullable=False, index=True)
    file_name = Column(String(255), nullable=False)
    file_url = Column(String(500), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)


class PolicyModel(Base):
    """이용약관/개인정보취급방침 버전 — policy_type: terms | privacy"""

    __tablename__ = "policies"
    __table_args__ = (
        UniqueConstraint("policy_type", "effective_date"),
        {"schema": "com"},
    )

    id = Column(CHAR(8), primary_key=True, default=gen_id)
    policy_type = Column(String(20), nullable=False)
    effective_date = Column(Date, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
