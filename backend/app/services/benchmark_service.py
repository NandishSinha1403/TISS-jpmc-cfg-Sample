"""Peer-benchmarking: plain SQL aggregation, deliberately no ML — percentile
rank against an anonymized cohort is a well-understood, fully explainable
computation and doesn't need a model."""

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.assessment import Quiz, QuizAttempt
from app.models.course import Course
from app.models.user import User


class QuizNotFoundError(Exception):
    pass


class CourseNotFoundError(Exception):
    pass


def _percentile_rank(value: float, population: list[float]) -> float:
    """Mean percentile rank: the fraction of the cohort scoring strictly
    below you, plus half the fraction scoring exactly the same (standard
    tie-handling so identical scores land at the same, centered percentile)."""
    below = sum(1 for v in population if v < value)
    equal = sum(1 for v in population if v == value)
    return round((below + 0.5 * equal) / len(population) * 100, 1)


def get_quiz_benchmark(db: Session, quiz_id: str, user: User) -> dict:
    if db.query(Quiz).filter(Quiz.id == quiz_id).first() is None:
        raise QuizNotFoundError(quiz_id)

    # Best score per user for this quiz — one row per (user_id, max(score_pct)).
    best_scores = (
        db.query(QuizAttempt.user_id, func.max(QuizAttempt.score_pct).label("best"))
        .filter(QuizAttempt.quiz_id == quiz_id)
        .group_by(QuizAttempt.user_id)
        .all()
    )

    cohort = [row.best for row in best_scores]
    your_row = next((row for row in best_scores if row.user_id == user.id), None)

    if your_row is None or not cohort:
        return {"quiz_id": quiz_id, "your_best_score_pct": None, "percentile": None, "cohort_size": len(cohort)}

    return {
        "quiz_id": quiz_id,
        "your_best_score_pct": your_row.best,
        "percentile": _percentile_rank(your_row.best, cohort),
        "cohort_size": len(cohort),
    }


def get_course_benchmark(db: Session, course_id: str, user: User) -> dict:
    if db.query(Course).filter(Course.id == course_id).first() is None:
        raise CourseNotFoundError(course_id)

    quiz_ids = [q.id for q in db.query(Quiz.id).filter(Quiz.course_id == course_id).all()]
    if not quiz_ids:
        return {"course_id": course_id, "your_average_score_pct": None, "percentile": None, "cohort_size": 0}

    # Per user: average of their best score per quiz, across all quizzes in the course.
    best_per_user_quiz = (
        db.query(QuizAttempt.user_id, QuizAttempt.quiz_id, func.max(QuizAttempt.score_pct).label("best"))
        .filter(QuizAttempt.quiz_id.in_(quiz_ids))
        .group_by(QuizAttempt.user_id, QuizAttempt.quiz_id)
        .all()
    )

    totals: dict[str, list[float]] = {}
    for row in best_per_user_quiz:
        totals.setdefault(row.user_id, []).append(row.best)

    averages = {uid: sum(scores) / len(scores) for uid, scores in totals.items()}
    cohort = list(averages.values())
    your_average = averages.get(user.id)

    if your_average is None or not cohort:
        return {"course_id": course_id, "your_average_score_pct": None, "percentile": None, "cohort_size": len(cohort)}

    return {
        "course_id": course_id,
        "your_average_score_pct": round(your_average, 1),
        "percentile": _percentile_rank(your_average, cohort),
        "cohort_size": len(cohort),
    }
