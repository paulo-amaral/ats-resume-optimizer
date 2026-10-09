import asyncio
import shutil
from importlib import resources

import pytest

pytest.importorskip("textual")

from textual.widgets import Static, TextArea  # noqa: E402

from ats_resume.tui import ResumeApp  # noqa: E402


async def until(pilot, condition, timeout=10.0):
    # DirectoryTree keeps a loader worker alive, so workers.wait_for_complete() would never return.
    for _ in range(int(timeout / 0.1)):
        if condition():
            return
        await pilot.pause(0.1)
    raise AssertionError("condition not met in time")


def test_tui_checks_file_scores_job_and_exports(tmp_path, monkeypatch):
    src = resources.files("ats_resume") / "data" / "example-en.json"
    resume = tmp_path / "resume.json"
    with resources.as_file(src) as p:
        shutil.copyfile(p, resume)
    monkeypatch.chdir(tmp_path)

    async def scenario():
        app = ResumeApp(str(resume), lang="en")
        async with app.run_test(size=(140, 45)) as pilot:
            await until(pilot, lambda: "structure is valid" in str(app.query_one("#ats", Static).render()))

            app.query_one("#job", TextArea).text = "Requirements: Python, Kafka, Rust"
            # debounce (0.6 s) fires the re-check in a thread worker
            await until(pilot, lambda: "rust" in str(app.query_one("#keywords", Static).render()))

            await pilot.press("ctrl+e")
            await until(pilot, (tmp_path / "resume-classic.pdf").exists)

    asyncio.run(scenario())
