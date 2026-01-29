# Project Progress Tracker

## Current Status: Foundation Phase

Last updated: 2026-01-29

---

## Phase 1: Foundation (Current)

### Completed
- [x] Initial project discussion and scope definition
- [x] Tech stack decision (FastAPI + React + PostgreSQL + S3)
- [x] Data model hierarchy defined (Project → Experiment → Plate → Well → Image)
- [x] Created project documentation (README.md, CLAUDE.md, PROGRESS.md)
- [x] Project scaffolding (backend + frontend structure)
- [x] Database schema design (SQLAlchemy models for all entities)
- [x] Backend project setup (FastAPI, SQLAlchemy, Alembic)
- [x] Frontend project setup (React 19, TypeScript, Vite, Tailwind CSS, Bun)
- [x] Docker Compose configuration (PostgreSQL, backend, frontend)

---

## Phase 2: Core Data Model & API

### Completed
- [x] SQLAlchemy models for: Project, Experiment, Plate, Well, Image, Compound, Analysis, User
- [x] Pydantic schemas for all entities (with base, create, read, update variants)
- [x] CRUD endpoints for all entities (projects, experiments, plates, wells, images, compounds, analyses)
- [x] Pagination support for list endpoints
- [x] API documentation (OpenAPI/Swagger auto-generated at /api/docs)
- [x] Alembic configured with async support

- [x] Initial Alembic migration created (all 8 tables: users, compounds, projects, experiments, plates, wells, images, analyses)
- [x] Fixed circular import issues in SQLAlchemy models (TYPE_CHECKING)

---

## Phase 3: Authentication

### Completed
- [x] User model (SQLAlchemy model and Pydantic schemas)
- [x] Login endpoint (POST /api/auth/login with JWT tokens)
- [x] Logout (client-side token removal - standard for JWT auth)
- [x] JWT-based session management (7-day token expiration)
- [x] Password hashing utilities (bcrypt via passlib)
- [x] Frontend login page (full-featured with AuthProvider context)
- [x] Protected routes (auth middleware on all API endpoints)
- [x] Admin user seeding script

---

## Phase 4: Data Exploration UI

### Pending
- [ ] Project list view
- [ ] Experiment list view (within project)
- [ ] Plate grid view (within experiment)
- [ ] Plate detail view with well heatmap
- [ ] Well detail view with thumbnails
- [ ] Channel color/threshold controls (basic)

---

## Phase 5: Analysis Display

### Pending
- [ ] Analysis data model refinement
- [ ] Z-score heatmap visualization
- [ ] DRC plot component
- [ ] Analysis tab in plate/well views

---

## Phase 6: Thumbnail Pipeline

### Pending
- [ ] Thumbnail generation service
- [ ] S3 integration for thumbnail storage
- [ ] Lazy loading in UI

---

## Future Phases (Out of MVP Scope)

### Phase 7: Full Image Upload
- File upload endpoint with progress tracking
- Background job processing
- Perkin Elmer format support via OMERO/bioformats

### Phase 8: AI-Assisted Analysis
- UI space for AI interaction
- Integration with segmentation tools (Cellpose, etc.)
- Algorithm persistence and reuse
- Batch quantification jobs

### Phase 9: Compound Browser
- Compound detail pages
- Links to related screening data
- Extended compound metadata (structure, MW, etc.)

---

## Architecture Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Python Version | 3.12 | Latest stable, performance improvements |
| Package Manager (Backend) | uv | Fast, modern Python package management |
| Package Manager (Frontend) | Bun | Fast runtime and package manager |
| Backend Framework | FastAPI | Async, modern Python, auto-docs |
| Frontend Framework | React 19 + TypeScript | Industry standard, type safety |
| Frontend Build Tool | Vite | Fast dev server, optimized builds |
| CSS Framework | Tailwind CSS | Utility-first, rapid development |
| Database | PostgreSQL | Robust, JSON support, extensions |
| Image Storage | AWS S3 | Scalable, cost-effective |
| Image Format | TIFF (Perkin Elmer) | Domain standard |
| Plate Format | Flexible (default 384) | Support various plate types |
| Auth | JWT-based | Stateless, simple for MVP |

---

## Open Questions

1. **Thumbnail dimensions**: What size for plate overview vs well detail?
2. **Heatmap color scales**: Predefined or user-configurable?
3. **Analysis data format**: What structure for imported analysis results?
4. **User roles implementation**: RBAC library or custom?

---

## Notes

- Images are heavy - prioritize thumbnail generation over full-resolution display
- Start with prepared/imported data, defer upload pipeline
- Compound model is minimal (ID + name) - extend later
- Single institute deployment initially
