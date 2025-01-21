from pathlib import Path
from tempfile import TemporaryDirectory

import pytest
from click.testing import CliRunner

from pysira.__main__ import cli

example_resume = (Path(__file__).parents[1] / "examples/resume.json").resolve()
example_options = (Path(__file__).parents[1] / "examples/altacv_options.json").resolve()

TEX_FILES_LEN = 3


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


@pytest.fixture
def tmpdir() -> str:
    with TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.mark.parametrize(
    ("theme", "filename", "n_files"),
    [
        ("elegant", "index.html", 1),
        ("altaCV", "main.tex", TEX_FILES_LEN),
    ],
)
def test_coverage_cli_html(
    runner: CliRunner, tmpdir: str, theme: str, filename: str, n_files: int
) -> None:
    runner.invoke(cli, ["export", "-t", theme, "-o", tmpdir, str(example_resume)])

    files_list = {p.name for p in Path(tmpdir).iterdir()}

    assert len(files_list) == n_files, files_list
    assert filename in files_list


def test_coverage_options(runner: CliRunner, tmpdir: str) -> None:
    runner.invoke(
        cli,
        [
            "export",
            "-t",
            "altaCV",
            "-o",
            tmpdir,
            "-op",
            str(example_options),
            str(example_resume),
        ],
    )

    files_list = {p.name for p in Path(tmpdir).iterdir()}

    assert len(files_list) == TEX_FILES_LEN, files_list
    assert "main.tex" in files_list
