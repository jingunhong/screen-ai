from pydantic import BaseModel

from app.schemas.base import IDSchema, TimestampSchema


class CompoundBase(TimestampSchema):
    identifier: str
    name: str | None = None


class CompoundCreate(BaseModel):
    identifier: str
    name: str | None = None


class CompoundUpdate(BaseModel):
    identifier: str | None = None
    name: str | None = None


class CompoundRead(CompoundBase, IDSchema):
    pass
