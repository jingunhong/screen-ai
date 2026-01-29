from pydantic import BaseModel

from app.schemas.common import BaseSchema, TimestampSchema, PaginatedResponse


class WellAnalysisBase(BaseModel):
    cell_count: int | None = None
    viability: float | None = None
    z_score: float | None = None
    metrics: dict | None = None


class WellAnalysisCreate(WellAnalysisBase):
    well_id: str


class WellAnalysisUpdate(WellAnalysisBase):
    pass


class WellAnalysisResponse(WellAnalysisBase, TimestampSchema):
    id: str
    well_id: str


# DRC schemas
class DRCDataPoint(BaseModel):
    concentration: float
    response: float
    std_error: float | None = None


class DoseResponseCurveBase(BaseModel):
    ic50: float | None = None
    ec50: float | None = None
    hill_slope: float | None = None
    top: float | None = None
    bottom: float | None = None
    r_squared: float | None = None
    data_points: list[DRCDataPoint] | None = None


class DoseResponseCurveCreate(DoseResponseCurveBase):
    experiment_id: str
    compound_id: str


class DoseResponseCurveUpdate(DoseResponseCurveBase):
    pass


class DoseResponseCurveResponse(DoseResponseCurveBase, TimestampSchema):
    id: str
    experiment_id: str
    compound_id: str


class DoseResponseCurveList(PaginatedResponse):
    items: list[DoseResponseCurveResponse]
