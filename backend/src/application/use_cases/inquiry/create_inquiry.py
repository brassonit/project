"""문의 생성 Use Case"""

import re
from datetime import datetime
from typing import Optional

from src.domain.entities.inquiry import Inquiry, InquiryStatus
from src.domain.repositories.inquiry_repository import IInquiryRepository

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")


class CreateInquiry:
    def __init__(self, inquiry_repo: IInquiryRepository) -> None:
        self.inquiry_repo = inquiry_repo

    async def execute(
        self,
        name: str,
        email: str,
        subject: str,
        message: str,
        phone: Optional[str] = None,
    ) -> Inquiry:
        if not EMAIL_REGEX.match(email):
            raise ValueError("유효하지 않은 이메일 형식입니다.")

        inquiry = Inquiry(
            id=None,
            name=name,
            email=email,
            phone=phone,
            subject=subject,
            message=message,
            status=InquiryStatus.PENDING,
            admin_reply=None,
            created_at=datetime.now(),
        )
        return await self.inquiry_repo.save(inquiry)
