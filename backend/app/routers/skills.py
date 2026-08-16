from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.assessment import SkillCategory
from app.models.user import User
from app.schemas.skill_gap import JobProfileResponse, SkillGapResponse
from app.services import skill_service
from app.ml.skill_gap import JOB_PROFILES

router = APIRouter(tags=["skills"])


@router.get(
    "/skills/categories", response_model=list[SkillCategory], dependencies=[Depends(get_current_user)]
)
def list_skill_categories():
    return list(SkillCategory)


@router.get(
    "/skills/jobs", response_model=list[JobProfileResponse], dependencies=[Depends(get_current_user)]
)
def list_job_profiles():
    return [
        {"id": p["id"], "title": p["title"], "weights": {k.value: v for k, v in p["weights"].items()}}
        for p in JOB_PROFILES
    ]


@router.get("/users/me/skill-gap", response_model=SkillGapResponse)
def get_my_skill_gap(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return skill_service.get_skill_gap(db, current_user)
