#!/usr/bin/env python3
"""Seed script to create a default admin user for demo purposes.

Usage:
    cd backend
    uv run python scripts/seed_admin.py

Or with custom credentials via environment variables:
    ADMIN_EMAIL=admin@test.com ADMIN_PASSWORD=secret123 uv run python scripts/seed_admin.py
"""

import asyncio
import sys
from pathlib import Path

# Add the app directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import select

from app.core.config import settings
from app.core.database import async_session_maker
from app.core.security import get_password_hash
from app.models.user import User


async def seed_admin_user() -> None:
    """Create or update the default admin user."""
    async with async_session_maker() as session:
        # Check if admin user already exists
        result = await session.execute(
            select(User).where(User.email == settings.admin_email)
        )
        existing_user = result.scalar_one_or_none()

        if existing_user:
            print(f"Admin user already exists: {settings.admin_email}")
            print("Updating password...")
            existing_user.hashed_password = get_password_hash(settings.admin_password)
            existing_user.is_superuser = True
            existing_user.is_active = True
            await session.commit()
            print("Admin user updated successfully!")
        else:
            # Create new admin user
            admin_user = User(
                email=settings.admin_email,
                hashed_password=get_password_hash(settings.admin_password),
                full_name=settings.admin_full_name,
                is_active=True,
                is_superuser=True,
            )
            session.add(admin_user)
            await session.commit()
            print(f"Admin user created successfully: {settings.admin_email}")

        print("\nAdmin credentials:")
        print(f"  Email: {settings.admin_email}")
        print(f"  Password: {settings.admin_password}")


if __name__ == "__main__":
    asyncio.run(seed_admin_user())
