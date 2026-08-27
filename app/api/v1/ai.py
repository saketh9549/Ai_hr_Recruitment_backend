from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.dependencies import get_current_user
from app.models.user import User
from app.models.resume import Resume
from app.db.session import get_db
from app.ai_integration.resume_parser import parse_resume, load_resume_file_bytes, _extract_skills
from app.ai_integration.embeddings import embed_text
from app.ai_integration.vector_client import upsert_resume_embedding
from app.ai_integration.skill_gap import compute_skill_gap

router = APIRouter(prefix="/ai", tags=["AI"])


@router.post("/resume/analyze/{resumeId}")
async def analyze_resume(
    resumeId: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Resume).where(Resume.id == resumeId))
    resume_row = result.scalar_one_or_none()
    if resume_row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found")

    file_bytes = await load_resume_file_bytes(resume_row.storage_path)
    file_format = resume_row.filename.rsplit(".", 1)[-1].lower()
    parsed = parse_resume(file_bytes, file_format)

    embedding = embed_text(parsed.redacted_text)
    upsert_resume_embedding(
        resumeId, embedding,
        metadata={"candidate_id": resume_row.candidate_id, "skills": ",".join(parsed.skills)},
    )

    overall_score = min(100, 40 + len(parsed.skills) * 8)

    resume_row.extracted_text = parsed.redacted_text
    resume_row.status = "analyzed"
    resume_row.overall_score = overall_score
    await db.commit()

    return {
        "resume_id": resumeId,
        "status": "completed",
        "overall_score": overall_score,
        "ats_score": overall_score,
        "sections": {
            "skills": {"score": overall_score, "feedback": f"Detected skills: {', '.join(parsed.skills) or 'none'}"},
            "experience": {
                "score": 70 if parsed.experience_years else 40,
                "feedback": f"{parsed.experience_years or 'Unknown'} years of experience detected",
            },
            "education": {
                "score": 70 if parsed.education else 40,
                "feedback": "; ".join(parsed.education) or "No education section detected",
            },
        },
        "keywords": parsed.skills,
        "strengths": [f"Has experience with {s}" for s in parsed.skills[:3]],
        "weaknesses": [] if parsed.skills else ["No recognized technical skills found"],
        "suggestions": ["Add more quantifiable achievements", "Include relevant certifications"],
    }


@router.get("/resume/score/{resumeId}")
async def get_resume_score(
    resumeId: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Resume).where(Resume.id == resumeId))
    resume_row = result.scalar_one_or_none()
    if resume_row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found")

    score = resume_row.overall_score if resume_row.overall_score is not None else 50

    return {
        "resume_id": resumeId,
        "overall_score": score,
        "breakdown": {
            "relevance": score,
            "experience": score,
            "skills": score,
            "education": score,
            "formatting": 75,
        },
    }


@router.get("/skill-gap/{candidateId}")
async def get_skill_gap(
    candidateId: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Resume)
        .where(Resume.candidate_id == candidateId)
        .order_by(Resume.uploaded_at.desc())
    )
    resume_row = result.scalars().first()

    if resume_row is None or not resume_row.extracted_text:
        candidate_skills = []
    else:
        candidate_skills = _extract_skills(resume_row.extracted_text)

    return compute_skill_gap(candidateId, candidate_skills)


@router.get("/match/{candidateId}/{jobId}")
async def get_match(candidateId: int, jobId: int, current_user: User = Depends(get_current_user)):
    return {
        "candidate_id": candidateId,
        "job_id": jobId,
        "match_score": 85,
        "matched_skills": ["Python", "FastAPI", "PostgreSQL"],
        "missing_skills": ["Kubernetes", "Terraform"],
        "experience_match": True,
        "education_match": True,
        "summary": "Strong match - candidate meets 85% of requirements",
    }


@router.get("/recommendations/jobs/{candidateId}")
async def recommend_jobs(candidateId: int, current_user: User = Depends(get_current_user)):
    return [
        {"job_id": 1, "title": "Senior Backend Engineer", "company": "TechCorp",
         "match_score": 92, "reason": "Strong alignment with Python and API development experience"},
    ]


@router.get("/recommendations/candidates/{jobId}")
async def recommend_candidates(jobId: int, current_user: User = Depends(get_current_user)):
    return [
        {"candidate_id": 1, "full_name": "Jane Smith", "match_score": 92,
         "top_skills": ["Python", "FastAPI", "AWS"], "experience_years": 6},
    ]


@router.get("/rank-candidates/{jobId}")
async def rank_candidates(jobId: int, current_user: User = Depends(get_current_user)):
    return {
        "job_id": jobId,
        "ranked_candidates": [
            {"rank": 1, "candidate_id": 1, "full_name": "Jane Smith", "score": 92},
        ],
    }


@router.get("/interview-feedback/{interviewId}")
async def get_interview_feedback(interviewId: int, current_user: User = Depends(get_current_user)):
    return {
        "interview_id": interviewId,
        "candidate_name": "Jane Smith",
        "overall_rating": 4.2,
        "strengths": ["Strong technical knowledge"],
        "areas_for_improvement": ["Could elaborate more on system design"],
        "recommendation": "proceed",
        "ai_summary": "Candidate demonstrated solid backend expertise.",
    }