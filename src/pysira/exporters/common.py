from __future__ import annotations
from typing import Any

from datetime import datetime


def parse_date(date: str, format_: str = r"%Y-%m-%d") -> datetime:
    return datetime.strptime(date, format_)  # noqa: DTZ007


def append(s: set | list, element: Any, unique: bool = False) -> set | list:
    if unique:
        s = set(s)
        s.add(element)
    else:
        s = list(s)
        s.append(element)
    return s
