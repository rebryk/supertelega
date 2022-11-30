import datetime


def get_current_date():
    return datetime.datetime.now(tz=datetime.timezone.utc)
