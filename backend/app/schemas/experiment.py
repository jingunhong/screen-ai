from datetime import date
from uuid import UUID

from pydantic import BaseModel

from app.schemas.base import IDSchema, TimestampSchema


class ExperimentBase(TimestampSchema):
    name: str
    description: str | None = None
    experiment_date: date | None = None


class ExperimentCreate(BaseModel):
    name: str
    description: str | None = None
    experiment_date: date | None = None
    project_id: UUID


class ExperimentUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    experiment_date: date | None = None


class ExperimentRead(ExperimentBase, IDSchema):
    project_id: UUID


class ExperimentReadWithPlates(ExperimentRead):
    from app.schemas.plate import PlateRead

    plates: list["PlateRead"] = []
