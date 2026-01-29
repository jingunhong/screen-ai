# Screen AI

AI-driven screening data platform for drug discovery research.

## Overview

Screen AI is a web application for managing, exploring, and analyzing high-content screening (HCS) data from drug discovery experiments. It provides researchers with tools to:

- **Organize** screening data in a hierarchical structure (Project → Experiment → Plate → Well)
- **Visualize** plate layouts with heatmaps based on analysis metrics
- **Browse** cell microscopy images with multi-channel support
- **Analyze** screening results with dose-response curves (DRC) and quality metrics (Z-score)
- **Develop** (future) custom image analysis algorithms with AI assistance

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Python 3.12, FastAPI, SQLAlchemy |
| Package Management | uv (Python), Bun (Frontend) |
| Frontend | React 19, TypeScript, Vite, Tailwind CSS |
| Database | PostgreSQL |
| Storage | AWS S3 |
| Containerization | Docker, Docker Compose |

## Data Model

```
Project
└── Experiment
    └── Plate (96, 384, 1536-well)
        └── Well (row, column, compound, concentration)
            └── Image (multi-channel: DAPI, GFP, etc.)
```

## Features

### MVP (Current Focus)
- User authentication (login/logout)
- Project and experiment browsing
- Plate visualization with well heatmaps
- Thumbnail-based image browsing
- Pre-computed analysis display (Z-score, DRC)

### Future
- Large file upload with progress tracking
- Full-resolution image viewing with channel controls
- AI-assisted image analysis algorithm development
- Compound browser with cross-experiment linking
- Batch quantification jobs

## Getting Started

### Prerequisites
- Python 3.12
- uv (Python package manager) - Install: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- Bun (Frontend runtime) - Install: `curl -fsSL https://bun.sh/install | bash`
- PostgreSQL 15+
- Docker & Docker Compose (optional)

### Development Setup

```bash
# Clone repository
git clone <repo-url>
cd screen-ai

# Backend setup
cd backend
uv sync                              # Install dependencies (creates .venv automatically)
uv run uvicorn app.main:app --reload

# Frontend setup (new terminal)
cd frontend
bun install
bun dev
```

### Managing Python Dependencies

```bash
cd backend
uv add <package-name>           # Add a dependency
uv add --dev <package-name>     # Add a dev dependency
uv remove <package-name>        # Remove a dependency
uv sync                         # Sync dependencies from pyproject.toml
```

### Environment Variables

Create `.env` files in backend and frontend directories:

**backend/.env**
```
DATABASE_URL=postgresql://user:password@localhost:5432/screen_ai
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
S3_BUCKET=screen-ai-images
SECRET_KEY=your_secret_key
```

**frontend/.env**
```
VITE_API_URL=http://localhost:8000
```

### Docker Compose

```bash
docker-compose up -d
```

## Project Structure

```
screen-ai/
├── backend/
│   ├── app/
│   │   ├── api/           # API routes
│   │   ├── models/        # Database models
│   │   ├── schemas/       # Pydantic schemas
│   │   ├── services/      # Business logic
│   │   └── core/          # Config, auth, dependencies
│   ├── alembic/           # Database migrations
│   ├── tests/
│   └── pyproject.toml     # Python dependencies (managed by uv)
├── frontend/
│   ├── src/
│   │   ├── components/    # Reusable UI components
│   │   ├── pages/         # Page components
│   │   ├── services/      # API client
│   │   └── hooks/         # Custom React hooks
│   └── public/
├── docs/                   # Additional documentation
├── CLAUDE.md              # AI assistant instructions
├── PROGRESS.md            # Development progress tracker
└── docker-compose.yml
```

## API Documentation

Once the backend is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Contributing

See PROGRESS.md for current development status and planned features.

## License

See LICENSE file.
