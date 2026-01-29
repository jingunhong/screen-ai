from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin, generate_uuid


class Image(Base, TimestampMixin):
    __tablename__ = "images"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    well_id: Mapped[str] = mapped_column(String(36), ForeignKey("wells.id"))

    # Image location
    s3_key: Mapped[str] = mapped_column(String(500))  # Full path in S3
    thumbnail_s3_key: Mapped[str | None] = mapped_column(String(500), nullable=True)

    # Image metadata
    field_index: Mapped[int] = mapped_column(Integer, default=0)  # For multiple fields per well
    channel: Mapped[str] = mapped_column(String(50))  # e.g., "DAPI", "GFP", "mCherry"
    channel_index: Mapped[int] = mapped_column(Integer, default=0)

    # Image properties
    width: Mapped[int | None] = mapped_column(Integer, nullable=True)
    height: Mapped[int | None] = mapped_column(Integer, nullable=True)
    pixel_size_um: Mapped[float | None] = mapped_column(Float, nullable=True)  # um per pixel

    # Original filename
    original_filename: Mapped[str | None] = mapped_column(String(500), nullable=True)

    # Relationships
    well: Mapped["Well"] = relationship("Well", back_populates="images")


from app.models.well import Well
