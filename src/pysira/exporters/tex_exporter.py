from __future__ import annotations

import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path
from subprocess import PIPE
from typing import TYPE_CHECKING

from jinja2 import Environment, FileSystemLoader, select_autoescape

from pysira import TEMPLATES_DIR, LANGUAGE_OVERRIDES_KEY
from pysira.exporters.common import append, parse_date
from pysira.exporters.exporter_base import ExporterBase

if TYPE_CHECKING:
    from pysira.json_resume import Resume

_CONV = {
    "&": r"\&",
    "%": r"\%",
    "$": r"\$",
    "#": r"\#",
    "_": r"\_",
    "{": r"\{",
    "}": r"\}",
    "~": r"\textasciitilde{}",
    "^": r"\^{}",
    "\\": r"\textbackslash{}",
    "<": r"\textless{}",
    ">": r"\textgreater{}",
}
_ESCAPE_REGEX = re.compile(
    "|".join(re.escape(key) for key in sorted(_CONV, key=lambda i: -len(i)))
)


class LatexExporter(ExporterBase):
    EXT = "tex"

    def __init__(self, config: dict) -> None:
        self.config = config
        self.theme_path = Path(config["theme_path"]).resolve()
        self.static_files = [self.theme_path / p for p in self.config.get("static", [])]

        template_path = config.get("template", "main.tex")
        secondary_templates_paths = config.get("secondary_templates", [])

        env = Environment(
            block_start_string=r"\BLOCK{",
            block_end_string="}",
            variable_start_string=r"\VAR{",
            variable_end_string="}",
            comment_start_string=r"\#{",
            comment_end_string="}",
            line_statement_prefix="%!!",
            line_comment_prefix="%#",
            trim_blocks=True,
            loader=FileSystemLoader([str(self.theme_path), str(TEMPLATES_DIR / "tex")]),
            autoescape=select_autoescape(),
        )

        env.filters["regex_replace"] = regex_replace
        env.filters["escape"] = tex_escape
        env.filters["parse_date"] = parse_date
        env.filters["append"] = append

        self.template = env.get_template(template_path)
        self.secondary_templates = {
            path: env.get_template(path) for path in secondary_templates_paths
        }

    def render(
        self,
        resume: Resume,
        path: str,
        format_: str,
        language: str | None = None,
        options: dict[str] | None = None,
    ) -> None:
        effective_options = self.config.get("default_options", {}).copy()
        effective_options.update(options or {})

        format_ = self.EXT if format_ is None else format_.lower()

        if format_ in {"latex", "tex"}:
            return self._render(resume, path, language, options=effective_options)

        if not format_.startswith("pdf"):
            raise ValueError(f"Unsupported Format: {format_}")

        with tempfile.TemporaryDirectory() as temp_dir:
            tex_file_path = Path(temp_dir).joinpath("main.tex")
            tex_file_stem = tex_file_path.stem
            tex_file = tex_file_path.as_posix()

            params = {"cwd": temp_dir, "stdout": PIPE, "timeout": 15}

            self._render(resume, tex_file, language, options=effective_options)

            pdflatex_cmd = os.environ.get("PYSIRA_PDFLATEX_CMD", "pdflatex")
            biber_cmd = os.environ.get("PYSIRA_BIBER_CMD", "biber")

            subprocess.run([pdflatex_cmd, tex_file], check=False, **params)
            if resume.resume.publications:
                subprocess.run([biber_cmd, tex_file_stem], check=False, **params)
                subprocess.run([pdflatex_cmd, tex_file], check=False, **params)
                subprocess.run([pdflatex_cmd, tex_file], check=False, **params)

            pdf = (Path(temp_dir) / f"{tex_file_stem}.pdf").read_bytes()

            Path(path).write_bytes(pdf)

    def _render(
        self,
        resume: Resume,
        path: str,
        language: str | None = None,
        options: dict[str] | None = None,
    ) -> None:
        options = options or {}
        additional_paths = [Path(p) for p in options.pop("static", [])]
        language = self.get_language_data(
            language or resume.language, options.get(LANGUAGE_OVERRIDES_KEY)
        )
        extra = self.get_extra_data(self.EXT)
        resume_dict = resume.dict

        image_path = resume_dict.get("basics", {}).get("image_path")
        if image_path:
            additional_paths.append(Path(image_path))

        # Create Path
        target_path = Path(path)
        if target_path.is_dir() or target_path.suffix.lower() != ".tex":
            target_path = target_path / self.config.get("default_name", "main.tex")

        target_path.parent.mkdir(exist_ok=True)
        for file in self.static_files + additional_paths:
            if file.is_dir():
                shutil.copytree(str(file), str(target_path.parent / file.name))
            else:
                shutil.copy(str(file), str(target_path.parent))

        latex = self.template.render(
            **resume_dict, language=language, options=options, extra=extra
        )
        target_path.write_text(latex, encoding="utf-8")

        for sec_path, template in self.secondary_templates.items():
            latex = template.render(
                **resume_dict, language=language, options=options, extra=extra
            )
            target_path.parent.joinpath(sec_path).write_text(latex, encoding="utf-8")


# Custom filter methods
def regex_replace(s: str, find: str, replace: str) -> str:
    return re.sub(find, replace, s)


def tex_escape(text: str) -> str:
    """
    Escape special characters.

    :param text: a plain text message
    :return: the message escaped to appear correctly in LaTeX
    """
    if not isinstance(text, str):
        return text

    return _ESCAPE_REGEX.sub(lambda match: _CONV[match.group()], text)
