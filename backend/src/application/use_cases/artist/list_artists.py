"""아티스트 목록 조회 Use Case"""

from typing import Optional

from src.domain.entities.artist import Artist
from src.domain.repositories.artist_repository import IArtistRepository
from src.domain.value_objects.artist_category import ArtistCategory


class ListArtists:
    def __init__(self, artist_repo: IArtistRepository) -> None:
        self.artist_repo = artist_repo

    async def execute(
        self,
        category: Optional[str] = None,
        search: Optional[str] = None,
        skip: int = 0,
        limit: int = 20,
    ) -> dict[str, object]:
        # 카테고리 유효성 검증
        if category:
            try:
                artist_category = ArtistCategory(category)
            except ValueError:
                valid = ", ".join(c.value for c in ArtistCategory)
                raise ValueError(f"유효하지 않은 카테고리입니다. 가능한 값: {valid}")

        if search:
            artists: list[Artist] = await self.artist_repo.search(query=search, skip=skip, limit=limit)
            total: int = await self.artist_repo.count_search(query=search)
        elif category:
            artists = await self.artist_repo.find_by_category(category=artist_category, skip=skip, limit=limit)
            total = await self.artist_repo.count_by_category(category=artist_category)
        else:
            artists = await self.artist_repo.find_all(skip=skip, limit=limit)
            total = await self.artist_repo.count_all()

        return {"artists": artists, "total": total}
