"""아티스트 수정 Use Case"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from src.domain.entities.artist import Artist
from src.domain.repositories.artist_repository import IArtistRepository
from src.domain.value_objects.artist_category import ArtistCategory


class UpdateArtist:
    def __init__(self, artist_repo: IArtistRepository) -> None:
        self.artist_repo = artist_repo

    async def execute(
        self,
        artist_id: UUID,
        name: Optional[str] = None,
        category: Optional[str] = None,
        description: Optional[str] = None,
        profile_image_url: Optional[str] = None,
        gallery_images: Optional[list[str]] = None,
        is_active: Optional[bool] = None,
    ) -> Artist:
        artist = await self.artist_repo.find_by_id(artist_id)
        if not artist:
            raise ValueError("아티스트를 찾을 수 없습니다.")

        if name is not None:
            artist.name = name
        if category is not None:
            try:
                artist.category = ArtistCategory(category)
            except ValueError:
                valid = ", ".join(c.value for c in ArtistCategory)
                raise ValueError(f"유효하지 않은 카테고리입니다. 가능한 값: {valid}")
        if description is not None:
            artist.description = description
        if profile_image_url is not None:
            artist.profile_image_url = profile_image_url
        if gallery_images is not None:
            artist.gallery_images = gallery_images
        if is_active is not None:
            artist.is_active = is_active

        artist.updated_at = datetime.now()
        return await self.artist_repo.update(artist)
