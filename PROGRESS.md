# Project Progress Tracker

## Current Status: Planning Phase

Last updated: 2025-01-29

---

## Phase 1: Foundation (Current)

### Completed
- [x] Initial project discussion and scope definition
- [x] Tech stack decision (FastAPI + React + PostgreSQL + S3)
- [x] Data model hierarchy defined (Project → Experiment → Plate → Well → Image)
- [x] Created project documentation (README.md, CLAUDE.md, PROGRESS.md)

### In Progress
- [ ] Project scaffolding (backend + frontend structure)

### Pending
- [ ] Database schema design
- [ ] Backend project setup (FastAPI, SQLAlchemy, Alembic)
- [ ] Frontend project setup (React, TypeScript)
- [ ] Docker Compose configuration

---

## Phase 2: Core Data Model & API

### Pending
- [ ] SQLAlchemy models for: Project, Experiment, Plate, Well, Image, Compound, Analysis
- [ ] Alembic migrations
- [ ] CRUD endpoints for all entities
- [ ] API documentation (OpenAPI/Swagger)

---

## Phase 3: Authentication

### Pending
- [ ] User model
- [ ] Login/logout endpoints
- [ ] Session management
- [ ] Frontend login page
- [ ] Protected routes

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
| Backend Framework | FastAPI | Async, modern Python, auto-docs |
| Frontend Framework | React + TypeScript | Industry standard, type safety |
| Database | PostgreSQL | Robust, JSON support, extensions |
| Image Storage | AWS S3 | Scalable, cost-effective |
| Image Format | TIFF (Perkin Elmer) | Domain standard |
| Plate Format | Flexible (default 384) | Support various plate types |
| Auth | Session-based | Simple for single-tenant MVP |

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
