"""관리자 대시보드 Use Case"""

from src.domain.entities.inquiry import InquiryStatus
from src.domain.repositories.artist_repository import IArtistRepository
from src.domain.repositories.inquiry_repository import IInquiryRepository
from src.domain.repositories.performance_repository import IPerformanceRepository


class GetDashboard:
    def __init__(
        self,
        artist_repo: IArtistRepository,
        performance_repo: IPerformanceRepository,
        inquiry_repo: IInquiryRepository,
    ) -> None:
        self.artist_repo = artist_repo
        self.performance_repo = performance_repo
        self.inquiry_repo = inquiry_repo

    async def execute(self) -> dict:
        artist_count = await self.artist_repo.count_all_admin()
        active_artist_count = await self.artist_repo.count_all()
        performance_count = await self.performance_repo.count_all()
        featured_count = await self.performance_repo.count_featured()
        inquiry_total = await self.inquiry_repo.count_all()
        inquiry_pending = await self.inquiry_repo.count_by_status(InquiryStatus.PENDING)
        inquiry_replied = await self.inquiry_repo.count_by_status(InquiryStatus.REPLIED)
        inquiry_closed = await self.inquiry_repo.count_by_status(InquiryStatus.CLOSED)

        return {
            "artists": {
                "total": artist_count,
                "active": active_artist_count,
                "inactive": artist_count - active_artist_count,
            },
            "performances": {
                "total": performance_count,
                "featured": featured_count,
            },
            "inquiries": {
                "total": inquiry_total,
                "pending": inquiry_pending,
                "replied": inquiry_replied,
                "closed": inquiry_closed,
            },
        }
