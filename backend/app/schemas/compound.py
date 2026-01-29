from pydantic import BaseModel

from app.schemas.common import BaseSchema, TimestampSchema, PaginatedResponse


class CompoundBase(BaseModel):
    external_id: str
    name: str | None = None


class CompoundCreate(CompoundBase):
    pass


class CompoundUpdate(BaseModel):
    name: str | None = None


class CompoundResponse(CompoundBase, TimestampSchema):
    id: str


class CompoundList(PaginatedResponse):
    items: list[CompoundResponse]
