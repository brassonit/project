"""공연 수정 Use Case"""

from datetime import date
from typing import Optional
from uuid import UUID

from src.domain.entities.performance import Performance
from src.domain.repositories.performance_repository import IPerformanceRepository


class UpdatePerformance:
    def __init__(self, performance_repo: IPerformanceRepository) -> None:
        self.performance_repo = performance_repo

    async def execute(
        self,
        performance_id: UUID,
        title: Optional[str] = None,
        description: Optional[str] = None,
        event_date: Optional[date] = None,
        venue: Optional[str] = None,
        image_url: Optional[str] = None,
        artist_id: Optional[UUID] = None,
        is_featured: Optional[bool] = None,
    ) -> Performance:
        performance = await self.performance_repo.find_by_id(performance_id)
        if not performance:
            raise ValueError("공연을 찾을 수 없습니다.")

        if title is not None:
            performance.title = title
        if description is not None:
            performance.description = description
        if event_date is not None:
            performance.event_date = event_date
        if venue is not None:
            performance.venue = venue
        if image_url is not None:
            performance.image_url = image_url
        if artist_id is not None:
            performance.artist_id = artist_id
        if is_featured is not None:
            performance.is_featured = is_featured

        return await self.performance_repo.update(performance)
