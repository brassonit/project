"""아티스트 API 라우터"""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from src.application.use_cases.artist.create_artist import CreateArtist
from src.application.use_cases.artist.delete_artist import DeleteArtist
from src.application.use_cases.artist.get_artist import GetArtist
from src.application.use_cases.artist.list_artists import ListArtists
from src.application.use_cases.artist.update_artist import UpdateArtist
from src.infrastructure.database.connection import get_db
from src.infrastructure.repositories.artist_repository import SqlAlchemyArtistRepository
from src.presentation.dependencies.auth import require_admin
from src.presentation.schemas.artist import (
    ArtistCreate,
    ArtistListResponse,
    ArtistResponse,
    ArtistUpdate,
)

router = APIRouter(prefix="/api/artists", tags=["artists"])


def _get_artist_repo(db: Session = Depends(get_db)) -> SqlAlchemyArtistRepository:
    return SqlAlchemyArtistRepository(db)


def _to_response(artist) -> ArtistResponse:
    return ArtistResponse(
        id=artist.id,
        name=artist.name,
        category=artist.category.value,
        category_label=artist.category.label_ko,
        description=artist.description,
        profile_image_url=artist.profile_image_url,
        gallery_images=artist.gallery_images,
        is_active=artist.is_active,
        created_at=artist.created_at,
        updated_at=artist.updated_at,
    )


@router.get("", response_model=ArtistListResponse)
async def list_artists(
    category: str | None = Query(None, description="카테고리 필터"),
    search: str | None = Query(None, description="이름 검색"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    artist_repo: SqlAlchemyArtistRepository = Depends(_get_artist_repo),
):
    use_case = ListArtists(artist_repo=artist_repo)
    try:
        result = await use_case.execute(category=category, search=search, skip=skip, limit=limit)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return ArtistListResponse(
        artists=[_to_response(a) for a in result["artists"]],
        total=result["total"],
        skip=skip,
        limit=limit,
    )


@router.get("/{artist_id}", response_model=ArtistResponse)
async def get_artist(
    artist_id: UUID,
    artist_repo: SqlAlchemyArtistRepository = Depends(_get_artist_repo),
):
    use_case = GetArtist(artist_repo=artist_repo)
    try:
        artist = await use_case.execute(artist_id=artist_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return _to_response(artist)


@router.post("", response_model=ArtistResponse, status_code=status.HTTP_201_CREATED)
async def create_artist(
    request: ArtistCreate,
    _admin: dict = Depends(require_admin),
    artist_repo: SqlAlchemyArtistRepository = Depends(_get_artist_repo),
):
    use_case = CreateArtist(artist_repo=artist_repo)
    try:
        artist = await use_case.execute(
            name=request.name,
            category=request.category,
            description=request.description,
            profile_image_url=request.profile_image_url,
            gallery_images=request.gallery_images,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return _to_response(artist)


@router.put("/{artist_id}", response_model=ArtistResponse)
async def update_artist(
    artist_id: UUID,
    request: ArtistUpdate,
    _admin: dict = Depends(require_admin),
    artist_repo: SqlAlchemyArtistRepository = Depends(_get_artist_repo),
):
    use_case = UpdateArtist(artist_repo=artist_repo)
    try:
        artist = await use_case.execute(
            artist_id=artist_id,
            name=request.name,
            category=request.category,
            description=request.description,
            profile_image_url=request.profile_image_url,
            gallery_images=request.gallery_images,
            is_active=request.is_active,
        )
    except ValueError as e:
        error_msg = str(e)
        if "찾을 수 없습니다" in error_msg:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error_msg)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error_msg)
    return _to_response(artist)


@router.delete("/{artist_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_artist(
    artist_id: UUID,
    _admin: dict = Depends(require_admin),
    artist_repo: SqlAlchemyArtistRepository = Depends(_get_artist_repo),
):
    use_case = DeleteArtist(artist_repo=artist_repo)
    try:
        await use_case.execute(artist_id=artist_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
