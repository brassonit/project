"""Category Repository 인터페이스"""

from abc import ABC, abstractmethod
from typing import Optional

from src.domain.entities.category import Category, Genre


class ICategoryRepository(ABC):
    @abstractmethod
    async def find_all(self) -> list[Category]:
        """카테고리 + 하위 장르 (sort_order 순)"""
        ...

    @abstractmethod
    async def find_genre_by_id(self, genre_id: int) -> Optional[Genre]: ...
