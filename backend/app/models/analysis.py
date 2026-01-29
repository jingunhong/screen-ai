from sqlalchemy import Float, ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin, generate_uuid


class WellAnalysis(Base, TimestampMixin):
    __tablename__ = "well_analyses"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    well_id: Mapped[str] = mapped_column(String(36), ForeignKey("wells.id"), unique=True)

    # Core metrics
    cell_count: Mapped[int | None] = mapped_column(nullable=True)
    viability: Mapped[float | None] = mapped_column(Float, nullable=True)  # 0-100%
    z_score: Mapped[float | None] = mapped_column(Float, nullable=True)

    # Extensible metrics stored as JSON
    metrics: Mapped[dict | None] = mapped_column(JSONB, nullable=True)

    # Relationships
    well: Mapped["Well"] = relationship("Well", back_populates="analysis")


class DoseResponseCurve(Base, TimestampMixin):
    __tablename__ = "dose_response_curves"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    experiment_id: Mapped[str] = mapped_column(String(36), ForeignKey("experiments.id"))
    compound_id: Mapped[str] = mapped_column(String(36), ForeignKey("compounds.id"))

    # DRC parameters
    ic50: Mapped[float | None] = mapped_column(Float, nullable=True)
    ec50: Mapped[float | None] = mapped_column(Float, nullable=True)
    hill_slope: Mapped[float | None] = mapped_column(Float, nullable=True)
    top: Mapped[float | None] = mapped_column(Float, nullable=True)
    bottom: Mapped[float | None] = mapped_column(Float, nullable=True)
    r_squared: Mapped[float | None] = mapped_column(Float, nullable=True)

    # Raw data points for plotting (JSON array of {concentration, response})
    data_points: Mapped[list | None] = mapped_column(JSONB, nullable=True)

    # Relationships
    experiment: Mapped["Experiment"] = relationship("Experiment", backref="dose_response_curves")
    compound: Mapped["Compound"] = relationship("Compound", backref="dose_response_curves")


from app.models.well import Well
from app.models.experiment import Experiment
from app.models.compound import Compound
