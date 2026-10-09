"""Interactive terminal app: pick a resume, paste a job, see ATS / style / keyword results live."""
from __future__ import annotations

import functools
import json
from pathlib import Path

from textual import on, work
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.widgets import (
    Button,
    DirectoryTree,
    Footer,
    Header,
    Input,
    Label,
    ProgressBar,
    Select,
    Static,
    TabbedContent,
    TabPane,
    TextArea,
)

from .cli import run_check
from .doc import load_doc
from .i18n import ui_lang
from .importer import import_resume
from .render import TEMPLATES, render

SUPPORTED = {".pdf", ".docx", ".json", ".txt"}
ICONS = {"ok": "[green]✓[/]", "warn": "[yellow]![/]", "fail": "[red]✗[/]"}

LABELS = {
    "en": {
        "file": "Resume file (.pdf .docx .json .txt)", "job": "Job description (optional, paste here)",
        "check": "Check", "export": "Export PDF", "import": "Import to JSON", "ats": "ATS file",
        "style": "Style", "keywords": "Keywords", "pick": "Pick a resume on the left or type its path.",
        "no_job": "Paste a job description to see keyword coverage.", "clean": "No style issues found.",
        "missing_req": "Missing required", "missing_pref": "Missing preferred",
        "estimate": "ESTIMATE, not a real ATS score. Add keywords only if you truly have the skill.",
    },
    "pt": {
        "file": "Currículo (.pdf .docx .json .txt)", "job": "Descrição da vaga (opcional, cole aqui)",
        "check": "Verificar", "export": "Exportar PDF", "import": "Importar p/ JSON", "ats": "Arquivo ATS",
        "style": "Estilo", "keywords": "Palavras-chave", "pick": "Escolha um currículo à esquerda ou digite o caminho.",
        "no_job": "Cole a descrição de uma vaga para ver a cobertura de palavras-chave.",
        "clean": "Nenhum problema de estilo.", "missing_req": "Obrigatórias ausentes",
        "missing_pref": "Desejáveis ausentes",
        "estimate": "ESTIMATIVA, não é nota real de ATS. Inclua só competências que você tem de verdade.",
    },
}


@functools.lru_cache(maxsize=16)
def _cached_load(path: str, mtime: float):
    # mtime is part of the key so an edited file is re-read; PDF parsing is the slow part.
    return load_doc(path)


class ResumeTree(DirectoryTree):
    def filter_paths(self, paths):
        return [p for p in paths if not p.name.startswith(".") and (p.is_dir() or p.suffix.lower() in SUPPORTED)]


class ResumeApp(App):
    TITLE = "ats-resume"
    CSS = """
    #tree { width: 34; border-right: solid $primary-background; }
    #main { padding: 0 1; }
    #job { height: 9; }
    #actions { height: auto; margin: 1 0 0 0; }
    #actions > * { margin-right: 1; }
    #template { width: 20; }
    #score-row { height: auto; margin: 1 0 0 0; }
    #score { width: 1fr; }
    #band { width: auto; padding: 0 1; }
    TabbedContent { height: 1fr; }
    Label.field { margin: 1 0 0 0; color: $text-muted; }
    """
    BINDINGS = [
        Binding("ctrl+r", "check", "Check"),
        Binding("ctrl+e", "export", "Export"),
        Binding("ctrl+t", "toggle_tree", "Files"),
        Binding("ctrl+q", "quit", "Quit"),
    ]

    def __init__(self, file: str | None = None, job: str | None = None, lang: str | None = None):
        super().__init__()
        self.lang = ui_lang(lang)
        self.L = LABELS[self.lang]
        self._file, self._job = file or "", job or ""

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal():
            yield ResumeTree(Path.cwd(), id="tree")
            with Vertical(id="main"):
                yield Label(self.L["file"], classes="field")
                yield Input(self._file, placeholder="cv.pdf", id="file")
                yield Label(self.L["job"], classes="field")
                yield TextArea(self._job, id="job", soft_wrap=True)
                with Horizontal(id="actions"):
                    yield Button(self.L["check"], id="check", variant="primary")
                    yield Select([(n, n) for n in sorted(TEMPLATES)], value="classic", allow_blank=False,
                                 id="template")
                    yield Button(self.L["export"], id="export")
                with Horizontal(id="score-row"):
                    yield ProgressBar(total=100, show_eta=False, id="score")
                    yield Static("", id="band")
                with TabbedContent():
                    with TabPane(self.L["ats"], id="tab-ats"):
                        yield VerticalScroll(Static(self.L["pick"], id="ats"))
                    with TabPane(self.L["style"], id="tab-style"):
                        yield VerticalScroll(Static("", id="style"))
                    with TabPane(self.L["keywords"], id="tab-keywords"):
                        yield VerticalScroll(Static(self.L["no_job"], id="keywords"))
        yield Footer()

    def on_mount(self) -> None:
        if self._file:
            self.action_check()

    # --- events -------------------------------------------------------------

    @on(DirectoryTree.FileSelected)
    def _picked(self, event: DirectoryTree.FileSelected) -> None:
        self.query_one("#file", Input).value = str(event.path)
        self.action_check()

    @on(Input.Submitted, "#file")
    @on(Button.Pressed, "#check")
    def _check_clicked(self) -> None:
        self.action_check()

    @on(Button.Pressed, "#export")
    def _export_clicked(self) -> None:
        self.action_export()

    @on(TextArea.Changed, "#job")
    def _job_changed(self) -> None:
        # Debounce: re-check 0.6 s after the user stops typing, not on every keystroke.
        if getattr(self, "_debounce", None):
            self._debounce.stop()
        self._debounce = self.set_timer(0.6, self.action_check)

    # --- actions ------------------------------------------------------------

    def _path(self) -> Path | None:
        path = Path(self.query_one("#file", Input).value.strip()).expanduser()
        return path if path.is_file() and path.suffix.lower() in SUPPORTED else None

    def action_toggle_tree(self) -> None:
        tree = self.query_one("#tree")
        tree.display = not tree.display

    def action_check(self) -> None:
        path = self._path()
        if path is None:
            self.query_one("#ats", Static).update(self.L["pick"])
            return
        self.query_one("#export", Button).label = self.L["export" if path.suffix == ".json" else "import"]
        self._run(str(path), self.query_one("#job", TextArea).text.strip() or None)

    @work(thread=True, exclusive=True)
    def _run(self, path: str, job: str | None) -> None:
        try:
            report = run_check(path, job, loaded=_cached_load(path, Path(path).stat().st_mtime))
        except Exception as e:  # unreadable/corrupt file: show it instead of crashing the app
            self.call_from_thread(self.notify, str(e), title="Error", severity="error")
            return
        self.call_from_thread(self._show, report)

    def _show(self, report: dict) -> None:
        L = self.L
        self.query_one("#ats", Static).update(
            "\n".join(f"{ICONS[i['level']]} {i['msg']}" for i in report["ats_file"]))

        findings = report["deslop"]["slop_findings"]
        self.query_one("#style", Static).update(
            "\n".join(f"[yellow]![/] [dim]{f['location']}[/]  [b]{f['found']}[/] → {f['suggest']}" for f in findings)
            or f"{ICONS['ok']} {L['clean']}")
        self.query_one(TabbedContent).get_tab("tab-style").label = f"{L['style']} ({len(findings)})"

        cov = report.get("coverage")
        bar, band = self.query_one("#score", ProgressBar), self.query_one("#band", Static)
        if cov is None:
            bar.update(progress=0)
            band.update("")
            self.query_one("#keywords", Static).update(L["no_job"])
            return
        bar.update(progress=cov["estimated_score_pct"])
        color = {"strong": "green", "moderate": "yellow", "weak": "red"}[cov["band"]]
        band.update(f"[{color}]{cov['estimated_score_pct']}% {cov['band']}[/]")
        lines = [f"[dim]{L['estimate']}[/]", ""]
        lines += [f"{k.removesuffix('_pct').replace('_', ' ')}: {v}%" for k, v in cov["components"].items()]
        for key, label in (("missing_required_keywords", "missing_req"), ("missing_preferred_keywords", "missing_pref")):
            if cov[key]:
                lines += ["", f"[b]{L[label]}[/] ({len(cov[key])})", ", ".join(cov[key])]
        self.query_one("#keywords", Static).update("\n".join(lines))

    def action_export(self) -> None:
        path = self._path()
        if path is None:
            self.notify(self.L["pick"], severity="warning")
            return
        if path.suffix == ".json":
            template = str(self.query_one("#template", Select).value)
            out = path.with_name(f"{path.stem}-{template}.pdf")
            render(_cached_load(str(path), path.stat().st_mtime)[1], out, template=template)
        else:
            out = path.with_suffix(".json")
            if out.exists():
                self.notify(f"{out.name} already exists", severity="warning")
                return
            out.write_text(json.dumps(import_resume(path), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            self.query_one("#tree", DirectoryTree).reload()
        self.notify(str(out), title="✓")


def run(file: str | None = None, job: str | None = None, lang: str | None = None) -> int:
    ResumeApp(file, job, lang).run()
    return 0
