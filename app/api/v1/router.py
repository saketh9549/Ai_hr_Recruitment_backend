from fastapi import APIRouter

from app.api.v1 import auth, candidate, feedback, hr, ai, interviews, reports, jobs, resumes, ws

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(auth.router)
api_router.include_router(candidate.router)
api_router.include_router(hr.router)
api_router.include_router(ai.router)
api_router.include_router(interviews.router)
api_router.include_router(reports.router)
api_router.include_router(jobs.router)
api_router.include_router(resumes.router)
api_router.include_router(ws.router)
api_router.include_router(feedback.router)
