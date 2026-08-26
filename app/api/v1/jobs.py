from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.models.job import Job
from app.schemas.job import JobResponse

router = APIRouter(prefix="/jobs", tags=["Jobs"])


@router.get("", response_model=List[JobResponse])
async def list_jobs(
    status: Optional[str] = Query(None, description="Filter by job status (e.g. open, closed, draft)"),
    department: Optional[str] = Query(None, description="Filter by department"),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Job)
    if status:
        stmt = stmt.where(Job.status == status)
    else:
        stmt = stmt.where(Job.status == "open")
    if department:
        stmt = stmt.where(Job.department == department)
    
    stmt = stmt.order_by(Job.created_at.desc())
    result = await db.execute(stmt)
    jobs = result.scalars().all()
    return jobs


@router.get("/{id}", response_model=JobResponse)
async def get_job(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Job).where(Job.id == id))
    job = result.scalar_one_or_none()
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    return job
