"""관리자 관련 Pydantic 스키마"""

from pydantic import BaseModel


class ArtistStats(BaseModel):
    total: int
    active: int
    inactive: int


class PerformanceStats(BaseModel):
    total: int
    featured: int


class InquiryStats(BaseModel):
    total: int
    pending: int
    replied: int
    closed: int


class DashboardResponse(BaseModel):
    artists: ArtistStats
    performances: PerformanceStats
    inquiries: InquiryStats


class ImageUploadResponse(BaseModel):
    url: str
