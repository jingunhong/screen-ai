from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, get_pagination
from app.models.analysis import Analysis
from app.schemas.analysis import AnalysisCreate, AnalysisRead, AnalysisUpdate
from app.schemas.pagination import PaginatedResponse, PaginationParams

router = APIRouter()


@router.get("", response_model=PaginatedResponse[AnalysisRead])
async def list_analyses(
    well_id: UUID | None = None,
    db: AsyncSession = Depends(get_db),
    pagination: PaginationParams = Depends(get_pagination),
) -> PaginatedResponse[AnalysisRead]:
    base_query = select(Analysis)
    if well_id:
        base_query = base_query.where(Analysis.well_id == well_id)

    count_query = select(func.count()).select_from(base_query.subquery())
    total = await db.scalar(count_query) or 0

    query = base_query.offset(pagination.offset).limit(pagination.limit)
    result = await db.execute(query)
    analyses = result.scalars().all()

    return PaginatedResponse.create(
        items=[AnalysisRead.model_validate(a) for a in analyses],
        total=total,
        params=pagination,
    )


@router.get("/{analysis_id}", response_model=AnalysisRead)
async def get_analysis(
    analysis_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> AnalysisRead:
    query = select(Analysis).where(Analysis.id == analysis_id)
    result = await db.execute(query)
    analysis = result.scalar_one_or_none()

    if analysis is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Analysis not found")

    return AnalysisRead.model_validate(analysis)


@router.post("", response_model=AnalysisRead, status_code=status.HTTP_201_CREATED)
async def create_analysis(
    analysis_in: AnalysisCreate,
    db: AsyncSession = Depends(get_db),
) -> AnalysisRead:
    analysis = Analysis(**analysis_in.model_dump())
    db.add(analysis)
    await db.flush()
    await db.refresh(analysis)
    return AnalysisRead.model_validate(analysis)


@router.patch("/{analysis_id}", response_model=AnalysisRead)
async def update_analysis(
    analysis_id: UUID,
    analysis_in: AnalysisUpdate,
    db: AsyncSession = Depends(get_db),
) -> AnalysisRead:
    query = select(Analysis).where(Analysis.id == analysis_id)
    result = await db.execute(query)
    analysis = result.scalar_one_or_none()

    if analysis is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Analysis not found")

    update_data = analysis_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(analysis, field, value)

    await db.flush()
    await db.refresh(analysis)
    return AnalysisRead.model_validate(analysis)


@router.delete("/{analysis_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_analysis(
    analysis_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> None:
    query = select(Analysis).where(Analysis.id == analysis_id)
    result = await db.execute(query)
    analysis = result.scalar_one_or_none()

    if analysis is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Analysis not found")

    await db.delete(analysis)
