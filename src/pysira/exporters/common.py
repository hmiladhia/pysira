from __future__ import annotations

from datetime import datetime


def parse_date(date: str, format_: str = r"%Y-%m-%d") -> datetime:
    return datetime.strptime(date, format_)


def append(s: set | list, element: str, unique: bool = False) -> set | list:
    if unique:
        s = set(s)
        s.add(element)
    else:
        s = list(s)
        s.append(element)
    return s
