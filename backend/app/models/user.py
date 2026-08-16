import enum
import uuid

from sqlalchemy import Column, String, Enum, DateTime, func

from app.core.database import Base


class UserRole(str, enum.Enum):
    learner = "learner"
    admin = "admin"


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.learner)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
