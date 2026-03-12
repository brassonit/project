"""공연 관련 Pydantic 스키마"""

from datetime import date, datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class PerformanceCreate(BaseModel):
    title: str
    description: str
    event_date: date
    venue: str
    image_url: Optional[str] = None
    artist_id: Optional[UUID] = None
    is_featured: bool = False


class PerformanceUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    event_date: Optional[date] = None
    venue: Optional[str] = None
    image_url: Optional[str] = None
    artist_id: Optional[UUID] = None
    is_featured: Optional[bool] = None


class PerformanceResponse(BaseModel):
    id: UUID
    title: str
    description: str
    event_date: date
    venue: str
    image_url: Optional[str]
    artist_id: Optional[UUID]
    is_featured: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class PerformanceListResponse(BaseModel):
    performances: list[PerformanceResponse]
    total: int
    skip: int
    limit: int
