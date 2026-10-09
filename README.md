# ATS Resume Optimizer: free ATS resume checker, CV builder and LinkedIn optimizer

[![CI](https://github.com/paulo-amaral/ats-resume-optimizer/actions/workflows/ci.yml/badge.svg)](https://github.com/paulo-amaral/ats-resume-optimizer/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/ats-resume)](https://pypi.org/project/ats-resume/)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License: MIT](https://img.shields.io/badge/license-MIT-green)
![Languages](https://img.shields.io/badge/lang-EN%20%7C%20PT--BR-orange)

**Português:** [README.pt-BR.md](README.pt-BR.md)

Check your resume the way an **Applicant Tracking System (ATS)** reads it, tailor it to
a job description, and export a clean **ATS-friendly PDF or DOCX**. Works three ways:

1. **Terminal app (TUI):** pick your CV, paste a job, see the results live.
2. **Command line (CLI):** one command per task, scriptable.
3. **AI agent skill for Claude Code:** your AI writes the words with you; the tools check layout, keywords and truthfulness.

Optimized for ATS parsing (Workday, Greenhouse, Lever, Taleo, iCIMS, Ashby), the
7-second recruiter skim, and LinkedIn recruiter search. **Zero fabrication:** it never
invents employers, titles, dates or numbers.

![Terminal app](https://raw.githubusercontent.com/paulo-amaral/ats-resume-optimizer/main/docs/tui.svg)

## Get started in 1 minute

You need [uv](https://docs.astral.sh/uv/getting-started/installation/) (one installer,
handles Python for you). Then:

```bash
uv tool install "ats-resume[tui]"
ats-resume tui
```

That's it. Pick your resume (PDF, DOCX, TXT or JSON) in the left panel, paste the job
description, and read the three tabs: **ATS file**, **Style**, **Keywords**.

Prefer `pipx`? `pipx install "ats-resume[tui]"`. Or plain pip: `pip install "ats-resume[tui]"`.

Try it without installing: `uvx ats-resume check my-cv.pdf`.

## What you can do

| Goal | Command |
| --- | --- |
| Check the resume you already have | `ats-resume check my-cv.pdf` |
| Compare it with a job posting | `ats-resume check my-cv.pdf --job job.txt` |
| Turn a PDF/DOCX into editable JSON | `ats-resume import my-cv.pdf` |
| Start from an example | `ats-resume new` (or `--lang pt`) |
| Export an ATS-safe PDF or DOCX | `ats-resume render resume.json -o Jane-Doe-Resume.pdf -t modern` |
| Export LaTeX (Overleaf) or a LaTeX-built PDF | `ats-resume render resume.json -o cv.tex` / `-o cv.pdf --latex` |
| Prove nothing was invented | `ats-resume validate resume.json --source master.json` |
| Interactive app | `ats-resume tui` |

Real output of `check` on the bundled example (`ats-resume new`, rendered with `-t modern`)
against this `job.txt`:

```text
Senior Data Engineer
Requirements:
- Python, SQL, Spark, Kafka
- Kubernetes and Terraform
Nice to have:
- dbt, Airflow
```

```text
ATS file check: en-modern.pdf
  ✓ selectable text (1906 chars)
  ✓ 1 page(s)
  ✓ email found
  ✓ standard section headings detected

Style (de-slop): 0
  ✓ no issues found

Keyword coverage vs job (ESTIMATE, not a real ATS score)
  94.0% (strong)  required_coverage=88.9%, preferred_coverage=100.0%, quantification_rate=92.3%, ...
  Missing required keywords: kubernetes
  Add missing keywords only if you truly have the skill: in Skills and in a real bullet.
```

The score is a labeled **estimate** of keyword fit. No tool can reproduce a real ATS's
internal ranking, and this one does not pretend to.

## Templates

Three single-column, text-based templates. All pass the built-in ATS check.

| `classic` | `modern` |
| --- | --- |
| ![classic](https://raw.githubusercontent.com/paulo-amaral/ats-resume-optimizer/main/docs/example-classic.png) | ![modern](https://raw.githubusercontent.com/paulo-amaral/ats-resume-optimizer/main/docs/example-modern.png) |

`compact` uses a serif font and tighter spacing to fit more on one page.

**LaTeX.** `ats-resume render resume.json -o cv.tex` writes LaTeX source you can edit or
upload to Overleaf, where the compiler must be set to XeLaTeX; `-o cv.pdf --latex` compiles it
locally with [Tectonic](https://tectonic-typesetting.github.io/), XeLaTeX or LuaLaTeX.
The LaTeX output is tuned for ATS text extraction: kerning is turned off, because kerned
pairs like "AW" or "Va" extract as split words ("A WS", "V arejo"). pdfLaTeX is not used
for that reason: it cannot switch kerning off, and CI caught it splitting "Texas". A test compiles the examples and fails if any
word from the source is missing from the extracted text.
Portuguese resumes (`"lang": "pt"`) get localized headings and A4 paper automatically.

## Use it with your AI agent

The agent writes the words with you; `ats-resume` checks layout, keywords and truthfulness.

| Agent | Install |
| --- | --- |
| **Claude Code** | `/plugin marketplace add paulo-amaral/ats-resume-optimizer` then `/plugin install ats-resume-optimizer@ats-resume-optimizer` |
| **Claude Cowork** (desktop) | In Customize, open Plugins, choose **Add marketplace**, enter `paulo-amaral/ats-resume-optimizer` and install the plugin |
| **OpenAI Codex** | `git clone https://github.com/paulo-amaral/ats-resume-optimizer && mkdir -p ~/.agents/skills && cp -R ats-resume-optimizer/skills/resume-ats-linkedin-optimizer ~/.agents/skills/` |
| **Cursor, Gemini CLI, others** | Open this repository in the agent: [`AGENTS.md`](AGENTS.md) tells it what to do. Or add the `skills/resume-ats-linkedin-optimizer/` folder to its context. |

Then ask, in English or Portuguese:

- *"Here is my old CV (cv.pdf). Import it, check it for ATS and improve it."*
- *"Tailor my resume to this job: ..."*
- *"Optimize my LinkedIn headline and About."*
- *"Write a cover letter for this role."*

**Importing a previous CV.** `ats-resume import old-cv.pdf` extracts what is safe to
extract automatically (contact data, headline, summary, skills, language) and keeps
every other section as raw text for the agent to structure, asking you when something
is ambiguous. Your original stays the source of truth: `ats-resume validate` proves no
employer, title, date or contact detail was invented. Step-by-step flow: [`AGENTS.md`](AGENTS.md).

The skill works in phases and finishes each one before starting the next: intake,
Master Profile, metric excavation, content, ATS formatting, keyword tailoring, rendering,
evaluation and, when asked, LinkedIn.

The **Master Profile** is your private record of everything you have done. Every resume
is a *selection* from it, never an invention on top of it.

## Why this one

- **Honest scoring.** A labeled keyword-coverage estimate, never a fake "ATS score 98/100".
- **Reads your real file.** Detects scanned PDFs with no selectable text, tables, images and header/footer text in DOCX, missing email, missing standard headings.
- **Sourced guidance.** Harvard/MIT career services, Google's XYZ formula, recruiter eye-tracking research, documented ATS parsing behavior. Myths are debunked in [`07-myths-and-truth.md`](skills/resume-ats-linkedin-optimizer/references/07-myths-and-truth.md).
- **Bilingual.** English and Brazilian Portuguese: headings, A4, PT-BR keyword matching (accents included), PT-BR cliché detection, and a [Brazilian market guide](skills/resume-ats-linkedin-optimizer/references/09-brazil-market.md) (LGPD, Lei 9.029/1995, Gupy).
- **Private.** Runs locally. Nothing is uploaded anywhere.

## Myths it refuses to repeat

- *"ATS auto-reject 75% of resumes."* A myth from a defunct 2012 vendor. What filters people out is recruiter overload and knockout questions.
- *"Hidden white-text keywords beat the bot."* Modern screening flags it.
- *"ATS can't read PDFs."* Text-based PDFs parse fine. Two-column and image layouts are the problem.

## Project layout

```text
src/ats_resume/        CLI, TUI, checks, renderer, importer (Python package)
skills/…/SKILL.md      the AI agent workflow (start here for the skill)
skills/…/references/   ATS, bullets, keywords, LinkedIn, scoring, myths, cover letters, Brazil
skills/…/assets/       schema, templates, verb banks and cliché lists (EN + PT-BR)
tests/                 pytest suite: renders every format, reads it back, and drives the TUI
```

## Develop

```bash
uv sync --all-extras
uv run pytest
uv run ruff check .
```

## Credits

Based on [artificialguybr/resume-ats-linkedin-optimizer](https://github.com/artificialguybr/resume-ats-linkedin-optimizer)
by João Vitor Amaral (MIT). This fork adds the installable CLI, the terminal app,
PDF/DOCX import and audit, three templates, Portuguese (PT-BR) support, tests and CI.

## License

MIT. See [LICENSE](LICENSE).
