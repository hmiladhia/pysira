from pathlib import Path
from tempfile import TemporaryDirectory

import pytest
from click.testing import CliRunner

from pysira.__main__ import cli

example_resume = (Path(__file__).parents[1] / 'examples/resume.json').resolve()


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def tmpdir():
    with TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.mark.parametrize(
    'theme,filename,n_files',
    [
        ('elegant', 'index.html', 1),
        ('altaCV', 'main.tex', 2),
    ],
)
def test_coverage_cli_html(runner, tmpdir, theme, filename, n_files):
    runner.invoke(cli, ['export', '-t', theme, '-o', tmpdir, str(example_resume)])

    files_list = {p.name for p in Path(tmpdir).iterdir()}

    assert len(files_list) == n_files, files_list
    assert filename in files_list
