"""Policy Repository SQLAlchemy 구현"""

from datetime import date
from typing import Optional

from sqlalchemy.orm import Session

from src.domain.entities.policy import Policy, PolicyType
from src.domain.repositories.policy_repository import IPolicyRepository
from src.infrastructure.database.models import PolicyModel


class SqlAlchemyPolicyRepository(IPolicyRepository):
    def __init__(self, db: Session) -> None:
        self.db = db

    def _to_entity(self, model: PolicyModel) -> Policy:
        return Policy(
            id=model.id,
            policy_type=PolicyType(model.policy_type),
            effective_date=model.effective_date,
            content=model.content,
            created_at=model.created_at,
        )

    async def find_versions(self, policy_type: PolicyType) -> list[date]:
        rows = (
            self.db.query(PolicyModel.effective_date)
            .filter(PolicyModel.policy_type == policy_type.value)
            .order_by(PolicyModel.effective_date.desc())
            .all()
        )
        return [r.effective_date for r in rows]

    async def find_by_type(
        self, policy_type: PolicyType, effective_date: Optional[date] = None
    ) -> Optional[Policy]:
        q = self.db.query(PolicyModel).filter(PolicyModel.policy_type == policy_type.value)
        if effective_date is not None:
            q = q.filter(PolicyModel.effective_date == effective_date)
        else:
            q = q.order_by(PolicyModel.effective_date.desc())
        model = q.first()
        return self._to_entity(model) if model else None
