from uuid import UUID

from pydantic import BaseModel

from app.schemas.base import IDSchema, TimestampSchema


class AnalysisBase(TimestampSchema):
    name: str
    analysis_type: str
    cell_count: int | None = None
    mean_intensity: float | None = None
    median_intensity: float | None = None
    std_intensity: float | None = None
    z_score: float | None = None
    percent_effect: float | None = None


class AnalysisCreate(BaseModel):
    name: str
    analysis_type: str
    cell_count: int | None = None
    mean_intensity: float | None = None
    median_intensity: float | None = None
    std_intensity: float | None = None
    z_score: float | None = None
    percent_effect: float | None = None
    raw_data: dict | None = None
    well_id: UUID


class AnalysisUpdate(BaseModel):
    name: str | None = None
    cell_count: int | None = None
    mean_intensity: float | None = None
    median_intensity: float | None = None
    std_intensity: float | None = None
    z_score: float | None = None
    percent_effect: float | None = None
    raw_data: dict | None = None


class AnalysisRead(AnalysisBase, IDSchema):
    raw_data: dict | None = None
    well_id: UUID
