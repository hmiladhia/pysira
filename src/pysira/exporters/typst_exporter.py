from __future__ import annotations

import shutil
import tempfile
from pathlib import Path
from typing import TYPE_CHECKING

import yaml

from pysira.exporters.exporter_base import ExporterBase

if TYPE_CHECKING:
    from pysira.json_resume import Resume


class TypstExporter(ExporterBase):
    EXT = "typ"

    def __init__(self, config: dict) -> None:
        self.config = config
        self.theme_path = Path(config["theme_path"]).resolve()
        self.static_files = [self.theme_path / p for p in self.config.get("static", [])]

    def render(
        self,
        resume: Resume,
        path: str,
        format_: str,
        language: str | None = None,
        options: dict[str] | None = None,
    ) -> None:
        import typst

        effective_options = self.config.get("default_options", {}).copy()
        effective_options.update(options or {})

        format_ = "pdf" if format_ is None else format_.lower()

        if not format_.startswith("pdf"):
            raise ValueError(f"Unsupported Format: {format_}")

        if Path(path).is_dir():
            path = str(Path(path) / self.config.get("default_name", "resume.pdf"))

        with tempfile.TemporaryDirectory() as temp_dir:
            main_file = self._prepare(resume, temp_dir, language, effective_options)
            typst.compile(main_file, output=path, format="pdf")

    def _prepare(
        self,
        resume: Resume,
        path: str,
        language: str | None = None,
        options: dict[str] | None = None,
    ) -> str:
        options = options or {}
        additional_paths = [Path(p) for p in options.pop("static", [])]
        language = self.get_language_data(language or resume.language)
        extra = self.get_extra_data(self.EXT)

        resume_dict = resume.dict

        image_path = resume_dict.get("basics", {}).get("image_path")
        if image_path:
            additional_paths.append(Path(image_path))

        # Create Path
        target_path = Path(path)
        if target_path.is_dir() or target_path.suffix.lower() != ".typ":
            target_path = target_path / self.config.get("template", "main.typ")

        target_path.parent.mkdir(exist_ok=True)
        template_files = list(Path(self.theme_path).glob("*"))
        for file in template_files + self.static_files + additional_paths:
            if file.is_dir():
                shutil.copytree(str(file), str(target_path.parent / file.name))
            else:
                shutil.copy(str(file), str(target_path.parent))

        _export_yaml(
            target_path.parent,
            resume=resume_dict,
            language=language,
            options=options,
            extra=extra,
        )

        return target_path.as_posix()


def _export_yaml(path: Path | str, **dicts: dict) -> None:
    path = Path(path)
    for name, value in dicts.items():
        with path.joinpath(f"{name}.yaml").open("w") as f:
            yaml.dump(value, f)
