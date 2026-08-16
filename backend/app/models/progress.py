import uuid

from sqlalchemy import Column, String, ForeignKey, DateTime, UniqueConstraint, func

from app.core.database import Base


class ModuleCompletion(Base):
    """A learner marking a module as done. Learner-initiated, not inferred."""

    __tablename__ = "module_completions"
    __table_args__ = (UniqueConstraint("user_id", "module_id", name="uq_user_module"),)

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    module_id = Column(String, ForeignKey("modules.id"), nullable=False)
    completed_at = Column(DateTime(timezone=True), server_default=func.now())
