"""
Pydantic schemas for everything Team AI's code returns.
"""

from pydantic import BaseModel


class CamelModel(BaseModel):
    pass


class SectionFeedback(CamelModel):
    score: int
    feedback: str


class ResumeAnalysis(CamelModel):
    resume_id: int
    status: str = "completed"
    overall_score: int
    ats_score: int
    sections: dict[str, SectionFeedback]
    keywords: list[str]
    strengths: list[str]
    weaknesses: list[str]
    suggestions: list[str]


class ResumeScoreBreakdown(CamelModel):
    relevance: int
    experience: int
    skills: int
    education: int
    formatting: int


class ResumeScore(CamelModel):
    resume_id: int
    overall_score: int
    breakdown: ResumeScoreBreakdown


class MatchResult(CamelModel):
    candidate_id: int
    job_id: int
    match_score: int
    matched_skills: list[str]
    missing_skills: list[str]
    experience_match: bool
    education_match: bool
    summary: str


class RecommendedJob(CamelModel):
    job_id: int
    title: str
    company: str
    match_score: int
    reason: str


class RecommendedCandidate(CamelModel):
    candidate_id: int
    full_name: str
    match_score: int
    top_skills: list[str]
    experience_years: float


class SkillGapItem(CamelModel):
    skill: str
    priority: str
    resources: list[str]


class SkillGapResult(CamelModel):
    candidate_id: int
    current_skills: list[str]
    market_demand: list[str]
    gaps: list[SkillGapItem]
    career_readiness_score: int


class RankedCandidate(CamelModel):
    rank: int
    candidate_id: int
    full_name: str
    score: int


class RankCandidatesResult(CamelModel):
    job_id: int
    ranked_candidates: list[RankedCandidate]


class InterviewFeedback(CamelModel):
    interview_id: int
    candidate_name: str
    overall_rating: float
    strengths: list[str]
    areas_for_improvement: list[str]
    recommendation: str
    ai_summary: str