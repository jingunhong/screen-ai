from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select, func

from app.core.deps import DbSession, CurrentUser
from app.models import Project, Experiment, Plate
from app.schemas import ExperimentCreate, ExperimentUpdate, ExperimentResponse, ExperimentList

router = APIRouter(prefix="/projects/{project_id}/experiments", tags=["experiments"])


async def get_project_or_404(db, project_id: str, user_id: str) -> Project:
    """Helper to get project and verify ownership."""
    result = await db.execute(
        select(Project).where(Project.id == project_id, Project.owner_id == user_id)
    )
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.get("", response_model=ExperimentList)
async def list_experiments(
    project_id: str,
    db: DbSession,
    current_user: CurrentUser,
    skip: int = 0,
    limit: int = 100,
):
    """List all experiments in a project."""
    await get_project_or_404(db, project_id, current_user.id)

    # Count total
    count_query = select(func.count(Experiment.id)).where(Experiment.project_id == project_id)
    total = (await db.execute(count_query)).scalar()

    # Get experiments
    query = (
        select(Experiment)
        .where(Experiment.project_id == project_id)
        .order_by(Experiment.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(query)
    experiments = result.scalars().all()

    # Get plate counts
    items = []
    for exp in experiments:
        plate_count_query = select(func.count(Plate.id)).where(Plate.experiment_id == exp.id)
        plate_count = (await db.execute(plate_count_query)).scalar()
        items.append(
            ExperimentResponse(
                id=exp.id,
                name=exp.name,
                description=exp.description,
                project_id=exp.project_id,
                created_at=exp.created_at,
                updated_at=exp.updated_at,
                plate_count=plate_count,
            )
        )

    return ExperimentList(items=items, total=total, skip=skip, limit=limit)


@router.post("", response_model=ExperimentResponse, status_code=status.HTTP_201_CREATED)
async def create_experiment(
    project_id: str,
    experiment_in: ExperimentCreate,
    db: DbSession,
    current_user: CurrentUser,
):
    """Create a new experiment in a project."""
    await get_project_or_404(db, project_id, current_user.id)

    experiment = Experiment(
        name=experiment_in.name,
        description=experiment_in.description,
        project_id=project_id,
    )
    db.add(experiment)
    await db.commit()
    await db.refresh(experiment)

    return ExperimentResponse(
        id=experiment.id,
        name=experiment.name,
        description=experiment.description,
        project_id=experiment.project_id,
        created_at=experiment.created_at,
        updated_at=experiment.updated_at,
        plate_count=0,
    )


@router.get("/{experiment_id}", response_model=ExperimentResponse)
async def get_experiment(
    project_id: str,
    experiment_id: str,
    db: DbSession,
    current_user: CurrentUser,
):
    """Get an experiment by ID."""
    await get_project_or_404(db, project_id, current_user.id)

    result = await db.execute(
        select(Experiment).where(
            Experiment.id == experiment_id, Experiment.project_id == project_id
        )
    )
    experiment = result.scalar_one_or_none()

    if not experiment:
        raise HTTPException(status_code=404, detail="Experiment not found")

    plate_count_query = select(func.count(Plate.id)).where(Plate.experiment_id == experiment.id)
    plate_count = (await db.execute(plate_count_query)).scalar()

    return ExperimentResponse(
        id=experiment.id,
        name=experiment.name,
        description=experiment.description,
        project_id=experiment.project_id,
        created_at=experiment.created_at,
        updated_at=experiment.updated_at,
        plate_count=plate_count,
    )


@router.patch("/{experiment_id}", response_model=ExperimentResponse)
async def update_experiment(
    project_id: str,
    experiment_id: str,
    experiment_in: ExperimentUpdate,
    db: DbSession,
    current_user: CurrentUser,
):
    """Update an experiment."""
    await get_project_or_404(db, project_id, current_user.id)

    result = await db.execute(
        select(Experiment).where(
            Experiment.id == experiment_id, Experiment.project_id == project_id
        )
    )
    experiment = result.scalar_one_or_none()

    if not experiment:
        raise HTTPException(status_code=404, detail="Experiment not found")

    update_data = experiment_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(experiment, field, value)

    await db.commit()
    await db.refresh(experiment)

    plate_count_query = select(func.count(Plate.id)).where(Plate.experiment_id == experiment.id)
    plate_count = (await db.execute(plate_count_query)).scalar()

    return ExperimentResponse(
        id=experiment.id,
        name=experiment.name,
        description=experiment.description,
        project_id=experiment.project_id,
        created_at=experiment.created_at,
        updated_at=experiment.updated_at,
        plate_count=plate_count,
    )


@router.delete("/{experiment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_experiment(
    project_id: str,
    experiment_id: str,
    db: DbSession,
    current_user: CurrentUser,
):
    """Delete an experiment and all its data."""
    await get_project_or_404(db, project_id, current_user.id)

    result = await db.execute(
        select(Experiment).where(
            Experiment.id == experiment_id, Experiment.project_id == project_id
        )
    )
    experiment = result.scalar_one_or_none()

    if not experiment:
        raise HTTPException(status_code=404, detail="Experiment not found")

    await db.delete(experiment)
    await db.commit()
