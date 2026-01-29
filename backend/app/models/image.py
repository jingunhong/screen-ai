from uuid import UUID

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel

if True:  # TYPE_CHECKING workaround for circular imports
    from app.models.well import Well


class Image(BaseModel):
    __tablename__ = "images"

    filename: Mapped[str] = mapped_column(String(500))
    s3_key: Mapped[str] = mapped_column(String(1000))
    thumbnail_s3_key: Mapped[str | None] = mapped_column(String(1000))
    channel: Mapped[str] = mapped_column(String(50))  # e.g., DAPI, GFP, etc.
    channel_index: Mapped[int] = mapped_column(default=0)
    field_index: Mapped[int] = mapped_column(default=0)  # For multiple fields per well
    width: Mapped[int | None]
    height: Mapped[int | None]
    well_id: Mapped[UUID] = mapped_column(ForeignKey("wells.id"))

    # Relationships
    well: Mapped["Well"] = relationship(back_populates="images")
