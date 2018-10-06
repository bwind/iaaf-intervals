from intervals.regex import SINGLE_QUOTE, DOUBLE_QUOTE

import re


def safe_int(s):
    try:
        return int(s)
    except (ValueError, TypeError):
        return s


def parse_time(s):
    if not isinstance(s, (str, bytes)):
        return s
    seconds = re.match(r'(\d+)' + DOUBLE_QUOTE, s)
    if seconds is not None:
        return int(seconds.group(1))
    minutes = re.match(r'(\d+)' + SINGLE_QUOTE, s)
    if minutes is not None:
        return int(minutes.group(1)) * 60
    return s


def to_time(s):
    if not isinstance(s, int):
        return s
    if s % 60 == 0:
        return '%s’' % (s // 60)
    return '%d”' % s
