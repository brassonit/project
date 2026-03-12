"""Artist 도메인 엔티티"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import UUID

from src.domain.value_objects.artist_category import ArtistCategory


@dataclass
class Artist:
    id: Optional[UUID]
    name: str
    category: ArtistCategory
    description: str
    profile_image_url: Optional[str]
    gallery_images: list[str] = field(default_factory=list)
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self) -> None:
        if not self.name or not self.name.strip():
            raise ValueError("아티스트 이름은 필수입니다.")
        if not self.description or not self.description.strip():
            raise ValueError("아티스트 설명은 필수입니다.")

    def deactivate(self) -> None:
        self.is_active = False
        self.updated_at = datetime.now()

    def activate(self) -> None:
        self.is_active = True
        self.updated_at = datetime.now()
