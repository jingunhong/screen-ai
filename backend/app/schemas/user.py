from pydantic import BaseModel, EmailStr

from app.schemas.common import BaseSchema, TimestampSchema


class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    role: str = "scientist"


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    full_name: str | None = None
    role: str | None = None
    is_active: bool | None = None


class UserResponse(UserBase, TimestampSchema):
    id: str
    is_active: bool


class UserInDB(UserResponse):
    hashed_password: str


# Auth schemas
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: str
    exp: int


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
