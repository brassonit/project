"""Artist Repository 인터페이스"""

from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from src.domain.entities.artist import Artist
from src.domain.value_objects.artist_category import ArtistCategory


class IArtistRepository(ABC):
    @abstractmethod
    async def save(self, artist: Artist) -> Artist: ...

    @abstractmethod
    async def find_by_id(self, artist_id: UUID) -> Optional[Artist]: ...

    @abstractmethod
    async def find_all(self, skip: int = 0, limit: int = 20) -> list[Artist]: ...

    @abstractmethod
    async def find_by_category(self, category: ArtistCategory, skip: int = 0, limit: int = 20) -> list[Artist]: ...

    @abstractmethod
    async def search(self, query: str, skip: int = 0, limit: int = 20) -> list[Artist]: ...

    @abstractmethod
    async def update(self, artist: Artist) -> Artist: ...

    @abstractmethod
    async def delete(self, artist_id: UUID) -> None: ...

    @abstractmethod
    async def count_all(self) -> int: ...

    @abstractmethod
    async def count_by_category(self, category: ArtistCategory) -> int: ...

    @abstractmethod
    async def count_search(self, query: str) -> int: ...

    @abstractmethod
    async def find_all_admin(self, skip: int = 0, limit: int = 20) -> list[Artist]: ...

    @abstractmethod
    async def count_all_admin(self) -> int: ...
