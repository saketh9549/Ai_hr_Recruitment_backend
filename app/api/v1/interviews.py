from fastapi import APIRouter, Depends

from app.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/interviews", tags=["Interviews"])


@router.get("/schedule")
async def get_schedule(current_user: User = Depends(get_current_user)):
    return [
        {
            "id": 1,
            "candidate_name": "Jane Smith",
            "job_title": "Senior Backend Engineer",
            "scheduled_at": "2024-01-20T14:00:00Z",
            "duration_minutes": 60,
            "type": "technical",
            "status": "scheduled",
            "interviewer": "Mike Johnson",
        },
        {
            "id": 2,
            "candidate_name": "John Doe",
            "job_title": "Product Designer",
            "scheduled_at": "2024-01-21T10:00:00Z",
            "duration_minutes": 45,
            "type": "behavioral",
            "status": "scheduled",
            "interviewer": "Sarah Lee",
        },
    ]


@router.get("/results")
async def get_results(current_user: User = Depends(get_current_user)):
    return [
        {
            "id": 1,
            "candidate_name": "Jane Smith",
            "job_title": "Senior Backend Engineer",
            "interview_date": "2024-01-15T14:00:00Z",
            "overall_rating": 4.2,
            "recommendation": "proceed",
            "interviewer": "Mike Johnson",
        },
    ]


@router.get("/{id}")
async def get_interview(id: int, current_user: User = Depends(get_current_user)):
    return {
        "id": id,
        "candidate_id": 1,
        "candidate_name": "Jane Smith",
        "job_id": 1,
        "job_title": "Senior Backend Engineer",
        "scheduled_at": "2024-01-20T14:00:00Z",
        "duration_minutes": 60,
        "type": "technical",
        "status": "scheduled",
        "interviewer": "Mike Johnson",
        "notes": "",
        "meeting_link": "https://meet.example.com/abc123",
    }


@router.post("")
async def create_interview(current_user: User = Depends(get_current_user)):
    return {
        "id": 3,
        "status": "scheduled",
        "scheduled_at": "2024-01-22T15:00:00Z",
        "created_at": "2024-01-16T10:00:00Z",
    }


@router.put("/{id}")
async def update_interview(id: int, current_user: User = Depends(get_current_user)):
    return {"id": id, "status": "rescheduled", "updated_at": "2024-01-16T10:00:00Z"}


@router.delete("/{id}")
async def delete_interview(id: int, current_user: User = Depends(get_current_user)):
    return {"message": "Interview cancelled successfully"}


@router.post("/{interviewId}/feedback")
async def submit_feedback(interviewId: int, current_user: User = Depends(get_current_user)):
    return {
        "interview_id": interviewId,
        "feedback_submitted": True,
        "submitted_at": "2024-01-20T15:30:00Z",
    }
