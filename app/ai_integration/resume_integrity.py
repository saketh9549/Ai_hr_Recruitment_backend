import re
from collections import Counter
from datetime import datetime


def check_resume_integrity(text: str, skills: list[str] | None = None):
    """
    Analyze a resume for suspicious or inconsistent signals.

    This does NOT prove fraud.
    It identifies items that may need manual verification.
    """

    if not text or not text.strip():
        return {
            "risk_score": 100,
            "risk_level": "HIGH",
            "flags": [
                {
                    "type": "empty_resume",
                    "severity": "high",
                    "message": "Resume contains no readable text."
                }
            ]
        }

    flags = []

    # ---------------------------------------------------------
    # 1. Check for unrealistic experience claims
    # ---------------------------------------------------------

    experience_matches = re.findall(
        r"(\d+(?:\.\d+)?)\+?\s*years?\s*(?:of\s*)?experience",
        text,
        re.IGNORECASE
    )

    if experience_matches:
        experience_years = max(float(x) for x in experience_matches)

        current_year = datetime.now().year

        if experience_years > 40:
            flags.append({
                "type": "unrealistic_experience",
                "severity": "high",
                "message": (
                    f"Resume claims {experience_years:g} years of experience. "
                    "This should be manually verified."
                )
            })

        elif experience_years > 25:
            flags.append({
                "type": "high_experience_claim",
                "severity": "medium",
                "message": (
                    f"Resume claims {experience_years:g} years of experience. "
                    "Verify against employment history."
                )
            })

    # ---------------------------------------------------------
    # 2. Detect repeated keywords
    # ---------------------------------------------------------

    words = re.findall(r"\b[a-zA-Z][a-zA-Z0-9+#.-]*\b", text.lower())

    word_counts = Counter(words)

    suspicious_keywords = []

    for word, count in word_counts.items():

        if len(word) >= 4 and count >= 15:
            suspicious_keywords.append({
                "keyword": word,
                "count": count
            })

    if suspicious_keywords:

        top_keywords = sorted(
            suspicious_keywords,
            key=lambda x: x["count"],
            reverse=True
        )[:5]

        flags.append({
            "type": "keyword_repetition",
            "severity": "medium",
            "message": "Some keywords appear unusually often.",
            "details": top_keywords
        })

    # ---------------------------------------------------------
    # 3. Check for suspicious date patterns
    # ---------------------------------------------------------

    years = re.findall(r"\b(19\d{2}|20\d{2})\b", text)

    numeric_years = [int(year) for year in years]

    current_year = datetime.now().year

    future_years = [
        year for year in numeric_years
        if year > current_year + 1
    ]

    if future_years:

        flags.append({
            "type": "future_date",
            "severity": "high",
            "message": (
                "Resume contains dates that appear to be in the future."
            ),
            "details": future_years
        })

    # ---------------------------------------------------------
    # 4. Check for very short resume
    # ---------------------------------------------------------

    word_count = len(words)

    if word_count < 80:

        flags.append({
            "type": "very_short_resume",
            "severity": "medium",
            "message": (
                "Resume contains very little information."
            )
        })

    # ---------------------------------------------------------
    # 5. Check duplicate lines
    # ---------------------------------------------------------

    lines = [
        line.strip().lower()
        for line in text.splitlines()
        if line.strip()
    ]

    line_counts = Counter(lines)

    duplicate_lines = [
        {
            "text": line,
            "count": count
        }
        for line, count in line_counts.items()
        if count >= 3 and len(line) > 20
    ]

    if duplicate_lines:

        flags.append({
            "type": "duplicate_content",
            "severity": "low",
            "message": (
                "Some resume content is repeated multiple times."
            ),
            "details": duplicate_lines[:5]
        })

    # ---------------------------------------------------------
    # 6. Check suspicious claims
    # ---------------------------------------------------------

    suspicious_phrases = [
        "100% expert",
        "world's best",
        "perfect in every technology",
        "expert in all technologies",
        "knows everything",
    ]

    found_phrases = []

    lower_text = text.lower()

    for phrase in suspicious_phrases:

        if phrase.lower() in lower_text:
            found_phrases.append(phrase)

    if found_phrases:

        flags.append({
            "type": "suspicious_claim",
            "severity": "low",
            "message": (
                "Resume contains unusually strong or absolute claims."
            ),
            "details": found_phrases
        })

    # ---------------------------------------------------------
    # Calculate risk score
    # ---------------------------------------------------------

    severity_points = {
        "low": 5,
        "medium": 15,
        "high": 30
    }

    risk_score = sum(
        severity_points.get(flag["severity"], 0)
        for flag in flags
    )

    risk_score = min(risk_score, 100)

    if risk_score < 20:
        risk_level = "LOW"

    elif risk_score < 50:
        risk_level = "MEDIUM"

    else:
        risk_level = "HIGH"

    # ---------------------------------------------------------
    # Final result
    # ---------------------------------------------------------

    return {
        "risk_score": risk_score,
        "risk_level": risk_level,
        "flags": flags,
        "total_flags": len(flags),
        "recommendation": (
            "Resume looks normal. No major anomalies detected."
            if risk_level == "LOW"
            else
            "Manual verification is recommended."
        )
    }