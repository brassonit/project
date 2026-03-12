"""공연 목록 조회 Use Case"""

from src.domain.entities.performance import Performance
from src.domain.repositories.performance_repository import IPerformanceRepository


class ListPerformances:
    def __init__(self, performance_repo: IPerformanceRepository) -> None:
        self.performance_repo = performance_repo

    async def execute(
        self,
        featured_only: bool = False,
        skip: int = 0,
        limit: int = 20,
    ) -> dict[str, object]:
        if featured_only:
            performances: list[Performance] = await self.performance_repo.find_featured(skip=skip, limit=limit)
            total: int = await self.performance_repo.count_featured()
        else:
            performances = await self.performance_repo.find_all(skip=skip, limit=limit)
            total = await self.performance_repo.count_all()

        return {"performances": performances, "total": total}
