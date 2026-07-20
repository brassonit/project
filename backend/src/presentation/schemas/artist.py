"""아티스트 관련 Pydantic 스키마"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class PortfolioItem(BaseModel):
    tag: str  # 주요활동 | 앨범 | 수상내역 | 경력사항
    year: int
    content: str


class VideoItem(BaseModel):
    video_url: str
    title: Optional[str] = None


class ArtistCreate(BaseModel):
    genre_id: int
    name: str
    members: Optional[str] = None
    description: str = ""
    images: list[str] = []
    portfolios: list[PortfolioItem] = []
    videos: list[VideoItem] = []


class ArtistUpdate(BaseModel):
    genre_id: Optional[int] = None
    name: Optional[str] = None
    members: Optional[str] = None
    description: Optional[str] = None
    images: Optional[list[str]] = None
    portfolios: Optional[list[PortfolioItem]] = None
    videos: Optional[list[VideoItem]] = None
    is_active: Optional[bool] = None


class ArtistResponse(BaseModel):
    id: str
    genre_id: int
    genre_name: Optional[str]
    category_name: Optional[str]
    name: str
    members: Optional[str]
    description: str
    like_count: int
    view_count: int
    is_active: bool
    images: list[str]
    portfolios: list[PortfolioItem]
    videos: list[VideoItem]
    created_at: datetime
    updated_at: datetime


class ArtistListResponse(BaseModel):
    artists: list[ArtistResponse]
    total: int
    skip: int
    limit: int
