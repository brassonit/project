"""아티스트 API 라우터"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from src.domain.entities.artist import Artist, ArtistPortfolio, ArtistVideo
from src.infrastructure.database.connection import get_db
from src.infrastructure.repositories.artist_repository import SqlAlchemyArtistRepository
from src.presentation.dependencies.auth import require_admin
from src.presentation.schemas.artist import (
    ArtistCreate,
    ArtistListResponse,
    ArtistResponse,
    ArtistUpdate,
    PortfolioItem,
    VideoItem,
)

router = APIRouter(prefix="/api/artists", tags=["artists"])


def _get_repo(db: Session = Depends(get_db)) -> SqlAlchemyArtistRepository:
    return SqlAlchemyArtistRepository(db)


def _to_response(a: Artist) -> ArtistResponse:
    return ArtistResponse(
        id=a.id,
        genre_id=a.genre_id,
        genre_name=a.genre_name,
        category_name=a.category_name,
        name=a.name,
        members=a.members,
        description=a.description,
        like_count=a.like_count,
        view_count=a.view_count,
        is_active=a.is_active,
        images=a.images,
        portfolios=[PortfolioItem(tag=p.tag, year=p.year, content=p.content) for p in a.portfolios],
        videos=[VideoItem(video_url=v.video_url, title=v.title) for v in a.videos],
        created_at=a.created_at,
        updated_at=a.updated_at,
    )


@router.get("", response_model=ArtistListResponse)
async def list_artists(
    category: str | None = Query(None, description="카테고리명 (예: 대중가수)"),
    genre: str | None = Query(None, description="장르명 (예: 아이돌)"),
    search: str | None = Query(None, description="이름/소개 검색"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    repo: SqlAlchemyArtistRepository = Depends(_get_repo),
):
    artists, total = await repo.find_all(category=category, genre=genre, search=search, skip=skip, limit=limit)
    return ArtistListResponse(artists=[_to_response(a) for a in artists], total=total, skip=skip, limit=limit)


@router.get("/{artist_id}", response_model=ArtistResponse)
async def get_artist(artist_id: str, repo: SqlAlchemyArtistRepository = Depends(_get_repo)):
    artist = await repo.find_by_id(artist_id)
    if not artist or not artist.is_active:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="아티스트를 찾을 수 없습니다.")
    await repo.increment_view(artist_id)
    artist.view_count += 1
    return _to_response(artist)


@router.post("", response_model=ArtistResponse, status_code=status.HTTP_201_CREATED)
async def create_artist(
    request: ArtistCreate,
    _admin: dict = Depends(require_admin),
    repo: SqlAlchemyArtistRepository = Depends(_get_repo),
):
    try:
        artist = Artist(
            id=None,
            genre_id=request.genre_id,
            name=request.name,
            members=request.members,
            description=request.description,
            images=request.images,
            portfolios=[ArtistPortfolio(tag=p.tag, year=p.year, content=p.content) for p in request.portfolios],
            videos=[ArtistVideo(video_url=v.video_url, title=v.title) for v in request.videos],
        )
        return _to_response(await repo.save(artist))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/{artist_id}", response_model=ArtistResponse)
async def update_artist(
    artist_id: str,
    request: ArtistUpdate,
    _admin: dict = Depends(require_admin),
    repo: SqlAlchemyArtistRepository = Depends(_get_repo),
):
    artist = await repo.find_by_id(artist_id)
    if not artist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="아티스트를 찾을 수 없습니다.")
    if request.genre_id is not None:
        artist.genre_id = request.genre_id
    if request.name is not None:
        artist.name = request.name
    if request.members is not None:
        artist.members = request.members
    if request.description is not None:
        artist.description = request.description
    if request.images is not None:
        artist.images = request.images
    if request.portfolios is not None:
        artist.portfolios = [ArtistPortfolio(tag=p.tag, year=p.year, content=p.content) for p in request.portfolios]
    if request.videos is not None:
        artist.videos = [ArtistVideo(video_url=v.video_url, title=v.title) for v in request.videos]
    if request.is_active is not None:
        artist.is_active = request.is_active
    try:
        return _to_response(await repo.update(artist))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{artist_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_artist(
    artist_id: str,
    _admin: dict = Depends(require_admin),
    repo: SqlAlchemyArtistRepository = Depends(_get_repo),
):
    artist = await repo.find_by_id(artist_id)
    if not artist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="아티스트를 찾을 수 없습니다.")
    await repo.delete(artist_id)
