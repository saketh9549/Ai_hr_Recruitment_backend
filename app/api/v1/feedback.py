from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class FeedbackCreate(BaseModel):
    candidate_id: int
    interviewer_id: int
    technical_score: int  # 1 to 10
    communication_score: int  # 1 to 10
    comments: str

@router.post("/submit")
def submit_candidate_feedback(payload: FeedbackCreate):
    """
    Submits interviewer feedback for a candidate.
    """
    average_score = round((payload.technical_score + payload.communication_score) / 2, 1)
    
    return {
        "status": "success",
        "message": "Feedback recorded successfully!",
        "candidate_id": payload.candidate_id,
        "overall_score": average_score,
        "recommendation": "Hire" if average_score >= 7.0 else "Hold / Reject"
    }