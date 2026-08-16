from sqlalchemy.orm import Session

from app.ml.practice_questions import PracticeQuestionGenerationError, generate_practice_questions
from app.models.course import Module

MAX_QUESTIONS_PER_REQUEST = 10


class ModuleNotFoundError(Exception):
    pass


def generate_for_module(db: Session, module_id: str, count: int) -> list[dict]:
    module = db.query(Module).filter(Module.id == module_id).first()
    if module is None:
        raise ModuleNotFoundError(module_id)

    count = max(1, min(count, MAX_QUESTIONS_PER_REQUEST))

    # PracticeQuestionGenerationError propagates to the router as-is — this
    # service adds no extra try/except, it only owns fetching the module
    # and bounding the requested count.
    return generate_practice_questions(module.title, module.content, count)
