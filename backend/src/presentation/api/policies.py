"""이용약관/개인정보취급방침 API 라우터 — 버전(시행일)별 콘텐츠 조회"""

from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from src.domain.entities.policy import PolicyType
from src.infrastructure.database.connection import get_db
from src.infrastructure.repositories.policy_repository import SqlAlchemyPolicyRepository
from src.presentation.schemas.policy import PolicyResponse

router = APIRouter(prefix="/api/policies", tags=["policies"])


@router.get("/{policy_type}", response_model=PolicyResponse)
async def get_policy(
    policy_type: PolicyType,
    effective_date: Optional[date] = Query(None, description="미지정 시 최신 버전"),
    db: Session = Depends(get_db),
):
    repo = SqlAlchemyPolicyRepository(db)
    policy = await repo.find_by_type(policy_type, effective_date)
    if not policy:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="등록된 버전이 없습니다.")
    versions = await repo.find_versions(policy_type)
    return PolicyResponse(
        policy_type=policy.policy_type.value,
        effective_date=policy.effective_date,
        content=policy.content,
        versions=versions,
    )
