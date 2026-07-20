"""Artist Repository 인터페이스"""

from abc import ABC, abstractmethod
from typing import Optional

from src.domain.entities.artist import Artist


class IArtistRepository(ABC):
    @abstractmethod
    async def save(self, artist: Artist) -> Artist: ...

    @abstractmethod
    async def find_by_id(self, artist_id: str) -> Optional[Artist]: ...

    @abstractmethod
    async def find_all(
        self,
        category: Optional[str] = None,  # 카테고리명 (예: 대중가수)
        genre: Optional[str] = None,  # 장르명 (예: 아이돌)
        search: Optional[str] = None,
        skip: int = 0,
        limit: int = 20,
    ) -> tuple[list[Artist], int]:
        """활성 아티스트 목록 + 전체 건수"""
        ...

    @abstractmethod
    async def update(self, artist: Artist) -> Artist: ...

    @abstractmethod
    async def delete(self, artist_id: str) -> None: ...

    @abstractmethod
    async def increment_view(self, artist_id: str) -> None: ...

    @abstractmethod
    async def find_all_admin(self, skip: int = 0, limit: int = 20) -> tuple[list[Artist], int]:
        """관리자용 (비활성 포함)"""
        ...

    @abstractmethod
    async def count_all(self) -> int: ...

    @abstractmethod
    async def count_all_admin(self) -> int: ...
