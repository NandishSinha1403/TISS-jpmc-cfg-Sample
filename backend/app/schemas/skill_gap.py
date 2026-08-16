from pydantic import BaseModel

from app.models.assessment import SkillCategory


class CategoryScore(BaseModel):
    category: SkillCategory
    score_pct: float


class JobReadiness(BaseModel):
    job_id: str
    title: str
    readiness_pct: float
    focus_next: SkillCategory


class SkillGapResponse(BaseModel):
    category_scores: list[CategoryScore]
    job_readiness: list[JobReadiness]


class JobProfileResponse(BaseModel):
    id: str
    title: str
    weights: dict[str, float]
