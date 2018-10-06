# IAAF Intervals

This library provides serialization and unserialization of interval notations
using the IAAF Standard Representation of Running Training for Python 3.6+.

## Usage

    >>> import intervals
    >>> set = intervals.load('2 x 6 x 400 (72”) [2’]')
    >>> set
    Set(repeats=2, repetitions=[Repetition(repeats=6, distance=400, pace=72, recovery=120)], recovery=None)
    >>> set.get_total_distance()
    4800
    >>> intervals.dump(set)
    2 x 6 x 400 (72”) [2’]

## Spec

sets x repetitions x distance (intensity/pace) [recovery between reps,
then recovery between sets]

For the original spec, see http://www.newintervaltraining.com/iaaf-standardised-sessions-www-newintervaltraining-com.pdf.
