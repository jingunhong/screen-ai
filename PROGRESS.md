# Project Progress Tracker

## Current Status: Phase 1 - Foundation (In Progress)

Last updated: 2025-01-29

---

## Phase 1: Foundation

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

### In Progress
- [ ] Create initial migration
- [ ] API routes for hierarchy (CRUD)

### Pending
- [ ] Frontend project setup (React, TypeScript)
- [ ] Docker Compose configuration

---

## Phase 2: Core API & Authentication

### Pending
- [ ] Auth endpoints (login, logout, me)
- [ ] User CRUD
- [ ] Project CRUD with pagination
- [ ] Experiment CRUD (nested under project)
- [ ] Plate CRUD (nested under experiment)
- [ ] Well CRUD (nested under plate)
- [ ] Image endpoints (metadata only, thumbnails)
- [ ] Protected routes middleware

---

## Phase 3: Frontend Foundation

### Pending
- [ ] React + TypeScript + Vite setup
- [ ] API client setup (React Query)
- [ ] Login page
- [ ] Protected route wrapper
- [ ] Navigation/layout components
- [ ] Project list page
- [ ] Experiment list page

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
