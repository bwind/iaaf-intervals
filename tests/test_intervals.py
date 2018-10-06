import re

from intervals import load
from intervals.regex import (
    GROUPED_SETS_REGEX,
    SETS_REGEX,
    REPETITION_REGEX,
)
from intervals.repetition import Repetition
from intervals.set import Set
from intervals.utils import parse_time, to_time


class TestUtils:
    def test_parse_time_minutes(self):
        assert parse_time('12’') == 720

    def test_parse_time_seconds(self):
        assert parse_time('30”') == 30

    def test_parse_time_none(self):
        assert parse_time(None) is None

    def test_to_time_string(self):
        assert to_time('max') == 'max'

    def test_to_time_minutes_and_seconds(self):
        assert to_time(90) == '1’30”'

    def test_to_time_seconds(self):
        assert to_time(30) == '30”'

    def test_to_time_minutes(self):
        assert to_time(120) == '2’'


class TestIntervals:
    def setup(self):
        self.repetition_minimal = '1 x 300 (max)'
        self.repetition_with_recovery = '10 x 400 (72”) [2’]'
        self.multiple_repetitions = '2 x 500 (300/48”, 200/max) [8’] [15’] 8 x 200 (35”) [1’]'  # noqa: E501
        self.grouped_sets = '2 x {1 x 500 (1500) [1’] 1 x 700 (1500) [30”] 1 x 300 (max)} [12’]'  # noqa: E501
        self.sets = '3 x 4 x 300 (3000) [100m r/o & 5’]'

    def test_regex_repetition_minimal(self):
        match = re.match(REPETITION_REGEX, self.repetition_minimal)
        assert match.group(1) == '1'
        assert match.group(2) == '300'
        assert match.group(3) == 'max'
        assert match.group(4) is None

    def test_regex_repetition_with_recovery(self):
        match = re.match(REPETITION_REGEX, self.repetition_with_recovery)
        assert match.group(1) == '10'
        assert match.group(2) == '400'
        assert match.group(3) == '72”'
        assert match.group(4) == '2’'

    def test_regex_multiple_repetitions_has_recovery_between_sets(self):
        match = re.findall(REPETITION_REGEX, self.multiple_repetitions)
        assert match[0][5] == '15’'

    def test_regex_grouped_sets(self):
        match = re.match(GROUPED_SETS_REGEX, self.grouped_sets)
        assert match.group(1) == '2'
        assert match.group(2) == '1 x 500 (1500) [1’] 1 x 700 (1500) [30”] 1 x 300 (max)'  # noqa: E501
        assert match.group(3) == '12’'

    def test_sets_has_repeats(self):
        match = re.match(SETS_REGEX, self.sets)
        assert match.group(1) == '3'
        assert match.group(2) == '4 x 300 (3000) [100m r/o & 5’]'

    def test_load_repetition_minimal(self):
        assert load(self.repetition_minimal) == Set(
            repeats=1,
            repetitions=[
                Repetition(
                    repeats=1,
                    distance=300,
                    pace='max',
                    recovery=None,
                ),
            ],
            recovery=None)

    def test_load_repetition_with_recovery(self):
        assert load(self.repetition_with_recovery) == Set(
            repeats=1,
            repetitions=[
                Repetition(
                    repeats=10,
                    distance=400,
                    pace=72,
                    recovery=120,
                ),
            ],
            recovery=None)

    def test_load_multiple_repetitions(self):
        assert load(self.multiple_repetitions) == Set(
            repeats=1,
            repetitions=[
                Repetition(
                    repeats=2,
                    distance=500,
                    pace='300/48”, 200/max',
                    recovery=480,
                ),
                Repetition(
                    repeats=8,
                    distance=200,
                    pace=35,
                    recovery=60,
                ),
            ],
            recovery=900)

    def test_load_grouped_sets(self):
        assert load(self.grouped_sets) == Set(
            repeats=1,
            repetitions=[
                Repetition(
                    repeats=1,
                    distance=500,
                    pace='1500',
                    recovery=60,
                ),
                Repetition(
                    repeats=1,
                    distance=700,
                    pace='1500',
                    recovery=30,
                ),
                Repetition(
                    repeats=1,
                    distance=300,
                    pace='max',
                    recovery=None,
                )
            ],
            recovery=720)

    def test_load_sets(self):
        '3 x 4 x 300 (3000) [100m r/o & 5’]'
        assert load(self.sets) == Set(
            repeats='3',
            repetitions=[
                Repetition(
                    repeats=4,
                    distance=300,
                    pace='3000',
                    recovery='100m r/o',
                ),
            ],
            recovery=300)
