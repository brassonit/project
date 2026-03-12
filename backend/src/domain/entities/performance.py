"""Performance 도메인 엔티티"""

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional
from uuid import UUID


@dataclass
class Performance:
    id: Optional[UUID]
    title: str
    description: str
    event_date: date
    venue: str
    image_url: Optional[str]
    artist_id: Optional[UUID]
    is_featured: bool = False
    created_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self) -> None:
        if not self.title or not self.title.strip():
            raise ValueError("공연 제목은 필수입니다.")
        if not self.venue or not self.venue.strip():
            raise ValueError("공연 장소는 필수입니다.")

    def set_featured(self, featured: bool) -> None:
        self.is_featured = featured
