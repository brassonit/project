"""카테고리/장르 Pydantic 스키마"""

from pydantic import BaseModel


class GenreResponse(BaseModel):
    id: int
    name: str


class CategoryResponse(BaseModel):
    id: int
    name: str
    genres: list[GenreResponse]


class CategoryListResponse(BaseModel):
    categories: list[CategoryResponse]
