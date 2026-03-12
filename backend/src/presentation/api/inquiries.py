"""문의 API 라우터"""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from src.application.use_cases.inquiry.create_inquiry import CreateInquiry
from src.application.use_cases.inquiry.delete_inquiry import DeleteInquiry
from src.application.use_cases.inquiry.list_inquiries import ListInquiries
from src.application.use_cases.inquiry.reply_inquiry import ReplyInquiry
from src.application.use_cases.inquiry.update_inquiry_status import UpdateInquiryStatus
from src.infrastructure.database.connection import get_db
from src.infrastructure.repositories.inquiry_repository import (
    SqlAlchemyInquiryRepository,
)
from src.presentation.dependencies.auth import require_admin
from src.presentation.schemas.inquiry import (
    InquiryCreate,
    InquiryListResponse,
    InquiryReply,
    InquiryResponse,
    InquiryStatusUpdate,
)

router = APIRouter(prefix="/api/inquiries", tags=["inquiries"])


def _get_repo(db: Session = Depends(get_db)) -> SqlAlchemyInquiryRepository:
    return SqlAlchemyInquiryRepository(db)


def _to_response(inq) -> InquiryResponse:
    return InquiryResponse(
        id=inq.id,
        name=inq.name,
        email=inq.email,
        phone=inq.phone,
        subject=inq.subject,
        message=inq.message,
        status=inq.status.value,
        admin_reply=inq.admin_reply,
        created_at=inq.created_at,
    )


@router.post("", response_model=InquiryResponse, status_code=status.HTTP_201_CREATED)
async def create_inquiry(
    request: InquiryCreate,
    repo: SqlAlchemyInquiryRepository = Depends(_get_repo),
):
    """문의 제출 (비로그인 가능)"""
    use_case = CreateInquiry(inquiry_repo=repo)
    try:
        inquiry = await use_case.execute(
            name=request.name,
            email=request.email,
            subject=request.subject,
            message=request.message,
            phone=request.phone,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return _to_response(inquiry)


@router.get("", response_model=InquiryListResponse)
async def list_inquiries(
    status_filter: str | None = Query(None, alias="status", description="상태 필터"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    _admin: dict = Depends(require_admin),
    repo: SqlAlchemyInquiryRepository = Depends(_get_repo),
):
    """문의 목록 (관리자 전용)"""
    use_case = ListInquiries(inquiry_repo=repo)
    try:
        result = await use_case.execute(status=status_filter, skip=skip, limit=limit)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return InquiryListResponse(
        inquiries=[_to_response(i) for i in result["inquiries"]],
        total=result["total"],
        skip=skip,
        limit=limit,
    )


@router.get("/{inquiry_id}", response_model=InquiryResponse)
async def get_inquiry(
    inquiry_id: UUID,
    _admin: dict = Depends(require_admin),
    repo: SqlAlchemyInquiryRepository = Depends(_get_repo),
):
    """문의 상세 (관리자 전용)"""

    inquiry = await repo.find_by_id(inquiry_id)
    if not inquiry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="문의를 찾을 수 없습니다.")
    return _to_response(inquiry)


@router.patch("/{inquiry_id}/reply", response_model=InquiryResponse)
async def reply_inquiry(
    inquiry_id: UUID,
    request: InquiryReply,
    _admin: dict = Depends(require_admin),
    repo: SqlAlchemyInquiryRepository = Depends(_get_repo),
):
    """문의 답변 (관리자 전용)"""
    use_case = ReplyInquiry(inquiry_repo=repo)
    try:
        inquiry = await use_case.execute(inquiry_id=inquiry_id, reply_text=request.reply)
    except ValueError as e:
        error_msg = str(e)
        if "찾을 수 없습니다" in error_msg:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error_msg)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error_msg)
    return _to_response(inquiry)


@router.patch("/{inquiry_id}/status", response_model=InquiryResponse)
async def update_inquiry_status(
    inquiry_id: UUID,
    request: InquiryStatusUpdate,
    _admin: dict = Depends(require_admin),
    repo: SqlAlchemyInquiryRepository = Depends(_get_repo),
):
    """문의 상태 변경 (관리자 전용)"""
    use_case = UpdateInquiryStatus(inquiry_repo=repo)
    try:
        inquiry = await use_case.execute(inquiry_id=inquiry_id, status=request.status)
    except ValueError as e:
        error_msg = str(e)
        if "찾을 수 없습니다" in error_msg:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error_msg)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error_msg)
    return _to_response(inquiry)


@router.delete("/{inquiry_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_inquiry(
    inquiry_id: UUID,
    _admin: dict = Depends(require_admin),
    repo: SqlAlchemyInquiryRepository = Depends(_get_repo),
):
    """문의 삭제 (관리자 전용)"""
    use_case = DeleteInquiry(inquiry_repo=repo)
    try:
        await use_case.execute(inquiry_id=inquiry_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
