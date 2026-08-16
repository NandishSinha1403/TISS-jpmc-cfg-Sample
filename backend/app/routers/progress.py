from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.schemas.progress import CourseProgressResponse, ModuleCompletionResponse
from app.services import progress_service

router = APIRouter(tags=["progress"])


@router.post("/modules/{module_id}/complete", response_model=ModuleCompletionResponse)
def complete_module(
    module_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    try:
        progress_service.mark_module_complete(db, module_id, current_user)
    except progress_service.ModuleNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Module not found")
    return ModuleCompletionResponse(module_id=module_id, completed=True)


@router.get("/courses/{course_id}/progress", response_model=CourseProgressResponse)
def get_course_progress(
    course_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    try:
        return progress_service.get_course_progress(db, course_id, current_user)
    except progress_service.CourseNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
