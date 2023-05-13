from __future__ import annotations

import re
import shutil
import subprocess
import tempfile
from pathlib import Path
from subprocess import PIPE
from typing import Any

from jinja2 import Environment, FileSystemLoader, select_autoescape

from pysira import TEMPLATES_DIR
from pysira.exporters.common import parse_date
from pysira.exporters.exporter_base import ExporterBase
from pysira.json_resume import Resume

_CONV = {
    '&': r'\&',
    '%': r'\%',
    '$': r'\$',
    '#': r'\#',
    '_': r'\_',
    '{': r'\{',
    '}': r'\}',
    '~': r'\textasciitilde{}',
    '^': r'\^{}',
    '\\': r'\textbackslash{}',
    '<': r'\textless{}',
    '>': r'\textgreater{}',
}
_ESCAPE_REGEX = re.compile(
    '|'.join(re.escape(key) for key in sorted(_CONV, key=lambda i: -len(i)))
)


class LatexExporter(ExporterBase):
    EXT = 'tex'

    def __init__(self, config: dict):
        self.config = config
        self.theme_path = Path(config['theme_path']).resolve()
        self.static_files = [self.theme_path / p for p in self.config.get('static', [])]

        template_path = config.get('template', 'main.tex')

        env = Environment(
            block_start_string=r'\BLOCK{',
            block_end_string='}',
            variable_start_string=r'\VAR{',
            variable_end_string='}',
            comment_start_string=r'\#{',
            comment_end_string='}',
            line_statement_prefix='%!!',
            line_comment_prefix='%#',
            trim_blocks=True,
            loader=FileSystemLoader([str(self.theme_path), str(TEMPLATES_DIR / 'tex')]),
            autoescape=select_autoescape(),
        )

        env.filters['regex_replace'] = regex_replace
        env.filters['escape'] = tex_escape
        env.filters['parse_date'] = parse_date

        self.template = env.get_template(template_path)

    def render(
        self, resume: Resume, path: str, format: str, language=None, options=None
    ):
        effective_options = self.config.get('default_options', {}).copy()
        effective_options.update(options or {})

        format = self.EXT if format is None else format.lower()

        if format in {'latex', 'tex'}:
            return self._render(resume, path, language, options=effective_options)

        if not format.startswith('pdf'):
            raise ValueError(f'Unsupported Format: {format}')

        with tempfile.TemporaryDirectory() as temp_dir:
            tex_file = Path(temp_dir) / 'main.tex'
            self._render(resume, str(tex_file), language, options=effective_options)

            subprocess.run(
                ['pdflatex', str(tex_file)], cwd=temp_dir, stdout=PIPE, timeout=15
            )
            pdf = (Path(temp_dir) / f'{tex_file.stem}.pdf').read_bytes()

            Path(path).write_bytes(pdf)

    def _render(
        self,
        resume: Resume,
        path: str,
        language: str = None,
        options: dict[str, Any] = None,
    ):
        language = self.get_language_data(language or resume.language)
        extra = self.get_extra_data(self.EXT)
        resume_dict = resume.dict

        image_path = resume_dict.get('basics', {}).get('image_path', [])
        if image_path:
            image_path = [Path(image_path)]

        # Create Path
        target_path = Path(path)
        if target_path.is_dir() or target_path.suffix.lower() != '.tex':
            target_path = target_path / self.config.get('default_name', 'main.tex')

        target_path.parent.mkdir(exist_ok=True)
        for file in self.static_files + image_path:
            if file.is_dir():
                shutil.copytree(str(file), str(target_path.parent / file.name))
            else:
                shutil.copy(str(file), str(target_path.parent))

        latex = self.template.render(
            **resume_dict, language=language, options=options, extra=extra
        )
        target_path.write_text(latex)


# Custom filter methods
def regex_replace(s, find, replace):
    return re.sub(find, replace, s)


def tex_escape(text):
    """
    :param text: a plain text message
    :return: the message escaped to appear correctly in LaTeX
    """
    if not isinstance(text, str):
        return text

    return _ESCAPE_REGEX.sub(lambda match: _CONV[match.group()], text)
