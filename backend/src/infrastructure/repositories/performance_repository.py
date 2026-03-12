"""Performance Repository SQLAlchemy 구현"""

from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from src.domain.entities.performance import Performance
from src.domain.repositories.performance_repository import IPerformanceRepository
from src.infrastructure.database.models import PerformanceModel


class SqlAlchemyPerformanceRepository(IPerformanceRepository):
    def __init__(self, db: Session) -> None:
        self.db = db

    def _to_entity(self, model: PerformanceModel) -> Performance:
        return Performance(
            id=model.id,
            title=model.title,
            description=model.description,
            event_date=model.event_date,
            venue=model.venue,
            image_url=model.image_url,
            artist_id=model.artist_id,
            is_featured=model.is_featured,
            created_at=model.created_at,
        )

    def _to_model(self, entity: Performance) -> PerformanceModel:
        return PerformanceModel(
            id=entity.id,
            title=entity.title,
            description=entity.description,
            event_date=entity.event_date,
            venue=entity.venue,
            image_url=entity.image_url,
            artist_id=entity.artist_id,
            is_featured=entity.is_featured,
            created_at=entity.created_at,
        )

    async def save(self, performance: Performance) -> Performance:
        model = self._to_model(performance)
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return self._to_entity(model)

    async def find_by_id(self, performance_id: UUID) -> Optional[Performance]:
        model = self.db.query(PerformanceModel).filter(PerformanceModel.id == performance_id).first()
        return self._to_entity(model) if model else None

    async def find_all(self, skip: int = 0, limit: int = 20) -> list[Performance]:
        models = (
            self.db.query(PerformanceModel).order_by(PerformanceModel.event_date.desc()).offset(skip).limit(limit).all()
        )
        return [self._to_entity(m) for m in models]

    async def find_featured(self, skip: int = 0, limit: int = 20) -> list[Performance]:
        models = (
            self.db.query(PerformanceModel)
            .filter(PerformanceModel.is_featured.is_(True))
            .order_by(PerformanceModel.event_date.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        return [self._to_entity(m) for m in models]

    async def update(self, performance: Performance) -> Performance:
        model = self.db.query(PerformanceModel).filter(PerformanceModel.id == performance.id).first()
        if not model:
            raise ValueError("공연을 찾을 수 없습니다.")
        model.title = performance.title
        model.description = performance.description
        model.event_date = performance.event_date
        model.venue = performance.venue
        model.image_url = performance.image_url
        model.artist_id = performance.artist_id
        model.is_featured = performance.is_featured
        self.db.commit()
        self.db.refresh(model)
        return self._to_entity(model)

    async def delete(self, performance_id: UUID) -> None:
        self.db.query(PerformanceModel).filter(PerformanceModel.id == performance_id).delete()
        self.db.commit()

    async def count_all(self) -> int:
        return self.db.query(PerformanceModel).count()

    async def count_featured(self) -> int:
        return self.db.query(PerformanceModel).filter(PerformanceModel.is_featured.is_(True)).count()
