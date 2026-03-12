"""Inquiry Repository 인터페이스"""

from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from src.domain.entities.inquiry import Inquiry, InquiryStatus


class IInquiryRepository(ABC):
    @abstractmethod
    async def save(self, inquiry: Inquiry) -> Inquiry: ...

    @abstractmethod
    async def find_by_id(self, inquiry_id: UUID) -> Optional[Inquiry]: ...

    @abstractmethod
    async def find_all(self, skip: int = 0, limit: int = 20) -> list[Inquiry]: ...

    @abstractmethod
    async def find_by_status(self, status: InquiryStatus, skip: int = 0, limit: int = 20) -> list[Inquiry]: ...

    @abstractmethod
    async def update(self, inquiry: Inquiry) -> Inquiry: ...

    @abstractmethod
    async def delete(self, inquiry_id: UUID) -> None: ...

    @abstractmethod
    async def count_all(self) -> int: ...

    @abstractmethod
    async def count_by_status(self, status: InquiryStatus) -> int: ...
