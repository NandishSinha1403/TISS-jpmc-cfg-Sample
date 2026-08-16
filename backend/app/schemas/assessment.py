from datetime import datetime

from pydantic import BaseModel, field_validator

from app.models.assessment import Difficulty


class QuestionCreate(BaseModel):
    text: str
    options: list[str]
    correct_index: int
    difficulty: Difficulty = Difficulty.medium
    order_index: int = 0

    @field_validator("text")
    @classmethod
    def text_not_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("text must not be blank")
        return v.strip()

    @field_validator("options")
    @classmethod
    def at_least_two_options(cls, v: list[str]) -> list[str]:
        if len(v) < 2:
            raise ValueError("a question needs at least 2 options")
        return v

    @field_validator("correct_index")
    @classmethod
    def correct_index_in_range(cls, v: int, info) -> int:
        options = info.data.get("options")
        if options is not None and not (0 <= v < len(options)):
            raise ValueError("correct_index must be a valid index into options")
        return v


class QuestionAdminResponse(BaseModel):
    id: str
    quiz_id: str
    text: str
    options: list[str]
    correct_index: int
    difficulty: Difficulty
    order_index: int

    model_config = {"from_attributes": True}


class QuestionLearnerResponse(BaseModel):
    """Question shape shown while taking a quiz — never includes correct_index."""

    id: str
    text: str
    options: list[str]
    difficulty: Difficulty
    order_index: int

    model_config = {"from_attributes": True}


class QuizCreate(BaseModel):
    title: str
    pass_threshold_pct: float = 70.0

    @field_validator("title")
    @classmethod
    def title_not_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("title must not be blank")
        return v.strip()


class QuizListResponse(BaseModel):
    id: str
    course_id: str
    title: str
    pass_threshold_pct: float
    created_at: datetime

    model_config = {"from_attributes": True}


class QuizAdminDetailResponse(QuizListResponse):
    questions: list[QuestionAdminResponse] = []


class QuizLearnerDetailResponse(QuizListResponse):
    questions: list[QuestionLearnerResponse] = []


class QuizSubmission(BaseModel):
    answers: dict[str, int]  # question_id -> selected option index


class QuizResultResponse(BaseModel):
    quiz_id: str
    score_pct: float
    passed: bool
    correct_count: int
    total_questions: int
