"""관리자 관련 Pydantic 스키마"""

from pydantic import BaseModel


class ArtistStats(BaseModel):
    total: int
    active: int
    inactive: int


class ShowStats(BaseModel):
    total: int
    upcoming: int
    past: int


class QuoteStats(BaseModel):
    total: int
    received: int
    replied: int


class DashboardResponse(BaseModel):
    artists: ArtistStats
    shows: ShowStats
    quotes: QuoteStats


class ImageUploadResponse(BaseModel):
    url: str
