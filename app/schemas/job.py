from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class JobBase(BaseModel):
    title: str
    description: str
    required_skills: Optional[str] = None
    min_experience_years: int = 0
    department: Optional[str] = None
    status: str = "open"


class JobCreate(JobBase):
    pass


class JobUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    required_skills: Optional[str] = None
    min_experience_years: Optional[int] = None
    department: Optional[str] = None
    status: Optional[str] = None


class JobResponse(JobBase):
    id: int
    posted_by: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
