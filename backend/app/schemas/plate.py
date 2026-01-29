from pydantic import BaseModel

from app.schemas.common import BaseSchema, TimestampSchema, PaginatedResponse


class PlateBase(BaseModel):
    name: str
    barcode: str | None = None
    description: str | None = None
    rows: int = 16
    columns: int = 24


class PlateCreate(PlateBase):
    pass


class PlateUpdate(BaseModel):
    name: str | None = None
    barcode: str | None = None
    description: str | None = None


class PlateResponse(PlateBase, TimestampSchema):
    id: str
    experiment_id: str
    well_count: int = 0
    format_name: str = "384-well"


class PlateList(PaginatedResponse):
    items: list[PlateResponse]
