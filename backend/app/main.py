from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select

from app.api import api_router
from app.core.config import settings
from app.core.database import async_session_maker
from app.core.security import get_password_hash
from app.models.user import User


async def create_admin_user() -> None:
    """Create default admin user if it doesn't exist."""
    async with async_session_maker() as session:
        result = await session.execute(select(User).where(User.email == settings.admin_email))
        existing_user = result.scalar_one_or_none()

        if not existing_user:
            admin_user = User(
                email=settings.admin_email,
                hashed_password=get_password_hash(settings.admin_password),
                full_name=settings.admin_full_name,
                is_active=True,
                is_superuser=True,
            )
            session.add(admin_user)
            await session.commit()
            print(f"Created admin user: {settings.admin_email}")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Application lifespan events."""
    # Startup
    if settings.create_admin_on_startup:
        await create_admin_user()
    yield
    # Shutdown (nothing to do)


app = FastAPI(
    title=settings.app_name,
    openapi_url="/api/openapi.json",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": f"Welcome to {settings.app_name}"}
