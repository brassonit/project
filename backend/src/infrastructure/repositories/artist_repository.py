"""Artist Repository SQLAlchemy 구현"""

from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from src.domain.entities.artist import Artist
from src.domain.repositories.artist_repository import IArtistRepository
from src.domain.value_objects.artist_category import ArtistCategory
from src.infrastructure.database.models import ArtistModel


class SqlAlchemyArtistRepository(IArtistRepository):
    def __init__(self, db: Session) -> None:
        self.db = db

    def _to_entity(self, model: ArtistModel) -> Artist:
        return Artist(
            id=model.id,
            name=model.name,
            category=ArtistCategory(model.category),
            description=model.description,
            profile_image_url=model.profile_image_url,
            gallery_images=model.gallery_images or [],
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def _to_model(self, entity: Artist) -> ArtistModel:
        return ArtistModel(
            id=entity.id,
            name=entity.name,
            category=entity.category.value,
            description=entity.description,
            profile_image_url=entity.profile_image_url,
            gallery_images=entity.gallery_images,
            is_active=entity.is_active,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    async def save(self, artist: Artist) -> Artist:
        model = self._to_model(artist)
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return self._to_entity(model)

    async def find_by_id(self, artist_id: UUID) -> Optional[Artist]:
        model = self.db.query(ArtistModel).filter(ArtistModel.id == artist_id).first()
        return self._to_entity(model) if model else None

    async def find_all(self, skip: int = 0, limit: int = 20) -> list[Artist]:
        models = (
            self.db.query(ArtistModel)
            .filter(ArtistModel.is_active.is_(True))
            .order_by(ArtistModel.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        return [self._to_entity(m) for m in models]

    async def find_by_category(self, category: ArtistCategory, skip: int = 0, limit: int = 20) -> list[Artist]:
        models = (
            self.db.query(ArtistModel)
            .filter(ArtistModel.category == category.value, ArtistModel.is_active.is_(True))
            .order_by(ArtistModel.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        return [self._to_entity(m) for m in models]

    async def search(self, query: str, skip: int = 0, limit: int = 20) -> list[Artist]:
        models = (
            self.db.query(ArtistModel)
            .filter(
                ArtistModel.is_active.is_(True),
                ArtistModel.name.ilike(f"%{query}%"),
            )
            .order_by(ArtistModel.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        return [self._to_entity(m) for m in models]

    async def update(self, artist: Artist) -> Artist:
        model = self.db.query(ArtistModel).filter(ArtistModel.id == artist.id).first()
        if not model:
            raise ValueError("아티스트를 찾을 수 없습니다.")
        model.name = artist.name
        model.category = artist.category.value
        model.description = artist.description
        model.profile_image_url = artist.profile_image_url
        model.gallery_images = artist.gallery_images
        model.is_active = artist.is_active
        model.updated_at = artist.updated_at
        self.db.commit()
        self.db.refresh(model)
        return self._to_entity(model)

    async def delete(self, artist_id: UUID) -> None:
        self.db.query(ArtistModel).filter(ArtistModel.id == artist_id).delete()
        self.db.commit()

    async def count_all(self) -> int:
        return self.db.query(ArtistModel).filter(ArtistModel.is_active.is_(True)).count()

    async def count_by_category(self, category: ArtistCategory) -> int:
        return (
            self.db.query(ArtistModel)
            .filter(ArtistModel.category == category.value, ArtistModel.is_active.is_(True))
            .count()
        )

    async def count_search(self, query: str) -> int:
        return (
            self.db.query(ArtistModel)
            .filter(
                ArtistModel.is_active.is_(True),
                ArtistModel.name.ilike(f"%{query}%"),
            )
            .count()
        )

    async def find_all_admin(self, skip: int = 0, limit: int = 20) -> list[Artist]:
        models = self.db.query(ArtistModel).order_by(ArtistModel.created_at.desc()).offset(skip).limit(limit).all()
        return [self._to_entity(m) for m in models]

    async def count_all_admin(self) -> int:
        return self.db.query(ArtistModel).count()
