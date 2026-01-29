from uuid import UUID

from pydantic import BaseModel, Field

from app.schemas.base import IDSchema, TimestampSchema


class PlateBase(TimestampSchema):
    name: str
    barcode: str | None = None
    format: int = Field(default=384, description="Plate format: 96, 384, or 1536")
    rows: int = Field(default=16, ge=1)
    columns: int = Field(default=24, ge=1)


class PlateCreate(BaseModel):
    name: str
    barcode: str | None = None
    format: int = 384
    rows: int = 16
    columns: int = 24
    experiment_id: UUID


class PlateUpdate(BaseModel):
    name: str | None = None
    barcode: str | None = None


class PlateRead(PlateBase, IDSchema):
    experiment_id: UUID


class PlateReadWithWells(PlateRead):
    from app.schemas.well import WellRead

    wells: list["WellRead"] = []
