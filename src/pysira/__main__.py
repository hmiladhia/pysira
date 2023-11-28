from __future__ import annotations

import json
from pathlib import Path

import click

from pysira.exporters import ExportFactory
from pysira.json_resume import Resume


@click.group()
def cli() -> None:
    pass


@cli.command()
@click.argument("resume_path", required=False, default="resume.json")
@click.option("--output", "-o", type=str, default="out")
@click.option("--theme", "-t", type=str, default="base")
@click.option("--language", "-l", type=str, default=None)
@click.option("--options", "-op", type=str, default=None)
@click.option("--format", "-f", "format_", type=str, default=None)
@click.option("--work", "-w", type=int, default=None)
@click.option("--projects", "-p", type=int, default=None)
@click.option("--skills", "-s", type=int, default=None)
@click.option("--certificates", "-c", type=int, default=None)
@click.option(
    "--summary/--no-summary",
    "--about/--no-about",
    "-a/-na",
    type=bool,
    default=True,
    is_flag=True,
)
@click.option("--yaml", "-y", type=bool, default=False, is_flag=True)
def export(
    resume_path: str,
    output: str,
    theme: str,
    format_: str,
    work: int,
    projects: int,
    skills: int,
    certificates: int,
    summary: bool,
    yaml: bool,
    language: str,
    options: str,
) -> None:
    resume = Resume.from_yaml(resume_path) if yaml else Resume.from_json(resume_path)
    resume = resume.abbreviate(work, projects, skills, certificates, summary=summary)

    factory = ExportFactory(theme)
    exp = factory.build()

    options_dict: dict[str] | None = None
    if options:
        options_path = Path(options)
        options_dict = json.loads(options_path.read_text())
        options_dict["static"] = [
            Path(p) if Path(p).is_absolute() else options_path.parent / p
            for p in options_dict.pop("static", [])
        ]

    exp.render(resume, output, format_, language=language, options=options_dict)


if __name__ == "__main__":
    cli()
