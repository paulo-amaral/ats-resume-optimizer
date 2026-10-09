"""ats-resume: check, tailor and render ATS-safe resumes.

Quick start:
  ats-resume check my-cv.pdf --job job.txt    audit the resume you already have
  ats-resume import my-cv.pdf                 turn it into resume.json for your AI agent
  ats-resume new                              start a resume.json from an example
  ats-resume render resume.json -o cv.pdf     build an ATS-safe PDF/DOCX

Add --json to any check for machine-readable output (used by the AI agent skill).
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from importlib import resources
from pathlib import Path

from . import __version__, checks
from .doc import load_doc, load_json
from .i18n import t, ui_lang
from .importer import import_resume
from .render import TEMPLATES, compile_latex, render

_COLORS = {"ok": "\033[32m", "warn": "\033[33m", "fail": "\033[31m", "dim": "\033[2m", "bold": "\033[1m"}
_ICONS = {"ok": "✓", "warn": "!", "fail": "✗"}


def _c(kind: str, text: str) -> str:
    return f"{_COLORS[kind]}{text}\033[0m" if sys.stdout.isatty() else text


def read_job(value: str) -> str:
    """Accept a file path or the job text itself. Long pasted text is not a valid path."""
    try:
        p = Path(value)
        if p.is_file():
            return p.read_text(encoding="utf-8")
    except OSError:
        pass
    return value


def _write_json(path: Path, data: dict, force: bool, lang: str) -> int:
    if path.exists() and not force:
        sys.exit(f"error: {path}: {t(lang, 'exists')}")
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"{t(lang, 'wrote')} {path}")
    return 0


def cmd_new(args) -> int:
    lang = ui_lang(args.lang)
    example = resources.files("ats_resume") / "data" / f"example-{lang}.json"
    out = Path(args.out)
    if out.exists() and not args.force:
        sys.exit(f"error: {out}: {t(lang, 'exists')}")
    with resources.as_file(example) as src:
        shutil.copyfile(src, out)
    print(f"{t(lang, 'wrote')} {out}")
    print(f"{t(lang, 'new_next')}: ats-resume render {out} -o cv.pdf")
    return 0


def cmd_import(args) -> int:
    lang = ui_lang(args.lang)
    _write_json(Path(args.out), import_resume(args.file), args.force, lang)
    print(t(lang, "import_next"))
    return 0


def run_check(file: str, job: str | None, loaded: tuple | None = None) -> dict:
    """All checks for one file. Shared by the CLI and the TUI (which passes a cached `loaded`)."""
    doc, resume = loaded or load_doc(file)
    report: dict = {"file": file, "lang": doc.lang}
    report["ats_file"] = checks.ats_file(file, doc) if resume is None else [
        {"level": "fail", "msg": m} for m in checks.validate(resume)["failures"]
    ] or [{"level": "ok", "msg": "resume.json structure is valid"}]
    report["deslop"] = checks.deslop(doc)
    if job:
        report["coverage"] = checks.coverage(doc, read_job(job))
    return report


def print_check(report: dict, lang: str) -> None:
    print(_c("bold", f"{t(lang, 'ats_title')}: {report['file']}"))
    for item in report["ats_file"]:
        print(f"  {_c(item['level'], _ICONS[item['level']])} {item['msg']}")

    findings = report["deslop"]["slop_findings"]
    print(_c("bold", f"\n{t(lang, 'style_title')}: {len(findings)}"))
    if not findings:
        print(f"  {_c('ok', '✓')} {t(lang, 'no_findings')}")
    for f in findings:
        print(f"  {_c('warn', '!')} {_c('dim', f['location'])}  \"{f['found']}\" → {f['suggest']}")

    cov = report.get("coverage")
    if cov is None:
        print(_c("dim", f"\n{t(lang, 'no_job')}"))
        return
    level = {"strong": "ok", "moderate": "warn", "weak": "fail"}[cov["band"]]
    print(_c("bold", f"\n{t(lang, 'coverage_title')}"))
    print(f"  {_c(level, str(cov['estimated_score_pct']) + '%')} ({cov['band']})  "
          + _c("dim", ", ".join(f"{k.removesuffix('_pct')}={v}%" for k, v in cov["components"].items())))
    for key, label in (("missing_required_keywords", "missing_req"), ("missing_preferred_keywords", "missing_pref")):
        if cov[key]:
            print(f"  {t(lang, label)}: {', '.join(cov[key][:25])}" + (" …" if len(cov[key]) > 25 else ""))
    print(_c("dim", f"  {t(lang, 'coverage_advice')}"))


def cmd_check(args) -> int:
    report = run_check(args.file, args.job)
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print_check(report, ui_lang(args.lang))
    return 1 if any(i["level"] == "fail" for i in report["ats_file"]) else 0


def cmd_render(args) -> int:
    lang = ui_lang(args.lang)
    target = Path(args.out)
    if args.latex and target.suffix.lower() == ".pdf":
        tex = render(load_json(args.resume), target.with_suffix(".tex"), template=args.template, paper=args.paper)
        try:
            out = compile_latex(tex)
        except RuntimeError as e:
            sys.exit(f"error: {e}")
    else:
        out = render(load_json(args.resume), target, template=args.template, paper=args.paper)
    print(f"{t(lang, 'wrote')} {out}  ({args.template}, single-column, ATS-safe)")
    return 0


def cmd_validate(args) -> int:
    lang = ui_lang(args.lang)
    report = checks.validate(load_json(args.resume), load_json(args.source) if args.source else None)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    print(t(lang, "invariants_ok" if report["invariants_passed"] else "invariants_fail"), file=sys.stderr)
    return 0 if report["invariants_passed"] else 1


def cmd_coverage(args) -> int:
    doc, _ = load_doc(args.resume)
    print(json.dumps(checks.coverage(doc, read_job(args.jd)), indent=2, ensure_ascii=False))
    return 0


def cmd_deslop(args) -> int:
    doc, _ = load_doc(args.resume)
    print(json.dumps(checks.deslop(doc), indent=2, ensure_ascii=False))
    return 0


def cmd_tui(args) -> int:
    try:
        from .tui import run
    except ImportError:
        sys.exit("error: the TUI needs an extra dependency. Install:  uv tool install 'ats-resume[tui]'")
    return run(args.file, args.job, args.lang)


def build_parser() -> argparse.ArgumentParser:
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--lang", choices=["en", "pt"], help="interface language (default: from $LANG)")

    parser = argparse.ArgumentParser(prog="ats-resume", description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("check", parents=[common], help="audit a resume (.pdf/.docx/.txt/.json), optionally vs a job")
    p.add_argument("file")
    p.add_argument("--job", "-j", help="job description: .txt path or the text itself")
    p.add_argument("--json", action="store_true", help="machine-readable output")
    p.set_defaults(func=cmd_check)

    p = sub.add_parser("import", parents=[common], help="existing .pdf/.docx/.txt resume -> resume.json skeleton")
    p.add_argument("file")
    p.add_argument("--out", "-o", default="resume.json")
    p.add_argument("--force", action="store_true")
    p.set_defaults(func=cmd_import)

    p = sub.add_parser("new", parents=[common], help="create resume.json from an example (EN or PT-BR)")
    p.add_argument("--out", "-o", default="resume.json")
    p.add_argument("--force", action="store_true")
    p.set_defaults(func=cmd_new)

    p = sub.add_parser("render", parents=[common], help="resume.json -> ATS-safe .pdf or .docx")
    p.add_argument("resume")
    p.add_argument("--out", "-o", default="resume.pdf", help="output path: .pdf, .docx or .tex")
    p.add_argument("--template", "-t", choices=sorted(TEMPLATES), default="classic")
    p.add_argument("--paper", choices=["a4", "letter"], help="default: a4 when lang=pt, else letter")
    p.add_argument("--latex", action="store_true",
                   help="with -o x.pdf: write x.tex and compile it (needs tectonic/pdflatex). -o x.tex writes source only")
    p.set_defaults(func=cmd_render)

    p = sub.add_parser("validate", parents=[common], help="truthfulness invariants (resume vs source)")
    p.add_argument("resume")
    p.add_argument("--source", "-s", help="master-profile.json or original resume.json")
    p.set_defaults(func=cmd_validate)

    p = sub.add_parser("coverage", parents=[common], help="keyword-coverage ESTIMATE vs a job (JSON output)")
    p.add_argument("resume")
    p.add_argument("--jd", required=True, help="job description: .txt path or the text itself")
    p.set_defaults(func=cmd_coverage)

    p = sub.add_parser("deslop", parents=[common], help="flag AI-tells / filler / inflated verbs (JSON output)")
    p.add_argument("resume")
    p.set_defaults(func=cmd_deslop)

    p = sub.add_parser("tui", parents=[common], help="interactive terminal app")
    p.add_argument("file", nargs="?")
    p.add_argument("--job", "-j")
    p.set_defaults(func=cmd_tui)
    return parser


def main(argv: list[str] | None = None) -> int:
    # Windows consoles/pipes may use cp1252, which cannot encode ✓ or →; degrade instead of crashing.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")
    args = build_parser().parse_args(argv)
    return args.func(args)
