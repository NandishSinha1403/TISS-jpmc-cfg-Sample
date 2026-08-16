import enum
import uuid

from sqlalchemy import Column, String, Text, Integer, Float, Boolean, ForeignKey, DateTime, Enum, JSON, func
from sqlalchemy.orm import relationship

from app.core.database import Base


class Difficulty(str, enum.Enum):
    easy = "easy"
    medium = "medium"
    hard = "hard"


class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    course_id = Column(String, ForeignKey("courses.id"), nullable=False)
    title = Column(String, nullable=False)
    pass_threshold_pct = Column(Float, nullable=False, default=70.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    questions = relationship(
        "Question", back_populates="quiz", cascade="all, delete-orphan", order_by="Question.order_index"
    )


class Question(Base):
    __tablename__ = "questions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    quiz_id = Column(String, ForeignKey("quizzes.id"), nullable=False)
    text = Column(Text, nullable=False)
    options = Column(JSON, nullable=False)  # list[str]
    correct_index = Column(Integer, nullable=False)
    difficulty = Column(Enum(Difficulty), nullable=False, default=Difficulty.medium)
    order_index = Column(Integer, nullable=False, default=0)

    quiz = relationship("Quiz", back_populates="questions")


class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    quiz_id = Column(String, ForeignKey("quizzes.id"), nullable=False)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    score_pct = Column(Float, nullable=False)
    passed = Column(Boolean, nullable=False)
    answers = Column(JSON, nullable=False)  # {question_id: selected_index}
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())
