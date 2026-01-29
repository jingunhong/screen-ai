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

### Creating Migrations
```bash
uv run alembic revision --autogenerate -m "description"
```

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
