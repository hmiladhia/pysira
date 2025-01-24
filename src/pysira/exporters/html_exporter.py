from __future__ import annotations

import base64
import shutil
import tempfile
from mimetypes import guess_type
from pathlib import Path
from typing import TYPE_CHECKING

from jinja2 import Environment, FileSystemLoader, select_autoescape

from pysira import TEMPLATES_DIR, LANGUAGE_OVERRIDES_KEY
from pysira.exporters.common import append, parse_date
from pysira.exporters.exporter_base import ExporterBase

if TYPE_CHECKING:
    from pysira.json_resume import Resume


class HtmlExporter(ExporterBase):
    EXT = "html"

    def __init__(self, config: dict[str], template_path: str = "index.html") -> None:
        self.config = config
        self.theme_path = Path(config["theme_path"]).resolve()
        self.static_files = [self.theme_path / p for p in self.config.get("static", [])]

        template_path = config.get("template", "index.html")
        secondary_templates_paths = config.get("secondary_templates", [])

        env = Environment(
            loader=FileSystemLoader(
                [str(self.theme_path), str(TEMPLATES_DIR / "html")]
            ),
            autoescape=select_autoescape(),
        )

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

        if format_ == self.EXT:
            return self._render(resume, path, language, effective_options)

        if not format_.startswith("pdf"):
            raise ValueError(f"Unsupported Format: {format_}")

        _, *engine = format_.split("/", 1)
        engine = engine[0] if engine else "pypdf"

        if engine == "pypdf":
            self._render_pyppdf(resume, path, language, options)

        elif engine == "xhtml2pdf":
            self._render_xhtml2pdf(resume, path, language, options)

        elif engine == "pdfkit":
            self._render_pdfkit(resume, path, language, options)

        else:
            raise ValueError("Unsupported Engine")

    def _render(  # noqa: C901
        self,
        resume: Resume,
        path: str | Path,
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

        for img_key, impath in self.config.get("image_b64", {}).items():
            img_path = self.theme_path / impath
            extra_images = extra.setdefault("image_b64", {})
            image = extra_images.setdefault(img_key, {})
            image["bytes"] = base64.b64encode(img_path.read_bytes()).decode("ascii")
            image["type"] = guess_type(str(img_path))[0]

        # Create Path
        target_path = Path(path)
        if target_path.is_dir() or target_path.suffix.lower() != ".html":
            target_path = target_path / self.config.get("default_name", "index.html")

        target_path.parent.mkdir(exist_ok=True)
        for file in self.static_files + additional_paths:
            if file.is_dir():
                shutil.copytree(str(file), str(target_path.parent / file.name))
            else:
                shutil.copy(str(file), str(target_path.parent))

        if options.get("update_assets_url", False):
            resume_dict.setdefault("meta", {})["assets_url"] = str(target_path.parent)

        html = self.template.render(
            **resume_dict, language=language, options=options, extra=extra
        )
        target_path.write_text(html)
        for sec_path, template in self.secondary_templates.items():
            html = template.render(
                **resume_dict, language=language, options=options, extra=extra
            )
            target_path.parent.joinpath(sec_path).write_text(html)

    def _render_pyppdf(
        self,
        resume: Resume,
        path: str | Path,
        language: str | None = None,
        options: dict[str] | None = None,
    ) -> None:
        from pyppdf import save_pdf

        args_dict = {
            # "launch": {"args": ['--font-render-hinting=none']},
            "goto": {"waitUntil": "networkidle0", "timeout": 10000},
            "pdf": {
                "scale": 0.95,
                "format": "A4",
                "preferCSSPageSize": True,
                "printBackground": True,
                "margin": {"top": "0", "right": "0", "bottom": "0", "left": "0"},
            },
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            html_file = Path(temp_dir) / "resume.html"
            self._render(resume, str(html_file), language, options)
            save_pdf(path, str(html_file), args_dict=args_dict)

    def _render_xhtml2pdf(
        self,
        resume: Resume,
        path: str | Path,
        language: str | None = None,
        options: dict[str] | None = None,
    ) -> None:
        from xhtml2pdf import pisa

        with tempfile.TemporaryDirectory() as temp_dir:
            html_file = Path(temp_dir) / "resume.html"
            self._render(resume, str(html_file), language, options)

            # convert HTML to PDF
            with Path(path).open("w+b") as output_path:
                pisa.CreatePDF(
                    html_file.read_text(),  # the HTML to convert
                    dest=output_path,  # file handle to receive result
                    xhtml=False,
                    encoding="utf-8",
                )

    def _render_pdfkit(
        self,
        resume: Resume,
        path: str | Path,
        language: str | None = None,
        options: dict[str] | None = None,
    ) -> None:
        import pdfkit

        # https://wkhtmltopdf.org/usage/wkhtmltopdf.txt
        arg_options = {
            "dpi": 365,
            "page-size": "A4",
            "margin-right": "0.25in",
            "margin-bottom": "0.25in",
            "margin-top": "0.25in",
            "margin-left": "0.25in",
            "encoding": "UTF-8",
            # 'custom-header' : [
            #     ('Accept-Encoding', 'gzip')
            # ],
            # 'no-outline': None,
            # "enable-javascript": "",
            # "disable-javascript ": None,
            # "disable-javascript": "",
            # "javascript-delay": 1,
            "enable-local-file-access": "",
            # "viewport-size": "100"
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            html_file = Path(temp_dir) / "resume.html"
            self._render(resume, str(html_file), language, options)
            pdfkit.from_file(str(html_file), str(path), options=arg_options)
