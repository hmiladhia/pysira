from __future__ import annotations

from datetime import datetime


def parse_date(date: str, format=r'%Y-%m-%d') -> datetime:
    return datetime.strptime(date, format)


def append(s: set | list, element, unique=False):
    if unique:
        s = set(s)
        s.add(element)
    else:
        s = list(s)
        s.append(element)
    return s
