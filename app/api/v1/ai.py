from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_current_user
from app.db.session import get_db

from app.models.user import User
from app.models.resume import Resume

from app.ai_integration.resume_integrity import check_resume_integrity


router = APIRouter(prefix="/ai", tags=["AI"])


# ============================================================
# 1. RESUME ANALYSIS
# ============================================================

@router.post("/resume/analyze/{resumeId}")
async def analyze_resume(
    resumeId: int,
    current_user: User = Depends(get_current_user)
):
    return {
        "resume_id": resumeId,
        "status": "completed",
        "overall_score": 78,
        "ats_score": 82,
        "sections": {
            "experience": {
                "score": 85,
                "feedback": "Strong relevant experience with quantifiable results"
            },
            "education": {
                "score": 70,
                "feedback": "Meets requirements, consider adding certifications"
            },
            "skills": {
                "score": 80,
                "feedback": "Good coverage of required technical skills"
            },
            "formatting": {
                "score": 75,
                "feedback": "Clean layout, ATS-friendly format"
            },
        },
        "keywords": [
            "python",
            "fastapi",
            "microservices",
            "aws",
            "docker"
        ],
        "suggestions": [
            "Add quantifiable achievements to each role",
            "Include relevant certifications",
            "Optimize for ATS with standard section headers",
        ],
    }


# ============================================================
# 2. RESUME SCORE
# ============================================================

@router.get("/resume/score/{resumeId}")
async def get_resume_score(
    resumeId: int,
    current_user: User = Depends(get_current_user)
):
    return {
        "resume_id": resumeId,
        "overall_score": 78,
        "breakdown": {
            "relevance": 80,
            "experience": 85,
            "skills": 75,
            "education": 70,
            "formatting": 82,
        },
    }


# ============================================================
# 3. CANDIDATE ↔ JOB MATCH
# ============================================================

@router.get("/match/{candidateId}/{jobId}")
async def get_match(
    candidateId: int,
    jobId: int,
    current_user: User = Depends(get_current_user)
):
    return {
        "candidate_id": candidateId,
        "job_id": jobId,
        "match_score": 85,
        "matched_skills": [
            "Python",
            "FastAPI",
            "PostgreSQL"
        ],
        "missing_skills": [
            "Kubernetes",
            "Terraform"
        ],
        "experience_match": True,
        "education_match": True,
        "summary": "Strong match — candidate meets 85% of requirements",
    }


# ============================================================
# 4. JOB RECOMMENDATIONS FOR CANDIDATE
# ============================================================

@router.get("/recommendations/jobs/{candidateId}")
async def recommend_jobs(
    candidateId: int,
    current_user: User = Depends(get_current_user)
):
    return [
        {
            "job_id": 1,
            "title": "Senior Backend Engineer",
            "company": "TechCorp",
            "match_score": 92,
            "reason": (
                "Strong alignment with Python and API "
                "development experience"
            ),
        },
        {
            "job_id": 3,
            "title": "Staff Engineer",
            "company": "StartupX",
            "match_score": 78,
            "reason": (
                "Good skills overlap, slight experience gap"
            ),
        },
    ]


# ============================================================
# 5. CANDIDATE RECOMMENDATIONS FOR JOB
# ============================================================

@router.get("/recommendations/candidates/{jobId}")
async def recommend_candidates(
    jobId: int,
    current_user: User = Depends(get_current_user)
):
    return [
        {
            "candidate_id": 1,
            "full_name": "Jane Smith",
            "match_score": 92,
            "top_skills": [
                "Python",
                "FastAPI",
                "AWS"
            ],
            "experience_years": 6,
        },
        {
            "candidate_id": 2,
            "full_name": "John Doe",
            "match_score": 78,
            "top_skills": [
                "Python",
                "Django",
                "Docker"
            ],
            "experience_years": 4,
        },
    ]


# ============================================================
# 6. SKILL GAP ANALYSIS
# ============================================================

@router.get("/skill-gap/{candidateId}")
async def get_skill_gap(
    candidateId: int,
    current_user: User = Depends(get_current_user)
):
    return {
        "candidate_id": candidateId,
        "current_skills": [
            "Python",
            "FastAPI",
            "SQL",
            "Docker"
        ],
        "market_demand": [
            "Kubernetes",
            "Terraform",
            "GraphQL",
            "TypeScript"
        ],
        "gaps": [
            {
                "skill": "Kubernetes",
                "priority": "high",
                "resources": [
                    "CKA Certification"
                ]
            },
            {
                "skill": "Terraform",
                "priority": "medium",
                "resources": [
                    "HashiCorp Learn"
                ]
            },
        ],
        "career_readiness_score": 72,
    }


# ============================================================
# 7. RANK CANDIDATES
# ============================================================

@router.get("/rank-candidates/{jobId}")
async def rank_candidates(
    jobId: int,
    current_user: User = Depends(get_current_user)
):
    return {
        "job_id": jobId,
        "ranked_candidates": [
            {
                "rank": 1,
                "candidate_id": 1,
                "full_name": "Jane Smith",
                "score": 92
            },
            {
                "rank": 2,
                "candidate_id": 3,
                "full_name": "Alice Johnson",
                "score": 85
            },
            {
                "rank": 3,
                "candidate_id": 2,
                "full_name": "John Doe",
                "score": 78
            },
        ],
    }


# ============================================================
# 8. INTERVIEW FEEDBACK
# ============================================================

@router.get("/interview-feedback/{interviewId}")
async def get_interview_feedback(
    interviewId: int,
    current_user: User = Depends(get_current_user)
):
    return {
        "interview_id": interviewId,
        "candidate_name": "Jane Smith",
        "overall_rating": 4.2,
        "strengths": [
            "Strong technical knowledge",
            "Clear communication"
        ],
        "areas_for_improvement": [
            "Could elaborate more on system design decisions"
        ],
        "recommendation": "proceed",
        "ai_summary": (
            "Candidate demonstrated solid backend expertise "
            "with good problem-solving approach."
        ),
    }


# ============================================================
# 9. 🛡️ RESUME INTEGRITY / ANOMALY DETECTION
# ============================================================

@router.post("/resume/integrity-check/{resumeId}")
async def resume_integrity_check(
    resumeId: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Analyze a resume for suspicious or inconsistent signals.

    This endpoint does NOT prove fraud.
    It identifies anomalies that may require
    manual verification by an HR recruiter.
    """

    # --------------------------------------------------------
    # Find resume in database
    # --------------------------------------------------------

    result = await db.execute(
        select(Resume).where(
            Resume.id == resumeId
        )
    )

    resume = result.scalar_one_or_none()

    # --------------------------------------------------------
    # Resume not found
    # --------------------------------------------------------

    if resume is None:
        raise HTTPException(
            status_code=404,
            detail="Resume not found"
        )

    # --------------------------------------------------------
    # Check whether resume has extracted text
    # --------------------------------------------------------

    if not resume.extracted_text:
        raise HTTPException(
            status_code=400,
            detail="Resume has not been parsed yet"
        )

    # --------------------------------------------------------
    # Run AI / anomaly detection engine
    # --------------------------------------------------------

    analysis = check_resume_integrity(
        resume.extracted_text
    )

    # --------------------------------------------------------
    # Return result
    # --------------------------------------------------------

    return {
        "resume_id": resume.id,
        "candidate_id": resume.candidate_id,
        "status": "completed",
        **analysis
    }