from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Application
    app_name: str = "Screen AI"
    debug: bool = False

    # Database
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/screen_ai"

    # Security
    secret_key: str = "change-me-in-production"
    access_token_expire_minutes: int = 60 * 24 * 7  # 1 week
    jwt_algorithm: str = "HS256"

    # Default admin user (for demo/development)
    admin_email: str = "admin@example.com"
    admin_password: str = "admin123"
    admin_full_name: str = "Admin User"
    create_admin_on_startup: bool = False  # Set to True to auto-create admin on startup

    # AWS S3
    s3_bucket: str = ""
    s3_region: str = "us-east-1"
    aws_access_key_id: str = ""
    aws_secret_access_key: str = ""


settings = Settings()
