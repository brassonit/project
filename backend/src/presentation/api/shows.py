"""기획공연 API 라우터"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.domain.entities.show import Show, ShowLineup, ShowTicket, ShowVideo
from src.infrastructure.database.connection import get_db
from src.infrastructure.repositories.show_repository import SqlAlchemyShowRepository
from src.presentation.dependencies.auth import require_admin
from src.presentation.schemas.show import (
    LineupItem,
    ShowCreate,
    ShowListResponse,
    ShowResponse,
    ShowUpdate,
    ShowVideoItem,
    TicketItem,
)

router = APIRouter(prefix="/api/shows", tags=["shows"])


def _get_repo(db: Session = Depends(get_db)) -> SqlAlchemyShowRepository:
    return SqlAlchemyShowRepository(db)


def _to_response(s: Show) -> ShowResponse:
    return ShowResponse(
        id=s.id,
        title=s.title,
        event_date=s.event_date,
        venue=s.venue,
        description=s.description,
        intro=s.intro,
        category_id=s.category_id,
        image_url=s.image_url,
        like_count=s.like_count,
        view_count=s.view_count,
        is_upcoming=s.is_upcoming(),
        lineup=[LineupItem(artist_id=lu.artist_id, artist_name=lu.artist_name) for lu in s.lineup],
        tickets=[TicketItem(label=t.label, url=t.url) for t in s.tickets],
        videos=[ShowVideoItem(video_url=v.video_url, title=v.title) for v in s.videos],
        created_at=s.created_at,
    )


@router.get("", response_model=ShowListResponse)
async def list_shows(repo: SqlAlchemyShowRepository = Depends(_get_repo)):
    shows, total = await repo.find_all()
    return ShowListResponse(shows=[_to_response(s) for s in shows], total=total)


@router.get("/{show_id}", response_model=ShowResponse)
async def get_show(show_id: str, repo: SqlAlchemyShowRepository = Depends(_get_repo)):
    show = await repo.find_by_id(show_id)
    if not show:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="공연을 찾을 수 없습니다.")
    await repo.increment_view(show_id)
    show.view_count += 1
    return _to_response(show)


@router.post("", response_model=ShowResponse, status_code=status.HTTP_201_CREATED)
async def create_show(
    request: ShowCreate,
    _admin: dict = Depends(require_admin),
    repo: SqlAlchemyShowRepository = Depends(_get_repo),
):
    try:
        show = Show(
            id=None,
            title=request.title,
            event_date=request.event_date,
            venue=request.venue,
            description=request.description,
            intro=request.intro,
            category_id=request.category_id,
            image_url=request.image_url,
            lineup=[ShowLineup(artist_id=aid) for aid in request.lineup_artist_ids],
            tickets=[ShowTicket(label=t.label, url=t.url) for t in request.tickets],
            videos=[ShowVideo(video_url=v.video_url, title=v.title) for v in request.videos],
        )
        return _to_response(await repo.save(show))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/{show_id}", response_model=ShowResponse)
async def update_show(
    show_id: str,
    request: ShowUpdate,
    _admin: dict = Depends(require_admin),
    repo: SqlAlchemyShowRepository = Depends(_get_repo),
):
    show = await repo.find_by_id(show_id)
    if not show:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="공연을 찾을 수 없습니다.")
    if request.title is not None:
        show.title = request.title
    if request.event_date is not None:
        show.event_date = request.event_date
    if request.venue is not None:
        show.venue = request.venue
    if request.description is not None:
        show.description = request.description
    if request.intro is not None:
        show.intro = request.intro
    if request.category_id is not None:
        show.category_id = request.category_id
    if request.image_url is not None:
        show.image_url = request.image_url
    if request.lineup_artist_ids is not None:
        show.lineup = [ShowLineup(artist_id=aid) for aid in request.lineup_artist_ids]
    if request.tickets is not None:
        show.tickets = [ShowTicket(label=t.label, url=t.url) for t in request.tickets]
    if request.videos is not None:
        show.videos = [ShowVideo(video_url=v.video_url, title=v.title) for v in request.videos]
    try:
        return _to_response(await repo.update(show))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{show_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_show(
    show_id: str,
    _admin: dict = Depends(require_admin),
    repo: SqlAlchemyShowRepository = Depends(_get_repo),
):
    show = await repo.find_by_id(show_id)
    if not show:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="공연을 찾을 수 없습니다.")
    await repo.delete(show_id)
