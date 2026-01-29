from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, get_pagination
from app.models.compound import Compound
from app.schemas.compound import CompoundCreate, CompoundRead, CompoundUpdate
from app.schemas.pagination import PaginatedResponse, PaginationParams

router = APIRouter()


@router.get("", response_model=PaginatedResponse[CompoundRead])
async def list_compounds(
    db: AsyncSession = Depends(get_db),
    pagination: PaginationParams = Depends(get_pagination),
) -> PaginatedResponse[CompoundRead]:
    count_query = select(func.count()).select_from(Compound)
    total = await db.scalar(count_query) or 0

    query = select(Compound).offset(pagination.offset).limit(pagination.limit)
    result = await db.execute(query)
    compounds = result.scalars().all()

    return PaginatedResponse.create(
        items=[CompoundRead.model_validate(c) for c in compounds],
        total=total,
        params=pagination,
    )


@router.get("/{compound_id}", response_model=CompoundRead)
async def get_compound(
    compound_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> CompoundRead:
    query = select(Compound).where(Compound.id == compound_id)
    result = await db.execute(query)
    compound = result.scalar_one_or_none()

    if compound is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Compound not found")

    return CompoundRead.model_validate(compound)


@router.post("", response_model=CompoundRead, status_code=status.HTTP_201_CREATED)
async def create_compound(
    compound_in: CompoundCreate,
    db: AsyncSession = Depends(get_db),
) -> CompoundRead:
    compound = Compound(**compound_in.model_dump())
    db.add(compound)
    await db.flush()
    await db.refresh(compound)
    return CompoundRead.model_validate(compound)


@router.patch("/{compound_id}", response_model=CompoundRead)
async def update_compound(
    compound_id: UUID,
    compound_in: CompoundUpdate,
    db: AsyncSession = Depends(get_db),
) -> CompoundRead:
    query = select(Compound).where(Compound.id == compound_id)
    result = await db.execute(query)
    compound = result.scalar_one_or_none()

    if compound is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Compound not found")

    update_data = compound_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(compound, field, value)

    await db.flush()
    await db.refresh(compound)
    return CompoundRead.model_validate(compound)


@router.delete("/{compound_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_compound(
    compound_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> None:
    query = select(Compound).where(Compound.id == compound_id)
    result = await db.execute(query)
    compound = result.scalar_one_or_none()

    if compound is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Compound not found")

    await db.delete(compound)
