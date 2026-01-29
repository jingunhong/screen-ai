from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin, generate_uuid


class Experiment(Base, TimestampMixin):
    __tablename__ = "experiments"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    name: Mapped[str] = mapped_column(String(255), index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    project_id: Mapped[str] = mapped_column(String(36), ForeignKey("projects.id"))

    # Relationships
    project: Mapped["Project"] = relationship("Project", back_populates="experiments")
    plates: Mapped[list["Plate"]] = relationship(
        "Plate", back_populates="experiment", cascade="all, delete-orphan"
    )


from app.models.project import Project
from app.models.plate import Plate
