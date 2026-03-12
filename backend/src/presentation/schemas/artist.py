"""아티스트 관련 Pydantic 스키마"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class ArtistCreate(BaseModel):
    name: str
    category: str
    description: str
    profile_image_url: Optional[str] = None
    gallery_images: list[str] = []


class ArtistUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    profile_image_url: Optional[str] = None
    gallery_images: Optional[list[str]] = None
    is_active: Optional[bool] = None


class ArtistResponse(BaseModel):
    id: UUID
    name: str
    category: str
    category_label: str
    description: str
    profile_image_url: Optional[str]
    gallery_images: list[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ArtistListResponse(BaseModel):
    artists: list[ArtistResponse]
    total: int
    skip: int
    limit: int
