"""Show Repository SQLAlchemy 구현"""

from datetime import date
from typing import Optional

from sqlalchemy.orm import Session

from src.domain.entities.show import Show, ShowLineup, ShowTicket, ShowVideo
from src.domain.repositories.show_repository import IShowRepository
from src.infrastructure.database.models import (
    ArtistModel,
    ShowLineupModel,
    ShowModel,
    ShowTicketModel,
    ShowVideoModel,
)


class SqlAlchemyShowRepository(IShowRepository):
    def __init__(self, db: Session) -> None:
        self.db = db

    def _to_entity(self, model: ShowModel) -> Show:
        lineup_rows = (
            self.db.query(ShowLineupModel, ArtistModel.name)
            .outerjoin(ArtistModel, ShowLineupModel.artist_id == ArtistModel.id)
            .filter(ShowLineupModel.show_id == model.id)
            .order_by(ShowLineupModel.sort_order)
            .all()
        )
        tickets = (
            self.db.query(ShowTicketModel)
            .filter(ShowTicketModel.show_id == model.id)
            .order_by(ShowTicketModel.sort_order)
            .all()
        )
        videos = (
            self.db.query(ShowVideoModel)
            .filter(ShowVideoModel.show_id == model.id)
            .order_by(ShowVideoModel.sort_order)
            .all()
        )
        return Show(
            id=model.id,
            category_id=model.category_id,
            title=model.title,
            event_date=model.event_date,
            venue=model.venue,
            description=model.description,
            intro=model.intro,
            image_url=model.image_url,
            like_count=model.like_count,
            view_count=model.view_count,
            lineup=[
                ShowLineup(artist_id=r.ShowLineupModel.artist_id, artist_name=r.name, sort_order=r.ShowLineupModel.sort_order)
                for r in lineup_rows
            ],
            tickets=[ShowTicket(id=t.id, label=t.label, url=t.url, sort_order=t.sort_order) for t in tickets],
            videos=[ShowVideo(id=v.id, video_url=v.video_url, title=v.title, sort_order=v.sort_order) for v in videos],
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def _sync_children(self, show_id: str, entity: Show) -> None:
        self.db.query(ShowLineupModel).filter(ShowLineupModel.show_id == show_id).delete()
        self.db.query(ShowTicketModel).filter(ShowTicketModel.show_id == show_id).delete()
        self.db.query(ShowVideoModel).filter(ShowVideoModel.show_id == show_id).delete()
        for i, lu in enumerate(entity.lineup):
            self.db.add(ShowLineupModel(show_id=show_id, artist_id=lu.artist_id, sort_order=i))
        for i, t in enumerate(entity.tickets):
            self.db.add(ShowTicketModel(show_id=show_id, label=t.label, url=t.url, sort_order=i))
        for i, v in enumerate(entity.videos):
            self.db.add(ShowVideoModel(show_id=show_id, video_url=v.video_url, title=v.title, sort_order=i))

    async def save(self, show: Show) -> Show:
        model = ShowModel(
            category_id=show.category_id,
            title=show.title,
            event_date=show.event_date,
            venue=show.venue,
            description=show.description,
            intro=show.intro,
            image_url=show.image_url,
        )
        self.db.add(model)
        self.db.flush()
        self._sync_children(model.id, show)
        self.db.commit()
        self.db.refresh(model)
        return self._to_entity(model)

    async def find_by_id(self, show_id: str) -> Optional[Show]:
        model = self.db.query(ShowModel).filter(ShowModel.id == show_id).first()
        return self._to_entity(model) if model else None

    async def find_all(self, skip: int = 0, limit: int = 100) -> tuple[list[Show], int]:
        q = self.db.query(ShowModel)
        total = q.count()
        models = q.order_by(ShowModel.event_date.desc()).offset(skip).limit(limit).all()
        return [self._to_entity(m) for m in models], total

    async def update(self, show: Show) -> Show:
        model = self.db.query(ShowModel).filter(ShowModel.id == show.id).first()
        if not model:
            raise ValueError("공연을 찾을 수 없습니다.")
        model.category_id = show.category_id
        model.title = show.title
        model.event_date = show.event_date
        model.venue = show.venue
        model.description = show.description
        model.intro = show.intro
        model.image_url = show.image_url
        model.updated_at = show.updated_at
        self._sync_children(model.id, show)
        self.db.commit()
        self.db.refresh(model)
        return self._to_entity(model)

    async def delete(self, show_id: str) -> None:
        self.db.query(ShowModel).filter(ShowModel.id == show_id).delete()
        self.db.commit()

    async def increment_view(self, show_id: str) -> None:
        self.db.query(ShowModel).filter(ShowModel.id == show_id).update(
            {ShowModel.view_count: ShowModel.view_count + 1}
        )
        self.db.commit()

    async def count_all(self) -> int:
        return self.db.query(ShowModel).count()

    async def count_upcoming(self) -> int:
        return self.db.query(ShowModel).filter(ShowModel.event_date >= date.today()).count()
