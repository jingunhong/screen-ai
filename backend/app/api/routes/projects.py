from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select, func

from app.core.deps import DbSession, CurrentUser
from app.models import Project, Experiment
from app.schemas import ProjectCreate, ProjectUpdate, ProjectResponse, ProjectList

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("", response_model=ProjectList)
async def list_projects(
    db: DbSession,
    current_user: CurrentUser,
    skip: int = 0,
    limit: int = 100,
):
    """List all projects for the current user."""
    # Count total
    count_query = select(func.count(Project.id)).where(Project.owner_id == current_user.id)
    total = (await db.execute(count_query)).scalar()

    # Get projects with experiment count
    query = (
        select(Project)
        .where(Project.owner_id == current_user.id)
        .order_by(Project.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(query)
    projects = result.scalars().all()

    # Get experiment counts
    items = []
    for project in projects:
        exp_count_query = select(func.count(Experiment.id)).where(
            Experiment.project_id == project.id
        )
        exp_count = (await db.execute(exp_count_query)).scalar()
        items.append(
            ProjectResponse(
                id=project.id,
                name=project.name,
                description=project.description,
                owner_id=project.owner_id,
                created_at=project.created_at,
                updated_at=project.updated_at,
                experiment_count=exp_count,
            )
        )

    return ProjectList(items=items, total=total, skip=skip, limit=limit)


@router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    project_in: ProjectCreate,
    db: DbSession,
    current_user: CurrentUser,
):
    """Create a new project."""
    project = Project(
        name=project_in.name,
        description=project_in.description,
        owner_id=current_user.id,
    )
    db.add(project)
    await db.commit()
    await db.refresh(project)

    return ProjectResponse(
        id=project.id,
        name=project.name,
        description=project.description,
        owner_id=project.owner_id,
        created_at=project.created_at,
        updated_at=project.updated_at,
        experiment_count=0,
    )


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: str,
    db: DbSession,
    current_user: CurrentUser,
):
    """Get a project by ID."""
    result = await db.execute(
        select(Project).where(Project.id == project_id, Project.owner_id == current_user.id)
    )
    project = result.scalar_one_or_none()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    exp_count_query = select(func.count(Experiment.id)).where(
        Experiment.project_id == project.id
    )
    exp_count = (await db.execute(exp_count_query)).scalar()

    return ProjectResponse(
        id=project.id,
        name=project.name,
        description=project.description,
        owner_id=project.owner_id,
        created_at=project.created_at,
        updated_at=project.updated_at,
        experiment_count=exp_count,
    )


@router.patch("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: str,
    project_in: ProjectUpdate,
    db: DbSession,
    current_user: CurrentUser,
):
    """Update a project."""
    result = await db.execute(
        select(Project).where(Project.id == project_id, Project.owner_id == current_user.id)
    )
    project = result.scalar_one_or_none()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    update_data = project_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(project, field, value)

    await db.commit()
    await db.refresh(project)

    exp_count_query = select(func.count(Experiment.id)).where(
        Experiment.project_id == project.id
    )
    exp_count = (await db.execute(exp_count_query)).scalar()

    return ProjectResponse(
        id=project.id,
        name=project.name,
        description=project.description,
        owner_id=project.owner_id,
        created_at=project.created_at,
        updated_at=project.updated_at,
        experiment_count=exp_count,
    )


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: str,
    db: DbSession,
    current_user: CurrentUser,
):
    """Delete a project and all its data."""
    result = await db.execute(
        select(Project).where(Project.id == project_id, Project.owner_id == current_user.id)
    )
    project = result.scalar_one_or_none()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    await db.delete(project)
    await db.commit()
