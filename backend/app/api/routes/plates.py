from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, get_pagination
from app.models.plate import Plate
from app.schemas.pagination import PaginatedResponse, PaginationParams
from app.schemas.plate import PlateCreate, PlateRead, PlateUpdate

router = APIRouter()


@router.get("", response_model=PaginatedResponse[PlateRead])
async def list_plates(
    experiment_id: UUID | None = None,
    db: AsyncSession = Depends(get_db),
    pagination: PaginationParams = Depends(get_pagination),
) -> PaginatedResponse[PlateRead]:
    base_query = select(Plate)
    if experiment_id:
        base_query = base_query.where(Plate.experiment_id == experiment_id)

    count_query = select(func.count()).select_from(base_query.subquery())
    total = await db.scalar(count_query) or 0

    query = base_query.offset(pagination.offset).limit(pagination.limit)
    result = await db.execute(query)
    plates = result.scalars().all()

    return PaginatedResponse.create(
        items=[PlateRead.model_validate(p) for p in plates],
        total=total,
        params=pagination,
    )


@router.get("/{plate_id}", response_model=PlateRead)
async def get_plate(
    plate_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> PlateRead:
    query = select(Plate).where(Plate.id == plate_id)
    result = await db.execute(query)
    plate = result.scalar_one_or_none()

    if plate is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plate not found")

    return PlateRead.model_validate(plate)


@router.post("", response_model=PlateRead, status_code=status.HTTP_201_CREATED)
async def create_plate(
    plate_in: PlateCreate,
    db: AsyncSession = Depends(get_db),
) -> PlateRead:
    plate = Plate(**plate_in.model_dump())
    db.add(plate)
    await db.flush()
    await db.refresh(plate)
    return PlateRead.model_validate(plate)


@router.patch("/{plate_id}", response_model=PlateRead)
async def update_plate(
    plate_id: UUID,
    plate_in: PlateUpdate,
    db: AsyncSession = Depends(get_db),
) -> PlateRead:
    query = select(Plate).where(Plate.id == plate_id)
    result = await db.execute(query)
    plate = result.scalar_one_or_none()

    if plate is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plate not found")

    update_data = plate_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(plate, field, value)

    await db.flush()
    await db.refresh(plate)
    return PlateRead.model_validate(plate)


@router.delete("/{plate_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_plate(
    plate_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> None:
    query = select(Plate).where(Plate.id == plate_id)
    result = await db.execute(query)
    plate = result.scalar_one_or_none()

    if plate is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plate not found")

    await db.delete(plate)
