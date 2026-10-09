"""Existing resume (PDF/DOCX/TXT) -> resume.json skeleton.

Only facts that can be extracted deterministically are filled (contact data, summary, skills).
Roles, dates and bullets stay in `_import.sections` as raw text for the AI agent to structure,
because guessing them here would risk the zero-fabrication rule.
"""
from __future__ import annotations

import re
from pathlib import Path

from .checks import EMAIL_RE
from .doc import extract_text, first_match, split_sections
from .i18n import detect_lang

PATTERNS = {
    "email": EMAIL_RE,
    "phone": r"\+?\d[\d\s().-]{7,}\d",
    "linkedin": r"(?:https?://)?(?:[a-z]{2,3}\.)?linkedin\.com/in/[\w%-]+/?",
    "github": r"(?:https?://)?github\.com/[\w-]+/?",
}


def _guess_name(header: list[str]) -> str:
    for line in header[:3]:
        words = line.split()
        if 1 < len(words) <= 5 and not re.search(r"[\d@/|]", line):
            return line
    return ""


def import_resume(path: str | Path) -> dict:
    text = extract_text(path)
    grouped = split_sections(text)
    header = grouped.get("header", [])
    basics = {"name": _guess_name(header)}
    for key, pattern in PATTERNS.items():
        value = first_match(pattern, text)
        if value:
            basics[key] = value
    name_idx = header.index(basics["name"]) if basics["name"] in header else -1
    if 0 <= name_idx + 1 < len(header) and not re.search(r"[\d@]", header[name_idx + 1]):
        basics["headline"] = header[name_idx + 1]

    skills = [s.strip(" •·-") for line in grouped.get("skills", []) for s in re.split(r"[,;|•]", line)]
    resume = {
        "lang": detect_lang(text),
        "basics": basics,
        "summary": " ".join(grouped.get("summary", [])),
        "experience": [],
        "education": [],
        "skills": [{"category": "Skills", "items": [s for s in skills if s]}] if skills else [],
        "_import": {
            "source": str(path),
            "note": "Raw text per section. Structure experience/education from it; never invent missing facts.",
            "sections": {k: v for k, v in grouped.items() if v},
        },
    }
    return resume
