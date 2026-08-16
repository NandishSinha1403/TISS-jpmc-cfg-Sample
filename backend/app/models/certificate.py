import uuid

from sqlalchemy import Column, String, ForeignKey, DateTime, UniqueConstraint, func

from app.core.database import Base


class Certificate(Base):
    __tablename__ = "certificates"
    __table_args__ = (UniqueConstraint("user_id", "course_id", name="uq_user_course_certificate"),)

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    course_id = Column(String, ForeignKey("courses.id"), nullable=False)
    issued_at = Column(DateTime(timezone=True), server_default=func.now())
