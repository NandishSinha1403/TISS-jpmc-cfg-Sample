from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import Base, engine
from app.models import assessment, certificate, course, progress, user  # noqa: F401 — ensures models are registered before create_all
from app.routers import assessments, auth, certificates, courses, health
from app.routers import progress as progress_router

app = FastAPI(title=settings.app_name)

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(auth.router)
app.include_router(courses.router)
app.include_router(assessments.router)
app.include_router(progress_router.router)
app.include_router(certificates.router)
