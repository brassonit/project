"""아티스트 생성 Use Case"""

from datetime import datetime
from typing import Optional

from src.domain.entities.artist import Artist
from src.domain.repositories.artist_repository import IArtistRepository
from src.domain.value_objects.artist_category import ArtistCategory


class CreateArtist:
    def __init__(self, artist_repo: IArtistRepository) -> None:
        self.artist_repo = artist_repo

    async def execute(
        self,
        name: str,
        category: str,
        description: str,
        profile_image_url: Optional[str] = None,
        gallery_images: Optional[list[str]] = None,
    ) -> Artist:
        # 카테고리 유효성 검증
        try:
            artist_category = ArtistCategory(category)
        except ValueError:
            valid = ", ".join(c.value for c in ArtistCategory)
            raise ValueError(f"유효하지 않은 카테고리입니다. 가능한 값: {valid}")

        artist = Artist(
            id=None,
            name=name,
            category=artist_category,
            description=description,
            profile_image_url=profile_image_url,
            gallery_images=gallery_images or [],
            is_active=True,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        return await self.artist_repo.save(artist)
