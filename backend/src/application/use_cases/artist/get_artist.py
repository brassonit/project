"""아티스트 상세 조회 Use Case"""

from uuid import UUID

from src.domain.entities.artist import Artist
from src.domain.repositories.artist_repository import IArtistRepository


class GetArtist:
    def __init__(self, artist_repo: IArtistRepository) -> None:
        self.artist_repo = artist_repo

    async def execute(self, artist_id: UUID) -> Artist:
        artist = await self.artist_repo.find_by_id(artist_id)
        if not artist:
            raise ValueError("아티스트를 찾을 수 없습니다.")
        return artist
