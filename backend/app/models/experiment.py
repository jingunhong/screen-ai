from datetime import date
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Date, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.plate import Plate
    from app.models.project import Project


class Experiment(BaseModel):
    __tablename__ = "experiments"

    name: Mapped[str] = mapped_column(String(255), index=True)
    description: Mapped[str | None] = mapped_column(Text)
    experiment_date: Mapped[date | None] = mapped_column(Date)
    project_id: Mapped[UUID] = mapped_column(ForeignKey("projects.id"))

    # Relationships
    project: Mapped["Project"] = relationship(back_populates="experiments")
    plates: Mapped[list["Plate"]] = relationship(
        back_populates="experiment",
        lazy="selectin",
        cascade="all, delete-orphan",
    )
