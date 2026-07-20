"""찜리스트/장바구니 API 라우터 — 로그인 필수"""

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.infrastructure.database.connection import get_db
from src.infrastructure.repositories.interaction_repository import SqlAlchemyInteractionRepository
from src.presentation.dependencies.auth import get_current_user_token

router = APIRouter(prefix="/api/me", tags=["interactions"])


class IdListResponse(BaseModel):
    artist_ids: list[str]


class ShowIdListResponse(BaseModel):
    show_ids: list[str]


class ToggleResponse(BaseModel):
    active: bool  # True = 찜됨/담김


class IdsRequest(BaseModel):
    artist_ids: list[str]


class ShowIdsRequest(BaseModel):
    show_ids: list[str]


def _get_repo(db: Session = Depends(get_db)) -> SqlAlchemyInteractionRepository:
    return SqlAlchemyInteractionRepository(db)


@router.get("/wishlist", response_model=IdListResponse)
async def list_wishlist(
    payload: dict = Depends(get_current_user_token),
    repo: SqlAlchemyInteractionRepository = Depends(_get_repo),
):
    return IdListResponse(artist_ids=await repo.list_wishlist(payload["sub"]))


@router.post("/wishlist/{artist_id}/toggle", response_model=ToggleResponse)
async def toggle_wishlist(
    artist_id: str,
    payload: dict = Depends(get_current_user_token),
    repo: SqlAlchemyInteractionRepository = Depends(_get_repo),
):
    return ToggleResponse(active=await repo.toggle_wishlist(payload["sub"], artist_id))


@router.post("/wishlist/remove", response_model=IdListResponse)
async def remove_wishlist(
    request: IdsRequest,
    payload: dict = Depends(get_current_user_token),
    repo: SqlAlchemyInteractionRepository = Depends(_get_repo),
):
    """선택 삭제"""
    await repo.remove_wishlist(payload["sub"], request.artist_ids)
    return IdListResponse(artist_ids=await repo.list_wishlist(payload["sub"]))


@router.get("/show-wishlist", response_model=ShowIdListResponse)
async def list_show_wishlist(
    payload: dict = Depends(get_current_user_token),
    repo: SqlAlchemyInteractionRepository = Depends(_get_repo),
):
    return ShowIdListResponse(show_ids=await repo.list_show_wishlist(payload["sub"]))


@router.post("/show-wishlist/{show_id}/toggle", response_model=ToggleResponse)
async def toggle_show_wishlist(
    show_id: str,
    payload: dict = Depends(get_current_user_token),
    repo: SqlAlchemyInteractionRepository = Depends(_get_repo),
):
    """공연 상세 ♥ 찜 토글 — shows.like_count도 증감"""
    return ToggleResponse(active=await repo.toggle_show_wishlist(payload["sub"], show_id))


@router.post("/show-wishlist/remove", response_model=ShowIdListResponse)
async def remove_show_wishlist(
    request: ShowIdsRequest,
    payload: dict = Depends(get_current_user_token),
    repo: SqlAlchemyInteractionRepository = Depends(_get_repo),
):
    """찜리스트 공연 테이블 — 삭제/선택 삭제"""
    await repo.remove_show_wishlist(payload["sub"], request.show_ids)
    return ShowIdListResponse(show_ids=await repo.list_show_wishlist(payload["sub"]))


@router.get("/cart", response_model=IdListResponse)
async def list_cart(
    payload: dict = Depends(get_current_user_token),
    repo: SqlAlchemyInteractionRepository = Depends(_get_repo),
):
    return IdListResponse(artist_ids=await repo.list_cart(payload["sub"]))


@router.post("/cart/{artist_id}/toggle", response_model=ToggleResponse)
async def toggle_cart(
    artist_id: str,
    payload: dict = Depends(get_current_user_token),
    repo: SqlAlchemyInteractionRepository = Depends(_get_repo),
):
    return ToggleResponse(active=await repo.toggle_cart(payload["sub"], artist_id))


@router.post("/cart/add", response_model=IdListResponse)
async def add_cart(
    request: IdsRequest,
    payload: dict = Depends(get_current_user_token),
    repo: SqlAlchemyInteractionRepository = Depends(_get_repo),
):
    """찜리스트 → 총 n팀 아티스트 장바구니 담기"""
    await repo.add_cart(payload["sub"], request.artist_ids)
    return IdListResponse(artist_ids=await repo.list_cart(payload["sub"]))


@router.post("/cart/remove", response_model=IdListResponse)
async def remove_cart(
    request: IdsRequest,
    payload: dict = Depends(get_current_user_token),
    repo: SqlAlchemyInteractionRepository = Depends(_get_repo),
):
    """선택 삭제"""
    await repo.remove_cart(payload["sub"], request.artist_ids)
    return IdListResponse(artist_ids=await repo.list_cart(payload["sub"]))
