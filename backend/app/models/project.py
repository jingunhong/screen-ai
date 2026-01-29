from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin, generate_uuid


class Project(Base, TimestampMixin):
    __tablename__ = "projects"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    name: Mapped[str] = mapped_column(String(255), index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    owner_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"))

    # Relationships
    owner: Mapped["User"] = relationship("User", backref="projects")
    experiments: Mapped[list["Experiment"]] = relationship(
        "Experiment", back_populates="project", cascade="all, delete-orphan"
    )


from app.models.user import User
from app.models.experiment import Experiment
