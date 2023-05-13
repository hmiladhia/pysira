import json
from abc import ABC, abstractmethod

from pysira import EXTRA_DIR, LANGUAGE_DIR
from pysira.json_resume import Resume


class ExporterBase(ABC):
    @staticmethod
    def get_language_data(language: str):
        language_path = LANGUAGE_DIR / f'{language}.json'
        return json.loads(language_path.read_text())

    @abstractmethod
    def render(
        self, resume: Resume, path: str, format: str, language=None, options=None
    ) -> None:
        ...

    @staticmethod
    def get_extra_data(type: str):
        extra_path = EXTRA_DIR / type

        extra = {}

        for file in extra_path.glob('**/*.json'):
            current_ctx = extra
            keys = file.relative_to(extra_path).with_suffix('').as_posix().split('/')
            for key in keys:
                current_ctx = current_ctx.setdefault(key, {})

            current_ctx.update(json.loads(file.read_text()))

        return extra
