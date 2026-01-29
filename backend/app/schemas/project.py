from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from pydantic import BaseModel

from app.schemas.base import IDSchema, TimestampSchema

if TYPE_CHECKING:
    from app.schemas.experiment import ExperimentRead


class ProjectBase(TimestampSchema):
    name: str
    description: str | None = None


class ProjectCreate(BaseModel):
    name: str
    description: str | None = None


class ProjectUpdate(BaseModel):
    name: str | None = None
    description: str | None = None


class ProjectRead(ProjectBase, IDSchema):
    owner_id: UUID


class ProjectReadWithExperiments(ProjectRead):
    experiments: list[ExperimentRead] = []
