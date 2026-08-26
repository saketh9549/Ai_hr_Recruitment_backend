from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class InterviewBase(BaseModel):
    candidate_id: int
    job_id: int
    scheduled_at: datetime
    status: str = "scheduled"
    transcript: Optional[str] = None
    notes: Optional[str] = None


class InterviewCreate(InterviewBase):
    pass


class InterviewUpdate(BaseModel):
    scheduled_at: Optional[datetime] = None
    status: Optional[str] = None
    transcript: Optional[str] = None
    notes: Optional[str] = None
    feedback_summary: Optional[str] = None
    feedback_score: Optional[float] = None


class InterviewFeedbackRequest(BaseModel):
    transcript: Optional[str] = None
    notes: Optional[str] = None
    feedback_summary: Optional[str] = None
    feedback_score: Optional[float] = None
    status: Optional[str] = "completed"


class InterviewResponse(InterviewBase):
    id: int
    feedback_summary: Optional[str] = None
    feedback_score: Optional[float] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
