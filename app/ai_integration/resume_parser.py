"""
Resume parsing: extract text + structured fields from PDF/DOCX, and
produce a PII-redacted version used for embedding/scoring.
"""

import io
import re

import pdfplumber
from docx import Document as DocxDocument

from app.core.exceptions import NotFoundException

_SKILL_KEYWORDS = [
    "python", "java", "javascript", "typescript", "react", "node.js", "fastapi",
    "django", "flask", "sql", "postgresql", "mongodb", "docker", "kubernetes",
    "aws", "azure", "gcp", "machine learning", "deep learning", "nlp",
    "tensorflow", "pytorch", "git", "ci/cd", "agile", "rest api", "graphql",
]

_EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
_PHONE_RE = re.compile(r"(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}")
_YEARS_RE = re.compile(r"(\d+(?:\.\d+)?)\+?\s*years?\s*(?:of\s*)?experience", re.IGNORECASE)


class ParsedResumeResult:
    def __init__(self, raw_text: str, redacted_text: str, name, email, skills: list[str], education: list[str], experience_years):
        self.raw_text = raw_text
        self.redacted_text = redacted_text
        self.name = name
        self.email = email
        self.skills = skills
        self.education = education
        self.experience_years = experience_years


def extract_text(file_bytes: bytes, file_format: str) -> str:
    if file_format == "pdf":
        parts = []
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    parts.append(text)
        text = "\n".join(parts)
    elif file_format == "docx":
        doc = DocxDocument(io.BytesIO(file_bytes))
        text = "\n".join(p.text for p in doc.paragraphs)
    else:
        raise ValueError(f"Unsupported resume format: {file_format}")

    if not text.strip():
        raise ValueError("Resume file contained no extractable text")
    return text


def _extract_name_email(text: str):
    email_match = _EMAIL_RE.search(text)
    name = None
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or _EMAIL_RE.search(stripped) or _PHONE_RE.search(stripped):
            continue
        if len(stripped.split()) <= 5:
            name = stripped
            break
    return name, (email_match.group(0) if email_match else None)


def _extract_skills(text: str) -> list[str]:
    lowered = text.lower()
    return sorted({skill for skill in _SKILL_KEYWORDS if skill in lowered})


def _extract_education(text: str) -> list[str]:
    keywords = ["bachelor", "master", "phd", "b.tech", "m.tech", "b.sc", "m.sc", "mba"]
    return [line.strip() for line in text.splitlines() if any(k in line.lower() for k in keywords)]


def _extract_experience_years(text: str):
    match = _YEARS_RE.search(text)
    return float(match.group(1)) if match else None


def _redact(text: str, name, email) -> str:
    redacted = text
    if email:
        redacted = redacted.replace(email, "[EMAIL_REDACTED]")
    if name:
        redacted = redacted.replace(name, "[NAME_REDACTED]")
    return redacted


def parse_resume(file_bytes: bytes, file_format: str) -> ParsedResumeResult:
    raw_text = extract_text(file_bytes, file_format)
    name, email = _extract_name_email(raw_text)

    return ParsedResumeResult(
        raw_text=raw_text,
        redacted_text=_redact(raw_text, name, email),
        name=name,
        email=email,
        skills=_extract_skills(raw_text),
        education=_extract_education(raw_text),
        experience_years=_extract_experience_years(raw_text),
    )


async def load_resume_file_bytes(storage_path: str) -> bytes:
    import os
    if not os.path.exists(storage_path):
        raise NotFoundException(f"Resume file not found at {storage_path}")
    with open(storage_path, "rb") as f:
        return f.read()
