from fastapi import APIRouter, Depends, UploadFile, File

from app.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/candidate", tags=["Candidate"])


@router.get("/profile")
async def get_profile(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "role": current_user.role,
        "phone": "",
        "location": "",
        "skills": [],
        "experience_years": 0,
        "education": [],
    }


@router.put("/profile")
async def update_profile(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "role": current_user.role,
        "phone": "",
        "location": "",
        "skills": [],
        "experience_years": 0,
        "education": [],
    }


@router.get("/resumes")
async def get_resumes(current_user: User = Depends(get_current_user)):
    return [
        {
            "id": 1,
            "filename": "resume_v1.pdf",
            "uploaded_at": "2024-01-15T10:30:00Z",
            "status": "analyzed",
            "score": 78,
        }
    ]


@router.post("/resumes/upload")
async def upload_resume(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
):
    return {
        "id": 2,
        "filename": file.filename,
        "uploaded_at": "2024-01-16T09:00:00Z",
        "status": "pending",
        "score": None,
    }


@router.get("/resumes/{resumeId}/analysis")
async def get_resume_analysis(resumeId: int, current_user: User = Depends(get_current_user)):
    return {
        "resume_id": resumeId,
        "overall_score": 78,
        "sections": {
            "experience": {"score": 85, "feedback": "Strong relevant experience"},
            "education": {"score": 70, "feedback": "Meets minimum requirements"},
            "skills": {"score": 80, "feedback": "Good technical skill coverage"},
        },
        "keywords_matched": ["python", "fastapi", "sql"],
        "suggestions": ["Add quantifiable achievements", "Include more action verbs"],
    }


@router.get("/applications")
async def get_applications(current_user: User = Depends(get_current_user)):
    return [
        {
            "id": 1,
            "job_id": 1,
            "job_title": "Senior Backend Engineer",
            "company": "TechCorp",
            "status": "under_review",
            "applied_at": "2024-01-10T14:00:00Z",
        }
    ]


@router.post("/applications")
async def create_application(current_user: User = Depends(get_current_user)):
    return {
        "id": 2,
        "job_id": 1,
        "status": "submitted",
        "applied_at": "2024-01-16T10:00:00Z",
    }


@router.get("/saved-jobs")
async def get_saved_jobs(current_user: User = Depends(get_current_user)):
    return [
        {
            "id": 1,
            "title": "Senior Backend Engineer",
            "company": "TechCorp",
            "location": "Remote",
            "saved_at": "2024-01-12T08:00:00Z",
        }
    ]


@router.post("/saved-jobs/{jobId}")
async def save_job(jobId: int, current_user: User = Depends(get_current_user)):
    return {"message": "Job saved successfully", "job_id": jobId}


@router.delete("/saved-jobs/{jobId}")
async def unsave_job(jobId: int, current_user: User = Depends(get_current_user)):
    return {"message": "Job removed from saved", "job_id": jobId}
