from fastapi import APIRouter

from app.api.routes import (
    analyses,
    auth,
    compounds,
    experiments,
    health,
    images,
    plates,
    projects,
    wells,
)

api_router = APIRouter()

api_router.include_router(health.router, tags=["health"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
api_router.include_router(experiments.router, prefix="/experiments", tags=["experiments"])
api_router.include_router(plates.router, prefix="/plates", tags=["plates"])
api_router.include_router(wells.router, prefix="/wells", tags=["wells"])
api_router.include_router(images.router, prefix="/images", tags=["images"])
api_router.include_router(compounds.router, prefix="/compounds", tags=["compounds"])
api_router.include_router(analyses.router, prefix="/analyses", tags=["analyses"])
