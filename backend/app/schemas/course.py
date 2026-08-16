from datetime import datetime

from pydantic import BaseModel, field_validator


class ModuleCreate(BaseModel):
    title: str
    content: str = ""
    order_index: int = 0

    @field_validator("title")
    @classmethod
    def title_not_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("title must not be blank")
        return v.strip()


class ModuleUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    order_index: int | None = None


class ModuleResponse(BaseModel):
    id: str
    course_id: str
    title: str
    content: str
    order_index: int

    model_config = {"from_attributes": True}


class CourseCreate(BaseModel):
    title: str
    description: str = ""

    @field_validator("title")
    @classmethod
    def title_not_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("title must not be blank")
        return v.strip()


class CourseUpdate(BaseModel):
    title: str | None = None
    description: str | None = None


class CourseListResponse(BaseModel):
    id: str
    title: str
    description: str
    created_at: datetime

    model_config = {"from_attributes": True}


class CourseDetailResponse(CourseListResponse):
    modules: list[ModuleResponse] = []
