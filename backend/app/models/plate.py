from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin, generate_uuid


class Plate(Base, TimestampMixin):
    __tablename__ = "plates"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    name: Mapped[str] = mapped_column(String(255), index=True)
    barcode: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    experiment_id: Mapped[str] = mapped_column(String(36), ForeignKey("experiments.id"))

    # Plate format
    rows: Mapped[int] = mapped_column(Integer, default=16)  # A-P for 384-well
    columns: Mapped[int] = mapped_column(Integer, default=24)  # 1-24 for 384-well

    # Relationships
    experiment: Mapped["Experiment"] = relationship("Experiment", back_populates="plates")
    wells: Mapped[list["Well"]] = relationship(
        "Well", back_populates="plate", cascade="all, delete-orphan"
    )

    @property
    def well_count(self) -> int:
        return self.rows * self.columns

    @property
    def format_name(self) -> str:
        count = self.well_count
        if count == 96:
            return "96-well"
        elif count == 384:
            return "384-well"
        elif count == 1536:
            return "1536-well"
        return f"{count}-well"


from app.models.experiment import Experiment
from app.models.well import Well
