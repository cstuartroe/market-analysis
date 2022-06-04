from datetime import date
from typing import Optional


def _get_quarter_name(start_date: date):
    quarter_number = (start_date.month + 2)//3
    return f"Q{quarter_number} {start_date.year}"


def _next_quarter_start(d: date):
    day = 1
    month = (int((d.month - 1)/3)*3 + 4) % 12
    year = (d.year + 1) if month == 1 else d.year

    return date(year, month, day)


def get_quarters(start_date: date, end_date: Optional[date] = None):
    if end_date is None:
        end_date = date.today()

    qstart = _next_quarter_start(start_date)
    qend = _next_quarter_start(qstart)

    while qend <= end_date:
        yield qstart, qend, _get_quarter_name(qstart)

        qstart, qend = qend, _next_quarter_start(qend)
