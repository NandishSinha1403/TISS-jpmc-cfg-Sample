from sqlalchemy.orm import Session, joinedload

from app.models.course import Course, Module
from app.schemas.course import CourseCreate, CourseUpdate, ModuleCreate, ModuleUpdate


class CourseNotFoundError(Exception):
    pass


class ModuleNotFoundError(Exception):
    pass


def list_courses(db: Session) -> list[Course]:
    return db.query(Course).order_by(Course.created_at.desc()).all()


def get_course(db: Session, course_id: str) -> Course:
    course = (
        db.query(Course)
        .options(joinedload(Course.modules))
        .filter(Course.id == course_id)
        .first()
    )
    if course is None:
        raise CourseNotFoundError(course_id)
    return course


def create_course(db: Session, data: CourseCreate) -> Course:
    course = Course(title=data.title, description=data.description)
    db.add(course)
    db.commit()
    db.refresh(course)
    return course


def update_course(db: Session, course_id: str, data: CourseUpdate) -> Course:
    course = db.query(Course).filter(Course.id == course_id).first()
    if course is None:
        raise CourseNotFoundError(course_id)

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(course, field, value)

    db.commit()
    db.refresh(course)
    return course


def delete_course(db: Session, course_id: str) -> None:
    course = db.query(Course).filter(Course.id == course_id).first()
    if course is None:
        raise CourseNotFoundError(course_id)
    db.delete(course)
    db.commit()


def add_module(db: Session, course_id: str, data: ModuleCreate) -> Module:
    course = db.query(Course).filter(Course.id == course_id).first()
    if course is None:
        raise CourseNotFoundError(course_id)

    module = Module(course_id=course_id, **data.model_dump())
    db.add(module)
    db.commit()
    db.refresh(module)
    return module


def update_module(db: Session, module_id: str, data: ModuleUpdate) -> Module:
    module = db.query(Module).filter(Module.id == module_id).first()
    if module is None:
        raise ModuleNotFoundError(module_id)

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(module, field, value)

    db.commit()
    db.refresh(module)
    return module


def delete_module(db: Session, module_id: str) -> None:
    module = db.query(Module).filter(Module.id == module_id).first()
    if module is None:
        raise ModuleNotFoundError(module_id)
    db.delete(module)
    db.commit()
