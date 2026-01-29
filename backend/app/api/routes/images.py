from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, get_pagination
from app.models.image import Image
from app.schemas.image import ImageCreate, ImageRead, ImageUpdate
from app.schemas.pagination import PaginatedResponse, PaginationParams

router = APIRouter()


@router.get("", response_model=PaginatedResponse[ImageRead])
async def list_images(
    well_id: UUID | None = None,
    db: AsyncSession = Depends(get_db),
    pagination: PaginationParams = Depends(get_pagination),
) -> PaginatedResponse[ImageRead]:
    base_query = select(Image)
    if well_id:
        base_query = base_query.where(Image.well_id == well_id)

    count_query = select(func.count()).select_from(base_query.subquery())
    total = await db.scalar(count_query) or 0

    query = base_query.offset(pagination.offset).limit(pagination.limit)
    result = await db.execute(query)
    images = result.scalars().all()

    return PaginatedResponse.create(
        items=[ImageRead.model_validate(i) for i in images],
        total=total,
        params=pagination,
    )


@router.get("/{image_id}", response_model=ImageRead)
async def get_image(
    image_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> ImageRead:
    query = select(Image).where(Image.id == image_id)
    result = await db.execute(query)
    image = result.scalar_one_or_none()

    if image is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")

    return ImageRead.model_validate(image)


@router.post("", response_model=ImageRead, status_code=status.HTTP_201_CREATED)
async def create_image(
    image_in: ImageCreate,
    db: AsyncSession = Depends(get_db),
) -> ImageRead:
    image = Image(**image_in.model_dump())
    db.add(image)
    await db.flush()
    await db.refresh(image)
    return ImageRead.model_validate(image)


@router.patch("/{image_id}", response_model=ImageRead)
async def update_image(
    image_id: UUID,
    image_in: ImageUpdate,
    db: AsyncSession = Depends(get_db),
) -> ImageRead:
    query = select(Image).where(Image.id == image_id)
    result = await db.execute(query)
    image = result.scalar_one_or_none()

    if image is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")

    update_data = image_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(image, field, value)

    await db.flush()
    await db.refresh(image)
    return ImageRead.model_validate(image)


@router.delete("/{image_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_image(
    image_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> None:
    query = select(Image).where(Image.id == image_id)
    result = await db.execute(query)
    image = result.scalar_one_or_none()

    if image is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")

    await db.delete(image)
