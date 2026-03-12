"""User Repository SQLAlchemy 구현"""

from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from src.domain.entities.user import User, UserRole
from src.domain.repositories.user_repository import IUserRepository
from src.infrastructure.database.models import UserModel


class SqlAlchemyUserRepository(IUserRepository):
    def __init__(self, db: Session) -> None:
        self.db = db

    def _to_entity(self, model: UserModel) -> User:
        return User(
            id=model.id,
            email=model.email,
            hashed_password=model.hashed_password,
            role=UserRole(model.role),
            is_verified=model.is_verified,
            verification_token=model.verification_token,
            created_at=model.created_at,
        )

    def _to_model(self, entity: User) -> UserModel:
        return UserModel(
            id=entity.id,
            email=entity.email,
            hashed_password=entity.hashed_password,
            role=entity.role.value,
            is_verified=entity.is_verified,
            verification_token=entity.verification_token,
            created_at=entity.created_at,
        )

    async def save(self, user: User) -> User:
        model = self._to_model(user)
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return self._to_entity(model)

    async def find_by_id(self, user_id: UUID) -> Optional[User]:
        model = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        return self._to_entity(model) if model else None

    async def find_by_email(self, email: str) -> Optional[User]:
        model = self.db.query(UserModel).filter(UserModel.email == email).first()
        return self._to_entity(model) if model else None

    async def find_by_verification_token(self, token: str) -> Optional[User]:
        model = self.db.query(UserModel).filter(UserModel.verification_token == token).first()
        return self._to_entity(model) if model else None

    async def update(self, user: User) -> User:
        model = self.db.query(UserModel).filter(UserModel.id == user.id).first()
        if model:
            model.email = user.email
            model.hashed_password = user.hashed_password
            model.role = user.role.value
            model.is_verified = user.is_verified
            model.verification_token = user.verification_token
            self.db.commit()
            self.db.refresh(model)
            return self._to_entity(model)
        raise ValueError("사용자를 찾을 수 없습니다.")

    async def delete(self, user_id: UUID) -> None:
        self.db.query(UserModel).filter(UserModel.id == user_id).delete()
        self.db.commit()
