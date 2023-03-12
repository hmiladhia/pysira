from __future__ import annotations

import base64
import json
from copy import deepcopy
from dataclasses import asdict
from mimetypes import guess_type
from pathlib import Path

from pysira.resume_data import ResumeData


def _dict_factory(d):
    return {k: v for k, v in dict(d).items() if v is not None}


class Resume:
    def __init__(self, resume: ResumeData, path=None):
        self.resume = resume
        self.path = Path(path or '.').resolve()
        self._set_image_extra()

    @property
    def dict(self):
        return asdict(self.resume, dict_factory=_dict_factory)

    @property
    def language(self):
        return self.resume.meta.language

    @staticmethod
    def from_json(path, encoding=None):
        resume_path = Path(path)
        json_content = resume_path.read_text(encoding=encoding)

        resume = ResumeData.from_dict(json.loads(json_content))

        return Resume(resume, resume_path.parent)

    @staticmethod
    def from_yaml(path, encoding=None):
        import yaml

        resume_path = Path(path)
        file_content = resume_path.read_text(encoding=encoding)

        resume = ResumeData.from_dict(yaml.safe_load(file_content))

        return Resume(resume, resume_path.parent)

    def _set_image_extra(self):
        if self.resume.basics.image is None:
            return

        image_path = self.path / self.resume.basics.image

        if not image_path.exists():
            return

        self.resume.basics.image_path = str(image_path)
        self.resume.basics.image_b64 = base64.b64encode(image_path.read_bytes()).decode(
            'ascii'
        )
        self.resume.basics.image_b64_mime_type = guess_type(str(image_path))[0]

    def abbreviate(
        self, work=None, projects=None, skills=None, certificates=None, summary=True
    ):
        resume = deepcopy(self.resume)

        if not summary:
            resume.basics.summary = None

        if work is not None:
            resume.work = resume.work[:work]

        if certificates is not None:
            resume.certificates = resume.certificates[:certificates]

        if projects is not None:
            resume.projects = resume.projects[:projects]

        if skills is not None:
            resume.skills = resume.skills[:skills]

        return Resume(resume, self.path)
