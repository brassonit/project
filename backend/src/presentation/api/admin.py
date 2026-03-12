"""관리자 API 라우터"""

from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, status
from sqlalchemy.orm import Session

from src.application.use_cases.admin.get_dashboard import GetDashboard
from src.infrastructure.database.connection import get_db
from src.infrastructure.repositories.artist_repository import SqlAlchemyArtistRepository
from src.infrastructure.repositories.inquiry_repository import SqlAlchemyInquiryRepository
from src.infrastructure.repositories.performance_repository import (
    SqlAlchemyPerformanceRepository,
)
from src.infrastructure.storage.file_storage import FileStorage
from src.presentation.dependencies.auth import require_admin
from src.presentation.schemas.admin import DashboardResponse, ImageUploadResponse
from src.presentation.schemas.artist import ArtistListResponse, ArtistResponse

router = APIRouter(prefix="/api/admin", tags=["admin"])

file_storage = FileStorage()


def _get_repos(db: Session = Depends(get_db)):
    return {
        "artist": SqlAlchemyArtistRepository(db),
        "performance": SqlAlchemyPerformanceRepository(db),
        "inquiry": SqlAlchemyInquiryRepository(db),
    }


@router.get("/dashboard", response_model=DashboardResponse)
async def get_dashboard(
    _admin: dict = Depends(require_admin),
    repos: dict = Depends(_get_repos),
):
    """관리자 대시보드 통계"""
    use_case = GetDashboard(
        artist_repo=repos["artist"],
        performance_repo=repos["performance"],
        inquiry_repo=repos["inquiry"],
    )
    return await use_case.execute()


@router.get("/artists", response_model=ArtistListResponse)
async def list_artists_admin(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    _admin: dict = Depends(require_admin),
    repos: dict = Depends(_get_repos),
):
    """관리자용 아티스트 목록 (비활성 포함)"""
    artist_repo = repos["artist"]
    artists = await artist_repo.find_all_admin(skip=skip, limit=limit)
    total = await artist_repo.count_all_admin()

    def _to_response(a):
        return ArtistResponse(
            id=a.id,
            name=a.name,
            category=a.category.value,
            category_label=a.category.label_ko,
            description=a.description,
            profile_image_url=a.profile_image_url,
            gallery_images=a.gallery_images,
            is_active=a.is_active,
            created_at=a.created_at,
            updated_at=a.updated_at,
        )

    return ArtistListResponse(
        artists=[_to_response(a) for a in artists],
        total=total,
        skip=skip,
        limit=limit,
    )


@router.post("/upload/image", response_model=ImageUploadResponse)
async def upload_image(
    file: UploadFile,
    _admin: dict = Depends(require_admin),
):
    """이미지 업로드 (관리자 전용)"""
    try:
        url = await file_storage.save_image(file)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return ImageUploadResponse(url=url)
