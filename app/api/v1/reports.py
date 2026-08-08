from fastapi import APIRouter, Depends

from app.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get("")
async def get_reports(current_user: User = Depends(get_current_user)):
    return [
        {
            "id": 1,
            "type": "hiring_summary",
            "title": "Q1 Hiring Report",
            "generated_at": "2024-01-15T10:00:00Z",
            "status": "ready",
        },
    ]


@router.get("/{id}")
async def get_report(id: int, current_user: User = Depends(get_current_user)):
    return {
        "id": id,
        "type": "hiring_summary",
        "title": "Q1 Hiring Report",
        "generated_at": "2024-01-15T10:00:00Z",
        "status": "ready",
        "data": {
            "total_hires": 5,
            "avg_time_to_hire": 21,
            "top_sources": ["LinkedIn", "Referral"],
        },
    }
