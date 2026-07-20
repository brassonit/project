"""카테고리/장르 API 라우터 — GNB·메가메뉴 구성"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.infrastructure.database.connection import get_db
from src.infrastructure.repositories.category_repository import SqlAlchemyCategoryRepository
from src.presentation.schemas.category import CategoryListResponse, CategoryResponse, GenreResponse

router = APIRouter(prefix="/api/categories", tags=["categories"])


@router.get("", response_model=CategoryListResponse)
async def list_categories(db: Session = Depends(get_db)):
    repo = SqlAlchemyCategoryRepository(db)
    categories = await repo.find_all()
    return CategoryListResponse(
        categories=[
            CategoryResponse(
                id=c.id,
                name=c.name,
                genres=[GenreResponse(id=g.id, name=g.name) for g in c.genres],
            )
            for c in categories
        ]
    )
