# Project Progress Tracker

## Current Status: Phase 3 - Frontend Foundation (In Progress)

Last updated: 2025-01-29

---

## Phase 1: Foundation - COMPLETED

### Completed
- [x] Initial project discussion and scope definition
- [x] Tech stack decision (FastAPI + React + PostgreSQL + S3 + uv)
- [x] Data model hierarchy defined (Project → Experiment → Plate → Well → Image)
- [x] Created project documentation (README.md, CLAUDE.md, PROGRESS.md)
- [x] Backend project setup with uv
- [x] FastAPI application structure
- [x] Database models created:
  - User (authentication)
  - Project
  - Experiment
  - Plate (flexible format: 96, 384, 1536-well)
  - Well (position, compound, concentration)
  - Compound (simple: ID + name)
  - Image (S3 keys, channels, metadata)
  - WellAnalysis (cell count, viability, z-score, extensible metrics)
  - DoseResponseCurve (IC50, EC50, hill slope, data points)
- [x] Alembic migrations setup (async)
- [x] Initial database migration created

---

## Phase 2: Core API & Authentication - COMPLETED

### Completed
- [x] Auth endpoints (login, register, me)
- [x] JWT-based authentication with dependency injection
- [x] Project CRUD with pagination
- [x] Experiment CRUD (nested under project)
- [x] Plate CRUD (nested under experiment)
- [x] Well CRUD (nested under plate)
- [x] Plate grid endpoint for heatmap data
- [x] Well thumbnails endpoint
- [x] Protected routes middleware

---

## Phase 3: Frontend Foundation - IN PROGRESS

### Completed
- [x] React + TypeScript + Vite setup
- [x] Tailwind CSS configuration
- [x] API client setup with axios
- [x] React Query for server state
- [x] Authentication context
- [x] Login page
- [x] Protected route wrapper
- [x] Navigation/layout components
- [x] Project list page with create/delete

### Pending
- [ ] Project detail page
- [ ] Experiment list page
- [ ] Plate list page

---

## Phase 4: Plate Visualization

### Pending
- [ ] Plate grid component
- [ ] Well heatmap (color by metric)
- [ ] Well tooltip (compound, concentration, metrics)
- [ ] Click well → detail view
- [ ] Thumbnail grid for well images

---

## Phase 5: Analysis Display

### Pending
- [ ] Z-score heatmap on plate view
- [ ] Analysis tab in well detail
- [ ] DRC plot component (Chart.js or similar)
- [ ] Metrics table display

---

## Future Phases (Out of MVP Scope)

### Phase 6: Thumbnail Pipeline
- Thumbnail generation service
- S3 integration for thumbnail storage
- Lazy loading in UI

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
| Package Manager | uv | Fast, modern Python packaging |
| Backend Framework | FastAPI | Async, modern Python, auto-docs |
| Frontend Framework | React + TypeScript | Industry standard, type safety |
| Frontend Build | Vite | Fast dev server, HMR |
| State Management | React Query | Server state caching, refetch |
| CSS | Tailwind CSS | Utility-first, rapid prototyping |
| Database | PostgreSQL | Robust, JSON support, extensions |
| Image Storage | AWS S3 | Scalable, cost-effective |
| Image Format | TIFF (Perkin Elmer) | Domain standard |
| Plate Format | Flexible (default 384) | Support various plate types |
| Auth | JWT tokens | Simple for single-tenant MVP |
| ORM | SQLAlchemy 2.0 (async) | Modern async support |
| Migrations | Alembic | Standard for SQLAlchemy |

---

## Data Model Summary

```
User
  └── owns → Project
                └── contains → Experiment
                                  └── contains → Plate (rows × columns)
                                                    └── contains → Well (row, col)
                                                                     ├── has → Image[] (channels, fields)
                                                                     ├── has → WellAnalysis
                                                                     └── references → Compound

DoseResponseCurve
  └── links Experiment ↔ Compound
```

---

## API Endpoints

### Auth
- `POST /api/auth/login` - Login with email/password
- `POST /api/auth/register` - Register new user
- `GET /api/auth/me` - Get current user

### Projects
- `GET /api/projects` - List projects (paginated)
- `POST /api/projects` - Create project
- `GET /api/projects/{id}` - Get project
- `PATCH /api/projects/{id}` - Update project
- `DELETE /api/projects/{id}` - Delete project

### Experiments
- `GET /api/projects/{id}/experiments` - List experiments
- `POST /api/projects/{id}/experiments` - Create experiment
- `GET /api/projects/{id}/experiments/{id}` - Get experiment
- `PATCH /api/projects/{id}/experiments/{id}` - Update experiment
- `DELETE /api/projects/{id}/experiments/{id}` - Delete experiment

### Plates
- `GET /api/experiments/{id}/plates` - List plates
- `POST /api/experiments/{id}/plates` - Create plate
- `GET /api/experiments/{id}/plates/{id}` - Get plate
- `GET /api/experiments/{id}/plates/{id}/grid` - Get plate grid for heatmap
- `PATCH /api/experiments/{id}/plates/{id}` - Update plate
- `DELETE /api/experiments/{id}/plates/{id}` - Delete plate

### Wells
- `GET /api/plates/{id}/wells` - List wells
- `POST /api/plates/{id}/wells` - Create well
- `GET /api/plates/{id}/wells/{id}` - Get well with compound
- `GET /api/plates/{id}/wells/{id}/thumbnails` - Get well image thumbnails
- `PATCH /api/plates/{id}/wells/{id}` - Update well
- `DELETE /api/plates/{id}/wells/{id}` - Delete well

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
- AI-assisted analysis UI space reserved but deferred
