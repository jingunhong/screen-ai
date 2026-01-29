from pydantic import BaseModel

from app.schemas.common import BaseSchema, TimestampSchema, PaginatedResponse
from app.schemas.compound import CompoundResponse


class WellBase(BaseModel):
    row: int
    column: int
    compound_id: str | None = None
    concentration: float | None = None
    concentration_unit: str = "uM"
    well_type: str = "sample"


class WellCreate(WellBase):
    pass


class WellUpdate(BaseModel):
    compound_id: str | None = None
    concentration: float | None = None
    concentration_unit: str | None = None
    well_type: str | None = None


class WellResponse(WellBase, TimestampSchema):
    id: str
    plate_id: str
    row_label: str
    column_label: str
    position: str


class WellWithCompound(WellResponse):
    compound: CompoundResponse | None = None


class WellList(PaginatedResponse):
    items: list[WellResponse]


# For plate grid view - minimal well data
class WellGridItem(BaseModel):
    id: str
    row: int
    column: int
    position: str
    well_type: str
    compound_id: str | None = None
    concentration: float | None = None
    # Analysis summary for heatmap
    cell_count: int | None = None
    viability: float | None = None
    z_score: float | None = None
