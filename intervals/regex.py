DOUBLE_QUOTE = '[”|"]'
SINGLE_QUOTE = "[’|']"

SETS = r'(?:(\d+)\s*x\s*)?'
REPEATS = r'(\d+)\s*x\s*'
DISTANCE = r'(\d+)\s*'
PACE_OR_INTENSITY = r'\((.*?)\)\s*'
RECOVERY_BETWEEN_REPETITIONS_AND_OR_SETS = \
    r'(?:\[(.*?)(?:\s*&\s*(.*?))?\]\s*)?'
RECOVERY_BETWEEN_SETS = r'(?:\[(.*?)\])?'


GROUPED_SETS_REGEX = r'(\d+)\s*x\s*\{(.*?)\}\s*\[(.*?)\]'

SETS_REGEX = SETS + r'(\d+\s*x\s*.*)'

REPETITION_REGEX = (
    REPEATS +
    DISTANCE +
    PACE_OR_INTENSITY +
    RECOVERY_BETWEEN_REPETITIONS_AND_OR_SETS +
    RECOVERY_BETWEEN_SETS)
