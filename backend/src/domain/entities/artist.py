"""Artist 도메인 엔티티 — 이미지 슬라이더/포트폴리오/영상 포함"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class ArtistPortfolio:
    tag: str  # 주요활동 | 앨범 | 수상내역 | 경력사항
    year: int
    content: str
    id: Optional[str] = None


@dataclass
class ArtistVideo:
    video_url: str
    title: Optional[str] = None
    sort_order: int = 0
    id: Optional[str] = None


@dataclass
class Artist:
    id: Optional[str]  # CHAR(8)
    genre_id: int
    name: str
    members: Optional[str]  # 예) 솔로, 5인조
    description: str
    like_count: int = 0
    view_count: int = 0
    is_active: bool = True
    images: list[str] = field(default_factory=list)  # 정렬된 이미지 URL, 첫 번째가 대표
    portfolios: list[ArtistPortfolio] = field(default_factory=list)
    videos: list[ArtistVideo] = field(default_factory=list)
    genre_name: Optional[str] = None  # 조회 시 채워짐
    category_name: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self) -> None:
        if not self.name or not self.name.strip():
            raise ValueError("아티스트 이름은 필수입니다.")

    def deactivate(self) -> None:
        self.is_active = False
        self.updated_at = datetime.now()

    def activate(self) -> None:
        self.is_active = True
        self.updated_at = datetime.now()
