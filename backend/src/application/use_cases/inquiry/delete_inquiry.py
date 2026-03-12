"""문의 삭제 Use Case"""

from uuid import UUID

from src.domain.repositories.inquiry_repository import IInquiryRepository


class DeleteInquiry:
    def __init__(self, inquiry_repo: IInquiryRepository) -> None:
        self.inquiry_repo = inquiry_repo

    async def execute(self, inquiry_id: UUID) -> None:
        inquiry = await self.inquiry_repo.find_by_id(inquiry_id)
        if not inquiry:
            raise ValueError("문의를 찾을 수 없습니다.")
        await self.inquiry_repo.delete(inquiry_id)
