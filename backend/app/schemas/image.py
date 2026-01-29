from uuid import UUID

from pydantic import BaseModel

from app.schemas.base import IDSchema, TimestampSchema


class ImageBase(TimestampSchema):
    filename: str
    channel: str
    channel_index: int = 0
    field_index: int = 0
    width: int | None = None
    height: int | None = None


class ImageCreate(BaseModel):
    filename: str
    s3_key: str
    thumbnail_s3_key: str | None = None
    channel: str
    channel_index: int = 0
    field_index: int = 0
    width: int | None = None
    height: int | None = None
    well_id: UUID


class ImageUpdate(BaseModel):
    thumbnail_s3_key: str | None = None
    width: int | None = None
    height: int | None = None


class ImageRead(ImageBase, IDSchema):
    s3_key: str
    thumbnail_s3_key: str | None = None
    well_id: UUID
