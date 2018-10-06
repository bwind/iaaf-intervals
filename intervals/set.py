from dataclasses import dataclass
from typing import List

from intervals.repetition import Repetition
from intervals.utils import parse_time, safe_int, to_time


@dataclass
class Set:
    repeats: int
    repetitions: List[Repetition]
    recovery: int

    def __init__(self, repeats, repetitions, recovery):
        self.repeats = safe_int(repeats)
        self.repetitions = repetitions
        self.recovery = parse_time(recovery)

    def dump(self):
        retval = ' '.join([rep.dump() for rep in self.repetitions])
        if not all([rep.recovery is not None for rep in self.repetitions]):
            retval = '{%s}' % retval
        if self.repeats > 1:
            retval = ('%d x ' % self.repeats) + retval
        if self.recovery:
            retval += ' [%s]' % to_time(self.recovery)
        return retval

    def get_total_distance(self):
        return self.repeats * sum([
            rep.get_total_distance() for rep in self.repetitions])
