"""Inquiry Repository SQLAlchemy 구현"""

from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from src.domain.entities.inquiry import Inquiry, InquiryStatus
from src.domain.repositories.inquiry_repository import IInquiryRepository
from src.infrastructure.database.models import InquiryModel


class SqlAlchemyInquiryRepository(IInquiryRepository):
    def __init__(self, db: Session) -> None:
        self.db = db

    def _to_entity(self, model: InquiryModel) -> Inquiry:
        return Inquiry(
            id=model.id,
            name=model.name,
            email=model.email,
            phone=model.phone,
            subject=model.subject,
            message=model.message,
            status=InquiryStatus(model.status),
            admin_reply=model.admin_reply,
            created_at=model.created_at,
        )

    def _to_model(self, entity: Inquiry) -> InquiryModel:
        return InquiryModel(
            id=entity.id,
            name=entity.name,
            email=entity.email,
            phone=entity.phone,
            subject=entity.subject,
            message=entity.message,
            status=entity.status.value,
            admin_reply=entity.admin_reply,
            created_at=entity.created_at,
        )

    async def save(self, inquiry: Inquiry) -> Inquiry:
        model = self._to_model(inquiry)
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return self._to_entity(model)

    async def find_by_id(self, inquiry_id: UUID) -> Optional[Inquiry]:
        model = self.db.query(InquiryModel).filter(InquiryModel.id == inquiry_id).first()
        return self._to_entity(model) if model else None

    async def find_all(self, skip: int = 0, limit: int = 20) -> list[Inquiry]:
        models = self.db.query(InquiryModel).order_by(InquiryModel.created_at.desc()).offset(skip).limit(limit).all()
        return [self._to_entity(m) for m in models]

    async def find_by_status(self, status: InquiryStatus, skip: int = 0, limit: int = 20) -> list[Inquiry]:
        models = (
            self.db.query(InquiryModel)
            .filter(InquiryModel.status == status.value)
            .order_by(InquiryModel.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        return [self._to_entity(m) for m in models]

    async def update(self, inquiry: Inquiry) -> Inquiry:
        model = self.db.query(InquiryModel).filter(InquiryModel.id == inquiry.id).first()
        if not model:
            raise ValueError("문의를 찾을 수 없습니다.")
        model.name = inquiry.name
        model.email = inquiry.email
        model.phone = inquiry.phone
        model.subject = inquiry.subject
        model.message = inquiry.message
        model.status = inquiry.status.value
        model.admin_reply = inquiry.admin_reply
        self.db.commit()
        self.db.refresh(model)
        return self._to_entity(model)

    async def delete(self, inquiry_id: UUID) -> None:
        self.db.query(InquiryModel).filter(InquiryModel.id == inquiry_id).delete()
        self.db.commit()

    async def count_all(self) -> int:
        return self.db.query(InquiryModel).count()

    async def count_by_status(self, status: InquiryStatus) -> int:
        return self.db.query(InquiryModel).filter(InquiryModel.status == status.value).count()
