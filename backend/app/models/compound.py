from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.base import TimestampMixin, generate_uuid


class Compound(Base, TimestampMixin):
    __tablename__ = "compounds"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    external_id: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    # Future: structure, molecular_weight, smiles, etc.
