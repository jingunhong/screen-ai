from fastapi import APIRouter

from app.api.routes import auth, projects, experiments, plates, wells

api_router = APIRouter(prefix="/api")

api_router.include_router(auth.router)
api_router.include_router(projects.router)
api_router.include_router(experiments.router)
api_router.include_router(plates.router)
api_router.include_router(wells.router)
