from datetime import datetime
from typing import NamedTuple


class DateRange(NamedTuple):
    """
        W'll use this class to check if a resource is available for
        a given date.
        r1 = DateRange(start=datetime(2021, 9, 9), end=datetime(2021, 9, 11))
    """
    start: datetime
    end: datetime


def overlap(start_date_1, end_date1, start_date_2, end_date_2):
    """
        Return > 0 if the two date range overlap and 0 else
    """
    r1 = DateRange(start=start_date_1, end=end_date1)
    r2 = DateRange(start=start_date_2, end=end_date_2)

    latest_start = max(r1.start, r2.start)
    earliest_end = min(r1.end, r2.end)

    delta = (earliest_end - latest_start).days + 1
    overlap = max(0, delta)

    return overlap
