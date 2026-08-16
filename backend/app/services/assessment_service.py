from sqlalchemy.orm import Session, joinedload

from app.ml.adaptive_difficulty import next_difficulty, pick_next_question
from app.models.assessment import Difficulty, Question, Quiz, QuizAttempt, QuizSession
from app.models.course import Course
from app.models.user import User
from app.schemas.assessment import AdaptiveAnswerSubmission, QuestionCreate, QuizCreate, QuizSubmission


class CourseNotFoundError(Exception):
    pass


class QuizNotFoundError(Exception):
    pass


class SessionNotFoundError(Exception):
    pass


class SessionAlreadyCompletedError(Exception):
    pass


class QuestionNotInQuizError(Exception):
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

    quiz = Quiz(
        course_id=course_id,
        title=data.title,
        pass_threshold_pct=data.pass_threshold_pct,
        adaptive=data.adaptive,
        questions_per_attempt=data.questions_per_attempt,
    )
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


def _score_answers(questions: list[Question], answers: dict[str, int]) -> tuple[int, int, float]:
    total = len(questions)
    correct = sum(
        1 for q in questions if answers.get(q.id) is not None and answers.get(q.id) == q.correct_index
    )
    score_pct = (correct / total * 100) if total > 0 else 0.0
    return correct, total, score_pct


def submit_attempt(db: Session, quiz_id: str, user: User, submission: QuizSubmission) -> QuizAttempt:
    quiz = (
        db.query(Quiz).options(joinedload(Quiz.questions)).filter(Quiz.id == quiz_id).first()
    )
    if quiz is None:
        raise QuizNotFoundError(quiz_id)

    _, _, score_pct = _score_answers(quiz.questions, submission.answers)
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


def start_adaptive_session(db: Session, quiz_id: str, user: User) -> tuple[QuizSession, Question | None]:
    quiz = (
        db.query(Quiz).options(joinedload(Quiz.questions)).filter(Quiz.id == quiz_id).first()
    )
    if quiz is None:
        raise QuizNotFoundError(quiz_id)

    session = QuizSession(
        quiz_id=quiz_id,
        user_id=user.id,
        asked_question_ids=[],
        answers={},
        current_difficulty=Difficulty.medium,
    )
    first_question = pick_next_question(quiz.questions, set(), Difficulty.medium)
    if first_question is not None:
        session.asked_question_ids = [first_question.id]

    db.add(session)
    db.commit()
    db.refresh(session)
    return session, first_question


def answer_adaptive_session(
    db: Session, quiz_id: str, session_id: str, user: User, submission: AdaptiveAnswerSubmission
):
    quiz = (
        db.query(Quiz).options(joinedload(Quiz.questions)).filter(Quiz.id == quiz_id).first()
    )
    if quiz is None:
        raise QuizNotFoundError(quiz_id)

    session = (
        db.query(QuizSession)
        .filter(QuizSession.id == session_id, QuizSession.quiz_id == quiz_id, QuizSession.user_id == user.id)
        .first()
    )
    if session is None:
        raise SessionNotFoundError(session_id)
    if session.completed:
        raise SessionAlreadyCompletedError(session_id)

    question_by_id = {q.id: q for q in quiz.questions}
    question = question_by_id.get(submission.question_id)
    if question is None or submission.question_id not in session.asked_question_ids:
        raise QuestionNotInQuizError(submission.question_id)

    answers = dict(session.answers)
    answers[submission.question_id] = submission.selected_index
    session.answers = answers

    was_correct = submission.selected_index == question.correct_index
    session.current_difficulty = next_difficulty(session.current_difficulty, was_correct)

    reached_target = len(session.asked_question_ids) >= quiz.questions_per_attempt
    next_question = None
    if not reached_target:
        asked_ids = set(session.asked_question_ids)
        next_question = pick_next_question(quiz.questions, asked_ids, session.current_difficulty)
        if next_question is not None:
            session.asked_question_ids = session.asked_question_ids + [next_question.id]

    if next_question is None:
        session.completed = True
        db.add(session)
        db.commit()
        db.refresh(session)

        asked_questions = [q for q in quiz.questions if q.id in session.asked_question_ids]
        correct, total, score_pct = _score_answers(asked_questions, session.answers)
        passed = score_pct >= quiz.pass_threshold_pct
        attempt = QuizAttempt(
            quiz_id=quiz_id,
            user_id=user.id,
            score_pct=score_pct,
            passed=passed,
            answers=session.answers,
        )
        db.add(attempt)
        db.commit()
        return session, None, (correct, total, score_pct, passed)

    db.add(session)
    db.commit()
    db.refresh(session)
    return session, next_question, None
