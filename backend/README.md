# Screen AI Backend

FastAPI backend for the Screen AI drug discovery screening data management platform.

## Setup

1. Install dependencies with uv:
   ```bash
   uv sync
   ```

2. Set up environment variables (copy from `.env.example` or create `.env`):
   ```bash
   DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/screen_ai
   SECRET_KEY=your-secret-key
   ```

3. Run database migrations:
   ```bash
   uv run alembic upgrade head
   ```

4. Start the development server:
   ```bash
   uv run uvicorn app.main:app --reload
   ```

## Development

### Running Tests
```bash
uv run pytest
```

### Database Migrations (Alembic)

**Apply all migrations:**
```bash
uv run alembic upgrade head
```

**Create a new migration (auto-generate from model changes):**
```bash
uv run alembic revision --autogenerate -m "description of changes"
```

**View migration history:**
```bash
uv run alembic history
```

**Downgrade one revision:**
```bash
uv run alembic downgrade -1
```

**Check current revision:**
```bash
uv run alembic current
```

> **Note:** Auto-generate requires a running PostgreSQL database to compare models against. For initial setup, ensure the database is running via Docker Compose before creating migrations.

### API Documentation
- Swagger UI: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc

## Project Structure

```
backend/
├── app/
│   ├── api/           # FastAPI routes
│   │   └── routes/    # Individual route modules
│   ├── core/          # Config, database, dependencies
│   ├── models/        # SQLAlchemy ORM models
│   ├── schemas/       # Pydantic schemas
│   ├── services/      # Business logic
│   └── main.py        # FastAPI application
├── alembic/           # Database migrations
├── tests/             # Test files
└── pyproject.toml     # Project dependencies
```
