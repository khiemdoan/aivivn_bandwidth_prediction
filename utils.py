from datetime import date, timedelta


def week_range(start_date: date, end_date: date, weekday=0):
    current_date = start_date
    while current_date < end_date:
        if current_date.weekday() == weekday:
            yield current_date
        current_date += timedelta(days=1)
