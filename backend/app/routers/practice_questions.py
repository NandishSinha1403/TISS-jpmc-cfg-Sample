from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.ml.practice_questions import PracticeQuestionGenerationError
from app.schemas.practice_question import PracticeQuestionRequest, PracticeQuestionResponse
from app.services import practice_question_service

router = APIRouter(tags=["practice-questions"])


@router.post("/modules/{module_id}/practice-questions", response_model=PracticeQuestionResponse)
def generate_practice_questions(
    module_id: str,
    data: PracticeQuestionRequest = PracticeQuestionRequest(),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        questions = practice_question_service.generate_for_module(db, module_id, data.count)
    except practice_question_service.ModuleNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Module not found")
    except PracticeQuestionGenerationError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Practice questions are unavailable right now. Please try again shortly.",
        )

    return PracticeQuestionResponse(module_id=module_id, questions=questions)
