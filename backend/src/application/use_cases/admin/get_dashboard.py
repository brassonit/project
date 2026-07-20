"""관리자 대시보드 Use Case"""

from src.domain.entities.quote import QuoteStatus
from src.domain.repositories.artist_repository import IArtistRepository
from src.domain.repositories.quote_repository import IQuoteRepository
from src.domain.repositories.show_repository import IShowRepository


class GetDashboard:
    def __init__(
        self,
        artist_repo: IArtistRepository,
        show_repo: IShowRepository,
        quote_repo: IQuoteRepository,
    ) -> None:
        self.artist_repo = artist_repo
        self.show_repo = show_repo
        self.quote_repo = quote_repo

    async def execute(self) -> dict:
        artist_total = await self.artist_repo.count_all_admin()
        artist_active = await self.artist_repo.count_all()
        show_total = await self.show_repo.count_all()
        show_upcoming = await self.show_repo.count_upcoming()
        quote_total = await self.quote_repo.count_all()
        quote_received = await self.quote_repo.count_by_status(QuoteStatus.RECEIVED)
        quote_replied = await self.quote_repo.count_by_status(QuoteStatus.REPLIED)

        return {
            "artists": {
                "total": artist_total,
                "active": artist_active,
                "inactive": artist_total - artist_active,
            },
            "shows": {
                "total": show_total,
                "upcoming": show_upcoming,
                "past": show_total - show_upcoming,
            },
            "quotes": {
                "total": quote_total,
                "received": quote_received,
                "replied": quote_replied,
            },
        }
