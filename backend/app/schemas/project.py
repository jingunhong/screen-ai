from pydantic import BaseModel

from app.schemas.common import BaseSchema, TimestampSchema, PaginatedResponse


class ProjectBase(BaseModel):
    name: str
    description: str | None = None


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: str | None = None
    description: str | None = None


class ProjectResponse(ProjectBase, TimestampSchema):
    id: str
    owner_id: str
    experiment_count: int = 0


class ProjectList(PaginatedResponse):
    items: list[ProjectResponse]
