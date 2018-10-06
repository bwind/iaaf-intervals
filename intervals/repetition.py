from dataclasses import dataclass

from intervals.utils import parse_time, safe_int, to_time


@dataclass
class Repetition:
    repeats: int
    distance: int
    pace: str
    recovery: int

    def __init__(self, repeats, distance, pace, recovery):
        self.repeats = safe_int(repeats)
        self.distance = safe_int(distance)
        self.pace = parse_time(pace)
        self.recovery = parse_time(recovery)

    def dump(self):
        retval = '%d x %s (%s)' % (
            self.repeats, self.distance, to_time(self.pace))
        if self.recovery:
            retval += ' [%s]' % to_time(self.recovery)
        return retval

    def get_total_distance(self):
        return self.repeats * self.distance
