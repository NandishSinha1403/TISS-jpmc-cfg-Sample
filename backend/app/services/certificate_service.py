from sqlalchemy.orm import Session

from app.models.assessment import Quiz, QuizAttempt
from app.models.certificate import Certificate
from app.models.course import Course
from app.models.user import User, UserRole
from app.services.certificate_pdf import render_certificate_pdf


class CertificateNotFoundError(Exception):
    pass


class CourseNotFoundError(Exception):
    pass


def _course_completed(db: Session, course_id: str, user_id: str) -> bool:
    """A course is complete when it has at least one quiz and every quiz
    has a passing best attempt for this user."""
    quiz_ids = [q.id for q in db.query(Quiz.id).filter(Quiz.course_id == course_id).all()]
    if not quiz_ids:
        return False

    for quiz_id in quiz_ids:
        passed = (
            db.query(QuizAttempt)
            .filter(QuizAttempt.quiz_id == quiz_id, QuizAttempt.user_id == user_id, QuizAttempt.passed.is_(True))
            .first()
        )
        if passed is None:
            return False

    return True


def check_and_issue_certificate(db: Session, course_id: str, user: User) -> Certificate | None:
    """Idempotent: call this after every quiz submission. Returns the
    certificate if one exists or was just issued, None if not yet earned."""
    existing = (
        db.query(Certificate)
        .filter(Certificate.course_id == course_id, Certificate.user_id == user.id)
        .first()
    )
    if existing is not None:
        return existing

    if not _course_completed(db, course_id, user.id):
        return None

    certificate = Certificate(user_id=user.id, course_id=course_id)
    db.add(certificate)
    db.commit()
    db.refresh(certificate)
    return certificate


def get_certificate_for_course(db: Session, course_id: str, user: User) -> Certificate | None:
    return (
        db.query(Certificate)
        .filter(Certificate.course_id == course_id, Certificate.user_id == user.id)
        .first()
    )


def get_certificate_pdf(db: Session, certificate_id: str, requesting_user: User) -> bytes:
    certificate = db.query(Certificate).filter(Certificate.id == certificate_id).first()
    is_owner = certificate is not None and certificate.user_id == requesting_user.id
    is_admin = requesting_user.role == UserRole.admin
    if certificate is None or not (is_owner or is_admin):
        raise CertificateNotFoundError(certificate_id)

    learner = db.query(User).filter(User.id == certificate.user_id).first()
    course = db.query(Course).filter(Course.id == certificate.course_id).first()

    return render_certificate_pdf(
        certificate_id=certificate.id,
        learner_name=learner.full_name,
        course_title=course.title,
        issued_at=certificate.issued_at,
    )


def verify_certificate(db: Session, certificate_id: str) -> dict:
    certificate = db.query(Certificate).filter(Certificate.id == certificate_id).first()
    if certificate is None:
        raise CertificateNotFoundError(certificate_id)

    learner = db.query(User).filter(User.id == certificate.user_id).first()
    course = db.query(Course).filter(Course.id == certificate.course_id).first()

    return {
        "valid": True,
        "certificate_id": certificate.id,
        "learner_name": learner.full_name,
        "course_title": course.title,
        "issued_at": certificate.issued_at,
    }
