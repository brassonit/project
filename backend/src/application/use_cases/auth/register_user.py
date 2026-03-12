"""회원가입 Use Case"""

import re
import secrets
from datetime import datetime

from src.domain.entities.user import User, UserRole
from src.domain.repositories.user_repository import IUserRepository
from src.infrastructure.email.email_service import EmailService
from src.infrastructure.security.password_hasher import PasswordHasher

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
MIN_PASSWORD_LENGTH = 8


class RegisterUser:
    def __init__(
        self,
        user_repo: IUserRepository,
        password_hasher: PasswordHasher,
        email_service: EmailService,
    ) -> None:
        self.user_repo = user_repo
        self.password_hasher = password_hasher
        self.email_service = email_service

    async def execute(self, email: str, password: str) -> User:
        # 이메일 형식 검증
        if not EMAIL_REGEX.match(email):
            raise ValueError("유효하지 않은 이메일 형식입니다.")

        # 비밀번호 강도 검증
        if len(password) < MIN_PASSWORD_LENGTH:
            raise ValueError(f"비밀번호는 최소 {MIN_PASSWORD_LENGTH}자 이상이어야 합니다.")

        # 이메일 중복 확인
        existing = await self.user_repo.find_by_email(email)
        if existing:
            raise ValueError("이미 등록된 이메일입니다.")

        # 사용자 생성
        hashed_password = self.password_hasher.hash(password)
        verification_token = secrets.token_urlsafe(32)

        user = User(
            id=None,
            email=email,
            hashed_password=hashed_password,
            role=UserRole.CUSTOMER,
            is_verified=False,
            verification_token=verification_token,
            created_at=datetime.now(),
        )

        saved_user = await self.user_repo.save(user)

        # 인증 이메일 발송
        await self.email_service.send_verification_email(email, verification_token)

        return saved_user
