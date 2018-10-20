import random
from typing import Any, Sequence


def visualize_control_chars(s: str) -> str:
    """
    Format a string to remove all literals, replacing them with their unicode
    pictoral symbol equivalent
    :param s: string to substitute
    :return: substituted string
    """
    r = {
        '\x00': '␀',  # null
        '\x01': '␁',  # Start of Heading
        '\x02': '␂',  # Start of Text
        '\x03': '␃',  # End of Text
        '\x04': '␄',  # End of Transmission
        '\x05': '␅',  # Equiry
        '\x06': '␆',  # Acknowledge
        '\x07': '␇',  # Bell
        '\x08': '␈',  # Backspace
        '\x09': '␉',  # Horizontal Tab
        '\x0a': '␊',  # Line Feed
        '\x0b': '␋',  # Vertical Tab
        '\x0c': '␌',  # Form Feed
        '\x0d': '␍',  # Carriage Return
        '\x0e': '␎',  # Shift Out
        '\x0f': '␏',  # Shift In
        '\x10': '␐',  # Data link Escape
        '\x11': '␑',  # Device Control 1
        '\x12': '␒',  # Device Control 2
        '\x13': '␓',  # Device Control 3
        '\x14': '␔',  # Device Control 4
        '\x15': '␕',  # Negative Acknowledge
        '\x16': '␖',  # Synchronous Idle
        '\x17': '␗',  # End of Transmission Block
        '\x18': ' ',  # Cancel
        '\x19': '␙',  # End of Medium
        '\x1a': '␚',  # Substitute
        '\x1b': '␛',  # Escape
        '\x1c': '␜',  # File Separator
        '\x1d': '␝',  # Group Separator
        '\x1e': '␞',  # Record Separator
        '\x1f': '␟',  # Unit Separator

        # other
        '\x20': '␠',  # it's a space...
        '\x7f': '␡',  # Delete
    }

    rs = ''
    for i in s:
        try:
            rs += r[i]
        except KeyError:
            rs += i

    return rs


# TODO: Further constrain types?
def weighted_choice(tuple_list: Sequence[Sequence[Any]]) -> Any:
    """
    Makes a weighted selection from a list of tuples
    :param tuple_list: List of n-tuples, of the form [(weight, ...), ...]
    :return: Slice [1:] of randomly selected list element
    """
    total = sum([x[0] for x in tuple_list])
    interval_tuples = [tuple((x[0] / total, n)) for n, x in
                       enumerate(tuple_list)]

    choice = random.random()
    choice -= interval_tuples[0][0]
    while choice > 0:
        interval_tuples = interval_tuples[1:]
        choice -= interval_tuples[0][0]
    return tuple_list[interval_tuples[0][1]][1:]
