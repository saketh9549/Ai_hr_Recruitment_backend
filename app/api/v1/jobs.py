from fastapi import APIRouter

router = APIRouter(prefix="/jobs", tags=["Jobs"])


@router.get("")
async def list_jobs():
    return [
        {
            "id": 1,
            "title": "Senior Backend Engineer",
            "department": "Engineering",
            "location": "Remote",
            "type": "full_time",
            "status": "open",
            "description": "We are looking for a senior backend engineer...",
            "posted_at": "2024-01-05T09:00:00Z",
        },
        {
            "id": 2,
            "title": "Product Designer",
            "department": "Design",
            "location": "New York, NY",
            "type": "full_time",
            "status": "open",
            "description": "Join our design team...",
            "posted_at": "2024-01-08T11:00:00Z",
        },
    ]


@router.get("/{id}")
async def get_job(id: int):
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
        "posted_at": "2024-01-05T09:00:00Z",
    }
