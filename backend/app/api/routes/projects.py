from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, get_pagination
from app.models.project import Project
from app.schemas.pagination import PaginatedResponse, PaginationParams
from app.schemas.project import ProjectCreate, ProjectRead, ProjectUpdate

router = APIRouter()


@router.get("", response_model=PaginatedResponse[ProjectRead])
async def list_projects(
    db: AsyncSession = Depends(get_db),
    pagination: PaginationParams = Depends(get_pagination),
) -> PaginatedResponse[ProjectRead]:
    count_query = select(func.count()).select_from(Project)
    total = await db.scalar(count_query) or 0

    query = select(Project).offset(pagination.offset).limit(pagination.limit)
    result = await db.execute(query)
    projects = result.scalars().all()

    return PaginatedResponse.create(
        items=[ProjectRead.model_validate(p) for p in projects],
        total=total,
        params=pagination,
    )


@router.get("/{project_id}", response_model=ProjectRead)
async def get_project(
    project_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> ProjectRead:
    query = select(Project).where(Project.id == project_id)
    result = await db.execute(query)
    project = result.scalar_one_or_none()

    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    return ProjectRead.model_validate(project)


@router.post("", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
async def create_project(
    project_in: ProjectCreate,
    db: AsyncSession = Depends(get_db),
) -> ProjectRead:
    # TODO: Get owner_id from authenticated user
    project = Project(**project_in.model_dump())
    db.add(project)
    await db.flush()
    await db.refresh(project)
    return ProjectRead.model_validate(project)


@router.patch("/{project_id}", response_model=ProjectRead)
async def update_project(
    project_id: UUID,
    project_in: ProjectUpdate,
    db: AsyncSession = Depends(get_db),
) -> ProjectRead:
    query = select(Project).where(Project.id == project_id)
    result = await db.execute(query)
    project = result.scalar_one_or_none()

    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    update_data = project_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(project, field, value)

    await db.flush()
    await db.refresh(project)
    return ProjectRead.model_validate(project)


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> None:
    query = select(Project).where(Project.id == project_id)
    result = await db.execute(query)
    project = result.scalar_one_or_none()

    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    await db.delete(project)
