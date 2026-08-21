"""
Skill gap analysis.
"""

from app.ai_integration.schemas import SkillGapItem, SkillGapResult

_MARKET_DEMAND_SKILLS = {
    "kubernetes": {"priority": "high", "resources": ["CKA Certification", "Kubernetes docs tutorial"]},
    "terraform": {"priority": "medium", "resources": ["HashiCorp Learn"]},
    "graphql": {"priority": "medium", "resources": ["GraphQL official docs"]},
    "typescript": {"priority": "high", "resources": ["TypeScript Handbook"]},
    "aws": {"priority": "high", "resources": ["AWS Certified Developer path"]},
}


def compute_skill_gap(candidate_id: int, candidate_skills: list[str]) -> SkillGapResult:
    candidate_skills_lower = {s.lower() for s in candidate_skills}

    gaps = [
        SkillGapItem(skill=skill.title(), priority=info["priority"], resources=info["resources"])
        for skill, info in _MARKET_DEMAND_SKILLS.items()
        if skill not in candidate_skills_lower
    ]
    gaps.sort(key=lambda g: {"high": 0, "medium": 1, "low": 2}[g.priority])

    total_demand = len(_MARKET_DEMAND_SKILLS)
    covered = total_demand - len(gaps)
    readiness = round((covered / total_demand) * 100) if total_demand else 100

    return SkillGapResult(
        candidate_id=candidate_id,
        current_skills=[s.title() for s in candidate_skills],
        market_demand=[s.title() for s in _MARKET_DEMAND_SKILLS.keys()],
        gaps=gaps,
        career_readiness_score=readiness,
    )
