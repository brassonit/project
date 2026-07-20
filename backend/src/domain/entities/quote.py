"""Quote(견적) 도메인 엔티티 — 견적 요청(로그인)/견적 문의(비로그인)"""

from dataclasses import dataclass, field
from datetime import date, datetime
from enum import Enum
from typing import Optional


class QuoteStatus(str, Enum):
    RECEIVED = "received"  # 접수완료
    REPLIED = "replied"  # 회신완료


@dataclass
class QuoteAttachment:
    file_name: str
    file_url: str
    id: Optional[str] = None


@dataclass
class QuoteArtist:
    artist_id: str
    artist_name: Optional[str] = None  # 조회 시 채워짐


@dataclass
class Quote:
    id: Optional[str]  # CHAR(8)
    user_id: Optional[str]  # NULL = 비로그인 문의
    email: str  # 회신 받을 이메일 (스냅샷)
    name: str  # 담당자 이름
    phone: str
    event_title: str  # 행사명
    event_date: Optional[date] = None  # 달력 선택 시
    event_date_text: Optional[str] = None  # 직접 입력 시 (둘 중 하나만)
    region: Optional[str] = None  # 행사지역
    content: str = ""
    show_id: Optional[str] = None  # 첨부된 공연
    show_title: Optional[str] = None  # 조회 시 채워짐
    show_lineup: list[str] = field(default_factory=list)  # 첨부 공연의 출연진 (조회 시 채워짐)
    status: QuoteStatus = QuoteStatus.RECEIVED
    quote_file_url: Optional[str] = None  # 회신완료 시 견적서 파일
    replied_at: Optional[datetime] = None
    artists: list[QuoteArtist] = field(default_factory=list)
    attachments: list[QuoteAttachment] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self) -> None:
        if not self.email or not self.email.strip():
            raise ValueError("이메일은 필수입니다.")
        if not self.name or not self.name.strip():
            raise ValueError("이름은 필수입니다.")
        if not self.phone or not self.phone.strip():
            raise ValueError("전화번호는 필수입니다.")
        if not self.event_title or not self.event_title.strip():
            raise ValueError("행사명은 필수입니다.")

    def reply(self, quote_file_url: Optional[str] = None) -> None:
        self.status = QuoteStatus.REPLIED
        self.quote_file_url = quote_file_url
        self.replied_at = datetime.now()
