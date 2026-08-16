from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.assessment import Quiz, QuizAttempt
from app.models.course import Course, Module
from app.models.progress import ModuleCompletion
from app.models.user import User


class CourseNotFoundError(Exception):
    pass


class ModuleNotFoundError(Exception):
    pass


def mark_module_complete(db: Session, module_id: str, user: User) -> None:
    if db.query(Module).filter(Module.id == module_id).first() is None:
        raise ModuleNotFoundError(module_id)

    existing = (
        db.query(ModuleCompletion)
        .filter(ModuleCompletion.module_id == module_id, ModuleCompletion.user_id == user.id)
        .first()
    )
    if existing is not None:
        return

    db.add(ModuleCompletion(module_id=module_id, user_id=user.id))
    db.commit()


def get_course_progress(db: Session, course_id: str, user: User) -> dict:
    course = db.query(Course).filter(Course.id == course_id).first()
    if course is None:
        raise CourseNotFoundError(course_id)

    module_ids = [m.id for m in db.query(Module.id).filter(Module.course_id == course_id).all()]
    modules_total = len(module_ids)
    completed_module_ids = (
        [
            row[0]
            for row in db.query(ModuleCompletion.module_id)
            .filter(ModuleCompletion.user_id == user.id, ModuleCompletion.module_id.in_(module_ids))
            .all()
        ]
        if module_ids
        else []
    )
    modules_completed = len(completed_module_ids)
    pct_complete = (modules_completed / modules_total * 100) if modules_total > 0 else 0.0

    quizzes = db.query(Quiz).filter(Quiz.course_id == course_id).all()
    quiz_progress = []
    for quiz in quizzes:
        best_attempt = (
            db.query(QuizAttempt)
            .filter(QuizAttempt.quiz_id == quiz.id, QuizAttempt.user_id == user.id)
            .order_by(QuizAttempt.score_pct.desc())
            .first()
        )
        quiz_progress.append(
            {
                "quiz_id": quiz.id,
                "quiz_title": quiz.title,
                "attempted": best_attempt is not None,
                "best_score_pct": best_attempt.score_pct if best_attempt else None,
                "passed": bool(best_attempt and best_attempt.passed),
            }
        )

    return {
        "course_id": course_id,
        "modules_completed": modules_completed,
        "modules_total": modules_total,
        "pct_complete": pct_complete,
        "completed_module_ids": completed_module_ids,
        "quizzes": quiz_progress,
    }
