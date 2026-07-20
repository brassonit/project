"""관리자 API 라우터"""

from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, status
from sqlalchemy.orm import Session

from src.application.use_cases.admin.get_dashboard import GetDashboard
from src.infrastructure.database.connection import get_db
from src.infrastructure.repositories.artist_repository import SqlAlchemyArtistRepository
from src.infrastructure.repositories.quote_repository import SqlAlchemyQuoteRepository
from src.infrastructure.repositories.show_repository import SqlAlchemyShowRepository
from src.infrastructure.storage.file_storage import FileStorage
from src.presentation.api.artists import _to_response as _artist_to_response
from src.presentation.dependencies.auth import require_admin
from src.presentation.schemas.admin import DashboardResponse, ImageUploadResponse
from src.presentation.schemas.artist import ArtistListResponse

router = APIRouter(prefix="/api/admin", tags=["admin"])

file_storage = FileStorage()


@router.get("/dashboard", response_model=DashboardResponse)
async def get_dashboard(
    _admin: dict = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """관리자 대시보드 통계"""
    use_case = GetDashboard(
        artist_repo=SqlAlchemyArtistRepository(db),
        show_repo=SqlAlchemyShowRepository(db),
        quote_repo=SqlAlchemyQuoteRepository(db),
    )
    return await use_case.execute()


@router.get("/artists", response_model=ArtistListResponse)
async def list_artists_admin(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    _admin: dict = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """관리자용 아티스트 목록 (비활성 포함)"""
    repo = SqlAlchemyArtistRepository(db)
    artists, total = await repo.find_all_admin(skip=skip, limit=limit)
    return ArtistListResponse(
        artists=[_artist_to_response(a) for a in artists],
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
