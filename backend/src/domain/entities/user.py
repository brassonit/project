"""User 도메인 엔티티"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID


class UserRole(str, Enum):
    CUSTOMER = "customer"
    ADMIN = "admin"


@dataclass
class User:
    id: Optional[UUID]
    email: str
    hashed_password: str
    role: UserRole
    is_verified: bool
    verification_token: Optional[str]
    created_at: datetime

    def verify_email(self) -> None:
        self.is_verified = True
        self.verification_token = None

    def is_admin(self) -> bool:
        return self.role == UserRole.ADMIN
