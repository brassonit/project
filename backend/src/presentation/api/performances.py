"""공연 API 라우터"""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from src.application.use_cases.performance.create_performance import CreatePerformance
from src.application.use_cases.performance.delete_performance import DeletePerformance
from src.application.use_cases.performance.get_performance import GetPerformance
from src.application.use_cases.performance.list_performances import ListPerformances
from src.application.use_cases.performance.update_performance import UpdatePerformance
from src.infrastructure.database.connection import get_db
from src.infrastructure.repositories.performance_repository import (
    SqlAlchemyPerformanceRepository,
)
from src.presentation.dependencies.auth import require_admin
from src.presentation.schemas.performance import (
    PerformanceCreate,
    PerformanceListResponse,
    PerformanceResponse,
    PerformanceUpdate,
)

router = APIRouter(prefix="/api/performances", tags=["performances"])


def _get_repo(db: Session = Depends(get_db)) -> SqlAlchemyPerformanceRepository:
    return SqlAlchemyPerformanceRepository(db)


def _to_response(p) -> PerformanceResponse:
    return PerformanceResponse(
        id=p.id,
        title=p.title,
        description=p.description,
        event_date=p.event_date,
        venue=p.venue,
        image_url=p.image_url,
        artist_id=p.artist_id,
        is_featured=p.is_featured,
        created_at=p.created_at,
    )


@router.get("", response_model=PerformanceListResponse)
async def list_performances(
    featured: bool = Query(False, description="주요 공연만 조회"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    repo: SqlAlchemyPerformanceRepository = Depends(_get_repo),
):
    use_case = ListPerformances(performance_repo=repo)
    result = await use_case.execute(featured_only=featured, skip=skip, limit=limit)
    return PerformanceListResponse(
        performances=[_to_response(p) for p in result["performances"]],
        total=result["total"],
        skip=skip,
        limit=limit,
    )


@router.get("/featured", response_model=PerformanceListResponse)
async def list_featured_performances(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    repo: SqlAlchemyPerformanceRepository = Depends(_get_repo),
):
    use_case = ListPerformances(performance_repo=repo)
    result = await use_case.execute(featured_only=True, skip=skip, limit=limit)
    return PerformanceListResponse(
        performances=[_to_response(p) for p in result["performances"]],
        total=result["total"],
        skip=skip,
        limit=limit,
    )


@router.get("/{performance_id}", response_model=PerformanceResponse)
async def get_performance(
    performance_id: UUID,
    repo: SqlAlchemyPerformanceRepository = Depends(_get_repo),
):
    use_case = GetPerformance(performance_repo=repo)
    try:
        performance = await use_case.execute(performance_id=performance_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return _to_response(performance)


@router.post("", response_model=PerformanceResponse, status_code=status.HTTP_201_CREATED)
async def create_performance(
    request: PerformanceCreate,
    _admin: dict = Depends(require_admin),
    repo: SqlAlchemyPerformanceRepository = Depends(_get_repo),
):
    use_case = CreatePerformance(performance_repo=repo)
    try:
        performance = await use_case.execute(
            title=request.title,
            description=request.description,
            event_date=request.event_date,
            venue=request.venue,
            image_url=request.image_url,
            artist_id=request.artist_id,
            is_featured=request.is_featured,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return _to_response(performance)


@router.put("/{performance_id}", response_model=PerformanceResponse)
async def update_performance(
    performance_id: UUID,
    request: PerformanceUpdate,
    _admin: dict = Depends(require_admin),
    repo: SqlAlchemyPerformanceRepository = Depends(_get_repo),
):
    use_case = UpdatePerformance(performance_repo=repo)
    try:
        performance = await use_case.execute(
            performance_id=performance_id,
            title=request.title,
            description=request.description,
            event_date=request.event_date,
            venue=request.venue,
            image_url=request.image_url,
            artist_id=request.artist_id,
            is_featured=request.is_featured,
        )
    except ValueError as e:
        error_msg = str(e)
        if "찾을 수 없습니다" in error_msg:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error_msg)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error_msg)
    return _to_response(performance)


@router.delete("/{performance_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_performance(
    performance_id: UUID,
    _admin: dict = Depends(require_admin),
    repo: SqlAlchemyPerformanceRepository = Depends(_get_repo),
):
    use_case = DeletePerformance(performance_repo=repo)
    try:
        await use_case.execute(performance_id=performance_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
