from fastapi import APIRouter, Depends

from app.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/hr", tags=["HR"])


@router.get("/jobs")
async def get_jobs(current_user: User = Depends(get_current_user)):
    return [
        {
            "id": 1,
            "title": "Senior Backend Engineer",
            "department": "Engineering",
            "location": "Remote",
            "type": "full_time",
            "status": "open",
            "applicants_count": 12,
            "created_at": "2024-01-05T09:00:00Z",
        },
        {
            "id": 2,
            "title": "Product Designer",
            "department": "Design",
            "location": "New York, NY",
            "type": "full_time",
            "status": "open",
            "applicants_count": 8,
            "created_at": "2024-01-08T11:00:00Z",
        },
    ]


@router.get("/jobs/{id}")
async def get_job(id: int, current_user: User = Depends(get_current_user)):
    return {
        "id": id,
        "title": "Senior Backend Engineer",
        "department": "Engineering",
        "location": "Remote",
        "type": "full_time",
        "status": "open",
        "description": "We are looking for a senior backend engineer...",
        "requirements": ["5+ years Python", "FastAPI or Django", "SQL databases"],
        "salary_range": {"min": 120000, "max": 180000, "currency": "USD"},
        "applicants_count": 12,
        "created_at": "2024-01-05T09:00:00Z",
    }


@router.post("/jobs")
async def create_job(current_user: User = Depends(get_current_user)):
    return {
        "id": 3,
        "title": "New Position",
        "status": "draft",
        "created_at": "2024-01-16T10:00:00Z",
    }


@router.put("/jobs/{id}")
async def update_job(id: int, current_user: User = Depends(get_current_user)):
    return {"id": id, "title": "Updated Position", "status": "open"}


@router.delete("/jobs/{id}")
async def delete_job(id: int, current_user: User = Depends(get_current_user)):
    return {"message": "Job deleted successfully"}


@router.get("/candidates")
async def get_candidates(current_user: User = Depends(get_current_user)):
    return [
        {
            "id": 1,
            "full_name": "Jane Smith",
            "email": "jane@example.com",
            "status": "under_review",
            "applied_for": "Senior Backend Engineer",
            "match_score": 85,
            "applied_at": "2024-01-10T14:00:00Z",
        },
        {
            "id": 2,
            "full_name": "John Doe",
            "email": "john@example.com",
            "status": "shortlisted",
            "applied_for": "Product Designer",
            "match_score": 72,
            "applied_at": "2024-01-11T09:30:00Z",
        },
    ]


@router.get("/candidates/{id}")
async def get_candidate(id: int, current_user: User = Depends(get_current_user)):
    return {
        "id": id,
        "full_name": "Jane Smith",
        "email": "jane@example.com",
        "phone": "+1-555-0100",
        "status": "under_review",
        "skills": ["Python", "FastAPI", "PostgreSQL"],
        "experience_years": 6,
        "resumes": [{"id": 1, "filename": "resume_v1.pdf", "score": 78}],
        "applications": [
            {"job_id": 1, "job_title": "Senior Backend Engineer", "status": "under_review"}
        ],
    }


@router.patch("/candidates/{id}/status")
async def update_candidate_status(id: int, current_user: User = Depends(get_current_user)):
    return {"id": id, "status": "shortlisted", "updated_at": "2024-01-16T10:00:00Z"}


@router.get("/metrics")
async def get_metrics(current_user: User = Depends(get_current_user)):
    return {
        "total_jobs": 15,
        "active_jobs": 8,
        "total_candidates": 142,
        "new_applications_today": 5,
        "interviews_scheduled": 12,
        "offers_pending": 3,
        "avg_time_to_hire": 21,
    }


@router.get("/analytics")
async def get_analytics(current_user: User = Depends(get_current_user)):
    return {
        "applications_by_month": [
            {"month": "2024-01", "count": 45},
            {"month": "2023-12", "count": 38},
            {"month": "2023-11", "count": 52},
        ],
        "top_sources": [
            {"source": "LinkedIn", "count": 65},
            {"source": "Direct", "count": 40},
            {"source": "Referral", "count": 25},
        ],
        "pipeline_stages": {
            "applied": 50,
            "screening": 30,
            "interview": 15,
            "offer": 5,
            "hired": 3,
        },
    }


@router.post("/reports")
async def generate_report(current_user: User = Depends(get_current_user)):
    return {
        "id": 1,
        "type": "hiring_summary",
        "status": "generated",
        "generated_at": "2024-01-16T10:00:00Z",
        "download_url": "/api/v1/reports/1/download",
    }
