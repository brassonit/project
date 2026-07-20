"""Quote Repository 인터페이스"""

from abc import ABC, abstractmethod
from typing import Optional

from src.domain.entities.quote import Quote, QuoteStatus


class IQuoteRepository(ABC):
    @abstractmethod
    async def save(self, quote: Quote) -> Quote: ...

    @abstractmethod
    async def find_by_id(self, quote_id: str) -> Optional[Quote]: ...

    @abstractmethod
    async def find_by_user(self, user_id: str, skip: int = 0, limit: int = 20) -> tuple[list[Quote], int]:
        """사용자 견적내역 (최신순) + 전체 건수"""
        ...

    @abstractmethod
    async def find_all(
        self, status: Optional[QuoteStatus] = None, skip: int = 0, limit: int = 20
    ) -> tuple[list[Quote], int]:
        """관리자용 전체 목록 + 전체 건수"""
        ...

    @abstractmethod
    async def update(self, quote: Quote) -> Quote: ...

    @abstractmethod
    async def delete(self, quote_id: str) -> None: ...

    @abstractmethod
    async def count_all(self) -> int: ...

    @abstractmethod
    async def count_by_status(self, status: QuoteStatus) -> int: ...
