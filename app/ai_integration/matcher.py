"""
Resume <-> Job matching logic.

Combines: (1) embedding similarity for overall semantic fit, and
(2) simple keyword overlap for an explainable matched/missing skills list.
"""

from app.ai_integration.embeddings import cosine_similarity, embed_text
from app.ai_integration.schemas import MatchResult
from app.ai_integration.vector_client import query_similar_resumes


def compute_match(
    *,
    candidate_id: int,
    job_id: int,
    resume_skills: list[str],
    resume_redacted_text: str,
    job_required_skills: list[str],
    job_description_text: str,
    candidate_experience_years: float | None,
    job_min_experience_years: float | None,
    candidate_has_required_education: bool,
) -> MatchResult:
    resume_skills_lower = {s.lower() for s in resume_skills}
    required_skills_lower = {s.lower() for s in job_required_skills}

    matched = sorted(resume_skills_lower & required_skills_lower)
    missing = sorted(required_skills_lower - resume_skills_lower)

    semantic_score = cosine_similarity(
        embed_text(resume_redacted_text), embed_text(job_description_text)
    )
    skill_overlap_ratio = len(matched) / len(required_skills_lower) if required_skills_lower else 1.0
    blended = (0.5 * semantic_score) + (0.5 * skill_overlap_ratio)
    match_score = round(max(0.0, min(1.0, blended)) * 100)

    experience_match = (
        job_min_experience_years is None
        or candidate_experience_years is None
        or candidate_experience_years >= job_min_experience_years
    )

    summary = (
        f"Strong match - candidate meets {match_score}% of requirements"
        if match_score >= 75
        else f"Partial match - candidate meets {match_score}% of requirements, "
             f"missing: {(', '.join(missing) if missing else 'none')}"
    )

    return MatchResult(
        candidate_id=candidate_id,
        job_id=job_id,
        match_score=match_score,
        matched_skills=[s.title() for s in matched],
        missing_skills=[s.title() for s in missing],
        experience_match=experience_match,
        education_match=candidate_has_required_education,
        summary=summary,
    )


def rank_candidates_for_job(job_id: int, job_description_text: str, top_k: int = 10) -> list[dict]:
    job_embedding = embed_text(job_description_text)
    matches = query_similar_resumes(job_embedding, top_k=top_k)
    for m in matches:
        m["score"] = round(max(0.0, 1 - m["distance"]) * 100)
    matches.sort(key=lambda m: m["score"], reverse=True)
    return matches
