from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user, require_role
from app.models.user import User, UserRole
from app.schemas.assessment import (
    QuestionAdminResponse,
    QuestionCreate,
    QuizAdminDetailResponse,
    QuizCreate,
    QuizLearnerDetailResponse,
    QuizListResponse,
    QuizResultResponse,
    QuizSubmission,
)
from app.services import assessment_service

router = APIRouter(tags=["assessments"])

admin_only = require_role(UserRole.admin)


@router.get(
    "/courses/{course_id}/quizzes",
    response_model=list[QuizListResponse],
    dependencies=[Depends(get_current_user)],
)
def list_quizzes(course_id: str, db: Session = Depends(get_db)):
    return assessment_service.list_quizzes_for_course(db, course_id)


@router.post(
    "/courses/{course_id}/quizzes",
    response_model=QuizListResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(admin_only)],
)
def create_quiz(course_id: str, data: QuizCreate, db: Session = Depends(get_db)):
    try:
        return assessment_service.create_quiz(db, course_id, data)
    except assessment_service.CourseNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")


@router.get("/quizzes/{quiz_id}")
def get_quiz(quiz_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        quiz = assessment_service.get_quiz(db, quiz_id)
    except assessment_service.QuizNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quiz not found")

    if current_user.role == UserRole.admin:
        return QuizAdminDetailResponse.model_validate(quiz)
    return QuizLearnerDetailResponse.model_validate(quiz)


@router.post(
    "/quizzes/{quiz_id}/questions",
    response_model=QuestionAdminResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(admin_only)],
)
def add_question(quiz_id: str, data: QuestionCreate, db: Session = Depends(get_db)):
    try:
        return assessment_service.add_question(db, quiz_id, data)
    except assessment_service.QuizNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quiz not found")


@router.post("/quizzes/{quiz_id}/submit", response_model=QuizResultResponse)
def submit_quiz(
    quiz_id: str,
    submission: QuizSubmission,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        attempt = assessment_service.submit_attempt(db, quiz_id, current_user, submission)
    except assessment_service.QuizNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quiz not found")

    quiz = assessment_service.get_quiz(db, quiz_id)
    correct_count = round(attempt.score_pct / 100 * len(quiz.questions))

    return QuizResultResponse(
        quiz_id=quiz_id,
        score_pct=attempt.score_pct,
        passed=attempt.passed,
        correct_count=correct_count,
        total_questions=len(quiz.questions),
    )
