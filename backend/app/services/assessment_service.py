from sqlalchemy.orm import Session, joinedload

from app.models.assessment import Question, Quiz, QuizAttempt
from app.models.course import Course
from app.models.user import User
from app.schemas.assessment import QuestionCreate, QuizCreate, QuizSubmission


class CourseNotFoundError(Exception):
    pass


class QuizNotFoundError(Exception):
    pass


def list_quizzes_for_course(db: Session, course_id: str) -> list[Quiz]:
    return db.query(Quiz).filter(Quiz.course_id == course_id).order_by(Quiz.created_at.desc()).all()


def get_quiz(db: Session, quiz_id: str) -> Quiz:
    quiz = (
        db.query(Quiz).options(joinedload(Quiz.questions)).filter(Quiz.id == quiz_id).first()
    )
    if quiz is None:
        raise QuizNotFoundError(quiz_id)
    return quiz


def create_quiz(db: Session, course_id: str, data: QuizCreate) -> Quiz:
    if db.query(Course).filter(Course.id == course_id).first() is None:
        raise CourseNotFoundError(course_id)

    quiz = Quiz(course_id=course_id, title=data.title, pass_threshold_pct=data.pass_threshold_pct)
    db.add(quiz)
    db.commit()
    db.refresh(quiz)
    return quiz


def add_question(db: Session, quiz_id: str, data: QuestionCreate) -> Question:
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if quiz is None:
        raise QuizNotFoundError(quiz_id)

    question = Question(quiz_id=quiz_id, **data.model_dump())
    db.add(question)
    db.commit()
    db.refresh(question)
    return question


def submit_attempt(db: Session, quiz_id: str, user: User, submission: QuizSubmission) -> QuizAttempt:
    quiz = (
        db.query(Quiz).options(joinedload(Quiz.questions)).filter(Quiz.id == quiz_id).first()
    )
    if quiz is None:
        raise QuizNotFoundError(quiz_id)

    total = len(quiz.questions)
    correct = 0
    for question in quiz.questions:
        selected = submission.answers.get(question.id)
        if selected is not None and selected == question.correct_index:
            correct += 1

    score_pct = (correct / total * 100) if total > 0 else 0.0
    passed = score_pct >= quiz.pass_threshold_pct

    attempt = QuizAttempt(
        quiz_id=quiz_id,
        user_id=user.id,
        score_pct=score_pct,
        passed=passed,
        answers=submission.answers,
    )
    db.add(attempt)
    db.commit()
    db.refresh(attempt)
    return attempt
