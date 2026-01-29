from pydantic import BaseModel

from app.schemas.common import BaseSchema, TimestampSchema, PaginatedResponse


class ImageBase(BaseModel):
    s3_key: str
    thumbnail_s3_key: str | None = None
    field_index: int = 0
    channel: str
    channel_index: int = 0
    width: int | None = None
    height: int | None = None
    pixel_size_um: float | None = None
    original_filename: str | None = None


class ImageCreate(ImageBase):
    well_id: str


class ImageUpdate(BaseModel):
    thumbnail_s3_key: str | None = None


class ImageResponse(ImageBase, TimestampSchema):
    id: str
    well_id: str


class ImageList(PaginatedResponse):
    items: list[ImageResponse]


# For thumbnail display
class ImageThumbnail(BaseModel):
    id: str
    channel: str
    channel_index: int
    field_index: int
    thumbnail_url: str | None = None
