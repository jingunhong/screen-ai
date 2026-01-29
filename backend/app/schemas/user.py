from pydantic import BaseModel, EmailStr

from app.schemas.base import IDSchema, TimestampSchema


class UserBase(TimestampSchema):
    email: EmailStr
    full_name: str | None = None
    is_active: bool = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str | None = None


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    password: str | None = None
    full_name: str | None = None
    is_active: bool | None = None


class UserRead(UserBase, IDSchema):
    is_superuser: bool = False
