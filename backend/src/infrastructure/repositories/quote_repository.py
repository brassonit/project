"""Quote Repository SQLAlchemy 구현"""

from typing import Optional

from sqlalchemy.orm import Session

from src.domain.entities.quote import Quote, QuoteArtist, QuoteAttachment, QuoteStatus
from src.domain.repositories.quote_repository import IQuoteRepository
from src.infrastructure.database.models import (
    ArtistModel,
    QuoteArtistModel,
    QuoteAttachmentModel,
    QuoteModel,
    ShowLineupModel,
    ShowModel,
)


class SqlAlchemyQuoteRepository(IQuoteRepository):
    def __init__(self, db: Session) -> None:
        self.db = db

    def _to_entity(self, model: QuoteModel) -> Quote:
        artist_rows = (
            self.db.query(QuoteArtistModel, ArtistModel.name)
            .outerjoin(ArtistModel, QuoteArtistModel.artist_id == ArtistModel.id)
            .filter(QuoteArtistModel.quote_id == model.id)
            .all()
        )
        attachments = (
            self.db.query(QuoteAttachmentModel).filter(QuoteAttachmentModel.quote_id == model.id).all()
        )
        show_title = None
        show_lineup: list[str] = []
        if model.show_id:
            show = self.db.query(ShowModel).filter(ShowModel.id == model.show_id).first()
            show_title = show.title if show else None
            lineup_rows = (
                self.db.query(ArtistModel.name)
                .join(ShowLineupModel, ShowLineupModel.artist_id == ArtistModel.id)
                .filter(ShowLineupModel.show_id == model.show_id)
                .order_by(ShowLineupModel.sort_order)
                .all()
            )
            show_lineup = [r.name for r in lineup_rows]
        return Quote(
            id=model.id,
            user_id=model.user_id,
            email=model.email,
            name=model.name,
            phone=model.phone,
            event_title=model.event_title,
            event_date=model.event_date,
            event_date_text=model.event_date_text,
            region=model.region,
            content=model.content,
            show_id=model.show_id,
            show_title=show_title,
            show_lineup=show_lineup,
            status=QuoteStatus(model.status),
            quote_file_url=model.quote_file_url,
            replied_at=model.replied_at,
            artists=[
                QuoteArtist(artist_id=r.QuoteArtistModel.artist_id, artist_name=r.name) for r in artist_rows
            ],
            attachments=[
                QuoteAttachment(id=a.id, file_name=a.file_name, file_url=a.file_url) for a in attachments
            ],
            created_at=model.created_at,
        )

    async def save(self, quote: Quote) -> Quote:
        model = QuoteModel(
            user_id=quote.user_id,
            email=quote.email,
            name=quote.name,
            phone=quote.phone,
            event_title=quote.event_title,
            event_date=quote.event_date,
            event_date_text=quote.event_date_text,
            region=quote.region,
            content=quote.content,
            show_id=quote.show_id,
            status=quote.status.value,
        )
        self.db.add(model)
        self.db.flush()
        for qa in quote.artists:
            self.db.add(QuoteArtistModel(quote_id=model.id, artist_id=qa.artist_id))
        for att in quote.attachments:
            self.db.add(
                QuoteAttachmentModel(quote_id=model.id, file_name=att.file_name, file_url=att.file_url)
            )
        self.db.commit()
        self.db.refresh(model)
        return self._to_entity(model)

    async def find_by_id(self, quote_id: str) -> Optional[Quote]:
        model = self.db.query(QuoteModel).filter(QuoteModel.id == quote_id).first()
        return self._to_entity(model) if model else None

    async def find_by_user(self, user_id: str, skip: int = 0, limit: int = 20) -> tuple[list[Quote], int]:
        q = self.db.query(QuoteModel).filter(QuoteModel.user_id == user_id)
        total = q.count()
        models = q.order_by(QuoteModel.created_at.desc()).offset(skip).limit(limit).all()
        return [self._to_entity(m) for m in models], total

    async def find_all(
        self, status: Optional[QuoteStatus] = None, skip: int = 0, limit: int = 20
    ) -> tuple[list[Quote], int]:
        q = self.db.query(QuoteModel)
        if status:
            q = q.filter(QuoteModel.status == status.value)
        total = q.count()
        models = q.order_by(QuoteModel.created_at.desc()).offset(skip).limit(limit).all()
        return [self._to_entity(m) for m in models], total

    async def update(self, quote: Quote) -> Quote:
        model = self.db.query(QuoteModel).filter(QuoteModel.id == quote.id).first()
        if not model:
            raise ValueError("견적을 찾을 수 없습니다.")
        model.status = quote.status.value
        model.quote_file_url = quote.quote_file_url
        model.replied_at = quote.replied_at
        self.db.commit()
        self.db.refresh(model)
        return self._to_entity(model)

    async def delete(self, quote_id: str) -> None:
        self.db.query(QuoteModel).filter(QuoteModel.id == quote_id).delete()
        self.db.commit()

    async def count_all(self) -> int:
        return self.db.query(QuoteModel).count()

    async def count_by_status(self, status: QuoteStatus) -> int:
        return self.db.query(QuoteModel).filter(QuoteModel.status == status.value).count()
