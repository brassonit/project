"""기획공연 관련 Pydantic 스키마"""

from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel


class TicketItem(BaseModel):
    label: str
    url: str


class LineupItem(BaseModel):
    artist_id: str
    artist_name: Optional[str] = None


class ShowVideoItem(BaseModel):
    video_url: str
    title: Optional[str] = None


class ShowCreate(BaseModel):
    title: str
    event_date: date
    venue: str
    description: str = ""
    intro: str = ""  # 하단 "공연 소개" 본문 (문단은 빈 줄 구분)
    category_id: Optional[int] = None
    image_url: Optional[str] = None
    lineup_artist_ids: list[str] = []
    tickets: list[TicketItem] = []
    videos: list[ShowVideoItem] = []


class ShowUpdate(BaseModel):
    title: Optional[str] = None
    event_date: Optional[date] = None
    venue: Optional[str] = None
    description: Optional[str] = None
    intro: Optional[str] = None
    category_id: Optional[int] = None
    image_url: Optional[str] = None
    lineup_artist_ids: Optional[list[str]] = None
    tickets: Optional[list[TicketItem]] = None
    videos: Optional[list[ShowVideoItem]] = None


class ShowResponse(BaseModel):
    id: str
    title: str
    event_date: date
    venue: str
    description: str
    intro: str
    category_id: Optional[int]
    image_url: Optional[str]
    like_count: int
    view_count: int
    is_upcoming: bool
    lineup: list[LineupItem]
    tickets: list[TicketItem]
    videos: list[ShowVideoItem]
    created_at: datetime


class ShowListResponse(BaseModel):
    shows: list[ShowResponse]
    total: int
