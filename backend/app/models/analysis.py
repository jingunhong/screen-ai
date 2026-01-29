from uuid import UUID

from sqlalchemy import JSON, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel

if True:  # TYPE_CHECKING workaround for circular imports
    from app.models.well import Well


class Analysis(BaseModel):
    __tablename__ = "analyses"

    name: Mapped[str] = mapped_column(String(255))
    analysis_type: Mapped[str] = mapped_column(String(100))  # e.g., cell_count, viability
    cell_count: Mapped[int | None]
    mean_intensity: Mapped[float | None] = mapped_column(Float)
    median_intensity: Mapped[float | None] = mapped_column(Float)
    std_intensity: Mapped[float | None] = mapped_column(Float)
    z_score: Mapped[float | None] = mapped_column(Float)
    percent_effect: Mapped[float | None] = mapped_column(Float)
    raw_data: Mapped[dict | None] = mapped_column(JSON)
    well_id: Mapped[UUID] = mapped_column(ForeignKey("wells.id"))

    # Relationships
    well: Mapped["Well"] = relationship(back_populates="analyses")
