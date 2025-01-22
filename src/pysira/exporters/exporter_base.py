from __future__ import annotations

import json
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from pysira import EXTRA_DIR, LANGUAGE_DIR

if TYPE_CHECKING:
    from pysira.json_resume import Resume


class ExporterBase(ABC):
    @staticmethod
    def get_language_data(language: str) -> dict[str]:
        language_path = LANGUAGE_DIR / f"{language}.json"
        lang = json.loads(language_path.read_text())
        lang["id"] = language
        return lang

    @staticmethod
    def get_extra_data(type_: str) -> dict:
        extra_path = EXTRA_DIR / type_

        extra = {}

        for file in extra_path.glob("**/*.json"):
            current_ctx = extra
            keys = file.relative_to(extra_path).with_suffix("").as_posix().split("/")
            for key in keys:
                current_ctx = current_ctx.setdefault(key, {})

            current_ctx.update(json.loads(file.read_text()))

        return extra

    @abstractmethod
    def render(
        self,
        resume: Resume,
        path: str,
        format_: str,
        language: str | None = None,
        options: dict[str] | None = None,
    ) -> None: ...
