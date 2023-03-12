import json
from abc import ABC, abstractmethod

from pysira import LANGUAGE_DIR
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
