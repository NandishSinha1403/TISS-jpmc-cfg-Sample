from pydantic import BaseModel, Field


class PracticeQuestionRequest(BaseModel):
    count: int = Field(default=5, ge=1, le=10)


class PracticeQuestionItem(BaseModel):
    text: str
    options: list[str]
    correct_index: int


class PracticeQuestionResponse(BaseModel):
    module_id: str
    questions: list[PracticeQuestionItem]
