"""User Repository SQLAlchemy 구현"""

from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from src.domain.entities.user import User, UserRole
from src.domain.repositories.user_repository import IUserRepository
from src.infrastructure.database.models import CartModel, ShowWishlistModel, UserModel, WishlistModel


class SqlAlchemyUserRepository(IUserRepository):
    def __init__(self, db: Session) -> None:
        self.db = db

    def _to_entity(self, model: UserModel) -> User:
        return User(
            id=model.id,
            email=model.email,
            hashed_password=model.hashed_password,
            name=model.name,
            phone=model.phone,
            role=UserRole(model.role),
            is_verified=model.is_verified,
            verification_token=model.verification_token,
            created_at=model.created_at,
            updated_at=model.updated_at,
            deleted_at=model.deleted_at,
        )

    def _active(self):
        return self.db.query(UserModel).filter(UserModel.deleted_at.is_(None))

    async def save(self, user: User) -> User:
        model = UserModel(
            email=user.email,
            hashed_password=user.hashed_password,
            name=user.name,
            phone=user.phone,
            role=user.role.value,
            is_verified=user.is_verified,
            verification_token=user.verification_token,
        )
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return self._to_entity(model)

    async def find_by_id(self, user_id: str) -> Optional[User]:
        model = self._active().filter(UserModel.id == user_id).first()
        return self._to_entity(model) if model else None

    async def find_by_email(self, email: str) -> Optional[User]:
        model = self._active().filter(UserModel.email == email).first()
        return self._to_entity(model) if model else None

    async def find_by_verification_token(self, token: str) -> Optional[User]:
        model = self._active().filter(UserModel.verification_token == token).first()
        return self._to_entity(model) if model else None

    async def update(self, user: User) -> User:
        model = self.db.query(UserModel).filter(UserModel.id == user.id).first()
        if not model:
            raise ValueError("사용자를 찾을 수 없습니다.")
        model.email = user.email
        model.hashed_password = user.hashed_password
        model.name = user.name
        model.phone = user.phone
        model.role = user.role.value
        model.is_verified = user.is_verified
        model.verification_token = user.verification_token
        model.updated_at = datetime.now()
        self.db.commit()
        self.db.refresh(model)
        return self._to_entity(model)

    async def delete(self, user_id: str) -> None:
        """회원탈퇴 (soft delete) — 찜/장바구니는 함께 제거"""
        model = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        if model:
            model.deleted_at = datetime.now()
            self.db.query(WishlistModel).filter(WishlistModel.user_id == user_id).delete()
            self.db.query(ShowWishlistModel).filter(ShowWishlistModel.user_id == user_id).delete()
            self.db.query(CartModel).filter(CartModel.user_id == user_id).delete()
            self.db.commit()
