from app.schemas.analysis import (
    AnalysisCreate,
    AnalysisRead,
    AnalysisUpdate,
)
from app.schemas.auth import (
    LoginRequest,
    Token,
    TokenPayload,
)
from app.schemas.compound import (
    CompoundCreate,
    CompoundRead,
    CompoundUpdate,
)
from app.schemas.experiment import (
    ExperimentCreate,
    ExperimentRead,
    ExperimentReadWithPlates,
    ExperimentUpdate,
)
from app.schemas.image import (
    ImageCreate,
    ImageRead,
    ImageUpdate,
)
from app.schemas.pagination import PaginatedResponse, PaginationParams
from app.schemas.plate import (
    PlateCreate,
    PlateRead,
    PlateReadWithWells,
    PlateUpdate,
)
from app.schemas.project import (
    ProjectCreate,
    ProjectRead,
    ProjectReadWithExperiments,
    ProjectUpdate,
)
from app.schemas.user import (
    UserCreate,
    UserRead,
    UserUpdate,
)
from app.schemas.well import (
    WellCreate,
    WellRead,
    WellReadWithRelations,
    WellUpdate,
)

# Rebuild models with forward references now that all schemas are imported
ProjectReadWithExperiments.model_rebuild()
ExperimentReadWithPlates.model_rebuild()
PlateReadWithWells.model_rebuild()
WellReadWithRelations.model_rebuild()

__all__ = [
    # Analysis
    "AnalysisCreate",
    "AnalysisRead",
    "AnalysisUpdate",
    # Auth
    "LoginRequest",
    "Token",
    "TokenPayload",
    # Compound
    "CompoundCreate",
    "CompoundRead",
    "CompoundUpdate",
    # Experiment
    "ExperimentCreate",
    "ExperimentRead",
    "ExperimentUpdate",
    # Image
    "ImageCreate",
    "ImageRead",
    "ImageUpdate",
    # Pagination
    "PaginatedResponse",
    "PaginationParams",
    # Plate
    "PlateCreate",
    "PlateRead",
    "PlateUpdate",
    # Project
    "ProjectCreate",
    "ProjectRead",
    "ProjectUpdate",
    # User
    "UserCreate",
    "UserRead",
    "UserUpdate",
    # Well
    "WellCreate",
    "WellRead",
    "WellUpdate",
]
