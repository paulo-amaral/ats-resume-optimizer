"""Language support: section headings (render + parse), CLI messages, language detection."""
from __future__ import annotations

import os
import re
import unicodedata

LANGS = ("en", "pt")

# Headings written by `render`. Standard wording on purpose: ATS map these to fields.
HEADINGS = {
    "en": {
        "summary": "Summary", "experience": "Work Experience", "projects": "Projects",
        "skills": "Skills", "education": "Education", "certifications": "Certifications",
        "publications": "Publications", "awards": "Awards",
    },
    "pt": {
        "summary": "Resumo Profissional", "experience": "Experiência Profissional",
        "projects": "Projetos", "skills": "Competências", "education": "Formação Acadêmica",
        "certifications": "Certificações", "publications": "Publicações", "awards": "Prêmios",
    },
}

# Headings recognised when reading an existing PDF/DOCX/TXT resume (compared after fold()).
HEADING_SYNONYMS = {
    "summary": [
        "summary", "professional summary", "profile", "professional profile", "about", "about me",
        "objective", "career objective", "resumo", "resumo profissional", "perfil",
        "perfil profissional", "objetivo", "objetivo profissional", "sobre", "sobre mim",
    ],
    "experience": [
        "experience", "work experience", "professional experience", "employment",
        "employment history", "work history", "experiencia", "experiencia profissional",
        "experiencias profissionais", "historico profissional",
    ],
    "education": [
        "education", "academic background", "formacao", "formacao academica", "educacao",
        "escolaridade",
    ],
    "skills": [
        "skills", "technical skills", "core skills", "competencies", "core competencies",
        "competencias", "competencias tecnicas", "habilidades", "conhecimentos",
        "conhecimentos tecnicos",
    ],
    "certifications": [
        "certifications", "licenses & certifications", "licenses and certifications",
        "certificacoes", "certificados", "cursos e certificacoes", "cursos",
    ],
    "projects": ["projects", "projetos", "personal projects", "projetos pessoais"],
    "languages": ["languages", "idiomas"],
}

MESSAGES = {
    "en": {
        "ats_title": "ATS file check",
        "style_title": "Style (de-slop)",
        "coverage_title": "Keyword coverage vs job (ESTIMATE, not a real ATS score)",
        "no_findings": "no issues found",
        "missing_req": "Missing required keywords",
        "missing_pref": "Missing preferred keywords",
        "coverage_advice": "Add missing keywords only if you truly have the skill: in Skills and in a real bullet.",
        "no_job": "Tip: add --job job.txt to measure keyword coverage against a job posting.",
        "wrote": "wrote",
        "import_next": "Next step: ask your AI agent to complete this file using the raw text in \"_import\".",
        "new_next": "Next step: edit the file (or ask your AI agent to fill it), then run",
        "exists": "file already exists (use --force to overwrite)",
        "unsupported": "unsupported file type",
        "invariants_ok": "truthfulness invariants passed",
        "invariants_fail": "truthfulness invariants FAILED. Reconcile with the user; never invent to fix.",
    },
    "pt": {
        "ats_title": "Verificação de arquivo ATS",
        "style_title": "Estilo (linguagem genérica)",
        "coverage_title": "Cobertura de palavras-chave da vaga (ESTIMATIVA, não é nota real de ATS)",
        "no_findings": "nenhum problema encontrado",
        "missing_req": "Palavras-chave obrigatórias ausentes",
        "missing_pref": "Palavras-chave desejáveis ausentes",
        "coverage_advice": "Inclua as ausentes só se você tem a competência de verdade: em Competências e num bullet real.",
        "no_job": "Dica: use --job vaga.txt para medir a cobertura de palavras-chave de uma vaga.",
        "wrote": "gerado",
        "import_next": "Próximo passo: peça ao seu agente de IA para completar este arquivo com o texto bruto em \"_import\".",
        "new_next": "Próximo passo: edite o arquivo (ou peça ao seu agente de IA para preencher) e rode",
        "exists": "o arquivo já existe (use --force para sobrescrever)",
        "unsupported": "tipo de arquivo não suportado",
        "invariants_ok": "invariantes de veracidade aprovadas",
        "invariants_fail": "invariantes de veracidade FALHARAM. Reconcilie com a pessoa; nunca invente para corrigir.",
    },
}


def fold(s: str) -> str:
    """Lowercase and strip accents so 'Experiência' and 'experiencia' compare equal."""
    nfkd = unicodedata.normalize("NFKD", s or "")
    return "".join(c for c in nfkd if not unicodedata.combining(c)).lower().strip()


def ui_lang(explicit: str | None = None) -> str:
    if explicit in LANGS:
        return explicit
    env = os.environ.get("LC_ALL") or os.environ.get("LC_MESSAGES") or os.environ.get("LANG") or ""
    return "pt" if env.lower().startswith("pt") else "en"


_PT_HINTS = {"de", "da", "do", "das", "dos", "em", "com", "para", "uma", "não", "experiência", "formação"}
_EN_HINTS = {"the", "and", "of", "with", "for", "experience", "education", "skills", "to", "in"}


def detect_lang(text: str) -> str:
    words = re.findall(r"[^\W\d_]+", (text or "").lower())
    pt = sum(w in _PT_HINTS for w in words)
    en = sum(w in _EN_HINTS for w in words)
    return "pt" if pt > en else "en"


def t(lang: str, key: str) -> str:
    return MESSAGES.get(lang, MESSAGES["en"])[key]
