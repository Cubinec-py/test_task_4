import datetime


def last_day_of_month(year, month):
    next_month = month % 12 + 1
    year += month // 12
    last_day = datetime.date(year, next_month, 1) - datetime.timedelta(days=1)
    return last_day.day
