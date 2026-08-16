from pydantic import BaseModel


class QuizBenchmarkResponse(BaseModel):
    quiz_id: str
    your_best_score_pct: float | None
    percentile: float | None
    cohort_size: int


class CourseBenchmarkResponse(BaseModel):
    course_id: str
    your_average_score_pct: float | None
    percentile: float | None
    cohort_size: int
