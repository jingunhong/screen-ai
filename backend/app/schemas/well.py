from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, Field, computed_field

from app.schemas.base import IDSchema, TimestampSchema
from app.schemas.compound import CompoundRead


class WellBase(TimestampSchema):
    row: int = Field(ge=0)
    column: int = Field(ge=0)
    row_label: str
    column_label: str
    well_type: str = "sample"
    concentration: float | None = None


class WellCreate(BaseModel):
    row: int
    column: int
    row_label: str
    column_label: str
    well_type: str = "sample"
    concentration: float | None = None
    plate_id: UUID
    compound_id: UUID | None = None


class WellUpdate(BaseModel):
    well_type: str | None = None
    concentration: float | None = None
    compound_id: UUID | None = None


class WellRead(WellBase, IDSchema):
    plate_id: UUID
    compound_id: UUID | None = None

    @computed_field
    @property
    def position(self) -> str:
        return f"{self.row_label}{self.column_label}"


class WellReadWithRelations(WellRead):
    compound: CompoundRead | None = None
    images: list[ImageRead] = []  # noqa: F821
    analyses: list[AnalysisRead] = []  # noqa: F821
