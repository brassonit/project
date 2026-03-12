"""문의 답변 Use Case"""

from uuid import UUID

from src.domain.entities.inquiry import Inquiry
from src.domain.repositories.inquiry_repository import IInquiryRepository


class ReplyInquiry:
    def __init__(self, inquiry_repo: IInquiryRepository) -> None:
        self.inquiry_repo = inquiry_repo

    async def execute(self, inquiry_id: UUID, reply_text: str) -> Inquiry:
        inquiry = await self.inquiry_repo.find_by_id(inquiry_id)
        if not inquiry:
            raise ValueError("문의를 찾을 수 없습니다.")

        if not reply_text or not reply_text.strip():
            raise ValueError("답변 내용은 필수입니다.")

        inquiry.reply(reply_text)
        return await self.inquiry_repo.update(inquiry)
