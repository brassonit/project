"""Policy(이용약관/개인정보취급방침) 도메인 엔티티 — 버전(effective_date)별 콘텐츠"""

from dataclasses import dataclass
from datetime import date, datetime
from enum import Enum


class PolicyType(str, Enum):
    TERMS = "terms"
    PRIVACY = "privacy"


@dataclass
class Policy:
    id: str
    policy_type: PolicyType
    effective_date: date
    content: str
    created_at: datetime
