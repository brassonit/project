"""회원탈퇴 Use Case — soft delete, 찜/장바구니 함께 삭제"""

from src.domain.repositories.user_repository import IUserRepository


class WithdrawUser:
    def __init__(self, user_repo: IUserRepository) -> None:
        self.user_repo = user_repo

    async def execute(self, user_id: str) -> None:
        user = await self.user_repo.find_by_id(user_id)
        if not user:
            raise ValueError("사용자를 찾을 수 없습니다.")
        await self.user_repo.delete(user_id)
