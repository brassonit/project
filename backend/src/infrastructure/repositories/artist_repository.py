"""Artist Repository SQLAlchemy 구현"""

from typing import Optional

from sqlalchemy import or_
from sqlalchemy.orm import Session

from src.domain.entities.artist import Artist, ArtistPortfolio, ArtistVideo
from src.domain.repositories.artist_repository import IArtistRepository
from src.infrastructure.database.models import (
    ArtistImageModel,
    ArtistModel,
    ArtistPortfolioModel,
    ArtistVideoModel,
    CategoryModel,
    GenreModel,
)

PF_TAG_ORDER = ["주요활동", "앨범", "수상내역", "경력사항"]


class SqlAlchemyArtistRepository(IArtistRepository):
    def __init__(self, db: Session) -> None:
        self.db = db

    def _to_entity(self, model: ArtistModel, with_children: bool = True) -> Artist:
        genre = self.db.query(GenreModel).filter(GenreModel.id == model.genre_id).first()
        category = (
            self.db.query(CategoryModel).filter(CategoryModel.id == genre.category_id).first() if genre else None
        )
        images: list[str] = []
        portfolios: list[ArtistPortfolio] = []
        videos: list[ArtistVideo] = []
        if with_children:
            images = [
                r.image_url
                for r in self.db.query(ArtistImageModel)
                .filter(ArtistImageModel.artist_id == model.id)
                .order_by(ArtistImageModel.sort_order)
                .all()
            ]
            portfolios = [
                ArtistPortfolio(id=r.id, tag=r.tag, year=r.year, content=r.content)
                for r in self.db.query(ArtistPortfolioModel)
                .filter(ArtistPortfolioModel.artist_id == model.id)
                .order_by(ArtistPortfolioModel.year.desc())
                .all()
            ]
            portfolios.sort(key=lambda p: (PF_TAG_ORDER.index(p.tag) if p.tag in PF_TAG_ORDER else 99, -p.year))
            videos = [
                ArtistVideo(id=r.id, video_url=r.video_url, title=r.title, sort_order=r.sort_order)
                for r in self.db.query(ArtistVideoModel)
                .filter(ArtistVideoModel.artist_id == model.id)
                .order_by(ArtistVideoModel.sort_order)
                .all()
            ]
        return Artist(
            id=model.id,
            genre_id=model.genre_id,
            name=model.name,
            members=model.members,
            description=model.description,
            like_count=model.like_count,
            view_count=model.view_count,
            is_active=model.is_active,
            images=images,
            portfolios=portfolios,
            videos=videos,
            genre_name=genre.name if genre else None,
            category_name=category.name if category else None,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def _sync_children(self, artist_id: str, entity: Artist) -> None:
        """이미지/포트폴리오/영상 전체 교체"""
        self.db.query(ArtistImageModel).filter(ArtistImageModel.artist_id == artist_id).delete()
        self.db.query(ArtistPortfolioModel).filter(ArtistPortfolioModel.artist_id == artist_id).delete()
        self.db.query(ArtistVideoModel).filter(ArtistVideoModel.artist_id == artist_id).delete()
        for i, url in enumerate(entity.images):
            self.db.add(ArtistImageModel(artist_id=artist_id, image_url=url, sort_order=i))
        for p in entity.portfolios:
            self.db.add(ArtistPortfolioModel(artist_id=artist_id, tag=p.tag, year=p.year, content=p.content))
        for i, v in enumerate(entity.videos):
            self.db.add(ArtistVideoModel(artist_id=artist_id, video_url=v.video_url, title=v.title, sort_order=i))

    async def save(self, artist: Artist) -> Artist:
        model = ArtistModel(
            genre_id=artist.genre_id,
            name=artist.name,
            members=artist.members,
            description=artist.description,
            like_count=artist.like_count,
            view_count=artist.view_count,
            is_active=artist.is_active,
        )
        self.db.add(model)
        self.db.flush()
        self._sync_children(model.id, artist)
        self.db.commit()
        self.db.refresh(model)
        return self._to_entity(model)

    async def find_by_id(self, artist_id: str) -> Optional[Artist]:
        model = self.db.query(ArtistModel).filter(ArtistModel.id == artist_id).first()
        return self._to_entity(model) if model else None

    def _base_query(self, category: Optional[str], genre: Optional[str], search: Optional[str]):
        q = self.db.query(ArtistModel).filter(ArtistModel.is_active.is_(True))
        if genre or category:
            q = q.join(GenreModel, ArtistModel.genre_id == GenreModel.id)
            if genre:
                q = q.filter(GenreModel.name == genre)
            if category:
                q = q.join(CategoryModel, GenreModel.category_id == CategoryModel.id).filter(
                    CategoryModel.name == category
                )
        if search:
            q = q.filter(or_(ArtistModel.name.ilike(f"%{search}%"), ArtistModel.description.ilike(f"%{search}%")))
        return q

    async def find_all(
        self,
        category: Optional[str] = None,
        genre: Optional[str] = None,
        search: Optional[str] = None,
        skip: int = 0,
        limit: int = 20,
    ) -> tuple[list[Artist], int]:
        q = self._base_query(category, genre, search)
        total = q.count()
        models = q.order_by(ArtistModel.created_at.desc()).offset(skip).limit(limit).all()
        return [self._to_entity(m) for m in models], total

    async def update(self, artist: Artist) -> Artist:
        model = self.db.query(ArtistModel).filter(ArtistModel.id == artist.id).first()
        if not model:
            raise ValueError("아티스트를 찾을 수 없습니다.")
        model.genre_id = artist.genre_id
        model.name = artist.name
        model.members = artist.members
        model.description = artist.description
        model.is_active = artist.is_active
        model.updated_at = artist.updated_at
        self._sync_children(model.id, artist)
        self.db.commit()
        self.db.refresh(model)
        return self._to_entity(model)

    async def delete(self, artist_id: str) -> None:
        self.db.query(ArtistModel).filter(ArtistModel.id == artist_id).delete()
        self.db.commit()

    async def increment_view(self, artist_id: str) -> None:
        self.db.query(ArtistModel).filter(ArtistModel.id == artist_id).update(
            {ArtistModel.view_count: ArtistModel.view_count + 1}
        )
        self.db.commit()

    async def find_all_admin(self, skip: int = 0, limit: int = 20) -> tuple[list[Artist], int]:
        q = self.db.query(ArtistModel)
        total = q.count()
        models = q.order_by(ArtistModel.created_at.desc()).offset(skip).limit(limit).all()
        return [self._to_entity(m) for m in models], total

    async def count_all(self) -> int:
        return self.db.query(ArtistModel).filter(ArtistModel.is_active.is_(True)).count()

    async def count_all_admin(self) -> int:
        return self.db.query(ArtistModel).count()
