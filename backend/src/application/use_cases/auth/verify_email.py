"""이메일 인증 Use Case"""

from src.domain.entities.user import User
from src.domain.repositories.user_repository import IUserRepository


class VerifyEmail:
    def __init__(self, user_repo: IUserRepository) -> None:
        self.user_repo = user_repo

    async def execute(self, token: str) -> User:
        user = await self.user_repo.find_by_verification_token(token)
        if not user:
            raise ValueError("유효하지 않은 인증 토큰입니다.")

        if user.is_verified:
            raise ValueError("이미 인증된 사용자입니다.")

        user.verify_email()
        await self.user_repo.update(user)

        return user
