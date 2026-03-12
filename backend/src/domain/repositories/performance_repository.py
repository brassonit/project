"""Performance Repository 인터페이스"""

from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from src.domain.entities.performance import Performance


class IPerformanceRepository(ABC):
    @abstractmethod
    async def save(self, performance: Performance) -> Performance: ...

    @abstractmethod
    async def find_by_id(self, performance_id: UUID) -> Optional[Performance]: ...

    @abstractmethod
    async def find_all(self, skip: int = 0, limit: int = 20) -> list[Performance]: ...

    @abstractmethod
    async def find_featured(self, skip: int = 0, limit: int = 20) -> list[Performance]: ...

    @abstractmethod
    async def update(self, performance: Performance) -> Performance: ...

    @abstractmethod
    async def delete(self, performance_id: UUID) -> None: ...

    @abstractmethod
    async def count_all(self) -> int: ...

    @abstractmethod
    async def count_featured(self) -> int: ...
