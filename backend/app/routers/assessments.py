from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user, require_role
from app.models.user import User, UserRole
from app.schemas.assessment import (
    AdaptiveAnswerSubmission,
    AdaptiveSessionResult,
    AdaptiveSessionState,
    QuestionAdminResponse,
    QuestionCreate,
    QuizAdminDetailResponse,
    QuizCreate,
    QuizLearnerDetailResponse,
    QuizListResponse,
    QuizResultResponse,
    QuizSubmission,
)
from app.services import assessment_service, certificate_service

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

    learner_view = QuizLearnerDetailResponse.model_validate(quiz)
    if quiz.adaptive:
        # Adaptive quizzes don't expose the full question pool up front —
        # questions are revealed one at a time via /start and /sessions/.../answer.
        learner_view.questions = []
    return learner_view


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

    certificate_service.check_and_issue_certificate(db, quiz.course_id, current_user)

    return QuizResultResponse(
        quiz_id=quiz_id,
        score_pct=attempt.score_pct,
        passed=attempt.passed,
        correct_count=correct_count,
        total_questions=len(quiz.questions),
        questions=assessment_service.build_question_review(quiz.questions, attempt.answers),
    )


@router.post("/quizzes/{quiz_id}/start", response_model=AdaptiveSessionState)
def start_adaptive_quiz(
    quiz_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    try:
        session, question = assessment_service.start_adaptive_session(db, quiz_id, current_user)
    except assessment_service.QuizNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quiz not found")

    if question is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="This quiz has no questions yet"
        )

    quiz = assessment_service.get_quiz(db, quiz_id)
    return AdaptiveSessionState(
        session_id=session.id,
        question=question,
        question_number=1,
        total_questions=min(quiz.questions_per_attempt, len(quiz.questions)),
    )


@router.post("/quizzes/{quiz_id}/sessions/{session_id}/answer")
def answer_adaptive_quiz(
    quiz_id: str,
    session_id: str,
    submission: AdaptiveAnswerSubmission,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        session, next_question, final = assessment_service.answer_adaptive_session(
            db, quiz_id, session_id, current_user, submission
        )
    except assessment_service.QuizNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quiz not found")
    except assessment_service.SessionNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
    except assessment_service.SessionAlreadyCompletedError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Session already completed")
    except assessment_service.QuestionNotInQuizError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Question does not belong to this session"
        )

    if final is not None:
        correct_count, total_questions, score_pct, passed = final
        quiz = assessment_service.get_quiz(db, quiz_id)
        certificate_service.check_and_issue_certificate(db, quiz.course_id, current_user)
        asked_questions = [q for q in quiz.questions if q.id in session.asked_question_ids]
        return AdaptiveSessionResult(
            session_id=session.id,
            result=QuizResultResponse(
                quiz_id=quiz_id,
                score_pct=score_pct,
                passed=passed,
                correct_count=correct_count,
                total_questions=total_questions,
                questions=assessment_service.build_question_review(asked_questions, session.answers),
            ),
        )

    quiz = assessment_service.get_quiz(db, quiz_id)
    return AdaptiveSessionState(
        session_id=session.id,
        question=next_question,
        question_number=len(session.asked_question_ids),
        total_questions=min(quiz.questions_per_attempt, len(quiz.questions)),
    )
