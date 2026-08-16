from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.schemas.benchmark import CourseBenchmarkResponse, QuizBenchmarkResponse
from app.services import benchmark_service

router = APIRouter(tags=["benchmark"])


@router.get("/quizzes/{quiz_id}/benchmark", response_model=QuizBenchmarkResponse)
def get_quiz_benchmark(
    quiz_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    try:
        return benchmark_service.get_quiz_benchmark(db, quiz_id, current_user)
    except benchmark_service.QuizNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quiz not found")


@router.get("/courses/{course_id}/benchmark", response_model=CourseBenchmarkResponse)
def get_course_benchmark(
    course_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    try:
        return benchmark_service.get_course_benchmark(db, course_id, current_user)
    except benchmark_service.CourseNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
