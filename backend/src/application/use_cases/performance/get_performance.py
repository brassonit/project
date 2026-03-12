"""공연 상세 조회 Use Case"""

from uuid import UUID

from src.domain.entities.performance import Performance
from src.domain.repositories.performance_repository import IPerformanceRepository


class GetPerformance:
    def __init__(self, performance_repo: IPerformanceRepository) -> None:
        self.performance_repo = performance_repo

    async def execute(self, performance_id: UUID) -> Performance:
        performance = await self.performance_repo.find_by_id(performance_id)
        if not performance:
            raise ValueError("공연을 찾을 수 없습니다.")
        return performance
