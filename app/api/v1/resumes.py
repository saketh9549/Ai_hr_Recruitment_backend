from fastapi import APIRouter, Depends

from app.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/resumes", tags=["Resumes"])


@router.get("/{id}")
async def get_resume(id: int, current_user: User = Depends(get_current_user)):
    return {
        "id": id,
        "filename": "resume_v1.pdf",
        "candidate_id": current_user.id,
        "uploaded_at": "2024-01-15T10:30:00Z",
        "status": "analyzed",
        "score": 78,
    }
