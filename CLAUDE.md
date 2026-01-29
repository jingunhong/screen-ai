# CLAUDE.md - AI Assistant Instructions

## Project Overview

Screen AI is a drug discovery screening data management and analysis platform. It allows researchers to upload, organize, explore, and analyze high-content screening data including cell microscopy images and associated metadata.

## Tech Stack

- **Backend**: Python 3.11+ with FastAPI
- **Frontend**: React (TypeScript)
- **Database**: PostgreSQL
- **Storage**: AWS S3 (images), PostgreSQL (metadata)
- **Authentication**: Simple session-based auth (initially)

## Project Structure (Target)

```
screen-ai/
├── backend/
│   ├── app/
│   │   ├── api/           # FastAPI routes
│   │   ├── models/        # SQLAlchemy models
│   │   ├── schemas/       # Pydantic schemas
│   │   ├── services/      # Business logic
│   │   ├── core/          # Config, security, deps
│   │   └── main.py
│   ├── alembic/           # DB migrations
│   ├── tests/
│   └── pyproject.toml     # uv package management
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/      # API clients
│   │   ├── hooks/
│   │   └── types/
│   └── package.json
├── docker-compose.yml
└── docs/
```

## Data Model Hierarchy

**Strict hierarchy**: Project → Experiment → Plate → Well → Image

- **Project**: Top-level grouping (e.g., "Cancer Cell Line Screening 2024")
- **Experiment**: A screening campaign within a project
- **Plate**: Physical plate (flexible format: 96, 384, 1536-well)
- **Well**: Individual well with coordinates (row, column)
- **Image**: Microscopy image with multiple channels (typically 3: DAPI, GFP, etc.)

## Key Entities

- **Compound**: Referenced by wells, starts with ID only (extend later)
- **Analysis**: Results like cell counts, Z-scores per well
- **DRC (Dose-Response Curve)**: Computed from analysis data across concentrations

## Development Guidelines

### Backend

- Use async SQLAlchemy with PostgreSQL
- Pydantic v2 for request/response schemas
- Alembic for migrations
- Pytest for testing
- Follow RESTful conventions

### Frontend

- React 18+ with TypeScript
- Use React Query for server state
- Component-based architecture
- Tailwind CSS or similar for styling

### API Design

- RESTful endpoints following hierarchy:
  - `/api/projects/{id}/experiments`
  - `/api/experiments/{id}/plates`
  - `/api/plates/{id}/wells`
  - `/api/wells/{id}/images`
- Pagination for list endpoints
- Proper error responses with status codes

## Current Phase: MVP

Focus areas:
1. Data model and API for hierarchy (Project → Experiment → Plate → Well)
2. Simple authentication (login page)
3. Plate visualization with heatmaps
4. Thumbnail generation and display
5. Basic analysis display (prepared data)

**Not in scope for MVP:**
- Full image upload pipeline
- AI-assisted analysis
- Full-resolution image viewing
- Compound management beyond ID

## Commands

```bash
# Backend
cd backend
uv sync                      # Install dependencies
uv run uvicorn app.main:app --reload

# Frontend
cd frontend
npm install
npm run dev

# Database migrations
cd backend
uv run alembic upgrade head

# Add new dependencies
uv add <package-name>
uv add --dev <dev-package>   # For dev dependencies
```

## Testing

- Backend: `pytest` in backend directory
- Frontend: `npm test` in frontend directory

## Notes for AI Assistant

- Always check PROGRESS.md for current state and next tasks
- Follow the strict hierarchy when designing APIs
- Image handling is complex - defer full-resolution display, focus on thumbnails
- Keep compound model simple (ID + name only) for now
- Analysis features use pre-computed data initially
