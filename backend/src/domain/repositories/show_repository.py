"""Show Repository 인터페이스"""

from abc import ABC, abstractmethod
from typing import Optional

from src.domain.entities.show import Show


class IShowRepository(ABC):
    @abstractmethod
    async def save(self, show: Show) -> Show: ...

    @abstractmethod
    async def find_by_id(self, show_id: str) -> Optional[Show]: ...

    @abstractmethod
    async def find_all(self, skip: int = 0, limit: int = 100) -> tuple[list[Show], int]:
        """공연 목록 (event_date 내림차순) + 전체 건수"""
        ...

    @abstractmethod
    async def update(self, show: Show) -> Show: ...

    @abstractmethod
    async def delete(self, show_id: str) -> None: ...

    @abstractmethod
    async def increment_view(self, show_id: str) -> None: ...

    @abstractmethod
    async def count_all(self) -> int: ...

    @abstractmethod
    async def count_upcoming(self) -> int: ...
