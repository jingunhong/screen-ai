from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from app.core.deps import DbSession, CurrentUser
from app.models import Project, Experiment, Plate, Well, Image
from app.schemas import WellCreate, WellUpdate, WellResponse, WellList, WellWithCompound
from app.schemas.image import ImageThumbnail

router = APIRouter(prefix="/plates/{plate_id}/wells", tags=["wells"])


async def get_plate_or_404(db, plate_id: str, user_id: str) -> Plate:
    """Helper to get plate and verify ownership through experiment and project."""
    result = await db.execute(
        select(Plate)
        .join(Experiment)
        .join(Project)
        .where(Plate.id == plate_id, Project.owner_id == user_id)
    )
    plate = result.scalar_one_or_none()
    if not plate:
        raise HTTPException(status_code=404, detail="Plate not found")
    return plate


@router.get("", response_model=WellList)
async def list_wells(
    plate_id: str,
    db: DbSession,
    current_user: CurrentUser,
    skip: int = 0,
    limit: int = 500,
):
    """List all wells in a plate."""
    await get_plate_or_404(db, plate_id, current_user.id)

    # Count total
    count_query = select(func.count(Well.id)).where(Well.plate_id == plate_id)
    total = (await db.execute(count_query)).scalar()

    # Get wells
    query = (
        select(Well)
        .where(Well.plate_id == plate_id)
        .order_by(Well.row, Well.column)
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(query)
    wells = result.scalars().all()

    items = [
        WellResponse(
            id=well.id,
            plate_id=well.plate_id,
            row=well.row,
            column=well.column,
            compound_id=well.compound_id,
            concentration=well.concentration,
            concentration_unit=well.concentration_unit,
            well_type=well.well_type,
            created_at=well.created_at,
            updated_at=well.updated_at,
            row_label=well.row_label,
            column_label=well.column_label,
            position=well.position,
        )
        for well in wells
    ]

    return WellList(items=items, total=total, skip=skip, limit=limit)


@router.post("", response_model=WellResponse, status_code=status.HTTP_201_CREATED)
async def create_well(
    plate_id: str,
    well_in: WellCreate,
    db: DbSession,
    current_user: CurrentUser,
):
    """Create a new well in a plate."""
    plate = await get_plate_or_404(db, plate_id, current_user.id)

    # Validate row/column
    if well_in.row < 0 or well_in.row >= plate.rows:
        raise HTTPException(status_code=400, detail=f"Row must be between 0 and {plate.rows - 1}")
    if well_in.column < 0 or well_in.column >= plate.columns:
        raise HTTPException(
            status_code=400, detail=f"Column must be between 0 and {plate.columns - 1}"
        )

    # Check for duplicate position
    existing = await db.execute(
        select(Well).where(
            Well.plate_id == plate_id, Well.row == well_in.row, Well.column == well_in.column
        )
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Well already exists at this position")

    well = Well(
        plate_id=plate_id,
        row=well_in.row,
        column=well_in.column,
        compound_id=well_in.compound_id,
        concentration=well_in.concentration,
        concentration_unit=well_in.concentration_unit,
        well_type=well_in.well_type,
    )
    db.add(well)
    await db.commit()
    await db.refresh(well)

    return WellResponse(
        id=well.id,
        plate_id=well.plate_id,
        row=well.row,
        column=well.column,
        compound_id=well.compound_id,
        concentration=well.concentration,
        concentration_unit=well.concentration_unit,
        well_type=well.well_type,
        created_at=well.created_at,
        updated_at=well.updated_at,
        row_label=well.row_label,
        column_label=well.column_label,
        position=well.position,
    )


@router.get("/{well_id}", response_model=WellWithCompound)
async def get_well(
    plate_id: str,
    well_id: str,
    db: DbSession,
    current_user: CurrentUser,
):
    """Get a well by ID with compound details."""
    await get_plate_or_404(db, plate_id, current_user.id)

    result = await db.execute(
        select(Well)
        .options(selectinload(Well.compound))
        .where(Well.id == well_id, Well.plate_id == plate_id)
    )
    well = result.scalar_one_or_none()

    if not well:
        raise HTTPException(status_code=404, detail="Well not found")

    return WellWithCompound(
        id=well.id,
        plate_id=well.plate_id,
        row=well.row,
        column=well.column,
        compound_id=well.compound_id,
        concentration=well.concentration,
        concentration_unit=well.concentration_unit,
        well_type=well.well_type,
        created_at=well.created_at,
        updated_at=well.updated_at,
        row_label=well.row_label,
        column_label=well.column_label,
        position=well.position,
        compound=well.compound,
    )


@router.get("/{well_id}/thumbnails", response_model=list[ImageThumbnail])
async def get_well_thumbnails(
    plate_id: str,
    well_id: str,
    db: DbSession,
    current_user: CurrentUser,
):
    """Get thumbnail URLs for all images in a well."""
    await get_plate_or_404(db, plate_id, current_user.id)

    # Verify well exists
    result = await db.execute(select(Well).where(Well.id == well_id, Well.plate_id == plate_id))
    well = result.scalar_one_or_none()
    if not well:
        raise HTTPException(status_code=404, detail="Well not found")

    # Get images
    result = await db.execute(
        select(Image)
        .where(Image.well_id == well_id)
        .order_by(Image.field_index, Image.channel_index)
    )
    images = result.scalars().all()

    # TODO: Generate actual thumbnail URLs from S3
    thumbnails = [
        ImageThumbnail(
            id=img.id,
            channel=img.channel,
            channel_index=img.channel_index,
            field_index=img.field_index,
            thumbnail_url=f"/api/images/{img.id}/thumbnail" if img.thumbnail_s3_key else None,
        )
        for img in images
    ]

    return thumbnails


@router.patch("/{well_id}", response_model=WellResponse)
async def update_well(
    plate_id: str,
    well_id: str,
    well_in: WellUpdate,
    db: DbSession,
    current_user: CurrentUser,
):
    """Update a well."""
    await get_plate_or_404(db, plate_id, current_user.id)

    result = await db.execute(
        select(Well).where(Well.id == well_id, Well.plate_id == plate_id)
    )
    well = result.scalar_one_or_none()

    if not well:
        raise HTTPException(status_code=404, detail="Well not found")

    update_data = well_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(well, field, value)

    await db.commit()
    await db.refresh(well)

    return WellResponse(
        id=well.id,
        plate_id=well.plate_id,
        row=well.row,
        column=well.column,
        compound_id=well.compound_id,
        concentration=well.concentration,
        concentration_unit=well.concentration_unit,
        well_type=well.well_type,
        created_at=well.created_at,
        updated_at=well.updated_at,
        row_label=well.row_label,
        column_label=well.column_label,
        position=well.position,
    )


@router.delete("/{well_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_well(
    plate_id: str,
    well_id: str,
    db: DbSession,
    current_user: CurrentUser,
):
    """Delete a well and all its data."""
    await get_plate_or_404(db, plate_id, current_user.id)

    result = await db.execute(
        select(Well).where(Well.id == well_id, Well.plate_id == plate_id)
    )
    well = result.scalar_one_or_none()

    if not well:
        raise HTTPException(status_code=404, detail="Well not found")

    await db.delete(well)
    await db.commit()
