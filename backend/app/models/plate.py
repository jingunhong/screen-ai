from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.experiment import Experiment
    from app.models.well import Well


class PlateFormat:
    PLATE_96 = 96
    PLATE_384 = 384
    PLATE_1536 = 1536


class Plate(BaseModel):
    __tablename__ = "plates"

    name: Mapped[str] = mapped_column(String(255), index=True)
    barcode: Mapped[str | None] = mapped_column(String(100), unique=True, index=True)
    format: Mapped[int] = mapped_column(default=PlateFormat.PLATE_384)
    rows: Mapped[int] = mapped_column(default=16)
    columns: Mapped[int] = mapped_column(default=24)
    experiment_id: Mapped[UUID] = mapped_column(ForeignKey("experiments.id"))

    # Relationships
    experiment: Mapped["Experiment"] = relationship(back_populates="plates")
    wells: Mapped[list["Well"]] = relationship(
        back_populates="plate",
        lazy="selectin",
        cascade="all, delete-orphan",
    )
