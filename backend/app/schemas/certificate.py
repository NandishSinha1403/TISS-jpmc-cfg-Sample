from datetime import datetime

from pydantic import BaseModel


class CertificateResponse(BaseModel):
    id: str
    user_id: str
    course_id: str
    issued_at: datetime

    model_config = {"from_attributes": True}


class VerifyResponse(BaseModel):
    valid: bool
    certificate_id: str
    learner_name: str
    course_title: str
    issued_at: datetime
