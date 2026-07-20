"""견적 API 라우터 — 견적 요청(로그인)/견적 문의(비로그인)"""

import re
from typing import Optional

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query, UploadFile, status
from sqlalchemy.orm import Session

from src.domain.entities.quote import Quote, QuoteArtist, QuoteAttachment, QuoteStatus
from src.infrastructure.database.connection import get_db
from src.infrastructure.email.email_service import EmailService
from src.infrastructure.repositories.interaction_repository import SqlAlchemyInteractionRepository
from src.infrastructure.repositories.quote_repository import SqlAlchemyQuoteRepository
from src.infrastructure.repositories.user_repository import SqlAlchemyUserRepository
from src.infrastructure.storage.file_storage import FileStorage
from src.infrastructure.storage.object_storage import OciObjectStorage
from src.presentation.dependencies.auth import (
    get_current_user_token,
    get_optional_user_token,
    require_admin,
)
from src.presentation.schemas.quote import (
    AttachmentItem,
    QuoteArtistItem,
    QuoteCreate,
    QuoteListResponse,
    QuoteReply,
    QuoteResponse,
)

router = APIRouter(prefix="/api/quotes", tags=["quotes"])

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")

file_storage = FileStorage()
# 오라클 Object Storage(S3 호환) — 설정돼 있으면 첨부파일을 버킷에 저장, 아니면 로컬 폴백
oci_storage = OciObjectStorage() if OciObjectStorage.is_configured() else None


def _get_repo(db: Session = Depends(get_db)) -> SqlAlchemyQuoteRepository:
    return SqlAlchemyQuoteRepository(db)


def _to_response(q: Quote) -> QuoteResponse:
    return QuoteResponse(
        id=q.id,
        user_id=q.user_id,
        email=q.email,
        name=q.name,
        phone=q.phone,
        event_title=q.event_title,
        event_date=q.event_date,
        event_date_text=q.event_date_text,
        region=q.region,
        content=q.content,
        show_id=q.show_id,
        show_title=q.show_title,
        status=q.status.value,
        quote_file_url=q.quote_file_url,
        replied_at=q.replied_at,
        artists=[QuoteArtistItem(artist_id=a.artist_id, artist_name=a.artist_name) for a in q.artists],
        attachments=[AttachmentItem(file_name=a.file_name, file_url=a.file_url) for a in q.attachments],
        created_at=q.created_at,
    )


@router.post("/attachments", response_model=list[AttachmentItem])
async def upload_attachments(files: list[UploadFile]):
    """견적 첨부파일 업로드 — 견적 생성 전에 호출, 비로그인 문의도 허용"""
    result: list[AttachmentItem] = []
    for f in files:
        try:
            if oci_storage:
                url = await oci_storage.save_attachment(f)
            else:
                url = await file_storage.save_attachment(f)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        result.append(AttachmentItem(file_name=f.filename or "첨부파일", file_url=url))
    return result


@router.post("", response_model=QuoteResponse, status_code=status.HTTP_201_CREATED)
async def create_quote(
    request: QuoteCreate,
    background_tasks: BackgroundTasks,
    payload: Optional[dict] = Depends(get_optional_user_token),
    db: Session = Depends(get_db),
    repo: SqlAlchemyQuoteRepository = Depends(_get_repo),
):
    """견적 생성 — 로그인 시 견적 요청, 비로그인 시 견적 문의(이메일 필수)"""
    user_repo = SqlAlchemyUserRepository(db)
    user = await user_repo.find_by_id(payload["sub"]) if payload else None

    if user:
        email = user.email
    else:
        email = (request.email or "").strip()
        if not EMAIL_REGEX.match(email):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="유효하지 않은 이메일 형식입니다.")

    try:
        quote = Quote(
            id=None,
            user_id=user.id if user else None,
            email=email,
            name=request.name,
            phone=request.phone,
            event_title=request.event_title,
            event_date=request.event_date,
            event_date_text=request.event_date_text,
            region=request.region,
            content=request.content,
            show_id=request.show_id,
            artists=[QuoteArtist(artist_id=aid) for aid in request.artist_ids],
            attachments=[QuoteAttachment(file_name=a.file_name, file_url=a.file_url) for a in request.attachments],
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    saved = await repo.save(quote)

    # 발송된 아티스트는 장바구니에서 제거
    if user and request.artist_ids:
        interaction_repo = SqlAlchemyInteractionRepository(db)
        await interaction_repo.remove_cart(user.id, request.artist_ids)

    # 회원정보의 이름/전화번호 업데이트 체크 시
    if user and request.update_profile:
        user.update_profile(name=request.name.strip(), phone=request.phone.strip())
        await user_repo.update(user)

    # 등록 내용 + 첨부파일을 관리자 메일로 발송 (응답을 막지 않도록 백그라운드)
    background_tasks.add_task(EmailService().send_quote_notification, saved)

    return _to_response(saved)


@router.get("/me", response_model=QuoteListResponse)
async def list_my_quotes(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    payload: dict = Depends(get_current_user_token),
    repo: SqlAlchemyQuoteRepository = Depends(_get_repo),
):
    """견적내역 (최신순)"""
    quotes, total = await repo.find_by_user(payload["sub"], skip=skip, limit=limit)
    return QuoteListResponse(quotes=[_to_response(q) for q in quotes], total=total, skip=skip, limit=limit)


@router.get("", response_model=QuoteListResponse)
async def list_quotes_admin(
    status_filter: str | None = Query(None, alias="status", description="received | replied"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    _admin: dict = Depends(require_admin),
    repo: SqlAlchemyQuoteRepository = Depends(_get_repo),
):
    st = None
    if status_filter:
        try:
            st = QuoteStatus(status_filter)
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="유효하지 않은 상태입니다.")
    quotes, total = await repo.find_all(status=st, skip=skip, limit=limit)
    return QuoteListResponse(quotes=[_to_response(q) for q in quotes], total=total, skip=skip, limit=limit)


@router.get("/{quote_id}", response_model=QuoteResponse)
async def get_quote(
    quote_id: str,
    payload: dict = Depends(get_current_user_token),
    repo: SqlAlchemyQuoteRepository = Depends(_get_repo),
):
    quote = await repo.find_by_id(quote_id)
    if not quote:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="견적을 찾을 수 없습니다.")
    if payload.get("role") != "admin" and quote.user_id != payload["sub"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="접근 권한이 없습니다.")
    return _to_response(quote)


@router.post("/{quote_id}/reply", response_model=QuoteResponse)
async def reply_quote(
    quote_id: str,
    request: QuoteReply,
    _admin: dict = Depends(require_admin),
    repo: SqlAlchemyQuoteRepository = Depends(_get_repo),
):
    """회신완료 처리 + 견적서 파일 등록"""
    quote = await repo.find_by_id(quote_id)
    if not quote:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="견적을 찾을 수 없습니다.")
    quote.reply(quote_file_url=request.quote_file_url)
    return _to_response(await repo.update(quote))


@router.delete("/{quote_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_quote(
    quote_id: str,
    _admin: dict = Depends(require_admin),
    repo: SqlAlchemyQuoteRepository = Depends(_get_repo),
):
    quote = await repo.find_by_id(quote_id)
    if not quote:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="견적을 찾을 수 없습니다.")
    await repo.delete(quote_id)
