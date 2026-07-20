"""회원정보 수정 Use Case — 이름/휴대폰/비밀번호 변경"""

from typing import Optional

from src.domain.entities.user import User
from src.domain.repositories.user_repository import IUserRepository
from src.infrastructure.security.password_hasher import PasswordHasher

MIN_PASSWORD_LENGTH = 8


class UpdateProfile:
    def __init__(self, user_repo: IUserRepository, password_hasher: PasswordHasher) -> None:
        self.user_repo = user_repo
        self.password_hasher = password_hasher

    async def execute(
        self,
        user_id: str,
        name: Optional[str] = None,
        phone: Optional[str] = None,
        password: Optional[str] = None,
    ) -> User:
        user = await self.user_repo.find_by_id(user_id)
        if not user:
            raise ValueError("사용자를 찾을 수 없습니다.")

        if password:
            if len(password) < MIN_PASSWORD_LENGTH:
                raise ValueError(f"비밀번호는 최소 {MIN_PASSWORD_LENGTH}자 이상이어야 합니다.")
            user.hashed_password = self.password_hasher.hash(password)

        user.update_profile(name=name, phone=phone)
        return await self.user_repo.update(user)
