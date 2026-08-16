from sqlalchemy.orm import Session

from app.ml.skill_gap import compute_category_scores, compute_job_readiness
from app.models.assessment import Quiz, QuizAttempt
from app.models.user import User


def get_skill_gap(db: Session, user: User) -> dict:
    tagged_quizzes = db.query(Quiz).filter(Quiz.skill_category.isnot(None)).all()

    best_scores_by_category = []
    for quiz in tagged_quizzes:
        best_attempt = (
            db.query(QuizAttempt)
            .filter(QuizAttempt.quiz_id == quiz.id, QuizAttempt.user_id == user.id)
            .order_by(QuizAttempt.score_pct.desc())
            .first()
        )
        if best_attempt is not None:
            best_scores_by_category.append((quiz.skill_category, best_attempt.score_pct))

    category_scores = compute_category_scores(best_scores_by_category)
    job_readiness = compute_job_readiness(category_scores)

    return {
        "category_scores": [
            {"category": category, "score_pct": round(score, 1)}
            for category, score in category_scores.items()
        ],
        "job_readiness": job_readiness,
    }
