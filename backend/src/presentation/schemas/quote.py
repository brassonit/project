"""견적 관련 Pydantic 스키마"""

from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel


class AttachmentItem(BaseModel):
    file_name: str
    file_url: str


class QuoteCreate(BaseModel):
    email: Optional[str] = None  # 비로그인 문의 시 필수, 로그인 시 가입 이메일 사용
    name: str
    phone: str
    event_title: str
    event_date: Optional[date] = None
    event_date_text: Optional[str] = None
    region: Optional[str] = None
    content: str = ""
    show_id: Optional[str] = None
    artist_ids: list[str] = []
    attachments: list[AttachmentItem] = []
    update_profile: bool = False  # 회원정보의 이름/전화번호 업데이트


class QuoteReply(BaseModel):
    quote_file_url: Optional[str] = None  # 견적서 파일


class QuoteArtistItem(BaseModel):
    artist_id: str
    artist_name: Optional[str] = None


class QuoteResponse(BaseModel):
    id: str
    user_id: Optional[str]
    email: str
    name: str
    phone: str
    event_title: str
    event_date: Optional[date]
    event_date_text: Optional[str]
    region: Optional[str]
    content: str
    show_id: Optional[str]
    show_title: Optional[str]
    status: str  # received(접수완료) | replied(회신완료)
    quote_file_url: Optional[str]
    replied_at: Optional[datetime]
    artists: list[QuoteArtistItem]
    attachments: list[AttachmentItem]
    created_at: datetime


class QuoteListResponse(BaseModel):
    quotes: list[QuoteResponse]
    total: int
    skip: int
    limit: int
