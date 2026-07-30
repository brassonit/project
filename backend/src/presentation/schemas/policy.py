"""Policy(이용약관/개인정보취급방침) Pydantic 스키마"""

from datetime import date

from pydantic import BaseModel


class PolicyResponse(BaseModel):
    policy_type: str
    effective_date: date
    content: str
    versions: list[date]  # 해당 정책의 전체 시행일 목록 (최신순)
