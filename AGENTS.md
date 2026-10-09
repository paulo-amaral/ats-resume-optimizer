# Instructions for AI agents (Codex, Cursor, Gemini CLI, Claude, others)

This repository is a resume/CV toolkit. When the user asks for anything about a resume,
CV, cover letter, ATS check or LinkedIn profile, follow
[`skills/resume-ats-linkedin-optimizer/SKILL.md`](skills/resume-ats-linkedin-optimizer/SKILL.md).
It defines the workflow, and the **zero-fabrication rule overrides everything**: never
invent employers, titles, dates, degrees or numbers.

Reply in the user's language. For Portuguese, use the references in
`skills/resume-ats-linkedin-optimizer/references/pt-BR/`.

## Tools

Use the `ats-resume` CLI for every deterministic step. If it is not installed:

```bash
uv tool install "ats-resume[tui]"
# or, inside this repository:
uv run ats-resume --help
```

## Start from the user's previous CV (most common request)

1. **Audit it as-is** so the user sees the starting point:
   `ats-resume check old-cv.pdf --job job.txt` (add `--json` to parse the result).
2. **Import it**: `ats-resume import old-cv.pdf -o resume.json`.
   This fills only what can be extracted safely: name, email, phone, LinkedIn, GitHub,
   headline, summary, skills, `lang`. Roles, dates and bullets stay as raw text in
   `_import.sections`.
3. **Structure the rest yourself** from `_import.sections` into `experience` and
   `education` (shape: `skills/resume-ats-linkedin-optimizer/assets/resume.schema.json`).
   Copy facts exactly; ask the user about anything ambiguous (a date range that did not
   parse, a title that is unclear). Then delete `_import`.
4. **Keep the original as the source of truth**: save the structured file as
   `master.json` before improving it, and run
   `ats-resume validate resume.json --source master.json` after every rewrite.
5. **Improve, tailor, render** following SKILL.md phases 1–6:
   `ats-resume render resume.json -o Firstname-Lastname-Resume.pdf -t classic|modern|compact`.
   For LaTeX: `-o cv.tex` (source; on Overleaf set the compiler to XeLaTeX) or `-o cv.pdf --latex` (compiles with Tectonic/XeLaTeX/LuaLaTeX).
6. **Re-check the final file**: `ats-resume check Firstname-Lastname-Resume.pdf --job job.txt`.

If the CLI cannot run in your environment, read the CV file directly, follow the same
steps by hand, and tell the user which automated checks were skipped.

## Privacy

Resumes contain personal data. Keep `resume.json`, `master*.json`, PDFs and DOCX files
local (they are in `.gitignore`). Never commit or upload them.

## Working on this repository's code

```bash
uv sync --all-extras
uv run pytest
uv run ruff check .
```

Package code lives in `src/ats_resume/`; tests in `tests/`. Keep rendering
single-column and text-based; `tests/test_ats_resume.py::test_no_source_word_is_lost_in_extraction`
must keep passing for every output format.
