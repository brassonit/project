"""Category Repository SQLAlchemy 구현"""

from typing import Optional

from sqlalchemy.orm import Session

from src.domain.entities.category import Category, Genre
from src.domain.repositories.category_repository import ICategoryRepository
from src.infrastructure.database.models import CategoryModel, GenreModel


class SqlAlchemyCategoryRepository(ICategoryRepository):
    def __init__(self, db: Session) -> None:
        self.db = db

    async def find_all(self) -> list[Category]:
        cats = self.db.query(CategoryModel).order_by(CategoryModel.sort_order).all()
        genres = self.db.query(GenreModel).order_by(GenreModel.sort_order).all()
        by_cat: dict[int, list[Genre]] = {}
        for g in genres:
            by_cat.setdefault(g.category_id, []).append(
                Genre(id=g.id, category_id=g.category_id, name=g.name, sort_order=g.sort_order)
            )
        return [
            Category(id=c.id, name=c.name, sort_order=c.sort_order, genres=by_cat.get(c.id, []))
            for c in cats
        ]

    async def find_genre_by_id(self, genre_id: int) -> Optional[Genre]:
        g = self.db.query(GenreModel).filter(GenreModel.id == genre_id).first()
        if not g:
            return None
        return Genre(id=g.id, category_id=g.category_id, name=g.name, sort_order=g.sort_order)
