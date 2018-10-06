import re

from intervals.regex import (
    GROUPED_SETS_REGEX,
    SETS_REGEX,
    REPETITION_REGEX,
)
from intervals.repetition import Repetition
from intervals.set import Set
from intervals.utils import parse_time, safe_int


def load(s):
    match = re.match(GROUPED_SETS_REGEX, s)
    if match is not None:
        repeats, sets, recovery_between_sets = match.groups()
        set = _load_set(sets)
        set.repeats = safe_int(repeats)
        set.recovery = parse_time(recovery_between_sets)
    else:
        # Not a grouped set. Try to load as regular set.
        set = _load_set(s)
        if set is None:
            # Not a set. Try to load as repetitions.
            set = _load_repetitions_set(s)
    return set


def dump(s):
    return s.dump()


def _load_repetitions_set(s, repeats=None):
    match = re.findall(REPETITION_REGEX, s)
    recovery_between_sets = match[0][4] or match[0][5] or None
    if match is not None:
        return Set(
            repeats=repeats or 1,
            repetitions=_load_repetitions_from_match(match),
            recovery=recovery_between_sets)


def _load_repetitions_from_match(match):
    return [Repetition(
        repeats=rep[0],
        distance=rep[1],
        pace=rep[2],
        recovery=rep[3] or None) for rep in match]


def _load_set(s):
    match = re.match(SETS_REGEX, s)
    repeats, repetitions = match.groups()
    return _load_repetitions_set(repetitions, repeats=repeats)
