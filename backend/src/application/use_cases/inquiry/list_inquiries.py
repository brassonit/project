"""문의 목록 조회 Use Case"""

from typing import Optional

from src.domain.entities.inquiry import Inquiry, InquiryStatus
from src.domain.repositories.inquiry_repository import IInquiryRepository


class ListInquiries:
    def __init__(self, inquiry_repo: IInquiryRepository) -> None:
        self.inquiry_repo = inquiry_repo

    async def execute(
        self,
        status: Optional[str] = None,
        skip: int = 0,
        limit: int = 20,
    ) -> dict[str, object]:
        if status:
            try:
                inquiry_status = InquiryStatus(status)
            except ValueError:
                valid = ", ".join(s.value for s in InquiryStatus)
                raise ValueError(f"유효하지 않은 상태입니다. 가능한 값: {valid}")
            inquiries: list[Inquiry] = await self.inquiry_repo.find_by_status(
                status=inquiry_status, skip=skip, limit=limit
            )
            total: int = await self.inquiry_repo.count_by_status(status=inquiry_status)
        else:
            inquiries = await self.inquiry_repo.find_all(skip=skip, limit=limit)
            total = await self.inquiry_repo.count_all()

        return {"inquiries": inquiries, "total": total}
