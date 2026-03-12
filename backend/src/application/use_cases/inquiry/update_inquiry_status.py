"""문의 상태 변경 Use Case"""

from uuid import UUID

from src.domain.entities.inquiry import Inquiry, InquiryStatus
from src.domain.repositories.inquiry_repository import IInquiryRepository


class UpdateInquiryStatus:
    def __init__(self, inquiry_repo: IInquiryRepository) -> None:
        self.inquiry_repo = inquiry_repo

    async def execute(self, inquiry_id: UUID, status: str) -> Inquiry:
        inquiry = await self.inquiry_repo.find_by_id(inquiry_id)
        if not inquiry:
            raise ValueError("문의를 찾을 수 없습니다.")

        try:
            new_status = InquiryStatus(status)
        except ValueError:
            valid = ", ".join(s.value for s in InquiryStatus)
            raise ValueError(f"유효하지 않은 상태입니다. 가능한 값: {valid}")

        inquiry.status = new_status
        return await self.inquiry_repo.update(inquiry)
