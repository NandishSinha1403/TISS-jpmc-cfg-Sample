from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import Base, engine
from app.models import assessment, course, user  # noqa: F401 — ensures models are registered before create_all
from app.routers import assessments, auth, courses, health

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
