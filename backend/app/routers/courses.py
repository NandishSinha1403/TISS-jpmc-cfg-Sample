from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user, require_role
from app.models.user import UserRole
from app.schemas.course import (
    CourseCreate,
    CourseDetailResponse,
    CourseListResponse,
    CourseUpdate,
    ModuleCreate,
    ModuleResponse,
    ModuleUpdate,
)
from app.services import course_service

router = APIRouter(prefix="/courses", tags=["courses"])

admin_only = require_role(UserRole.admin)


@router.get("", response_model=list[CourseListResponse], dependencies=[Depends(get_current_user)])
def list_courses(db: Session = Depends(get_db)):
    return course_service.list_courses(db)


@router.get(
    "/{course_id}", response_model=CourseDetailResponse, dependencies=[Depends(get_current_user)]
)
def get_course(course_id: str, db: Session = Depends(get_db)):
    try:
        return course_service.get_course(db, course_id)
    except course_service.CourseNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")


@router.post(
    "",
    response_model=CourseListResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(admin_only)],
)
def create_course(data: CourseCreate, db: Session = Depends(get_db)):
    return course_service.create_course(db, data)


@router.put(
    "/{course_id}", response_model=CourseListResponse, dependencies=[Depends(admin_only)]
)
def update_course(course_id: str, data: CourseUpdate, db: Session = Depends(get_db)):
    try:
        return course_service.update_course(db, course_id, data)
    except course_service.CourseNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")


@router.delete(
    "/{course_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(admin_only)]
)
def delete_course(course_id: str, db: Session = Depends(get_db)):
    try:
        course_service.delete_course(db, course_id)
    except course_service.CourseNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")


@router.post(
    "/{course_id}/modules",
    response_model=ModuleResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(admin_only)],
)
def add_module(course_id: str, data: ModuleCreate, db: Session = Depends(get_db)):
    try:
        return course_service.add_module(db, course_id, data)
    except course_service.CourseNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")


@router.put(
    "/{course_id}/modules/{module_id}",
    response_model=ModuleResponse,
    dependencies=[Depends(admin_only)],
)
def update_module(course_id: str, module_id: str, data: ModuleUpdate, db: Session = Depends(get_db)):
    try:
        return course_service.update_module(db, module_id, data)
    except course_service.ModuleNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Module not found")


@router.delete(
    "/{course_id}/modules/{module_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(admin_only)],
)
def delete_module(course_id: str, module_id: str, db: Session = Depends(get_db)):
    try:
        course_service.delete_module(db, module_id)
    except course_service.ModuleNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Module not found")
