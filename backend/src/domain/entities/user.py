"""User 도메인 엔티티"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class UserRole(str, Enum):
    CUSTOMER = "customer"
    ADMIN = "admin"


@dataclass
class User:
    id: Optional[str]  # CHAR(8)
    email: str
    hashed_password: str
    role: UserRole
    is_verified: bool
    verification_token: Optional[str]
    created_at: datetime
    name: Optional[str] = None
    phone: Optional[str] = None
    updated_at: datetime = field(default_factory=datetime.now)
    deleted_at: Optional[datetime] = None  # 회원탈퇴 (soft delete)

    def verify_email(self) -> None:
        self.is_verified = True
        self.verification_token = None

    def update_profile(self, name: Optional[str], phone: Optional[str]) -> None:
        self.name = name
        self.phone = phone
        self.updated_at = datetime.now()

    def withdraw(self) -> None:
        self.deleted_at = datetime.now()

    def is_admin(self) -> bool:
        return self.role == UserRole.ADMIN
