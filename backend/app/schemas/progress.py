from pydantic import BaseModel


class ModuleCompletionResponse(BaseModel):
    module_id: str
    completed: bool


class QuizProgress(BaseModel):
    quiz_id: str
    quiz_title: str
    attempted: bool
    best_score_pct: float | None
    passed: bool


class CourseProgressResponse(BaseModel):
    course_id: str
    modules_completed: int
    modules_total: int
    pct_complete: float
    completed_module_ids: list[str]
    quizzes: list[QuizProgress]
