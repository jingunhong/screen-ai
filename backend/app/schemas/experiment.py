from pydantic import BaseModel

from app.schemas.common import BaseSchema, TimestampSchema, PaginatedResponse


class ExperimentBase(BaseModel):
    name: str
    description: str | None = None


class ExperimentCreate(ExperimentBase):
    pass


class ExperimentUpdate(BaseModel):
    name: str | None = None
    description: str | None = None


class ExperimentResponse(ExperimentBase, TimestampSchema):
    id: str
    project_id: str
    plate_count: int = 0


class ExperimentList(PaginatedResponse):
    items: list[ExperimentResponse]
