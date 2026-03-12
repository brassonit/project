"""공연 생성 Use Case"""

from datetime import date, datetime
from typing import Optional
from uuid import UUID

from src.domain.entities.performance import Performance
from src.domain.repositories.performance_repository import IPerformanceRepository


class CreatePerformance:
    def __init__(self, performance_repo: IPerformanceRepository) -> None:
        self.performance_repo = performance_repo

    async def execute(
        self,
        title: str,
        description: str,
        event_date: date,
        venue: str,
        image_url: Optional[str] = None,
        artist_id: Optional[UUID] = None,
        is_featured: bool = False,
    ) -> Performance:
        performance = Performance(
            id=None,
            title=title,
            description=description,
            event_date=event_date,
            venue=venue,
            image_url=image_url,
            artist_id=artist_id,
            is_featured=is_featured,
            created_at=datetime.now(),
        )
        return await self.performance_repo.save(performance)
