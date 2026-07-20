"""Show(기획공연) 도메인 엔티티 — 출연진/예매 링크 포함"""

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional


@dataclass
class ShowLineup:
    artist_id: str
    artist_name: Optional[str] = None  # 조회 시 채워짐
    sort_order: int = 0


@dataclass
class ShowTicket:
    label: str  # 예) 1회차 08.15 (토) — 인터파크 티켓
    url: str
    sort_order: int = 0
    id: Optional[str] = None


@dataclass
class ShowVideo:
    video_url: str
    title: Optional[str] = None
    sort_order: int = 0
    id: Optional[str] = None


@dataclass
class Show:
    id: Optional[str]  # CHAR(8)
    title: str
    event_date: date
    venue: str
    description: str = ""
    intro: str = ""  # 하단 "공연 소개" 본문 (문단은 빈 줄 구분)
    category_id: Optional[int] = None
    image_url: Optional[str] = None
    like_count: int = 0
    view_count: int = 0
    lineup: list[ShowLineup] = field(default_factory=list)
    tickets: list[ShowTicket] = field(default_factory=list)
    videos: list[ShowVideo] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self) -> None:
        if not self.title or not self.title.strip():
            raise ValueError("공연 제목은 필수입니다.")
        if not self.venue or not self.venue.strip():
            raise ValueError("공연 장소는 필수입니다.")

    def is_upcoming(self, today: Optional[date] = None) -> bool:
        return self.event_date >= (today or date.today())
