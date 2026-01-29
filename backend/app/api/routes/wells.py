from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import CurrentUser, get_db, get_pagination
from app.models.well import Well
from app.schemas.pagination import PaginatedResponse, PaginationParams
from app.schemas.well import WellCreate, WellRead, WellUpdate

router = APIRouter()


@router.get("", response_model=PaginatedResponse[WellRead])
async def list_wells(
    _current_user: CurrentUser,
    plate_id: UUID | None = None,
    db: AsyncSession = Depends(get_db),
    pagination: PaginationParams = Depends(get_pagination),
) -> PaginatedResponse[WellRead]:
    base_query = select(Well)
    if plate_id:
        base_query = base_query.where(Well.plate_id == plate_id)

    count_query = select(func.count()).select_from(base_query.subquery())
    total = await db.scalar(count_query) or 0

    query = base_query.offset(pagination.offset).limit(pagination.limit)
    result = await db.execute(query)
    wells = result.scalars().all()

    return PaginatedResponse.create(
        items=[WellRead.model_validate(w) for w in wells],
        total=total,
        params=pagination,
    )


@router.get("/{well_id}", response_model=WellRead)
async def get_well(
    well_id: UUID,
    _current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
) -> WellRead:
    query = select(Well).where(Well.id == well_id)
    result = await db.execute(query)
    well = result.scalar_one_or_none()

    if well is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Well not found")

    return WellRead.model_validate(well)


@router.post("", response_model=WellRead, status_code=status.HTTP_201_CREATED)
async def create_well(
    well_in: WellCreate,
    _current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
) -> WellRead:
    well = Well(**well_in.model_dump())
    db.add(well)
    await db.flush()
    await db.refresh(well)
    return WellRead.model_validate(well)


@router.patch("/{well_id}", response_model=WellRead)
async def update_well(
    well_id: UUID,
    well_in: WellUpdate,
    _current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
) -> WellRead:
    query = select(Well).where(Well.id == well_id)
    result = await db.execute(query)
    well = result.scalar_one_or_none()

    if well is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Well not found")

    update_data = well_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(well, field, value)

    await db.flush()
    await db.refresh(well)
    return WellRead.model_validate(well)


@router.delete("/{well_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_well(
    well_id: UUID,
    _current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
) -> None:
    query = select(Well).where(Well.id == well_id)
    result = await db.execute(query)
    well = result.scalar_one_or_none()

    if well is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Well not found")

    await db.delete(well)
