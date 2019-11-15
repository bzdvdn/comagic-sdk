import pytz
from datetime import datetime


def parse_datetime(s):
    if not s:
        return None
    return datetime.strptime(s, '%Y-%m-%d %H:%M:%S')
