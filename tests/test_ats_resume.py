import json
import re
import shutil
from importlib import resources

import pytest

from ats_resume import checks
from ats_resume.cli import main, read_job
from ats_resume.doc import extract_text, from_resume, from_text
from ats_resume.importer import import_resume
from ats_resume.render import LATEX_ENGINES, TEMPLATES, compile_latex, render


def example(lang: str) -> dict:
    return json.loads((resources.files("ats_resume") / "data" / f"example-{lang}.json").read_text("utf-8"))


# --- coverage ---------------------------------------------------------------

def test_tokenize_keeps_accented_words_whole():
    assert checks.tokenize("Gestão de análise") == ["gestão", "de", "análise"]
    assert "c++" in checks.tokenize("C++ and C#") and "c#" in checks.tokenize("C++ and C#")


def test_coverage_portuguese_job_finds_missing_keyword():
    jd = "Requisitos:\nExperiência com Spark, Kafka e Kubernetes\nDiferenciais:\nTerraform"
    report = checks.coverage(from_resume(example("pt")), jd)
    assert "kubernetes" in report["missing_required_keywords"]
    assert "spark" not in report["missing_required_keywords"]
    assert "terraform" not in report["missing_preferred_keywords"]


def test_coverage_matches_regardless_of_accents():
    present, _ = checks.coverage_of({"gestão"}, "Gestao de projetos")
    assert present == {"gestão"}


def test_read_job_accepts_long_pasted_text():
    long_text = "Python " * 200  # longer than any filename; used to raise OSError
    assert read_job(long_text) == long_text


# --- validate ---------------------------------------------------------------

def test_validate_two_roles_same_company_no_false_date_warning():
    source = {"basics": {"name": "A"}, "experience": [
        {"company": "Acme", "title": "Engineer", "start": "2019"},
        {"company": "Acme", "title": "Senior Engineer", "start": "2022"},
    ]}
    report = checks.validate(source, source)
    assert report["invariants_passed"] and report["warnings"] == []


def test_validate_flags_fabricated_employer_and_identity_change():
    source = example("en")
    resume = json.loads(json.dumps(source))
    resume["experience"][0]["company"] = "Google"
    resume["basics"]["email"] = "other@example.com"
    report = checks.validate(resume, source)
    assert not report["invariants_passed"]
    assert any("FABRICATED" in f for f in report["failures"])
    assert any("email" in f for f in report["failures"])


# --- deslop -----------------------------------------------------------------

def test_deslop_flags_english_and_portuguese():
    doc = from_text("• Responsável por gerenciar a equipe com sucesso\n• Spearheaded a robust migration")
    found = {f["found"] for f in checks.deslop(doc)["slop_findings"]}
    assert {"responsável por", "com sucesso", "spearheaded", "robust"} <= found


def test_deslop_uses_word_boundaries():
    doc = from_text("Dynamically scaled the helpedesk")  # neither 'dynamic' nor 'helped' as words
    assert checks.deslop(doc)["clean"]


# --- render + read back -----------------------------------------------------

@pytest.mark.parametrize("template", sorted(TEMPLATES))
@pytest.mark.parametrize("suffix", [".pdf", ".docx"])
def test_render_round_trip_is_parseable(tmp_path, template, suffix):
    resume = example("pt")
    out = render(resume, tmp_path / f"cv{suffix}", template=template)
    text = extract_text(out)
    assert "Ana Exemplo" in text
    assert "EXPERIÊNCIA PROFISSIONAL" in text.upper()  # localized heading, accents survive
    report = checks.ats_file(out, from_text(text))
    assert all(item["level"] != "fail" for item in report), report


def test_pdf_paper_defaults_to_a4_for_portuguese(tmp_path):
    from pypdf import PdfReader

    out = render(example("pt"), tmp_path / "cv.pdf")
    width = float(PdfReader(out).pages[0].mediabox.width)
    assert round(width) == 595  # A4 width in points


# --- import -----------------------------------------------------------------

def test_import_extracts_contacts_and_keeps_raw_sections(tmp_path):
    out = render(example("en"), tmp_path / "cv.docx")
    resume = import_resume(out)
    assert resume["basics"]["name"] == "Jordan Rivera"
    assert resume["basics"]["email"] == "jordan.rivera@example.com"
    assert resume["lang"] == "en"
    assert resume["experience"] == []  # never guessed
    assert "experience" in resume["_import"]["sections"]


# --- cli --------------------------------------------------------------------

def test_cli_new_render_check(tmp_path, capsys):
    resume = tmp_path / "resume.json"
    assert main(["new", "--lang", "pt", "-o", str(resume)]) == 0
    assert main(["render", str(resume), "-o", str(tmp_path / "cv.pdf"), "-t", "modern"]) == 0
    capsys.readouterr()
    assert main(["check", str(tmp_path / "cv.pdf"), "--job", "Python, Kafka, Rust", "--json"]) == 0
    report = json.loads(capsys.readouterr().out)
    assert "rust" in report["coverage"]["missing_required_keywords"]


def test_rendered_resume_passes_its_own_deslop(tmp_path):
    out = render(example("pt"), tmp_path / "cv.pdf")
    assert checks.deslop(from_text(extract_text(out)))["clean"]


# --- latex ------------------------------------------------------------------

def test_latex_escapes_specials_and_localizes(tmp_path):
    resume = example("pt")
    resume["experience"][0]["bullets"].append("Cut cost 50% & saved $10_000 #1")
    tex = render(resume, tmp_path / "cv.tex").read_text("utf-8")
    assert r"50\% \& saved \$10\_000 \#1" in tex
    assert r"\section*{Experiência Profissional}" in tex
    assert r"\pdfgentounicode=1" in tex and "a4paper" in tex
    assert tex.count(r"\begin{itemize}") == tex.count(r"\end{itemize}")


def _words(text: str) -> set[str]:
    return set(re.findall(r"\w[\w.+#-]*", text))


@pytest.mark.parametrize("lang", ["en", "pt"])
@pytest.mark.parametrize("suffix", [".pdf", ".docx", ".tex"])
def test_no_source_word_is_lost_in_extraction(tmp_path, lang, suffix):
    """What an ATS extracts must contain every word we wrote (kerning gaps, ligatures, accents)."""
    if suffix == ".tex" and not any(shutil.which(e) for e in LATEX_ENGINES):
        pytest.skip("no LaTeX engine installed")
    resume = example(lang)
    out = render(resume, tmp_path / f"cv{suffix}")
    if suffix == ".tex":
        out = compile_latex(out)
    lost = _words(from_resume(resume).text) - _words(extract_text(out))
    assert not lost, lost
