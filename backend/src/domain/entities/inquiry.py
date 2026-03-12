"""Inquiry 도메인 엔티티"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID


class InquiryStatus(str, Enum):
    PENDING = "pending"
    REPLIED = "replied"
    CLOSED = "closed"


@dataclass
class Inquiry:
    id: Optional[UUID]
    name: str
    email: str
    phone: Optional[str]
    subject: str
    message: str
    status: InquiryStatus = InquiryStatus.PENDING
    admin_reply: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self) -> None:
        if not self.name or not self.name.strip():
            raise ValueError("이름은 필수입니다.")
        if not self.subject or not self.subject.strip():
            raise ValueError("제목은 필수입니다.")
        if not self.message or not self.message.strip():
            raise ValueError("내용은 필수입니다.")

    def reply(self, reply_text: str) -> None:
        self.admin_reply = reply_text
        self.status = InquiryStatus.REPLIED

    def close(self) -> None:
        self.status = InquiryStatus.CLOSED
