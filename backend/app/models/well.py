from uuid import UUID

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel

if True:  # TYPE_CHECKING workaround for circular imports
    from app.models.analysis import Analysis
    from app.models.compound import Compound
    from app.models.image import Image
    from app.models.plate import Plate


class WellType:
    SAMPLE = "sample"
    POSITIVE_CONTROL = "positive_control"
    NEGATIVE_CONTROL = "negative_control"
    EMPTY = "empty"


class Well(BaseModel):
    __tablename__ = "wells"

    row: Mapped[int]
    column: Mapped[int]
    row_label: Mapped[str] = mapped_column(String(2))  # A-Z, AA-AF
    column_label: Mapped[str] = mapped_column(String(3))  # 1-48
    well_type: Mapped[str] = mapped_column(String(50), default=WellType.SAMPLE)
    concentration: Mapped[float | None]
    plate_id: Mapped[UUID] = mapped_column(ForeignKey("plates.id"))
    compound_id: Mapped[UUID | None] = mapped_column(ForeignKey("compounds.id"))

    # Relationships
    plate: Mapped["Plate"] = relationship(back_populates="wells")
    compound: Mapped["Compound | None"] = relationship(lazy="selectin")
    images: Mapped[list["Image"]] = relationship(
        back_populates="well",
        lazy="selectin",
        cascade="all, delete-orphan",
    )
    analyses: Mapped[list["Analysis"]] = relationship(
        back_populates="well",
        lazy="selectin",
        cascade="all, delete-orphan",
    )

    @property
    def position(self) -> str:
        return f"{self.row_label}{self.column_label}"
