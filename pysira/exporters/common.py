from datetime import datetime


def parse_date(date: str, format=r'%Y-%m-%d') -> datetime:
    return datetime.strptime(date, format)
