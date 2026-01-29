from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from app.core.deps import DbSession, CurrentUser
from app.models import Project, Experiment, Plate, Well, WellAnalysis
from app.schemas import PlateCreate, PlateUpdate, PlateResponse, PlateList
from app.schemas.well import WellGridItem

router = APIRouter(prefix="/experiments/{experiment_id}/plates", tags=["plates"])


async def get_experiment_or_404(db, experiment_id: str, user_id: str) -> Experiment:
    """Helper to get experiment and verify ownership through project."""
    result = await db.execute(
        select(Experiment)
        .join(Project)
        .where(Experiment.id == experiment_id, Project.owner_id == user_id)
    )
    experiment = result.scalar_one_or_none()
    if not experiment:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return experiment


@router.get("", response_model=PlateList)
async def list_plates(
    experiment_id: str,
    db: DbSession,
    current_user: CurrentUser,
    skip: int = 0,
    limit: int = 100,
):
    """List all plates in an experiment."""
    await get_experiment_or_404(db, experiment_id, current_user.id)

    # Count total
    count_query = select(func.count(Plate.id)).where(Plate.experiment_id == experiment_id)
    total = (await db.execute(count_query)).scalar()

    # Get plates
    query = (
        select(Plate)
        .where(Plate.experiment_id == experiment_id)
        .order_by(Plate.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(query)
    plates = result.scalars().all()

    # Get well counts
    items = []
    for plate in plates:
        well_count_query = select(func.count(Well.id)).where(Well.plate_id == plate.id)
        well_count = (await db.execute(well_count_query)).scalar()
        items.append(
            PlateResponse(
                id=plate.id,
                name=plate.name,
                barcode=plate.barcode,
                description=plate.description,
                experiment_id=plate.experiment_id,
                rows=plate.rows,
                columns=plate.columns,
                created_at=plate.created_at,
                updated_at=plate.updated_at,
                well_count=well_count,
                format_name=plate.format_name,
            )
        )

    return PlateList(items=items, total=total, skip=skip, limit=limit)


@router.post("", response_model=PlateResponse, status_code=status.HTTP_201_CREATED)
async def create_plate(
    experiment_id: str,
    plate_in: PlateCreate,
    db: DbSession,
    current_user: CurrentUser,
):
    """Create a new plate in an experiment."""
    await get_experiment_or_404(db, experiment_id, current_user.id)

    plate = Plate(
        name=plate_in.name,
        barcode=plate_in.barcode,
        description=plate_in.description,
        experiment_id=experiment_id,
        rows=plate_in.rows,
        columns=plate_in.columns,
    )
    db.add(plate)
    await db.commit()
    await db.refresh(plate)

    return PlateResponse(
        id=plate.id,
        name=plate.name,
        barcode=plate.barcode,
        description=plate.description,
        experiment_id=plate.experiment_id,
        rows=plate.rows,
        columns=plate.columns,
        created_at=plate.created_at,
        updated_at=plate.updated_at,
        well_count=0,
        format_name=plate.format_name,
    )


@router.get("/{plate_id}", response_model=PlateResponse)
async def get_plate(
    experiment_id: str,
    plate_id: str,
    db: DbSession,
    current_user: CurrentUser,
):
    """Get a plate by ID."""
    await get_experiment_or_404(db, experiment_id, current_user.id)

    result = await db.execute(
        select(Plate).where(Plate.id == plate_id, Plate.experiment_id == experiment_id)
    )
    plate = result.scalar_one_or_none()

    if not plate:
        raise HTTPException(status_code=404, detail="Plate not found")

    well_count_query = select(func.count(Well.id)).where(Well.plate_id == plate.id)
    well_count = (await db.execute(well_count_query)).scalar()

    return PlateResponse(
        id=plate.id,
        name=plate.name,
        barcode=plate.barcode,
        description=plate.description,
        experiment_id=plate.experiment_id,
        rows=plate.rows,
        columns=plate.columns,
        created_at=plate.created_at,
        updated_at=plate.updated_at,
        well_count=well_count,
        format_name=plate.format_name,
    )


@router.get("/{plate_id}/grid", response_model=list[WellGridItem])
async def get_plate_grid(
    experiment_id: str,
    plate_id: str,
    db: DbSession,
    current_user: CurrentUser,
):
    """Get plate grid data for heatmap visualization."""
    await get_experiment_or_404(db, experiment_id, current_user.id)

    # Verify plate exists
    result = await db.execute(
        select(Plate).where(Plate.id == plate_id, Plate.experiment_id == experiment_id)
    )
    plate = result.scalar_one_or_none()
    if not plate:
        raise HTTPException(status_code=404, detail="Plate not found")

    # Get wells with analysis data
    query = (
        select(Well)
        .options(selectinload(Well.analysis))
        .where(Well.plate_id == plate_id)
        .order_by(Well.row, Well.column)
    )
    result = await db.execute(query)
    wells = result.scalars().all()

    grid_items = []
    for well in wells:
        analysis = well.analysis
        grid_items.append(
            WellGridItem(
                id=well.id,
                row=well.row,
                column=well.column,
                position=well.position,
                well_type=well.well_type,
                compound_id=well.compound_id,
                concentration=well.concentration,
                cell_count=analysis.cell_count if analysis else None,
                viability=analysis.viability if analysis else None,
                z_score=analysis.z_score if analysis else None,
            )
        )

    return grid_items


@router.patch("/{plate_id}", response_model=PlateResponse)
async def update_plate(
    experiment_id: str,
    plate_id: str,
    plate_in: PlateUpdate,
    db: DbSession,
    current_user: CurrentUser,
):
    """Update a plate."""
    await get_experiment_or_404(db, experiment_id, current_user.id)

    result = await db.execute(
        select(Plate).where(Plate.id == plate_id, Plate.experiment_id == experiment_id)
    )
    plate = result.scalar_one_or_none()

    if not plate:
        raise HTTPException(status_code=404, detail="Plate not found")

    update_data = plate_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(plate, field, value)

    await db.commit()
    await db.refresh(plate)

    well_count_query = select(func.count(Well.id)).where(Well.plate_id == plate.id)
    well_count = (await db.execute(well_count_query)).scalar()

    return PlateResponse(
        id=plate.id,
        name=plate.name,
        barcode=plate.barcode,
        description=plate.description,
        experiment_id=plate.experiment_id,
        rows=plate.rows,
        columns=plate.columns,
        created_at=plate.created_at,
        updated_at=plate.updated_at,
        well_count=well_count,
        format_name=plate.format_name,
    )


@router.delete("/{plate_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_plate(
    experiment_id: str,
    plate_id: str,
    db: DbSession,
    current_user: CurrentUser,
):
    """Delete a plate and all its data."""
    await get_experiment_or_404(db, experiment_id, current_user.id)

    result = await db.execute(
        select(Plate).where(Plate.id == plate_id, Plate.experiment_id == experiment_id)
    )
    plate = result.scalar_one_or_none()

    if not plate:
        raise HTTPException(status_code=404, detail="Plate not found")

    await db.delete(plate)
    await db.commit()
