from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, get_pagination
from app.models.experiment import Experiment
from app.schemas.experiment import ExperimentCreate, ExperimentRead, ExperimentUpdate
from app.schemas.pagination import PaginatedResponse, PaginationParams

router = APIRouter()


@router.get("", response_model=PaginatedResponse[ExperimentRead])
async def list_experiments(
    project_id: UUID | None = None,
    db: AsyncSession = Depends(get_db),
    pagination: PaginationParams = Depends(get_pagination),
) -> PaginatedResponse[ExperimentRead]:
    base_query = select(Experiment)
    if project_id:
        base_query = base_query.where(Experiment.project_id == project_id)

    count_query = select(func.count()).select_from(base_query.subquery())
    total = await db.scalar(count_query) or 0

    query = base_query.offset(pagination.offset).limit(pagination.limit)
    result = await db.execute(query)
    experiments = result.scalars().all()

    return PaginatedResponse.create(
        items=[ExperimentRead.model_validate(e) for e in experiments],
        total=total,
        params=pagination,
    )


@router.get("/{experiment_id}", response_model=ExperimentRead)
async def get_experiment(
    experiment_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> ExperimentRead:
    query = select(Experiment).where(Experiment.id == experiment_id)
    result = await db.execute(query)
    experiment = result.scalar_one_or_none()

    if experiment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Experiment not found")

    return ExperimentRead.model_validate(experiment)


@router.post("", response_model=ExperimentRead, status_code=status.HTTP_201_CREATED)
async def create_experiment(
    experiment_in: ExperimentCreate,
    db: AsyncSession = Depends(get_db),
) -> ExperimentRead:
    experiment = Experiment(**experiment_in.model_dump())
    db.add(experiment)
    await db.flush()
    await db.refresh(experiment)
    return ExperimentRead.model_validate(experiment)


@router.patch("/{experiment_id}", response_model=ExperimentRead)
async def update_experiment(
    experiment_id: UUID,
    experiment_in: ExperimentUpdate,
    db: AsyncSession = Depends(get_db),
) -> ExperimentRead:
    query = select(Experiment).where(Experiment.id == experiment_id)
    result = await db.execute(query)
    experiment = result.scalar_one_or_none()

    if experiment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Experiment not found")

    update_data = experiment_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(experiment, field, value)

    await db.flush()
    await db.refresh(experiment)
    return ExperimentRead.model_validate(experiment)


@router.delete("/{experiment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_experiment(
    experiment_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> None:
    query = select(Experiment).where(Experiment.id == experiment_id)
    result = await db.execute(query)
    experiment = result.scalar_one_or_none()

    if experiment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Experiment not found")

    await db.delete(experiment)
