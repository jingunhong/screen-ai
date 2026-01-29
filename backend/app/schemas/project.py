from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel

from app.schemas.base import IDSchema, TimestampSchema


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
    experiments: list[ExperimentRead] = []  # noqa: F821
