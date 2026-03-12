"""문의 관련 Pydantic 스키마"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class InquiryCreate(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    subject: str
    message: str


class InquiryReply(BaseModel):
    reply: str


class InquiryStatusUpdate(BaseModel):
    status: str


class InquiryResponse(BaseModel):
    id: UUID
    name: str
    email: str
    phone: Optional[str]
    subject: str
    message: str
    status: str
    admin_reply: Optional[str]
    created_at: datetime

    model_config = {"from_attributes": True}


class InquiryListResponse(BaseModel):
    inquiries: list[InquiryResponse]
    total: int
    skip: int
    limit: int
