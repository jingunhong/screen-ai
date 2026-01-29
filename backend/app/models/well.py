from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin, generate_uuid


class Well(Base, TimestampMixin):
    __tablename__ = "wells"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    plate_id: Mapped[str] = mapped_column(String(36), ForeignKey("plates.id"))

    # Well position
    row: Mapped[int] = mapped_column(Integer)  # 0-indexed (0 = A, 1 = B, etc.)
    column: Mapped[int] = mapped_column(Integer)  # 0-indexed (0 = 1, 1 = 2, etc.)

    # Compound info
    compound_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("compounds.id"), nullable=True
    )
    concentration: Mapped[float | None] = mapped_column(Float, nullable=True)
    concentration_unit: Mapped[str] = mapped_column(String(20), default="uM")

    # Well type
    well_type: Mapped[str] = mapped_column(
        String(50), default="sample"
    )  # sample, positive_control, negative_control, empty

    # Relationships
    plate: Mapped["Plate"] = relationship("Plate", back_populates="wells")
    compound: Mapped["Compound | None"] = relationship("Compound", backref="wells")
    images: Mapped[list["Image"]] = relationship(
        "Image", back_populates="well", cascade="all, delete-orphan"
    )
    analysis: Mapped["WellAnalysis | None"] = relationship(
        "WellAnalysis", back_populates="well", uselist=False, cascade="all, delete-orphan"
    )

    @property
    def row_label(self) -> str:
        return chr(ord("A") + self.row)

    @property
    def column_label(self) -> str:
        return str(self.column + 1)

    @property
    def position(self) -> str:
        return f"{self.row_label}{self.column_label}"


from app.models.plate import Plate
from app.models.compound import Compound
from app.models.image import Image
from app.models.analysis import WellAnalysis
