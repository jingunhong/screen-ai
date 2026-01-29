from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import api_router
from app.core.config import settings

app = FastAPI(
    title=settings.app_name,
    description="Drug discovery screening data management and analysis platform",
    version="0.1.0",
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Screen AI API", "version": "0.1.0"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


# Include API routes
app.include_router(api_router)
