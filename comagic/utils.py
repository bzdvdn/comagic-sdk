import pytz
from datetime import datetime

DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'


def parse_datetime(s):
    if not s:
        return None
    return datetime.strptime(s, DATETIME_FORMAT)
