"""로그인 Use Case"""

from typing import Any

from src.domain.repositories.user_repository import IUserRepository
from src.infrastructure.security.jwt_handler import JWTHandler
from src.infrastructure.security.password_hasher import PasswordHasher


class LoginUser:
    def __init__(
        self,
        user_repo: IUserRepository,
        password_hasher: PasswordHasher,
        jwt_handler: JWTHandler,
    ) -> None:
        self.user_repo = user_repo
        self.password_hasher = password_hasher
        self.jwt_handler = jwt_handler

    async def execute(self, email: str, password: str) -> dict[str, Any]:
        # 사용자 조회
        user = await self.user_repo.find_by_email(email)
        if not user:
            raise ValueError("등록되지 않은 이메일입니다.")

        # 이메일 인증 확인
        if not user.is_verified:
            raise ValueError("이메일 인증이 필요합니다. 이메일을 확인해주세요.")

        # 비밀번호 검증
        if not self.password_hasher.verify(password, user.hashed_password):
            raise ValueError("비밀번호가 일치하지 않습니다.")

        # JWT 토큰 생성
        access_token = self.jwt_handler.create_access_token(user.id, user.role.value)

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": user,
        }
